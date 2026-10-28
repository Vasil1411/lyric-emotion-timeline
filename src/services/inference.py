import torch
from pathlib import Path
from transformers import AutoTokenizer
from src.config import SAVED_MODEL_DIR, EMOTIONS, MAX_LENGTH, MODEL_NAME
from src.models.model import LyricEmotionClassifier  

def load_trained_model(device):
    """
    Loads your fine-tuned LyricEmotionClassifier with the correct 5 classes.
    """
    model_path = SAVED_MODEL_DIR if (SAVED_MODEL_DIR.exists() and any(SAVED_MODEL_DIR.iterdir())) else MODEL_NAME
    
    print(f"📂 Loading tokenizer and model from: {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    # 1. Инициализираме модела
    model = LyricEmotionClassifier()
    
    # 2. ПРЕХВЪРЛЯМЕ ГО НА УСТРОЙСТВОТО (GPU/CUDA) ПРЕДИ ДА ЗАРЕДИМ ТЕЖЕСТИТЕ!
    model.to(device)
    
    # 3. Load trained model weights
    weights_path = SAVED_MODEL_DIR / "model_weights.pth"
    if weights_path.exists():
        print(f"🔗 Loading fine-tuned weights from {weights_path}")
        model.load_state_dict(torch.load(weights_path, map_location=device))
    else:
        print("⚠️ Warning: No fine-tuned weights found, using base model weights!")
        
    return tokenizer, model

def analyze_song_timeline(song_text: str):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🔥 Running inference on device: {device.type.upper()}")
    
    tokenizer, model = load_trained_model(device)
    model.eval()

    # Split song into stanzas
    stanzas = [stanza.strip() for stanza in song_text.split("\n\n") if stanza.strip()]
    
    print("\n" + "="*60)
    print("🎵 LYRIC EMOTION TIMELINE ANALYSIS 🎵")
    print("="*60 + "\n")

    for idx, stanza in enumerate(stanzas, 1):
        print(f"--- Stanza / Verse [{idx}] ---")
        clean_stanza_text = " ".join(stanza.splitlines())
        print(f"\"{clean_stanza_text}\"\n")
        
        # Tokenization & Inference
        encoding = tokenizer(
            clean_stanza_text,
            max_length=MAX_LENGTH,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        input_ids = encoding["input_ids"].to(device)
        attention_mask = encoding["attention_mask"].to(device)

        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits if hasattr(outputs, "logits") else outputs
            probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]

        results = {EMOTIONS[i]: probabilities[i].item() for i in range(len(EMOTIONS))}
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        
        print("Emotions breakdown:")
        for emotion, score in sorted_results:
            bar = "█" * int(score * 20)
            print(f"  {emotion.ljust(10)}: {score * 100:5.2f}% {bar}")
        print("-" * 60 + "\n")

if __name__ == "__main__":
    # Test sample text
    song_text = """
    First stanza or verse text goes here for testing...
    
    Second stanza or chorus text goes here...
    """

    analyze_song_timeline(song_text)