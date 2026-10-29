import torch
from pathlib import Path
from transformers import AutoTokenizer
from src.config import SAVED_MODEL_DIR, EMOTIONS, MAX_LENGTH, MODEL_NAME
from src.models.model import LyricEmotionClassifier  

def load_trained_model(device):
    """
    Loads your fine-tuned LyricEmotionClassifier with the correct classes.
    """
    model_path = SAVED_MODEL_DIR if (SAVED_MODEL_DIR.exists() and any(SAVED_MODEL_DIR.iterdir())) else MODEL_NAME
    
    print(f"📂 Loading tokenizer and model from: {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    # 1. Initialize model
    model = LyricEmotionClassifier()
    
    # 2. Move to device (GPU/CUDA) before loading weights
    model.to(device)
    
    # 3. Load trained model weights
    weights_path = SAVED_MODEL_DIR / "model_weights.pth"
    if weights_path.exists():
        print(f"🔗 Loading fine-tuned weights from {weights_path}")
        model.load_state_dict(torch.load(weights_path, map_location=device))
    else:
        print("⚠️ Warning: No fine-tuned weights found, using base model weights!")
        
    return tokenizer, model

def analyze_song_timeline(song_text: str) -> list:
    """
    Analyzes the song stanza by stanza and returns a structured timeline of emotions 
    suitable for database storage and API responses.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🔥 Running inference on device: {device.type.upper()}")
    
    tokenizer, model = load_trained_model(device)
    model.eval()

    # Split song into stanzas
    stanzas = [stanza.strip() for stanza in song_text.split("\n\n") if stanza.strip()]
    timeline_results = []

    for idx, stanza in enumerate(stanzas, 1):
        clean_stanza_text = " ".join(stanza.splitlines())
        
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

        emotions_dict = {EMOTIONS[i]: probabilities[i].item() for i in range(len(EMOTIONS))}
        
        # Append stanza analysis to timeline
        timeline_results.append({
            "stanza_index": idx,
            "stanza_text": clean_stanza_text,
            "emotions": emotions_dict
        })

    return timeline_results

if __name__ == "__main__":
    # Test sample text when run directly
    song_text = """
    First stanza or verse text goes here for testing...
    
    Second stanza or chorus text goes here...
    """
    results = analyze_song_timeline(song_text)
    print("Inference results test:", results)