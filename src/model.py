"""Emotion classification model factory."""

from __future__ import annotations

from transformers import AutoModelForSequenceClassification

from .config import EMOTION_LABELS, MODEL_NAME


def create_model(model_name: str = MODEL_NAME):
    """Create the configured multilingual sequence classifier."""
    labels = list(EMOTION_LABELS.values())
    return AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(labels),
        id2label=EMOTION_LABELS,
        label2id={label: index for index, label in EMOTION_LABELS.items()},
    )
