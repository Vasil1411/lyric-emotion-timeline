import json
from sqlalchemy.orm import Session
from src.repositories.song_repository import SongRepository
from src.entities.song_timeline import SongTimelineEntity

class SearchService:
    def __init__(self):
        # Session will be injected via method parameters
        pass

    def search_by_artist(self, db: Session, artist_name: str) -> list:
        """Search songs by artist name (supports partial/case-insensitive matches using SQLAlchemy)."""
        repo = SongRepository(db)
        # Можем да разширим SongRepository или да ползваме ilike директно тук през сесията
        songs = db.query(repo.model).filter(repo.model.artist.ilike(f"%{artist_name}%")).all()
        return [self._enrich_song_data(db, song) for song in songs]

    def search_by_title(self, db: Session, title: str) -> list:
        """Search songs by title (supports partial/case-insensitive matches)."""
        repo = SongRepository(db)
        songs = db.query(repo.model).filter(repo.model.title.ilike(f"%{title}%")).all()
        return [self._enrich_song_data(db, song) for song in songs]

    def filter_by_genre(self, db: Session, genre: str) -> list:
        """Filter songs by specific musical genre."""
        repo = SongRepository(db)
        songs = db.query(repo.model).filter(repo.model.genre.ilike(f"%{genre}%")).all()
        return [self._enrich_song_data(db, song) for song in songs]

    def _enrich_song_data(self, db: Session, song_entity) -> dict:
        """Internal helper to attach emotion timeline and profile to the song record using SQLAlchemy."""
        # Fetch timeline stanzas for this song
        timeline_entries = db.query(SongTimelineEntity).filter(
            SongTimelineEntity.song_id == song_entity.id
        ).order_by(SongTimelineEntity.stanza_index).all()

        stanzas = [
            {
                "stanza_index": entry.stanza_index,
                "text": entry.text,
                "emotion": entry.emotion,
                "confidence": entry.confidence
            }
            for entry in timeline_entries
        ]

        # Parse overall_profile JSON string if present
        profile = {}
        if song_entity.overall_profile:
            try:
                profile = json.loads(song_entity.overall_profile)
            except (json.JSONDecodeError, TypeError):
                profile = {}

        return {
            "id": song_entity.id,
            "artist": song_entity.artist,
            "title": song_entity.title,
            "genre": song_entity.genre,
            "overall_profile": profile,
            "emotion_timeline": stanzas
        }