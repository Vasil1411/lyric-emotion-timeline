from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserCreateRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FeedbackRequest(BaseModel):
    user_id: int
    song_id: int
    interaction_type: str = "liked"
    rating: float = Field(default=1.0, ge=-1.0, le=1.0)  