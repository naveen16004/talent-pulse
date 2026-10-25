import pytest
from fastapi import HTTPException
from app.schemas import CandidateProfile, EvaluationReport
from app.parser import extract_text_from_pdf


def test_candidate_profile_schema():
    profile = CandidateProfile(
        full_name="Jane Doe",
        email="jane@example.com",
        total_experience_years=4.5,
        primary_skills=["Python", "FastAPI", "Docker"],
        education=["B.S. in Computer Science"],
    )
    assert profile.full_name == "Jane Doe"
    assert profile.total_experience_years == 4.5
    assert len(profile.primary_skills) == 3


def test_evaluation_report_schema_bounds():
    with pytest.raises(ValueError):
        EvaluationReport(
            match_score=150,
            recommendation="Strong Match",
            key_strengths=[],
            critical_gaps=[],
            interview_questions=[],
            reasoning="Invalid score test",
        )


def test_extract_text_empty_bytes():
    with pytest.raises(HTTPException) as exc_info:
        extract_text_from_pdf(b"")
    assert exc_info.value.status_code == 400