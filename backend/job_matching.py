from pathlib import Path
from typing import List

from backend.parsing.job_parser import parse_job_profile
from backend.parsing.resume_parser import parse_resume
from backend.matching.scoring import compute_component_scores, compute_overall_score
from backend.matching.explanation import build_rationale
from backend.models import MatchResult

def rank_candidates(job_pdf: str, resumes_dir: str, top_n: int = 10, weights=None) -> List[MatchResult]:
    job_path = Path(job_pdf)
    resumes_path = Path(resumes_dir)

    if not job_path.exists():
        raise FileNotFoundError(f"Job profile file not found: {job_path.resolve()}")
    if not resumes_path.exists() or not resumes_path.is_dir():
        raise FileNotFoundError(f"Resumes folder not found or not a directory: {resumes_path.resolve()}")

    job = parse_job_profile(str(job_path))

    results: List[MatchResult] = []
    resume_files = list(resumes_path.glob("*"))
    if not resume_files:
        raise FileNotFoundError(f"No resume files found in folder: {resumes_path.resolve()}")

    for path in resume_files:
        if path.suffix.lower() not in {".pdf", ".doc", ".docx"}:
            continue
        cand = parse_resume(str(path))

        comps, matched, missing_req, missing_pref = compute_component_scores(job, cand)
        fit = compute_overall_score(comps, weights)
        rationale = build_rationale(job, cand, comps, matched, missing_req, missing_pref)

        results.append(
            MatchResult(
                candidate_id=cand.candidate_id,
                name=cand.name,
                fit_score_0_100=round(fit, 2),
                components=comps,
                matched_skills=matched,
                missing_required_skills=missing_req,
                nice_to_have_missing_skills=missing_pref,
                rationale=rationale,
            )
        )

    results.sort(key=lambda r: r.fit_score_0_100, reverse=True)
    return results[:top_n]
