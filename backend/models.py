from typing import List, Optional, Dict
from pydantic import BaseModel

class EducationEntry(BaseModel):
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    institution: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None

class ExperienceEntry(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    description: Optional[str] = None
    domain: Optional[str] = None

class JobProfile(BaseModel):
    raw_text: str
    title: Optional[str] = None
    role_summary: Optional[str] = None
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    experience_expectations: Optional[str] = None
    min_years_experience: Optional[float] = None
    domain: Optional[str] = None
    education_requirements: List[str] = []
    certifications_required: List[str] = []
    certifications_preferred: List[str] = []
    embedding: Optional[List[float]] = None
    extra_metadata: Dict[str, str] = {}

class CandidateProfile(BaseModel):
    candidate_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    education: List[EducationEntry] = []
    experience: List[ExperienceEntry] = []
    skills: List[str] = []
    technologies: List[str] = []
    certifications: List[str] = []
    projects: List[str] = []

    total_years_experience: Optional[float] = None
    domains: List[str] = []

    embedding: Optional[List[float]] = None
    raw_text: str

class MatchComponentScore(BaseModel):
    skill_match: float
    experience_alignment: float
    education_match: float
    certifications_match: float
    semantic_similarity: float

class MatchResult(BaseModel):
    candidate_id: str
    name: Optional[str]
    fit_score_0_100: float
    components: MatchComponentScore
    matched_skills: List[str]
    missing_required_skills: List[str]
    nice_to_have_missing_skills: List[str]
    rationale: str
