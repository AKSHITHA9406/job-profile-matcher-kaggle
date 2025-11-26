from backend.models import JobProfile, CandidateProfile, MatchComponentScore

def build_rationale(
    job: JobProfile,
    cand: CandidateProfile,
    comps: MatchComponentScore,
    matched_skills,
    missing_required,
    missing_pref,
) -> str:
    top_matched = ", ".join(matched_skills[:5]) or "no key skills"
    missing_req_str = ", ".join(missing_required[:3])
    missing_pref_str = ", ".join(missing_pref[:3])

    parts = []
    parts.append(
        f"Strong skill overlap ({int(comps.skill_match * 100)}%) including {top_matched}."
    )

    if comps.experience_alignment >= 0.9:
        parts.append("Candidate meets or exceeds the experience requirement.")
    elif comps.experience_alignment >= 0.6:
        parts.append("Experience is slightly below the requirement but still relevant.")
    else:
        parts.append("Experience appears below the required level.")

    if missing_req_str:
        parts.append(f"Missing required skills: {missing_req_str}.")
    if missing_pref_str:
        parts.append(f"Missing preferred skills: {missing_pref_str}.")

    return " ".join(parts)
