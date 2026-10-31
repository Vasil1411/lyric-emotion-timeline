from fastapi import FastAPI
from src.core.database import engine, Base
from src.routers import auth, songs
from fastapi.middleware.cors import CORSMiddleware

# Automatically create database tables on startup if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lyric Emotion Timeline & Recommendation Platform",
    version="2.0.0",
    description="Clean Architecture API integrated with Machine Learning Inference & Personalization"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Register application routers
app.include_router(auth.router)
app.include_router(songs.router)

@app.get("/")
def root():
    return {"message": "Welcome to the ML Backend API! Go to /docs for Swagger UI."}