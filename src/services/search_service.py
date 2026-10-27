import sqlite3
import json
from pathlib import Path

class SearchService:
    def __init__(self, db_path="data/songs.db"):
        self.db_path = Path(db_path)

    def _get_connection(self):
        """Helper to create a SQLite connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def search_by_artist(self, artist_name: str):
        """Search songs by artist name (supports partial matches)."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM songs WHERE artist LIKE ?", 
            (f"%{artist_name}%",)
        )
        rows = cursor.fetchall()
        
        results = [self._enrich_song_data(row, conn) for row in rows]
        conn.close()
        return results

    def search_by_title(self, title: str):
        """Search songs by title (supports partial matches)."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM songs WHERE title LIKE ?", 
            (f"%{title}%",)
        )
        rows = cursor.fetchall()
        
        results = [self._enrich_song_data(row, conn) for row in rows]
        conn.close()
        return results

    def filter_by_genre(self, genre: str):
        """Filter songs by specific musical genre."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM songs WHERE genre LIKE ?", 
            (f"%{genre}%",)
        )
        rows = cursor.fetchall()
        
        results = [self._enrich_song_data(row, conn) for row in rows]
        conn.close()
        return results

    def _enrich_song_data(self, song_row, conn):
        """Internal helper to attach emotion timeline and profile to the song record."""
        song_id = song_row["id"]
        
        cursor = conn.cursor()
        cursor.execute(
            "SELECT stanza_index, text, emotion, confidence FROM emotion_timeline WHERE song_id = ? ORDER BY stanza_index", 
            (song_id,)
        )
        stanzas = [dict(st_row) for st_row in cursor.fetchall()]

        return {
            "id": song_id,
            "artist": song_row["artist"],
            "title": song_row["title"],
            "genre": song_row["genre"],
            "overall_profile": json.loads(song_row["overall_profile"]),
            "emotion_timeline": stanzas
        }

if __name__ == "__main__":
    # Quick test of the search service
    service = SearchService()
    
    print("🔍 Testing search by artist ('Giorgos Mazonakis'):")
    songs = service.search_by_artist("Mazonakis")
    print(f"Found {len(songs)} songs.")
    
    if songs:
        first_song = songs[0]
        print(f"🎵 Title: {first_song['title']} | Genre: {first_song['genre']}")
        print(f"📊 Overall Profile: {first_song['overall_profile']}")