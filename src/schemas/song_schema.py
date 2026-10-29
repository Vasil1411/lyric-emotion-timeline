from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class SongIngestRequest(BaseModel):
    artist: str
    title: str
    user_id: Optional[int] = None

class SongResponse(BaseModel):
    id: int
    artist: str
    title: str
    genre: Optional[str] = None
    overall_profile: Optional[str] = None  
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  