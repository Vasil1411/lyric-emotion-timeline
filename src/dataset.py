"""Dataset loading and preprocessing helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_lyrics_dataset(path: str | Path) -> pd.DataFrame:
    """Load a CSV dataset containing at least a lyrics/text column."""
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file was not found: {dataset_path}")

    dataset = pd.read_csv(dataset_path)
    if "text" not in dataset.columns:
        raise ValueError("The dataset must contain a 'text' column.")
    return dataset
