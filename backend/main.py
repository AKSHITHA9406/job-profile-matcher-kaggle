from fastapi import FastAPI, UploadFile, File
from typing import List
import tempfile
import shutil
from pathlib import Path

from backend.parsing.job_parser import parse_job_profile
from backend.parsing.resume_parser import parse_resume
from backend.matching.scoring import compute_component_scores, compute_overall_score
from backend.matching.explanation import build_rationale
from backend.models import MatchResult

app = FastAPI(title="AI-Based Job Profile and Resume Matching API (Kaggle-ready)")

@app.post("/match", response_model=List[MatchResult])
async def match_candidates(
    job_file: UploadFile = File(...),
    resume_files: List[UploadFile] = File(...),
    top_n: int = 10,
):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        job_path = tmpdir_path / job_file.filename
        with open(job_path, "wb") as f:
            shutil.copyfileobj(job_file.file, f)

        resume_paths = []
        for rf in resume_files:
            rp = tmpdir_path / rf.filename
            with open(rp, "wb") as f:
                shutil.copyfileobj(rf.file, f)
            resume_paths.append(rp)

        job = parse_job_profile(str(job_path))

        results: List[MatchResult] = []
        for rp in resume_paths:
            cand = parse_resume(str(rp))
            comps, matched, missing_req, missing_pref = compute_component_scores(job, cand)
            fit = compute_overall_score(comps)
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
