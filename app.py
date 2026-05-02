"""
SDA Property Screener — Team Server
Flask app with login, session tracking, usage logging, admin panel
"""

from flask import Flask, request, session, redirect, url_for, render_template, jsonify, send_file, abort
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, json, os, datetime, secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Replace with fixed key in production

DB = os.path.join(os.path.dirname(__file__), 'usage.db')
DASHBOARD_HTML = os.path.join(os.path.dirname(__file__), 'dashboard.html')

# ── Database setup ────────────────────────────────────────────────────────────

def get_db():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'team',  -- 'admin' or 'team'
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
    ''')
    db.commit()

    # Create default admin if no users exist
    existing = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if existing == 0:
        db.execute('''
            INSERT INTO users (username, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin', generate_password_hash('admin123'), 'Administrator', 'admin'))
        db.commit()
        print("✓ Default admin created: admin / admin123")
        print("  IMPORTANT: Change the admin password immediately!")
    db.close()

# ── Auth helpers ──────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return redirect(url_for('login'))
        db = get_db()
        sess = db.execute(
            'SELECT s.*, u.username, u.full_name, u.role, u.active FROM sessions s '
            'JOIN users u ON s.user_id = u.id '
            'WHERE s.session_token = ? AND s.logout_at IS NULL',
            (token,)
        ).fetchone()
        db.close()
        if not sess or not sess['active']:
            session.clear()
            return redirect(url_for('login'))
        # Update last_active
        db = get_db()
        db.execute('UPDATE sessions SET last_active = ? WHERE session_token = ?',
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
    if not token:
        return
    db = get_db()
    sess = db.execute('SELECT id, user_id FROM sessions WHERE session_token = ?', (token,)).fetchone()
    if sess:
        db.execute(
            'INSERT INTO events (session_id, user_id, event_type, event_data) VALUES (?, ?, ?, ?)',
            (sess['id'], sess['user_id'], event_type, json.dumps(event_data) if event_data else None)
        )
        db.commit()
    db.close()

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'token' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND active = 1', (username,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user['password_hash'], password):
            token = secrets.token_urlsafe(32)
            db = get_db()
            db.execute(
                'INSERT INTO sessions (user_id, session_token, ip_address) VALUES (?, ?, ?)',
                (user['id'], token, request.remote_addr)
            )
            db.commit()
            db.close()
            session['token'] = token
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            log_event('login', {'username': username})
            if user['role'] == 'admin':
                return redirect(url_for('dashboard'))
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password.'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    token = session.get('token')
    if token:
        log_event('logout')
        db = get_db()
        db.execute('UPDATE sessions SET logout_at = ? WHERE session_token = ?',
                   (datetime.datetime.utcnow().isoformat(), token))
        db.commit()
        db.close()
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    log_event('dashboard_view')
    return send_file(DASHBOARD_HTML)

@app.route('/api/log', methods=['POST'])
@login_required
def api_log():
    """Frontend calls this to log property views, downloads etc."""
    data = request.get_json()
    event_type = data.get('type')
    event_data = data.get('data')
    if event_type:
        log_event(event_type, event_data)
    return jsonify({'ok': True})

@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html',
                           current_user=request.current_user)

@app.route('/admin/api/stats')
@admin_required
def admin_stats():
    db = get_db()

    # Overall stats
    total_users = db.execute("SELECT COUNT(*) FROM users WHERE role='team'").fetchone()[0]
    total_sessions = db.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
    total_events = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]

    # Per-user stats
    users = db.execute('''
        SELECT u.id, u.full_name, u.username, u.role, u.active,
               COUNT(DISTINCT s.id) as session_count,
               MAX(s.login_at) as last_login,
               SUM(CASE WHEN s.logout_at IS NOT NULL
                   THEN ROUND((julianday(s.logout_at) - julianday(s.login_at)) * 24 * 60)
                   ELSE NULL END) as total_minutes
        FROM users u
        LEFT JOIN sessions s ON s.user_id = u.id
        GROUP BY u.id
        ORDER BY last_login DESC NULLS LAST
    ''').fetchall()

    # Recent events
    events = db.execute('''
        SELECT e.*, u.full_name, u.username
        FROM events e
        JOIN users u ON e.user_id = u.id
        ORDER BY e.created_at DESC
        LIMIT 200
    ''').fetchall()

    # Per-user property views
    prop_views = db.execute('''
        SELECT u.full_name, u.username,
               e.event_data,
               e.created_at
        FROM events e
        JOIN users u ON e.user_id = u.id
        WHERE e.event_type IN ('property_view','csv_download','docx_download')
        ORDER BY e.created_at DESC
    ''').fetchall()

    # Downloads summary
    downloads = db.execute('''
        SELECT u.full_name,
               e.event_type,
               e.event_data,
               e.created_at
        FROM events e
        JOIN users u ON e.user_id = u.id
        WHERE e.event_type IN ('csv_download','docx_download')
        ORDER BY e.created_at DESC
    ''').fetchall()

    db.close()

    return jsonify({
        'stats': {
            'total_users': total_users,
            'total_sessions': total_sessions,
            'total_events': total_events
        },
        'users': [dict(u) for u in users],
        'events': [dict(e) for e in events],
        'prop_views': [dict(p) for p in prop_views],
        'downloads': [dict(d) for d in downloads]
    })

@app.route('/admin/users', methods=['GET'])
@admin_required
def admin_users():
    db = get_db()
    users = db.execute('SELECT id, username, full_name, role, active, created_at FROM users ORDER BY full_name').fetchall()
    db.close()
    return jsonify([dict(u) for u in users])

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
        db.execute(
            'INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)',
            (username, generate_password_hash(password), full_name, role)
        )
        db.commit()
        db.close()
        return jsonify({'ok': True})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

@app.route('/admin/users/<int:uid>/password', methods=['POST'])
@admin_required
def change_password(uid):
    data = request.get_json()
    password = data.get('password','')
    if len(password) < 6:
        return jsonify({'error': 'Password too short (min 6 chars)'}), 400
    db = get_db()
    db.execute('UPDATE users SET password_hash = ? WHERE id = ?',
               (generate_password_hash(password), uid))
    db.commit()
    db.close()
    return jsonify({'ok': True})

@app.route('/admin/users/<int:uid>/toggle', methods=['POST'])
@admin_required
def toggle_user(uid):
    db = get_db()
    user = db.execute('SELECT active FROM users WHERE id = ?', (uid,)).fetchone()
    if user:
        db.execute('UPDATE users SET active = ? WHERE id = ?', (1 - user['active'], uid))
        db.commit()
    db.close()
    return jsonify({'ok': True})

@app.route('/admin/users/<int:uid>/sessions')
@admin_required
def user_sessions(uid):
    db = get_db()
    sessions = db.execute('''
        SELECT s.id, s.login_at, s.logout_at, s.last_active, s.ip_address,
               CASE WHEN s.logout_at IS NOT NULL
                    THEN ROUND((julianday(s.logout_at) - julianday(s.login_at)) * 24 * 60)
                    ELSE ROUND((julianday(s.last_active) - julianday(s.login_at)) * 24 * 60)
               END as duration_mins,
               (SELECT COUNT(*) FROM events e WHERE e.session_id = s.id) as event_count
        FROM sessions s
        WHERE s.user_id = ?
        ORDER BY s.login_at DESC
    ''', (uid,)).fetchall()

    events = db.execute('''
        SELECT e.event_type, e.event_data, e.created_at, s.login_at
        FROM events e
        JOIN sessions s ON e.session_id = s.id
        WHERE e.user_id = ?
        ORDER BY e.created_at DESC
        LIMIT 500
    ''', (uid,)).fetchall()
    db.close()

    return jsonify({
        'sessions': [dict(s) for s in sessions],
        'events': [dict(e) for e in events]
    })

if __name__ == '__main__':
    init_db()
    print("\n" + "="*50)
    print("SDA Property Screener — Team Server")
    print("="*50)
    print(f"Dashboard: http://localhost:5000")
    print(f"Admin:     http://localhost:5000/admin")
    print("="*50 + "\n")
    app.run(debug=False, host='0.0.0.0', port=5000)
