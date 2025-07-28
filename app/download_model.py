from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

MODEL_NAME = "microsoft/MiniLM-L12-H384-uncased"
SAVE_PATH = "./models/minilm-heading"

os.makedirs(SAVE_PATH, exist_ok=True)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

tokenizer.save_pretrained(SAVE_PATH)
model.save_pretrained(SAVE_PATH)

print(f"✅ Model saved to {SAVE_PATH}")
