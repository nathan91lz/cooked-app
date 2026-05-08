import sqlite3

DB_NAME = "db.sqlite"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            location TEXT NOT NULL,
            UNIQUE(name, location)
        )
        """)

    conn.commit()
    conn.close()