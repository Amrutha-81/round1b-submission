import os
import fitz  # PyMuPDF
import json
from datetime import datetime

# --- Configuration ---
INPUT_DIR = "app/input"
OUTPUT_DIR = "app/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "final_output.json")

# --- Persona Definition ---
persona = "Undergraduate Chemistry Student preparing for exams on reaction kinetics"
job_to_be_done = "Identify key concepts and mechanisms for exam preparation on reaction kinetics"

# --- Define Relevant Keywords ---
KEYWORDS = [
    "reaction", "kinetics", "rate", "mechanism", "activation energy",
    "chemical reaction", "transition state", "order", "catalyst", "intermediate"
]

# --- Function to check keyword match ---
def is_relevant(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in KEYWORDS)

# --- Rank section based on number of keyword hits ---
def calculate_importance(text):
    text_lower = text.lower()
    return sum(1 for keyword in KEYWORDS if keyword in text_lower)

# --- Extract headings or lines with relevance ---
def extract_relevant_sections(filepath):
    print(f"Processing: {os.path.basename(filepath)}")
    doc = fitz.open(filepath)
    sections = []

    for page_number in range(len(doc)):
        page = doc[page_number]
        blocks = page.get_text("blocks")

        for block in blocks:
            text = block[4].strip()
            if len(text) < 20:
                continue  # Skip tiny blocks
            if is_relevant(text):
                importance = calculate_importance(text)
                sections.append({
                    "document": os.path.basename(filepath),
                    "page": page_number + 1,
                    "section_title": text,
                    "importance_rank": importance
                })

    # Sort and return top 5 per PDF
    sections.sort(key=lambda x: x["importance_rank"], reverse=True)
    return sections[:5]

# --- Main execution ---
def main():
    print("main() started")

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    all_sections = []
    input_files = [
        f for f in os.listdir(INPUT_DIR)
        if f.endswith(".pdf")
    ]

    for filename in input_files:
        path = os.path.join(INPUT_DIR, filename)
        sections = extract_relevant_sections(path)
        all_sections.extend(sections)

    # Sort final combined results
    all_sections.sort(key=lambda x: x["importance_rank"], reverse=True)

    # Prepare Output JSON
    output = {
        "metadata": {
            "input_documents": input_files,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "timestamp": str(datetime.now())
        },
        "extracted_sections": all_sections[:10],  # Only top 10 relevant sections overall
        "subsection_analysis": [
            {
                "document": s["document"],
                "page": s["page"],
                "refined_text": s["section_title"],
                "importance_rank": s["importance_rank"]
            } for s in all_sections[:10]
        ]
    }

    print(f"Saving output to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print(f"Output written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
