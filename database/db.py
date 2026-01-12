import sqlite3

DB_PATH = "cases.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id TEXT PRIMARY KEY,
        name TEXT,
        age TEXT,
        gender TEXT,
        date DATE,
        path TEXT
    )
    """)

    conn.commit()
    conn.close()
