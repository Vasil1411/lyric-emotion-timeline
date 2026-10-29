import os
import sys
import json
from pathlib import Path
from sqlalchemy.orm import Session

# --- PROFESSIONAL PATH RESOLUTION ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
# -----------------------------------

import lyricsgenius
from dotenv import load_dotenv
import torch

# Import existing modules and functions properly
from src.data.clean_data import clean_lyrics
from src.services.inference import load_trained_model
from src.config import EMOTIONS, MAX_LENGTH
from src.repositories.song_repository import SongRepository
from src.entities.song_timeline import SongTimelineEntity

env_path = ROOT_DIR / ".env"
load_dotenv(dotenv_path=env_path)

class IngestionService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # 1. Initialize Genius API
        genius_token = os.getenv("GENIUS_ACCESS_TOKEN")
        if not genius_token:
            raise ValueError("❌ GENIUS_ACCESS_TOKEN is missing in your .env file!")
            
        self.genius = lyricsgenius.Genius(genius_token, timeout=15, retries=3, sleep_time=1.0)
        self.genius.remove_section_headers = False
        self.genius.skip_non_songs = True
        self.genius.excluded_terms = ["Tracklist", "Album Art", "Remix", "Live"]

        print(f"🔥 IngestionService initialized on device: {self.device.type.upper()}")
        
        # 2. Load model and tokenizer
        self.tokenizer, self.model = load_trained_model(self.device)
        self.model.eval()

    def fetch_song_from_api(self, artist: str, title: str) -> str:
        """Fetches raw song lyrics from the Genius API with a robust fallback search for Cyrillic."""
        query = f"{artist} {title}"
        print(f"🔍 Searching Genius API for: {query}...")
        try:
            # 1. Direct search attempt
            song_obj = self.genius.search_song(title, artist)
            if song_obj and song_obj.lyrics:
                return song_obj.lyrics
            
            # 2. Fallback general search for Cyrillic matching issues
            print("⚠️ Direct search missed. Trying general search fallback...")
            search_results = self.genius.search(query, per_page=3)
            
            hits = search_results.get("hits", []) if isinstance(search_results, dict) else getattr(search_results, "hits", [])
            
            for hit in hits:
                result = hit.get("result") if isinstance(hit, dict) else getattr(hit, "result", None)
                if not result:
                    continue
                
                found_title = result.get("title") if isinstance(result, dict) else getattr(result, "title", None)
                
                artist_data = result.get("primary_artist") if isinstance(result, dict) else getattr(result, "primary_artist", None)
                primary_artist = None
                if isinstance(artist_data, dict):
                    primary_artist = artist_data.get("name")
                elif artist_data is not None:
                    primary_artist = getattr(artist_data, "name", None)

                if found_title and primary_artist:
                    print(f"🎯 Found match in search: {primary_artist} - {found_title}. Fetching lyrics...")
                    song_obj = self.genius.search_song(found_title, primary_artist)
                    if song_obj and song_obj.lyrics:
                        return song_obj.lyrics
                            
        except Exception as e:
            print(f"⚠️ API Error during search: {e}")
            
        return None
        
    def ingest_song(self, db: Session, artist: str, title: str, genre: str = "Pop-folk") -> int:
        """
        Full ingestion pipeline for a new song using SQLAlchemy Repository:
        1. Check if it exists in the database via SongRepository.
        2. Fetch via Genius API if missing.
        3. Clean text and split into stanzas using clean_lyrics().
        4. Run on-the-fly inference per stanza using the model.
        5. Save song and timeline via SQLAlchemy session.
        """
        repo = SongRepository(db)

        # Step 1: Check if the song already exists
        existing = repo.get_by_artist_and_title(artist, title)
        if existing:
            print(f"⚠️ Song '{title}' by {artist} already exists in database (ID: {existing.id}).")
            return existing.id

        # Step 2: Fetch from API
        raw_lyrics = self.fetch_song_from_api(artist, title)
        if not raw_lyrics:
            print(f"❌ Could not fetch or find lyrics for {artist} - {title}.")
            return None

        # Step 3: Clean using the external clean_lyrics() function
        stanzas = clean_lyrics(raw_lyrics)
        if not stanzas:
            print(f"❌ No valid stanzas found after cleaning for {artist} - {title}.")
            return None

        print(f"🎵 Analyzing {len(stanzas)} clean stanzas for {artist} - {title}...")

        stanza_results = []
        emotion_sums = {emo: 0.0 for emo in EMOTIONS}

        # Step 4: On-the-fly inference for each stanza
        for idx, stanza_text in enumerate(stanzas, 1):
            encoding = self.tokenizer(
                stanza_text,
                max_length=MAX_LENGTH,
                padding="max_length",
                truncation=True,
                return_tensors="pt"
            )

            input_ids = encoding["input_ids"].to(self.device)
            attention_mask = encoding["attention_mask"].to(self.device)

            with torch.no_grad():
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs.logits if hasattr(outputs, "logits") else outputs
                probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]

            scores = {EMOTIONS[i]: probabilities[i].item() for i in range(len(EMOTIONS))}
            
            for emo, score in scores.items():
                emotion_sums[emo] += score

            top_emotion = max(scores, key=scores.get)
            top_confidence = scores[top_emotion]

            stanza_results.append({
                "stanza_index": idx,
                "text": stanza_text,
                "emotion": top_emotion,
                "confidence": top_confidence,
                "scores": scores
            })

        num_stanzas = len(stanzas)
        overall_profile = {emo: (total / num_stanzas) for emo, total in emotion_sums.items()}

        # Step 5: Save to database using SQLAlchemy Repository & Session
        song_data = {
            "artist": artist,
            "title": title,
            "genre": genre,
            "overall_profile": json.dumps(overall_profile, ensure_ascii=False)
        }
        created_song = repo.create_song(song_data)
        song_id = created_song.id

        for stz in stanza_results:
            timeline_entry = SongTimelineEntity(
                song_id=song_id,
                stanza_index=stz["stanza_index"],
                text=stz["text"],
                emotion=stz["emotion"],
                confidence=stz["confidence"]
            )
            db.add(timeline_entry)

        db.commit()

        print(f"✅ Successfully ingested, cleaned, and analyzed song ID {song_id}: {artist} - {title}")
        return song_id

if __name__ == "__main__":
    # Test block (requires a session maker if run directly, or kept for tests)
    pass