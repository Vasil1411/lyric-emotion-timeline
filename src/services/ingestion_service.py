import os
import sys
import sqlite3
import json
from pathlib import Path

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

env_path = ROOT_DIR / ".env"
load_dotenv(dotenv_path=env_path)

class IngestionService:
    def __init__(self, db_path="data/songs.db"):
        self.db_path = ROOT_DIR / db_path
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
        query = f"{artist} - {title}"
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
                
                # Безопасно извличане на заглавие
                found_title = result.get("title") if isinstance(result, dict) else getattr(result, "title", None)
                
                # Безопасно извличане на името на изпълнителя
                primary_artist = None
                artist_data = result.get("primary_artist") if isinstance(result, dict) else getattr(result, "primary_artist", None)
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
        
    def ingest_song(self, artist: str, title: str, genre: str = "Pop-folk") -> int:
        """
        Full ingestion pipeline for a new song:
        1. Check if it exists in the SQLite database.
        2. Fetch via Genius API if missing (with fallback).
        3. Clean text and split into stanzas using clean_lyrics().
        4. Run on-the-fly inference per stanza using the model.
        5. Calculate overall_profile and save to SQLite.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Step 1: Check if the song already exists
        cursor.execute("SELECT id FROM songs WHERE artist = ? AND title = ?", (artist, title))
        existing = cursor.fetchone()
        if existing:
            conn.close()
            print(f"⚠️ Song '{title}' by {artist} already exists in database (ID: {existing[0]}).")
            return existing[0]
        conn.close()

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

        # Step 5: Save to SQLite database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO songs (artist, title, genre, overall_profile)
            VALUES (?, ?, ?, ?)
            """,
            (artist, title, genre, json.dumps(overall_profile, ensure_ascii=False))
        )
        song_id = cursor.lastrowid

        for stz in stanza_results:
            cursor.execute(
                """
                INSERT INTO emotion_timeline (song_id, stanza_index, text, emotion, confidence)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    song_id,
                    stz["stanza_index"],
                    stz["text"],
                    stz["emotion"],
                    stz["confidence"]
                )
            )

        conn.commit()
        conn.close()

        print(f"✅ Successfully ingested, cleaned, and analyzed song ID {song_id}: {artist} - {title}")
        return song_id

if __name__ == "__main__":
    # Test with the requested song
    service = IngestionService()
    service.ingest_song("Симона", "Прахосмукачка", "Pop-folk")