from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_path = "models/minilm-heading"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def is_heading(text):
    if len(text.split()) < 2:
        return False
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=1)
        predicted = torch.argmax(probs, dim=1).item()
    return predicted == 1  
