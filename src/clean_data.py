import glob
import json
import re
from pathlib import Path


def clean_lyrics(raw_lyrics: str) -> list[str]:
  """Cleans raw song lyrics and splits them into stanzas without metadata tags."""
  if not raw_lyrics:
    return []

  # 1. Remove the standard Genius header: [Текст на песента "Title"]
  cleaned = re.sub(r"\[Текст на песента.*?\]", "", raw_lyrics)

  # 2. Remove ALL tags inside square brackets like [Предприпев], [Куплет 1], [Chorus], [Refrain], etc.
  cleaned = re.sub(r"\[.*?\]", "", cleaned)

  # 3. Split stanzas by double newlines
  stanzas = []
  raw_stanzas = cleaned.split("\n\n")

  for stanza in raw_stanzas:
    # Clean up extra spaces and newlines within each stanza
    lines = [line.strip() for line in stanza.split("\n") if line.strip()]
    if lines:
      stanza_text = " ".join(lines)
      # Filter out too short/empty lines after tag removal
      if len(stanza_text) > 15:
        stanzas.append(stanza_text)

  return stanzas


def process_all_artist_files():
  input_files = glob.glob("data/*_songs.json")
  all_training_samples = []

  print(f"📂 Found files to process: {len(input_files)}")

  for file_path in input_files:
    with open(file_path, "r", encoding="utf-8") as f:
      songs = json.load(f)

    for song in songs:
      artist = song.get("artist", "Unknown")
      title = song.get("title", "Unknown")
      raw_lyrics = song.get("lyrics", "")

      stanzas = clean_lyrics(raw_lyrics)

      for stanza in stanzas:
        all_training_samples.append(
            {"artist": artist, "title": title, "text": stanza}
        )

  # Save the cleaned dataset ready for model training/inference
  output_path = Path("data/processed_training_data.json")
  output_path.parent.mkdir(exist_ok=True)

  with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_training_samples, f, ensure_ascii=False, indent=4)

  print(
      f"✅ Successfully generated {len(all_training_samples)} clean text"
      f" blocks/stanzas!"
  )
  print(f"💾 Saved to: {output_path}")


if __name__ == "__main__":
  process_all_artist_files()