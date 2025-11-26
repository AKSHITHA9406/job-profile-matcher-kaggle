import spacy
from typing import List, Dict
import json
from pathlib import Path
from .normalization import normalize_skill, normalize_degree

try:
    _nlp = spacy.load("en_core_web_sm")
except OSError as e:
    raise RuntimeError(
        "spaCy model 'en_core_web_sm' is not installed. "
        "Run: python -m spacy download en_core_web_sm"
    ) from e

skills_path = Path(__file__).resolve().parent.parent / "data" / "skills_dictionary.json"
if skills_path.exists():
    _SKILLS_SET = set(json.loads(skills_path.read_text()))
else:
    _SKILLS_SET = set()

_DEGREE_KEYWORDS = ["bachelor", "master", "phd", "b.tech", "bsc", "msc"]

def extract_entities(text: str) -> Dict[str, List[str]]:
    doc = _nlp(text)

    skills = set()
    orgs = set()
    certs = set()
    degrees = set()
    projects = set()

    for ent in doc.ents:
        if ent.label_ in ("ORG", "GPE"):
            orgs.add(ent.text.strip())
        if ent.label_ in ("WORK_OF_ART", "PRODUCT"):
            projects.add(ent.text.strip())

    lowered = text.lower()
    for skill in _SKILLS_SET:
        if skill.lower() in lowered:
            skills.add(normalize_skill(skill))

    for kw in _DEGREE_KEYWORDS:
        if kw in lowered:
            degrees.add(normalize_degree(kw))

    common_certs = ["aws certified", "pmp", "ccna", "ocp", "cissp"]
    for c in common_certs:
        if c in lowered:
            certs.add(c.upper())

    return {
        "skills": sorted(skills),
        "organizations": sorted(orgs),
        "certifications": sorted(certs),
        "degrees": sorted(degrees),
        "projects": sorted(projects),
    }
