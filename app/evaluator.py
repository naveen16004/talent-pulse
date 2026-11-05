import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.schemas import CandidateProfile, EvaluationReport, ScreeningResult

load_dotenv()


def get_client() -> OpenAI:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in .env file.")
    return OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
    )


def resolve_available_model(client: OpenAI) -> str:
    """Dynamically picks the best available supported model from the Groq account."""
    preferred_order = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
    try:
        available_ids = {m.id for m in client.models.list().data}
        for model in preferred_order:
            if model in available_ids:
                return model
        # Fallback to the first available chat model
        for model_id in available_ids:
            if "whisper" not in model_id:
                return model_id
    except Exception:
        pass
    return "llama3-8b-8192"


def evaluate_candidate(resume_text: str, job_description: str) -> ScreeningResult:
    client = get_client()
    model_name = resolve_available_model(client)

    # Step 1: Extract candidate profile
    profile_prompt = f"""
    You are an expert technical recruiter and resume parser.
    Extract the candidate profile information from this resume text into valid JSON.
    Schema:
    {{
      "full_name": string or null,
      "email": string or null,
      "total_experience_years": float,
      "primary_skills": [string],
      "education": [string]
    }}

    Return ONLY the raw JSON object.

    RESUME TEXT:
    {resume_text}
    """

    res1 = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": profile_prompt}],
        response_format={"type": "json_object"},
    )
    profile_data = json.loads(res1.choices[0].message.content)
    profile = CandidateProfile(**profile_data)

    # Step 2: Evaluate against Job Description
    eval_prompt = f"""
    You are an objective hiring manager.
    Evaluate the candidate against the target job description.

    CANDIDATE DETAILS:
    - Experience: {profile.total_experience_years} years
    - Key Skills: {', '.join(profile.primary_skills)}
    - Full Resume Context:
    {resume_text}

    TARGET JOB DESCRIPTION:
    {job_description}

    Schema:
    {{
      "match_score": integer between 0 and 100,
      "recommendation": "Strong Match" or "Potential Match" or "No Match",
      "key_strengths": ["strength 1", "strength 2", "strength 3"],
      "critical_gaps": ["gap 1", "gap 2"],
      "interview_questions": ["question 1", "question 2", "question 3"],
      "reasoning": "2-sentence executive summary"
    }}

    Return ONLY the raw JSON object.
    """

    res2 = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": eval_prompt}],
        response_format={"type": "json_object"},
    )
    eval_data = json.loads(res2.choices[0].message.content)
    evaluation = EvaluationReport(**eval_data)

    return ScreeningResult(candidate=profile, evaluation=evaluation)