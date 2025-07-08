# Retrains model using HF Transformers

import os
import pandas as pd
from datasets import load_dataset, concatenate_datasets, Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

def retrain(task="sentiment"):
    assert task in ["sentiment", "toxicity"], "Task must be either 'sentiment' or 'toxicity'"

    print(f"🔁 Starting retraining for {task} model...")

    # Define Hugging Face model repo ID
    model_id = f"raghavv2710/{task}-roberta-base"
    batch_dir = f"storage/{task}_batches"

    # Collect all batches
    batch_files = [os.path.join(batch_dir, f) for f in os.listdir(batch_dir) if f.endswith(".csv")]
    if not batch_files:
        print(f"No batches found for {task}. Skipping.")
        return

    datasets = [load_dataset("csv", data_files=file)["train"] for file in batch_files]
    full_dataset = concatenate_datasets(datasets)

    # Tokenization
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    def tokenize_fn(example): return tokenizer(example["text"], padding=True, truncation=True, max_length=256)
    tokenized_dataset = full_dataset.map(tokenize_fn)

    # Load base model
    model = AutoModelForSequenceClassification.from_pretrained("roberta-base", num_labels=2)

    # Training arguments
    output_dir = f"models/{task}_retrained"
    args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=16,
        num_train_epochs=3,
        evaluation_strategy="no",
        save_strategy="epoch",
        logging_steps=50,
        push_to_hub=True,
        hub_model_id=model_id,
        hub_token=os.getenv("HF_TOKEN")  # Set in .env or passed in CI
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized_dataset
    )

    trainer.train()

    print(f"✅ Retrained {task} model pushed to Hugging Face Hub: {model_id}")
