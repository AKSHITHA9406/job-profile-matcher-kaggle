from typing import Dict, List, Tuple
import numpy as np

from backend.models import JobProfile, CandidateProfile, MatchComponentScore
from backend.config import DEFAULT_WEIGHTS

def cosine_sim(a: List[float], b: List[float]) -> float:
    a_arr = np.array(a, dtype=float)
    b_arr = np.array(b, dtype=float)
    if np.linalg.norm(a_arr) == 0 or np.linalg.norm(b_arr) == 0:
        return 0.0
    return float(a_arr.dot(b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))

def skill_match_score(job: JobProfile, cand: CandidateProfile) -> Tuple[float, List[str], List[str], List[str]]:
    job_required = set(job.required_skills)
    cand_skills = set(cand.skills)

    exact = job_required & cand_skills

    fuzzy = set()
    for js in job_required:
        for cs in cand_skills:
            if js in cs or cs in js:
                fuzzy.add(js)

    covered = exact | fuzzy
    score = len(covered) / len(job_required) if job_required else 1.0

    missing_required = sorted(job_required - covered)
    nice_to_have_missing = sorted(set(job.preferred_skills) - cand_skills)

    return score, sorted(covered), missing_required, nice_to_have_missing

def experience_alignment_score(job: JobProfile, cand: CandidateProfile) -> float:
    if job.min_years_experience is None or cand.total_years_experience is None:
        return 0.5
    ratio = cand.total_years_experience / job.min_years_experience
    if ratio >= 1:
        return 1.0
    return max(0.0, ratio)

def education_match_score(job: JobProfile, cand: CandidateProfile) -> float:
    if not job.education_requirements:
        return 1.0
    cand_degrees = {e.degree for e in cand.education if e.degree}
    if not cand_degrees:
        return 0.0
    overlap = cand_degrees & set(job.education_requirements)
    return len(overlap) / len(job.education_requirements)

def certifications_match_score(job: JobProfile, cand: CandidateProfile) -> float:
    if not job.certifications_required:
        return 1.0
    cand_certs = set(cand.certifications)
    overlap = cand_certs & set(job.certifications_required)
    return len(overlap) / len(job.certifications_required)

def semantic_similarity_score(job: JobProfile, cand: CandidateProfile) -> float:
    if not job.embedding or not cand.embedding:
        return 0.0
    return cosine_sim(job.embedding, cand.embedding)

def compute_component_scores(job: JobProfile, cand: CandidateProfile):
    s_skill, matched, missing_req, missing_pref = skill_match_score(job, cand)
    s_exp = experience_alignment_score(job, cand)
    s_edu = education_match_score(job, cand)
    s_cert = certifications_match_score(job, cand)
    s_sem = semantic_similarity_score(job, cand)

    comps = MatchComponentScore(
        skill_match=s_skill,
        experience_alignment=s_exp,
        education_match=s_edu,
        certifications_match=s_cert,
        semantic_similarity=s_sem,
    )
    return comps, matched, missing_req, missing_pref

def compute_overall_score(comps: MatchComponentScore, weights: Dict[str, float] | None = None) -> float:
    w = weights or DEFAULT_WEIGHTS
    total = (
        comps.skill_match * w["skill_match"]
        + comps.experience_alignment * w["experience_alignment"]
        + comps.education_match * w["education_match"]
        + comps.certifications_match * w["certifications_match"]
        + comps.semantic_similarity * w["semantic_similarity"]
    )
    return total * 100.0
