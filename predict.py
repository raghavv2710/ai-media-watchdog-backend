"""
✅ Model Prediction (predict.py)
Loads models from Hugging Face Hub using secure token (via env var).
Supports both sentiment and toxicity prediction.
"""

import os
from typing import Dict
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load Hugging Face token from environment
HF_TOKEN = os.environ.get("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("❌ HF_TOKEN not found in environment variables.")

# Load models from Hugging Face Hub
sentiment_model = AutoModelForSequenceClassification.from_pretrained(
    "raghavv2710/sentiment-roberta-base",
    token=HF_TOKEN
)
toxicity_model = AutoModelForSequenceClassification.from_pretrained(
    "raghavv2710/toxicity-roberta-base",
    token=HF_TOKEN
)
tokenizer = AutoTokenizer.from_pretrained("roberta-base", token=HF_TOKEN)

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
sentiment_model.to(device)
toxicity_model.to(device)

# Inference function
def classify(text: str) -> Dict[str, str]:
    if not isinstance(text, str):
        raise ValueError("Input to classify must be a string.")
    
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=256)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        sentiment_logits = sentiment_model(**inputs).logits
        toxicity_logits = toxicity_model(**inputs).logits

    sentiment = torch.argmax(sentiment_logits, dim=1).item()
    toxicity = torch.argmax(toxicity_logits, dim=1).item()

    return {
        "sentiment": "positive" if sentiment == 1 else "negative",
        "toxicity": "toxic" if toxicity == 1 else "non-toxic"
    }
