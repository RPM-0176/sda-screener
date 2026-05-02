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
<title>Admin Panel — SDA Screener</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#f3f4f6;color:#111827}
.topbar{background:#002060;color:#fff;padding:14px 28px;display:flex;justify-content:space-between;align-items:center}
.topbar h1{font-size:16px;font-weight:700}
.topbar a{color:#93c5fd;font-size:13px;text-decoration:none}
.topbar a:hover{color:#fff}
.container{max-width:1400px;margin:0 auto;padding:24px}
.tabs{display:flex;gap:4px;margin-bottom:24px;background:#fff;padding:6px;border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.tab{padding:10px 20px;border:none;background:none;cursor:pointer;font-size:13px;font-weight:600;color:#6B7280;border-radius:7px;transition:.15s}
.tab.active{background:#002060;color:#fff}
.panel{display:none}
.panel.active{display:block}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}
.stat-card{background:#fff;border-radius:10px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.stat-card .num{font-size:32px;font-weight:800;color:#002060}
.stat-card .lbl{font-size:12px;color:#6B7280;margin-top:4px;font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.card{background:#fff;border-radius:10px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,.08);margin-bottom:20px}
.card h2{font-size:14px;font-weight:700;color:#002060;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;padding:10px 12px;background:#f9fafb;color:#6B7280;font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.04em;border-bottom:1px solid #e5e7eb}
td{padding:10px 12px;border-bottom:1px solid #f3f4f6;color:#374151}
tr:hover td{background:#fafbff}
.badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:700}
.badge-admin{background:#fef3c7;color:#92400e}
.badge-team{background:#e0f2fe;color:#0369a1}
.badge-active{background:#dcfce7;color:#166534}
.badge-inactive{background:#fee2e2;color:#991b1b}
.badge-login{background:#f0f5fb;color:#185FA5}
.badge-view{background:#f0fdf4;color:#0F6E56}
.badge-csv{background:#fef9c3;color:#854d0e}
.badge-docx{background:#faf5ff;color:#7c3aed}
.btn{padding:7px 14px;border:none;border-radius:6px;cursor:pointer;font-size:12px;font-weight:700}
.btn-primary{background:#002060;color:#fff}
.btn-danger{background:#fee2e2;color:#991b1b}
.btn-success{background:#dcfce7;color:#166534}
.btn-sm{padding:4px 10px;font-size:11px}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);z-index:1000;align-items:center;justify-content:center}
.modal.open{display:flex}
.modal-box{background:#fff;border-radius:12px;padding:28px;width:100%;max-width:480px;box-shadow:0 20px 60px rgba(0,0,0,.3)}
.modal-box h3{font-size:16px;font-weight:700;color:#002060;margin-bottom:20px}
.form-row{margin-bottom:14px}
.form-row label{display:block;font-size:11px;font-weight:700;color:#6B7280;margin-bottom:5px;text-transform:uppercase}
.form-row input,.form-row select{width:100%;padding:9px 12px;border:1px solid #d1d5db;border-radius:7px;font-size:13px;font-family:Arial}
.form-row input:focus,.form-row select:focus{outline:none;border-color:#185FA5}
.modal-actions{display:flex;gap:10px;justify-content:flex-end;margin-top:20px}
.search-bar{padding:8px 12px;border:1px solid #d1d5db;border-radius:7px;font-size:13px;width:280px;margin-bottom:14px}
.user-row-detail{display:none;background:#f9fafb;padding:16px 20px}
.prop-tag{display:inline-block;background:#f0f5fb;color:#185FA5;border:1px solid #c8ddf5;padding:2px 8px;border-radius:4px;font-size:11px;margin:2px}
</style>
</head>
<body>
<div class="topbar">
  <h1>⚙ SDA Screener — Admin Panel</h1>
  <div style="display:flex;gap:20px;align-items:center">
    <span style="font-size:13px;color:#93c5fd">👤 {{ current_user.full_name }}</span>
    <a href="/dashboard">← Dashboard</a>
    <a href="/logout">Sign out</a>
  </div>
</div>

<div class="container">
  <!-- Stats -->
  <div class="stats-grid" id="stats-grid">
    <div class="stat-card"><div class="num" id="stat-users">—</div><div class="lbl">Team members</div></div>
    <div class="stat-card"><div class="num" id="stat-sessions">—</div><div class="lbl">Total sessions</div></div>
    <div class="stat-card"><div class="num" id="stat-views">—</div><div class="lbl">Property views</div></div>
    <div class="stat-card"><div class="num" id="stat-downloads">—</div><div class="lbl">Downloads</div></div>
  </div>

  <!-- Tabs -->
  <div class="tabs">
    <button class="tab active" onclick="showTab('team')">👥 Team activity</button>
    <button class="tab" onclick="showTab('properties')">🏠 Property views</button>
    <button class="tab" onclick="showTab('downloads')">📄 Downloads</button>
    <button class="tab" onclick="showTab('users')">⚙ Manage users</button>
  </div>

  <!-- Team activity panel -->
  <div id="panel-team" class="panel active">
    <div class="card">
      <h2>Team member activity</h2>
      <input class="search-bar" placeholder="Search team member..." oninput="filterTable('team-table',this.value)">
      <table id="team-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Username</th>
            <th>Role</th>
            <th>Sessions</th>
            <th>Last login</th>
            <th>Total time</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody id="team-tbody"></tbody>
      </table>
    </div>
  </div>

  <!-- Property views panel -->
  <div id="panel-properties" class="panel">
    <div class="card">
      <h2>Property views (all team members)</h2>
      <input class="search-bar" placeholder="Search address or user..." oninput="filterTable('props-table',this.value)">
      <table id="props-table">
        <thead>
          <tr><th>When</th><th>User</th><th>Property address</th><th>State</th><th>SA4</th><th>Price</th></tr>
        </thead>
        <tbody id="props-tbody"></tbody>
      </table>
    </div>
  </div>

  <!-- Downloads panel -->
  <div id="panel-downloads" class="panel">
    <div class="card">
      <h2>Downloads — CSV & Word reports</h2>
      <input class="search-bar" placeholder="Search address or user..." oninput="filterTable('dl-table',this.value)">
      <table id="dl-table">
        <thead>
          <tr><th>When</th><th>User</th><th>Type</th><th>Property address</th><th>State</th><th>SA4</th></tr>
        </thead>
        <tbody id="dl-tbody"></tbody>
      </table>
    </div>
  </div>

  <!-- Manage users panel -->
  <div id="panel-users" class="panel">
    <div class="card">
      <h2>Manage users</h2>
      <button class="btn btn-primary" onclick="openAddUser()" style="margin-bottom:16px">+ Add team member</button>
      <table id="users-table">
        <thead>
          <tr><th>Name</th><th>Username</th><th>Role</th><th>Created</th><th>Status</th><th>Actions</th></tr>
        </thead>
        <tbody id="users-tbody"></tbody>
      </table>
    </div>
  </div>
</div>

<!-- User detail modal -->
<div id="user-modal" class="modal">
  <div class="modal-box" style="max-width:700px">
    <h3 id="modal-user-title">User sessions</h3>
    <div id="modal-user-content"></div>
    <div class="modal-actions">
      <button class="btn btn-primary" onclick="closeModal('user-modal')">Close</button>
    </div>
  </div>
</div>

<!-- Add user modal -->
<div id="add-user-modal" class="modal">
  <div class="modal-box">
    <h3>Add team member</h3>
    <div class="form-row"><label>Full name</label><input id="new-name" placeholder="e.g. Sarah Johnson"></div>
    <div class="form-row"><label>Username</label><input id="new-username" placeholder="e.g. sarah.johnson"></div>
    <div class="form-row"><label>Password</label><input id="new-password" type="password" placeholder="Min 6 characters"></div>
    <div class="form-row"><label>Role</label>
      <select id="new-role">
        <option value="team">Team member</option>
        <option value="admin">Admin</option>
      </select>
    </div>
    <div id="add-error" style="color:#A32D2D;font-size:13px;margin-top:8px;display:none"></div>
    <div class="modal-actions">
      <button class="btn" style="background:#f3f4f6" onclick="closeModal('add-user-modal')">Cancel</button>
      <button class="btn btn-primary" onclick="submitAddUser()">Add member</button>
    </div>
  </div>
</div>

<!-- Change password modal -->
<div id="pw-modal" class="modal">
  <div class="modal-box">
    <h3>Change password</h3>
    <p id="pw-modal-name" style="color:#6B7280;font-size:13px;margin-bottom:16px"></p>
    <div class="form-row"><label>New password</label><input id="pw-new" type="password" placeholder="Min 6 characters"></div>
    <div id="pw-error" style="color:#A32D2D;font-size:13px;margin-top:8px;display:none"></div>
    <div class="modal-actions">
      <button class="btn" style="background:#f3f4f6" onclick="closeModal('pw-modal')">Cancel</button>
      <button class="btn btn-primary" onclick="submitPwChange()">Update password</button>
    </div>
  </div>
</div>

<script>
var allData = null;
var pwTargetId = null;

function showTab(name){
  document.querySelectorAll('.tab').forEach(function(t){t.classList.remove('active');});
  document.querySelectorAll('.panel').forEach(function(p){p.classList.remove('active');});
  event.target.classList.add('active');
  document.getElementById('panel-'+name).classList.add('active');
}

function filterTable(tableId, query){
  var rows = document.getElementById(tableId).querySelectorAll('tbody tr');
  var q = query.toLowerCase();
  rows.forEach(function(row){
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
}

function fmt(dt){
  if(!dt) return '—';
  var d = new Date(dt+'Z');
  return d.toLocaleDateString('en-AU',{day:'2-digit',month:'short',year:'numeric'})
    +' '+d.toLocaleTimeString('en-AU',{hour:'2-digit',minute:'2-digit'});
}

function fmtDuration(mins){
  if(!mins) return '—';
  if(mins < 60) return Math.round(mins)+'m';
  return Math.floor(mins/60)+'h '+Math.round(mins%60)+'m';
}

function loadData(){
  fetch('/admin/api/stats').then(r=>r.json()).then(function(data){
    allData = data;

    // Stats
    document.getElementById('stat-users').textContent = data.stats.total_users;
    document.getElementById('stat-sessions').textContent = data.stats.total_sessions;
    var views = data.events.filter(function(e){return e.event_type==='property_view';}).length;
    var dls = data.events.filter(function(e){return e.event_type==='csv_download'||e.event_type==='docx_download';}).length;
    document.getElementById('stat-views').textContent = views;
    document.getElementById('stat-downloads').textContent = dls;

    // Team table
    var tbody = document.getElementById('team-tbody');
    tbody.innerHTML = data.users.map(function(u){
      var roleBadge = u.role==='admin'?'badge-admin':'badge-team';
      var statusBadge = u.active?'badge-active':'badge-inactive';
      return '<tr>'
        +'<td><strong>'+u.full_name+'</strong></td>'
        +'<td>'+u.username+'</td>'
        +'<td><span class="badge '+roleBadge+'">'+u.role+'</span></td>'
        +'<td>'+u.session_count+'</td>'
        +'<td>'+fmt(u.last_login)+'</td>'
        +'<td>'+fmtDuration(u.total_minutes)+'</td>'
        +'<td><span class="badge '+(u.active?'badge-active':'badge-inactive')+'">'+(u.active?'Active':'Disabled')+'</span></td>'
        +'<td><button class="btn btn-sm btn-primary" onclick="showUserDetail('+u.id+',\''+u.full_name+'\')">Detail</button></td>'
        +'</tr>';
    }).join('');

    // Property views table
    var propsTbody = document.getElementById('props-tbody');
    var propEvents = data.events.filter(function(e){return e.event_type==='property_view';});
    propsTbody.innerHTML = propEvents.map(function(e){
      var d = {};
      try{d=JSON.parse(e.event_data||'{}');}catch(x){}
      return '<tr>'
        +'<td>'+fmt(e.created_at)+'</td>'
        +'<td>'+e.full_name+'</td>'
        +'<td>'+( d.addr||'—')+'</td>'
        +'<td>'+(d.state?d.state.toUpperCase():'—')+'</td>'
        +'<td>'+(d.sa4||'—')+'</td>'
        +'<td>'+(d.price?'$'+parseInt(d.price).toLocaleString():'—')+'</td>'
        +'</tr>';
    }).join('');

    // Downloads table
    var dlTbody = document.getElementById('dl-tbody');
    var dlEvents = data.events.filter(function(e){return e.event_type==='csv_download'||e.event_type==='docx_download';});
    dlTbody.innerHTML = dlEvents.map(function(e){
      var d = {};
      try{d=JSON.parse(e.event_data||'{}');}catch(x){}
      var typeBadge = e.event_type==='csv_download'?'badge-csv':'badge-docx';
      var typeLabel = e.event_type==='csv_download'?'CSV':'Word doc';
      return '<tr>'
        +'<td>'+fmt(e.created_at)+'</td>'
        +'<td>'+e.full_name+'</td>'
        +'<td><span class="badge '+typeBadge+'">'+typeLabel+'</span></td>'
        +'<td>'+(d.addr||'—')+'</td>'
        +'<td>'+(d.state?d.state.toUpperCase():'—')+'</td>'
        +'<td>'+(d.sa4||'—')+'</td>'
        +'</tr>';
    }).join('');

    // Users management table
    loadUsersTable();
  });
}

function loadUsersTable(){
  fetch('/admin/users').then(r=>r.json()).then(function(users){
    var tbody = document.getElementById('users-tbody');
    tbody.innerHTML = users.map(function(u){
      return '<tr>'
        +'<td><strong>'+u.full_name+'</strong></td>'
        +'<td>'+u.username+'</td>'
        +'<td><span class="badge '+(u.role==='admin'?'badge-admin':'badge-team')+'">'+u.role+'</span></td>'
        +'<td>'+fmt(u.created_at)+'</td>'
        +'<td><span class="badge '+(u.active?'badge-active':'badge-inactive')+'">'+(u.active?'Active':'Disabled')+'</span></td>'
        +'<td style="display:flex;gap:6px">'
        +'<button class="btn btn-sm" style="background:#f0f5fb;color:#185FA5" onclick="openPwModal('+u.id+',\''+u.full_name+'\')">Change PW</button>'
        +'<button class="btn btn-sm '+(u.active?'btn-danger':'btn-success')+'" onclick="toggleUser('+u.id+')">'+(u.active?'Disable':'Enable')+'</button>'
        +'</td>'
        +'</tr>';
    }).join('');
  });
}

function showUserDetail(uid, name){
  document.getElementById('modal-user-title').textContent = name+' — Session detail';
  document.getElementById('modal-user-content').innerHTML = 'Loading...';
  document.getElementById('user-modal').classList.add('open');

  fetch('/admin/users/'+uid+'/sessions').then(r=>r.json()).then(function(data){
    var sessHtml = '<table style="margin-bottom:20px"><thead><tr>'
      +'<th>Login time</th><th>Logout</th><th>Duration</th><th>IP</th><th>Events</th>'
      +'</tr></thead><tbody>'
      +data.sessions.map(function(s){
        return '<tr>'
          +'<td>'+fmt(s.login_at)+'</td>'
          +'<td>'+(s.logout_at?fmt(s.logout_at):'<span style="color:#0F6E56">Active</span>')+'</td>'
          +'<td>'+fmtDuration(s.duration_mins)+'</td>'
          +'<td>'+s.ip_address+'</td>'
          +'<td>'+s.event_count+'</td>'
          +'</tr>';
      }).join('')+'</tbody></table>';

    var evtHtml = '<h4 style="font-size:13px;font-weight:700;color:#374151;margin-bottom:10px">Activity log</h4>';
    evtHtml += data.events.slice(0,50).map(function(e){
      var d={};try{d=JSON.parse(e.event_data||'{}');}catch(x){}
      var typeMap={login:'🔐 Login',logout:'🚪 Logout',dashboard_view:'📊 Dashboard',
        property_view:'🏠 Property view',csv_download:'📋 CSV download',docx_download:'📄 Word download'};
      var label = typeMap[e.event_type]||e.event_type;
      var detail = '';
      if(d.addr) detail = ' — '+d.addr;
      else if(d.username) detail = ' — '+d.username;
      return '<div style="padding:5px 0;border-bottom:1px solid #f3f4f6;font-size:12px">'
        +'<span style="color:#6B7280;width:140px;display:inline-block">'+fmt(e.created_at)+'</span>'
        +'<span>'+label+'</span>'
        +'<span style="color:#6B7280">'+detail+'</span>'
        +'</div>';
    }).join('');

    document.getElementById('modal-user-content').innerHTML = sessHtml + evtHtml;
  });
}

function closeModal(id){document.getElementById(id).classList.remove('open');}

function openAddUser(){
  ['new-name','new-username','new-password'].forEach(function(id){document.getElementById(id).value='';});
  document.getElementById('new-role').value='team';
  document.getElementById('add-error').style.display='none';
  document.getElementById('add-user-modal').classList.add('open');
  document.getElementById('new-name').focus();
}

function submitAddUser(){
  var name=document.getElementById('new-name').value.trim();
  var user=document.getElementById('new-username').value.trim();
  var pw=document.getElementById('new-password').value;
  var role=document.getElementById('new-role').value;
  var errEl=document.getElementById('add-error');
  if(!name||!user||!pw){errEl.textContent='All fields required.';errEl.style.display='block';return;}
  if(pw.length<6){errEl.textContent='Password must be at least 6 characters.';errEl.style.display='block';return;}
  fetch('/admin/users/add',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({full_name:name,username:user,password:pw,role:role})
  }).then(r=>r.json()).then(function(res){
    if(res.error){errEl.textContent=res.error;errEl.style.display='block';return;}
    closeModal('add-user-modal');
    loadData();
  });
}

function openPwModal(uid, name){
  pwTargetId=uid;
  document.getElementById('pw-modal-name').textContent='User: '+name;
  document.getElementById('pw-new').value='';
  document.getElementById('pw-error').style.display='none';
  document.getElementById('pw-modal').classList.add('open');
  document.getElementById('pw-new').focus();
}

function submitPwChange(){
  var pw=document.getElementById('pw-new').value;
  var errEl=document.getElementById('pw-error');
  if(pw.length<6){errEl.textContent='Password must be at least 6 characters.';errEl.style.display='block';return;}
  fetch('/admin/users/'+pwTargetId+'/password',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({password:pw})
  }).then(r=>r.json()).then(function(res){
    if(res.error){errEl.textContent=res.error;errEl.style.display='block';return;}
    closeModal('pw-modal');
    alert('Password updated successfully.');
  });
}

function toggleUser(uid){
  if(!confirm('Toggle this user\'s access?')) return;
  fetch('/admin/users/'+uid+'/toggle',{method:'POST'}).then(function(){loadData();});
}

// Auto-refresh every 60 seconds
loadData();
setInterval(loadData, 60000);
</script>
</body>
</html>
"""


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
