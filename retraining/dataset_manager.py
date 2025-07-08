# Adds new samples, saves batches, prepares training data

import os
import json
import uuid
import pandas as pd

LOG_PATH = "storage/inputs_log.jsonl"
SENTIMENT_DIR = "storage/sentiment_batches"
TOXICITY_DIR = "storage/toxicity_batches"
BATCH_SIZE = 1000

os.makedirs(SENTIMENT_DIR, exist_ok=True)
os.makedirs(TOXICITY_DIR, exist_ok=True)

def add_sample(text, sentiment, toxicity):
    """Add a new sample to the log file."""
    log_entry = {
        "id": str(uuid.uuid4()),
        "text": text[:1000],
        "sentiment": sentiment,
        "toxicity": toxicity
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

def save_batches():
    """Save new batches if enough samples are collected."""
    if not os.path.exists(LOG_PATH):
        return "No log file yet."

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) < BATCH_SIZE:
        return f"{len(lines)} samples collected — waiting for {BATCH_SIZE - len(lines)} more."

    samples = [json.loads(line) for line in lines]
    sentiment_rows = [{"text": s["text"], "label": 1 if s["sentiment"] == "positive" else 0} for s in samples]
    toxicity_rows = [{"text": s["text"], "label": 1 if s["toxicity"] == "toxic" else 0} for s in samples]

    batch_id = str(uuid.uuid4())[:8]
    pd.DataFrame(sentiment_rows).to_csv(f"{SENTIMENT_DIR}/batch_{batch_id}.csv", index=False)
    pd.DataFrame(toxicity_rows).to_csv(f"{TOXICITY_DIR}/batch_{batch_id}.csv", index=False)

    # Clear log after saving
    open(LOG_PATH, "w").close()
    return f"Saved new batches with {len(samples)} samples."

def prepare_training_data(task="sentiment"):
    """Combine all batches and return a DataFrame for training."""
    assert task in ["sentiment", "toxicity"], "Task must be 'sentiment' or 'toxicity'"
    batch_dir = SENTIMENT_DIR if task == "sentiment" else TOXICITY_DIR
    batch_files = [os.path.join(batch_dir, f) for f in os.listdir(batch_dir) if f.endswith(".csv")]
    if not batch_files:
        return pd.DataFrame(columns=["text", "label"])
    dfs = [pd.read_csv(f) for f in batch_files]
    return pd.concat(dfs, ignore_index=True)

