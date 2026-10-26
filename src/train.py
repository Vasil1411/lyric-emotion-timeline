import torch
import csv
from pathlib import Path
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from torch.optim import AdamW
from src.config import MODEL_NAME, MAX_LENGTH, BATCH_SIZE, LEARNING_RATE, EPOCHS, SAVED_MODEL_DIR
from src.model import LyricEmotionClassifier
from src.dataset import LyricDataset

def load_dataset_from_csv(file_path: str):
    """
    Load texts and labels from a CSV file located in data/raw/
    Expected CSV format: text,label
    """
    texts = []
    labels = []
    
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"❌ Dataset file not found at {file_path}. Please run generate_data.py first!")
        
    print(f"📂 Loading dataset from {file_path}...")
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row["text"])
            labels.append(int(row["label"]))
            
    print(f"✅ Loaded {len(texts)} samples successfully.")
    return texts, labels

def train_model():
    # 1. Automatically choose between GPU (CUDA) or CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🔥 Training on device: {device.type.upper()}")

    print("🚀 Initializing tokenizer and model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    # 2. Transfer the model to the GPU device
    model = LyricEmotionClassifier().to(device)

    # Load the multilingual dataset from data/raw/train_lyrics.csv
    csv_path = Path("data/raw/train_lyrics.csv")
    sample_texts, sample_labels = load_dataset_from_csv(csv_path)

    # Create Dataset and DataLoader
    dataset = LyricDataset(sample_texts, sample_labels, tokenizer, MAX_LENGTH)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    # Optimizer
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)

    total_batches = len(dataloader)
    print(f"🏋️ Starting training for {EPOCHS} epochs with {len(sample_texts)} samples ({total_batches} batches per epoch)...")
    model.train()

    for epoch in range(EPOCHS):
        total_loss = 0
        
        for step, batch in enumerate(dataloader):
            optimizer.zero_grad()

            # 3. Transfer batch data to the GPU device
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            # Forward pass
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss

            # Backward pass and optimization
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            
            # 💡 Print progress every 50 steps so you can track live training performance
            if (step + 1) % 50 == 0 or (step + 1) == total_batches:
                print(f"Epoch [{epoch+1}/{EPOCHS}] | Step [{step+1}/{total_batches}] | Loss: {loss.item():.4f}")

        avg_loss = total_loss / total_batches
        print(f"🎉 Epoch [{epoch+1}/{EPOCHS}] completed. Average Loss: {avg_loss:.4f}\n")

    # Save the fine-tuned model and tokenizer properly so inference.py can load them
    print(f"💾 Saving trained model to {SAVED_MODEL_DIR}...")
    
    try:
        if hasattr(model, "transformer"):
            model.transformer.save_pretrained(SAVED_MODEL_DIR)
        elif hasattr(model, "model"):
            model.model.save_pretrained(SAVED_MODEL_DIR)
        else:
            model.save_pretrained(SAVED_MODEL_DIR)
    except Exception as e:
        print(f"⚠️ Warning during save: {e}. Saving state_dict instead.")
        torch.save(model.state_dict(), SAVED_MODEL_DIR / "model_weights.pth")
        
    tokenizer.save_pretrained(SAVED_MODEL_DIR)
    print("✅ Training finished and model successfully saved!")

if __name__ == "__main__":
    train_model()