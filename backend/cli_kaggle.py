import argparse
import json
import sys

from backend.parsing.job_parser import parse_job_profile
from backend.datasets.kaggle_loader import load_kaggle_resumes
from backend.matching.scoring import compute_component_scores, compute_overall_score
from backend.matching.explanation import build_rationale
from backend.models import MatchResult

def main():
    parser = argparse.ArgumentParser(description="AI-Based Job & Resume Matching (Kaggle dataset version)")
    parser.add_argument("--job", required=True, help="Path to job profile PDF")
    parser.add_argument("--csv-path", required=True, help="Path to Kaggle CSV with resumes")
    parser.add_argument("--text-column", default="Resume", help="Column containing full resume text")
    parser.add_argument("--name-column", default=None, help="Optional column containing candidate names")
    parser.add_argument("--max-rows", type=int, default=None, help="Max rows from Kaggle CSV (for quicker tests)")
    parser.add_argument("--topn", type=int, default=10, help="Number of top candidates to return")
    args = parser.parse_args()

    try:
        job = parse_job_profile(args.job)
        candidates = load_kaggle_resumes(
            csv_path=args.csv_path,
            text_column=args.text_column,
            name_column=args.name_column,
            max_rows=args.max_rows,
        )
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    results: list[MatchResult] = []

    for cand in candidates:
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
    results = results[: args.topn]

    print(json.dumps([r.model_dump() for r in results], indent=2))

if __name__ == "__main__":
    main()
