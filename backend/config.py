from typing import Dict

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

DEFAULT_WEIGHTS: Dict[str, float] = {
    "skill_match": 0.40,
    "experience_alignment": 0.25,
    "education_match": 0.15,
    "certifications_match": 0.05,
    "semantic_similarity": 0.15,
}
