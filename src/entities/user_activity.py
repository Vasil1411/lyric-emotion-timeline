from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.core.database import Base

class UserActivityEntity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action_type = Column(String, nullable=False)
    query_payload = Column(Text, nullable=True)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())