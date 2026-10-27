import json
from pathlib import Path
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer
from src.config import MAX_LENGTH, SAVED_MODEL_DIR
from src.model import LyricEmotionClassifier


def auto_label_dataset(confidence_threshold: float = 0.70):
    json_path = Path("data/processed_training_data.json")

    if not json_path.exists():
        raise FileNotFoundError(f"❌ File {json_path} not found!")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🔥 Loading model on device: {device.type.upper()}...")

    tokenizer = AutoTokenizer.from_pretrained(SAVED_MODEL_DIR)
    model = LyricEmotionClassifier().to(device)

    # Explicitly load trained weights
    weights_path = SAVED_MODEL_DIR / "model_weights.pth"
    if weights_path.exists():
        print(f"📂 Loading weights from {weights_path}...")
        checkpoint = torch.load(weights_path, map_location=device)
        model.load_state_dict(checkpoint)
        print("✅ Weights loaded successfully!")
    else:
        print("⚠️ WARNING: model_weights.pth not found! Using raw model.")

    model.eval()

    with open(json_path, "r", encoding="utf-8") as f:
        samples = json.load(f)

    print(f"📂 Processing {len(samples)} stanzas...")

    labeled_count = 0
    skipped_count = 0

    with torch.no_grad():
        for i, item in enumerate(samples):
            text = item["text"]

            inputs = tokenizer(
                text,
                padding="max_length",
                truncation=True,
                max_length=MAX_LENGTH,
                return_tensors="pt",
            ).to(device)

            outputs = model(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
            )

            logits = outputs.logits if hasattr(outputs, "logits") else outputs
            probs = F.softmax(logits, dim=-1)

            max_prob, predicted_class = torch.max(probs, dim=-1)
            confidence = max_prob.item()

            # Print first 5 confidences for debugging
            if i < 5:
                print(
                    f"🔍 Sample {i+1} confidence: {confidence:.4f} (Class:"
                    f" {predicted_class.item()})"
                )

            if confidence >= confidence_threshold:
                item["label"] = predicted_class.item()
                item["confidence"] = round(confidence, 4)
                labeled_count += 1
            else:
                item["label"] = None
                item["confidence"] = round(confidence, 4)
                skipped_count += 1

    
    output_path = Path("data/auto_labeled_training_data.json") 
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=4)

    print(f"\n✅ Finished and saved to {json_path}!")
    print(f"🎯 Labeled: {labeled_count} | ⚠️ Skipped: {skipped_count}")


if __name__ == "__main__":
    auto_label_dataset(confidence_threshold=0.85)