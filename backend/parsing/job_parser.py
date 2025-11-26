from typing import List, Tuple, Optional
import re

from .text_extraction import extract_text_any, TextExtractionError
from backend.nlp.ner_skill_extractor import extract_entities
from backend.nlp.embeddings import embed_text
from backend.models import JobProfile

def _extract_title(text: str) -> Optional[str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines[0] if lines else None

def _extract_role_summary(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(sentences[:4])

def _extract_experience(text: str) -> Tuple[Optional[int], Optional[str]]:
    matches = re.findall(r"(\d+)\+?\s+years?", text.lower())
    years = max(map(int, matches)) if matches else None
    expectation_sentence = None
    m = re.search(r"(?P<sent>[^.]*years[^.]*)\.", text, flags=re.IGNORECASE)
    if m:
        expectation_sentence = m.group("sent").strip()
    return years, expectation_sentence

def _extract_education_req(text: str) -> List[str]:
    degrees = []
    lowered = text.lower()
    if any(x in lowered for x in ["bachelor", "bsc", "b.tech"]):
        degrees.append("BACHELOR")
    if any(x in lowered for x in ["master", "msc", "m.tech"]):
        degrees.append("MASTER")
    if any(x in lowered for x in ["phd", "doctorate"]):
        degrees.append("PHD")
    return degrees

def parse_job_profile(path: str) -> JobProfile:
    try:
        raw = extract_text_any(path)
    except TextExtractionError as e:
        raise RuntimeError(f"Error reading job profile file: {e}") from e

    ents = extract_entities(raw)

    title = _extract_title(raw)
    role_summary = _extract_role_summary(raw)
    min_years, exp_expect = _extract_experience(raw)
    education_req = _extract_education_req(raw)

    required_skills = ents["skills"]
    preferred_skills: List[str] = []

    domain = None
    cert_req = ents["certifications"]
    embedding = embed_text(raw)

    return JobProfile(
        raw_text=raw,
        title=title,
        role_summary=role_summary,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        experience_expectations=exp_expect,
        min_years_experience=min_years,
        domain=domain,
        education_requirements=education_req,
        certifications_required=cert_req,
        certifications_preferred=[],
        embedding=embedding,
    )
