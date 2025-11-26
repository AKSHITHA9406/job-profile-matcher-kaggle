def normalize_skill(skill: str) -> str:
    skill = skill.strip().lower()
    mapping = {
        "js": "javascript",
        "node.js": "nodejs",
        "node": "nodejs",
        "py": "python",
    }
    return mapping.get(skill, skill)

def normalize_degree(text: str) -> str:
    t = text.lower()
    if "phd" in t or "doctor" in t:
        return "PHD"
    if "master" in t or "msc" in t or "m.tech" in t:
        return "MASTER"
    if "bachelor" in t or "bsc" in t or "b.tech" in t:
        return "BACHELOR"
    return "OTHER"
