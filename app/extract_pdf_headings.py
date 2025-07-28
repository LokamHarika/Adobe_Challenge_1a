
import fitz
import os
import json
import re
from app.utils import clean_text, normalize_text
from app.heading_detector import is_heading

def extract_title_and_headings(pdf_path):
    doc = fitz.open(pdf_path)
    font_size_map = {}

    all_text_blocks = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                line_text = ""
                font_sizes = []
                bold_flags = []
                for span in line["spans"]:
                    text = clean_text(span["text"])
                    if text:
                        line_text += text + " "
                        font_sizes.append(span["size"])
                        bold_flags.append(span["flags"])
                text = normalize_text(line_text)
                if not text:
                    continue
                avg_font_size = sum(font_sizes) / len(font_sizes)
                is_bold = any(flag == 20 or flag == 21 for flag in bold_flags)
                all_text_blocks.append({
                    "text": text,
                    "font_size": avg_font_size,
                    "bold": is_bold,
                    "page": page_num
                })

                if avg_font_size not in font_size_map:
                    font_size_map[avg_font_size] = 0
                font_size_map[avg_font_size] += 1

    largest_font = max(font_size_map.keys())
    title_candidates = [b for b in all_text_blocks if abs(b["font_size"] - largest_font) < 0.5]
    title = " ".join([t["text"] for t in title_candidates]).strip()

    headings = []
    avg_font = sum([b["font_size"] for b in all_text_blocks]) / len(all_text_blocks)

    for block in all_text_blocks:
        text = block["text"]
        words = text.split()
        font_size = block["font_size"]

        if len(words) > 12:
            continue
        if font_size < avg_font:
            continue
        if re.match(r"^(Page \\d+|Version|May \\d{1,2}, \\d{4}|Copyright)", text, re.IGNORECASE):
            continue
        if is_heading(text):
            headings.append({
                "text": text,
                "page": block["page"],
                "font_size": font_size,
                "bold": block["bold"]
            })

    seen = set()
    unique_headings = []
    for h in headings:
        key = (h["text"].strip().lower(), h["page"])
        if key in seen:
            continue
        seen.add(key)
        unique_headings.append(h)

    headings = unique_headings

    if len(headings) < 2:
        outline = []
    else:
        unique_fonts = sorted({round(h["font_size"], 2) for h in headings}, reverse=True)
        level_map = {size: f"H{idx+1}" for idx, size in enumerate(unique_fonts)}
        for size in level_map:
            if int(level_map[size][1]) > 3:
                level_map[size] = "H3"

        outline = []
        for h in headings:
            level = level_map.get(round(h["font_size"], 2), "H3")
            outline.append({
                "level": level,
                "text": h["text"],
                "page": h["page"]
            })

    return {
        "title": title,
        "outline": outline
    }

def process_pdf(input_path, output_path):
    data = extract_title_and_headings(input_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)




