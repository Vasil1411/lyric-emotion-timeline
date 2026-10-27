import lyricsgenius
import json
from pathlib import Path


GENIUS_TOKEN = "WWZ09vJIIgmfJxIwko7zMrmZOaj9_SVuxrH7DASrCF3x_eYz5WpLGMacts2KxkOw"

def fetch_songs_for_artists(
    artists_list: list[str], max_songs_per_artist: int = 25
):
  """Fetches songs for a list of artists using Genius API and appends new ones to JSON files."""
  genius = lyricsgenius.Genius(
      GENIUS_TOKEN, timeout=15, retries=3, sleep_time=1.0
  )

  genius.remove_section_headers = False
  genius.skip_non_songs = True
  genius.excluded_terms = ["Tracklist", "Album Art", "Remix", "Live"]

  for artist_name in artists_list:
    print("\n" + "=" * 50)
    print(f"🎤 Processing artist: {artist_name}")
    print("=" * 50)

    file_name = f"{artist_name.lower().replace(' ', '_')}_songs.json"
    file_path = Path("data") / file_name

    # Load existing songs if file exists
    existing_titles = set()
    collected_songs = []
    if file_path.exists():
      with open(file_path, "r", encoding="utf-8") as f:
        collected_songs = json.load(f)
        existing_titles = {song["title"].lower() for song in collected_songs}
      print(
          f"📂 Loaded {len(collected_songs)} existing songs for {artist_name}."
      )

    print(
        f"🔍 Searching Genius for {artist_name} (target up to"
        f" {max_songs_per_artist} songs)..."
    )

    try:
      artist = genius.search_artist(
          artist_name, max_songs=max_songs_per_artist, sort="popularity"
      )

      if not artist or not artist.songs:
        print(f"❌ No songs found for artist: {artist_name}.")
        continue

      new_added_count = 0
      for song in artist.songs:
        if song.title.lower() not in existing_titles:
          print(f"🎵 New song found & added: {song.title}")
          collected_songs.append({
              "artist": artist.name,
              "title": song.title,
              "lyrics": song.lyrics,
          })
          existing_titles.add(song.title.lower())
          new_added_count += 1

      # Save updated list back to JSON
      file_path.parent.mkdir(exist_ok=True)
      with open(file_path, "w", encoding="utf-8") as f:
        json.dump(collected_songs, f, ensure_ascii=False, indent=4)

      print(
          f"💾 Successfully added {new_added_count} new songs for"
          f" {artist_name}! Total in file: {len(collected_songs)}"
      )

    except Exception as e:
      print(f"⚠️ An error occurred for {artist_name}: {e}")


if __name__ == "__main__":
  # List of target Balkan artists
  target_artists = [
        "Меди",
        "Галин",
        "Мирела",
        "Селина",
        "Вирго",
        
  ]

  fetch_songs_for_artists(
      artists_list=target_artists, max_songs_per_artist=25
  )