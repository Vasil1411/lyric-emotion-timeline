import sqlite3
import json
from pathlib import Path
import math

class RecommendationService:
    def __init__(self, db_path="data/songs.db"):
        self.db_path = Path(db_path)
        self.emotions = ['Joy', 'Sadness', 'Anger', 'Hype', 'Nostalgia']

    def _get_connection(self):
        """Helper to create a SQLite connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def recommend_by_song_id(self, song_id: int, top_n: int = 5):
        """Recommends songs similar to a given song ID based on its overall emotional profile."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get target song
        cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
        target_row = cursor.fetchone()
        if not target_row:
            conn.close()
            raise ValueError(f"Song with ID {song_id} not found in database.")
        
        target_profile = json.loads(target_row["overall_profile"])
        
        # Get all other songs
        cursor.execute("SELECT * FROM songs WHERE id != ?", (song_id,))
        all_rows = cursor.fetchall()
        conn.close()

        scored_songs = []
        for row in all_rows:
            profile = json.loads(row["overall_profile"])
            # Calculate distance across emotion vectors (lower distance = higher similarity)
            distance = self._calculate_distance(target_profile, profile)
            scored_songs.append({
                "id": row["id"],
                "artist": row["artist"],
                "title": row["title"],
                "genre": row["genre"],
                "overall_profile": profile,
                "distance": distance
            })

        # Sort by distance (ascending)
        scored_songs.sort(key=lambda x: x["distance"])
        return scored_songs[:top_n]

    def recommend_by_profile(self, target_profile: dict, top_n: int = 5):
        """Recommends songs based on a custom/live emotional profile (e.g. from a new song)."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM songs")
        all_rows = cursor.fetchall()
        conn.close()

        scored_songs = []
        for row in all_rows:
            profile = json.loads(row["overall_profile"])
            distance = self._calculate_distance(target_profile, profile)
            scored_songs.append({
                "id": row["id"],
                "artist": row["artist"],
                "title": row["title"],
                "genre": row["genre"],
                "overall_profile": profile,
                "distance": distance
            })

        scored_songs.sort(key=lambda x: x["distance"])
        return scored_songs[:top_n]

    def _calculate_distance(self, p1: dict, p2: dict) -> float:
        """Calculates Euclidean distance between two emotion profiles across 5 dimensions."""
        sum_sq = 0.0
        for emotion in self.emotions:
            v1 = p1.get(emotion, 0.0)
            v2 = p2.get(emotion, 0.0)
            sum_sq += (v1 - v2) ** 2
        return math.sqrt(sum_sq)

if __name__ == "__main__":
    # Quick test of the recommendation service
    rec_service = RecommendationService()
    
    print("🎵 Testing recommendations based on Song ID 1:")
    try:
        recommendations = rec_service.recommend_by_song_id(1, top_n=3)
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['artist']} - {rec['title']} ({rec['genre']}) [Distance: {rec['distance']:.4f}]")
            print(f"   Profile: {rec['overall_profile']}")
    except Exception as e:
        print(f"❌ Error: {e}")