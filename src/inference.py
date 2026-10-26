import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.config import SAVED_MODEL_DIR, EMOTIONS, MAX_LENGTH, MODEL_NAME

def load_trained_model():
    """
    Load the fine-tuned model and tokenizer from SAVED_MODEL_DIR.
    Falls back to base model if fine-tuned doesn't exist.
    """
    if SAVED_MODEL_DIR.exists() and any(SAVED_MODEL_DIR.iterdir()):
        model_path = SAVED_MODEL_DIR
    else:
        model_path = MODEL_NAME

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    return tokenizer, model

def predict_emotion(text: str, tokenizer, model, device):
    """
    Analyze the emotion of a given text snippet.
    """
    encoding = tokenizer(
        text,
        max_length=MAX_LENGTH,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )

    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]

    results = {EMOTIONS[i]: probabilities[i].item() for i in range(len(EMOTIONS))}
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_results

def analyze_song_timeline(song_text: str):
    """
    Splits a song into verses/paragraphs and analyzes the emotion timeline.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🔥 Running inference on device: {device.type.upper()}")
    
    tokenizer, model = load_trained_model()
    model.to(device)
    model.eval()

    stanzas = [stanza.strip() for stanza in song_text.split("\n\n") if stanza.strip()]
    
    print("\n" + "="*60)
    print("🎵 LYRIC EMOTION TIMELINE ANALYSIS 🎵")
    print("="*60 + "\n")

    for idx, stanza in enumerate(stanzas, 1):
        print(f"--- Stanza / Verse [{idx}] ---")
        clean_stanza_text = " ".join(stanza.splitlines())
        print(f"\"{clean_stanza_text}\"\n")
        
        predictions = predict_emotion(clean_stanza_text, tokenizer, model, device)
        
        print("Emotions breakdown:")
        for emotion, score in predictions:
            bar = "█" * int(score * 20)
            print(f"  {emotion.ljust(10)}: {score * 100:5.2f}% {bar}")
        print("-" * 60 + "\n")

if __name__ == "__main__":
    song_text = """
Душата е празна, празно сърцето
Стаята — празна, всичко е празно
И друга да имам — не ми пожелавай
Боли ме, но карай, не ме съжалявай

Поне бил съм твой
И имам си спомени безброй
Поне бил съм твой

Беше есен, сърцето ми пръсна, "късаме"
Каза и тръгна
Тежка зима гледах тавана, плаках и
Пих на дивана
Цяла пролет нищо не писа, мразя те
Сърцето ми е в криза
Идва лято, жега е мръсна, връзката
Нещо прекъсна


Сега е време да си поживея, да подивея
От кеф да се размажа
Вместо да се разболея, ще си налея
По нов ще полудея
Време да си поживея, да подивея
От кеф да се размажа
Луди нощи, секс на плажа — добре ми влезна
Това, че ти изчезна
"""

    analyze_song_timeline(song_text)