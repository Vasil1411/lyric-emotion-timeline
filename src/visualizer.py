"""Plotly visualizations for emotion timelines."""

from __future__ import annotations

import pandas as pd
import plotly.express as px


def emotion_timeline(scores: pd.DataFrame):
    """Build a line chart from rows containing segment, emotion and score."""
    required_columns = {"segment", "emotion", "score"}
    missing = required_columns.difference(scores.columns)
    if missing:
        raise ValueError(f"Missing visualization columns: {sorted(missing)}")

    return px.line(
        scores,
        x="segment",
        y="score",
        color="emotion",
        markers=True,
        title="Lyric emotion timeline",
    )
