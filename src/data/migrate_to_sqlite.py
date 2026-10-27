import json
import sqlite3
from pathlib import Path

def migrate_json_to_sqlite():
    json_path = Path("data/processed/songs_database.json")
    db_path = Path("data/songs.db")
    
    if not json_path.exists():
        print(f"❌ Error: File {json_path} not found! Please run the JSON database builder script first.")
        return

    print(f"📂 Reading data from {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        songs_data = json.load(f)

    print(f"⚙️ Creating SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Create songs table (Metadata & Overall Profile)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT NOT NULL,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            overall_profile TEXT NOT NULL
        )
    ''')

    # 2. Create emotion timeline table for stanzas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotion_timeline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_id INTEGER,
            stanza_index INTEGER,
            text TEXT,
            emotion TEXT,
            confidence REAL,
            FOREIGN KEY (song_id) REFERENCES songs (id)
        )
    ''')

    # Clear old records if migrating again
    cursor.execute("DELETE FROM emotion_timeline")
    cursor.execute("DELETE FROM songs")
    conn.commit()

    print(f"🔄 Inserting records into the database...")
    inserted_songs = 0
    inserted_stanzas = 0

    for song in songs_data:
        artist = song["artist"]
        title = song["title"]
        genre = song["genre"]
        overall_profile = json.dumps(song["overall_profile"], ensure_ascii=False)

        # Insert song record
        cursor.execute('''
            INSERT INTO songs (artist, title, genre, overall_profile)
            VALUES (?, ?, ?, ?)
        ''', (artist, title, genre, overall_profile))
        
        song_id = cursor.lastrowid
        inserted_songs += 1

        # Insert song stanzas into timeline
        for stanza in song["emotion_timeline"]:
            cursor.execute('''
                INSERT INTO emotion_timeline (song_id, stanza_index, text, emotion, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                song_id,
                stanza["stanza_index"],
                stanza["text"],
                stanza["emotion"],
                stanza["confidence"]
            ))
            inserted_stanzas += 1

    conn.commit()
    conn.close()

    print(f"\n✅ Successful migration to SQLite!")
    print(f"📊 Total unique songs saved: {inserted_songs}")
    print(f"📊 Total stanzas/rows saved: {inserted_stanzas}")
    print(f"📁 Database file: {db_path}")

if __name__ == "__main__":
    migrate_json_to_sqlite()