# 🎯 TalentPulse — AI-Powered Candidate Screening Engine

[![CI Pipeline](https://github.com/<YOUR_GITHUB_USERNAME>/talent-pulse/actions/workflows/ci.yml/badge.svg)](https://github.com/<YOUR_GITHUB_USERNAME>/talent-pulse/actions)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-FF4B4B.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)

An enterprise-ready candidate profiling and resume evaluation system. TalentPulse extracts structured candidate data from unstructured PDF resumes, benchmarks qualifications against target job descriptions using high-throughput LLMs, and outputs objective hiring intelligence (match score, key strengths, skill deficiencies, and targeted screening questions).

---

## ⚡ Core Features

- **Automated Resume Parsing**: In-memory text extraction from raw PDF byte streams via `pypdf`.
- **Structured LLM Profiling**: Extracts candidate metadata (skills, experience duration, education) strictly mapped into typed Pydantic schemas.
- **Objective Rubric Evaluation**: Benchmarks candidates against job requirements, returning a 0–100 match score, strengths, critical gaps, and 3 gap-specific interview screening questions.
- **Resilient Model Resolution**: Dynamic LLM routing with fallback to active high-throughput inference endpoints (Groq / OpenAI API compatible).
- **Interactive Recruiter Dashboard**: Streamlit frontend for one-click candidate analysis and visual reporting.
- **Production CI/CD**: Automated GitHub Actions testing pipeline validating schemas, parser behavior, and API contract boundaries.

---

## 🏗️ System Architecture
```

+-------------------------------+
             |       Recruiter UI            |
             |     (Streamlit :8501)         |
             +---------------+---------------+
                             |
                             |  Multipart Form / REST
                             v
             +-------------------------------+
             |       TalentPulse API         |
             |      (FastAPI :8000)          |
             +---------------+---------------+
                             |
             +---------------+---------------+
             |                               |
             v                               v
     +---------------+               +---------------+
     | In-Memory PDF |               | LLM Evaluator |
     | Parser (pypdf)|               | (Groq / Llama)|
     +---------------+               +---------------+
```


## 🚀 Quickstart

### Prerequisites
- Python 3.11+
- Git
- Groq API Key (Free tier available at [console.groq.com](https://console.groq.com))

### 1. Clone & Set Up Environment

```bash
git clone [https://github.com/](https://github.com/)<YOUR_GITHUB_USERNAME>/talent-pulse.git
cd talent-pulse

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

2. Configure Environment Variables
Create a .env file in the project root:

Code snippet
```
GROQ_API_KEY=gsk_your_groq_api_key_here
```

3. Run the Services
Terminal 1 — Backend API:
```
uvicorn app.main:app --reload --port 8000
```

Terminal 2 — Dashboard:
```
streamlit run dashboard/app.py --server.port 8501
```

🧪 Running Tests

```
pytest tests/ -v
```
