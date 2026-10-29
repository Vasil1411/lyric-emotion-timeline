from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from src.core.database import get_db
from src.core.security import get_password_hash, verify_password, create_access_token
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreateRequest, UserResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(payload: UserCreateRequest, db: Session = Depends(get_db)):
    """Register a new user in the database."""
    repo = UserRepository(db)
    existing_user = repo.get_user_by_username(payload.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered.")
        
    hashed_password = get_password_hash(payload.password)
    new_user = repo.create_user(username=payload.username, password_hash=hashed_password)
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return a JWT access token."""
    repo = UserRepository(db)
    user = repo.get_user_by_username(form_data.username)
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}