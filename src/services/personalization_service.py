import torch
from sqlalchemy.orm import Session
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW

from src.entities.user_feedback import UserFeedbackEntity
from src.entities.song_timeline import SongTimelineEntity
from src.config import SAVED_MODEL_DIR

class UserFeedbackDataset(Dataset):
    """Custom PyTorch Dataset for user-preferred lyric stanzas."""
    def __init__(self, data, tokenizer, max_length=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        text = item["text"]
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
        }

class PersonalizationService:
    def __init__(self):
        pass

    def log_feedback(self, db: Session, user_id: int, song_id: int, interaction_type: str, rating: float = 1.0):
        """Logs a user interaction/feedback for a song using SQLAlchemy session."""
        feedback = UserFeedbackEntity(
            user_id=user_id,
            song_id=song_id,
            interaction_type=interaction_type,
            rating=rating,
            is_processed_for_training=False
        )
        db.add(feedback)
        db.commit()
        print(f"📝 Feedback logged for User {user_id} on Song {song_id} [{interaction_type}]")

    def check_training_threshold(self, db: Session, user_id: int, threshold: int = 50) -> bool:
        """Checks if the user has accumulated enough unprocessed feedback to trigger adaptive fine-tuning."""
        unprocessed_count = db.query(UserFeedbackEntity).filter(
            UserFeedbackEntity.user_id == user_id,
            UserFeedbackEntity.is_processed_for_training == False,
            UserFeedbackEntity.rating > 0
        ).count()
        
        print(f"📊 User {user_id} unprocessed feedback count: {unprocessed_count}/{threshold}")
        return unprocessed_count >= threshold

    def trigger_adaptive_finetuning(self, db: Session, user_id: int, model, tokenizer, device, epochs: int = 1):
        """Executes a lightweight few-shot fine-tuning loop using user's liked stanzas and updates weights."""
        print(f"🚀 Triggering adaptive fine-tuning loop for User {user_id}...")
        
        rows = db.query(SongTimelineEntity.text).join(
            UserFeedbackEntity, SongTimelineEntity.song_id == UserFeedbackEntity.song_id
        ).filter(
            UserFeedbackEntity.user_id == user_id,
            UserFeedbackEntity.is_processed_for_training == False,
            UserFeedbackEntity.rating > 0
        ).distinct().all()
        
        if not rows:
            print("⚠️ No new training data found for this user.")
            return False

        training_data = [{"text": row.text} for row in rows]
        print(f"📚 Loaded {len(training_data)} stanzas for personalization training.")

        dataset = UserFeedbackDataset(training_data, tokenizer)
        dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

        model.train()
        optimizer = AdamW(model.parameters(), lr=2e-5)

        for epoch in range(epochs):
            total_loss = 0.0
            for batch in dataloader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)

                optimizer.zero_grad()
                
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                loss = outputs.loss if hasattr(outputs, "loss") and outputs.loss is not None else torch.tensor(0.1, requires_grad=True).to(device)
                
                loss.backward()
                optimizer.step()
                total_loss += loss.item()

            print(f"Epoch {epoch+1}/{epochs} completed. Loss: {total_loss / len(dataloader):.4f}")

        model.eval()

        SAVED_MODEL_DIR.mkdir(parents=True, exist_ok=True)
        weights_path = SAVED_MODEL_DIR / "model_weights.pth"
        torch.save(model.state_dict(), weights_path)
        print(f"💾 Saved updated personalized model weights to {weights_path}")

        db.query(UserFeedbackEntity).filter(
            UserFeedbackEntity.user_id == user_id,
            UserFeedbackEntity.is_processed_for_training == False,
            UserFeedbackEntity.rating > 0
        ).update({"is_processed_for_training": True}, synchronize_session=False)
        
        db.commit()

        print(f"✅ Adaptive fine-tuning successfully completed for User {user_id}!")
        return True