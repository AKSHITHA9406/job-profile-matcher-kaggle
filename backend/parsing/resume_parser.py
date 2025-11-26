from typing import List, Tuple
import re
import uuid

from .text_extraction import extract_text_any, TextExtractionError
from backend.nlp.ner_skill_extractor import extract_entities
from backend.nlp.embeddings import embed_text
from backend.models import CandidateProfile, EducationEntry, ExperienceEntry

EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
PHONE_REGEX = r"(\+?\d[\d\-\s]{7,}\d)"

def _extract_contact(text: str) -> Tuple[str | None, str | None]:
    email_match = re.search(EMAIL_REGEX, text)
    phone_match = re.search(PHONE_REGEX, text)
    return (
        email_match.group(0) if email_match else None,
        phone_match.group(0) if phone_match else None,
    )

def _estimate_total_experience(text: str) -> float | None:
    matches = re.findall(r"(\d+)\+?\s+years?", text.lower())
    return float(max(map(int, matches))) if matches else None

def parse_resume(path: str, mask_pii: bool = True) -> CandidateProfile:
    try:
        raw = extract_text_any(path)
    except TextExtractionError as e:
        raise RuntimeError(f"Error reading resume file '{path}': {e}") from e

    ents = extract_entities(raw)

    email, phone = _extract_contact(raw)
    candidate_id = str(uuid.uuid4())
    name = None  # could be improved

    education = [
        EducationEntry(
            degree=d,
            field_of_study=None,
            institution=None,
            start_year=None,
            end_year=None,
        )
        for d in ents["degrees"]
    ]

    experience: List[ExperienceEntry] = []

    total_exp = _estimate_total_experience(raw)
    embedding = embed_text(raw)

    if mask_pii:
        email = None
        phone = None

    return CandidateProfile(
        candidate_id=candidate_id,
        name=name,
        email=email,
        phone=phone,
        education=education,
        experience=experience,
        skills=ents["skills"],
        technologies=ents["skills"],
        certifications=ents["certifications"],
        projects=ents["projects"],
        total_years_experience=total_exp,
        domains=[],
        embedding=embedding,
        raw_text=raw,
    )
