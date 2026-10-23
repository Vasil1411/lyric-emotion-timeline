"""Inference helpers for predicting emotions from lyrics."""

from __future__ import annotations

from transformers import pipeline

from .config import MODEL_NAME


def create_classifier(model_name: str = MODEL_NAME):
    """Create a text-classification pipeline."""
    return pipeline("text-classification", model=model_name, top_k=None)


def predict(text: str, model_name: str = MODEL_NAME):
    """Return emotion scores for a lyric excerpt."""
    if not text.strip():
        raise ValueError("Text must not be empty.")
    return create_classifier(model_name)(text)
