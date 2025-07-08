# Tracks input count, triggers retraining

import os
import json
import uuid
import pandas as pd
from retraining.trainer import retrain
import threading
import time

LOG_PATH = "storage/inputs_log.jsonl"
SENTIMENT_DIR = "storage/sentiment_batches"
TOXICITY_DIR = "storage/toxicity_batches"
THRESHOLD = 1000

os.makedirs(SENTIMENT_DIR, exist_ok=True)
os.makedirs(TOXICITY_DIR, exist_ok=True)

def monitor_and_trigger():
    if not os.path.exists(LOG_PATH):
        return "No log file yet."

    # Read all inputs
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) < THRESHOLD:
        return f"{len(lines)} samples collected — waiting for {THRESHOLD - len(lines)} more."

    # Parse and prepare batch
    samples = [json.loads(line) for line in lines]
    sentiment_rows = [{"text": s["text"], "label": 1 if s["sentiment"] == "positive" else 0} for s in samples]
    toxicity_rows = [{"text": s["text"], "label": 1 if s["toxicity"] == "toxic" else 0} for s in samples]

    # Save batches
    batch_id = str(uuid.uuid4())[:8]
    pd.DataFrame(sentiment_rows).to_csv(f"{SENTIMENT_DIR}/batch_{batch_id}.csv", index=False)
    pd.DataFrame(toxicity_rows).to_csv(f"{TOXICITY_DIR}/batch_{batch_id}.csv", index=False)

    # Clear log
    open(LOG_PATH, "w").close()

    # Trigger retraining
    retrain("sentiment")
    retrain("toxicity")

    return f"Retrained both models with {len(samples)} new samples."

def start_monitoring(interval=3600):
    def loop():
        while True:
            print(monitor_and_trigger())
            time.sleep(interval)
    t = threading.Thread(target=loop, daemon=True)
    t.start()

# To start monitoring automatically, call start_monitoring() from somewhere (e.g., main.py or __main__)
