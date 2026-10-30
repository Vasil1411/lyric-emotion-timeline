from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr  
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FeedbackRequest(BaseModel):
    user_id: int
    song_id: int
    stanza_id: Optional[int] = None
    interaction_type: str = "liked"
    rating: float = Field(default=1.0, ge=-1.0, le=1.0)  