from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.repositories.song_repository import SongRepository
from src.schemas.song_schema import SongIngestRequest, SongResponse
from src.api.deps import get_current_user
from src.entities.user import UserEntity

# Import Business Logic & ML Services
from src.services.ingestion_service import IngestionService
from src.services.recommendation_service import RecommendationService
from src.services.search_service import SearchService
from src.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/songs", tags=["Songs & ML Services"])

@router.get("/", response_model=list[SongResponse])
def get_all_songs(db: Session = Depends(get_db)):
    """Retrieve a list of all songs in the database."""
    repo = SongRepository(db)
    return repo.get_all_songs()

@router.get("/{song_id}")
def get_song_by_id(song_id: int, db: Session = Depends(get_db)):
    """Retrieve details and emotion timeline for a specific song using SearchService."""
    repo = SongRepository(db)
    song = repo.get_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Delegate to SearchService to attach timeline data
    search_service = SearchService()
    return search_service._enrich_song_data(db, song)

@router.post("/ingest", response_model=SongResponse)
def ingest_song(
    payload: SongIngestRequest, 
    db: Session = Depends(get_db), 
    current_user: UserEntity = Depends(get_current_user)
):
    """
    Ingest a new song: 
    Triggers IngestionService to fetch lyrics from Genius, 
    run PyTorch model inference, and store the results.
    """
    try:
        ingestion_service = IngestionService()
        song_id = ingestion_service.ingest_song(db, payload.artist, payload.title, genre="Pop-folk")
        
        if not song_id:
            raise HTTPException(status_code=400, detail="Failed to fetch lyrics or run ML inference for this song.")
            
        repo = SongRepository(db)
        return repo.get_by_id(song_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/{song_id}")
def get_recommendations_by_song(
    song_id: int,
    top_n: int = 5,
    db: Session = Depends(get_db), 
    current_user: UserEntity = Depends(get_current_user)
):
    """
    Return song recommendations based on emotional profile similarity 
    using RecommendationService (Euclidean distance).
    """
    try:
        rec_service = RecommendationService()
        recommendations = rec_service.recommend_by_song_id(db, song_id, top_n=top_n)
        
        return {
            "user": current_user.username,
            "target_song_id": song_id,
            "recommended_songs": recommendations
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/analytics/artist/{artist_name}")
def get_artist_emotional_profile(
    artist_name: str,
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):
    """Get aggregated emotional profile for an artist using AnalyticsService."""
    analytics_service = AnalyticsService()
    profile = analytics_service.get_artist_profile(db, artist_name)
    if not profile:
        raise HTTPException(status_code=404, detail=f"No data found for artist: {artist_name}")
    return profile