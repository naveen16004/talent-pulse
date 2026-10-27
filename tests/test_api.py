import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import CandidateProfile, EvaluationReport
from app.parser import extract_text_from_pdf

client = TestClient(app)


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


def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "talentpulse-api"}


def test_screen_endpoint_rejects_non_pdf():
    response = client.post(
        "/api/v1/screen",
        files={"resume": ("sample.txt", b"plain text content", "text/plain")},
        data={"job_description": "Looking for a Python Developer."},
    )
    assert response.status_code == 400
    assert "Only PDF files are supported" in response.json()["detail"]