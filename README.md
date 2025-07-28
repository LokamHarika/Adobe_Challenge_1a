# Adobe Hackathon Round 1A – PDF Outline Extractor

## Challenge 1A - Adobe India Hackathon 2025
### PDF Title & Heading Extractor (Title, H1, H2, H3 with Page Numbers)

This project is a solution for Challenge 1A of the Adobe India Hackathon 2025. The goal is to extract structured information from PDFs by identifying the document title and all semantic headings (H1, H2, H3), and outputting the results in a hierarchical JSON format with associated page numbers.

## What It Does

The solution automatically analyzes PDF files to:
1. Detect the **document title** using the embedded metadata or fallback to the file name.
2. Extract semantic **headings** using a fine-tuned MiniLM transformer model.
3. Assign a **heading level** to each heading (H1, H2, H3) based on numbering and structure.
4. Output the result as a structured JSON file including the title and outline of headings with their levels and page numbers.

## Why This Approach?

Traditional rule-based systems fail to generalize across different types of documents. This project leverages:
- **PyMuPDF** for extracting layout-aware information from PDFs including text, font size, and positioning.
- **MiniLM transformer model** fine-tuned for heading classification, ensuring semantic understanding.
- **Font and numbering rules** to determine heading levels, maintaining hierarchical integrity.

This combination ensures the solution is robust across application forms, syllabi, academic documents, and other unstructured or semi-structured PDFs.

## Folder Structure

```
Challenge_1a/
├── app/
│   ├── heading_detector.py         # Contains heading classifier logic using MiniLM
│   ├── utils.py
│   ├── extract_pdf_headings.py     # Extracts title and headings from PDFs
│   ├── train_model.py              # Trains MiniLM model on custom labeled dataset
│   ├── download_model.py           # Downloads pretrained MiniLM model from HuggingFace
│   └── models/
│       └── minilm-heading/         # Folder where the fine-tuned model and tokenizer are stored
├── input/                          # Directory where input PDFs are placed for processing
│   └── sample.pdf
├── output/                         # Directory where output JSON files are saved
│   └── sample.json
├── run.py                          # Main script to extract headings from all PDFs in the input folder
├── Dockerfile                      # Docker setup to run the application in an isolated environment
├── requirements.txt                # List of Python dependencies
└── README.md                       # Documentation
```

## ⚙️ Technologies & Modules Used
- **Python 3.10+**
- **PyMuPDF (fitz)** - To extract text + font info from PDFs
- **HuggingFace Transformers** - For loading and fine-tuning MiniLM
- **MiniLM** - Lightweight transformer used for heading classification
- **scikit-learn** - Train-test split, accuracy evaluation
- **Docker** - Optional, for reproducible offline CPU-only execution

## 📥 Input Format
Place your PDF(s) in the `input/` folder. Each file is a standalone document.

## 📤 Output Format
Each processed PDF will output a `.json` file in the `output/` folder:
```json
{
  "title": "Your PDF Title",
  "outline": [
    { "level": "H1", "text": "1. Introduction", "page": 0 },
    { "level": "H2", "text": "1.1 Overview", "page": 0 }
  ]
}
```

## 🚀  How to Run

### A. Using Python (Locally)

```bash
# 1. Clone the repo and navigate
cd Challenge_1a

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download model
python app/download_model.py

# 4. Train model if not present
python app/train_model.py

# 5. Run the extractor
python run.py
```

### B. Using Docker (Offline, CPU-only)

```bash
# Build the Docker image
docker build -t adobe1a .

# Run the container (processes all PDFs from input/ → output/)
docker run --rm -v "$PWD/input:/app/input" -v "$PWD/output:/app/output" adobe1a
```

## ❓ Why These Tools?

- **MiniLM**: Lightweight (<100MB), fast on CPU, semantically rich
- **PyMuPDF**: Accurately captures font size, position, layout — critical for heading detection
- **Docker**: Ensures environment reproducibility, guarantees offline CPU-only compliance

## 📊 Performance (on Sample Dataset)

| Metric               | Value              |
|----------------------|--------------------|
| Model Size           | ~90MB              |
| Accuracy (Val Set)   | ~96%               |
| Inference Time       | 2–4 sec per PDF    |
| Offline/CPU Support  | ✅ Fully supported  |

## 👨‍💻 Authors
 
**Team**: Learnova  
**Challenge**: Adobe Document Intelligence - Round 1A
