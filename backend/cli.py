import argparse
import json
import sys

from backend.job_matching import rank_candidates

def main():
    parser = argparse.ArgumentParser(description="AI-Based Job Profile and Resume Matching System (folder-based resumes)")
    parser.add_argument("--job", required=True, help="Path to job profile PDF")
    parser.add_argument("--resumes", required=True, help="Folder with candidate resumes (PDF/DOCX)")
    parser.add_argument("--topn", type=int, default=10, help="Number of top candidates to return")
    args = parser.parse_args()

    try:
        ranked = rank_candidates(args.job, args.resumes, args.topn)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps([r.model_dump() for r in ranked], indent=2))

if __name__ == "__main__":
    main()
