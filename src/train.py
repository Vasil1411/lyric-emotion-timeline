"""Training entry point for the emotion classifier."""

from __future__ import annotations

from .config import BATCH_SIZE, LEARNING_RATE, NUM_TRAIN_EPOCHS


def train(dataset_path: str, output_dir: str = "artifacts/model"):
    """Train the classifier using the Hugging Face Trainer."""
    from datasets import Dataset
    from transformers import TrainingArguments

    from .dataset import load_lyrics_dataset
    from .model import create_model

    dataset = Dataset.from_pandas(load_lyrics_dataset(dataset_path))
    model = create_model()
    arguments = TrainingArguments(
        output_dir=output_dir,
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=BATCH_SIZE,
        num_train_epochs=NUM_TRAIN_EPOCHS,
        report_to="none",
    )
    from transformers import Trainer

    trainer = Trainer(model=model, args=arguments, train_dataset=dataset)
    trainer.train()
    trainer.save_model(output_dir)
    return trainer


if __name__ == "__main__":
    train("data/lyrics.csv")
