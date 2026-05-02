#!/usr/bin/env python3
"""
SDA Screener — User Management Script
Run this to add/manage team members from command line
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

DB = os.path.join(os.path.dirname(__file__), 'usage.db')

def get_db():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db

def list_users():
    db = get_db()
    users = db.execute('SELECT id, username, full_name, role, active, created_at FROM users ORDER BY full_name').fetchall()
    db.close()
    print(f"\n{'ID':<5} {'Name':<25} {'Username':<20} {'Role':<8} {'Active':<8} {'Created'}")
    print("-" * 80)
    for u in users:
        print(f"{u['id']:<5} {u['full_name']:<25} {u['username']:<20} {u['role']:<8} {'Yes' if u['active'] else 'No':<8} {u['created_at'][:10]}")
    print()

def add_user(full_name, username, password, role='team'):
    db = get_db()
    try:
        db.execute(
            'INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)',
            (username.lower(), generate_password_hash(password), full_name, role)
        )
        db.commit()
        print(f"✓ Added: {full_name} ({username}) as {role}")
    except sqlite3.IntegrityError:
        print(f"✗ Username '{username}' already exists")
    db.close()

def change_password(username, new_password):
    db = get_db()
    result = db.execute('UPDATE users SET password_hash = ? WHERE username = ?',
                        (generate_password_hash(new_password), username.lower()))
    db.commit()
    if result.rowcount:
        print(f"✓ Password changed for {username}")
    else:
        print(f"✗ User '{username}' not found")
    db.close()

def toggle_user(username):
    db = get_db()
    user = db.execute('SELECT id, active, full_name FROM users WHERE username = ?', (username.lower(),)).fetchone()
    if not user:
        print(f"✗ User '{username}' not found")
    else:
        new_state = 1 - user['active']
        db.execute('UPDATE users SET active = ? WHERE id = ?', (new_state, user['id']))
        db.commit()
        print(f"✓ {user['full_name']} is now {'Active' if new_state else 'Disabled'}")
    db.close()

# Pre-load 13 team members — edit these before running!
TEAM_MEMBERS = [
    # (Full Name, Username, Password)
    ("Team Member 1",  "member1",  "changeMe1!"),
    ("Team Member 2",  "member2",  "changeMe2!"),
    ("Team Member 3",  "member3",  "changeMe3!"),
    ("Team Member 4",  "member4",  "changeMe4!"),
    ("Team Member 5",  "member5",  "changeMe5!"),
    ("Team Member 6",  "member6",  "changeMe6!"),
    ("Team Member 7",  "member7",  "changeMe7!"),
    ("Team Member 8",  "member8",  "changeMe8!"),
    ("Team Member 9",  "member9",  "changeMe9!"),
    ("Team Member 10", "member10", "changeMe10!"),
    ("Team Member 11", "member11", "changeMe11!"),
    ("Team Member 12", "member12", "changeMe12!"),
    ("Team Member 13", "member13", "changeMe13!"),
]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""
Usage:
  python3 manage.py list                          — list all users
  python3 manage.py add "Full Name" user pass     — add a user
  python3 manage.py password username newpass     — change password
  python3 manage.py toggle username               — enable/disable user
  python3 manage.py seed                          — add all 13 team members (edit first!)
        """)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == 'list':
        list_users()
    elif cmd == 'add' and len(sys.argv) >= 5:
        role = sys.argv[5] if len(sys.argv) > 5 else 'team'
        add_user(sys.argv[2], sys.argv[3], sys.argv[4], role)
    elif cmd == 'password' and len(sys.argv) >= 4:
        change_password(sys.argv[2], sys.argv[3])
    elif cmd == 'toggle' and len(sys.argv) >= 3:
        toggle_user(sys.argv[2])
    elif cmd == 'seed':
        print("Adding team members...")
        for name, user, pw in TEAM_MEMBERS:
            add_user(name, user, pw)
        print("\n✓ Done. Edit their names and passwords in the admin panel or rerun after editing TEAM_MEMBERS.")
    else:
        print("Unknown command. Run without args for help.")
