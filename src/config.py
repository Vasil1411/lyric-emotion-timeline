import os
from pathlib import Path

# Base directory of the project (points to the root lyric-emotion-timeline folder)
BASE_DIR = Path(__file__).resolve().parent.parent

# Model and Tokenizer settings
MODEL_NAME = "xlm-roberta-base"
MAX_LENGTH = 128

# Emotion classes mapping
EMOTIONS = ["Joy", "Sadness", "Hype", "Anger", "Nostalgia"]
NUM_LABELS = len(EMOTIONS)

# Training hyperparameters
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
EPOCHS = 3
WEIGHT_DECAY = 0.01

# Directory paths configuration
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"
SAVED_MODEL_DIR = MODELS_DIR / "best_model"

# Automatically create necessary directories if they don't exist yet
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(SAVED_MODEL_DIR, exist_ok=True)