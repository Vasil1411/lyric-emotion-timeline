import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AdamW
from src.config import MODEL_NAME, MAX_LENGTH, BATCH_SIZE, LEARNING_RATE, EPOCHS, SAVED_MODEL_DIR
from src.model import LyricEmotionClassifier
from src.dataset import LyricDataset

def train_model():
    print("🚀 Initializing tokenizer and model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = LyricEmotionClassifier()

    # Temporary sample dataset for testing multilingual training (Bulgarian, English, Spanish, etc.)
    sample_texts = [
        "Слънцето грее и днес съм толкова щастлив!",  # Bulgarian (Joy)
        "Чувствам се толкова сам и тъжен в тази нощ.",  # Bulgarian (Sadness)
        "Let's go, party all night, we have the energy!", # English (Hype)
        "Всичко ме дразни, омръзна ми от тези лъжи!",   # Bulgarian (Anger)
        "Спомням си старите дни и детството ни...",      # Bulgarian (Nostalgia)
        "Estoy tan feliz hoy, todo es maravilloso.",   # Spanish (Joy)
        "Me siento muy triste y con el corazón roto.", # Spanish (Sadness)
        "¡Esta fiesta está increíble, con mucha energía!" # Spanish (Hype)
    ]
    
    # Corresponding emotion labels mapped to integers (0 to 4)
    # Emotions: ["Joy", "Sadness", "Hype", "Anger", "Nostalgia"]
    sample_labels = [0, 1, 2, 3, 4, 0, 1, 2]

    # Create Dataset and DataLoader
    dataset = LyricDataset(sample_texts, sample_labels, tokenizer, MAX_LENGTH)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    # Optimizer
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)

    print(f"🏋️ Starting training for {EPOCHS} epochs...")
    model.train()

    for epoch in range(EPOCHS):
        total_loss = 0
        for batch in dataloader:
            optimizer.zero_grad()

            input_ids = batch["input_ids"]
            attention_mask = batch["attention_mask"]
            labels = batch["labels"]

            # Forward pass
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss

            # Backward pass and optimization
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch [{epoch+1}/{EPOCHS}] completed. Average Loss: {avg_loss:.4f}")

    # Save the fine-tuned model and tokenizer
    print(f"💾 Saving trained model to {SAVED_MODEL_DIR}...")
    torch.save(model.state_dict(), SAVED_MODEL_DIR / "model_weights.pth")
    tokenizer.save_pretrained(SAVED_MODEL_DIR)
    print("✅ Training finished and model successfully saved!")

if __name__ == "__main__":
    train_model()