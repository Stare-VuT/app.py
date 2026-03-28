import sqlite3
from datetime import datetime

DB_NAME = "database.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            banned INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    conn.commit()

    existing_admin = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    if not existing_admin:
        conn.execute("""
            INSERT INTO users (username, password, role, banned, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, ("admin", "123456", "admin", 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

    conn.close()


def create_user(username, password):
    conn = get_db()
    try:
        conn.execute("""
            INSERT INTO users (username, password, role, banned, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (username, password, "user", 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def get_user(username):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user


def verify_user(username, password):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()
    conn.close()
    return user
