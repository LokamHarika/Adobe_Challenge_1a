import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

MODEL_PATH = "./models/minilm-heading"

df = pd.read_csv("app/training_data.csv")  
df = df.dropna()
df = df[['text', 'label']]  

tokenizer = AutoTokenizer.from_pretrained("microsoft/MiniLM-L12-H384-uncased")

def tokenize(batch):
    return tokenizer(batch['text'], padding=True, truncation=True)

dataset = Dataset.from_pandas(df)
dataset = dataset.train_test_split(test_size=0.1)
dataset = dataset.map(tokenize, batched=True)

model = AutoModelForSequenceClassification.from_pretrained("microsoft/MiniLM-L12-H384-uncased", num_labels=2)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=10,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
)

trainer.train()

model.save_pretrained(MODEL_PATH)
tokenizer.save_pretrained(MODEL_PATH)

print("✅ Model fine-tuned and saved to", MODEL_PATH)
