from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.core.database import Base

class SongTimelineEntity(Base):
    __tablename__ = "emotion_timeline"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    stanza_index = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    emotion = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)