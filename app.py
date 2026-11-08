ADMIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Admin - SDA Screener</title>
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
.tab{padding:10px 18px;border-radius:6px;font-size:13px;font-weight:600;background:#e5e7eb;color:#374151;text-decoration:none;display:inline-block}
.tab.on{background:#002060;color:#fff}
.card{background:#fff;border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:16px}
.card h2{font-size:13px;font-weight:700;color:#002060;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}
table{width:100%;border-collapse:collapse;font-size:12px}
th{text-align:left;padding:8px 10px;background:#f9fafb;color:#6B7280;font-size:11px;font-weight:700;text-transform:uppercase;border-bottom:1px solid #e5e7eb}
td{padding:8px 10px;border-bottom:1px solid #f3f4f6;vertical-align:middle}
.badge{display:inline-block;padding:2px 6px;border-radius:10px;font-size:10px;font-weight:700}
.ba{background:#fef3c7;color:#92400e}
.bt{background:#e0f2fe;color:#0369a1}
.bact{background:#dcfce7;color:#166534}
.bina{background:#fee2e2;color:#991b1b}
.btn{padding:5px 10px;border:none;border-radius:5px;cursor:pointer;font-size:11px;font-weight:700;text-decoration:none;display:inline-block}
.blue{background:#002060;color:#fff}
.red{background:#fee2e2;color:#991b1b}
.grn{background:#dcfce7;color:#166534}
form.inline{display:inline}
.addform{background:#fff;border-radius:8px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:16px}
.addform .grid{display:grid;grid-template-columns:1fr 1fr 1fr 1fr auto;gap:10px;align-items:end}
.addform label{display:block;font-size:11px;font-weight:700;color:#6B7280;margin-bottom:4px;text-transform:uppercase}
.addform input,.addform select{width:100%;padding:8px 10px;border:1px solid #d1d5db;border-radius:6px;font-size:13px}
.pwfield{padding:6px 10px;border:1px solid #d1d5db;border-radius:6px;font-size:12px;width:140px}
.msg{padding:10px 14px;border-radius:6px;margin-bottom:14px;font-size:13px}
.ok{background:#dcfce7;color:#166534;border:1px solid #86efac}
.er{background:#fee2e2;color:#991b1b;border:1px solid #fca5a5}
</style>
</head>
<body>
<div class="top">
  <h1>SDA Screener - Admin Panel</h1>
  <div>
    <span style="font-size:13px">{{ current_user.full_name }}</span>
    <a href="/dashboard">Dashboard</a>
    <a href="/logout">Sign out</a>
  </div>
</div>
<div class="wrap">
  {% if msg %}<div class="msg {{ msg_type }}">{{ msg }}</div>{% endif %}
  <div class="stats">
    <div class="stat"><div class="n">{{ stats.total_users }}</div><div class="l">Team members</div></div>
    <div class="stat"><div class="n">{{ stats.total_sessions }}</div><div class="l">Sessions</div></div>
    <div class="stat"><div class="n">{{ stats.views }}</div><div class="l">Property views</div></div>
    <div class="stat"><div class="n">{{ stats.downloads }}</div><div class="l">Downloads</div></div>
  </div>
  <div class="tabs">
    <a href="/admin/activity" class="tab {% if section=='activity' %}on{% endif %}">Team activity</a>
    <a href="/admin/props" class="tab {% if section=='props' %}on{% endif %}">Property views</a>
    <a href="/admin/downloads" class="tab {% if section=='downloads' %}on{% endif %}">Downloads</a>
    <a href="/admin/hidden" class="tab {% if section=='hidden' %}on{% endif %}">Hidden properties{% if hidden_count %} ({{ hidden_count }}){% endif %}</a>
    <a href="/admin/users" class="tab {% if section=='users' %}on{% endif %}">Manage users</a>
    <a href="/admin/earnings" class="tab {% if section=='earnings' %}on{% endif %}" style="{% if section!='earnings' %}color:#7F1D1D;border-color:#7F1D1D{% endif %}">&#128274; Group earnings</a>
    <a href="/admin/upload_page" class="tab" style="background:#0F6E56;color:#fff">Upload CSV data</a>
    <a href="/admin/upload_sda_page" class="tab" style="background:#185FA5;color:#fff">Upload SDA market</a>
    <a href="/admin/upload_supply_page" class="tab" style="background:#0F6E56;color:#fff">Upload SDA supply</a>
    <a href="/admin/upload_performl_page" class="tab" style="background:#7C3AED;color:#fff">Upload Performl</a>
  </div>

  {% if section == 'activity' %}
  <div class="card">
    <h2>Team member activity</h2>
    <table><thead><tr><th>Name</th><th>Username</th><th>Role</th><th>Sessions</th><th>Last login</th><th>Status</th><th>Change password</th></tr></thead>
    <tbody>
    {% for u in users %}
    <tr>
      <td><strong>{{ u.full_name }}</strong></td>
      <td>{{ u.username }}</td>
      <td><span class="badge {{ 'ba' if u.role=='admin' else 'bt' }}">{{ u.role }}</span></td>
      <td>{{ u.session_count or 0 }}</td>
      <td>{{ u.last_login[:16] if u.last_login else 'Never' }}</td>
      <td><span class="badge {{ 'bact' if u.active else 'bina' }}">{{ 'Active' if u.active else 'Disabled' }}</span></td>
      <td>
        <form class="inline" method="POST" action="/admin/users/{{ u.id }}/password">
          <input type="password" name="password" placeholder="New password" class="pwfield">
          <button type="submit" class="btn blue">Update</button>
        </form>
      </td>
    </tr>
    {% else %}
    <tr><td colspan="7" style="color:#9CA3AF;padding:12px">No team members yet. Go to Manage Users to add them.</td></tr>
    {% endfor %}
    </tbody></table>
  </div>
  {% endif %}

  {% if section == 'props' %}
  <div class="card">
    <h2>Property views</h2>
    <table><thead><tr><th>When</th><th>User</th><th>Address</th><th>State</th><th>SA4</th><th>Price</th></tr></thead>
    <tbody>
    {% for e in prop_views %}
    <tr><td>{{ e.created_at[:16] }}</td><td>{{ e.full_name }}</td><td>{{ e.addr }}</td><td>{{ e.state }}</td><td>{{ e.sa4 }}</td><td>{{ e.price }}</td></tr>
    {% else %}
    <tr><td colspan="6" style="color:#9CA3AF;padding:12px">No property views logged yet</td></tr>
    {% endfor %}
    </tbody></table>
  </div>
  {% endif %}

  {% if section == 'downloads' %}
  <div class="card">
    <h2>Downloads</h2>
    <table><thead><tr><th>When</th><th>User</th><th>Type</th><th>Address</th><th>State</th></tr></thead>
    <tbody>
    {% for e in downloads %}
    <tr><td>{{ e.created_at[:16] }}</td><td>{{ e.full_name }}</td><td>{{ e.event_type }}</td><td>{{ e.addr }}</td><td>{{ e.state }}</td></tr>
    {% else %}
    <tr><td colspan="5" style="color:#9CA3AF;padding:12px">No downloads logged yet</td></tr>
    {% endfor %}
    </tbody></table>
  </div>
  {% endif %}

  {% if section == 'hidden' %}
  <div class="card">
    <h2>Hidden properties</h2>
    <p style="font-size:11px;color:#6B7280;margin-bottom:10px">
      Team members can hide a property from the screener by giving a reason. Restore puts it back in the screener. Hard delete removes it from the CSV permanently &mdash; this cannot be undone.
    </p>
    <table>
      <thead><tr>
        <th>When</th><th>Hidden by</th><th>State</th><th>Address</th><th>Reason</th><th style="text-align:right">Action</th>
      </tr></thead>
      <tbody>
      {% for h in hidden %}
        <tr id="hide-row-{{ h.id }}">
          <td>{{ h.hidden_at[:16] }}</td>
          <td>{{ h.hidden_by_name }}</td>
          <td><span class="badge bt">{{ h.state|upper }}</span></td>
          <td>{{ h.address }}</td>
          <td style="max-width:340px;white-space:normal">{{ h.reason }}</td>
          <td style="text-align:right;white-space:nowrap">
            <button type="button" class="btn grn" onclick="hideAction({{ h.id }}, 'restore')">Restore</button>
            <button type="button" class="btn red" data-state="{{ h.state|e }}" data-addr="{{ h.address|e }}" onclick="hideAction({{ h.id }}, 'harddelete', this)">Hard delete</button>
          </td>
        </tr>
      {% else %}
        <tr><td colspan="6" style="color:#9CA3AF;padding:12px">No properties are currently hidden.</td></tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
  <script>
  function adminToast(text){
    var t = document.getElementById('admin-toast');
    if(!t){
      t = document.createElement('div');
      t.id = 'admin-toast';
      t.style.cssText = 'position:fixed;right:20px;bottom:20px;z-index:9999;background:#0F6E56;color:#fff;padding:12px 16px;border-radius:8px;font-weight:600;font-size:14px;box-shadow:0 2px 12px rgba(0,0,0,0.2);max-width:380px;line-height:1.35';
      document.body.appendChild(t);
    }
    t.textContent = text;
    t.style.display = 'block';
    clearTimeout(window._adminToastTimer);
    window._adminToastTimer = setTimeout(function(){ t.style.display='none'; }, 5000);
  }
  function hideAction(id, kind, btn){
    if(kind === 'restore'){
      if(!confirm('Restore this property to the screener?')) return;
      fetch('/api/unhide-property', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({id: id})
      }).then(function(r){return r.json().then(function(j){return {ok:r.ok, j:j};});})
        .then(function(res){
          if(res.ok){
            var row = document.getElementById('hide-row-'+id);
            if(row) row.remove();
            adminToast('Restored to the screener. Reload your dashboard tab to see it (clear any filters if it does not appear).');
          } else {
            alert('Restore failed: '+(res.j && res.j.error || 'unknown'));
          }
        }).catch(function(e){ alert('Restore error: '+e); });
    } else if(kind === 'harddelete'){
      var state = (btn && btn.getAttribute('data-state')) || '';
      var address = (btn && btn.getAttribute('data-addr')) || '';
      if(!confirm('PERMANENTLY delete this property from the '+state.toUpperCase()+' CSV: '+address+'. This cannot be undone; re-uploading the CSV will bring it back.')) return;
      fetch('/api/hard-delete-property', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({state: state, address: address})
      }).then(function(r){return r.json().then(function(j){return {ok:r.ok, j:j};});})
        .then(function(res){
          if(res.ok){
            var row = document.getElementById('hide-row-'+id);
            if(row) row.remove();
            adminToast('Permanently removed from the '+state.toUpperCase()+' CSV.');
          } else {
            alert('Hard delete failed: '+(res.j && res.j.error || 'unknown'));
          }
        }).catch(function(e){ alert('Hard delete error: '+e); });
    }
  }
  </script>
  {% endif %}

  {% if section == 'earnings' %}
  <div class="card">
    <h2>Group earnings</h2>
    <p style="font-size:13px;color:#555;margin:6px 0 14px">What Radius (fees and build margin), Radius Maintenance, Haven SDA, Away Site Vision and Radius Real Estate earn from each property in a portfolio, as an Excel download. Only admins can open this page or the download. It uses the same figures as the portfolio (actuals once Under contract, each project&rsquo;s switches and build margin).</p>
    <table><thead><tr><th>Portfolio</th><th>Properties</th><th>Created by</th><th>Last changed</th><th></th></tr></thead>
    <tbody>
    {% for p in portfolios %}
      <tr><td><b>{{ p.name }}</b></td><td>{{ p.n }}</td><td>{{ p.created_by_name or '' }}</td><td>{{ (p.updated_at or '')[:10] }}</td>
      <td>{% if p.n %}<a href="/dashboard?earnings={{ p.id }}" target="_blank" style="background:#7F1D1D;color:#fff;padding:5px 12px;border-radius:5px;text-decoration:none;font-size:12px;font-weight:700">&#11015; Download group earnings</a>{% else %}<span style="color:#999;font-size:12px">empty</span>{% endif %}</td></tr>
      {% if p['props'] %}
      <tr><td colspan="5" style="padding:4px 10px 14px 28px;background:#fafafa">
        <div style="font-size:11px;font-weight:700;color:#7F1D1D;margin:4px 0">Radius build margin per house <span style="font-weight:400;color:#666">(standard ${{ '{:,.0f}'.format(std_margin) }}. Lowering it lowers that project&rsquo;s house build price by the same amount. Blank = standard.)</span></div>
        <table style="width:auto"><tbody>
        {% for it in p['props'] %}
          <tr><td style="font-size:12px;padding:3px 10px 3px 0">{{ it.address }}</td><td style="font-size:12px;color:#666;padding:3px 10px">{{ it.model_name }}</td>
          <td style="padding:3px 0"><form method="POST" action="/admin/earnings/margin" style="display:flex;gap:6px;align-items:center;margin:0">
            <input type="hidden" name="iid" value="{{ it.id }}">
            <input type="text" name="margin" value="{{ '%.0f'|format(it.margin) if it.margin is not none else '' }}" placeholder="standard" style="width:100px;padding:3px 6px;border:1px solid #fca5a5;border-radius:4px;font-size:12px;text-align:right">
            <button type="submit" style="padding:3px 10px;border:none;border-radius:4px;background:#7F1D1D;color:#fff;font-size:11px;cursor:pointer">Save</button>
          </form></td></tr>
        {% endfor %}
        </tbody></table></td></tr>
      {% endif %}
    {% else %}
      <tr><td colspan="5" style="color:#888">No portfolios yet.</td></tr>
    {% endfor %}
    </tbody></table>
    <p style="font-size:11px;color:#888;margin-top:10px">The download opens the screener in a new tab, builds the file and saves it. You can close that tab afterwards.</p>
  </div>
  {% endif %}

  {% if section == 'users' %}
  <div class="addform">
    <h2 style="margin-bottom:16px">Add team member</h2>
    <form method="POST" action="/admin/users/add_form">
      <div class="grid">
        <div><label>Full name</label><input name="full_name" placeholder="e.g. Sarah Johnson" required></div>
        <div><label>Username</label><input name="username" placeholder="e.g. sarah" required></div>
        <div><label>Password</label><input type="password" name="password" placeholder="Min 6 characters" required></div>
        <div><label>Role</label><select name="role"><option value="team">Team member</option><option value="admin">Admin</option></select></div>
        <div><label>&nbsp;</label><button type="submit" class="btn blue" style="width:100%;padding:9px">Add</button></div>
      </div>
    </form>
  </div>
  <div class="card">
    <h2>All users</h2>
    <table><thead><tr><th>Name</th><th>Username</th><th>Role</th><th>Status</th><th>Change password</th><th>Access</th></tr></thead>
    <tbody>
    {% for u in all_users %}
    <tr>
      <td><strong>{{ u.full_name }}</strong></td>
      <td>{{ u.username }}</td>
      <td>
        <span class="badge {{ 'ba' if u.role=='admin' else 'bt' }}">{{ u.role }}</span>
        {% if u.id != current_user.user_id %}
        <form class="inline" method="POST" action="/admin/users/{{ u.id }}/toggle_role" style="display:inline-block;margin-left:6px"
              onsubmit="return confirm('Change {{ u.full_name }} to {{ 'team member' if u.role=='admin' else 'admin' }}?')">
          <button type="submit" class="btn" style="padding:3px 9px;font-size:11px;background:#fff;border:1px solid #185FA5;color:#185FA5;font-weight:600">{{ '\u2192 Team' if u.role=='admin' else '\u2192 Admin' }}</button>
        </form>
        {% endif %}
      </td>
      <td><span class="badge {{ 'bact' if u.active else 'bina' }}">{{ 'Active' if u.active else 'Disabled' }}</span></td>
      <td>
        <form class="inline" method="POST" action="/admin/users/{{ u.id }}/password">
          <input type="password" name="password" placeholder="New password" class="pwfield">
          <button type="submit" class="btn blue">Update</button>
        </form>
      </td>
      <td>
        <form class="inline" method="POST" action="/admin/users/{{ u.id }}/toggle">
          <button type="submit" class="btn {{ 'red' if u.active else 'grn' }}">{{ 'Disable' if u.active else 'Enable' }}</button>
        </form>
      </td>
    </tr>
    {% else %}
    <tr><td colspan="6" style="color:#9CA3AF;padding:12px">No users yet</td></tr>
    {% endfor %}
    </tbody></table>
  </div>
  {% endif %}

</div>
</body>
</html>"""

UPLOAD_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Upload Data - SDA Screener</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#f3f4f6}
.top{background:#002060;color:#fff;padding:14px 24px;display:flex;justify-content:space-between;align-items:center}
.top h1{font-size:15px;font-weight:700}
.top a{color:#93c5fd;font-size:13px;text-decoration:none;margin-left:16px}
.wrap{max-width:900px;margin:0 auto;padding:24px}
.card{background:#fff;border-radius:8px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:16px}
.card h2{font-size:14px;font-weight:700;color:#002060;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}
.upload-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:20px}
.state-card{border:2px solid #e5e7eb;border-radius:8px;padding:16px;text-align:center}
.state-card.loaded{border-color:#0F6E56;background:#f0fdf4}
.state-name{font-size:18px;font-weight:800;color:#002060;margin-bottom:8px}
.state-rows{font-size:13px;color:#0F6E56;font-weight:600;margin-bottom:4px}
.state-date{font-size:11px;color:#6B7280;margin-bottom:12px}
.state-none{font-size:12px;color:#9CA3AF;margin-bottom:12px}
.upload-form{display:flex;flex-direction:column;gap:8px}
.upload-form input[type=file]{font-size:12px}
.btn{padding:8px 16px;border:none;border-radius:6px;cursor:pointer;font-size:12px;font-weight:700}
.blue{background:#002060;color:#fff;width:100%}
.msg{padding:10px 14px;border-radius:6px;margin-bottom:16px;font-size:13px}
.ok{background:#dcfce7;color:#166534;border:1px solid #86efac}
.er{background:#fee2e2;color:#991b1b;border:1px solid #fca5a5}
</style>
</head>
<body>
<div class="top">
  <h1>SDA Screener - Upload Property Data</h1>
  <div>
    <a href="/admin">Admin panel</a>
    <a href="/dashboard">Dashboard</a>
    <a href="/logout">Sign out</a>
  </div>
</div>
<div class="wrap">
  <div id="msg-area"></div>
  <div class="card">
    <h2>Upload CSV files for each state</h2>
    <p style="font-size:12px;color:#6B7280;margin-bottom:16px">Upload the *_screener_ready.csv files generated by process_rp_data.py. Once uploaded, all team members will see the data automatically when they log in.</p>
    <div class="upload-grid" id="state-grid"></div>
  </div>
</div>
<script>
var status = {{STATUS}};
var msg = '{{MSG}}';
var msgType = '{{MSG_TYPE}}';
var states = ['vic','nsw','qld'];
var labels = {vic:'VIC',nsw:'NSW',qld:'QLD'};

if(msg){
  var d = document.getElementById('msg-area');
  d.innerHTML = '<div class="msg '+msgType+'">'+decodeURIComponent(msg.replace(/[+]/g,' '))+'</div>';
}

var grid = document.getElementById('state-grid');
states.forEach(function(st){
  var s = status[st];
  var loaded = s && s.rows > 0;
  var html = '<div class="state-card '+(loaded?'loaded':'')+'">'
    +'<div class="state-name">'+labels[st]+'</div>';
  if(loaded){
    html += '<div class="state-rows">'+s.rows+' properties</div>'
      +'<div class="state-date">Uploaded: '+s.uploaded_at.substring(0,16)+' by '+s.uploaded_by+'</div>';
  } else {
    html += '<div class="state-none">No data uploaded yet</div>';
  }
  html += '<form class="upload-form" method="POST" action="/admin/upload" enctype="multipart/form-data">'
    +'<input type="hidden" name="state" value="'+st+'">'
    +'<input type="file" name="csvfile" accept=".csv" required>'
    +'<button type="submit" class="btn blue">'+(loaded?'Replace ':'Upload ')+labels[st]+' CSV</button>'
    +'</form></div>';
  grid.innerHTML += html;
});
</script>
</body></html>"""

UPLOAD_SDA_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Upload SDA Market - SDA Screener</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#f3f4f6}
.top{background:#002060;color:#fff;padding:14px 24px;display:flex;justify-content:space-between;align-items:center}
.top h1{font-size:15px;font-weight:700}
.top a{color:#93c5fd;font-size:13px;text-decoration:none;margin-left:16px}
.wrap{max-width:1100px;margin:0 auto;padding:24px}
.card{background:#fff;border-radius:8px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:16px}
.card h2{font-size:14px;font-weight:700;color:#002060;margin-bottom:8px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}
.layer-section{margin-bottom:24px}
.layer-title{font-size:13px;font-weight:700;color:#002060;margin:18px 0 10px;padding:6px 10px;border-radius:4px;display:inline-flex;align-items:center;gap:6px}
.layer-title.radius{background:#dbeafe;color:#1e40af}
.layer-title.existing{background:#dcfce7;color:#166534}
.layer-title.ghomes{background:#ede9fe;color:#5b21b6}
.layer-title.permitted{background:#fef9c3;color:#854d0e}
.dot{width:10px;height:10px;border-radius:50%}
.dot.radius{background:#1e40af}
.dot.existing{background:#0F6E56}
.dot.ghomes{background:#7C3AED}
.dot.permitted{background:#EAB308}
.upload-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:8px}
.state-card{border:2px solid #e5e7eb;border-radius:8px;padding:12px;text-align:center}
.state-card.loaded{border-color:#0F6E56;background:#f0fdf4}
.state-name{font-size:14px;font-weight:800;color:#002060;margin-bottom:6px}
.state-pins{font-size:12px;color:#0F6E56;font-weight:600;margin-bottom:2px}
.state-date{font-size:10px;color:#6B7280;margin-bottom:8px}
.state-none{font-size:11px;color:#9CA3AF;margin-bottom:8px}
.upload-form{display:flex;flex-direction:column;gap:6px}
.upload-form input[type=file]{font-size:11px}
.btn{padding:7px 12px;border:none;border-radius:6px;cursor:pointer;font-size:11px;font-weight:700}
.blue{background:#002060;color:#fff;width:100%}
.msg{padding:10px 14px;border-radius:6px;margin-bottom:16px;font-size:13px}
.ok{background:#dcfce7;color:#166534;border:1px solid #86efac}
.er{background:#fee2e2;color:#991b1b;border:1px solid #fca5a5}
.help{font-size:11px;color:#6B7280;line-height:1.5;background:#f9fafb;padding:10px 14px;border-radius:6px;margin-bottom:14px;border-left:3px solid #185FA5}
</style>
</head>
<body>
<div class="top">
  <h1>SDA Screener - Upload SDA Market Data</h1>
  <div>
    <a href="/admin">Admin panel</a>
    <a href="/admin/upload_page">Property data</a>
    <a href="/dashboard">Dashboard</a>
    <a href="/logout">Sign out</a>
  </div>
</div>
<div class="wrap">
  <div id="msg-area"></div>

  <div class="card">
    <h2>SDA Market Map data</h2>
    <p class="help">Four pin layers for the SDA Market Map: <strong>Radius</strong> (your own pipeline + built projects), <strong>Existing SDA</strong> (operating, filled SDA dwellings), <strong>Group Homes</strong> (non-SDA disability accommodation), <strong>Permitted/approved</strong> (approved but not yet built). Upload one CSV per layer-state combination. Each upload <strong>replaces</strong> all pins for that layer+state. CSVs should be LandChecker-format with at minimum: Address, Suburb, State, Coordinates (the lng,lat pair).</p>
    <div id="layer-areas"></div>
  </div>
</div>
<script>
var status = {{STATUS}};
var msg = '{{MSG}}';
var msgType = '{{MSG_TYPE}}';
var states = ['vic','nsw','qld'];
var stateLabels = {vic:'VIC',nsw:'NSW',qld:'QLD'};
var layers = [
  {key:'radius',    label:'Radius pipeline / built'},
  {key:'existing',  label:'Existing SDA'},
  {key:'ghomes',    label:'Group Homes'},
  {key:'permitted', label:'Permitted / approved'}
];
if(msg){
  var d = document.getElementById('msg-area');
  d.innerHTML = '<div class="msg '+msgType+'">'+decodeURIComponent(msg.replace(/[+]/g,' '))+'</div>';
}

var areas = document.getElementById('layer-areas');
layers.forEach(function(L){
  var section = '<div class="layer-section">'
    + '<div class="layer-title '+L.key+'"><span class="dot '+L.key+'"></span>'+L.label+'</div>'
    + '<div class="upload-grid">';
  states.forEach(function(st){
    var s = (status[L.key] && status[L.key][st]) || null;
    var loaded = s && s.pins > 0;
    var html = '<div class="state-card '+(loaded?'loaded':'')+'">'
      + '<div class="state-name">'+stateLabels[st]+'</div>';
    if(loaded){
      html += '<div class="state-pins">'+s.pins+' pins</div>'
        + '<div class="state-date">Uploaded: '+s.uploaded_at.substring(0,16)+' by '+s.uploaded_by+'</div>';
    } else {
      html += '<div class="state-none">No data uploaded</div>';
    }
    html += '<form class="upload-form" method="POST" action="/admin/upload_sda" enctype="multipart/form-data">'
      + '<input type="hidden" name="layer" value="'+L.key+'">'
      + '<input type="hidden" name="state" value="'+st+'">'
      + '<input type="file" name="csvfile" accept=".csv" required>'
      + '<button type="submit" class="btn blue">'+(loaded?'Replace ':'Upload ')+stateLabels[st]+'</button>'
      + '</form></div>';
    section += html;
  });
  section += '</div></div>';
  areas.innerHTML += section;
});
</script>
</body></html>"""

"""SDA Property Screener - Team Server"""
from flask import Flask, request, session, redirect, url_for, jsonify, send_file, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import Template
import sqlite3, json, os, datetime, secrets, math, csv, io
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Database location.
#
# Background: Railway (and most modern PaaS — Heroku, Render, Fly.io,
# Cloud Run) runs containers with an EPHEMERAL filesystem. Anything written
# to disk inside the container is lost on every redeploy, daily container
# recycle, or scale-from-zero. Before this fix, usage.db lived next to
# app.py inside the container, so every restart wiped users, sessions,
# manual properties, hidden properties, uploaded CSV data, shortlists, the
# SDA market data, and the SDA supply snapshot.
#
# Fix: read the path from DB_PATH so it can be pointed at a mounted Railway
# Volume (which IS persistent across deploys/restarts). To migrate without
# data loss:
#   1. In Railway, attach a Volume to the service (Settings → Volumes).
#      Pick any mount path, e.g. /data.
#   2. Set the DB_PATH environment variable on the service to that path
#      plus a filename, e.g. /data/usage.db.
#   3. Redeploy. On first run init_db() creates the schema in the new
#      location. (If you had existing data worth keeping you would copy
#      usage.db onto the volume BEFORE the redeploy via a one-off shell
#      session — see RAILWAY_VOLUME_SETUP.md.)
#
# Local dev keeps working: with no DB_PATH set, it falls back to the
# repo-local usage.db exactly as before.
DB = os.environ.get('DB_PATH') or os.path.join(os.path.dirname(__file__), 'usage.db')

# Make sure the parent directory exists. Railway Volumes are mounted by
# the platform so the directory will already exist there, but creating it
# defensively keeps local-dev and other deploy targets working when the
# user points DB_PATH at a fresh location.
_db_dir = os.path.dirname(os.path.abspath(DB))
if _db_dir and not os.path.exists(_db_dir):
    try:
        os.makedirs(_db_dir, exist_ok=True)
    except OSError:
        pass  # If we can't create it, the sqlite3.connect below will surface a clearer error

# How often (in seconds) the login_required decorator refreshes a session's
# last_active timestamp. Previously this fired on every single request, which
# caused "database is locked" errors under multi-user load on SQLite. 60s of
# precision is plenty for "is this user currently active" — the admin Team
# activity view shows times rounded to the minute anyway.
SESSION_TOUCH_SECONDS = 60

# Google Maps Platform API key — read from environment (set on Railway).
# Used for: Geocoding, Places (New) Nearby Search, and Maps Static API.
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')

def get_db():
    # timeout=10 makes Python wait up to 10s for the file lock before raising
    # OperationalError. busy_timeout sets the same at the SQLite engine level.
    # WAL mode (persisted to the DB file on first connect) lets readers and a
    # single writer work concurrently without blocking each other; this is the
    # main fix for the "database is locked" errors we were seeing under
    # multi-user load with the default rollback-journal mode.
    db = sqlite3.connect(DB, timeout=10.0)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA busy_timeout=5000')
    db.execute('PRAGMA journal_mode=WAL')
    db.execute('PRAGMA synchronous=NORMAL')
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
        CREATE TABLE IF NOT EXISTS property_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT UNIQUE NOT NULL,
            csv_data TEXT NOT NULL,
            row_count INTEGER DEFAULT 0,
            uploaded_by TEXT,
            uploaded_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS shortlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            property_ids TEXT DEFAULT '[]',
            dd_data TEXT DEFAULT '{}',
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS sda_market (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            layer TEXT NOT NULL,           -- 'radius' | 'existing' | 'permitted'
            state TEXT NOT NULL,           -- vic | nsw | qld
            address TEXT NOT NULL,
            suburb TEXT,
            postcode TEXT,
            area_m2 REAL,
            frontage_m REAL,
            planning_zones TEXT,
            notes TEXT,
            lat REAL,
            lng REAL,
            uploaded_by TEXT,
            uploaded_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_sda_market_layer ON sda_market(layer);
        CREATE INDEX IF NOT EXISTS idx_sda_market_state ON sda_market(state);
        -- Soft-delete: any logged-in user can hide a property with a required reason.
        -- Admins can review the list and restore (delete this row) or hard-delete
        -- (remove from property_data CSV blob entirely). Non-admins may un-hide
        -- only their own hide within HIDE_UNDO_SECONDS of creating it.
        CREATE TABLE IF NOT EXISTS hidden_properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            address TEXT NOT NULL,
            address_key TEXT NOT NULL,        -- lowercased + trimmed address for matching
            hidden_by_id INTEGER NOT NULL,
            hidden_by_name TEXT NOT NULL,
            hidden_at TEXT DEFAULT (datetime('now')),
            reason TEXT NOT NULL,
            FOREIGN KEY (hidden_by_id) REFERENCES users(id)
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_hidden_properties_unique
            ON hidden_properties(state, address_key);
        -- C2: manually-added properties (separate from CSV blobs in
        -- property_data). The screener pipeline treats these as first-class
        -- rows once they are merged client-side. Address is the matching
        -- key shared with hidden_properties so C1 hide/restore endpoints
        -- work on them with no extra plumbing.
        CREATE TABLE IF NOT EXISTS manual_properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,                 -- vic | nsw | qld
            address TEXT NOT NULL,
            address_key TEXT NOT NULL,           -- normalised for matching
            suburb TEXT NOT NULL,
            postcode TEXT,
            price REAL NOT NULL,
            land REAL NOT NULL,
            design_type TEXT NOT NULL,           -- 2p | 3p | dp | d3 | hv
            sale_type TEXT NOT NULL,             -- Private Sale | Auction | Off-market | EOI
            auction_date TEXT,                   -- only when sale_type=Auction
            sa4 TEXT,
            sa3 TEXT,
            lat REAL,
            lng REAL,
            hosp1_name TEXT, hosp1_km REAL,
            hosp2_name TEXT, hosp2_km REAL,
            hosp3_name TEXT, hosp3_km REAL,
            medical_name TEXT, medical_km REAL,
            shop_name TEXT, shop_km REAL,
            train_name TEXT, train_km REAL,
            bus_km REAL,
            tram_name TEXT, tram_km REAL,
            created_by_id INTEGER NOT NULL,
            created_by_name TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            last_edited_by_id INTEGER,
            last_edited_by_name TEXT,
            last_edited_at TEXT,
            FOREIGN KEY (created_by_id) REFERENCES users(id),
            FOREIGN KEY (last_edited_by_id) REFERENCES users(id)
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_manual_properties_unique
            ON manual_properties(state, address_key);
        CREATE INDEX IF NOT EXISTS idx_manual_properties_state
            ON manual_properties(state);
        -- C3: SA2-level SDA supply & demand snapshot
        -- One row per (state, SA2). data_json holds the full aggregation:
        --   counts, deficit, provider lists, design-category mix.
        -- The full table is sent to the client on dashboard load so badge
        -- rendering and panel display happen instantly without per-row
        -- API calls. The blob is keyed off (state, SA2) because the same
        -- SA2 name CAN repeat across states (e.g. "Wellington" in NSW vs VIC).
        CREATE TABLE IF NOT EXISTS sda_supply (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,            -- vic | nsw | qld
            sa2 TEXT NOT NULL,
            sa3 TEXT,
            sa4 TEXT,
            data_json TEXT NOT NULL,        -- aggregated supply blob
            data_as_of TEXT,                -- date from the source files (e.g. 2025-12-31)
            uploaded_by TEXT,
            uploaded_at TEXT DEFAULT (datetime('now'))
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_sda_supply_unique
            ON sda_supply(state, sa2);

        -- Performl SA3 market snapshot (INTERNAL ONLY - never rendered on
        -- partner / investor / Supavest docs). One row per (state, SA3).
        -- Performl publishes on ABS 2016 SA3s; names were checked to match
        -- the screener's SA3D names for VIC/NSW/QLD. data_as_of = demand /
        -- supply date, vacancy_as_of = vacancy measurement date.
        CREATE TABLE IF NOT EXISTS performl_sa3 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,            -- vic | nsw | qld | sa | wa | tas | nt | act
            sa3 TEXT NOT NULL,
            sa4 TEXT,
            data_json TEXT NOT NULL,
            data_as_of TEXT,
            vacancy_as_of TEXT,
            uploaded_by TEXT,
            uploaded_at TEXT DEFAULT (datetime('now'))
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_performl_sa3_unique
            ON performl_sa3(state, sa3);

        -- Performl SDA provider register, aggregated per (state, SA2) with the
        -- provider dimension dropped. INTERNAL ONLY. data_json is a list of
        -- [dwelling_type, building_stock, design_category, places, vacant, dwellings].
        -- SA2 -> SA3 mapping happens in the dashboard (suburb tables).
        CREATE TABLE IF NOT EXISTS performl_register (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            sa2 TEXT NOT NULL,
            sa4 TEXT,
            data_json TEXT NOT NULL,
            data_as_of TEXT,
            uploaded_by TEXT,
            uploaded_at TEXT DEFAULT (datetime('now'))
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_performl_register_unique
            ON performl_register(state, sa2);

        -- Same register, provider-level (one row per register line). INTERNAL
        -- ONLY - powers the Providers tab and "largest providers" on the card.
        CREATE TABLE IF NOT EXISTS performl_providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            sa2 TEXT NOT NULL,
            sa4 TEXT,
            provider TEXT NOT NULL,
            dwelling_type TEXT,
            building_stock TEXT,
            design_category TEXT,
            places INTEGER DEFAULT 0,
            vacant INTEGER DEFAULT 0,
            dwellings INTEGER DEFAULT 0,
            website TEXT,
            email TEXT,
            phone TEXT,
            data_as_of TEXT,
            res_bed TEXT,                  -- e.g. 'Residents 3, Bedrooms unspecified'
            sprinklers TEXT,
            ooa TEXT,
            breakout TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_performl_providers_name
            ON performl_providers(provider);

        -- Partner one-pager: per-property reference code (RAD-####), keyed by
        -- (state, address_key) like hidden/manual so it survives weekly CSV
        -- re-uploads. The code is opaque and global; it never encodes partner
        -- or suburb. 'seq' is the numeric part, used for MAX()+1 allocation.
        CREATE TABLE IF NOT EXISTS partner_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            address TEXT NOT NULL,
            address_key TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE,
            seq INTEGER NOT NULL UNIQUE,
            created_by_id INTEGER,
            created_by_name TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_partner_codes_addr
            ON partner_codes(state, address_key);

        -- One row per (property, partner) introduction event. Powers the audit
        -- trail / reverse lookup ("Introduced to Supavest on [date] by [who]").
        -- The unique index dedupes repeat generations for the same partner.
        CREATE TABLE IF NOT EXISTS introductions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            address TEXT NOT NULL,
            address_key TEXT NOT NULL,
            partner_name TEXT NOT NULL,
            introduced_by_id INTEGER,
            introduced_by_name TEXT,
            introduced_at TEXT DEFAULT (datetime('now'))
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_introductions_unique
            ON introductions(state, address_key, partner_name);

        -- Partner doc snapshots: the evidential record of every partner-facing
        -- document generated, so a doc can be RETRIEVED rather than
        -- regenerated. This matters because regenerating is not reproducible —
        -- build costs, NDIS rates, the offer price, the cap rate, Supavest's
        -- interest rate and the renderer itself all change over time, so
        -- hitting Generate again weeks later produces a different document
        -- that looks the same.
        --
        -- pdf_blob is the exact bytes that were sent. snapshot_json holds the
        -- inputs behind them (PARAMS, SH, SUPAVEST, price, model, cap rate)
        -- plus BOTH the partner-facing figures and the internal ones (true
        -- cost excluding any build uplift, developer profit, POC, IRR), which
        -- is what makes the document reconstructable years later.
        --
        -- The address is stored on this row directly, not just joined from
        -- partner_codes, so each snapshot is self-describing and survives any
        -- drift or damage to the code index.
        CREATE TABLE IF NOT EXISTS partner_doc_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            seq INTEGER,
            state TEXT NOT NULL,
            address TEXT NOT NULL,
            address_key TEXT NOT NULL,
            doc_type TEXT NOT NULL,          -- 'supavest' | 'partner'
            partner_name TEXT,
            version INTEGER NOT NULL,        -- increments per (code, doc_type)
            pdf_filename TEXT,
            pdf_bytes INTEGER,
            pdf_blob BLOB NOT NULL,
            snapshot_json TEXT NOT NULL,
            renderer_version TEXT,
            generated_by_id INTEGER,
            generated_by_name TEXT,
            generated_at TEXT DEFAULT (datetime('now')),
            onedrive_status TEXT,      -- NULL | 'ok' | 'failed' | 'disabled'
            onedrive_url TEXT,
            onedrive_error TEXT,
            onedrive_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_pds_code ON partner_doc_snapshots(code);
        CREATE INDEX IF NOT EXISTS idx_pds_addr ON partner_doc_snapshots(state, address_key);
        CREATE UNIQUE INDEX IF NOT EXISTS idx_pds_version
            ON partner_doc_snapshots(code, doc_type, version);

        -- Portfolios (Stage 1). A named group of properties with a master feaso.
        -- Visible to every logged-in user; editable by admins and the creator
        -- only (enforced in the API below, not just the UI).
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_by_id INTEGER NOT NULL,
            created_by_name TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            equity_type TEXT,            -- 'amount' | 'pct' | NULL (= use screener LVR)
            equity_value REAL,           -- dollars, or percent of TDC (0-100)
            FOREIGN KEY (created_by_id) REFERENCES users(id)
        );

        -- Automatic site check (Vicmap open data), cached per address.
        CREATE TABLE IF NOT EXISTS site_checks (
            address_key TEXT PRIMARY KEY,
            state TEXT,
            address TEXT,
            result_json TEXT,
            checked_at TEXT,
            checked_by TEXT
        );

        -- One row per property in a portfolio. snapshot_json is a full copy of
        -- the property taken when it was added (address byte-for-byte, price,
        -- land, SA4/SA3, NDIS SDA rates, category) so a listing that drops out
        -- of the weekly RP Data CSV once sold is never lost from a portfolio.
        -- 'model' is the CURRENT build model for the line (editable); the
        -- model at the time of adding stays inside the snapshot.
        CREATE TABLE IF NOT EXISTS portfolio_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_id INTEGER NOT NULL,
            state TEXT NOT NULL,
            address TEXT NOT NULL,
            address_key TEXT NOT NULL,
            model TEXT NOT NULL,
            snapshot_json TEXT NOT NULL,
            occupancy TEXT,              -- JSON {il,fa,hps} residents now; NULL = full house
            status TEXT DEFAULT 'target', -- target, offer, contract, settled, design, construction, complete
            actuals TEXT,                -- JSON {price, stamp, build, cons, rents:{il:[..],fa:[..],hps:[..],villa}}
            added_by_id INTEGER,
            added_by_name TEXT,
            added_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_portfolio_items_unique
            ON portfolio_items(portfolio_id, state, address_key);
        CREATE INDEX IF NOT EXISTS idx_portfolio_items_pid
            ON portfolio_items(portfolio_id);
    """)
    db.commit()

    # Additive column migrations. CREATE TABLE IF NOT EXISTS won't add columns
    # to a table that already exists, so anyone who deployed the snapshot table
    # before the SharePoint sync landed needs these added in place.
    def _ensure_columns(table, columns):
        try:
            have = {r[1] for r in db.execute('PRAGMA table_info(%s)' % table).fetchall()}
        except sqlite3.OperationalError:
            return  # table doesn't exist yet; CREATE TABLE above will have made it
        for name, decl in columns:
            if name not in have:
                try:
                    db.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table, name, decl))
                except sqlite3.OperationalError as e:
                    app.logger.warning('Could not add %s.%s: %s', table, name, e)
        db.commit()

    _ensure_columns('performl_providers', [
        ('res_bed', 'TEXT'), ('sprinklers', 'TEXT'), ('ooa', 'TEXT'), ('breakout', 'TEXT'),
    ])
    _ensure_columns('portfolio_items', [('occupancy', 'TEXT'), ('status', "TEXT DEFAULT 'target'"), ('actuals', 'TEXT'), ('itemised', 'TEXT'), ('margin', 'REAL')])
    _ensure_columns('portfolios', [('equity_type', 'TEXT'), ('equity_value', 'REAL')])
    _ensure_columns('partner_doc_snapshots', [
        ('onedrive_status', 'TEXT'),
        ('onedrive_url', 'TEXT'),
        ('onedrive_error', 'TEXT'),
        ('onedrive_at', 'TEXT'),
    ])

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
        # One DB connection for both the read and the (throttled) write.
        # Previously this used two separate connections per request which
        # multiplied lock contention under concurrent users.
        db = get_db()
        try:
            sess = db.execute(
                'SELECT s.*,u.username,u.full_name,u.role,u.active FROM sessions s '
                'JOIN users u ON s.user_id=u.id WHERE s.session_token=? AND s.logout_at IS NULL', (token,)
            ).fetchone()
            if not sess or not sess['active']:
                session.clear()
                return redirect(url_for('login'))
            # Throttle the last_active write to once per SESSION_TOUCH_SECONDS.
            # Refreshing the timestamp on every single request was the main
            # cause of "database is locked" errors — every page load, every
            # api/log POST, every api/me poll was queueing an UPDATE on the
            # sessions table. Sub-minute precision on last_active isn't
            # operationally useful, so we now only write when it's stale.
            # Wrapped in try/except so a transient lock here never 500s the
            # actual page the user is trying to view.
            try:
                now = datetime.datetime.utcnow()
                last_active_str = sess['last_active']
                stale = True
                if last_active_str:
                    try:
                        last_active = datetime.datetime.fromisoformat(last_active_str)
                        stale = (now - last_active).total_seconds() >= SESSION_TOUCH_SECONDS
                    except (ValueError, TypeError):
                        stale = True
                if stale:
                    db.execute('UPDATE sessions SET last_active=? WHERE session_token=?',
                               (now.isoformat(), token))
                    db.commit()
            except sqlite3.OperationalError as e:
                # DB locked / busy / etc — last_active refresh is non-critical,
                # log it and continue. Without this guard the lock would
                # propagate as a 500 on every request.
                app.logger.warning('session last_active refresh skipped: %s', e)
        finally:
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

def get_dashboard_html():
    # Serve the repo file FIRST so that committing dashboard.html to GitHub
    # actually updates the live dashboard on redeploy (this is the real deploy
    # path). Fall back to a copy stored in the DB config (legacy path, no longer
    # has an upload UI), then to a placeholder.
    p = os.path.join(os.path.dirname(__file__), 'dashboard.html')
    if os.path.exists(p):
        with open(p) as f:
            return f.read()
    db = get_db()
    row = db.execute("SELECT value FROM config WHERE key='dashboard_html'").fetchone()
    db.close()
    if row and row['value']:
        return row['value']
    return '<h1>Dashboard not loaded. Upload via admin panel.</h1>'


# ===========================================================================
# Soft-delete (hide) helpers
# ---------------------------------------------------------------------------
# Any logged-in user can hide a property from the screener by giving a reason.
# Admins can review the hidden list and restore (un-hide) or hard-delete
# (permanently remove the row from the CSV blob in property_data).
# Non-admins can un-hide only their own hide within HIDE_UNDO_SECONDS of
# creating it (powers the "Undo" toast immediately after hiding by mistake).
# ===========================================================================
HIDE_UNDO_SECONDS = 300  # 5 minutes — covers the 8-second undo toast plus slack

def _address_key(addr):
    """Normalise an address into a stable matching key.

    The CSV has free-text addresses with arbitrary whitespace, quoting, and
    case. We lower-case, collapse internal whitespace, and trim. Anything
    fancier (postcode-stripping, fuzzy match) would risk false positives;
    keep it strict so 'hide' only hits the exact row the user clicked."""
    if not addr:
        return ''
    return ' '.join(str(addr).strip().lower().split())

def _get_hidden_address_keys(state):
    """Return a set of normalised address keys hidden for the given state."""
    db = get_db()
    rows = db.execute(
        'SELECT address_key FROM hidden_properties WHERE state=?', (state,)
    ).fetchall()
    db.close()
    return {r['address_key'] for r in rows}

def _strip_hidden_from_csv(csv_data, hidden_keys, addr_col_candidates=('address', 'street address', 'street')):
    """Remove rows from a CSV blob whose Address column matches a hidden key.

    Mirrors the column-detection logic the dashboard uses client-side
    (processText in dashboard.html). Returns (new_csv_text, removed_count)."""
    if not csv_data or not hidden_keys:
        return csv_data, 0
    lines = csv_data.split('\n')
    if not lines:
        return csv_data, 0
    # Find header line (first non-empty line)
    header_idx = 0
    while header_idx < len(lines) and not lines[header_idx].strip():
        header_idx += 1
    if header_idx >= len(lines):
        return csv_data, 0
    header = lines[header_idx]
    cols = [c.strip().strip('"').lower() for c in header.split(',')]
    addr_idx = -1
    for cand in addr_col_candidates:
        for i, col in enumerate(cols):
            if col == cand or cand in col:
                addr_idx = i
                break
        if addr_idx >= 0:
            break
    if addr_idx < 0:
        # Couldn't find address column — leave CSV untouched rather than
        # silently dropping rows.
        return csv_data, 0
    out_lines = lines[:header_idx + 1]
    removed = 0
    for line in lines[header_idx + 1:]:
        if not line.strip():
            out_lines.append(line)
            continue
        # Same naive CSV-with-quoted-fields parse the dashboard uses
        cells, cur, in_q = [], '', False
        for ch in line:
            if ch == '"':
                in_q = not in_q
            elif ch == ',' and not in_q:
                cells.append(cur.strip())
                cur = ''
            else:
                cur += ch
        cells.append(cur.strip())
        addr_val = cells[addr_idx] if addr_idx < len(cells) else ''
        addr_val = addr_val.replace('"', '')
        if _address_key(addr_val) in hidden_keys:
            removed += 1
            continue
        out_lines.append(line)
    return '\n'.join(out_lines), removed


# ===========================================================================
# Google Maps proxy helpers
# ---------------------------------------------------------------------------
# These run server-side so the Google API key is never exposed to the browser
# and HTTP-referer key restrictions don't apply (since requests originate from
# Railway's server IP, not from a browser).
# ===========================================================================

def _http_get_json(url, timeout=10):
    """GET a URL and return parsed JSON. Returns dict with 'error' key on failure."""
    try:
        req = Request(url, headers={'User-Agent': 'SDA-Screener/1.0'})
        with urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode('utf-8'))
    except HTTPError as e:
        return {'error': f'HTTP {e.code}: {e.reason}'}
    except URLError as e:
        return {'error': f'Network: {e.reason}'}
    except Exception as e:
        return {'error': str(e)}

def _http_post_json(url, body, headers=None, timeout=10):
    """POST JSON body and return parsed JSON. Returns dict with 'error' key on failure."""
    try:
        data = json.dumps(body).encode('utf-8')
        req_headers = {'Content-Type': 'application/json', 'User-Agent': 'SDA-Screener/1.0'}
        if headers:
            req_headers.update(headers)
        req = Request(url, data=data, headers=req_headers, method='POST')
        with urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode('utf-8'))
    except HTTPError as e:
        body_text = ''
        try:
            body_text = e.read().decode('utf-8')[:500]
        except Exception:
            pass
        return {'error': f'HTTP {e.code}: {e.reason}', 'body': body_text}
    except URLError as e:
        return {'error': f'Network: {e.reason}'}
    except Exception as e:
        return {'error': str(e)}

def _haversine_km(lat1, lng1, lat2, lng2):
    """Straight-line distance in km between two lat/lng points."""
    R = 6371.0
    rlat1, rlat2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlng/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

@app.route('/api/geocode')
@login_required
def api_geocode():
    """Geocode an address to lat/lng. Returns {lat, lng} or {error}."""
    if not GOOGLE_MAPS_API_KEY:
        return jsonify({'error': 'GOOGLE_MAPS_API_KEY not configured on server'}), 500
    addr = (request.args.get('address') or '').strip()
    if not addr:
        return jsonify({'error': 'Missing address parameter'}), 400
    url = ('https://maps.googleapis.com/maps/api/geocode/json'
           '?address=' + quote_plus(addr + ', Australia') +
           '&key=' + GOOGLE_MAPS_API_KEY)
    data = _http_get_json(url)
    if 'error' in data:
        return jsonify({'error': data['error']}), 502
    if data.get('status') != 'OK' or not data.get('results'):
        return jsonify({'error': 'Geocode status: ' + data.get('status', 'unknown'),
                        'message': data.get('error_message', '')}), 502
    loc = data['results'][0]['geometry']['location']
    return jsonify({'lat': loc['lat'], 'lng': loc['lng']})

# ======================================================== automatic site check
# Victoria only for now. Looks up the title lot, planning zone and overlays for
# an address from Vicmap open data (Victorian Government, CC BY 4.0) and scores
# it Pass / Check / Fail against the screener's site rules (sent by the
# dashboard). Results are cached per address in site_checks.
SC_WFS = 'https://opendata.maps.vic.gov.au/geoserver/wfs'
SC_FAIL_OVERLAYS = {'HO': 'Heritage Overlay', 'PAO': 'Public Acquisition Overlay'}
SC_CHECK_OVERLAYS = {
    'LSIO': 'Land Subject to Inundation (flood)', 'FO': 'Floodway Overlay',
    'SBO': 'Special Building Overlay (flood)', 'BMO': 'Bushfire Management Overlay',
    'EAO': 'Environmental Audit Overlay (possible contamination)',
    'VPO': 'Vegetation Protection Overlay', 'SLO': 'Significant Landscape Overlay',
    'ESO': 'Environmental Significance Overlay', 'NCO': 'Neighbourhood Character Overlay',
    'EMO': 'Erosion Management Overlay', 'SMO': 'Salinity Management Overlay',
    'DPO': 'Development Plan Overlay',
}
SC_OK_ZONES = ('GRZ', 'NRZ', 'RGZ', 'MUZ', 'TZ', 'ACZ', 'CDZ', 'UGZ', 'CCZ', 'PDZ', 'SUZ', 'HCTZ')
SC_CHECK_ZONES = {'LDRZ': 'Low Density Residential (check sewer and minimum lot size)',
                  'RLZ': 'Rural Living (check sewer and minimum lot size)'}
_SC_LAYERS = {}


def _sc_layers():
    if _SC_LAYERS:
        return _SC_LAYERS
    import re as _re
    url = SC_WFS + '?service=WFS&version=1.1.0&request=GetCapabilities'
    req = Request(url, headers={'User-Agent': 'SDA-Screener/1.0'})
    with urlopen(req, timeout=60) as r:
        xml = r.read().decode('utf-8', 'replace')
    names = _re.findall(r'<(?:wfs:)?Name>([^<]+)</(?:wfs:)?Name>', xml)

    def pick(prefer, must):
        for c in prefer:
            if c in names:
                return c
        for n in names:
            if all(k in n.lower() for k in must):
                return n
        return None
    found = {
        'parcel': pick(['open-data-platform:v_parcel_mp', 'open-data-platform:parcel_mp'], ['parcel']),
        'zone': pick(['open-data-platform:plan_zone'], ['plan_zone']),
        'overlay': pick(['open-data-platform:plan_overlay'], ['plan_overlay']),
    }
    missing = [k for k, v in found.items() if not v]
    if missing:
        seen = ', '.join(n for n in names if any(w in n.lower() for w in ('parcel', 'plan', 'property')))[:500]
        raise RuntimeError('Vicmap layer(s) not found: %s. Seen: %s' % (', '.join(missing), seen or 'none'))
    _SC_LAYERS.update(found)
    return _SC_LAYERS


def _sc_features(layer, minx, miny, maxx, maxy):
    def get(bbox):
        q = ('service=WFS&version=1.1.0&request=GetFeature&outputFormat=application/json'
             '&srsName=EPSG:4326&maxFeatures=60&typeName=' + quote_plus(layer) + '&bbox=' + quote_plus(bbox))
        d = _http_get_json(SC_WFS + '?' + q, timeout=30)
        if 'error' in d and 'features' not in d:
            raise RuntimeError('Vicmap: ' + str(d['error']))
        return d.get('features') or []
    feats = get('%f,%f,%f,%f,EPSG:4326' % (minx, miny, maxx, maxy))
    if not feats:
        feats = get('%f,%f,%f,%f,EPSG:4326' % (miny, minx, maxy, maxx))
    return feats


def _sc_polys(geom):
    if not geom:
        return []
    t, c = geom.get('type'), geom.get('coordinates') or []
    if t == 'Polygon':
        return [[[tuple(p[:2]) for p in ring] for ring in c]]
    if t == 'MultiPolygon':
        return [[[tuple(p[:2]) for p in ring] for ring in poly] for poly in c]
    return []


def _sc_in_ring(pt, ring):
    x, y = pt
    inside = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-12) + x1:
            inside = not inside
    return inside


def _sc_in_poly(pt, poly):
    return _sc_in_ring(pt, poly[0]) and not any(_sc_in_ring(pt, h) for h in poly[1:])


def _sc_area(ring):
    a = 0.0
    for i in range(len(ring) - 1):
        a += ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1]
    return a / 2.0


def _sc_min_rect(points):
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in points))
    if len(pts) < 3:
        return 0, 0, 0

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    hull = lo[:-1] + hi[:-1]
    best = None
    for i in range(len(hull)):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1) % len(hull)]
        ang = math.atan2(y2 - y1, x2 - x1)
        c, s_ = math.cos(-ang), math.sin(-ang)
        xs = [x * c - y * s_ for x, y in hull]
        ys = [x * s_ + y * c for x, y in hull]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        if best is None or w * h < best[2]:
            best = (min(w, h), max(w, h), w * h)
    return best


def _sc_shrink(ring, metres=1.0):
    cx = sum(p[0] for p in ring) / len(ring)
    cy = sum(p[1] for p in ring) / len(ring)
    out = []
    for x, y in ring:
        d = math.hypot(x - cx, y - cy) or 1
        k = max(0.0, (d - metres) / d)
        out.append((cx + (x - cx) * k, cy + (y - cy) * k))
    return out


def _sc_code(props):
    keys = {k.lower(): v for k, v in (props or {}).items()}
    for k in ('zone_code', 'zone_cod', 'overlay_code', 'ovl_code', 'code'):
        if keys.get(k):
            return str(keys[k]).upper()
    return ''


def _sc_base(code):
    return ''.join(ch for ch in (code or '').upper() if ch.isalpha())


def _site_check(address, lat, lng, listed_land, rules):
    """Run the checks. rules = {model: {label, minFrontage, minDepth, minLand}}."""
    r = {'address': address, 'result': 'Unknown', 'fails': [], 'checks': [], 'notes': [],
         'frontage': None, 'depth': None, 'lot_area': None, 'fits': [], 'zone': '', 'overlays': '',
         'lat': lat, 'lng': lng, 'source': 'Vicmap open data (Victorian Government)'}
    L = _sc_layers()
    kx, ky = 111320.0 * math.cos(math.radians(lat)), 110574.0

    def xy(p):
        return ((p[0] - lng) * kx, (p[1] - lat) * ky)
    d = 0.0004
    best = None
    feats = _sc_features(L['parcel'], lng - d, lat - d, lng + d, lat + d)
    for f in feats:
        for poly in _sc_polys(f.get('geometry')):
            if _sc_in_poly((lng, lat), poly):
                rings = [[xy(p) for p in ring] for ring in poly]
                a = abs(_sc_area(rings[0]))
                if a > 5 and (best is None or a < best[0]):
                    best = (a, rings, poly)
    if not best:
        raise RuntimeError('No title lot found at the address point (%d parcels nearby)' % len(feats))
    area, rings, poly_ll = best
    short, long_, rect = _sc_min_rect([p for rg in rings for p in rg])
    r['lot_area'], r['frontage'], r['depth'] = round(area), round(short, 1), round(long_, 1)
    if rect and area / rect < 0.85:
        r['checks'].append('Irregular lot shape (%d%% of its bounding rectangle): frontage and depth are approximate' % round(area / rect * 100))
    if listed_land and listed_land > 0 and abs(area - listed_land) / listed_land > 0.15:
        r['checks'].append('Title lot %d m2 vs listing %d m2: may be part of a bigger holding, or the wrong lot' % (area, listed_land))
    for key, rule in (rules or {}).items():
        try:
            mf, md, ml = float(rule.get('minFrontage') or 0), float(rule.get('minDepth') or 0), float(rule.get('minLand') or 0)
        except (TypeError, ValueError):
            continue
        if short >= mf and (not md or long_ >= md) and area >= ml:
            r['fits'].append(rule.get('label') or key)
    if rules and not r['fits']:
        r['fails'].append('Lot too small for every build model (%.1f m x %.1f m, %d m2)' % (short, long_, area))

    lons = [p[0] for p in poly_ll[0]]
    lats = [p[1] for p in poly_ll[0]]
    bbox = (min(lons), min(lats), max(lons), max(lats))
    inner = _sc_shrink(rings[0])
    cx = sum(p[0] for p in inner) / len(inner)
    cy = sum(p[1] for p in inner) / len(inner)
    probes = [(cx, cy)] + inner

    def covering(kind):
        out = []
        for f in _sc_features(L[kind], *bbox):
            for poly in _sc_polys(f.get('geometry')):
                mp = [[xy(p) for p in ring] for ring in poly]
                if any(_sc_in_poly(pt, mp) for pt in probes):
                    out.append(f.get('properties') or {})
                    break
        return out
    zones = covering('zone')
    zcodes = sorted(set(_sc_code(z) for z in zones if _sc_code(z)))
    if zones and not zcodes:
        r['notes'].append('Zone fields: ' + ', '.join(sorted(zones[0].keys()))[:200])
    r['zone'] = ', '.join(zcodes)
    if not zcodes:
        r['checks'].append('No planning zone found')
    for b in set(_sc_base(z) for z in zcodes):
        if b in SC_CHECK_ZONES:
            r['checks'].append(SC_CHECK_ZONES[b])
        elif b not in SC_OK_ZONES:
            r['fails'].append('Zone %s does not allow a house' % b)
    ocodes = sorted(set(_sc_code(o) for o in covering('overlay') if _sc_code(o)))
    r['overlays'] = ', '.join(ocodes) or 'none'
    for c in ocodes:
        b = _sc_base(c)
        if b in SC_FAIL_OVERLAYS:
            r['fails'].append('%s (%s)' % (SC_FAIL_OVERLAYS[b], c))
        elif b in SC_CHECK_OVERLAYS:
            r['checks'].append('%s (%s)' % (SC_CHECK_OVERLAYS[b], c))
    r['result'] = 'Fail' if r['fails'] else ('Check' if r['checks'] else 'Pass')
    return r


# ---------------------------------------------------------------------------
# Itemised feasibility workbooks (Excel). The screener works out every line for
# every project (Radius cost library + each project's switches) and posts it
# here; itemised_feaso.py writes the workbook with live formulas.
#   /api/itemised-xlsx  - any signed-in user (client / funder safe)
#   /api/earnings-xlsx  - admins only (group earnings: Radius, Haven, Away, RRE)
# ---------------------------------------------------------------------------
import itemised_feaso as _IF

_XL_A_KEYS = ('cIr', 'cLine', 'cEst', 'cLvr', 'cMonths', 'lvr', 'ir', 'cap', 'rrc', 'sdaMgr',
              'cleanPa', 'fire', 'ins', 'rates', 'maint')


def _is_admin_user(u):
    return bool(u) and u.get('role') == 'admin'


def _xl_safe(v, depth=0):
    """Client text never becomes a formula; numbers stay numbers."""
    if depth > 6:
        return None
    if isinstance(v, str):
        v = v[:300]
        return (' ' + v) if v[:1] in ('=', '+', '-', '@') else v
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, (int, float)):
        return v if math.isfinite(v) else 0
    if isinstance(v, list):
        return [_xl_safe(x, depth + 1) for x in v[:200]]
    if isinstance(v, dict):
        return {str(k)[:40]: _xl_safe(x, depth + 1) for k, x in list(v.items())[:200]}
    return None


def _xl_assumptions(a):
    out = {}
    for k in _XL_A_KEYS:
        try:
            out[k] = float((a or {}).get(k))
        except (TypeError, ValueError):
            return None
        if not math.isfinite(out[k]):
            return None
    return out


def _xl_send(wb, name):
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    safe = ''.join(ch for ch in name if ch.isalnum() or ch in ' _-').strip()[:80] or 'Feasibility'
    return send_file(buf, as_attachment=True, download_name=safe.replace(' ', '_') + '.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.route('/api/itemised-xlsx', methods=['POST'])
@login_required
def api_itemised_xlsx():
    data = request.get_json(silent=True) or {}
    projects = data.get('projects')
    A = _xl_assumptions(data.get('A'))
    if not isinstance(projects, list) or not projects or len(projects) > 60 or A is None:
        return jsonify({'error': 'Nothing to export'}), 400
    projects = _xl_safe(projects)
    lib = _xl_safe(data.get('lib')) if isinstance(data.get('lib'), list) else None
    for p in projects:
        if not isinstance(p, dict) or p.get('model') not in _IF.MODELS:
            return jsonify({'error': 'Bad project'}), 400
        if lib:
            p['lib'] = lib
    title = _xl_safe(str(data.get('title') or 'Portfolio'))[:120]
    try:
        wb = _IF.build_feaso_workbook(title + ' – itemised feasibility', projects, A)[0]
    except Exception as e:  # never leave the user with a half-written file
        app.logger.exception('itemised export failed')
        return jsonify({'error': 'Could not build the workbook: %s' % e}), 500
    log_event('itemised_export', {'title': title, 'projects': len(projects), 'kind': data.get('kind')})
    return _xl_send(wb, (data.get('filename') or title) + ' Itemised Feaso')


@app.route('/api/earnings-xlsx', methods=['POST'])
@login_required
def api_earnings_xlsx():
    if not _is_admin_user(request.current_user):
        return jsonify({'error': 'Admins only'}), 403
    data = request.get_json(silent=True) or {}
    rows = data.get('rows')
    A = _xl_assumptions(data.get('A'))
    if not isinstance(rows, list) or not rows or len(rows) > 60 or A is None:
        return jsonify({'error': 'Nothing to export'}), 400
    rows = _xl_safe(rows)
    keys = ('price', 'ba', 'pm', 'cam', 'letting', 'mkt', 'houses', 'villas', 'titles', 'dw', 'gross', 'value')
    for r in rows:
        if not isinstance(r, dict):
            return jsonify({'error': 'Bad row'}), 400
        for k in keys:
            try:
                r[k] = float(r.get(k) or 0)
            except (TypeError, ValueError):
                return jsonify({'error': 'Bad row'}), 400
        r['name'] = str(r.get('name') or '')[:80]
    # The Radius build margin per house comes from the database, never the browser.
    db = get_db()
    for r in rows:
        mg = None
        try:
            iid = int(r.get('iid') or 0)
            row = db.execute('SELECT margin FROM portfolio_items WHERE id=?', (iid,)).fetchone() if iid else None
            mg = row['margin'] if row is not None else None
        except (TypeError, ValueError, sqlite3.Error):
            mg = None
        r['margin'] = float(mg) if mg is not None else RADIUS_STD_MARGIN
    db.close()
    title = _xl_safe(str(data.get('title') or 'Portfolio'))[:120]
    wb = _IF.build_earnings_workbook(title, rows, A)
    log_event('earnings_export', {'title': title, 'projects': len(rows)})
    return _xl_send(wb, 'ADMIN ' + title + ' Group Earnings')


@app.route('/api/site-check', methods=['POST'])
@login_required
def api_site_check():
    data = request.get_json(silent=True) or {}
    address = str(data.get('address') or '').strip()
    state = str(data.get('state') or '').strip().lower()
    if not address:
        return jsonify({'error': 'Missing address'}), 400
    if state != 'vic':
        return jsonify({'error': 'The automatic site check covers Victoria only for now'}), 400
    key = _address_key(address)
    db = get_db()
    if not data.get('refresh'):
        row = db.execute('SELECT result_json, checked_at, checked_by FROM site_checks WHERE address_key=?', (key,)).fetchone()
        if row:
            db.close()
            res = json.loads(row['result_json'])
            res['cached'] = True
            res['checked_at'] = row['checked_at']
            res['checked_by'] = row['checked_by']
            return jsonify(res)
    lat, lng = data.get('lat'), data.get('lng')
    try:
        lat, lng = float(lat), float(lng)
    except (TypeError, ValueError):
        lat = lng = None
    if lat is None:
        if not GOOGLE_MAPS_API_KEY:
            db.close()
            return jsonify({'error': 'GOOGLE_MAPS_API_KEY not configured on server'}), 500
        g = _http_get_json('https://maps.googleapis.com/maps/api/geocode/json?address=' +
                           quote_plus(address + ', Australia') + '&key=' + GOOGLE_MAPS_API_KEY)
        if g.get('status') != 'OK' or not g.get('results'):
            db.close()
            return jsonify({'error': 'Could not find the address (' + str(g.get('status') or g.get('error')) + ')'}), 502
        loc = g['results'][0]['geometry']
        lat, lng = loc['location']['lat'], loc['location']['lng']
        approx = loc.get('location_type') != 'ROOFTOP'
    else:
        approx = False
    try:
        land = float(data.get('land') or 0)
    except (TypeError, ValueError):
        land = 0
    try:
        res = _site_check(address, lat, lng, land, data.get('rules') or {})
    except Exception as e:
        db.close()
        return jsonify({'error': 'Site check failed: %s' % e, 'lat': lat, 'lng': lng}), 502
    if approx:
        res['checks'].insert(0, 'Address found only approximately: the lot may be wrong')
        if res['result'] == 'Pass':
            res['result'] = 'Check'
    now = datetime.datetime.utcnow().isoformat(timespec='seconds') + 'Z'
    u = getattr(request, 'current_user', None)
    who = (u['full_name'] if u else '') or ''
    db.execute('INSERT OR REPLACE INTO site_checks (address_key, state, address, result_json, checked_at, checked_by) VALUES (?,?,?,?,?,?)',
               (key, state, address, json.dumps(res), now, who))
    db.commit()
    db.close()
    res['cached'] = False
    res['checked_at'] = now
    log_event('site_check', {'address': address, 'result': res['result']})
    return jsonify(res)


def _places_search(lat, lng, place_type, radius=5000):
    """Search Google Places near (lat, lng) for `place_type`.

    Encapsulates the hospital text-search + name-filter logic, the
    supermarket major-chain filter, and the shopping_mall name filter so the
    same rules apply to both /api/places-nearby (client-driven) and manual
    property creation (server-driven, in /api/manual-properties).

    Returns a list of dicts [{'name': str, 'km': float}, ...] sorted by
    distance ascending, or an empty list. Raises ValueError with a message
    on upstream errors so callers can decide how to surface them.
    """
    radius = max(50, min(int(radius), 50000))

    # ----- HOSPITAL: use Text Search instead of Nearby Search -----
    # Google's Nearby Search tags too many things as primaryType=hospital
    # (medical centres, kidney clinics, individual doctors). With distance
    # ranking, those false positives get ranked above real hospitals further
    # out. Text Search "hospital near {lat,lng}" understands the human
    # meaning of 'hospital' and ranks real hospitals (Mercy, Northern,
    # Royal Melbourne, etc.) at the top.
    if place_type == 'hospital':
        text_body = {
            'textQuery': 'hospital',
            'maxResultCount': 20,
            'locationBias': {
                'circle': {
                    'center': {'latitude': lat, 'longitude': lng},
                    'radius': radius
                }
            }
        }
        text_headers = {
            'X-Goog-Api-Key': GOOGLE_MAPS_API_KEY,
            'X-Goog-FieldMask': 'places.displayName,places.location,places.primaryType,places.types'
        }
        data = _http_post_json('https://places.googleapis.com/v1/places:searchText',
                               text_body, headers=text_headers)
    else:
        body = {
            'includedTypes': [place_type],
            'maxResultCount': 20,
            'rankPreference': 'DISTANCE',
            'locationRestriction': {
                'circle': {
                    'center': {'latitude': lat, 'longitude': lng},
                    'radius': radius
                }
            }
        }
        headers = {
            'X-Goog-Api-Key': GOOGLE_MAPS_API_KEY,
            'X-Goog-FieldMask': 'places.displayName,places.location,places.primaryType,places.types'
        }
        data = _http_post_json('https://places.googleapis.com/v1/places:searchNearby',
                               body, headers=headers)
    if 'error' in data:
        raise ValueError(data['error'])
    places = data.get('places') or []
    if not places:
        return []

    # For 'hospital' searches via Text Search: Google's results are already
    # high-quality (real hospitals at the top). We still apply name-based
    # filters to catch the rare bad result, then re-sort by distance.
    if place_type == 'hospital':
        # Things to exclude even when name contains 'hospital' (animal/private/etc.)
        NAME_EXCLUDE_KEYWORDS = [
            'animal hospital', 'pet hospital', 'veterinary',
            'institute', 'foundation', 'association', 'society',
            'training', 'engineering', 'consulting', 'consultancy',
            'cosmetic', 'plastic surgery'
        ]
        # Acceptable hospital naming patterns
        REQUIRED_NAME_KEYWORDS = [
            'hospital', 'health service', 'health network',
            'northern health', 'austin health', 'eastern health',
            'monash health', 'western health', 'alfred health',
            'mercy health', 'st vincent', 'royal melbourne', 'royal childrens',
            'royal children', 'box hill', 'epworth', 'cabrini', 'peter maccallum'
        ]
        EXCLUDE_TYPES = {
            'doctor', 'medical_lab', 'dental_clinic', 'dentist',
            'physiotherapist', 'chiropractor', 'pharmacy', 'drugstore',
            'veterinary_care', 'spa', 'beauty_salon', 'wellness_center'
        }
        def name_required(nm):
            n = (nm or '').lower()
            return any(kw in n for kw in REQUIRED_NAME_KEYWORDS)
        def name_excluded(nm):
            n = (nm or '').lower()
            return any(kw in n for kw in NAME_EXCLUDE_KEYWORDS)

        filtered = []
        for p in places:
            types = set(p.get('types') or [])
            nm = ((p.get('displayName') or {}).get('text')) or ''
            if (name_required(nm)
                    and not name_excluded(nm)
                    and not (types & EXCLUDE_TYPES)):
                filtered.append(p)
        places = filtered

    # For 'supermarket': prefer well-known major retailers by name.
    if place_type == 'supermarket':
        SUPERMARKET_KEYWORDS = [
            'coles', 'woolworths', 'woolies', 'aldi', 'iga', 'foodworks',
            'costco', 'drakes', 'spudshed', 'harris farm', 'ritchies'
        ]
        def is_known_chain(nm):
            n = (nm or '').lower()
            return any(kw in n for kw in SUPERMARKET_KEYWORDS)
        places = [p for p in places
                  if is_known_chain(((p.get('displayName') or {}).get('text')) or '')]

    # For 'shopping_mall': require the name to contain a shopping-centre keyword.
    if place_type == 'shopping_mall':
        MALL_KEYWORDS = [
            'shopping centre', 'shopping center', 'shopping mall',
            'shopping village', 'shopping plaza', 'plaza', 'westfield',
            'marketplace', 'arcade', 'town centre', 'town center',
            'square', 'mall', 'qv ', 'emporium', 'galleria', 'outlet'
        ]
        def is_mall(nm):
            n = (nm or '').lower()
            return any(kw in n for kw in MALL_KEYWORDS)
        places = [p for p in places
                  if is_mall(((p.get('displayName') or {}).get('text')) or '')]

    out = []
    for p in places:
        loc = p.get('location') or {}
        if 'latitude' not in loc or 'longitude' not in loc:
            continue
        nm = ((p.get('displayName') or {}).get('text')) or '—'
        km = _haversine_km(lat, lng, loc['latitude'], loc['longitude'])
        out.append({'name': nm, 'km': round(km, 2)})
    out.sort(key=lambda x: x['km'])
    return out


def _compute_amenities(lat, lng):
    """Run the six Google Places lookups used for a manual property and
    return a flat dict matching the column names the dashboard expects:
    hosp1_name/km, hosp2_name/km, hosp3_name/km, medical_name/km,
    shop_name/km, train_name/km, bus_km, tram_name/km. Any field that
    can't be filled comes back as ''. Errors from the upstream API are
    logged but never raise — a property still saves even if a lookup
    fails."""
    out = {
        'hosp1_name': '', 'hosp1_km': '',
        'hosp2_name': '', 'hosp2_km': '',
        'hosp3_name': '', 'hosp3_km': '',
        'medical_name': '', 'medical_km': '',
        'shop_name': '', 'shop_km': '',
        'train_name': '', 'train_km': '',
        'bus_km': '',
        'tram_name': '', 'tram_km': '',
    }
    if not GOOGLE_MAPS_API_KEY:
        return out

    def safe(place_type, radius=5000):
        try:
            return _places_search(lat, lng, place_type, radius)
        except ValueError as e:
            print('[_compute_amenities]', place_type, 'failed:', e, flush=True)
            return []

    # Hospitals: top 3
    hosps = safe('hospital', radius=15000)  # wider radius — hospitals are rarer
    for i, h in enumerate(hosps[:3], start=1):
        out['hosp' + str(i) + '_name'] = h['name']
        out['hosp' + str(i) + '_km'] = h['km']

    # Doctor (any GP / medical centre)
    docs = safe('doctor')
    if docs:
        out['medical_name'] = docs[0]['name']
        out['medical_km'] = docs[0]['km']

    # Supermarket — fall back to shopping_mall when no major chain nearby
    sups = safe('supermarket')
    if sups:
        out['shop_name'] = sups[0]['name']
        out['shop_km'] = sups[0]['km']
    else:
        malls = safe('shopping_mall')
        if malls:
            out['shop_name'] = malls[0]['name']
            out['shop_km'] = malls[0]['km']

    # Train
    trains = safe('train_station')
    if trains:
        out['train_name'] = trains[0]['name']
        out['train_km'] = trains[0]['km']

    # Bus — store distance only (matches CSV schema, which has bus_km but no bus_name)
    buses = safe('bus_station', radius=2000)
    if buses:
        out['bus_km'] = buses[0]['km']

    # Tram
    trams = safe('light_rail_station', radius=3000)
    if trams:
        out['tram_name'] = trams[0]['name']
        out['tram_km'] = trams[0]['km']

    return out


@app.route('/api/places-nearby')
@login_required
def api_places_nearby():
    """Find the nearest place of a given type. Args: lat, lng, type, radius (m).
    Returns {name, km} of the closest match, or {error} / {name: null} if none found."""
    if not GOOGLE_MAPS_API_KEY:
        return jsonify({'error': 'GOOGLE_MAPS_API_KEY not configured on server'}), 500
    try:
        lat = float(request.args.get('lat', ''))
        lng = float(request.args.get('lng', ''))
    except ValueError:
        return jsonify({'error': 'Invalid lat/lng'}), 400
    place_type = (request.args.get('type') or '').strip()
    if not place_type:
        return jsonify({'error': 'Missing type'}), 400
    try:
        radius = int(request.args.get('radius', 5000))
    except ValueError:
        radius = 5000

    try:
        results = _places_search(lat, lng, place_type, radius=radius)
    except ValueError as e:
        return jsonify({'error': str(e)}), 502

    if not results:
        return jsonify({'name': None, 'km': None})
    return jsonify({'name': results[0]['name'], 'km': results[0]['km']})



@app.route('/api/static-map')
@login_required
def api_static_map():
    """Proxy a Google Static Maps request. Args: lat, lng (or address as fallback).
    Returns the PNG image bytes directly."""
    if not GOOGLE_MAPS_API_KEY:
        return jsonify({'error': 'GOOGLE_MAPS_API_KEY not configured on server'}), 500
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    addr = request.args.get('address')
    if lat and lng:
        try:
            float(lat); float(lng)
        except ValueError:
            return jsonify({'error': 'Invalid lat/lng'}), 400
        center = lat + ',' + lng
    elif addr:
        center = quote_plus(addr.strip() + ', Australia')
    else:
        return jsonify({'error': 'Missing lat/lng or address'}), 400
    try:
        zoom = int(request.args.get('zoom', 14))
    except ValueError:
        zoom = 14
    zoom = max(1, min(zoom, 20))
    size = request.args.get('size', '600x300')
    if not all(p.isdigit() for p in size.split('x')) or 'x' not in size:
        size = '600x300'
    url = ('https://maps.googleapis.com/maps/api/staticmap'
           '?center=' + center +
           '&zoom=' + str(zoom) +
           '&size=' + size +
           '&scale=2&maptype=roadmap'
           '&markers=color:red%7Csize:mid%7C' + center +
           '&key=' + GOOGLE_MAPS_API_KEY)
    try:
        req = Request(url, headers={'User-Agent': 'SDA-Screener/1.0'})
        with urlopen(req, timeout=15) as r:
            img_bytes = r.read()
            content_type = r.headers.get('Content-Type', 'image/png')
        resp = make_response(img_bytes)
        resp.headers['Content-Type'] = content_type
        resp.headers['Cache-Control'] = 'private, max-age=3600'
        return resp
    except (HTTPError, URLError) as e:
        return jsonify({'error': str(e)}), 502

@app.route('/api/suburb-info')
@login_required
def api_suburb_info():
    """Look up suburb info from Wikipedia.
    Query params: suburb, state (e.g. 'Thornbury', 'VIC')
    Returns: {summary: str, population: int|null, title: str} or {error}
    No API key needed for Wikipedia REST API."""
    suburb = (request.args.get('suburb') or '').strip()
    state_code = (request.args.get('state') or '').strip().upper()
    if not suburb:
        return jsonify({'error': 'Missing suburb parameter'}), 400
    state_full = {'VIC': 'Victoria', 'NSW': 'New South Wales', 'QLD': 'Queensland',
                  'SA': 'South Australia', 'WA': 'Western Australia',
                  'TAS': 'Tasmania', 'NT': 'Northern Territory', 'ACT': 'Australian Capital Territory'}
    # Try increasingly specific queries, returning first match
    titles_to_try = []
    if state_code in state_full:
        titles_to_try.append(suburb + ', ' + state_full[state_code])
    titles_to_try.append(suburb)
    summary, title_used = None, None
    for title in titles_to_try:
        url = ('https://en.wikipedia.org/api/rest_v1/page/summary/'
               + quote_plus(title.replace(' ', '_')))
        try:
            req = Request(url, headers={'User-Agent': 'SDA-Screener/1.0 (radius project mgmt)'})
            with urlopen(req, timeout=8) as r:
                data = json.loads(r.read().decode('utf-8'))
            # Skip disambiguation pages and missing pages
            if data.get('type') == 'disambiguation' or data.get('type') == 'no-extract':
                continue
            extract = (data.get('extract') or '').strip()
            if extract:
                summary = extract
                title_used = data.get('title') or title
                break
        except (HTTPError, URLError, ValueError):
            continue
    if not summary:
        return jsonify({'error': 'Suburb info not found', 'suburb': suburb})
    # Try to extract a population figure from the summary text
    population = None
    import re as _re
    # Match "population of 21,567" or "21,567 people" or "(2021 population: 21,567)"
    patterns = [
        r'population[^\d]{0,30}(\d{1,3}(?:,\d{3})+|\d{4,7})',
        r'(\d{1,3}(?:,\d{3})+|\d{4,7})\s*(?:people|residents|inhabitants)',
    ]
    for pat in patterns:
        m = _re.search(pat, summary, _re.IGNORECASE)
        if m:
            try:
                population = int(m.group(1).replace(',', ''))
                break
            except ValueError:
                pass
    # Trim summary to ~3 sentences for compact display
    sentences = _re.split(r'(?<=[.!?])\s+', summary)
    short_summary = ' '.join(sentences[:3]).strip()
    if len(short_summary) > 450:
        short_summary = short_summary[:447].rstrip() + '...'
    return jsonify({
        'title': title_used,
        'summary': short_summary,
        'population': population
    })

LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>SDA Property Screener - Login</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#001540 0%,#002060 50%,#003090 100%);min-height:100vh;display:flex;align-items:center;justify-content:center}
.card{background:#fff;border-radius:16px;padding:48px 40px;width:100%;max-width:400px;box-shadow:0 24px 80px rgba(0,0,0,0.4)}
.logo{text-align:center;margin-bottom:32px}
.logo-icon{font-size:40px;margin-bottom:12px}
.logo h1{font-size:22px;font-weight:800;color:#002060;margin-bottom:4px}
.logo p{font-size:13px;color:#6B7280}
label{display:block;font-size:12px;font-weight:700;color:#374151;margin-bottom:6px;text-transform:uppercase}
input{width:100%;padding:12px 14px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;margin-bottom:16px}
input:focus{outline:none;border-color:#185FA5}
button{width:100%;padding:14px;background:#002060;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:700;cursor:pointer}
button:hover{background:#003090}
.error{background:#fff3f3;border:1px solid #fca5a5;color:#A32D2D;padding:12px 14px;border-radius:8px;font-size:13px;margin-bottom:16px}
.footer{text-align:center;margin-top:24px;font-size:12px;color:#9CA3AF}
</style></head>
<body><div class="card">
<div class="logo"><div class="logo-icon">&#127968;</div><h1>SDA Property Screener</h1><p>NDIS Investment Analysis Platform</p></div>
{% if error %}<div class="error">{{ error }}</div>{% endif %}
<form method="POST"><label>USERNAME</label><input name="username" placeholder="Enter your username" autofocus>
<label>PASSWORD</label><input type="password" name="password" placeholder="Enter your password">
<button type="submit">Sign In</button></form>
<div class="footer">Confidential - Authorised users only</div>
</div></body></html>"""

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
    return make_response(Template(LOGIN_HTML).render(error=error))

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
    html = get_dashboard_html()
    # Inject the Maps JS API key for the SDA Map tab (browser-side rendering).
    # The same GOOGLE_MAPS_API_KEY env var is reused — for browser use, ensure
    # Application restrictions in Google Cloud Console include HTTP referrer
    # for your Railway domain, AND that Maps JavaScript API is enabled.
    html = html.replace('{{GOOGLE_MAPS_API_KEY}}', GOOGLE_MAPS_API_KEY or '')
    return make_response(html)

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
    if state not in ('vic','nsw','qld'): abort(400)
    db = get_db()
    row = db.execute('SELECT csv_data,row_count,uploaded_at FROM property_data WHERE state=?', (state,)).fetchone()
    db.close()
    if not row: return jsonify({'data': None, 'rows': 0, 'uploaded_at': None})
    csv_data = row['csv_data']
    row_count = row['row_count']
    # Strip soft-deleted (hidden) rows before sending to the dashboard.
    # Admins reviewing the hidden list use /api/hidden-properties instead.
    hidden_keys = _get_hidden_address_keys(state)
    if hidden_keys:
        csv_data, removed = _strip_hidden_from_csv(csv_data, hidden_keys)
        row_count = max(0, row_count - removed)
    return jsonify({'data': csv_data, 'rows': row_count, 'uploaded_at': row['uploaded_at']})

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
    if not row: return jsonify({'ids': [], 'dd': {}})
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
                  dd_data=excluded.dd_data,updated_at=datetime('now')""", (uid, ids, dd))
    db.commit()
    db.close()
    return jsonify({'ok': True})


# ===========================================================================
# Soft-delete (hide) API endpoints
# ===========================================================================

@app.route('/api/me')
@login_required
def api_me():
    """Return identity for the logged-in user.

    The dashboard uses this to decide whether to show admin-only controls
    (Restore / Hard-delete) and to label its own hide-undo eligibility."""
    u = request.current_user
    return jsonify({
        'username': u['username'],
        'full_name': u['full_name'],
        'role': u['role'],
        'is_admin': u['role'] == 'admin',
        'hide_undo_seconds': HIDE_UNDO_SECONDS,
    })


@app.route('/api/hide-property', methods=['POST'])
@login_required
def api_hide_property():
    """Soft-delete a property from the screener.

    Any logged-in user can call this. Reason is required (min 3 chars).
    Returns the new hidden_properties row id so the client can offer Undo."""
    data = request.get_json(silent=True) or {}
    state = (data.get('state') or '').strip().lower()
    address = (data.get('address') or '').strip()
    reason = (data.get('reason') or '').strip()
    if state not in ('vic', 'nsw', 'qld'):
        return jsonify({'error': 'Invalid state'}), 400
    if not address:
        return jsonify({'error': 'Missing address'}), 400
    if len(reason) < 3:
        return jsonify({'error': 'Reason is required (min 3 characters)'}), 400
    addr_key = _address_key(address)
    if not addr_key:
        return jsonify({'error': 'Address could not be normalised'}), 400
    u = request.current_user
    db = get_db()
    try:
        cur = db.execute(
            """INSERT INTO hidden_properties
               (state, address, address_key, hidden_by_id, hidden_by_name, reason)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (state, address, addr_key, u['user_id'], u['full_name'], reason)
        )
        db.commit()
        new_id = cur.lastrowid
    except sqlite3.IntegrityError:
        # Already hidden by someone else — that's fine, the property is gone
        # either way. Return the existing row id so Undo still works for the
        # admin (and the original hider) but not for this user.
        existing = db.execute(
            'SELECT id FROM hidden_properties WHERE state=? AND address_key=?',
            (state, addr_key)
        ).fetchone()
        db.close()
        return jsonify({
            'ok': True,
            'id': existing['id'] if existing else None,
            'already_hidden': True,
        })
    db.close()
    log_event('property_hidden', {'state': state, 'address': address, 'reason': reason})
    return jsonify({'ok': True, 'id': new_id, 'already_hidden': False})


@app.route('/api/unhide-property', methods=['POST'])
@login_required
def api_unhide_property():
    """Restore a hidden property (delete the hidden_properties row).

    Admins can unhide any row. Non-admins can unhide only their own hide
    within HIDE_UNDO_SECONDS — this powers the 'Undo' toast immediately
    after a mistaken click."""
    data = request.get_json(silent=True) or {}
    try:
        hid = int(data.get('id'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Missing or invalid id'}), 400
    u = request.current_user
    db = get_db()
    row = db.execute(
        'SELECT id, state, address, hidden_by_id, hidden_at FROM hidden_properties WHERE id=?',
        (hid,)
    ).fetchone()
    if not row:
        db.close()
        return jsonify({'error': 'Hide record not found'}), 404
    is_admin = u['role'] == 'admin'
    is_owner = (row['hidden_by_id'] == u['user_id'])
    within_window = False
    if is_owner:
        try:
            # SQLite stores as 'YYYY-MM-DD HH:MM:SS' UTC
            hidden_at = datetime.datetime.strptime(row['hidden_at'], '%Y-%m-%d %H:%M:%S')
            age = (datetime.datetime.utcnow() - hidden_at).total_seconds()
            within_window = age <= HIDE_UNDO_SECONDS
        except (ValueError, TypeError):
            within_window = False
    if not (is_admin or (is_owner and within_window)):
        db.close()
        if is_owner:
            return jsonify({'error': 'Undo window has expired. Ask an admin to restore.'}), 403
        return jsonify({'error': 'Only an admin can restore this property'}), 403
    db.execute('DELETE FROM hidden_properties WHERE id=?', (hid,))
    db.commit()
    db.close()
    log_event('property_unhidden', {
        'state': row['state'], 'address': row['address'],
        'by_admin': is_admin and not is_owner,
    })
    return jsonify({'ok': True})


@app.route('/api/hidden-properties')
@admin_required
def api_list_hidden():
    """List all currently hidden properties. Admin only."""
    db = get_db()
    rows = db.execute(
        """SELECT id, state, address, hidden_by_id, hidden_by_name,
                  hidden_at, reason
           FROM hidden_properties ORDER BY hidden_at DESC"""
    ).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/hard-delete-property', methods=['POST'])
@admin_required
def api_hard_delete_property():
    """Permanently remove a property from the CSV blob for its state.

    Also removes any matching hidden_properties row so the address can later
    be re-added (e.g. via manual entry in Stage C2) without conflict.
    Admin only."""
    data = request.get_json(silent=True) or {}
    state = (data.get('state') or '').strip().lower()
    address = (data.get('address') or '').strip()
    if state not in ('vic', 'nsw', 'qld'):
        return jsonify({'error': 'Invalid state'}), 400
    if not address:
        return jsonify({'error': 'Missing address'}), 400
    addr_key = _address_key(address)
    db = get_db()
    row = db.execute(
        'SELECT csv_data, row_count FROM property_data WHERE state=?', (state,)
    ).fetchone()
    if not row:
        db.close()
        return jsonify({'error': 'No property data for that state'}), 404
    new_csv, removed = _strip_hidden_from_csv(row['csv_data'], {addr_key})
    if removed == 0:
        # The address wasn't in the CSV. Still purge any hidden_properties row
        # for it (so the admin can clean up orphan hides).
        db.execute(
            'DELETE FROM hidden_properties WHERE state=? AND address_key=?',
            (state, addr_key)
        )
        db.commit()
        db.close()
        return jsonify({
            'ok': True,
            'removed_from_csv': 0,
            'note': 'Address was not present in the current CSV; any hide record cleared.',
        })
    new_row_count = max(0, (row['row_count'] or 0) - removed)
    db.execute(
        'UPDATE property_data SET csv_data=?, row_count=? WHERE state=?',
        (new_csv, new_row_count, state)
    )
    db.execute(
        'DELETE FROM hidden_properties WHERE state=? AND address_key=?',
        (state, addr_key)
    )
    db.commit()
    db.close()
    log_event('property_hard_deleted', {'state': state, 'address': address, 'rows_removed': removed})
    return jsonify({'ok': True, 'removed_from_csv': removed})


# ===========================================================================
# C2: Manual property addition
# ---------------------------------------------------------------------------
# Anyone signed-in can add a property; the row is geocoded server-side and
# the same Google Places amenity lookups run that the CSV pipeline does, so
# manual entries are indistinguishable from CSV ones in the screener.
# The hide/restore endpoints from C1 already key on (state, address_key)
# and therefore work on manual properties with no further code. Hard delete
# of a manual property (admin only) ALSO purges any matching hidden_properties
# row so the address can be re-added cleanly later.
# ===========================================================================

VALID_DESIGN_TYPES = {'2p', '3p', 'dp', 'd3', 'hv'}
VALID_SALE_TYPES = {'Private Sale', 'Auction', 'Off-market', 'Expression of Interest'}


def _manual_row_to_dict(r):
    """Serialise a manual_properties SQLite row for the JSON API."""
    return {
        'id': r['id'],
        'state': r['state'],
        'address': r['address'],
        'suburb': r['suburb'],
        'postcode': r['postcode'] or '',
        'price': r['price'],
        'land': r['land'],
        'design_type': r['design_type'],
        'sale_type': r['sale_type'],
        'auction_date': r['auction_date'] or '',
        'sa4': r['sa4'] or '',
        'sa3': r['sa3'] or '',
        'lat': r['lat'],
        'lng': r['lng'],
        'hosp1_name': r['hosp1_name'] or '', 'hosp1_km': r['hosp1_km'] if r['hosp1_km'] is not None else '',
        'hosp2_name': r['hosp2_name'] or '', 'hosp2_km': r['hosp2_km'] if r['hosp2_km'] is not None else '',
        'hosp3_name': r['hosp3_name'] or '', 'hosp3_km': r['hosp3_km'] if r['hosp3_km'] is not None else '',
        'medical_name': r['medical_name'] or '', 'medical_km': r['medical_km'] if r['medical_km'] is not None else '',
        'shop_name': r['shop_name'] or '', 'shop_km': r['shop_km'] if r['shop_km'] is not None else '',
        'train_name': r['train_name'] or '', 'train_km': r['train_km'] if r['train_km'] is not None else '',
        'bus_km': r['bus_km'] if r['bus_km'] is not None else '',
        'tram_name': r['tram_name'] or '', 'tram_km': r['tram_km'] if r['tram_km'] is not None else '',
        'created_by_id': r['created_by_id'],
        'created_by_name': r['created_by_name'],
        'created_at': r['created_at'],
        'last_edited_by_id': r['last_edited_by_id'],
        'last_edited_by_name': r['last_edited_by_name'] or '',
        'last_edited_at': r['last_edited_at'] or '',
    }


def _validate_manual_payload(data, partial=False):
    """Validate the JSON payload for create / update.

    Returns (cleaned_dict, error_or_none). `partial=True` skips required-field
    checks (used on PUT where the address is fixed and only changed fields
    matter; required fields still get range-checked if present)."""
    out = {}

    state = (data.get('state') or '').strip().lower()
    if state or not partial:
        if state not in ('vic', 'nsw', 'qld'):
            return None, 'state must be vic, nsw or qld'
        out['state'] = state

    address = (data.get('address') or '').strip()
    if address or not partial:
        if len(address) < 5:
            return None, 'address is required (min 5 characters)'
        out['address'] = address

    suburb = (data.get('suburb') or '').strip()
    if suburb or not partial:
        if not suburb:
            return None, 'suburb is required'
        out['suburb'] = suburb

    # Postcode is optional; if given, must be 4 digits
    if 'postcode' in data:
        pc = (data.get('postcode') or '').strip()
        if pc and not (pc.isdigit() and len(pc) == 4):
            return None, 'postcode must be 4 digits'
        out['postcode'] = pc

    if 'price' in data or not partial:
        try:
            price = float(data.get('price'))
        except (TypeError, ValueError):
            return None, 'price must be a number'
        if price < 100000:
            return None, 'price must be at least $100,000'
        out['price'] = price

    if 'land' in data or not partial:
        try:
            land = float(data.get('land'))
        except (TypeError, ValueError):
            return None, 'land size must be a number'
        # Match the screener's existing applyF filter (>1000m² is excluded)
        if land <= 0 or land > 1000:
            return None, 'land size must be between 1 and 1000 m²'
        out['land'] = land

    if 'design_type' in data or not partial:
        dt = (data.get('design_type') or '').strip().lower()
        if dt not in VALID_DESIGN_TYPES:
            return None, 'design_type must be one of: 2p, 3p, dp, d3, hv'
        out['design_type'] = dt

    if 'sale_type' in data or not partial:
        st = (data.get('sale_type') or '').strip()
        if st not in VALID_SALE_TYPES:
            return None, 'sale_type must be one of: ' + ', '.join(sorted(VALID_SALE_TYPES))
        out['sale_type'] = st

    # auction_date — required iff effective sale_type is Auction.
    # We only run this check when the request actually touches sale_type or
    # auction_date. A partial PUT that just changes (say) price must not
    # demand the user re-supply auction_date on every edit.
    touches_auction = ('sale_type' in out) or ('auction_date' in data)
    if touches_auction:
        effective_sale = out.get('sale_type') or data.get('_existing_sale_type')
        if effective_sale == 'Auction':
            ad = (data.get('auction_date') or '').strip()
            if not ad:
                # If we're not changing sale_type (i.e. it's already Auction
                # in the DB) and the client sent an empty auction_date,
                # treat that as 'keep existing' rather than 'clear it'.
                if 'sale_type' not in out and 'auction_date' not in data:
                    pass
                else:
                    return None, 'auction_date is required when sale_type=Auction'
            else:
                try:
                    datetime.datetime.strptime(ad, '%Y-%m-%d')
                except ValueError:
                    return None, 'auction_date must be in YYYY-MM-DD format'
                out['auction_date'] = ad
        else:
            # Switching away from Auction (or non-Auction create): clear the date.
            out['auction_date'] = None

    # SA4/SA3 — accept whatever the client looked up (or the user override)
    if 'sa4' in data:
        out['sa4'] = (data.get('sa4') or '').strip()
    if 'sa3' in data:
        out['sa3'] = (data.get('sa3') or '').strip()

    return out, None


@app.route('/api/partner-code', methods=['GET'])
@login_required
def get_partner_code():
    """Return a property's partner reference code (if any) and its full
    introduction history. Keyed by (state, address_key). Any logged-in user."""
    state = (request.args.get('state') or '').strip().lower()
    address = (request.args.get('address') or '').strip()
    addr_key = _address_key(address)
    if state not in ('vic', 'nsw', 'qld') or not addr_key:
        return jsonify({'error': 'Invalid state or address'}), 400
    db = get_db()
    row = db.execute('SELECT code FROM partner_codes WHERE state=? AND address_key=?',
                     (state, addr_key)).fetchone()
    intros = db.execute(
        'SELECT partner_name, introduced_by_name, introduced_at '
        'FROM introductions WHERE state=? AND address_key=? ORDER BY introduced_at',
        (state, addr_key)).fetchall()
    db.close()
    return jsonify({
        'code': row['code'] if row else None,
        'introductions': [dict(r) for r in intros]
    })


def _get_or_create_partner_code(db, state, address, addr_key, u):
    """Return the property's permanent RAD-#### code, allocating the next one
    on first need. Caller commits. Shared by the partner one-pager and the
    portfolio funder export so both use the same code for the same property."""
    row = db.execute('SELECT code FROM partner_codes WHERE state=? AND address_key=?',
                     (state, addr_key)).fetchone()
    if row:
        return row['code']
    for _attempt in range(6):
        mx = db.execute('SELECT MAX(seq) AS m FROM partner_codes').fetchone()
        nxt = (mx['m'] or 0) + 1
        candidate = 'RAD-%04d' % nxt
        try:
            db.execute(
                'INSERT INTO partner_codes '
                '(state, address, address_key, code, seq, created_by_id, created_by_name) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (state, address, addr_key, candidate, nxt, u['user_id'], u['full_name']))
            return candidate
        except sqlite3.IntegrityError:
            # A concurrent request grabbed this seq, or this property got a
            # code in parallel - re-read and either adopt it or retry.
            existing = db.execute(
                'SELECT code FROM partner_codes WHERE state=? AND address_key=?',
                (state, addr_key)).fetchone()
            if existing:
                return existing['code']
            continue
    return None


@app.route('/api/partner-code', methods=['POST'])
@login_required
def create_partner_code():
    """Introduce a property to a partner: assign its permanent RAD-#### code on
    first need (get-or-create), then record the introduction. Any logged-in
    user; the introduction is stamped with whoever generated it. The code
    sequence is global across all properties and never reused. Repeat
    generations for the same partner do not add duplicate introductions."""
    data = request.get_json(silent=True) or {}
    state = (data.get('state') or '').strip().lower()
    address = (data.get('address') or '').strip()
    partner = (data.get('partner') or 'Partner').strip()
    addr_key = _address_key(address)
    if state not in ('vic', 'nsw', 'qld'):
        return jsonify({'error': 'Invalid state'}), 400
    if not addr_key:
        return jsonify({'error': 'Address could not be normalised'}), 400
    if not partner:
        return jsonify({'error': 'Missing partner'}), 400
    u = request.current_user
    db = get_db()
    code = _get_or_create_partner_code(db, state, address, addr_key, u)
    if not code:
        db.close()
        return jsonify({'error': 'Could not allocate a reference code'}), 500
    # Record the introduction (one row per property+partner; repeats ignored).
    db.execute(
        'INSERT OR IGNORE INTO introductions '
        '(state, address, address_key, partner_name, introduced_by_id, introduced_by_name) '
        'VALUES (?, ?, ?, ?, ?, ?)',
        (state, address, addr_key, partner, u['user_id'], u['full_name']))
    db.commit()
    intros = db.execute(
        'SELECT partner_name, introduced_by_name, introduced_at '
        'FROM introductions WHERE state=? AND address_key=? ORDER BY introduced_at',
        (state, addr_key)).fetchall()
    db.close()
    return jsonify({'code': code, 'introductions': [dict(r) for r in intros]})


@app.route('/api/partner-code/lookup', methods=['GET'])
@login_required
def lookup_partner_code():
    """Resolve a reference code to its property. Accepts the code with or
    without the RAD- prefix and any zero-padding (matched on the numeric part).
    Any logged-in user. Returns {found, code, state, address}."""
    raw = request.args.get('code') or ''
    digits = ''.join(ch for ch in raw if ch.isdigit())
    if not digits:
        return jsonify({'found': False})
    seq = int(digits)
    db = get_db()
    row = db.execute('SELECT code, state, address, address_key FROM partner_codes WHERE seq=?', (seq,)).fetchone()
    if not row:
        db.close()
        return jsonify({'found': False})
    intros = db.execute(
        'SELECT partner_name, introduced_by_name, introduced_at '
        'FROM introductions WHERE state=? AND address_key=? ORDER BY introduced_at',
        (row['state'], row['address_key'])).fetchall()
    n_docs = db.execute(
        'SELECT COUNT(*) FROM partner_doc_snapshots WHERE code=?', (row['code'],)).fetchone()[0]
    db.close()
    first = dict(intros[0]) if intros else {}
    return jsonify({
        'found': True, 'code': row['code'], 'state': row['state'], 'address': row['address'],
        'partner': first.get('partner_name'),
        'introduced_at': first.get('introduced_at'),
        'introduced_by_name': first.get('introduced_by_name'),
        'introductions': [dict(r) for r in intros],
        'doc_count': n_docs,
    })


# ===========================================================================
# Partner doc snapshots
# ---------------------------------------------------------------------------
# Every partner-facing PDF is stored at the moment it is generated: the exact
# bytes, plus a JSON record of the inputs that produced them. Retrieval only —
# nothing is ever recomputed, because recomputation is not reproducible.
#
# Any signed-in team member can list and download past docs. Dating and
# versioning are what make that safe: two versions of the same deal are
# distinguishable at a glance rather than silently interchangeable.
# ===========================================================================

MAX_SNAPSHOT_PDF_BYTES = 8 * 1024 * 1024   # generous ceiling; real docs are ~40KB
VALID_DOC_TYPES = {'supavest', 'partner'}


def _snapshot_row_summary(r, include_snapshot=False):
    """Serialise a snapshot row for the list API. The PDF blob is never
    included here — only metadata plus the small headline `summary` block the
    client stored inside snapshot_json, so the list stays light no matter how
    many versions exist."""
    out = {
        'id': r['id'],
        'code': r['code'],
        'state': r['state'],
        'address': r['address'],
        'doc_type': r['doc_type'],
        'partner_name': r['partner_name'] or '',
        'version': r['version'],
        'pdf_filename': r['pdf_filename'] or '',
        'pdf_bytes': r['pdf_bytes'] or 0,
        'renderer_version': r['renderer_version'] or '',
        'generated_by_name': r['generated_by_name'] or '',
        'generated_at': r['generated_at'],
        'onedrive_status': (r['onedrive_status'] if 'onedrive_status' in r.keys() else None) or '',
        'onedrive_url': (r['onedrive_url'] if 'onedrive_url' in r.keys() else None) or '',
        'onedrive_error': (r['onedrive_error'] if 'onedrive_error' in r.keys() else None) or '',
        'summary': {},
    }
    try:
        snap = json.loads(r['snapshot_json'])
        out['summary'] = snap.get('summary') or {}
        if include_snapshot:
            out['snapshot'] = snap
    except (json.JSONDecodeError, TypeError):
        pass
    return out


# ===========================================================================
# SharePoint / OneDrive document sync
# ---------------------------------------------------------------------------
# Pushes every archived partner doc to a SharePoint document library as it is
# generated, so the PDFs exist somewhere outside this database. This is a COPY,
# not a backup: it protects against losing the Railway volume, not against
# someone deleting the SharePoint folder. Keep the volume backups running.
#
# Dormant until all three credentials are present in the environment. With no
# env vars set, nothing is attempted and nothing changes.
#
# Environment variables:
#   MS_TENANT_ID     Directory (tenant) ID from the Entra app registration
#   MS_CLIENT_ID     Application (client) ID
#   MS_CLIENT_SECRET Client secret VALUE (not the secret ID)
#   MS_SITE_URL      e.g. https://radiuspropertygroup.sharepoint.com/sites/RadiusPropertyGroup
#   MS_FOLDER_PATH   e.g. SDA Housing/SDA Partner Docs   (within the default library)
#
# Auth is client-credentials (app-only): the server signs in as itself, so
# there is no user token to expire and it works unattended.
# ===========================================================================

MS_TENANT_ID = os.environ.get('MS_TENANT_ID', '').strip()
MS_CLIENT_ID = os.environ.get('MS_CLIENT_ID', '').strip()
MS_CLIENT_SECRET = os.environ.get('MS_CLIENT_SECRET', '').strip()
MS_SITE_URL = os.environ.get('MS_SITE_URL', '').strip().rstrip('/')
MS_FOLDER_PATH = os.environ.get('MS_FOLDER_PATH', 'SDA Partner Docs').strip().strip('/')

# Cached access token and resolved site id. Both are cheap to re-fetch, so the
# cache is a plain module global rather than anything persistent.
_ms_token = {'value': None, 'expires_at': 0}
_ms_site_id = {'value': None}


def onedrive_configured():
    return bool(MS_TENANT_ID and MS_CLIENT_ID and MS_CLIENT_SECRET and MS_SITE_URL)


def _ms_get_token():
    """Client-credentials token for Microsoft Graph. Cached until 60s before
    expiry. Raises ValueError with a readable message on failure — the most
    common one being an expired client secret, which otherwise fails silently."""
    import time
    from urllib.parse import urlencode
    now = time.time()
    if _ms_token['value'] and now < _ms_token['expires_at']:
        return _ms_token['value']
    url = 'https://login.microsoftonline.com/%s/oauth2/v2.0/token' % MS_TENANT_ID
    body = urlencode({
        'client_id': MS_CLIENT_ID,
        'client_secret': MS_CLIENT_SECRET,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials',
    }).encode('utf-8')
    try:
        req = Request(url, data=body, method='POST',
                      headers={'Content-Type': 'application/x-www-form-urlencoded'})
        with urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
    except HTTPError as e:
        detail = ''
        try:
            detail = json.loads(e.read().decode('utf-8')).get('error_description', '')[:200]
        except Exception:
            pass
        raise ValueError('Token request failed (HTTP %s). %s' % (e.code, detail))
    except URLError as e:
        raise ValueError('Could not reach Microsoft login: %s' % e.reason)
    tok = data.get('access_token')
    if not tok:
        raise ValueError('No access_token in token response')
    _ms_token['value'] = tok
    _ms_token['expires_at'] = now + float(data.get('expires_in', 3600)) - 60
    return tok


def _ms_site_lookup(token):
    """Resolve MS_SITE_URL to a Graph site id, cached for the process life."""
    if _ms_site_id['value']:
        return _ms_site_id['value']
    from urllib.parse import urlparse
    u = urlparse(MS_SITE_URL)
    host = u.netloc
    path = u.path  # e.g. /sites/RadiusPropertyGroup
    if not host:
        raise ValueError('MS_SITE_URL does not look like a URL: ' + MS_SITE_URL)
    url = 'https://graph.microsoft.com/v1.0/sites/%s:%s' % (host, path)
    try:
        req = Request(url, headers={'Authorization': 'Bearer ' + token})
        with urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
    except HTTPError as e:
        hint = ''
        if e.code == 403:
            hint = (' — the app has no access to this site. If you used Sites.Selected, '
                    'the site permission grant (step 5) has not been applied.')
        elif e.code == 404:
            hint = ' — site not found; check MS_SITE_URL.'
        raise ValueError('Site lookup failed (HTTP %s)%s' % (e.code, hint))
    except URLError as e:
        raise ValueError('Could not reach Graph: %s' % e.reason)
    sid = data.get('id')
    if not sid:
        raise ValueError('No site id returned')
    _ms_site_id['value'] = sid
    return sid


def _ms_upload_pdf(pdf_bytes, folder_path, filename):
    """Upload one PDF to the site's default document library.
    Returns the item's webUrl. Raises ValueError with a readable message."""
    from urllib.parse import quote
    token = _ms_get_token()
    site_id = _ms_site_lookup(token)
    rel = '/'.join(p for p in (folder_path or '').split('/') if p)
    full = (rel + '/' + filename) if rel else filename
    # Graph path addressing: /drive/root:/<path>:/content . Each segment is
    # encoded but the slashes stay as separators.
    enc = '/'.join(quote(seg, safe='') for seg in full.split('/'))
    url = ('https://graph.microsoft.com/v1.0/sites/%s/drive/root:/%s:/content'
           % (site_id, enc))
    try:
        req = Request(url, data=pdf_bytes, method='PUT',
                      headers={'Authorization': 'Bearer ' + token,
                               'Content-Type': 'application/pdf'})
        with urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode('utf-8'))
    except HTTPError as e:
        detail = ''
        try:
            detail = json.loads(e.read().decode('utf-8')).get('error', {}).get('message', '')[:200]
        except Exception:
            pass
        raise ValueError('Upload failed (HTTP %s). %s' % (e.code, detail))
    except URLError as e:
        raise ValueError('Could not reach Graph: %s' % e.reason)
    return data.get('webUrl') or ''


def _sync_snapshot_to_onedrive(snapshot_id):
    """Upload a stored snapshot and record the outcome on its row.

    Runs after the snapshot has been committed, so a Graph failure can never
    cost us the archive record — the doc is safe in the database either way and
    the upload can be retried. Status is written back so the archive list can
    show plainly whether a doc reached SharePoint."""
    db = get_db()
    r = db.execute(
        'SELECT id, code, doc_type, version, pdf_filename, pdf_blob '
        'FROM partner_doc_snapshots WHERE id=?', (snapshot_id,)).fetchone()
    if not r:
        db.close()
        return {'ok': False, 'error': 'Snapshot not found'}
    if not onedrive_configured():
        db.execute("UPDATE partner_doc_snapshots SET onedrive_status='disabled' WHERE id=?",
                   (snapshot_id,))
        db.commit(); db.close()
        return {'ok': False, 'error': 'SharePoint sync not configured'}

    name = r['pdf_filename'] or ('%s_%s_v%d.pdf' % (r['code'], r['doc_type'], r['version']))
    base, ext = (name[:-4], '.pdf') if name.lower().endswith('.pdf') else (name, '.pdf')
    # Version is in the filename so a v2 never silently overwrites a v1 — the
    # whole point of versioning would be lost if it did.
    if ('_v%d' % r['version']) not in base:
        base = '%s_v%d' % (base, r['version'])
    filename = base + ext
    # One subfolder per reference code keeps the library navigable.
    folder = (MS_FOLDER_PATH + '/' + r['code']).strip('/')

    try:
        web_url = _ms_upload_pdf(bytes(r['pdf_blob']), folder, filename)
        db.execute(
            "UPDATE partner_doc_snapshots SET onedrive_status='ok', onedrive_url=?, "
            "onedrive_error=NULL, onedrive_at=datetime('now') WHERE id=?",
            (web_url, snapshot_id))
        db.commit(); db.close()
        return {'ok': True, 'url': web_url, 'filename': filename}
    except ValueError as e:
        msg = str(e)[:400]
        db.execute(
            "UPDATE partner_doc_snapshots SET onedrive_status='failed', onedrive_error=?, "
            "onedrive_at=datetime('now') WHERE id=?", (msg, snapshot_id))
        db.commit(); db.close()
        app.logger.warning('SharePoint sync failed for snapshot %s: %s', snapshot_id, msg)
        return {'ok': False, 'error': msg}


@app.route('/api/partner-doc-snapshot/<int:sid>/sync', methods=['POST'])
@login_required
def retry_partner_doc_sync(sid):
    """Retry the SharePoint upload for one snapshot. Any signed-in user —
    if a doc failed to sync, whoever notices should be able to fix it."""
    if not onedrive_configured():
        return jsonify({'ok': False, 'error': 'SharePoint sync is not configured on the server'}), 400
    res = _sync_snapshot_to_onedrive(sid)
    return (jsonify(res), 200 if res.get('ok') else 502)


@app.route('/api/onedrive-status')
@login_required
def onedrive_status():
    """Report whether sync is configured and, if so, whether it actually works.

    Deliberately performs a live token + site lookup rather than just checking
    that env vars exist — an expired client secret looks identical to a working
    one until you try to use it."""
    if not onedrive_configured():
        missing = [n for n, v in (('MS_TENANT_ID', MS_TENANT_ID), ('MS_CLIENT_ID', MS_CLIENT_ID),
                                  ('MS_CLIENT_SECRET', MS_CLIENT_SECRET), ('MS_SITE_URL', MS_SITE_URL))
                   if not v]
        return jsonify({'configured': False, 'missing': missing})
    try:
        token = _ms_get_token()
        site_id = _ms_site_lookup(token)
        return jsonify({'configured': True, 'ok': True, 'site_id': site_id,
                        'site_url': MS_SITE_URL, 'folder': MS_FOLDER_PATH})
    except ValueError as e:
        return jsonify({'configured': True, 'ok': False, 'error': str(e)}), 502


@app.route('/api/partner-doc-snapshot', methods=['POST'])
@login_required
def create_partner_doc_snapshot():
    """Store a generated partner doc: the PDF bytes plus the inputs behind it.

    Called by the dashboard immediately after a doc is produced. Failure here
    must never block the download the user just triggered, so the client fires
    this without awaiting it — but we still return a clear error so the client
    can warn that the doc was NOT archived."""
    data = request.get_json(silent=True) or {}
    code = (data.get('code') or '').strip().upper()
    state = (data.get('state') or '').strip().lower()
    address = (data.get('address') or '').strip()
    doc_type = (data.get('doc_type') or '').strip().lower()
    partner = (data.get('partner_name') or '').strip()
    filename = (data.get('filename') or '').strip()
    renderer = (data.get('renderer_version') or '').strip()
    pdf_b64 = data.get('pdf_base64') or ''
    snapshot = data.get('snapshot')

    if not code:
        return jsonify({'error': 'Missing code'}), 400
    if state not in ('vic', 'nsw', 'qld'):
        return jsonify({'error': 'Invalid state'}), 400
    if not address:
        return jsonify({'error': 'Missing address'}), 400
    if doc_type not in VALID_DOC_TYPES:
        return jsonify({'error': 'doc_type must be one of: ' + ', '.join(sorted(VALID_DOC_TYPES))}), 400
    if not isinstance(snapshot, dict) or not snapshot:
        return jsonify({'error': 'Missing snapshot payload'}), 400
    if not pdf_b64:
        return jsonify({'error': 'Missing pdf_base64'}), 400

    import base64
    try:
        pdf_bytes = base64.b64decode(pdf_b64, validate=True)
    except Exception:
        return jsonify({'error': 'pdf_base64 is not valid base64'}), 400
    if not pdf_bytes.startswith(b'%PDF'):
        return jsonify({'error': 'Decoded payload is not a PDF'}), 400
    if len(pdf_bytes) > MAX_SNAPSHOT_PDF_BYTES:
        return jsonify({'error': 'PDF exceeds size limit'}), 413

    addr_key = _address_key(address)
    u = request.current_user
    db = get_db()

    # Pull the sequence number off partner_codes if we have it, so a snapshot
    # can still be tied back to the code index numerically.
    seq_row = db.execute('SELECT seq FROM partner_codes WHERE code=?', (code,)).fetchone()
    seq = seq_row['seq'] if seq_row else None

    # Version increments per (code, doc_type). Retried on collision in case two
    # people generate the same doc simultaneously.
    new_id = None
    version = None
    for _attempt in range(6):
        mx = db.execute(
            'SELECT MAX(version) AS m FROM partner_doc_snapshots WHERE code=? AND doc_type=?',
            (code, doc_type)).fetchone()
        version = (mx['m'] or 0) + 1
        try:
            cur = db.execute(
                """INSERT INTO partner_doc_snapshots
                   (code, seq, state, address, address_key, doc_type, partner_name,
                    version, pdf_filename, pdf_bytes, pdf_blob, snapshot_json,
                    renderer_version, generated_by_id, generated_by_name)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (code, seq, state, address, addr_key, doc_type, partner or None,
                 version, filename or None, len(pdf_bytes),
                 sqlite3.Binary(pdf_bytes),
                 json.dumps(snapshot, separators=(',', ':')),
                 renderer or None, u['user_id'], u['full_name']))
            db.commit()
            new_id = cur.lastrowid
            break
        except sqlite3.IntegrityError:
            continue
    db.close()
    if new_id is None:
        return jsonify({'error': 'Could not allocate a version number'}), 500

    log_event('partner_doc_snapshot', {
        'code': code, 'doc_type': doc_type, 'version': version,
        'state': state, 'address': address, 'bytes': len(pdf_bytes),
    })

    # Copy to SharePoint. Deliberately AFTER the commit above: the archive
    # record is the thing that must not be lost, and a Graph outage should
    # never cost us one. A failure here is reported back so the client can
    # show it, and is retryable from the archive list.
    sync = {'attempted': False}
    if onedrive_configured():
        sync = _sync_snapshot_to_onedrive(new_id)
        sync['attempted'] = True

    return jsonify({'ok': True, 'id': new_id, 'version': version, 'code': code,
                    'sync': sync})


@app.route('/api/partner-doc-snapshots')
@login_required
def list_partner_doc_snapshots():
    """List stored docs for a code, or for a (state, address) pair.

    Newest first. Metadata and headline figures only — call the download
    endpoint for the actual PDF."""
    code = (request.args.get('code') or '').strip().upper()
    state = (request.args.get('state') or '').strip().lower()
    address = (request.args.get('address') or '').strip()

    db = get_db()
    if code:
        # Accept a bare number or an unpadded code the same way the code
        # lookup does, so "23" and "rad-23" both find RAD-0023.
        rows = db.execute(
            'SELECT * FROM partner_doc_snapshots WHERE code=? '
            'ORDER BY generated_at DESC, version DESC', (code,)).fetchall()
        if not rows:
            digits = ''.join(ch for ch in code if ch.isdigit())
            if digits:
                rows = db.execute(
                    'SELECT * FROM partner_doc_snapshots WHERE seq=? '
                    'ORDER BY generated_at DESC, version DESC', (int(digits),)).fetchall()
    elif state in ('vic', 'nsw', 'qld') and address:
        rows = db.execute(
            'SELECT * FROM partner_doc_snapshots WHERE state=? AND address_key=? '
            'ORDER BY generated_at DESC, version DESC',
            (state, _address_key(address))).fetchall()
    else:
        db.close()
        return jsonify({'error': 'Provide code, or state and address'}), 400
    db.close()
    return jsonify([_snapshot_row_summary(r) for r in rows])


@app.route('/api/partner-doc-snapshot/<int:sid>')
@login_required
def get_partner_doc_snapshot(sid):
    """Full snapshot record including the stored inputs, minus the PDF blob.

    This is what answers 'why does the doc say X' months later: it carries the
    PARAMS, SH and SUPAVEST settings in force at generation time alongside both
    the partner-facing and internal figures."""
    db = get_db()
    r = db.execute('SELECT * FROM partner_doc_snapshots WHERE id=?', (sid,)).fetchone()
    db.close()
    if not r:
        return jsonify({'error': 'Snapshot not found'}), 404
    return jsonify(_snapshot_row_summary(r, include_snapshot=True))


@app.route('/api/partner-doc-snapshot/<int:sid>/download')
@login_required
def download_partner_doc_snapshot(sid):
    """Return the exact PDF bytes that were generated. Any signed-in user."""
    db = get_db()
    r = db.execute(
        'SELECT code, doc_type, version, pdf_filename, pdf_blob '
        'FROM partner_doc_snapshots WHERE id=?', (sid,)).fetchone()
    db.close()
    if not r:
        return jsonify({'error': 'Snapshot not found'}), 404
    name = r['pdf_filename'] or ('%s_%s_v%d.pdf' % (r['code'], r['doc_type'], r['version']))
    # Guard the header against quoting/newline injection from a stored filename.
    safe = ''.join(ch for ch in name if ch.isalnum() or ch in '._- ').strip() or 'partner_doc.pdf'
    if not safe.lower().endswith('.pdf'):
        safe += '.pdf'
    resp = make_response(bytes(r['pdf_blob']))
    resp.headers['Content-Type'] = 'application/pdf'
    resp.headers['Content-Disposition'] = 'attachment; filename="%s"' % safe
    resp.headers['Cache-Control'] = 'private, max-age=0'
    log_event('partner_doc_retrieved', {'id': sid, 'code': r['code'],
                                        'doc_type': r['doc_type'], 'version': r['version']})
    return resp


@app.route('/api/manual-properties', methods=['GET'])
@login_required
def api_list_manual_properties():
    """List manual properties. Hidden ones (per C1 hidden_properties)
    are stripped before returning, so the dashboard sees the same view it
    does for CSV rows — without that, hiding a manual property via the
    existing ✕ button would not actually remove it from the screener."""
    db = get_db()
    rows = db.execute(
        'SELECT * FROM manual_properties ORDER BY created_at DESC'
    ).fetchall()
    # Build the set of (state, address_key) pairs that are hidden so we
    # can drop them in a single pass.
    hidden = db.execute(
        'SELECT state, address_key FROM hidden_properties'
    ).fetchall()
    db.close()
    hidden_set = {(h['state'], h['address_key']) for h in hidden}
    out = []
    for r in rows:
        if (r['state'], r['address_key']) in hidden_set:
            continue
        out.append(_manual_row_to_dict(r))
    return jsonify(out)


@app.route('/api/manual-properties/_diag', methods=['GET'])
@login_required
def api_manual_properties_diag():
    """Diagnostic endpoint for investigating 'manual properties disappear
    after logout/login' reports. Returns a summary that lets us tell apart
    the three possible failure modes:

      1. Properties are missing from the DB entirely  → total_rows is low
      2. Properties are in the DB but filtered out as hidden  → visible_rows < total_rows
      3. Properties are in the DB and not hidden, but the client isn't
         displaying them  → both counts look fine here, so the bug is
         client-side and the diagnostic ring buffer in dashboard.html will
         show what fetch() actually returned.

    Returns total_rows, visible_rows, hidden_rows, last_5_created (with
    minimal fields — id, state, address, created_by, created_at), and the
    list of currently-hidden (state, address_key) pairs for cross-reference.
    """
    db = get_db()
    total = db.execute('SELECT COUNT(*) FROM manual_properties').fetchone()[0]
    hidden = db.execute(
        'SELECT state, address_key FROM hidden_properties'
    ).fetchall()
    hidden_set = {(h['state'], h['address_key']) for h in hidden}
    all_rows = db.execute(
        'SELECT state, address_key, id, address, created_by_name, created_at '
        'FROM manual_properties ORDER BY created_at DESC'
    ).fetchall()
    db.close()
    visible = sum(1 for r in all_rows if (r['state'], r['address_key']) not in hidden_set)
    return jsonify({
        'total_rows': total,
        'visible_rows': visible,
        'hidden_rows': total - visible,
        'last_5_created': [
            {
                'id': r['id'],
                'state': r['state'],
                'address': r['address'],
                'created_by': r['created_by_name'],
                'created_at': r['created_at'],
                'is_hidden': (r['state'], r['address_key']) in hidden_set,
            }
            for r in all_rows[:5]
        ],
        'hidden_pairs_total': len(hidden_set),
    })


@app.route('/api/manual-properties', methods=['POST'])
@login_required
def api_create_manual_property():
    """Create a new manual property. Geocodes the address and runs the
    Google Places amenity lookups server-side."""
    data = request.get_json(silent=True) or {}
    cleaned, err = _validate_manual_payload(data, partial=False)
    if err:
        return jsonify({'error': err}), 400

    state = cleaned['state']
    address = cleaned['address']
    addr_key = _address_key(address)

    # Reject if this address already exists as a manual property in the
    # same state (the unique index would catch it but we'd rather a clean
    # 409 than an IntegrityError).
    db = get_db()
    existing = db.execute(
        'SELECT id FROM manual_properties WHERE state=? AND address_key=?',
        (state, addr_key)
    ).fetchone()
    if existing:
        db.close()
        return jsonify({'error': 'A manual property with that address already exists in ' + state.upper(),
                        'existing_id': existing['id']}), 409

    # Geocode. We don't hard-fail on geocode failure — the amenity lookups
    # will silently come back empty and the user can edit + recompute later.
    lat, lng = None, None
    if GOOGLE_MAPS_API_KEY:
        url = ('https://maps.googleapis.com/maps/api/geocode/json'
               '?address=' + quote_plus(address + ', Australia') +
               '&key=' + GOOGLE_MAPS_API_KEY)
        geo = _http_get_json(url)
        if geo.get('status') == 'OK' and geo.get('results'):
            loc = geo['results'][0]['geometry']['location']
            lat, lng = loc['lat'], loc['lng']

    amenities = _compute_amenities(lat, lng) if (lat is not None and lng is not None) else {
        'hosp1_name': '', 'hosp1_km': '',
        'hosp2_name': '', 'hosp2_km': '',
        'hosp3_name': '', 'hosp3_km': '',
        'medical_name': '', 'medical_km': '',
        'shop_name': '', 'shop_km': '',
        'train_name': '', 'train_km': '',
        'bus_km': '',
        'tram_name': '', 'tram_km': '',
    }

    u = request.current_user
    try:
        cur = db.execute("""INSERT INTO manual_properties
            (state, address, address_key, suburb, postcode, price, land,
             design_type, sale_type, auction_date, sa4, sa3, lat, lng,
             hosp1_name, hosp1_km, hosp2_name, hosp2_km, hosp3_name, hosp3_km,
             medical_name, medical_km, shop_name, shop_km, train_name, train_km,
             bus_km, tram_name, tram_km, created_by_id, created_by_name)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (state, address, addr_key, cleaned['suburb'], cleaned.get('postcode') or None,
             cleaned['price'], cleaned['land'], cleaned['design_type'],
             cleaned['sale_type'], cleaned.get('auction_date'),
             cleaned.get('sa4') or None, cleaned.get('sa3') or None,
             lat, lng,
             amenities['hosp1_name'] or None, amenities['hosp1_km'] or None,
             amenities['hosp2_name'] or None, amenities['hosp2_km'] or None,
             amenities['hosp3_name'] or None, amenities['hosp3_km'] or None,
             amenities['medical_name'] or None, amenities['medical_km'] or None,
             amenities['shop_name'] or None, amenities['shop_km'] or None,
             amenities['train_name'] or None, amenities['train_km'] or None,
             amenities['bus_km'] or None,
             amenities['tram_name'] or None, amenities['tram_km'] or None,
             u['user_id'], u['full_name']))
        db.commit()
        new_id = cur.lastrowid
    except sqlite3.IntegrityError:
        # Race condition: another request slipped past the explicit
        # duplicate check above and inserted the same (state, address_key)
        # between our SELECT and our INSERT. Return the same clean 409 the
        # explicit path returns rather than leaking the SQLite error.
        winner = db.execute(
            'SELECT id FROM manual_properties WHERE state=? AND address_key=?',
            (state, addr_key)
        ).fetchone()
        db.close()
        return jsonify({
            'error': 'A manual property with that address already exists in ' + state.upper(),
            'existing_id': winner['id'] if winner else None,
        }), 409

    row = db.execute('SELECT * FROM manual_properties WHERE id=?', (new_id,)).fetchone()
    db.close()
    log_event('manual_property_created', {'id': new_id, 'state': state, 'address': address})
    return jsonify({'ok': True, 'property': _manual_row_to_dict(row)})


@app.route('/api/manual-properties/<int:mid>', methods=['PUT'])
@login_required
def api_update_manual_property(mid):
    """Update a manual property. Only the creator and admins can edit.
    Address cannot be changed (it's the matching key for hides). Supports
    optional ?recompute_amenities=true to redo the Google Places lookups."""
    u = request.current_user
    db = get_db()
    row = db.execute('SELECT * FROM manual_properties WHERE id=?', (mid,)).fetchone()
    if not row:
        db.close()
        return jsonify({'error': 'Manual property not found'}), 404

    is_admin = u['role'] == 'admin'
    is_owner = (row['created_by_id'] == u['user_id'])
    if not (is_admin or is_owner):
        db.close()
        return jsonify({'error': 'Only the creator or an admin can edit this property'}), 403

    data = request.get_json(silent=True) or {}
    # Hand the validator the existing sale_type so auction_date validation
    # works even when the client only sends auction_date.
    data.setdefault('_existing_sale_type', row['sale_type'])
    cleaned, err = _validate_manual_payload(data, partial=True)
    if err:
        db.close()
        return jsonify({'error': err}), 400

    # Address is immutable — silently drop it if the client sent one.
    cleaned.pop('address', None)
    # State change is allowed (sometimes a row gets entered under the wrong
    # state); recompute address_key isn't needed because address didn't change.

    if not cleaned and 'recompute_amenities' not in request.args:
        db.close()
        return jsonify({'error': 'No editable fields supplied'}), 400

    # Build dynamic UPDATE
    set_clauses, values = [], []
    for k, v in cleaned.items():
        set_clauses.append(k + '=?')
        values.append(v)

    # Optional amenity recompute
    if request.args.get('recompute_amenities', '').lower() == 'true':
        lat = row['lat']
        lng = row['lng']
        # If lat/lng missing, try to geocode now using the (immutable) address
        if (lat is None or lng is None) and GOOGLE_MAPS_API_KEY:
            url = ('https://maps.googleapis.com/maps/api/geocode/json'
                   '?address=' + quote_plus(row['address'] + ', Australia') +
                   '&key=' + GOOGLE_MAPS_API_KEY)
            geo = _http_get_json(url)
            if geo.get('status') == 'OK' and geo.get('results'):
                loc = geo['results'][0]['geometry']['location']
                lat, lng = loc['lat'], loc['lng']
                set_clauses += ['lat=?', 'lng=?']
                values += [lat, lng]
        if lat is not None and lng is not None:
            am = _compute_amenities(lat, lng)
            for col in ('hosp1_name','hosp1_km','hosp2_name','hosp2_km',
                        'hosp3_name','hosp3_km','medical_name','medical_km',
                        'shop_name','shop_km','train_name','train_km',
                        'bus_km','tram_name','tram_km'):
                set_clauses.append(col + '=?')
                values.append(am[col] if am[col] != '' else None)

    # Always stamp last_edited_*
    set_clauses += ['last_edited_by_id=?', 'last_edited_by_name=?', 'last_edited_at=?']
    values += [u['user_id'], u['full_name'], datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')]

    values.append(mid)
    db.execute('UPDATE manual_properties SET ' + ', '.join(set_clauses) + ' WHERE id=?', values)
    db.commit()

    updated = db.execute('SELECT * FROM manual_properties WHERE id=?', (mid,)).fetchone()
    db.close()
    log_event('manual_property_edited', {'id': mid, 'fields': list(cleaned.keys()),
                                          'recomputed': request.args.get('recompute_amenities','').lower()=='true'})
    return jsonify({'ok': True, 'property': _manual_row_to_dict(updated)})


@app.route('/api/manual-properties/<int:mid>', methods=['DELETE'])
@admin_required
def api_delete_manual_property(mid):
    """Permanently delete a manual property. Admin only.
    Also purges any matching hidden_properties row so the same address can
    be re-added later without a stale C1 hide blocking it."""
    db = get_db()
    row = db.execute(
        'SELECT id, state, address, address_key FROM manual_properties WHERE id=?', (mid,)
    ).fetchone()
    if not row:
        db.close()
        return jsonify({'error': 'Manual property not found'}), 404
    state = row['state']
    addr_key = row['address_key']
    db.execute('DELETE FROM manual_properties WHERE id=?', (mid,))
    purged = db.execute(
        'DELETE FROM hidden_properties WHERE state=? AND address_key=?',
        (state, addr_key)
    ).rowcount
    db.commit()
    db.close()
    log_event('manual_property_deleted', {
        'id': mid, 'state': state, 'address': row['address'],
        'hide_rows_purged': purged,
    })
    return jsonify({'ok': True, 'hide_rows_purged': purged})


# ===========================================================================
# Portfolios (Stage 1)
# ---------------------------------------------------------------------------
# Every logged-in user can SEE every portfolio. Only admins (Jason, Tanya) can
# edit any portfolio; team members can edit only portfolios they created.
# All write endpoints check this server-side via _portfolio_can_edit().
# Estimates are calculated in the dashboard from the stored snapshot plus the
# current Settings; the server only stores and permission-checks.
# ===========================================================================
PORTFOLIO_STATES = {'vic', 'nsw', 'qld'}
PORTFOLIO_SNAPSHOT_MAX_BYTES = 50000
PORTFOLIO_PLACES = {'2p': 2, '3p': 3, 'dp': 4, 'd3': 6, 'hv': 2}  # hv: the 2P house; villa resident stored as occupancy['villa']


def _portfolio_can_edit(u, row):
    return u.get('role') == 'admin' or row['created_by_id'] == u.get('user_id')


def _portfolio_summary(r, u, item_count=0):
    return {
        'id': r['id'],
        'name': r['name'],
        'created_by_id': r['created_by_id'],
        'created_by_name': r['created_by_name'],
        'created_at': r['created_at'],
        'updated_at': r['updated_at'],
        'item_count': item_count,
        'can_edit': _portfolio_can_edit(u, r),
        'equity_type': r['equity_type'] if 'equity_type' in r.keys() else None,
        'equity_value': r['equity_value'] if 'equity_value' in r.keys() else None,
    }


# Stage 3 live tracking. Order matters: index >= 2 means under contract or later.
PORTFOLIO_STATUSES = ['target', 'offer', 'contract', 'settled', 'design', 'construction', 'complete']
_PORTFOLIO_COST_ACTUALS = ('price', 'stamp', 'build', 'cons')


def _clean_portfolio_actuals(a):
    """Validate the actuals object for a line. Returns (clean_dict, error).
    Cost actuals: price, stamp, build (build contract excl. contingency), cons
    (consultant quotes) - each a number >= 0, or null/missing to fall back to
    the estimate. rents: agreed SDA rent per resident per year, as lists per
    category ({il:[..], fa:[..], hps:[..]}) plus villa for the 2P+villa model;
    a null slot means not yet agreed."""
    if a is None:
        return {}, None
    if not isinstance(a, dict):
        return None, 'actuals must be an object'

    def num(v, label):
        if v is None or v == '':
            return None, None
        try:
            f = float(v)
        except (TypeError, ValueError):
            return None, '%s must be a number' % label
        if f != f or f < 0 or f > 1e9:
            return None, '%s must be a positive amount' % label
        return round(f, 2), None

    out = {}
    for k in _PORTFOLIO_COST_ACTUALS:
        v, err = num(a.get(k), k)
        if err:
            return None, err
        if v is not None:
            out[k] = v
    rents = a.get('rents')
    if rents is not None:
        if not isinstance(rents, dict):
            return None, 'rents must be an object'
        r_out = {}
        for cat in ('il', 'fa', 'hps'):
            lst = rents.get(cat)
            if lst is None:
                continue
            if not isinstance(lst, list) or len(lst) > 6:
                return None, 'rents.%s must be a list of up to 6 amounts' % cat
            clean = []
            for v in lst:
                f, err = num(v, 'Agreed rent')
                if err:
                    return None, err
                clean.append(f)
            if any(x is not None for x in clean):
                r_out[cat] = clean
        v, err = num(rents.get('villa'), 'Agreed villa rent')
        if err:
            return None, err
        if v is not None:
            r_out['villa'] = v
        if r_out:
            out['rents'] = r_out
    return out, None


def _prune_portfolio_rents(act, occ_json):
    """Agreed rents belong to residents. Trim them to the residents now
    entered; drop them all when the line is back on a full house."""
    if not act or 'rents' not in act:
        return act
    try:
        occ = json.loads(occ_json) if occ_json else None
    except (ValueError, TypeError):
        occ = None
    if not occ:
        act.pop('rents', None)
        return act
    rents = act.get('rents') or {}
    out = {}
    for cat in ('il', 'fa', 'hps'):
        n = int(occ.get(cat) or 0)
        lst = (rents.get(cat) or [])[:n]
        if any(x is not None for x in lst):
            out[cat] = lst
    if occ.get('villa') and rents.get('villa') is not None:
        out['villa'] = rents['villa']
    if out:
        act['rents'] = out
    else:
        act.pop('rents', None)
    return act


_ITEMISED_KEY = __import__('re').compile(r'^[a-z][a-z0-9_]{0,23}$')


def _clean_itemised(v):
    """Per-project changes to the itemised cost lines: {key: {on, qty, rate, gst}}.
    Only differences from the Radius standard are stored."""
    if v is None:
        return {}, None
    if not isinstance(v, dict):
        return None, 'itemised must be an object'
    if len(v) > 120:
        return None, 'Too many itemised lines'
    out = {}
    for k, o in v.items():
        if not isinstance(k, str) or not _ITEMISED_KEY.match(k) or not isinstance(o, dict):
            return None, 'Bad itemised line'
        c = {}
        if 'on' in o:
            c['on'] = bool(o['on'])
        for f in ('qty', 'rate'):
            if f in o and o[f] is not None:
                try:
                    n = float(o[f])
                except (TypeError, ValueError):
                    return None, 'Qty and rate must be numbers'
                if not math.isfinite(n) or n < 0 or n > 1e9:
                    return None, 'Qty and rate must be between 0 and 1,000,000,000'
                c[f] = n
        if 'gst' in o:
            if o['gst'] not in ('+GST', 'Inc', 'None'):
                return None, 'GST must be +GST, Inc or None'
            c['gst'] = o['gst']
        if c:
            out[k] = c
    return out, None


RADIUS_STD_MARGIN = 200000.0   # Radius margin built into the standard house build price


def _portfolio_item_to_dict(r):
    try:
        snap = json.loads(r['snapshot_json'])
    except (ValueError, TypeError):
        snap = {}
    occ = None
    try:
        if r['occupancy']:
            occ = json.loads(r['occupancy'])
    except (ValueError, TypeError, IndexError, KeyError):
        occ = None
    keys = r.keys()
    status = (r['status'] if 'status' in keys else None) or 'target'
    if status not in PORTFOLIO_STATUSES:
        status = 'target'
    act = None
    try:
        if 'actuals' in keys and r['actuals']:
            act = json.loads(r['actuals'])
    except (ValueError, TypeError):
        act = None
    itm = None
    try:
        if 'itemised' in keys and r['itemised']:
            itm = json.loads(r['itemised'])
    except (ValueError, TypeError):
        itm = None
    # Radius build margin per house. Admins see and set the margin; everyone
    # else only sees the effect on the build price (build_adj, per house).
    mg = r['margin'] if 'margin' in keys else None
    out_extra = {'build_adj': (float(mg) - RADIUS_STD_MARGIN) if mg is not None else 0}
    try:
        if _is_admin_user(request.current_user):
            out_extra['margin'] = mg
    except Exception:
        pass
    return {
        **out_extra,
        'id': r['id'],
        'itemised': itm,
        'state': r['state'],
        'address': r['address'],
        'address_key': r['address_key'],
        'model': r['model'],
        'occupancy': occ,
        'status': status,
        'actuals': act,
        'snapshot': snap,
        'added_by_name': r['added_by_name'] or '',
        'added_at': r['added_at'],
    }


def _clean_portfolio_name(data):
    name = ' '.join(str((data or {}).get('name') or '').split())
    if not name:
        return None, 'Portfolio name is required'
    if len(name) > 120:
        return None, 'Portfolio name must be 120 characters or fewer'
    return name, None


def _load_portfolio_for_edit(db, pid):
    """Returns (row, error_response). error_response is set on 404/403."""
    row = db.execute('SELECT * FROM portfolios WHERE id=?', (pid,)).fetchone()
    if not row:
        return None, (jsonify({'error': 'Portfolio not found'}), 404)
    if not _portfolio_can_edit(request.current_user, row):
        return None, (jsonify({'error': 'Only an admin or the person who created this portfolio can change it'}), 403)
    return row, None


def _touch_portfolio(db, pid):
    db.execute("UPDATE portfolios SET updated_at=datetime('now') WHERE id=?", (pid,))


@app.route('/api/portfolios', methods=['GET'])
@login_required
def api_list_portfolios():
    u = request.current_user
    db = get_db()
    rows = db.execute(
        'SELECT p.*, (SELECT COUNT(*) FROM portfolio_items i WHERE i.portfolio_id=p.id) AS n '
        'FROM portfolios p ORDER BY p.updated_at DESC, p.id DESC'
    ).fetchall()
    db.close()
    return jsonify([_portfolio_summary(r, u, r['n']) for r in rows])


@app.route('/api/portfolios', methods=['POST'])
@login_required
def api_create_portfolio():
    u = request.current_user
    name, err = _clean_portfolio_name(request.get_json(silent=True))
    if err:
        return jsonify({'error': err}), 400
    db = get_db()
    cur = db.execute('INSERT INTO portfolios (name, created_by_id, created_by_name) VALUES (?,?,?)',
                     (name, u['user_id'], u['full_name']))
    db.commit()
    row = db.execute('SELECT * FROM portfolios WHERE id=?', (cur.lastrowid,)).fetchone()
    db.close()
    log_event('portfolio_created', {'id': row['id'], 'name': name})
    return jsonify({'ok': True, 'portfolio': _portfolio_summary(row, u, 0)})


@app.route('/api/portfolios/<int:pid>', methods=['GET'])
@login_required
def api_get_portfolio(pid):
    u = request.current_user
    db = get_db()
    row = db.execute('SELECT * FROM portfolios WHERE id=?', (pid,)).fetchone()
    if not row:
        db.close()
        return jsonify({'error': 'Portfolio not found'}), 404
    items = db.execute('SELECT * FROM portfolio_items WHERE portfolio_id=? ORDER BY id', (pid,)).fetchall()
    db.close()
    out = _portfolio_summary(row, u, len(items))
    out['items'] = [_portfolio_item_to_dict(i) for i in items]
    return jsonify(out)


@app.route('/api/portfolios/<int:pid>', methods=['PUT'])
@login_required
def api_update_portfolio(pid):
    """Rename a portfolio and/or set its total equity.
    equity: {"type": "amount"|"pct", "value": n} or null (= use the screener LVR).
    Equity is the total cash going into the portfolio; debt funds the rest."""
    data = request.get_json(silent=True) or {}
    if 'name' not in data and 'equity' not in data:
        return jsonify({'error': 'Nothing to change'}), 400
    sets, vals = [], []
    if 'name' in data:
        name, err = _clean_portfolio_name(data)
        if err:
            return jsonify({'error': err}), 400
        sets.append('name=?'); vals.append(name)
    if 'equity' in data:
        eq = data.get('equity')
        if eq is None:
            sets += ['equity_type=?', 'equity_value=?']; vals += [None, None]
        else:
            if not isinstance(eq, dict):
                return jsonify({'error': 'equity must be {type, value} or null'}), 400
            et = str(eq.get('type') or '').strip().lower()
            if et not in ('amount', 'pct'):
                return jsonify({'error': 'equity type must be amount or pct'}), 400
            try:
                ev = float(eq.get('value'))
            except (TypeError, ValueError):
                return jsonify({'error': 'Equity must be a number'}), 400
            if ev < 0 or (et == 'pct' and ev > 100):
                return jsonify({'error': 'Equity must be 0 or more (and at most 100%)'}), 400
            sets += ['equity_type=?', 'equity_value=?']; vals += [et, ev]
    db = get_db()
    row, bad = _load_portfolio_for_edit(db, pid)
    if bad:
        db.close()
        return bad
    db.execute("UPDATE portfolios SET " + ', '.join(sets) + ", updated_at=datetime('now') WHERE id=?", vals + [pid])
    db.commit()
    db.close()
    log_event('portfolio_updated', {'id': pid, 'fields': [k for k in ('name', 'equity') if k in data]})
    return jsonify({'ok': True})


@app.route('/api/portfolios/<int:pid>', methods=['DELETE'])
@login_required
def api_delete_portfolio(pid):
    db = get_db()
    row, bad = _load_portfolio_for_edit(db, pid)
    if bad:
        db.close()
        return bad
    n = db.execute('DELETE FROM portfolio_items WHERE portfolio_id=?', (pid,)).rowcount
    db.execute('DELETE FROM portfolios WHERE id=?', (pid,))
    db.commit()
    db.close()
    log_event('portfolio_deleted', {'id': pid, 'name': row['name'], 'items': n})
    return jsonify({'ok': True})


@app.route('/api/portfolios/<int:pid>/items', methods=['POST'])
@login_required
def api_add_portfolio_item(pid):
    u = request.current_user
    data = request.get_json(silent=True) or {}
    snap = data.get('snapshot')
    model = str(data.get('model') or '').strip().lower()
    if not isinstance(snap, dict):
        return jsonify({'error': 'snapshot is required'}), 400
    if model not in VALID_DESIGN_TYPES:
        return jsonify({'error': 'model must be one of: 2p, 3p, dp, d3, hv'}), 400
    address = snap.get('address')
    state = str(snap.get('state') or '').strip().lower()
    if not isinstance(address, str) or not address.strip():
        return jsonify({'error': 'snapshot.address is required'}), 400
    if state not in PORTFOLIO_STATES:
        return jsonify({'error': 'snapshot.state must be one of: vic, nsw, qld'}), 400
    try:
        price = float(snap.get('price'))
        land = float(snap.get('land') or 0)
    except (TypeError, ValueError):
        return jsonify({'error': 'snapshot.price and snapshot.land must be numbers'}), 400
    if price <= 0 or land < 0:
        return jsonify({'error': 'snapshot.price must be above zero'}), 400
    if not isinstance(snap.get('sda'), dict):
        return jsonify({'error': 'snapshot.sda (NDIS rates) is required'}), 400
    snap['state'] = state
    snap_json = json.dumps(snap)
    if len(snap_json) > PORTFOLIO_SNAPSHOT_MAX_BYTES:
        return jsonify({'error': 'snapshot too large'}), 400
    addr_key = _address_key(address)

    db = get_db()
    row, bad = _load_portfolio_for_edit(db, pid)
    if bad:
        db.close()
        return bad
    try:
        # Address is stored exactly as received (byte-for-byte); only the
        # matching key is normalised.
        cur = db.execute(
            'INSERT INTO portfolio_items (portfolio_id, state, address, address_key, model, snapshot_json, '
            'added_by_id, added_by_name) VALUES (?,?,?,?,?,?,?,?)',
            (pid, state, address, addr_key, model, snap_json, u['user_id'], u['full_name']))
        _touch_portfolio(db, pid)
        db.commit()
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({'error': 'That property is already in "' + row['name'] + '"'}), 409
    item = db.execute('SELECT * FROM portfolio_items WHERE id=?', (cur.lastrowid,)).fetchone()
    db.close()
    log_event('portfolio_item_added', {'portfolio_id': pid, 'address': address, 'model': model})
    return jsonify({'ok': True, 'item': _portfolio_item_to_dict(item)})


@app.route('/api/portfolios/<int:pid>/items/<int:iid>', methods=['PUT'])
@login_required
def api_update_portfolio_item(pid, iid):
    """Change a line's build model and/or its residents now.
    occupancy: {"il":n,"fa":n,"hps":n} or null (= full house on the income basis).
    If a model change leaves fewer places than the residents entered, the
    residents are cleared back to a full house."""
    data = request.get_json(silent=True) or {}
    if not any(k in data for k in ('model', 'occupancy', 'status', 'actuals', 'itemised', 'margin')):
        return jsonify({'error': 'Nothing to change'}), 400
    db = get_db()
    row, bad = _load_portfolio_for_edit(db, pid)
    if bad:
        db.close()
        return bad
    item = db.execute('SELECT * FROM portfolio_items WHERE id=? AND portfolio_id=?', (iid, pid)).fetchone()
    if not item:
        db.close()
        return jsonify({'error': 'Property not found in this portfolio'}), 404

    model = item['model']
    if 'model' in data:
        model = str(data.get('model') or '').strip().lower()
        if model not in VALID_DESIGN_TYPES:
            db.close()
            return jsonify({'error': 'model must be one of: 2p, 3p, dp, d3, hv'}), 400
    places = PORTFOLIO_PLACES[model]

    occ_json = item['occupancy']
    if 'occupancy' in data:
        occ = data.get('occupancy')
        if occ is None:
            occ_json = None
        else:
            if not isinstance(occ, dict):
                db.close()
                return jsonify({'error': 'occupancy must be {il, fa, hps} or null'}), 400
            clean = {}
            for k in ('il', 'fa', 'hps'):
                try:
                    v = int(occ.get(k) or 0)
                except (TypeError, ValueError):
                    db.close()
                    return jsonify({'error': 'Resident numbers must be whole numbers'}), 400
                if v < 0:
                    db.close()
                    return jsonify({'error': 'Resident numbers cannot be negative'}), 400
                clean[k] = v
            if sum(clean.values()) > places:
                db.close()
                return jsonify({'error': 'This build model has %d places, so it can take at most %d residents' % (places, places)}), 400
            if model == 'hv':
                villa = str(occ.get('villa') or '').strip().lower()
                if villa not in ('', 'il', 'fa', 'hps'):
                    db.close()
                    return jsonify({'error': 'villa must be il, fa, hps or empty'}), 400
                clean['villa'] = villa
            occ_json = json.dumps(clean)
    elif occ_json:
        # Model changed: keep the residents only if they still fit.
        try:
            cur = json.loads(occ_json)
            if sum(int(cur.get(k) or 0) for k in ('il', 'fa', 'hps')) > places:
                occ_json = None
            else:
                if model != 'hv':
                    cur.pop('villa', None)
                occ_json = json.dumps(cur)
        except (ValueError, TypeError, AttributeError):
            occ_json = None

    keys = item.keys()
    status = (item['status'] if 'status' in keys else None) or 'target'
    if 'status' in data:
        status = str(data.get('status') or '').strip().lower()
        if status not in PORTFOLIO_STATUSES:
            db.close()
            return jsonify({'error': 'status must be one of: ' + ', '.join(PORTFOLIO_STATUSES)}), 400

    try:
        act = json.loads(item['actuals']) if ('actuals' in keys and item['actuals']) else {}
    except (ValueError, TypeError):
        act = {}
    if not isinstance(act, dict):
        act = {}
    if 'actuals' in data:
        new_act, err = _clean_portfolio_actuals(data.get('actuals'))
        if err:
            db.close()
            return jsonify({'error': err}), 400
        act = new_act
    act = _prune_portfolio_rents(act, occ_json)
    act_json = json.dumps(act) if act else None

    itm_json = item['itemised'] if 'itemised' in keys else None
    if 'itemised' in data:
        itm, err = _clean_itemised(data.get('itemised'))
        if err:
            db.close()
            return jsonify({'error': err}), 400
        itm_json = json.dumps(itm) if itm else None
    margin = item['margin'] if 'margin' in keys else None
    if 'margin' in data:
        if not _is_admin_user(request.current_user):
            db.close()
            return jsonify({'error': 'Only an admin can change the Radius build margin'}), 403
        mv = data.get('margin')
        if mv is None or mv == '':
            margin = None
        else:
            try:
                margin = float(mv)
            except (TypeError, ValueError):
                db.close()
                return jsonify({'error': 'Margin must be a number'}), 400
            if not math.isfinite(margin) or margin < 0 or margin > 5000000:
                db.close()
                return jsonify({'error': 'Margin must be between $0 and $5,000,000'}), 400
    db.execute('UPDATE portfolio_items SET model=?, occupancy=?, status=?, actuals=?, itemised=?, margin=? WHERE id=?',
               (model, occ_json, status, act_json, itm_json, margin, iid))
    _touch_portfolio(db, pid)
    db.commit()
    updated = db.execute('SELECT * FROM portfolio_items WHERE id=?', (iid,)).fetchone()
    db.close()
    log_event('portfolio_item_updated', {'portfolio_id': pid, 'item_id': iid, 'model': model,
                                         'occupancy': occ_json, 'status': status, 'actuals': act_json,
                                         'itemised': itm_json, 'margin_changed': 'margin' in data})
    return jsonify({'ok': True, 'item': _portfolio_item_to_dict(updated)})


@app.route('/api/portfolios/<int:pid>/items/<int:iid>', methods=['DELETE'])
@login_required
def api_delete_portfolio_item(pid, iid):
    db = get_db()
    row, bad = _load_portfolio_for_edit(db, pid)
    if bad:
        db.close()
        return bad
    item = db.execute('SELECT address FROM portfolio_items WHERE id=? AND portfolio_id=?', (iid, pid)).fetchone()
    if not item:
        db.close()
        return jsonify({'error': 'Property not found in this portfolio'}), 404
    db.execute('DELETE FROM portfolio_items WHERE id=?', (iid,))
    _touch_portfolio(db, pid)
    db.commit()
    db.close()
    log_event('portfolio_item_removed', {'portfolio_id': pid, 'address': item['address']})
    return jsonify({'ok': True})


@app.route('/api/portfolios/<int:pid>/funder-codes', methods=['POST'])
@login_required
def api_portfolio_funder_codes(pid):
    """For the funder export: get-or-create the RAD-#### code for every line in
    the portfolio and record the introduction to the named funder (same tables
    as the partner one-pager). Returns {codes: {item_id: code}} only; the client
    builds the funder document from codes, never from addresses. Any logged-in
    user may generate a funder export, as with partner documents."""
    data = request.get_json(silent=True) or {}
    partner = ' '.join(str(data.get('partner') or '').split())
    if not partner:
        return jsonify({'error': 'Funder name is required'}), 400
    if len(partner) > 120:
        return jsonify({'error': 'Funder name must be 120 characters or fewer'}), 400
    u = request.current_user
    db = get_db()
    pf = db.execute('SELECT id FROM portfolios WHERE id=?', (pid,)).fetchone()
    if not pf:
        db.close()
        return jsonify({'error': 'Portfolio not found'}), 404
    items = db.execute('SELECT id, state, address, address_key FROM portfolio_items WHERE portfolio_id=?',
                       (pid,)).fetchall()
    codes = {}
    for it in items:
        code = _get_or_create_partner_code(db, it['state'], it['address'], it['address_key'], u)
        if not code:
            db.rollback()
            db.close()
            return jsonify({'error': 'Could not allocate a reference code'}), 500
        codes[str(it['id'])] = code
        db.execute(
            'INSERT OR IGNORE INTO introductions '
            '(state, address, address_key, partner_name, introduced_by_id, introduced_by_name) '
            'VALUES (?, ?, ?, ?, ?, ?)',
            (it['state'], it['address'], it['address_key'], partner, u['user_id'], u['full_name']))
    db.commit()
    db.close()
    log_event('portfolio_funder_export', {'portfolio_id': pid, 'partner': partner, 'items': len(codes)})
    return jsonify({'ok': True, 'codes': codes})


# ===========================================================================
# C3: SDA Supply intelligence (SA2-level)
# ---------------------------------------------------------------------------
# Two NDIS XLSX files (SDA-by-provider and Group-homes-by-provider) get
# uploaded together by an admin. Per SA2, we compute:
#   - Filled SDA places, vacancies, providers
#   - Filled group-home places, vacancies, providers (future SDA demand,
#     since group homes are being wound down and residents will need SDA)
#   - Net 'conversion deficit' = filled_gh - sda_vacancies
#   - Design-category mix of existing SDA stock
# Robust is excluded from BOTH sides because RPG doesn't build for Robust
# participants (they need dedicated specialty facilities, not HPS dwellings).
# The aggregated blob is stored once and served to every client on dashboard
# load — no per-row API calls.
# ===========================================================================

def _title_case_provider(name):
    """Some provider names come in ALL CAPS, others Title Case. Normalise to
    Title Case for display, but leave already-mixed names alone."""
    if not name:
        return ''
    s = str(name).strip()
    if any(c.islower() for c in s):
        return s
    out = []
    for w in s.split():
        if '&' in w or '/' in w:
            out.append(w)
        else:
            out.append(w.title())
    return ' '.join(out)


def _parse_supply_xlsx(file_storage, kind):
    """Parse one of the NDIS XLSX files into a list of dicts.
    `kind` is 'sda' or 'gh'; both files have the same column structure.
    Returns (rows, error_or_none, data_as_of_iso)."""
    try:
        from openpyxl import load_workbook
        wb = load_workbook(file_storage, read_only=True, data_only=True)
        ws = wb.active
    except Exception as e:
        return None, f'Could not open as XLSX: {e}', None

    rows_iter = ws.iter_rows(values_only=True)
    try:
        header = list(next(rows_iter))
    except StopIteration:
        return None, 'File is empty', None

    # Required columns
    required = ['State or Territory', 'SA4 Region', 'SA3 Region', 'SA2 Region',
                'Provider name', 'Design category', 'Places', 'Vacancies']
    missing = [c for c in required if c not in header]
    if missing:
        return None, f'Missing columns: {", ".join(missing)}', None

    col = {name: header.index(name) for name in header if name in required + ['Date', 'Dwelling type']}

    rows = []
    data_date = None
    for r in rows_iter:
        if not r or all(v is None for v in r):
            continue
        try:
            state = str(r[col['State or Territory']] or '').strip()
            sa4 = str(r[col['SA4 Region']] or '').strip()
            sa3 = str(r[col['SA3 Region']] or '').strip()
            sa2 = str(r[col['SA2 Region']] or '').strip()
            provider = str(r[col['Provider name']] or '').strip()
            design = str(r[col['Design category']] or '').strip()
            places = int(r[col['Places']] or 0)
            vacancies = int(r[col['Vacancies']] or 0)
            if 'Dwelling type' in col:
                dwelling = str(r[col['Dwelling type']] or '').strip()
            else:
                dwelling = ''
            if 'Date' in col and r[col['Date']]:
                d = r[col['Date']]
                if hasattr(d, 'isoformat'):
                    data_date = d.isoformat()[:10]
                else:
                    data_date = str(d)[:10]
        except (ValueError, IndexError, TypeError):
            continue
        if not state or not sa2:
            continue
        rows.append({
            'state': state, 'sa4': sa4, 'sa3': sa3, 'sa2': sa2,
            'provider': provider, 'design': design, 'dwelling': dwelling,
            'places': places, 'vacancies': vacancies,
        })

    return rows, None, data_date


def _aggregate_supply(sda_rows, gh_rows):
    """Combine per-row supply data into per-SA2 aggregates.
    Excludes Robust dwellings from both sides — RPG only builds HPS dwellings
    accepting HPS/FA/IL participants; Robust is a separate market segment.

    Returns {state_code: {sa2_name: aggregate_dict}}."""
    STATE_MAP = {
        'Victoria': 'vic',
        'New South Wales': 'nsw',
        'Queensland': 'qld',
    }

    # Filter Robust out of both inputs
    sda_rel = [r for r in sda_rows if r['design'] != 'Robust']
    gh_rel  = [r for r in gh_rows  if r['design'] != 'Robust']

    # Index by (state, sa2)
    by_sa2 = {}
    for r in sda_rel:
        st = STATE_MAP.get(r['state'])
        if not st:
            continue
        key = (st, r['sa2'])
        rec = by_sa2.setdefault(key, _empty_sa2_record(r['sa3'], r['sa4']))
        rec['sda_places'] += r['places']
        rec['sda_vacancies'] += r['vacancies']
        # Provider tally for SDA side
        prov = rec['sda_provider_idx'].setdefault(r['provider'], {'places': 0, 'vacancies': 0})
        prov['places'] += r['places']
        prov['vacancies'] += r['vacancies']
        # Design mix
        design_key = {
            'High physical support': 'HPS',
            'Fully accessible': 'FA',
            'Improved liveability': 'IL',
            'Multiple design category': 'Multi',
        }.get(r['design'])
        if design_key:
            rec['design_mix'][design_key] += r['places']

    for r in gh_rel:
        st = STATE_MAP.get(r['state'])
        if not st:
            continue
        key = (st, r['sa2'])
        rec = by_sa2.setdefault(key, _empty_sa2_record(r['sa3'], r['sa4']))
        rec['gh_places'] += r['places']
        rec['gh_vacancies'] += r['vacancies']
        prov = rec['gh_provider_idx'].setdefault(r['provider'], {'places': 0, 'vacancies': 0})
        prov['places'] += r['places']
        prov['vacancies'] += r['vacancies']

    # Finalise: compute derived fields and turn provider indices into sorted lists
    out = {'vic': {}, 'nsw': {}, 'qld': {}}
    for (st, sa2), rec in by_sa2.items():
        rec['sda_filled'] = rec['sda_places'] - rec['sda_vacancies']
        rec['gh_filled']  = rec['gh_places']  - rec['gh_vacancies']
        rec['deficit']    = rec['gh_filled'] - rec['sda_vacancies']
        # Convert provider dicts to lists sorted by places desc
        rec['sda_providers'] = sorted(
            ({'name': _title_case_provider(n), **v} for n, v in rec['sda_provider_idx'].items()),
            key=lambda x: x['places'], reverse=True,
        )
        rec['gh_providers'] = sorted(
            ({'name': _title_case_provider(n), **v} for n, v in rec['gh_provider_idx'].items()),
            key=lambda x: x['places'], reverse=True,
        )
        del rec['sda_provider_idx']
        del rec['gh_provider_idx']
        out[st][sa2] = rec
    return out


def _empty_sa2_record(sa3, sa4):
    return {
        'sa3': sa3, 'sa4': sa4,
        'sda_places': 0, 'sda_vacancies': 0, 'sda_filled': 0,
        'gh_places': 0, 'gh_vacancies': 0, 'gh_filled': 0,
        'deficit': 0,
        'sda_provider_idx': {},
        'gh_provider_idx': {},
        'design_mix': {'HPS': 0, 'FA': 0, 'IL': 0, 'Multi': 0},
    }


@app.route('/api/sda-supply')
@login_required
def api_sda_supply():
    """Return the full SA2 supply snapshot.

    Shape: {'as_of': '2025-12-31', 'data': {state: {sa2: {...aggregate}}}}.
    Small enough (~400KB JSON) to ship in one request — the client caches it
    in memory and joins it to property rows on render."""
    db = get_db()
    rows = db.execute(
        'SELECT state, sa2, data_json, data_as_of FROM sda_supply'
    ).fetchall()
    db.close()
    data = {'vic': {}, 'nsw': {}, 'qld': {}}
    as_of = None
    for r in rows:
        try:
            data[r['state']][r['sa2']] = json.loads(r['data_json'])
            if r['data_as_of'] and (not as_of or r['data_as_of'] > as_of):
                as_of = r['data_as_of']
        except (json.JSONDecodeError, KeyError):
            continue
    return jsonify({'as_of': as_of, 'data': data})


UPLOAD_SUPPLY_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Upload SDA Supply Data - SDA Screener</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#f3f4f6;color:#111}
.top{background:#002060;color:#fff;padding:14px 24px;display:flex;justify-content:space-between;align-items:center}
.top h1{font-size:15px;font-weight:700}
.top a{color:#93c5fd;font-size:13px;text-decoration:none;margin-left:16px}
.wrap{max-width:900px;margin:0 auto;padding:24px}
.card{background:#fff;border-radius:8px;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:16px}
.card h2{font-size:15px;font-weight:700;color:#002060;margin-bottom:10px;padding-bottom:10px;border-bottom:2px solid #e5e7eb}
.help{font-size:12px;color:#374151;line-height:1.6;background:#f9fafb;padding:14px 18px;border-radius:6px;margin-bottom:18px;border-left:3px solid #0F6E56}
.help b{color:#0F6E56}
.field{margin-bottom:18px}
.field label{display:block;font-size:11px;color:#6B7280;font-weight:700;margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px}
.field input[type=file]{width:100%;padding:10px;border:2px dashed #d1d5db;border-radius:8px;background:#f9fafb;font-size:12px;cursor:pointer}
.field input[type=file]:hover{border-color:#0F6E56;background:#f0fdf4}
.btn{padding:12px 24px;background:#0F6E56;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;font-weight:700;width:100%}
.btn:hover{background:#0a5942}
.msg{padding:12px 16px;border-radius:6px;margin-bottom:16px;font-size:13px;line-height:1.5}
.ok{background:#dcfce7;color:#166534;border:1px solid #86efac}
.er{background:#fee2e2;color:#991b1b;border:1px solid #fca5a5}
.status-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:18px}
.status-card{border:2px solid #e5e7eb;border-radius:8px;padding:14px;text-align:center}
.status-card.loaded{border-color:#0F6E56;background:#f0fdf4}
.status-state{font-size:14px;font-weight:800;color:#002060;margin-bottom:6px}
.status-count{font-size:18px;color:#0F6E56;font-weight:700}
.status-empty{font-size:12px;color:#9CA3AF}
.status-date{font-size:10px;color:#6B7280;margin-top:6px}
.tabs{display:flex;gap:4px;margin-bottom:16px}
.tab{padding:10px 18px;border-radius:6px;font-size:13px;font-weight:600;background:#e5e7eb;color:#374151;text-decoration:none;display:inline-block}
.tab.on{background:#002060;color:#fff}
</style></head>
<body>
<div class="top">
  <h1>SDA Screener - Upload SDA Supply Data</h1>
  <div>
    <a href="/admin">Admin panel</a>
    <a href="/dashboard">Dashboard</a>
  </div>
</div>
<div class="wrap">
  <div class="tabs">
    <a href="/admin/upload_page" class="tab">Property data (CSV)</a>
    <a href="/admin/upload_sda_page" class="tab">SDA market</a>
    <a href="/admin/upload_supply_page" class="tab on">SDA supply (SA2)</a>
    <a href="/admin/upload_performl_page" class="tab">Performl (SA3)</a>
  </div>
  {{MSG_BLOCK}}
  <div class="card">
    <h2>Current data status</h2>
    <div class="status-grid">{{STATUS_GRID}}</div>
    {{AS_OF}}
  </div>
  <div class="card">
    <h2>Upload new snapshot</h2>
    <div class="help">
      Upload <b>both</b> NDIS quarterly XLSX files together. The server excludes Robust dwellings from both sides
      (since RPG only builds HPS dwellings) and computes the conversion deficit per SA2.
      Uploading replaces all existing supply data — old rows are cleared first.
      <br><br>
      <b>Source:</b> NDIS quarterly market position statements, "SA2 by provider" exports for SDA and Group Homes.
    </div>
    <form method="POST" action="/admin/upload_supply" enctype="multipart/form-data">
      <div class="field">
        <label for="sda_file">SDA file (sa2_by_provider_SDA.xlsx)</label>
        <input type="file" id="sda_file" name="sda_file" accept=".xlsx" required>
      </div>
      <div class="field">
        <label for="gh_file">Group homes file (sa2_by_provider_Group_Homes.xlsx)</label>
        <input type="file" id="gh_file" name="gh_file" accept=".xlsx" required>
      </div>
      <button class="btn" type="submit">Upload &amp; aggregate</button>
    </form>
  </div>
</div>
</body></html>"""


@app.route('/admin/upload_supply_page')
@admin_required
def upload_supply_page():
    """Render the SDA supply upload page with current data status."""
    db = get_db()
    rows = db.execute("""
        SELECT state, COUNT(*) AS sa2s, MAX(uploaded_at) AS uploaded_at,
               MAX(uploaded_by) AS uploaded_by, MAX(data_as_of) AS data_as_of
        FROM sda_supply GROUP BY state
    """).fetchall()
    db.close()
    status_by_state = {r['state']: dict(r) for r in rows}
    grid_html = ''
    for st, label in [('vic', 'VIC'), ('nsw', 'NSW'), ('qld', 'QLD')]:
        s = status_by_state.get(st)
        if s and s['sa2s']:
            grid_html += (f'<div class="status-card loaded">'
                          f'<div class="status-state">{label}</div>'
                          f'<div class="status-count">{s["sa2s"]} SA2s</div>'
                          f'<div class="status-date">uploaded {(s["uploaded_at"] or "")[:10]} by {s["uploaded_by"] or "?"}</div>'
                          f'</div>')
        else:
            grid_html += (f'<div class="status-card">'
                          f'<div class="status-state">{label}</div>'
                          f'<div class="status-empty">no data</div>'
                          f'</div>')
    overall_as_of = max(
        (r['data_as_of'] for r in rows if r['data_as_of']), default=None
    )
    as_of_html = (f'<div style="font-size:11px;color:#6B7280;text-align:center;margin-top:8px">'
                  f'Data as of {overall_as_of}</div>') if overall_as_of else ''

    msg = request.args.get('msg', '')
    msg_type = request.args.get('msg_type', 'ok')
    msg_block = f'<div class="msg {msg_type}">{msg}</div>' if msg else ''

    html = (UPLOAD_SUPPLY_HTML
            .replace('{{STATUS_GRID}}', grid_html)
            .replace('{{AS_OF}}', as_of_html)
            .replace('{{MSG_BLOCK}}', msg_block))
    return make_response(html)


@app.route('/admin/upload_supply', methods=['POST'])
@admin_required
def upload_supply():
    """Accept both NDIS XLSX files, aggregate, and replace the stored
    supply snapshot. This is an all-or-nothing replace so the dashboard
    always shows a consistent snapshot."""
    sda_file = request.files.get('sda_file')
    gh_file = request.files.get('gh_file')
    if not sda_file or not gh_file:
        return redirect('/admin/upload_supply_page?msg=Both+files+required&msg_type=er')

    sda_rows, err, sda_date = _parse_supply_xlsx(sda_file, 'sda')
    if err:
        return redirect(f'/admin/upload_supply_page?msg=SDA+file:+{quote_plus(err)}&msg_type=er')
    gh_rows, err, gh_date = _parse_supply_xlsx(gh_file, 'gh')
    if err:
        return redirect(f'/admin/upload_supply_page?msg=Group+home+file:+{quote_plus(err)}&msg_type=er')

    # Sanity check: file looks like NDIS data?
    if len(sda_rows) < 100:
        return redirect(f'/admin/upload_supply_page?msg=SDA+file+only+had+{len(sda_rows)}+rows+(expected+thousands)&msg_type=er')
    if len(gh_rows) < 50:
        return redirect(f'/admin/upload_supply_page?msg=Group+home+file+only+had+{len(gh_rows)}+rows&msg_type=er')

    aggregated = _aggregate_supply(sda_rows, gh_rows)
    data_as_of = sda_date or gh_date

    u = request.current_user
    by_user = u.get('full_name') or u.get('username') or '?'

    db = get_db()
    db.execute('DELETE FROM sda_supply')
    total_inserted = 0
    for st, sa2_map in aggregated.items():
        for sa2, rec in sa2_map.items():
            db.execute(
                """INSERT INTO sda_supply
                   (state, sa2, sa3, sa4, data_json, data_as_of, uploaded_by)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (st, sa2, rec.get('sa3', ''), rec.get('sa4', ''),
                 json.dumps(rec, separators=(',', ':')),
                 data_as_of, by_user)
            )
            total_inserted += 1
    db.commit()
    db.close()
    log_event('sda_supply_uploaded', {
        'sa2_count': total_inserted, 'data_as_of': data_as_of,
        'sda_rows': len(sda_rows), 'gh_rows': len(gh_rows),
    })
    return redirect(f'/admin/upload_supply_page?msg=Loaded+{total_inserted}+SA2s+(data+as+of+{data_as_of or "unknown"})&msg_type=ok')


# ---------------------------------------------------------------------------
# Performl SA3 market snapshot (INTERNAL ONLY)
# ---------------------------------------------------------------------------
# Source: Performl "SDA market snapshot - per region" CSV export at SA3 level.
# Used only for the on-screen Demand & supply card (HPS-house pool test).
# Never fed into partner / Supavest / full-feaso exports; the NDIS Quarterly
# Performance Report remains the cited source on anything external.

PERFORML_STATE_MAP = {
    'victoria': 'vic', 'new south wales': 'nsw', 'queensland': 'qld',
    'south australia': 'sa', 'western australia': 'wa', 'tasmania': 'tas',
    'northern territory': 'nt', 'australian capital territory': 'act',
}

# compact key -> exact Performl column header
PERFORML_NUM_COLS = {
    'need': 'SDA need',
    'need_undef': 'SDA need (undefined)',
    'need_il': 'SDA need (IL)',
    'need_fa': 'SDA need (FA)',
    'need_hps': 'SDA need (HPS)',
    'need_robust': 'SDA need (robust)',
    'in_use': 'SDA in use',
    'not_in_use': 'SDA not in use',
    'enr_new_build': 'SDA places - new build',
    'enr_nonbasic_existing': 'SDA places - non-basic existing and legacy',
    'enr_basic_existing': 'SDA places - basic existing and legacy',
    'enr_total': 'SDA places - enrolled total',
    'enr_basic': 'SDA places - enrolled basic',
    'enr_il': 'SDA places - enrolled IL',
    'enr_fa': 'SDA places - enrolled FA',
    'enr_hps': 'SDA places - enrolled HPS',
    'enr_robust': 'SDA places - enrolled robust',
    'enr_mdc': 'SDA places - enrolled MDC',
    'pipe_0_3': 'SDA places - pipeline (0 to 3 years)',
    'pipe_3_plus': 'SDA places - pipeline (over 3 years)',
    'pipe_all': 'SDA places - pipeline (ALL)',
    'pipe_il': 'SDA places - pipeline (IL)',
    'pipe_fa': 'SDA places - pipeline (FA)',
    'pipe_hps': 'SDA places - pipeline (HPS)',
    'pipe_robust': 'SDA places - pipeline (robust)',
    'pipe_mdc': 'SDA places - pipeline (MDC)',
}
PERFORML_PCT_COLS = {
    'pct_undef': 'Percent of SDA need undefined',
    'vac_new': 'New build/refurbished places - peak self-reported vacancy rate over last 12 weeks',
    'vac_existing': 'Existing and legacy places - peak self-reported vacancy rate over last 12 weeks',
}
PERFORML_REQUIRED = ['State/Territory, if applicable', 'Geographic dimension',
                     'Geographic region'] + list(PERFORML_NUM_COLS.values())


def _pf_num(v):
    v = (v or '').strip().replace(',', '')
    if not v or v.lower() in ('nan', 'n/a', '-'):
        return 0
    try:
        f = float(v)
        return int(round(f))
    except ValueError:
        return 0


def _pf_pct(v):
    """'15.56%' -> 15.56; text like 'No SDA self-reported vacancy data' -> None."""
    v = (v or '').strip().replace(',', '')
    if not v.endswith('%'):
        return None
    try:
        return round(float(v[:-1]), 2)
    except ValueError:
        return None


def _pf_date(v):
    """'June 30, 2026' -> '2026-06-30'. Returns None if unparseable."""
    v = (v or '').strip()
    for fmt in ('%B %d, %Y', '%Y-%m-%d', '%d/%m/%Y'):
        try:
            return datetime.datetime.strptime(v, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return None


def _parse_performl_csv(fileobj):
    """Returns (records, error, data_as_of, vacancy_as_of)."""
    try:
        text = fileobj.read().decode('utf-8-sig')
    except UnicodeDecodeError:
        return None, 'File is not UTF-8 CSV', None, None
    reader = csv.DictReader(io.StringIO(text))
    headers = reader.fieldnames or []
    missing = [c for c in PERFORML_REQUIRED if c not in headers]
    if missing:
        return None, 'Missing columns: ' + ', '.join(missing[:4]) + ('...' if len(missing) > 4 else ''), None, None
    records, data_as_of, vac_as_of = [], None, None
    for row in reader:
        dim = (row.get('Geographic dimension') or '')
        if 'SA3' not in dim:
            continue  # only SA3-level rows are used
        st = PERFORML_STATE_MAP.get((row.get('State/Territory, if applicable') or '').strip().lower())
        sa3 = (row.get('Geographic region') or '').strip()
        if not st or not sa3:
            continue
        rec = {k: _pf_num(row.get(col)) for k, col in PERFORML_NUM_COLS.items()}
        for k, col in PERFORML_PCT_COLS.items():
            rec[k] = _pf_pct(row.get(col))
        rec['sa3'] = sa3
        rec['sa4'] = (row.get('SA4 Region (ABS 2016), if applicable') or '').strip()
        d = _pf_date(row.get('Measurement date (demand, supply, surplus/(deficit) measures)'))
        vd = _pf_date(row.get('Measurement date (vacancy measures)'))
        if d and (not data_as_of or d > data_as_of):
            data_as_of = d
        if vd and (not vac_as_of or vd > vac_as_of):
            vac_as_of = vd
        records.append((st, rec))
    return records, None, data_as_of, vac_as_of


@app.route('/api/performl-sa3')
@login_required
def api_performl_sa3():
    """Shape: {'as_of', 'vacancy_as_of', 'data': {state: {sa3: {...}}}}.
    INTERNAL ONLY - consumed by the on-screen Demand & supply card."""
    db = get_db()
    rows = db.execute(
        'SELECT state, sa3, data_json, data_as_of, vacancy_as_of FROM performl_sa3'
    ).fetchall()
    db.close()
    data, as_of, vac_as_of = {}, None, None
    for r in rows:
        try:
            data.setdefault(r['state'], {})[r['sa3']] = json.loads(r['data_json'])
        except json.JSONDecodeError:
            continue
        if r['data_as_of'] and (not as_of or r['data_as_of'] > as_of):
            as_of = r['data_as_of']
        if r['vacancy_as_of'] and (not vac_as_of or r['vacancy_as_of'] > vac_as_of):
            vac_as_of = r['vacancy_as_of']
    return jsonify({'as_of': as_of, 'vacancy_as_of': vac_as_of, 'data': data})


UPLOAD_PERFORML_HTML = (UPLOAD_SUPPLY_HTML
    .replace('Upload SDA Supply Data - SDA Screener', 'Upload Performl Data - SDA Screener')
    .replace('SDA Screener - Upload SDA Supply Data', 'SDA Screener - Upload Performl SA3 Snapshot')
    .replace('<a href="/admin/upload_supply_page" class="tab on">SDA supply (SA2)</a>',
             '<a href="/admin/upload_supply_page" class="tab">SDA supply (SA2)</a>')
    .replace('<a href="/admin/upload_performl_page" class="tab">Performl (SA3)</a>',
             '<a href="/admin/upload_performl_page" class="tab on">Performl (SA3)</a>'))
# Swap the form/help card for the Performl one.
_pf_form_start = UPLOAD_PERFORML_HTML.index('<div class="help">')
_pf_form_end = UPLOAD_PERFORML_HTML.index('</form>') + len('</form>')
UPLOAD_PERFORML_HTML = (UPLOAD_PERFORML_HTML[:_pf_form_start] + """<div class="help">
      Upload the Performl <b>"SDA market snapshot - per region"</b> CSV export at <b>SA3</b> level
      (all states). Uploading replaces all existing Performl data. Do this quarterly when Performl refreshes.
      <br><br>
      <b>Internal only.</b> Used for the HPS-house pool test on the Demand &amp; supply card. Never shown on
      partner, investor or TIC documents.
    </div>
    <form method="POST" action="/admin/upload_performl" enctype="multipart/form-data">
      <div class="field">
        <label for="pf_file">Performl SA3 snapshot (.csv)</label>
        <input type="file" id="pf_file" name="pf_file" accept=".csv" required>
      </div>
      <button class="btn" type="submit">Upload snapshot</button>
    </form>
  </div>
  <div class="card">
    <h2>Upload provider register</h2>
    {{REG_STATUS}}
    <div class="help">
      Upload the Performl <b>"SDA provider register - SA2 level data"</b> CSV export (all states).
      Used to break competing places down by dwelling type (apartment, house, villa/townhouse) and to
      deduct group homes and legacy stock, which are closing. Replaces all existing register data.
      <br><br><b>Internal only.</b>
    </div>
    <form method="POST" action="/admin/upload_performl_register" enctype="multipart/form-data">
      <div class="field">
        <label for="reg_file">Performl provider register (.csv)</label>
        <input type="file" id="reg_file" name="reg_file" accept=".csv" required>
      </div>
      <button class="btn" type="submit">Upload provider register</button>
    </form>
  </div>
  <div class="card">
    <h2>Upload NDIA SDA price calculator</h2>
    {{PRICE_STATUS}}
    <div class="help">
      Upload the NDIA <b>SDA Price Calculator</b> .xlsx for the current financial year (once a year, when the NDIA
      publishes it). Used to estimate SDA revenue through each provider's properties on the Providers screen.
      <br><br><b>Internal only.</b>
    </div>
    <form method="POST" action="/admin/upload_sda_prices" enctype="multipart/form-data">
      <div class="field">
        <label for="price_file">NDIA SDA Price Calculator (.xlsx)</label>
        <input type="file" id="price_file" name="price_file" accept=".xlsx" required>
      </div>
      <button class="btn" type="submit">Upload price calculator</button>
    </form>""" + UPLOAD_PERFORML_HTML[_pf_form_end:])


@app.route('/admin/upload_performl_page')
@admin_required
def upload_performl_page():
    db = get_db()
    rows = db.execute("""
        SELECT state, COUNT(*) AS n, MAX(uploaded_at) AS uploaded_at,
               MAX(uploaded_by) AS uploaded_by, MAX(data_as_of) AS data_as_of,
               MAX(vacancy_as_of) AS vacancy_as_of
        FROM performl_sa3 GROUP BY state
    """).fetchall()
    db.close()
    by_state = {r['state']: dict(r) for r in rows}
    grid_html = ''
    for st, label in [('vic', 'VIC'), ('nsw', 'NSW'), ('qld', 'QLD')]:
        s = by_state.get(st)
        if s and s['n']:
            grid_html += (f'<div class="status-card loaded"><div class="status-state">{label}</div>'
                          f'<div class="status-count">{s["n"]} SA3s</div>'
                          f'<div class="status-date">uploaded {(s["uploaded_at"] or "")[:10]} by {s["uploaded_by"] or "?"}</div></div>')
        else:
            grid_html += (f'<div class="status-card"><div class="status-state">{label}</div>'
                          f'<div class="status-empty">no data</div></div>')
    other = sum(r['n'] for r in rows if r['state'] not in ('vic', 'nsw', 'qld'))
    d = max((r['data_as_of'] for r in rows if r['data_as_of']), default=None)
    vd = max((r['vacancy_as_of'] for r in rows if r['vacancy_as_of']), default=None)
    as_of_html = ''
    if d or other:
        as_of_html = (f'<div style="font-size:11px;color:#6B7280;text-align:center;margin-top:8px">'
                      f'Demand/supply as of {d or "?"} &middot; vacancy as of {vd or "?"}'
                      + (f' &middot; plus {other} SA3s in other states' if other else '') + '</div>')
    db = get_db()
    reg = db.execute('SELECT COUNT(*) AS n, MAX(data_as_of) AS d, MAX(uploaded_at) AS u FROM performl_register').fetchone()
    db.close()
    if reg and reg['n']:
        reg_html = (f'<div style="font-size:12px;color:#0F6E56;margin-bottom:12px;font-weight:700">'
                    f'Loaded: {reg["n"]} SA2s &middot; data as of {reg["d"] or "?"} &middot; uploaded {(reg["u"] or "")[:10]}</div>')
    else:
        reg_html = '<div style="font-size:12px;color:#9CA3AF;margin-bottom:12px">No provider register loaded yet.</div>'
    msg = request.args.get('msg', '')
    msg_type = request.args.get('msg_type', 'ok')
    msg_block = f'<div class="msg {msg_type}">{msg}</div>' if msg else ''
    T = _load_price_tables()
    price_html = (f'<div style="font-size:12px;color:#0F6E56;margin-bottom:12px;font-weight:700">Loaded: {T.get("year") or "price tables"} '
                  f'&middot; RRC ${T.get("rrc", 0):,.0f}/yr</div>') if T else \
                 '<div style="font-size:12px;color:#9CA3AF;margin-bottom:12px">No price calculator loaded yet.</div>'
    html = (UPLOAD_PERFORML_HTML
            .replace('{{PRICE_STATUS}}', price_html)
            .replace('{{REG_STATUS}}', reg_html)
            .replace('{{STATUS_GRID}}', grid_html)
            .replace('{{AS_OF}}', as_of_html)
            .replace('{{MSG_BLOCK}}', msg_block))
    return make_response(html)


@app.route('/admin/upload_performl', methods=['POST'])
@admin_required
def upload_performl():
    f = request.files.get('pf_file')
    if not f:
        return redirect('/admin/upload_performl_page?msg=File+required&msg_type=er')
    records, err, data_as_of, vac_as_of = _parse_performl_csv(f)
    if err:
        return redirect(f'/admin/upload_performl_page?msg={quote_plus(err)}&msg_type=er')
    if len(records) < 50:
        return redirect(f'/admin/upload_performl_page?msg=Only+{len(records)}+SA3+rows+found+(expected+~330).+Check+the+export+is+at+SA3+level.&msg_type=er')
    u = request.current_user
    by_user = u.get('full_name') or u.get('username') or '?'
    db = get_db()
    db.execute('DELETE FROM performl_sa3')
    n = 0
    for st, rec in records:
        db.execute(
            """INSERT OR REPLACE INTO performl_sa3
               (state, sa3, sa4, data_json, data_as_of, vacancy_as_of, uploaded_by)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (st, rec['sa3'], rec['sa4'], json.dumps(rec, separators=(',', ':')),
             data_as_of, vac_as_of, by_user))
        n += 1
    db.commit()
    db.close()
    log_event('performl_uploaded', {'sa3_count': n, 'data_as_of': data_as_of,
                                     'vacancy_as_of': vac_as_of})
    return redirect(f'/admin/upload_performl_page?msg=Loaded+{n}+SA3s+(demand+as+of+{data_as_of or "unknown"},+vacancy+as+of+{vac_as_of or "unknown"})&msg_type=ok')


PERFORML_REG_REQUIRED = ['State/Territory', 'Geographic dimension', 'Geographic region',
                         'Building stock', 'Design category', 'Dwelling type',
                         'Number of SDA dwellings', 'Number of SDA places',
                         'Number of SDA places self-reported vacant']


def _parse_performl_register(fileobj):
    """Returns (by_sa2, error, as_of, prov_rows).
    by_sa2: {(st, sa2): {'sa4':..., 'rows': {(dt,bs,dc): [places, vacant, dwellings]}}}
    prov_rows: list of dicts, one per register line (provider level)."""
    try:
        text = fileobj.read().decode('utf-8-sig')
    except UnicodeDecodeError:
        return None, 'File is not UTF-8 CSV', None, None
    reader = csv.DictReader(io.StringIO(text))
    headers = reader.fieldnames or []
    missing = [c for c in PERFORML_REG_REQUIRED if c not in headers]
    if missing:
        return None, 'Missing columns: ' + ', '.join(missing[:4]), None, None
    out, as_of, prov_rows = {}, None, []
    for row in reader:
        if 'SA2' not in (row.get('Geographic dimension') or ''):
            continue
        st = PERFORML_STATE_MAP.get((row.get('State/Territory') or '').strip().lower())
        sa2 = (row.get('Geographic region') or '').strip()
        if not st or not sa2:
            continue
        key = (st, sa2)
        rec = out.setdefault(key, {'sa4': (row.get('Parent region') or '').strip(), 'rows': {}})
        k2 = ((row.get('Dwelling type') or '').strip(),
              (row.get('Building stock') or '').strip(),
              (row.get('Design category') or '').strip())
        agg = rec['rows'].setdefault(k2, [0, 0, 0])
        agg[0] += _pf_num(row.get('Number of SDA places'))
        agg[1] += _pf_num(row.get('Number of SDA places self-reported vacant'))
        agg[2] += _pf_num(row.get('Number of SDA dwellings'))
        prov_rows.append({
            'state': st, 'sa2': sa2, 'sa4': rec['sa4'],
            'provider': (row.get('Provider') or '').strip() or '(unnamed provider)',
            'dt': k2[0], 'bs': k2[1], 'dc': k2[2],
            'places': _pf_num(row.get('Number of SDA places')),
            'vacant': _pf_num(row.get('Number of SDA places self-reported vacant')),
            'dwellings': _pf_num(row.get('Number of SDA dwellings')),
            'website': (row.get('Provider website') or '').strip(),
            'email': (row.get('Provider email') or '').strip(),
            'phone': (row.get('Provider phone') or '').strip(),
            'res_bed': (row.get('Resident capacity and bedroom count') or '').strip(),
            'sprinklers': (row.get('Fire sprinklers') or '').strip(),
            'ooa': (row.get('OOA room') or '').strip(),
            'breakout': (row.get('Breakout room') or '').strip(),
        })
        d = _pf_date(row.get('Date'))
        if d and (not as_of or d > as_of):
            as_of = d
    return out, None, as_of, prov_rows


@app.route('/api/performl-register')
@login_required
def api_performl_register():
    """Shape: {'as_of', 'data': {state: {sa2: [[dwelling_type, stock, category, places, vacant, dwellings], ...]}}}.
    INTERNAL ONLY."""
    db = get_db()
    rows = db.execute('SELECT state, sa2, data_json, data_as_of FROM performl_register').fetchall()
    db.close()
    data, as_of = {}, None
    for r in rows:
        try:
            data.setdefault(r['state'], {})[r['sa2']] = json.loads(r['data_json'])
        except json.JSONDecodeError:
            continue
        if r['data_as_of'] and (not as_of or r['data_as_of'] > as_of):
            as_of = r['data_as_of']
    return jsonify({'as_of': as_of, 'data': data})


# ---------------------------------------------------------------------------
# NDIA SDA price calculator -> estimated SDA revenue per register line.
# The admin uploads the NDIA "SDA Price Calculator" xlsx once a year; its
# benchmark tables, location factors and MRRC are stored in config as JSON.
# INTERNAL ONLY - estimates for the Providers screen.
# ---------------------------------------------------------------------------
PF_STATE_ABBR = {'vic': 'VIC', 'nsw': 'NSW', 'qld': 'QLD', 'sa': 'SA', 'wa': 'WA',
                 'tas': 'TAS', 'nt': 'NT', 'act': 'ACT'}
_PRICE_CAT_KEY = {'improved liveability': 'IL', 'fully accessible': 'FA', 'robust': 'R',
                  'robust with breakout room': 'RB', 'high physical support': 'HPS', 'basic': 'Basic'}


def _parse_sda_price_calculator(fileobj):
    """Returns (tables, error). tables = {'year', 'rrc', 'bench': {'new|0': {building: {col: price}}},
    'lf': {'new'|'other': {region_lower: {building_lower: factor}}}}"""
    import re as _re
    from openpyxl import load_workbook
    try:
        wb = load_workbook(fileobj, data_only=True, read_only=True)
    except Exception as e:
        return None, 'Could not open workbook: %s' % e
    if 'Benchmark Amounts' not in wb.sheetnames:
        return None, 'No "Benchmark Amounts" sheet - is this the NDIA SDA Price Calculator?'
    rows = [[c for c in r if c is not None] for r in wb['Benchmark Amounts'].iter_rows(values_only=True)]
    bench, i = {}, 0
    while i < len(rows):
        r = rows[i]
        title = str(r[0]).upper() if r else ''
        key = None
        # New builds have two GST variants; use 'input tax credits were NOT claimed',
        # the same table the screener's feaso SDA rates are built from.
        is_new = 'NEW BUILD' in title
        if title.startswith('ANNUAL') and (not is_new or 'NOT CLAIMED' in title):
            stock = 'new' if is_new else ('existing' if 'EXISTING' in title else ('legacy' if 'LEGACY' in title else None))
            spr = '0' if 'WITHOUT' in title else '1'
            if stock:
                key = stock + '|' + spr
        if key and i + 2 < len(rows):
            cats = rows[i + 1][2:]   # after 'Dwelling category', 'Number of residents'
            ooas = rows[i + 2]
            # One OOA label per category column (Basic is always 'No OOA').
            cols = []
            for oi, c in enumerate(cats):
                ck = _PRICE_CAT_KEY.get(str(c).strip().lower())
                if ck == 'Basic':
                    cols.append('Basic')
                    continue
                o = str(ooas[oi]).lower() if oi < len(ooas) else ''
                cols.append((ck or '?') + ('1' if 'with' in o else '0'))
            t, j = {}, i + 3
            while j < len(rows) and rows[j] and isinstance(rows[j][0], str) and not str(rows[j][0]).upper().startswith('ANNUAL') \
                    and rows[j][0] not in ('Existing Stock', 'Legacy Stock', 'New Builds'):
                vals = rows[j][2:]
                t[rows[j][0].strip().lower()] = {cols[k]: v for k, v in enumerate(vals) if k < len(cols) and isinstance(v, (int, float))}
                j += 1
            bench[key] = t
            i = j
            continue
        i += 1
    if not bench.get('new|1') or not bench.get('existing|1'):
        return None, 'Could not read the benchmark tables from the calculator.'
    lf = {}
    for sheet, k in (('Location Factors - New Builds', 'new'), ('Location Factors - Other', 'other')):
        if sheet not in wb.sheetnames:
            continue
        rws = [[c for c in r if c is not None] for r in wb[sheet].iter_rows(values_only=True)]
        hdr = next((r for r in rws if r and str(r[0]).lower().startswith('apartment')), None)
        if not hdr:
            continue
        hdr = [str(h).strip().lower() for h in hdr]
        d = {}
        for r in rws:
            if r and isinstance(r[0], str) and ' - ' in r[0] and len(r) > 2:
                d[r[0].strip().lower()] = {hdr[n]: v for n, v in enumerate(r[1:]) if n < len(hdr) and isinstance(v, (int, float))}
        lf[k] = d
    rrc = 0
    if 'MRRC' in wb.sheetnames:
        for r in wb['MRRC'].iter_rows(values_only=True):
            r = [c for c in r if c is not None]
            if r and str(r[0]).strip().lower() == 'per annum' and len(r) > 1:
                rrc = float(r[1])
                break
    year = None
    for r in rows[:4]:
        m = _re.search(r'(20\d\d-\d\d)', ' '.join(str(c) for c in r))
        if m:
            year = m.group(1)
            break
    if not year and 'Calculator' in wb.sheetnames:
        for r in wb['Calculator'].iter_rows(values_only=True, max_row=4):
            m = _re.search(r'(20\d\d-\d\d)', ' '.join(str(c) for c in r if c is not None))
            if m:
                year = m.group(1)
                break
    return {'year': year, 'rrc': rrc, 'bench': bench, 'lf': lf}, None


def _load_price_tables():
    db = get_db()
    row = db.execute("SELECT value FROM config WHERE key='sda_price_tables'").fetchone()
    db.close()
    if not row:
        return None
    try:
        return json.loads(row['value'])
    except (json.JSONDecodeError, TypeError):
        return None


def _calc_building(dt, res, beds, ooa):
    if dt == 'Apartment':
        if res <= 1:
            return 'apartment, 2 bedrooms, 1 resident' if (beds == 2 or (beds is None and ooa)) else 'apartment, 1 bedroom, 1 resident'
        return 'apartment, 3 bedrooms, 2 residents' if beds == 3 else 'apartment, 2 bedrooms, 2 residents'
    if dt == 'Villa duplex townhouse':
        r = min(max(res, 1), 3)
        return 'villa/duplex/townhouse, %d resident%s' % (r, '' if r == 1 else 's')
    if dt in ('House', 'Group home'):
        if res <= 1:
            return 'villa/duplex/townhouse, 1 resident'
        if res <= 3:
            return 'house, %d residents' % res
        if res <= 5:
            return 'group home, %d residents' % res
    return 'legacy stock, %d residents' % min(max(res, 6), 10)


def _price_per_place(T, state, sa4, dt, bs, dc, res_bed, sprinklers, ooa_s, breakout, places, dwellings):
    """Estimated annual SDA payment per occupied place (benchmark x location factor). 0 if unknown."""
    import re as _re
    if not T or not res_bed:
        return 0
    m = _re.match(r'Residents (\d+)(\+?), Bedrooms (\w+)', res_bed)
    if not m:
        return 0
    res = int(m.group(1))
    beds = int(m.group(3)) if m.group(3).isdigit() else None
    if m.group(2) == '+':
        res = max(6, int(round(places / max(dwellings, 1))))
    ooa = (ooa_s == 'Available')
    spr = '1' if sprinklers == 'Installed' else '0'
    stock = 'new' if bs.startswith('New build') else ('legacy' if bs == 'Legacy' else 'existing')
    b = _calc_building(dt, res, beds, ooa)
    if b.startswith('legacy'):
        stock = 'legacy'
    elif stock == 'legacy':
        stock = 'existing'
    t = (T.get('bench') or {}).get(stock + '|' + spr) or {}
    cols = t.get(b)
    if not cols:
        return 0
    ck = {'Improved liveability': 'IL', 'Fully accessible': 'FA', 'High physical support': 'HPS',
          'Robust': 'R', 'Basic': 'Basic', 'Multiple design category': 'IL'}.get(dc, 'IL')
    if ck == 'R' and breakout == 'Exists':
        ck = 'RB'
    if ck == 'Basic':
        price = cols.get('Basic') or cols.get('IL' + ('1' if ooa else '0'))
    else:
        price = cols.get(ck + ('1' if ooa else '0')) or cols.get('IL' + ('1' if ooa else '0'))
    if not price:
        return 0
    lfk = 'new' if stock == 'new' else 'other'
    region = ('%s - %s' % (PF_STATE_ABBR.get(state, state.upper()), sa4)).lower()
    lb = 'legacy stock, 6+ residents' if b.startswith('legacy') else b
    factor = (((T.get('lf') or {}).get(lfk) or {}).get(region) or {}).get(lb, 1.0)
    return round(price * factor)


@app.route('/admin/upload_sda_prices', methods=['POST'])
@admin_required
def upload_sda_prices():
    f = request.files.get('price_file')
    if not f:
        return redirect('/admin/upload_performl_page?msg=File+required&msg_type=er')
    tables, err = _parse_sda_price_calculator(f)
    if err:
        return redirect(f'/admin/upload_performl_page?msg=Price+calculator:+{quote_plus(err)}&msg_type=er')
    db = get_db()
    db.execute("INSERT OR REPLACE INTO config (key, value, updated_at) VALUES ('sda_price_tables', ?, datetime('now'))",
               (json.dumps(tables, separators=(',', ':')),))
    db.commit()
    db.close()
    log_event('sda_prices_uploaded', {'year': tables.get('year')})
    return redirect(f'/admin/upload_performl_page?msg=NDIA+SDA+price+calculator+{tables.get("year") or ""}+loaded&msg_type=ok')


@app.route('/api/performl-providers')
@login_required
def api_performl_providers():
    """Compact provider-level register. INTERNAL ONLY.
    Shape: {'as_of',
            'providers': [[name, website, email, phone], ...],
            'areas': [[state, sa2, sa4], ...],
            'types': [...], 'stocks': [...], 'cats': [...],
            'rows': [[provider_i, area_i, type_i, stock_i, cat_i, places, vacant, dwellings, sda_per_place], ...],
            'rrc': annual rent contribution per participant, 'price_year': e.g. '2026-27'}
    sda_per_place is 0 when no NDIA price calculator has been uploaded.
    Repeated strings are sent once and referenced by index to keep the payload small."""
    T = _load_price_tables()
    db = get_db()
    rows = db.execute("""SELECT state, sa2, sa4, provider, dwelling_type, building_stock,
                                design_category, places, vacant, dwellings,
                                website, email, phone, data_as_of,
                                res_bed, sprinklers, ooa, breakout
                         FROM performl_providers""").fetchall()
    db.close()
    lk = {'providers': {}, 'areas': {}, 'types': {}, 'stocks': {}, 'cats': {}}
    lists = {'providers': [], 'areas': [], 'types': [], 'stocks': [], 'cats': []}

    def ix(kind, key, value):
        d = lk[kind]
        if key not in d:
            d[key] = len(lists[kind])
            lists[kind].append(value)
        return d[key]

    out, as_of = [], None
    for r in rows:
        pi = ix('providers', r['provider'], [r['provider'], r['website'] or '', r['email'] or '', r['phone'] or ''])
        pv = lists['providers'][pi]
        for i, col in ((1, 'website'), (2, 'email'), (3, 'phone')):
            if not pv[i] and r[col]:
                pv[i] = r[col]
        ai = ix('areas', (r['state'], r['sa2']), [r['state'], r['sa2'], r['sa4'] or ''])
        ti = ix('types', r['dwelling_type'] or '', r['dwelling_type'] or '')
        si = ix('stocks', r['building_stock'] or '', r['building_stock'] or '')
        ci = ix('cats', r['design_category'] or '', r['design_category'] or '')
        ppy = _price_per_place(T, r['state'], r['sa4'] or '', r['dwelling_type'] or '', r['building_stock'] or '',
                               r['design_category'] or '', r['res_bed'] or '', r['sprinklers'] or '',
                               r['ooa'] or '', r['breakout'] or '', r['places'] or 0, r['dwellings'] or 0)
        out.append([pi, ai, ti, si, ci, r['places'] or 0, r['vacant'] or 0, r['dwellings'] or 0, ppy])
        if r['data_as_of'] and (not as_of or r['data_as_of'] > as_of):
            as_of = r['data_as_of']
    resp = {'as_of': as_of, 'rows': out,
            'rrc': (T or {}).get('rrc') or 0, 'price_year': (T or {}).get('year')}
    resp.update(lists)
    return jsonify(resp)


@app.route('/admin/upload_performl_register', methods=['POST'])
@admin_required
def upload_performl_register():
    f = request.files.get('reg_file')
    if not f:
        return redirect('/admin/upload_performl_page?msg=File+required&msg_type=er')
    by_sa2, err, as_of, prov_rows = _parse_performl_register(f)
    if err:
        return redirect(f'/admin/upload_performl_page?msg=Register:+{quote_plus(err)}&msg_type=er')
    if len(by_sa2) < 200:
        return redirect(f'/admin/upload_performl_page?msg=Register+only+had+{len(by_sa2)}+SA2s+(expected+~1,200).+Check+it+is+the+SA2-level+export.&msg_type=er')
    u = request.current_user
    by_user = u.get('full_name') or u.get('username') or '?'
    db = get_db()
    db.execute('DELETE FROM performl_register')
    n = 0
    for (st, sa2), rec in by_sa2.items():
        rows = [[k[0], k[1], k[2], v[0], v[1], v[2]] for k, v in rec['rows'].items()]
        db.execute(
            """INSERT OR REPLACE INTO performl_register
               (state, sa2, sa4, data_json, data_as_of, uploaded_by)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (st, sa2, rec['sa4'], json.dumps(rows, separators=(',', ':')), as_of, by_user))
        n += 1
    db.execute('DELETE FROM performl_providers')
    db.executemany(
        """INSERT INTO performl_providers
           (state, sa2, sa4, provider, dwelling_type, building_stock, design_category,
            places, vacant, dwellings, website, email, phone, data_as_of,
            res_bed, sprinklers, ooa, breakout)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [(r['state'], r['sa2'], r['sa4'], r['provider'], r['dt'], r['bs'], r['dc'],
          r['places'], r['vacant'], r['dwellings'], r['website'], r['email'], r['phone'], as_of,
          r['res_bed'], r['sprinklers'], r['ooa'], r['breakout'])
         for r in prov_rows])
    db.commit()
    db.close()
    log_event('performl_register_uploaded', {'sa2_count': n, 'data_as_of': as_of,
                                              'provider_rows': len(prov_rows)})
    return redirect(f'/admin/upload_performl_page?msg=Provider+register+loaded:+{n}+SA2s+(as+of+{as_of or "unknown"})&msg_type=ok')


@app.route('/admin/upload_dashboard', methods=['POST'])
@admin_required
def upload_dashboard():
    f = request.files.get('htmlfile')
    if not f: return redirect('/admin/upload_page?msg=No+file&msg_type=er')
    html = f.read().decode('utf-8')
    db = get_db()
    db.execute("INSERT INTO config (key,value) VALUES ('dashboard_html',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value,updated_at=datetime('now')", (html,))
    db.commit()
    db.close()
    return redirect('/admin/upload_page?msg=Dashboard+updated+successfully&msg_type=ok')

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
               COUNT(DISTINCT s.id) as session_count, MAX(s.login_at) as last_login,
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
    # Hidden properties — always fetch the count (for the tab badge), and the
    # full list only if we're rendering that section.
    hidden_count = db.execute('SELECT COUNT(*) FROM hidden_properties').fetchone()[0]
    hidden = []
    if section == 'hidden':
        hidden = [dict(r) for r in db.execute(
            """SELECT id, state, address, hidden_by_id, hidden_by_name,
                      hidden_at, reason
               FROM hidden_properties ORDER BY hidden_at DESC"""
        ).fetchall()]
    portfolios = []
    if section == 'earnings':
        portfolios = [dict(r) for r in db.execute(
            'SELECT p.id, p.name, p.created_by_name, p.updated_at, '
            '(SELECT COUNT(*) FROM portfolio_items i WHERE i.portfolio_id=p.id) AS n '
            'FROM portfolios p ORDER BY p.updated_at DESC, p.id DESC').fetchall()]
        names = {'2p': '2P House', '3p': '3P House', 'dp': '2P Duplex', 'd3': '3P Duplex', 'hv': '2P House + 1P Villa'}
        for p in portfolios:
            p['props'] = [dict(r, model_name=names.get(r['model'], r['model'])) for r in db.execute(
                'SELECT id, address, model, margin FROM portfolio_items WHERE portfolio_id=? ORDER BY id', (p['id'],)).fetchall()]
    db.close()
    msg = request.args.get('msg','')
    msg_type = request.args.get('msg_type','ok')
    # Check if dashboard is loaded
    dash_loaded = bool(get_dashboard_html() != '<h1>Dashboard not loaded. Upload via admin panel.</h1>')
    from jinja2 import Template as T
    return make_response(T(ADMIN_HTML).render(
        current_user=request.current_user, section=section,
        stats=stats, users=users, all_users=all_users,
        prop_views=prop_views, downloads=dl_list,
        hidden=hidden, hidden_count=hidden_count, portfolios=portfolios, std_margin=RADIUS_STD_MARGIN,
        msg=msg, msg_type=msg_type, dash_loaded=dash_loaded
    ))

@app.route('/admin/earnings/margin', methods=['POST'])
@admin_required
def admin_set_margin():
    try:
        iid = int(request.form.get('iid') or 0)
    except ValueError:
        iid = 0
    raw = (request.form.get('margin') or '').replace('$', '').replace(',', '').strip()
    margin = None
    if raw:
        try:
            margin = float(raw)
        except ValueError:
            return redirect('/admin/earnings?msg=' + quote_plus('Enter the margin as a number, e.g. 150000') + '&msg_type=er')
        if not math.isfinite(margin) or margin < 0 or margin > 5000000:
            return redirect('/admin/earnings?msg=' + quote_plus('Margin must be between $0 and $5,000,000') + '&msg_type=er')
    db = get_db()
    row = db.execute('SELECT portfolio_id, address FROM portfolio_items WHERE id=?', (iid,)).fetchone()
    if not row:
        db.close()
        return redirect('/admin/earnings?msg=' + quote_plus('Property not found') + '&msg_type=er')
    db.execute('UPDATE portfolio_items SET margin=? WHERE id=?', (margin, iid))
    _touch_portfolio(db, row['portfolio_id'])
    db.commit()
    db.close()
    log_event('portfolio_margin_set', {'item_id': iid})
    return redirect('/admin/earnings?msg=' + quote_plus('Build margin saved for ' + row['address']) + '&msg_type=ok')


@app.route('/admin/upload_page')
@admin_required
def upload_page():
    db = get_db()
    rows = db.execute('SELECT state,row_count,uploaded_at,uploaded_by FROM property_data').fetchall()
    db.close()
    status = {r['state']: dict(r) for r in rows}
    msg = request.args.get('msg','')
    msg_type = request.args.get('msg_type','ok')
    html = UPLOAD_HTML.replace('{{STATUS}}', json.dumps(status)).replace('{{MSG}}', msg).replace('{{MSG_TYPE}}', msg_type)
    return make_response(html)

@app.route('/admin/upload', methods=['POST'])
@admin_required
def upload_csv():
    state = request.form.get('state','').lower()
    if state not in ('vic','nsw','qld'): return redirect('/admin/upload_page?msg=Invalid+state&msg_type=er')
    f = request.files.get('csvfile')
    if not f: return redirect('/admin/upload_page?msg=No+file+selected&msg_type=er')
    try:
        csv_data = f.read().decode('utf-8')
        rows = len([l for l in csv_data.strip().split('\n') if l]) - 1
        db = get_db()
        db.execute("""INSERT INTO property_data (state,csv_data,row_count,uploaded_by) VALUES (?,?,?,?)
                      ON CONFLICT(state) DO UPDATE SET csv_data=excluded.csv_data,
                      row_count=excluded.row_count,uploaded_by=excluded.uploaded_by,
                      uploaded_at=datetime('now')""",
                   (state, csv_data, rows, request.current_user['username']))
        db.commit()
        db.close()
        return redirect('/admin/upload_page?msg='+state.upper()+'+uploaded+('+str(0)+'+properties)&msg_type=ok')
    except: return redirect('/admin/upload_page?msg=Upload+failed&msg_type=er')


# =============================================================================
# SDA Market Map — three layers (Radius / Existing / Permitted)
# Stores per-property pin data for the SDA market map. CSVs come from
# LandChecker exports which already have lat/lng in a 'Coordinates' column,
# so no geocoding is needed at upload time.
# =============================================================================

def _parse_landchecker_csv(csv_text):
    """Parse a LandChecker-style CSV. Returns list of dicts ready for insertion.
    Required column: Address. Coordinates column is "lng, lat" pair string."""
    import csv as _csv, io
    reader = _csv.DictReader(io.StringIO(csv_text))
    rows = []
    skipped = 0
    for raw in reader:
        # Normalise keys (case + whitespace insensitive)
        r = {(k or '').strip().lower(): (v or '').strip() for k, v in raw.items()}
        addr = r.get('address') or ''
        if not addr:
            skipped += 1
            continue
        # Coordinates are "lng, lat" e.g. "145.17783486692818, -37.976366172276954"
        lat, lng = None, None
        coords = r.get('coordinates') or ''
        if coords:
            parts = [p.strip() for p in coords.split(',')]
            if len(parts) == 2:
                try:
                    lng = float(parts[0])
                    lat = float(parts[1])
                except ValueError:
                    pass
        # Combine 3 Note fields into one searchable notes blob
        note_blob = []
        for n in ('1', '2', '3'):
            txt = r.get(f'note {n}') or ''
            author = r.get(f'note {n} author') or ''
            date = r.get(f'note {n} date') or ''
            if txt:
                if author or date:
                    note_blob.append(f'[{date} {author}] {txt}'.strip())
                else:
                    note_blob.append(txt)
        try:
            area = float(r.get('area') or 0) or None
        except ValueError:
            area = None
        try:
            frontage = float(r.get('frontage (m)') or r.get('frontage') or 0) or None
        except ValueError:
            frontage = None
        rows.append({
            'address': addr,
            'suburb': (r.get('suburb') or '').upper(),
            'state': (r.get('state') or '').lower(),
            'postcode': r.get('postcode') or '',
            'area_m2': area,
            'frontage_m': frontage,
            'planning_zones': r.get('planning zones') or '',
            'notes': '\n'.join(note_blob) if note_blob else '',
            'lat': lat,
            'lng': lng,
        })
    return rows, skipped


def _parse_radius_pipeline_csv(csv_text):
    """Parse the Radius internal pipeline CSV format (Name / Dwelling / Location).

    Format has nested sections with section headers, the column header row
    'Name,Dwelling,Location', and 'New Item' separators. We extract any row that
    has a non-empty Location, treating it as a property regardless of section.
    Returns list of dicts (without lat/lng — caller must geocode)."""
    import csv as _csv, io
    reader = _csv.reader(io.StringIO(csv_text))
    rows = []
    skipped = 0
    section = None
    for raw in reader:
        cells = [(c or '').strip() for c in raw]
        if not cells or all(c == '' for c in cells):
            continue
        # Section header (single non-empty cell, rest empty)
        if cells[0] and (len(cells) == 1 or not any(cells[1:])):
            section = cells[0]
            continue
        # Column header row — skip
        if cells[0].lower() == 'name' and len(cells) > 1 and cells[1].lower() == 'dwelling':
            continue
        # Padding row 'New Item,,'
        if cells[0].lower() == 'new item':
            continue
        # Data row: Name, Dwelling, Location
        name = cells[0]
        dwelling = cells[1] if len(cells) > 1 else ''
        location = cells[2] if len(cells) > 2 else ''
        # Need at least a location to geocode
        if not location:
            skipped += 1
            continue
        # Try to parse a state code from the location string
        state = ''
        for st in ('VIC', 'NSW', 'QLD'):
            if st in location.upper():
                state = st.lower()
                break
        # Notes: Dwelling type + section context
        notes_parts = []
        if dwelling:
            notes_parts.append('Dwelling: ' + dwelling)
        if section and section not in ('SDA Project Pipeline', 'All SDA'):
            notes_parts.append('Status: ' + section)
        rows.append({
            'address': location,             # use the cleaner Google-formatted location for geocoding
            'suburb': '',                    # filled in if geocoder returns it
            'state': state,
            'postcode': '',
            'area_m2': None,
            'frontage_m': None,
            'planning_zones': '',
            'notes': '\n'.join(notes_parts),
            'lat': None,
            'lng': None,
        })
    return rows, skipped


def _detect_csv_format(csv_text):
    """Return 'landchecker' or 'radius_pipeline' based on header inspection."""
    head = csv_text[:2000].lower()
    if 'coordinates' in head and 'planning zones' in head:
        return 'landchecker'
    if 'sda project pipeline' in head or ('name,dwelling,location' in head):
        return 'radius_pipeline'
    # Fallback: assume landchecker if it has 'address' as the first header
    return 'landchecker'


def _geocode_address(addr):
    """Server-side geocode a single address. Returns (lat, lng) or (None, None)."""
    if not addr or not GOOGLE_MAPS_API_KEY:
        return (None, None)
    try:
        url = ('https://maps.googleapis.com/maps/api/geocode/json'
               '?address=' + quote_plus(addr) + '&region=au'
               '&key=' + GOOGLE_MAPS_API_KEY)
        data = _http_get_json(url, timeout=10)
        if data.get('status') == 'OK' and data.get('results'):
            loc = data['results'][0].get('geometry', {}).get('location', {})
            if 'lat' in loc and 'lng' in loc:
                return (loc['lat'], loc['lng'])
    except Exception:
        pass
    return (None, None)


@app.route('/admin/upload_sda', methods=['POST'])
@admin_required
def upload_sda_market():
    """Upload an SDA market CSV. Accepts either:
      - LandChecker export format (has Coordinates column — no geocoding needed)
      - Radius pipeline format (Name / Dwelling / Location — geocoded server-side)
    Form fields: layer (radius|existing|permitted), state (vic|nsw|qld), csvfile"""
    layer = (request.form.get('layer') or '').lower()
    state = (request.form.get('state') or '').lower()
    if layer not in ('radius', 'existing', 'ghomes', 'permitted'):
        return redirect('/admin/upload_sda_page?msg=Invalid+layer&msg_type=er')
    if state not in ('vic', 'nsw', 'qld'):
        return redirect('/admin/upload_sda_page?msg=Invalid+state&msg_type=er')
    f = request.files.get('csvfile')
    if not f:
        return redirect('/admin/upload_sda_page?msg=No+file+selected&msg_type=er')
    try:
        csv_text = f.read().decode('utf-8-sig')
    except UnicodeDecodeError:
        try:
            csv_text = f.read().decode('latin-1')
        except Exception:
            return redirect('/admin/upload_sda_page?msg=Could+not+decode+file&msg_type=er')

    fmt = _detect_csv_format(csv_text)
    try:
        if fmt == 'radius_pipeline':
            rows, skipped = _parse_radius_pipeline_csv(csv_text)
        else:
            rows, skipped = _parse_landchecker_csv(csv_text)
    except Exception as e:
        return redirect(f'/admin/upload_sda_page?msg=Parse+error:+{e}&msg_type=er')
    if not rows:
        return redirect('/admin/upload_sda_page?msg=No+rows+parsed+(check+CSV+structure)&msg_type=er')

    # Geocode any rows that don't already have lat/lng (Radius pipeline format)
    geocode_failed = 0
    for r in rows:
        if r['lat'] is None or r['lng'] is None:
            lat, lng = _geocode_address(r['address'])
            if lat is not None:
                r['lat'] = lat
                r['lng'] = lng
            else:
                geocode_failed += 1

    db = get_db()
    # For Radius pipeline format, the CSV may span multiple states. We delete
    # all rows for this layer (across all states) and let the per-row state
    # detection determine where each pin ends up. For LandChecker format,
    # only delete the specific (layer, state) combo.
    if fmt == 'radius_pipeline':
        db.execute('DELETE FROM sda_market WHERE layer=?', (layer,))
    else:
        db.execute('DELETE FROM sda_market WHERE layer=? AND state=?', (layer, state))
    by = request.current_user['username']
    inserted = 0
    state_counts = {}
    for r in rows:
        # For Radius pipeline format, prefer the auto-detected state from each row.
        # For LandChecker, force form-selected state (handles mixed CSVs gracefully).
        row_state = r['state'] if (fmt == 'radius_pipeline' and r['state']) else state
        state_counts[row_state] = state_counts.get(row_state, 0) + 1
        db.execute("""INSERT INTO sda_market
                      (layer, state, address, suburb, postcode, area_m2, frontage_m,
                       planning_zones, notes, lat, lng, uploaded_by)
                      VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                   (layer, row_state, r['address'], r['suburb'], r['postcode'],
                    r['area_m2'], r['frontage_m'], r['planning_zones'],
                    r['notes'], r['lat'], r['lng'], by))
        inserted += 1
    db.commit()
    db.close()
    msg_parts = [f'{layer.upper()}+uploaded:+{inserted}+pins']
    if state_counts and fmt == 'radius_pipeline':
        bd = '+'.join(f'{k.upper()}:{v}' for k, v in sorted(state_counts.items()))
        msg_parts.append('split:+' + bd)
    if skipped:
        msg_parts.append(f'{skipped}+skipped')
    if geocode_failed:
        msg_parts.append(f'{geocode_failed}+failed+to+geocode')
    if fmt == 'radius_pipeline':
        msg_parts.append('(Radius+pipeline+format,+geocoded+server-side)')
    return redirect('/admin/upload_sda_page?msg=' + '+•+'.join(msg_parts) + '&msg_type=ok')


@app.route('/api/sda-market')
@login_required
def api_sda_market():
    """Return all SDA market pins.
    Query params (optional): layer, state — to filter."""
    layer = (request.args.get('layer') or '').lower()
    state = (request.args.get('state') or '').lower()
    sql = ('SELECT id, layer, state, address, suburb, postcode, area_m2, frontage_m, '
           'planning_zones, notes, lat, lng FROM sda_market WHERE lat IS NOT NULL AND lng IS NOT NULL')
    args = []
    if layer in ('radius', 'existing', 'ghomes', 'permitted'):
        sql += ' AND layer=?'
        args.append(layer)
    if state in ('vic', 'nsw', 'qld'):
        sql += ' AND state=?'
        args.append(state)
    db = get_db()
    rows = db.execute(sql, args).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/sda-market/status')
@login_required
def api_sda_market_status():
    """Return per-(layer,state) pin counts and last-upload metadata."""
    db = get_db()
    rows = db.execute("""
        SELECT layer, state, COUNT(*) AS pins, MAX(uploaded_at) AS uploaded_at,
               MAX(uploaded_by) AS uploaded_by
        FROM sda_market GROUP BY layer, state
    """).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/sda-nearby')
@login_required
def api_sda_nearby():
    """Find SDA market pins within radius_km of (lat, lng).
    Query: lat, lng, radius_km (default 5)
    Returns: { 'radius':[...], 'existing':[...], 'permitted':[...] } where
    each item has address, suburb, state, area_m2, frontage_m, planning_zones,
    notes, lat, lng, distance_km. Sorted by distance ascending."""
    try:
        lat = float(request.args.get('lat', ''))
        lng = float(request.args.get('lng', ''))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid lat/lng'}), 400
    try:
        radius_km = float(request.args.get('radius_km') or 5.0)
    except ValueError:
        radius_km = 5.0
    radius_km = max(0.1, min(50.0, radius_km))

    # Pre-filter with a bounding box to avoid running haversine on every row.
    # 1 deg latitude  ~= 111 km
    # 1 deg longitude ~= 111 km * cos(lat)
    import math
    dlat = radius_km / 111.0
    dlng = radius_km / (111.0 * max(0.001, math.cos(math.radians(lat))))
    db = get_db()
    rows = db.execute("""
        SELECT layer, state, address, suburb, postcode, area_m2, frontage_m,
               planning_zones, notes, lat, lng
        FROM sda_market
        WHERE lat IS NOT NULL AND lng IS NOT NULL
          AND lat BETWEEN ? AND ?
          AND lng BETWEEN ? AND ?
    """, (lat - dlat, lat + dlat, lng - dlng, lng + dlng)).fetchall()
    db.close()

    out = {'radius': [], 'existing': [], 'ghomes': [], 'permitted': []}
    for r in rows:
        d = _haversine_km(lat, lng, r['lat'], r['lng'])
        if d > radius_km:
            continue
        item = dict(r)
        item['distance_km'] = round(d, 2)
        layer = item['layer']
        if layer in out:
            out[layer].append(item)
    # Sort each layer by distance
    for k in out:
        out[k].sort(key=lambda x: x['distance_km'])
    return jsonify(out)


@app.route('/admin/upload_sda_page')
@admin_required
def upload_sda_page():
    """Render the SDA market upload page."""
    db = get_db()
    rows = db.execute("""
        SELECT layer, state, COUNT(*) AS pins, MAX(uploaded_at) AS uploaded_at,
               MAX(uploaded_by) AS uploaded_by
        FROM sda_market GROUP BY layer, state
    """).fetchall()
    db.close()
    status = {}
    for r in rows:
        status.setdefault(r['layer'], {})[r['state']] = {
            'pins': r['pins'],
            'uploaded_at': r['uploaded_at'],
            'uploaded_by': r['uploaded_by']
        }
    msg = request.args.get('msg', '')
    msg_type = request.args.get('msg_type', 'ok')
    html = (UPLOAD_SDA_HTML
            .replace('{{STATUS}}', json.dumps(status))
            .replace('{{MSG}}', msg)
            .replace('{{MSG_TYPE}}', msg_type))
    return make_response(html)


@app.route('/admin/users/add_form', methods=['POST'])
@admin_required
def add_user_form():
    full_name = request.form.get('full_name','').strip()
    username = request.form.get('username','').strip().lower()
    password = request.form.get('password','')
    role = request.form.get('role','team')
    if not full_name or not username or len(password) < 6:
        return redirect('/admin/users?msg=All+fields+required&msg_type=er')
    try:
        db = get_db()
        db.execute('INSERT INTO users (username,password_hash,full_name,role) VALUES (?,?,?,?)',
                   (username, generate_password_hash(password), full_name, role))
        db.commit(); db.close()
        return redirect('/admin/users?msg='+full_name+'+added&msg_type=ok')
    except sqlite3.IntegrityError:
        return redirect('/admin/users?msg=Username+exists&msg_type=er')

@app.route('/admin/users/add', methods=['POST'])
@admin_required
def add_user():
    data = request.get_json()
    try:
        db = get_db()
        db.execute('INSERT INTO users (username,password_hash,full_name,role) VALUES (?,?,?,?)',
                   (data['username'].lower(), generate_password_hash(data['password']), data['full_name'], data.get('role','team')))
        db.commit(); db.close()
        return jsonify({'ok': True})
    except: return jsonify({'error': 'Failed'}), 400

@app.route('/admin/users/<int:uid>/password', methods=['POST'])
@admin_required
def change_password(uid):
    pw = (request.get_json(silent=True) or {}).get('password') or request.form.get('password','')
    if len(pw) < 6:
        return redirect('/admin/users?msg=Password+too+short&msg_type=er') if 'json' not in (request.content_type or '') else (jsonify({'error':'Too short'}), 400)
    db = get_db()
    db.execute('UPDATE users SET password_hash=? WHERE id=?', (generate_password_hash(pw), uid))
    db.commit(); db.close()
    if 'json' in (request.content_type or ''): return jsonify({'ok': True})
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
    if 'json' in (request.content_type or ''): return jsonify({'ok': True})
    return redirect('/admin/users?msg=Updated&msg_type=ok')

@app.route('/admin/users/<int:uid>/toggle_role', methods=['POST'])
@admin_required
def toggle_role(uid):
    # Flip a user's role between 'admin' and 'team'. Two safety guards:
    #   1. Admins can't demote themselves (would lock them out of admin pages
    #      immediately on next click).
    #   2. The last remaining admin can't be demoted at all, preventing the
    #      system from ending up with zero admins.
    me = getattr(request, 'current_user', None) or {}
    if me.get('user_id') == uid:
        return redirect('/admin/users?msg=You+cannot+change+your+own+role&msg_type=er')
    db = get_db()
    user = db.execute('SELECT role,full_name FROM users WHERE id=?', (uid,)).fetchone()
    if not user:
        db.close()
        return redirect('/admin/users?msg=User+not+found&msg_type=er')
    new_role = 'team' if user['role'] == 'admin' else 'admin'
    if new_role == 'team':
        # Guard against demoting the last active admin.
        admin_count = db.execute("SELECT COUNT(*) AS c FROM users WHERE role='admin' AND active=1").fetchone()['c']
        if admin_count <= 1:
            db.close()
            return redirect('/admin/users?msg=Cannot+demote+the+last+admin&msg_type=er')
    db.execute('UPDATE users SET role=? WHERE id=?', (new_role, uid))
    db.commit(); db.close()
    msg = user['full_name'].replace(' ', '+') + '+is+now+' + new_role
    return redirect('/admin/users?msg=' + msg + '&msg_type=ok')

@app.route('/admin/api/stats')
@admin_required
def admin_stats():
    db = get_db()
    users = db.execute("""
        SELECT u.id,u.full_name,u.username,u.role,u.active,
               COUNT(DISTINCT s.id) as session_count,MAX(s.login_at) as last_login
        FROM users u LEFT JOIN sessions s ON s.user_id=u.id GROUP BY u.id
    """).fetchall()
    events = db.execute("SELECT e.*,u.full_name,u.username FROM events e JOIN users u ON e.user_id=u.id ORDER BY e.created_at DESC LIMIT 200").fetchall()
    db.close()
    return jsonify({'stats':{'total_users':0,'total_sessions':0,'total_events':0},
                    'users':[dict(u) for u in users],'events':[dict(e) for e in events]})

@app.route('/admin/api/users')
@admin_required
def admin_users_api():
    db = get_db()
    users = db.execute('SELECT id,username,full_name,role,active FROM users ORDER BY full_name').fetchall()
    db.close()
    return jsonify([dict(u) for u in users])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)



