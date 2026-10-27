import json
from pathlib import Path

# Mapping for emotion index to name
EMOTION_MAP = {
    0: "Joy",
    1: "Sadness",
    2: "Anger",
    3: "Hype",
    4: "Nostalgia"
}

def get_genre_for_artist(artist_name: str) -> str:
    """Automatically determine genre based on artist name."""
    artist_lower = artist_name.lower()
    
    # Pop-Folk (Bulgaria)
    if any(name in artist_lower for name in ["selina", "medi", "galin", "mirela", "preslava"]):
        return "Pop-Folk"
    
    # Laika / Greek Pop
    elif any(name in artist_lower for name in ["pantelis", "argiros", "mazonakis", "vertis"]):
        return "Laika / Greek Pop"
    
    # Serbian Folk / Turbo-Folk
    elif any(name in artist_lower for name in ["saulic", "tairovic"]):
        return "Serbian Folk"
    
    # Turkish Pop
    elif "tarkan" in artist_lower:
        return "Turkish Pop"
        
    # Albanian Pop
    elif "butrint" in artist_lower:
        return "Albanian Pop"
        
    # Default
    return "Balkan / World"

def build_database():
    input_path = Path("data/processed_training_data.json")
    
    if not input_path.exists():
        print(f"❌ Error: File {input_path} not found!")
        return

    print(f"📖 Reading data from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # Dictionary to group songs by key: (artist, title)
    songs_grouped = {}

    for item in raw_data:
        artist = item.get("artist", "Unknown Artist")
        title = item.get("title", "Unknown Title")
        text = item.get("text", "")
        label_idx = item.get("label", 1)
        confidence = item.get("confidence", 0.0)

        key = (artist, title)

        if key not in songs_grouped:
            detected_genre = get_genre_for_artist(artist)
            
            songs_grouped[key] = {
                "artist": artist,
                "title": title,
                "genre": detected_genre,
                "stanzas": []
            }

        emotion_name = EMOTION_MAP.get(label_idx, "Sadness")
        
        songs_grouped[key]["stanzas"].append({
            "text": text,
            "emotion": emotion_name,
            "confidence": confidence
        })

    # Formatting into final database structure
    structured_songs = []
    
    for (artist, title), data in songs_grouped.items():
        timeline = []
        emotion_counts = {}

        for idx, stanza_info in enumerate(data["stanzas"], 1):
            timeline.append({
                "stanza_index": idx,
                "text": stanza_info["text"],
                "emotion": stanza_info["emotion"],
                "confidence": stanza_info["confidence"]
            })
            
            emo = stanza_info["emotion"]
            conf = stanza_info["confidence"]
            emotion_counts[emo] = emotion_counts.get(emo, 0) + conf

        total_conf = sum(emotion_counts.values()) if emotion_counts else 1.0
        overall_profile = {emo: round(val / total_conf, 4) for emo, val in emotion_counts.items()}

        structured_songs.append({
            "artist": artist,
            "title": title,
            "genre": data["genre"],
            "emotion_timeline": timeline,
            "overall_profile": overall_profile
        })

    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "songs_database.json"

    with open(output_path, mode="w", encoding="utf-8") as f:
        json.dump(structured_songs, f, ensure_ascii=False, indent=4)

    print(f"\n✅ Successfully generated songs database with genres!")
    print(f"📁 Saved to: {output_path}")
    print(f"📊 Total unique songs processed: {len(structured_songs)}")

if __name__ == "__main__":
    build_database()