from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.parser import extract_text_from_pdf
from app.evaluator import evaluate_candidate
from app.schemas import ScreeningResult

app = FastAPI(
    title="TalentPulse Engine",
    description="Intelligent Resume Screening & Candidate Profiling API",
    version="1.0.0",
)

# Enable CORS for dashboard and external frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "talentpulse-api"}


@app.post("/api/v1/screen", response_model=ScreeningResult)
async def screen_candidate(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    contents = await resume.read()
    resume_text = extract_text_from_pdf(contents)
    result = evaluate_candidate(resume_text, job_description)
    return result