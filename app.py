"""
SDA Property Screener — Team Server
"""
from flask import Flask, request, session, redirect, url_for, jsonify, send_file, abort, make_response, Response
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import Template
import sqlite3, json, os, datetime, secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Initialise database on startup (works with both gunicorn and direct run)
with app.app_context():
    pass  # init_db called below after functions are defined

DB = os.path.join(os.path.dirname(__file__), 'usage.db')
DASHBOARD_HTML = os.path.join(os.path.dirname(__file__), 'dashboard.html')

LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SDA Property Screener — Login</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#001540 0%,#002060 50%,#003090 100%);min-height:100vh;display:flex;align-items:center;justify-content:center}
  .card{background:#fff;border-radius:16px;padding:48px 40px;width:100%;max-width:400px;box-shadow:0 24px 80px rgba(0,0,0,0.4)}
  .logo{text-align:center;margin-bottom:32px}
  .logo h1{font-size:22px;font-weight:800;color:#002060;margin-bottom:4px}
  .logo p{font-size:13px;color:#6B7280}
  .logo-icon{font-size:40px;margin-bottom:12px}
  label{display:block;font-size:12px;font-weight:700;color:#374151;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em}
  input{width:100%;padding:12px 14px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;font-family:Arial;margin-bottom:16px;color:#111827;transition:border-color .2s}
  input:focus{outline:none;border-color:#185FA5;box-shadow:0 0 0 3px rgba(24,95,165,.12)}
  button{width:100%;padding:14px;background:#002060;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer;margin-top:4px;transition:background .2s}
  button:hover{background:#003090}
  .error{background:#fff3f3;border:1px solid #fca5a5;color:#A32D2D;padding:12px 14px;border-radius:8px;font-size:13px;margin-bottom:16px}
  .footer{text-align:center;margin-top:24px;font-size:12px;color:#9CA3AF}
</style>
</head>
<body>
<div class="card">
  <div class="logo">
    <div class="logo-icon">🏠</div>
    <h1>SDA Property Screener</h1>
    <p>NDIS Investment Analysis Platform</p>
  </div>
  {% if error %}
  <div class="error">{{ error }}</div>
  {% endif %}
  <form method="POST">
    <label>Username</label>
    <input type="text" name="username" autocomplete="username" autofocus required placeholder="Enter your username">
    <label>Password</label>
    <input type="password" name="password" autocomplete="current-password" required placeholder="Enter your password">
    <button type="submit">Sign In</button>
  </form>
  <div class="footer">Confidential — Authorised users only</div>
</div>
</body>
</html>
"""

ADMIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Admin — SDA Screener</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#f3f4f6;color:#111}
.top{background:#002060;color:#fff;padding:14px 24px;display:flex;justify-content:space-between;align-items:center}
.top h1{font-size:15px;font-weight:700}
.top a{color:#93c5fd;font-size:13px;text-decoration:none;margin-left:16px}
.wrap{max-width:1200px;margin:0 auto;padding:20px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
.stat{background:#fff;border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.1)}
.stat .n{font-size:28px;font-weight:800;color:#002060}
.stat .l{font-size:11px;color:#6B7280;margin-top:4px;text-transform:uppercase;font-weight:600}
.tabs{display:flex;gap:4px;margin-bottom:16px}
.tab{padding:10px 18px;border:none;border-radius:6px;cursor:pointer;font-size:13px;font-weight:600;background:#e5e7eb;color:#374151}
.tab.on{background:#002060;color:#fff}
.panel{display:none}
.panel.on{display:block}
.card{background:#fff;border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:16px}
.card h2{font-size:13px;font-weight:700;color:#002060;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}
table{width:100%;border-collapse:collapse;font-size:12px}
th{text-align:left;padding:8px 10px;background:#f9fafb;color:#6B7280;font-size:11px;font-weight:700;text-transform:uppercase;border-bottom:1px solid #e5e7eb}
td{padding:8px 10px;border-bottom:1px solid #f3f4f6}
tr:hover td{background:#fafbff}
.btn{padding:5px 10px;border:none;border-radius:5px;cursor:pointer;font-size:11px;font-weight:700}
.blue{background:#002060;color:#fff}
.red{background:#fee2e2;color:#991b1b}
.green{background:#dcfce7;color:#166534}
.gray{background:#f3f4f6;color:#374151}
.badge{display:inline-block;padding:2px 6px;border-radius:10px;font-size:10px;font-weight:700}
.ba{background:#fef3c7;color:#92400e}
.bt{background:#e0f2fe;color:#0369a1}
.bactive{background:#dcfce7;color:#166534}
.binactive{background:#fee2e2;color:#991b1b}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);z-index:999;align-items:center;justify-content:center}
.modal.on{display:flex}
.mbox{background:#fff;border-radius:10px;padding:24px;width:420px;box-shadow:0 20px 40px rgba(0,0,0,.3)}
.mbox h3{font-size:15px;font-weight:700;color:#002060;margin-bottom:16px}
.fl{margin-bottom:12px}
.fl label{display:block;font-size:11px;font-weight:700;color:#6B7280;margin-bottom:4px;text-transform:uppercase}
.fl input,.fl select{width:100%;padding:8px 10px;border:1px solid #d1d5db;border-radius:6px;font-size:13px}
.mact{display:flex;gap:8px;justify-content:flex-end;margin-top:16px}
.err{color:#A32D2D;font-size:12px;margin-top:8px;display:none}
input[type=search]{padding:7px 10px;border:1px solid #d1d5db;border-radius:6px;font-size:12px;margin-bottom:10px;width:250px}
</style>
</head>
<body>
<div class="top">
  <h1>⚙ SDA Screener — Admin Panel</h1>
  <div>
    <span style="font-size:13px">👤 {{ current_user.full_name }}</span>
    <a href="/dashboard">← Dashboard</a>
    <a href="/logout">Sign out</a>
  </div>
</div>
<div class="wrap">
  <div class="stats">
    <div class="stat"><div class="n" id="s1">—</div><div class="l">Team members</div></div>
    <div class="stat"><div class="n" id="s2">—</div><div class="l">Total sessions</div></div>
    <div class="stat"><div class="n" id="s3">—</div><div class="l">Property views</div></div>
    <div class="stat"><div class="n" id="s4">—</div><div class="l">Downloads</div></div>
  </div>
  <div class="tabs">
    <button class="tab on" onclick="showTab('activity',this)">👥 Team activity</button>
    <button class="tab" onclick="showTab('props',this)">🏠 Property views</button>
    <button class="tab" onclick="showTab('dls',this)">📄 Downloads</button>
    <button class="tab" onclick="showTab('users',this)">⚙ Manage users</button>
  </div>
  <div id="panel-activity" class="panel on">
    <div class="card">
      <h2>Team member activity</h2>
      <input type="search" placeholder="Search..." oninput="filterTbl('tbl-activity',this.value)">
      <table id="tbl-activity"><thead><tr><th>Name</th><th>Username</th><th>Role</th><th>Sessions</th><th>Last login</th><th>Total time</th><th>Status</th><th></th></tr></thead><tbody id="tbody-activity"></tbody></table>
    </div>
  </div>
  <div id="panel-props" class="panel">
    <div class="card">
      <h2>Property views</h2>
      <input type="search" placeholder="Search..." oninput="filterTbl('tbl-props',this.value)">
      <table id="tbl-props"><thead><tr><th>When</th><th>User</th><th>Address</th><th>State</th><th>SA4</th><th>Price</th></tr></thead><tbody id="tbody-props"></tbody></table>
    </div>
  </div>
  <div id="panel-dls" class="panel">
    <div class="card">
      <h2>Downloads</h2>
      <input type="search" placeholder="Search..." oninput="filterTbl('tbl-dls',this.value)">
      <table id="tbl-dls"><thead><tr><th>When</th><th>User</th><th>Type</th><th>Address</th><th>State</th></tr></thead><tbody id="tbody-dls"></tbody></table>
    </div>
  </div>
  <div id="panel-users" class="panel">
    <div class="card">
      <h2>Manage users</h2>
      <button class="btn blue" onclick="openAdd()" style="margin-bottom:12px">+ Add team member</button>
      <table id="tbl-users"><thead><tr><th>Name</th><th>Username</th><th>Role</th><th>Status</th><th>Actions</th></tr></thead><tbody id="tbody-users"></tbody></table>
    </div>
  </div>
</div>

<!-- Add user modal -->
<div id="modal-add" class="modal">
  <div class="mbox">
    <h3>Add team member</h3>
    <div class="fl"><label>Full name</label><input id="add-name" placeholder="e.g. Sarah Johnson"></div>
    <div class="fl"><label>Username</label><input id="add-user" placeholder="e.g. sarah.johnson"></div>
    <div class="fl"><label>Password</label><input id="add-pw" type="password" placeholder="Min 6 characters"></div>
    <div class="fl"><label>Role</label><select id="add-role"><option value="team">Team member</option><option value="admin">Admin</option></select></div>
    <div class="err" id="add-err"></div>
    <div class="mact">
      <button class="btn gray" onclick="closeModal('modal-add')">Cancel</button>
      <button class="btn blue" onclick="submitAdd()">Add</button>
    </div>
  </div>
</div>

<!-- Change password modal -->
<div id="modal-pw" class="modal">
  <div class="mbox">
    <h3>Change password</h3>
    <p id="pw-name" style="color:#6B7280;font-size:13px;margin-bottom:14px"></p>
    <div class="fl"><label>New password</label><input id="pw-val" type="password" placeholder="Min 6 characters"></div>
    <div class="err" id="pw-err"></div>
    <div class="mact">
      <button class="btn gray" onclick="closeModal('modal-pw')">Cancel</button>
      <button class="btn blue" onclick="submitPw()">Update</button>
    </div>
  </div>
</div>

<script>
var pwUid = null;

function showTab(name, btn) {
  document.querySelectorAll('.panel').forEach(function(p){ p.classList.remove('on'); });
  document.querySelectorAll('.tab').forEach(function(t){ t.classList.remove('on'); });
  document.getElementById('panel-'+name).classList.add('on');
  btn.classList.add('on');
}

function filterTbl(id, q) {
  var rows = document.getElementById(id).querySelectorAll('tbody tr');
  q = q.toLowerCase();
  rows.forEach(function(r){ r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none'; });
}

function fmt(dt) {
  if(!dt) return '—';
  var d = new Date(dt.replace(' ','T')+'Z');
  return d.toLocaleDateString('en-AU',{day:'2-digit',month:'short',year:'numeric'})
    +' '+d.toLocaleTimeString('en-AU',{hour:'2-digit',minute:'2-digit'});
}

function fmtMins(m) {
  if(!m) return '—';
  m = Math.round(m);
  return m < 60 ? m+'m' : Math.floor(m/60)+'h '+( m%60)+'m';
}

function openAdd() { 
  ['add-name','add-user','add-pw'].forEach(function(id){ document.getElementById(id).value=''; });
  document.getElementById('add-role').value='team';
  document.getElementById('add-err').style.display='none';
  document.getElementById('modal-add').classList.add('on');
}

function closeModal(id) { document.getElementById(id).classList.remove('on'); }

function submitAdd() {
  var name=document.getElementById('add-name').value.trim();
  var user=document.getElementById('add-user').value.trim();
  var pw=document.getElementById('add-pw').value;
  var role=document.getElementById('add-role').value;
  var err=document.getElementById('add-err');
  if(!name||!user||pw.length<6){ err.textContent='All fields required. Password min 6 chars.'; err.style.display='block'; return; }
  fetch('/admin/users/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({full_name:name,username:user,password:pw,role:role})})
    .then(function(r){return r.json();}).then(function(res){
      if(res.error){ err.textContent=res.error; err.style.display='block'; return; }
      closeModal('modal-add'); loadData();
    });
}

function openPw(uid, name) {
  pwUid=uid;
  document.getElementById('pw-name').textContent='User: '+name;
  document.getElementById('pw-val').value='';
  document.getElementById('pw-err').style.display='none';
  document.getElementById('modal-pw').classList.add('on');
}

function submitPw() {
  var pw=document.getElementById('pw-val').value;
  var err=document.getElementById('pw-err');
  if(pw.length<6){ err.textContent='Password min 6 characters.'; err.style.display='block'; return; }
  fetch('/admin/users/'+pwUid+'/password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:pw})})
    .then(function(r){return r.json();}).then(function(res){
      if(res.error){ err.textContent=res.error; err.style.display='block'; return; }
      closeModal('modal-pw'); alert('Password updated!');
    });
}

function toggleUser(uid) {
  if(!confirm('Toggle this user access?')) return;
  fetch('/admin/users/'+uid+'/toggle',{method:'POST'}).then(function(){ loadData(); });
}

function loadData() {
  fetch('/admin/api/stats').then(function(r){return r.json();}).then(function(data){
    document.getElementById('s1').textContent = data.stats.total_users;
    document.getElementById('s2').textContent = data.stats.total_sessions;
    var views = data.events.filter(function(e){return e.event_type==='property_view';}).length;
    var dls = data.events.filter(function(e){return e.event_type==='csv_download'||e.event_type==='docx_download';}).length;
    document.getElementById('s3').textContent = views;
    document.getElementById('s4').textContent = dls;

    // Team activity
    var tb = document.getElementById('tbody-activity');
    tb.innerHTML = data.users.map(function(u){
      return '<tr><td><strong>'+u.full_name+'</strong></td><td>'+u.username+'</td>'
        +'<td><span class="badge '+(u.role==='admin'?'ba':'bt')+'">'+u.role+'</span></td>'
        +'<td>'+u.session_count+'</td><td>'+fmt(u.last_login)+'</td><td>'+fmtMins(u.total_minutes)+'</td>'
        +'<td><span class="badge '+(u.active?'bactive':'binactive')+'">'+(u.active?'Active':'Disabled')+'</span></td>'
        +'<td><button class="btn blue" onclick="openPw('+u.id+',''+u.full_name+'')">Change PW</button></td></tr>';
    }).join('');

    // Property views
    var tp = document.getElementById('tbody-props');
    tp.innerHTML = data.events.filter(function(e){return e.event_type==='property_view';}).map(function(e){
      var d={}; try{d=JSON.parse(e.event_data||'{}');}catch(x){}
      return '<tr><td>'+fmt(e.created_at)+'</td><td>'+e.full_name+'</td><td>'+(d.addr||'—')+'</td><td>'+(d.state?d.state.toUpperCase():'—')+'</td><td>'+(d.sa4||'—')+'</td><td>'+(d.price?'$'+parseInt(d.price).toLocaleString():'—')+'</td></tr>';
    }).join('') || '<tr><td colspan="6" style="color:#9CA3AF;padding:12px">No property views yet</td></tr>';

    // Downloads
    var td = document.getElementById('tbody-dls');
    td.innerHTML = data.events.filter(function(e){return e.event_type==='csv_download'||e.event_type==='docx_download';}).map(function(e){
      var d={}; try{d=JSON.parse(e.event_data||'{}');}catch(x){}
      return '<tr><td>'+fmt(e.created_at)+'</td><td>'+e.full_name+'</td><td>'+(e.event_type==='csv_download'?'CSV':'Word doc')+'</td><td>'+(d.addr||'—')+'</td><td>'+(d.state?d.state.toUpperCase():'—')+'</td></tr>';
    }).join('') || '<tr><td colspan="5" style="color:#9CA3AF;padding:12px">No downloads yet</td></tr>';

    // Users table
    loadUsers();
  });
}

function loadUsers() {
  fetch('/admin/users').then(function(r){return r.json();}).then(function(users){
    var tb = document.getElementById('tbody-users');
    tb.innerHTML = users.map(function(u){
      return '<tr><td><strong>'+u.full_name+'</strong></td><td>'+u.username+'</td>'
        +'<td><span class="badge '+(u.role==='admin'?'ba':'bt')+'">'+u.role+'</span></td>'
        +'<td><span class="badge '+(u.active?'bactive':'binactive')+'">'+(u.active?'Active':'Disabled')+'</span></td>'
        +'<td style="display:flex;gap:6px">'
        +'<button class="btn blue" onclick="openPw('+u.id+',''+u.full_name+'')">Change PW</button>'
        +'<button class="btn '+(u.active?'red':'green')+'" onclick="toggleUser('+u.id+')">'+(u.active?'Disable':'Enable')+'</button>'
        +'</td></tr>';
    }).join('');
  });
}

loadData();
setInterval(loadData, 60000);
</script>
</body>
</html>"""


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

# Initialise database immediately on module load
init_db()

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

    if LOGIN_HTML:
        from jinja2 import Template
        return make_response(Template(LOGIN_HTML).render(error=error))
    return make_response(f'<h2>Login</h2><form method="POST"><input name="username" placeholder="Username"><br><input type="password" name="password" placeholder="Password"><br><input type="submit" value="Login"></form>' + (f'<p style="color:red">{error}</p>' if error else ''))

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
    if ADMIN_HTML:
        from jinja2 import Template
        return make_response(Template(ADMIN_HTML).render(current_user=request.current_user))
    return make_response('<h2>Admin</h2><p>Admin template not found</p>')

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
