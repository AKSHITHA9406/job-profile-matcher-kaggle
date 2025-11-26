from typing import Iterable, List
from pathlib import Path
import uuid

import pandas as pd

from backend.models import CandidateProfile, EducationEntry, ExperienceEntry
from backend.nlp.ner_skill_extractor import extract_entities
from backend.nlp.embeddings import embed_text

def load_kaggle_resumes(
    csv_path: str,
    text_column: str = "Resume",
    name_column: str | None = None,
    max_rows: int | None = None,
) -> List[CandidateProfile]:
    """Load resumes from a Kaggle CSV file and convert them to CandidateProfile objects.

    Parameters
    ----------
    csv_path : str
        Path to the Kaggle CSV dataset.
    text_column : str, default "Resume"
        Column that contains the full resume text.
    name_column : str | None, optional
        Optional column for candidate name; if None, names will be left empty.
    max_rows : int | None, optional
        Limit the number of rows to load (for quick testing).

    Returns
    -------
    List[CandidateProfile]
    """
    p = Path(csv_path)
    if not p.exists():
        raise FileNotFoundError(f"Kaggle CSV not found: {p.resolve()}")

    df = pd.read_csv(p)

    if text_column not in df.columns:
        raise ValueError(
            f"Expected text column '{text_column}' not found. "
            f"Available columns: {list(df.columns)}"
        )

    if max_rows is not None:
        df = df.head(max_rows)

    candidates: List[CandidateProfile] = []

    for _, row in df.iterrows():
        text = str(row[text_column])
        name = str(row[name_column]) if name_column and name_column in df.columns else None

        ents = extract_entities(text)
        embedding = embed_text(text)

        cand = CandidateProfile(
            candidate_id=str(uuid.uuid4()),
            name=name,
            email=None,
            phone=None,
            education=[
                EducationEntry(degree=d) for d in ents["degrees"]
            ],
            experience=[],
            skills=ents["skills"],
            technologies=ents["skills"],
            certifications=ents["certifications"],
            projects=ents["projects"],
            total_years_experience=None,
            domains=[],
            embedding=embedding,
            raw_text=text,
        )
        candidates.append(cand)

    return candidates
