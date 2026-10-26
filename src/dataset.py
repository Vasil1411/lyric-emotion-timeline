import torch
from torch.utils.data import Dataset

class LyricDataset(Dataset):
    """
    Custom PyTorch Dataset for handling and tokenizing song lyrics 
    along with their corresponding emotion labels.
    """
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        """Returns the total number of samples in the dataset."""
        return len(self.texts)

    def __getitem__(self, idx):
        """Retrieves and tokenizes a single song verse by index."""
        text = str(self.texts[idx])
        label = self.labels[idx]

        # Tokenize the text using the multilingual tokenizer
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "labels": torch.tensor(label, dtype=torch.long)
        }