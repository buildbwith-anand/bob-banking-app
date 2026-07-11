import os
import sqlite3
from werkzeug.security import generate_password_hash

# Resolve the absolute path to banking.db relative to this file's location.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'banking.db')


def get_db():
    """Open and return a new SQLite connection with row_factory set."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the users table if it does not exist and seed one demo account."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL,
            name     TEXT    NOT NULL,
            balance  REAL    NOT NULL DEFAULT 0.0
        )
    """)

    cursor.execute("SELECT COUNT(*) AS cnt FROM users")
    if cursor.fetchone()['cnt'] == 0:
        hashed = generate_password_hash('password123')
        cursor.execute(
            "INSERT INTO users (username, password, name, balance) VALUES (?, ?, ?, ?)",
            ('demo', hashed, 'Alex Johnson', 5000.00)
        )

    conn.commit()
    conn.close()
