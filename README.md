# SDA Property Screener — Team Server

## What's in this folder

| File | Purpose |
|------|---------|
| `app.py` | Main Flask server |
| `manage.py` | Command-line user management |
| `dashboard.html` | The screener dashboard (served after login) |
| `requirements.txt` | Python dependencies |
| `templates/login.html` | Login page |
| `templates/admin.html` | Admin panel |
| `usage.db` | SQLite database (created automatically) |

---

## Deployment on Railway.app (recommended — free tier available)

### Step 1 — Create a Railway account
Go to https://railway.app and sign up with GitHub.

### Step 2 — Create new project
- Click "New Project" → "Deploy from GitHub repo"
- Push this folder to a GitHub repo first (or use Railway CLI)

### Step 3 — Set environment variables in Railway
In Railway dashboard → Variables, add:
```
SECRET_KEY=your-random-secret-key-here-make-it-long
PORT=5000
```

### Step 4 — Add Procfile
Create a file called `Procfile` (no extension) in this folder:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### Step 5 — Deploy
Railway will auto-detect Python and deploy. You'll get a URL like:
`https://sda-screener-production.up.railway.app`

---

## Alternative: Run locally on your Mac

```bash
# Install dependencies (once)
pip3 install flask werkzeug gunicorn

# Start the server
python3 app.py
```
Server runs at http://localhost:5000
Admin panel at http://localhost:5000/admin

---

## Setting up team members

### Method 1 — Admin panel (recommended)
1. Go to yoursite.com/admin
2. Login as admin (default: admin / admin123)
3. Click "Manage users" tab → "+ Add team member"
4. Fill in name, username, password

### Method 2 — Command line
```bash
# List all users
python3 manage.py list

# Add a single user
python3 manage.py add "Sarah Johnson" sarah.johnson MyPassword123

# Add all 13 at once (edit TEAM_MEMBERS in manage.py first)
python3 manage.py seed

# Change a password
python3 manage.py password sarah.johnson NewPassword456

# Disable a user
python3 manage.py toggle sarah.johnson
```

---

## First login checklist

1. ✅ Go to /admin and login as `admin` / `admin123`
2. ✅ **Change the admin password immediately** (Manage users → Change PW)
3. ✅ Add all 13 team members
4. ✅ Send each team member their login URL and credentials
5. ✅ Update `dashboard.html` whenever you regenerate the CSVs

---

## Admin panel features

| Tab | What it shows |
|-----|--------------|
| Team activity | Each member's session count, last login, total time spent |
| Property views | Every property any team member clicked on, with timestamp |
| Downloads | Every CSV and Word doc downloaded, by who and for which property |
| Manage users | Add, disable, change passwords |

Click any team member's "Detail" button to see:
- Every login session with duration
- Full activity log: what they did and when

---

## Updating the dashboard

When you generate new CSVs from RP Data, update the dashboard:
1. Run `process_rp_data.py` to generate new `*_screener_ready.csv` files
2. The CSVs are still uploaded via the dashboard interface
3. Replace `dashboard.html` with the latest version

---

## Security notes

- All passwords are hashed (bcrypt via Werkzeug) — never stored in plain text
- Sessions expire when user logs out
- Admin can disable any user instantly
- Set a strong `SECRET_KEY` environment variable in production
- Use HTTPS in production (Railway provides this automatically)
