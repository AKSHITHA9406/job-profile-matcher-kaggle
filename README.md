# AI-Based Job Profile & Resume Matching System (Kaggle Edition)

This is your project in a **GitHub-ready format**, similar in style to the Anime Chatbot repository you shared, but built for:

- **Job profile understanding** (from PDF)
- **Resume parsing & profiling**
- **AI-based matching & recommendation**
- **Integration with a large Kaggle resume dataset**

---

## 1. Features

- Parses **job profiles (PDF)**:
  - Role summary
  - Required & preferred skills
  - Experience expectations
  - Education requirements
  - Certifications
  - Embedding for semantic similarity

- Builds **candidate profiles** from:
  - **PDF/DOCX resumes** (folder-based)
  - **Kaggle resume dataset (CSV)** – large-scale testing

- Computes a **composite fit score** (0–100) with weights:
  - Skill Match – 40%
  - Experience Alignment – 25%
  - Education Match – 15%
  - Certifications Match – 5%
  - Semantic Similarity – 15%

- Provides for each candidate:
  - Overall fit score
  - Component scores
  - Matched skills
  - Missing required skills
  - Missing nice-to-have skills
  - Short AI-style rationale

- Uses **local embeddings** (Sentence-BERT, `all-MiniLM-L6-v2`) →  
  **No API key, no billing, works offline.**

---

## 2. Project Structure

```text
job-profile-matcher-kaggle/
├── README.md
├── LICENSE
├── .gitignore
├── datasets/
│   └── README.md
└── backend/
    ├── requirements.txt
    ├── main.py              # FastAPI app (/match endpoint)
    ├── cli.py               # CLI for job PDF + resume PDFs/DOCX
    ├── cli_kaggle.py        # CLI for job PDF + Kaggle resume CSV
    ├── config.py            # Weights & model config
    ├── models.py            # Pydantic models
    ├── job_matching.py      # Shared ranking logic for folder-based resumes
    ├── datasets/
    │   └── kaggle_loader.py # Utilities to load Kaggle resume dataset
    ├── data/
    │   └── skills_dictionary.json
    ├── parsing/
    │   ├── __init__.py
    │   ├── text_extraction.py
    │   ├── job_parser.py
    │   └── resume_parser.py
    ├── nlp/
    │   ├── __init__.py
    │   ├── normalization.py
    │   ├── ner_skill_extractor.py
    │   └── embeddings.py
    └── matching/
        ├── __init__.py
        ├── scoring.py
        └── explanation.py
```

---

## 3. Setup (VS Code / Local)

### 3.1. Clone and open in VS Code

```bash
git clone https://github.com/YOUR-USERNAME/job-profile-matcher-kaggle.git
cd job-profile-matcher-kaggle
code .
```

### 3.2. Create & activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# or on Windows (PowerShell):
# .venv\Scripts\activate
```

### 3.3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## 4. Using a Kaggle Dataset

### 4.1. Download a resume dataset from Kaggle

You can use any resume dataset where each row has a full resume text column (for example, Kaggle's "Resume Dataset" which has a `Resume` column).

1. Download the dataset CSV from Kaggle.
2. Save it as:

```text
datasets/kaggle/resumes.csv
```

> You can customize:
> - File path via `--csv-path`  
> - Text column via `--text-column`  

### 4.2. Run matching with Kaggle dataset (CLI)

From `backend/`:

```bash
python3 cli_kaggle.py \
  --job "/absolute/path/to/job_profile.pdf" \
  --csv-path "../datasets/kaggle/resumes.csv" \
  --text-column "Resume" \
  --topn 20
```

This will:

- Parse the job PDF.
- Load thousands of resumes from the Kaggle CSV.
- Build candidate embeddings.
- Score and rank them.
- Print the **top N candidates** as JSON in the terminal.

---
