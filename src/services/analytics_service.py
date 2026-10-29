import json
from sqlalchemy.orm import Session
from src.config import EMOTIONS
from src.repositories.song_repository import SongRepository

class AnalyticsService:
    def __init__(self):
        # Database session will now be injected via methods to match FastAPI dependency injection
        pass

    def get_artist_profile(self, db: Session, artist_name: str) -> dict:
        """
        Calculates the overall aggregated emotional profile for a specific artist
        across all their ingested songs in the database using SongRepository.
        """
        repo = SongRepository(db)
        songs = repo.get_songs_by_artist(artist_name)

        if not songs:
            print(f"⚠️ No songs found in database for artist: '{artist_name}'")
            return None

        total_songs = len(songs)
        aggregated_sums = {emo: 0.0 for emo in EMOTIONS}

        for song in songs:
            profile_json = song.overall_profile
            if profile_json:
                try:
                    profile = json.loads(profile_json)
                    for emo in EMOTIONS:
                        aggregated_sums[emo] += profile.get(emo, 0.0)
                except json.JSONDecodeError:
                    continue

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

    def get_top_artists_by_emotion(self, db: Session, emotion: str, top_n: int = 5) -> list:
        """
        Ranks all artists in the DB by their average score for a specific emotion using SongRepository.
        """
        if emotion not in EMOTIONS:
            raise ValueError(f"❌ Invalid emotion '{emotion}'. Must be one of {EMOTIONS}")

        repo = SongRepository(db)
        songs = repo.get_all_songs()

        if not songs:
            print("⚠️ No songs found in the database.")
            return []

        # Aggregate per artist
        artist_scores = {}
        artist_song_counts = {}

        for song in songs:
            if not song.overall_profile or not song.artist:
                continue
            
            try:
                profile = json.loads(song.overall_profile)
                score = profile.get(emotion, 0.0)

                artist_scores[song.artist] = artist_scores.get(song.artist, 0.0) + score
                artist_song_counts[song.artist] = artist_song_counts.get(song.artist, 0) + 1
            except json.JSONDecodeError:
                continue

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