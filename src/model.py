import torch.nn as nn
from transformers import AutoModelForSequenceClassification
from src.config import MODEL_NAME, NUM_LABELS

class LyricEmotionClassifier(nn.Module):
    """
    Custom wrapper for XLM-RoBERTa sequence classification model.
    Handles the pre-trained transformer and the classification head for 5 emotions.
    """
    def __init__(self, model_name: str = MODEL_NAME, num_labels: int = NUM_LABELS):
        super(LyricEmotionClassifier, self).__init__()
        
        # Load the pre-trained multilingual transformer with a sequence classification head
        self.transformer = AutoModelForSequenceClassification.from_pretrained(
            model_name, 
            num_labels=num_labels
        )

    def forward(self, input_ids, attention_mask, labels=None):
        """
        Forward pass for training and inference.
        """
        outputs = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )
        return outputs