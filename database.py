import sqlite3
from datetime import datetime

def log_user(user_id, username, chat_id):
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER,
                    username TEXT,
                    chat_id INTEGER,
                    timestamp TEXT
                )''')

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (
        user_id,
        username or "Unknown",
        chat_id,
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()