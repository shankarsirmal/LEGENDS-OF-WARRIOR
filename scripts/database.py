import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "game_data.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            high_score INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def save_player(name, level, score):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, high_score FROM players WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        pid, high = row
        if score > high:
            cur.execute("UPDATE players SET high_score = ?, level = ? WHERE id = ?", (score, level, pid))
    else:
        cur.execute("INSERT INTO players (name, level, high_score) VALUES (?, ?, ?)", (name, level, score))
    conn.commit()
    conn.close()

def get_top_players(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name, high_score FROM players ORDER BY high_score DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
