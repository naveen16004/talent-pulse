from pydantic import BaseModel, Field
from typing import List, Optional


class CandidateProfile(BaseModel):
    full_name: Optional[str] = Field(
        default=None, description="Extracted full name of the candidate"
    )
    email: Optional[str] = Field(
        default=None, description="Email address of the candidate"
    )
    total_experience_years: float = Field(
        default=0.0, description="Calculated total years of professional experience"
    )
    primary_skills: List[str] = Field(
        default_factory=list, description="Top technical and domain skills found in resume"
    )
    education: List[str] = Field(
        default_factory=list, description="Degrees, universities, or notable certifications"
    )


class EvaluationReport(BaseModel):
    match_score: int = Field(
        ge=0, le=100, description="Overall match score between 0 and 100"
    )
    recommendation: str = Field(
        description="'Strong Match', 'Potential Match', or 'No Match'"
    )
    key_strengths: List[str] = Field(
        default_factory=list,
        description="Top 3-4 strengths directly aligned with the job description",
    )
    critical_gaps: List[str] = Field(
        default_factory=list,
        description="Missing must-have requirements or skill deficiencies",
    )
    interview_questions: List[str] = Field(
        default_factory=list,
        description="3 targeted technical questions to test gaps during screening",
    )
    reasoning: str = Field(
        description="Concise 2-sentence executive summary for the hiring manager"
    )


class ScreeningResult(BaseModel):
    candidate: CandidateProfile
    evaluation: EvaluationReport