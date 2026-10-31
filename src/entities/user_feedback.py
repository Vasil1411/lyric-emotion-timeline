# src/entities/user_feedback.py

from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from src.core.database import Base

class UserFeedbackEntity(Base):
    __tablename__ = "user_feedback_log"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    stanza_id = Column(Integer, nullable=True)
    interaction_type = Column(String, nullable=False)
    rating = Column(Float, default=1.0)
    is_processed_for_training = Column(Boolean, default=False)
    timestamp = Column(DateTime, server_default=func.now())