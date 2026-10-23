# Lyric Emotion Timeline: Multilingual Song Emotion & Dynamics Classifier

A production-grade Machine Learning project that analyzes the emotional dynamics of songs verse by verse, rather than performing a static sentiment analysis on the track as a whole.

## Project Structure

```text
lyric-emotion-timeline/
├── data/                    # Raw and processed datasets
├── notebooks/               # Exploratory data analysis & experiments
├── src/                     # Core Python package
│   ├── __init__.py
│   ├── config.py            # Configurations, hyperparameters & class mappings
│   ├── dataset.py           # PyTorch Dataset & DataLoaders for multilingual text
│   ├── model.py             # XLM-RoBERTa classification architecture
│   ├── train.py             # Training loop with metrics and evaluation
│   ├── inference.py         # Prediction pipeline & timeline smoothing
│   └── visualizer.py        # Interactive Plotly charts generator
├── app.py                   # Streamlit web application interface
├── Dockerfile               # Containerization setup
└── requirements.txt         # Project dependencies

## Getting Started

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

For training, your CSV dataset must contain a text column and can be executed via
`python -m src.train`.
