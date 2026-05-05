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
    <a href="/admin/users" class="tab {% if section=='users' %}on{% endif %}">Manage users</a>
    <a href="/admin/upload_page" class="tab" style="background:#0F6E56;color:#fff">Upload CSV data</a>
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
      <td><span class="badge {{ 'ba' if u.role=='admin' else 'bt' }}">{{ u.role }}</span></td>
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

"""SDA Property Screener - Team Server"""
from flask import Flask, request, session, redirect, url_for, jsonify, send_file, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import Template
import sqlite3, json, os, datetime, secrets, math
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
DB = os.path.join(os.path.dirname(__file__), 'usage.db')

# Google Maps Platform API key — read from environment (set on Railway).
# Used for: Geocoding, Places (New) Nearby Search, and Maps Static API.
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')

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

def get_dashboard_html():
    # Try database first, then file
    db = get_db()
    row = db.execute("SELECT value FROM config WHERE key='dashboard_html'").fetchone()
    db.close()
    if row and row['value']:
        return row['value']
    p = os.path.join(os.path.dirname(__file__), 'dashboard.html')
    if os.path.exists(p):
        with open(p) as f:
            return f.read()
    return '<h1>Dashboard not loaded. Upload via admin panel.</h1>'

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
    radius = max(50, min(radius, 50000))

    body = {
        'includedTypes': [place_type],
        'maxResultCount': 5,
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
        'X-Goog-FieldMask': 'places.displayName,places.location'
    }
    data = _http_post_json('https://places.googleapis.com/v1/places:searchNearby',
                           body, headers=headers)
    if 'error' in data:
        return jsonify({'error': data['error']}), 502
    places = data.get('places') or []
    if not places:
        return jsonify({'name': None, 'km': None})
    best = places[0]
    loc = best.get('location') or {}
    if 'latitude' not in loc or 'longitude' not in loc:
        return jsonify({'name': None, 'km': None})
    name = ((best.get('displayName') or {}).get('text')) or '—'
    km = _haversine_km(lat, lng, loc['latitude'], loc['longitude'])
    return jsonify({'name': name, 'km': round(km, 2)})

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
    return make_response(get_dashboard_html())

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
        msg=msg, msg_type=msg_type, dash_loaded=dash_loaded
    ))

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
    pw = (request.get_json() or {}).get('password') or request.form.get('password','')
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

