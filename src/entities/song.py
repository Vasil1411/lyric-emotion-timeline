from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from src.core.database import Base

class SongEntity(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    artist = Column(String, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    genre = Column(String, nullable=True)
    overall_profile = Column(Text, nullable=True)  # JSON string of emotions
    created_at = Column(DateTime, server_default=func.now())