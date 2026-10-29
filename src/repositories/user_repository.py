from sqlalchemy.orm import Session
from src.entities.user import UserEntity
from src.entities.user_feedback import UserFeedbackEntity
from src.entities.user_activity import UserActivityEntity
from src.entities.song import SongEntity

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.id == user_id).first()

    def get_user_by_username(self, username: str) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.username == username).first()

    def create_user(self, username: str, password_hash: str) -> UserEntity:
        user = UserEntity(username=username, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def log_feedback(self, user_id: int, song_id: int, interaction_type: str, rating: float = 1.0):
        feedback = UserFeedbackEntity(
            user_id=user_id,
            song_id=song_id,
            interaction_type=interaction_type,
            rating=rating,
            is_processed_for_training=False
        )
        self.db.add(feedback)
        self.db.commit()
        return feedback

    def count_unprocessed_feedback(self, user_id: int) -> int:
        return self.db.query(UserFeedbackEntity).filter(
            UserFeedbackEntity.user_id == user_id,
            UserFeedbackEntity.is_processed_for_training == False,
            UserFeedbackEntity.rating > 0
        ).count()

    def mark_feedback_as_processed(self, user_id: int):
        self.db.query(UserFeedbackEntity).filter(
            UserFeedbackEntity.user_id == user_id,
            UserFeedbackEntity.is_processed_for_training == False,
            UserFeedbackEntity.rating > 0
        ).update({"is_processed_for_training": True})
        self.db.commit()

    def log_activity(self, user_id: int, action_type: str, query_payload: str = None, song_id: int = None):
        activity = UserActivityEntity(
            user_id=user_id,
            action_type=action_type,
            query_payload=query_payload,
            song_id=song_id
        )
        self.db.add(activity)
        self.db.commit()
        return activity

    def get_unprocessed_feedback_stanzas(self, user_id: int):
        """Fetches lyric stanzas or song data from songs that the user positively interacted with, for fine-tuning."""
        results = self.db.query(UserFeedbackEntity, SongEntity).join(
            SongEntity, UserFeedbackEntity.song_id == SongEntity.id
        ).filter(
            UserFeedbackEntity.user_id == user_id,
            UserFeedbackEntity.is_processed_for_training == False,
            UserFeedbackEntity.rating > 0
        ).all()
        return results