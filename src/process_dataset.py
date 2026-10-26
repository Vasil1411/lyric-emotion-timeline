import csv
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.config import SAVED_MODEL_DIR

def chunk_text(text, max_chars=300):
    """Splits a long song lyric into smaller logical chunks."""
    lines = text.split("\n")
    chunks = []
    current_chunk = ""
    
    for line in lines:
        if len(current_chunk) + len(line) < max_chars:
            current_chunk += " " + line
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = line
            
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
        
    return chunks

def process_kaggle_dataset_safely(input_path, output_path, limit_songs=50, confidence_threshold=0.75):
    print(f"📂 Loading trained model for safe pseudo-labeling...")
    tokenizer = AutoTokenizer.from_pretrained(SAVED_MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(SAVED_MODEL_DIR)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    
    emotion_labels = {
        0: "Joy 😃", 1: "Sadness 😢", 2: "Anger 😡", 
        3: "Energy/Hype 🔥", 4: "Neutral/Chill 🌿"
    }
    
    print(f"📖 Reading Kaggle dataset from {input_path}...")
    new_rows = []
    skipped_count = 0
    
    with open(input_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        song_count = 0
        for row in reader:
            lyrics = row.get("Lyrics", "") or row.get("lyrics", "")
            
            if lyrics and len(lyrics) > 100:
                parts = chunk_text(lyrics)
                
                for part in parts:
                    if len(part) > 30:
                        inputs = tokenizer(part, return_tensors="pt", truncation=True, padding=True, max_length=128)
                        inputs = {k: v.to(device) for k, v in inputs.items()}
                        
                        with torch.no_grad():
                            outputs = model(**inputs)
                            probabilities = torch.softmax(outputs.logits, dim=-1)
                            pred_label = torch.argmax(probabilities, dim=-1).item()
                            confidence = probabilities[0][pred_label].item()
                        
                        # Apply Confidence Filter (Етап 2: пази само ако моделът е уверен)
                        if confidence >= confidence_threshold:
                            new_rows.append([part, pred_label])
                            # Print first few samples to visually inspect (Етап 1)
                            if len(new_rows) <= 50:
                                print(f"✅ [APPROVED] ({confidence:.2%}) -> {emotion_labels[pred_label]}: \"{part[:60]}...\"")
                        else:
                            skipped_count += 1
                
                song_count += 1
                if song_count >= limit_songs:
                    break

    print(f"\n📊 Summary: Approved {len(new_rows)} chunks, Skipped {skipped_count} uncertain chunks.")
    
    # Save approved samples to training file
    print(f"💾 Saving to {output_path}...")
    with open(output_path, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)
        
    print("✅ Stage completed successfully!")

if __name__ == "__main__":
    kaggle_csv = "data/raw/train_02.csv"
    train_csv = "data/raw/train_lyrics.csv"
    
    # Test the function with a smaller limit for safety during development
    process_kaggle_dataset_safely(kaggle_csv, train_csv, limit_songs=1000, confidence_threshold=0.75)