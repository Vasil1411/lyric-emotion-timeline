import sqlite3
import json
from pathlib import Path
import sys

# --- PROFESSIONAL PATH RESOLUTION ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
# -----------------------------------

from src.config import EMOTIONS

class AnalyticsService:
    def __init__(self, db_path="data/songs.db"):
        self.db_path = ROOT_DIR / db_path

    def get_artist_profile(self, artist_name: str) -> dict:
        """
        Calculates the overall aggregated emotional profile for a specific artist
        across all their ingested songs in the database.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT overall_profile FROM songs WHERE LOWER(artist) = LOWER(?)",
            (artist_name,)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print(f"⚠️ No songs found in database for artist: '{artist_name}'")
            return None

        total_songs = len(rows)
        aggregated_sums = {emo: 0.0 for emo in EMOTIONS}

        for row in rows:
            profile_json = row[0]
            if profile_json:
                profile = json.loads(profile_json)
                for emo in EMOTIONS:
                    aggregated_sums[emo] += profile.get(emo, 0.0)

        # Calculate average per emotion
        artist_profile = {
            emo: round(aggregated_sums[emo] / total_songs, 4)
            for emo in EMOTIONS
        }

        return {
            "artist": artist_name,
            "total_songs_analyzed": total_songs,
            "emotional_profile": artist_profile
        }

    def get_top_artists_by_emotion(self, emotion: str, top_n: int = 5) -> list:
        """
        Ranks all artists in the DB by their average score for a specific emotion.
        """
        if emotion not in EMOTIONS:
            raise ValueError(f"❌ Invalid emotion '{emotion}'. Must be one of {EMOTIONS}")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Retrieve all songs grouped by artist
        cursor.execute("SELECT artist, overall_profile FROM songs")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("⚠️ No songs found in the database.")
            return []

        # Aggregate per artist
        artist_scores = {}
        artist_song_counts = {}

        for artist, profile_json in rows:
            if not profile_json:
                continue
            
            profile = json.loads(profile_json)
            score = profile.get(emotion, 0.0)

            artist_scores[artist] = artist_scores.get(artist, 0.0) + score
            artist_song_counts[artist] = artist_song_counts.get(artist, 0) + 1

        # Calculate average score for the selected emotion per artist
        results = []
        for artist, total_score in artist_scores.items():
            count = artist_song_counts[artist]
            avg_score = total_score / count
            results.append({
                "artist": artist,
                "songs_count": count,
                "score": round(avg_score, 4)
            })

        # Sort descending by target emotion score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_n]


if __name__ == "__main__":
    analytics = AnalyticsService()
    
    print("\n==========================================")
    print("📊 ARTIST EMOTIONAL PROFILE DEMO")
    print("==========================================\n")
    
    # 1. Fetch artist emotional profile (e.g., Симона)
    artist_name = "Симона"
    simona_profile = analytics.get_artist_profile(artist_name)
    if simona_profile:
        print(f"🎤 Artist: {simona_profile['artist']}")
        print(f"🎵 Total Songs Analyzed: {simona_profile['total_songs_analyzed']}")
        print("🎭 Emotional Breakdown:")
        for emo, score in simona_profile["emotional_profile"].items():
            bar = "█" * int(score * 20)
            print(f"   {emo.ljust(10)}: {score * 100:5.2f}% {bar}")

    print("\n------------------------------------------")
    print("🏆 TOP ARTISTS RANKING BY EMOTION")
    print("------------------------------------------")
    
    # 2. Rank artists by specific emotion (e.g., Sadness)
    target_emotion = "Sadness"
    rankings = analytics.get_top_artists_by_emotion(target_emotion, top_n=5)
    
    print(f"\n🔝 Top Artists for Emotion '{target_emotion}':")
    for rank, item in enumerate(rankings, 1):
        print(f"  {rank}. {item['artist']} ({item['songs_count']} songs) - {item['score'] * 100:.2f}%")