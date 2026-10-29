import json
import math
from sqlalchemy.orm import Session
from src.config import EMOTIONS
from src.repositories.song_repository import SongRepository

class RecommendationService:
    def __init__(self):
        self.emotions = EMOTIONS

    def recommend_by_song_id(self, db: Session, song_id: int, top_n: int = 5) -> list:
        """Recommends songs similar to a given song ID based on its overall emotional profile."""
        repo = SongRepository(db)
        
        target_song = repo.get_by_id(song_id)
        if not target_song:
            raise ValueError(f"Song with ID {song_id} not found in database.")
        
        target_profile = json.loads(target_song.overall_profile) if target_song.overall_profile else {}
        
        all_songs = repo.get_all_songs()
        scored_songs = []
        
        for song in all_songs:
            if song.id == song_id:
                continue
            
            profile = json.loads(song.overall_profile) if song.overall_profile else {}
            distance = self._calculate_distance(target_profile, profile)
            
            scored_songs.append({
                "id": song.id,
                "artist": song.artist,
                "title": song.title,
                "genre": song.genre,
                "overall_profile": profile,
                "distance": distance
            })

        # Sort by distance (ascending - lower distance means higher similarity)
        scored_songs.sort(key=lambda x: x["distance"])
        return scored_songs[:top_n]

    def recommend_by_profile(self, db: Session, target_profile: dict, top_n: int = 5) -> list:
        """Recommends songs based on a custom/live emotional profile."""
        repo = SongRepository(db)
        all_songs = repo.get_all_songs()
        
        scored_songs = []
        for song in all_songs:
            profile = json.loads(song.overall_profile) if song.overall_profile else {}
            distance = self._calculate_distance(target_profile, profile)
            
            scored_songs.append({
                "id": song.id,
                "artist": song.artist,
                "title": song.title,
                "genre": song.genre,
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