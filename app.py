"""SDA Property Screener - Team Server"""
from flask import Flask, request, session, redirect, url_for, jsonify, send_file, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import Template
import sqlite3, json, os, datetime, secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

DB = os.path.join(os.path.dirname(__file__), 'usage.db')
_DASHBOARD = None

def get_dashboard():
    global _DASHBOARD
    if _DASHBOARD is None:
        p = os.path.join(os.path.dirname(__file__), 'dashboard.html')
        if os.path.exists(p):
            with open(p) as f:
                _DASHBOARD = f.read()
    return _DASHBOARD or '<h1>Dashboard not found</h1>'

"""SDA Property Screener - Team Server"""
from flask import Flask, request, session, redirect, url_for, jsonify, send_file, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import Template
import sqlite3, json, os, datetime, secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

DB = os.path.join(os.path.dirname(__file__), 'usage.db')

def get_db():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'team',
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            login_at TEXT DEFAULT (datetime('now')),
            logout_at TEXT,
            last_active TEXT DEFAULT (datetime('now')),
            ip_address TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            event_data TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (session_id) REFERENCES sessions(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS shortlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            property_ids TEXT DEFAULT '[]',
            dd_data TEXT DEFAULT '{}',
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS property_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT UNIQUE NOT NULL,
            csv_data TEXT NOT NULL,
            row_count INTEGER DEFAULT 0,
            uploaded_by TEXT,
            uploaded_at TEXT DEFAULT (datetime('now'))
        );
    """)
    db.commit()
    existing = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if existing == 0:
        db.execute('INSERT INTO users (username,password_hash,full_name,role) VALUES (?,?,?,?)',
                   ('admin', generate_password_hash('admin123'), 'Administrator', 'admin'))
        db.commit()
    db.close()

init_db()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return redirect(url_for('login'))
        db = get_db()
        sess = db.execute(
            'SELECT s.*,u.username,u.full_name,u.role,u.active FROM sessions s '
            'JOIN users u ON s.user_id=u.id WHERE s.session_token=? AND s.logout_at IS NULL', (token,)
        ).fetchone()
        db.close()
        if not sess or not sess['active']:
            session.clear()
            return redirect(url_for('login'))
        db = get_db()
        db.execute('UPDATE sessions SET last_active=? WHERE session_token=?',
                   (datetime.datetime.utcnow().isoformat(), token))
        db.commit()
        db.close()
        request.current_user = dict(sess)
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if request.current_user.get('role') != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated

def log_event(event_type, event_data=None):
    token = session.get('token')
    if not token: return
    db = get_db()
    sess = db.execute('SELECT id,user_id FROM sessions WHERE session_token=?', (token,)).fetchone()
    if sess:
        db.execute('INSERT INTO events (session_id,user_id,event_type,event_data) VALUES (?,?,?,?)',
                   (sess['id'], sess['user_id'], event_type, json.dumps(event_data) if event_data else None))
        db.commit()
    db.close()

@app.route('/')
def index():
    if 'token' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username','').strip().lower()
        password = request.form.get('password','')
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username=? AND active=1', (username,)).fetchone()
        db.close()
        if user and check_password_hash(user['password_hash'], password):
            token = secrets.token_urlsafe(32)
            db = get_db()
            db.execute('INSERT INTO sessions (user_id,session_token,ip_address) VALUES (?,?,?)',
                       (user['id'], token, request.remote_addr))
            db.commit()
            db.close()
            session['token'] = token
            log_event('login', {'username': username})
            return redirect(url_for('dashboard'))
        error = 'Invalid username or password.'
    p = os.path.join(os.path.dirname(__file__), 'templates', 'login.html')
    login_html = open(p).read() if os.path.exists(p) else '<form method="POST"><input name="username"><input type="password" name="password"><button>Login</button></form>'
    return make_response(Template(login_html).render(error=error))

@app.route('/logout')
def logout():
    token = session.get('token')
    if token:
        log_event('logout')
        db = get_db()
        db.execute('UPDATE sessions SET logout_at=? WHERE session_token=?',
                   (datetime.datetime.utcnow().isoformat(), token))
        db.commit()
        db.close()
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    log_event('dashboard_view')
    return make_response(get_dashboard())

@app.route('/api/log', methods=['POST'])
@login_required
def api_log():
    data = request.get_json()
    if data and data.get('type'):
        log_event(data['type'], data.get('data'))
    return jsonify({'ok': True})

@app.route('/api/properties/<state>')
@login_required
def get_properties(state):
    if state not in ('vic','nsw','qld'):
        abort(400)
    db = get_db()
    row = db.execute('SELECT csv_data,row_count,uploaded_at FROM property_data WHERE state=?', (state,)).fetchone()
    db.close()
    if not row:
        return jsonify({'data': None, 'rows': 0, 'uploaded_at': None})
    return jsonify({'data': row['csv_data'], 'rows': row['row_count'], 'uploaded_at': row['uploaded_at']})

@app.route('/api/properties/status')
@login_required
def properties_status():
    db = get_db()
    rows = db.execute('SELECT state,row_count,uploaded_at,uploaded_by FROM property_data').fetchall()
    db.close()
    return jsonify({r['state']: {'rows': r['row_count'], 'uploaded_at': r['uploaded_at'], 'uploaded_by': r['uploaded_by']} for r in rows})

@app.route('/api/shortlist', methods=['GET'])
@login_required
def get_shortlist():
    uid = request.current_user['id']
    db = get_db()
    row = db.execute('SELECT property_ids,dd_data FROM shortlists WHERE user_id=?', (uid,)).fetchone()
    db.close()
    if not row:
        return jsonify({'ids': [], 'dd': {}})
    return jsonify({'ids': json.loads(row['property_ids']), 'dd': json.loads(row['dd_data'] or '{}')})

@app.route('/api/shortlist', methods=['POST'])
@login_required
def save_shortlist():
    uid = request.current_user['id']
    data = request.get_json()
    ids = json.dumps(data.get('ids', []))
    dd = json.dumps(data.get('dd', {}))
    db = get_db()
    db.execute("""INSERT INTO shortlists (user_id,property_ids,dd_data) VALUES (?,?,?)
                  ON CONFLICT(user_id) DO UPDATE SET property_ids=excluded.property_ids,
                  dd_data=excluded.dd_data, updated_at=datetime('now')""", (uid, ids, dd))
    db.commit()
    db.close()
    return jsonify({'ok': True})

@app.route('/admin')
@app.route('/admin/<section>')
@admin_required
def admin(section='activity'):
    db = get_db()
    total_users = db.execute("SELECT COUNT(*) FROM users WHERE role='team'").fetchone()[0]
    total_sessions = db.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
    views = db.execute("SELECT COUNT(*) FROM events WHERE event_type='property_view'").fetchone()[0]
    dls = db.execute("SELECT COUNT(*) FROM events WHERE event_type IN ('csv_download','docx_download')").fetchone()[0]
    stats = {'total_users':total_users,'total_sessions':total_sessions,'views':views,'downloads':dls}
    users = [dict(r) for r in db.execute("""
        SELECT u.id,u.full_name,u.username,u.role,u.active,
               COUNT(DISTINCT s.id) as session_count,
               MAX(s.login_at) as last_login,
               SUM(CASE WHEN s.logout_at IS NOT NULL
                   THEN ROUND((julianday(s.logout_at)-julianday(s.login_at))*24*60)
                   ELSE NULL END) as total_minutes
        FROM users u LEFT JOIN sessions s ON s.user_id=u.id
        GROUP BY u.id ORDER BY last_login DESC
    """).fetchall()]
    all_users = [dict(r) for r in db.execute('SELECT * FROM users ORDER BY full_name').fetchall()]
    prop_views = []
    for e in db.execute("SELECT e.*,u.full_name FROM events e JOIN users u ON e.user_id=u.id WHERE e.event_type='property_view' ORDER BY e.created_at DESC LIMIT 200").fetchall():
        row = dict(e)
        try:
            d = json.loads(row.get('event_data') or '{}')
            row['addr']=d.get('addr','n/a'); row['state']=d.get('state','').upper()
            row['sa4']=d.get('sa4','n/a'); row['price']='$'+str(int(d['price'])) if d.get('price') else 'n/a'
        except: row['addr']=row['state']=row['sa4']=row['price']='n/a'
        prop_views.append(row)
    dl_list = []
    for e in db.execute("SELECT e.*,u.full_name FROM events e JOIN users u ON e.user_id=u.id WHERE e.event_type IN ('csv_download','docx_download') ORDER BY e.created_at DESC LIMIT 200").fetchall():
        row = dict(e)
        try:
            d = json.loads(row.get('event_data') or '{}')
            row['addr']=d.get('addr','n/a'); row['state']=d.get('state','').upper()
        except: row['addr']=row['state']='n/a'
        dl_list.append(row)
    db.close()
    msg = request.args.get('msg','')
    msg_type = request.args.get('msg_type','ok')
    p = os.path.join(os.path.dirname(__file__), "templates", "admin.html")
    admin_html = open(p).read() if os.path.exists(p) else "<h1>Admin</h1>"
    return make_response(Template(admin_html).render(
        current_user=request.current_user, section=section,
        stats=stats, users=users, all_users=all_users,
        prop_views=prop_views, downloads=dl_list, msg=msg, msg_type=msg_type
    ))

@app.route('/admin/api/stats')
@admin_required
def admin_stats():
    db = get_db()
    users = db.execute("""
        SELECT u.id,u.full_name,u.username,u.role,u.active,
               COUNT(DISTINCT s.id) as session_count, MAX(s.login_at) as last_login,
               SUM(CASE WHEN s.logout_at IS NOT NULL
                   THEN ROUND((julianday(s.logout_at)-julianday(s.login_at))*24*60)
                   ELSE NULL END) as total_minutes
        FROM users u LEFT JOIN sessions s ON s.user_id=u.id
        GROUP BY u.id ORDER BY last_login DESC
    """).fetchall()
    events = db.execute("SELECT e.*,u.full_name,u.username FROM events e JOIN users u ON e.user_id=u.id ORDER BY e.created_at DESC LIMIT 200").fetchall()
    db.close()
    return jsonify({'stats':{'total_users':0,'total_sessions':0,'total_events':0},
                    'users':[dict(u) for u in users], 'events':[dict(e) for e in events]})

@app.route('/admin/api/users')
@admin_required
def admin_users():
    db = get_db()
    users = db.execute('SELECT id,username,full_name,role,active,created_at FROM users ORDER BY full_name').fetchall()
    db.close()
    return jsonify([dict(u) for u in users])

@app.route('/admin/users/add_form', methods=['POST'])
@admin_required
def add_user_form():
    full_name = request.form.get('full_name','').strip()
    username = request.form.get('username','').strip().lower()
    password = request.form.get('password','')
    role = request.form.get('role','team')
    if not full_name or not username or len(password) < 6:
        return redirect('/admin/users?msg=All+fields+required.+Password+min+6+chars&msg_type=er')
    try:
        db = get_db()
        db.execute('INSERT INTO users (username,password_hash,full_name,role) VALUES (?,?,?,?)',
                   (username, generate_password_hash(password), full_name, role))
        db.commit()
        db.close()
        return redirect('/admin/users?msg='+full_name+'+added&msg_type=ok')
    except sqlite3.IntegrityError:
        return redirect('/admin/users?msg=Username+already+exists&msg_type=er')

@app.route('/admin/users/add', methods=['POST'])
@admin_required
def add_user():
    data = request.get_json()
    username = data.get('username','').strip().lower()
    password = data.get('password','')
    full_name = data.get('full_name','').strip()
    role = data.get('role','team')
    if not username or not password or not full_name:
        return jsonify({'error': 'Missing fields'}), 400
    try:
        db = get_db()
        db.execute('INSERT INTO users (username,password_hash,full_name,role) VALUES (?,?,?,?)',
                   (username, generate_password_hash(password), full_name, role))
        db.commit()
        db.close()
        return jsonify({'ok': True})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

@app.route('/admin/users/<int:uid>/password', methods=['POST'])
@admin_required
def change_password(uid):
    if request.content_type and 'json' in request.content_type:
        password = request.get_json().get('password','')
    else:
        password = request.form.get('password','')
    if len(password) < 6:
        if request.content_type and 'json' in request.content_type:
            return jsonify({'error': 'Password too short'}), 400
        return redirect('/admin/users?msg=Password+must+be+at+least+6+characters&msg_type=er')
    db = get_db()
    db.execute('UPDATE users SET password_hash=? WHERE id=?', (generate_password_hash(password), uid))
    db.commit()
    db.close()
    if request.content_type and 'json' in request.content_type:
        return jsonify({'ok': True})
    return redirect('/admin/users?msg=Password+updated&msg_type=ok')

@app.route('/admin/users/<int:uid>/toggle', methods=['POST'])
@admin_required
def toggle_user(uid):
    db = get_db()
    user = db.execute('SELECT active FROM users WHERE id=?', (uid,)).fetchone()
    if user:
        db.execute('UPDATE users SET active=? WHERE id=?', (1-user['active'], uid))
        db.commit()
    db.close()
    if request.content_type and 'json' in request.content_type:
        return jsonify({'ok': True})
    return redirect('/admin/users?msg=User+updated&msg_type=ok')

@app.route('/admin/upload_page')
@admin_required
def upload_page():
    db = get_db()
    rows = db.execute('SELECT state,row_count,uploaded_at,uploaded_by FROM property_data').fetchall()
    db.close()
    status = {r['state']: dict(r) for r in rows}
    msg = request.args.get('msg','')
    msg_type = request.args.get('msg_type','ok')
    p2 = os.path.join(os.path.dirname(__file__), "templates", "upload.html")
    UPLOAD_HTML = open(p2).read() if os.path.exists(p2) else ""
    html = UPLOAD_HTML.replace('{{STATUS}}', json.dumps(status)).replace('{{MSG}}', msg).replace('{{MSG_TYPE}}', msg_type)
    return make_response(html)

@app.route('/admin/upload', methods=['POST'])
@admin_required
def upload_csv():
    state = request.form.get('state','').lower()
    if state not in ('vic','nsw','qld'):
        return redirect('/admin/upload_page?msg=Invalid+state&msg_type=er')
    f = request.files.get('csvfile')
    if not f:
        return redirect('/admin/upload_page?msg=No+file+selected&msg_type=er')
    try:
        csv_data = f.read().decode('utf-8')
        rows = len([l for l in csv_data.strip().split('\n') if l]) - 1
        db = get_db()
        db.execute("""INSERT INTO property_data (state,csv_data,row_count,uploaded_by) VALUES (?,?,?,?)
                      ON CONFLICT(state) DO UPDATE SET csv_data=excluded.csv_data,
                      row_count=excluded.row_count, uploaded_by=excluded.uploaded_by,
                      uploaded_at=datetime('now')""",
                   (state, csv_data, rows, request.current_user['username']))
        db.commit()
        db.close()
        return redirect('/admin/upload_page?msg='+state.upper()+'+uploaded+('+str(rows)+'+properties)&msg_type=ok')
    except Exception as e:
        return redirect('/admin/upload_page?msg=Upload+failed&msg_type=er')

@app.route('/admin/users/<int:uid>/sessions')
@admin_required
def user_sessions(uid):
    db = get_db()
    sessions = db.execute("""
        SELECT s.id,s.login_at,s.logout_at,s.last_active,s.ip_address,
               CASE WHEN s.logout_at IS NOT NULL
                    THEN ROUND((julianday(s.logout_at)-julianday(s.login_at))*24*60)
                    ELSE ROUND((julianday(s.last_active)-julianday(s.login_at))*24*60)
               END as duration_mins,
               (SELECT COUNT(*) FROM events e WHERE e.session_id=s.id) as event_count
        FROM sessions s WHERE s.user_id=? ORDER BY s.login_at DESC
    """, (uid,)).fetchall()
    events = db.execute("""
        SELECT e.event_type,e.event_data,e.created_at FROM events e
        WHERE e.user_id=? ORDER BY e.created_at DESC LIMIT 500
    """, (uid,)).fetchall()
    db.close()
    return jsonify({'sessions':[dict(s) for s in sessions],'events':[dict(e) for e in events]})

if __name__ == '__main__':
    print("SDA Property Screener - Team Server")
    app.run(debug=False, host='0.0.0.0', port=5000)
