import sqlite3
from pathlib import Path
import sys

# --- PROFESSIONAL PATH RESOLUTION ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
# -----------------------------------

def init_user_tables(db_path="data/songs.db"):
    full_path = ROOT_DIR / db_path
    print(f"📂 Connecting to database at: {full_path}")
    
    conn = sqlite3.connect(full_path)
    cursor = conn.cursor()

    # 1. Users table (Потребители)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. User activity history (История на търсения, анализи и заявки)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action_type TEXT NOT NULL, --  'SEARCH', 'ANALYZE', 'RECOMMEND'
        query_payload TEXT,        -- JSON string of the query or parameters
        song_id INTEGER,           -- Optional reference to a song if the action is related to a specific song
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(song_id) REFERENCES songs(id)
    )
    """)

    # 3. User preferences / feedback 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_preferences (
        user_id INTEGER,
        song_id INTEGER,
        rating REAL DEFAULT 1.0,   -- 1.0 за харесано, -1.0 за нехаресано
        interaction_type TEXT,     -- 'liked', 'saved', 'queried'
        PRIMARY KEY(user_id, song_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(song_id) REFERENCES songs(id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Successfully initialized user management and tracking tables in songs.db!")

if __name__ == "__main__":
    init_user_tables()