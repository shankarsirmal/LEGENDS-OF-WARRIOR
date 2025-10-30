import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "game_data.db")

def init_db():
    """Initialize the database and create table if not exists."""
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
    """Insert or update player score, then keep only top 3."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check if player already exists
    cur.execute("SELECT id, high_score FROM players WHERE name = ?", (name,))
    row = cur.fetchone()

    if row:
        pid, high = row
        if score > high:
            cur.execute("UPDATE players SET high_score = ?, level = ? WHERE id = ?", (score, level, pid))
    else:
        cur.execute("INSERT INTO players (name, level, high_score) VALUES (?, ?, ?)", (name, level, score))

    # Keep only top 3 players by score
    cur.execute("SELECT id FROM players ORDER BY high_score DESC, id ASC")
    all_ids = [r[0] for r in cur.fetchall()]
    if len(all_ids) > 3:
        # Delete oldest/lower ones (FIFO style)
        to_delete = all_ids[3:]
        cur.executemany("DELETE FROM players WHERE id = ?", [(i,) for i in to_delete])

    conn.commit()
    conn.close()


def get_top_players(limit=3):
    """Fetch top 3 high-score players."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name, high_score FROM players ORDER BY high_score DESC, id ASC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
