# connecting-the-dots-round1b

**Adobe "Connecting the Dots" Challenge — Round 1B Submission**

This project acts as a **Persona-Driven Document Intelligence System**. It analyzes a set of PDF documents and intelligently extracts and ranks the most relevant sections based on a provided persona and their specific job-to-be-done.

---

##  Problem Statement

> “Connect What Matters — For the User Who Matters”

You are given:
- A collection of related PDF documents
- A persona definition (their role and focus area)
- A job-to-be-done (task the persona wants to accomplish)

 The goal is to:
- Identify and extract the most relevant sections
- Rank them by importance
- Analyze sub-sections for further insights

---

##  Technologies Used

- **Python 3.10**
- **PyMuPDF (`fitz`)** — PDF parsing and section detection
- **Docker** — Ensures offline, platform-independent execution

---

##  Folder Structure
├── Dockerfile
├── requirements.txt
├── instructions.txt
├── approach_explanation.md
├── app/
│ ├── main.py
│ ├── input/
│ │ ├── (Your PDFs here)
│ │ └── persona_job.json
│ └── output/
│ └── final_output.json


---

##  How to Run

### 1. Place Your Files

Put your input PDFs and `persona_job.json` inside the `app/input/` folder.

---

### 2. Build the Docker Image

```bash
docker build -t persona_extractor:round1b .

Run the container
docker run --rm ^
-v "%cd%\app\input":/app/input ^
-v "%cd%\app\output":/app/output ^
--network none persona_extractor:round1b

Output
The result will be saved as:

app/output/final_output.json
Contents:
Metadata: input files, persona, job-to-be-done, timestamp

Extracted Sections: document, page number, title, importance rank

Sub-section Analysis: refined highlights for deep insight


Constraints Met
Model runs fully offline

Uses CPU only

Executes in under 60 seconds

Docker image is < 1GB



Example persona
{
  "persona": "Investment Analyst",
  "job_to_be_done": "Analyze revenue trends and R&D investments from company reports"
}


