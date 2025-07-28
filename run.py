import os
from app.extract_pdf_headings import process_pdf  

INPUT_DIR = "input"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🟢 Starting heading extraction...")

for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".pdf"):
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
        process_pdf(input_path, output_path) 

print("✅ All PDFs processed.")

