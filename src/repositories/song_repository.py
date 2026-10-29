from sqlalchemy.orm import Session
from src.entities import SongEntity

class SongRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, song_id: int) -> SongEntity:
        return self.db.query(SongEntity).filter(SongEntity.id == song_id).first()

    def get_by_artist_and_title(self, artist: str, title: str) -> SongEntity:
        return self.db.query(SongEntity).filter(
            SongEntity.artist.ilike(artist),
            SongEntity.title.ilike(title)
        ).first()

    def get_all_songs(self):
        return self.db.query(SongEntity).all()

    def create_song(self, song_data: dict) -> SongEntity:
        song_entity = SongEntity(**song_data)
        self.db.add(song_entity)
        self.db.commit()
        self.db.refresh(song_entity)
        return song_entity