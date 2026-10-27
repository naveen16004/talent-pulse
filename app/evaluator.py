import os
from openai import OpenAI
from app.schemas import CandidateProfile, EvaluationReport, ScreeningResult


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "mock-key")
    return OpenAI(api_key=api_key)


def evaluate_candidate(resume_text: str, job_description: str) -> ScreeningResult:
    client = get_openai_client()

    # Step 1: Extract candidate profile
    profile_prompt = f"""
    You are an expert technical recruiter and resume parser.
    Extract the candidate profile information from this resume text:
    ---
    {resume_text}
    """
    profile_response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": profile_prompt}],
        response_format=CandidateProfile,
    )
    profile = profile_response.choices[0].message.parsed

    # Step 2: Evaluate candidate against job description
    eval_prompt = f"""
    Evaluate this candidate against the target job description.

    CANDIDATE DETAILS:
    - Experience: {profile.total_experience_years} years
    - Key Skills: {', '.join(profile.primary_skills)}
    - Full Resume Context:
    {resume_text}

    TARGET JOB DESCRIPTION:
    {job_description}

    Provide:
    1. An objective match score (0-100).
    2. Recommendation: 'Strong Match', 'Potential Match', or 'No Match'.
    3. Distinct strengths directly mapping to requirements.
    4. Gaps or missing qualifications.
    5. Exactly 3 technical screening questions targeting identified gaps.
    6. A concise 2-sentence executive summary.
    """
    eval_response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": eval_prompt}],
        response_format=EvaluationReport,
    )
    evaluation = eval_response.choices[0].message.parsed

    return ScreeningResult(candidate=profile, evaluation=evaluation)