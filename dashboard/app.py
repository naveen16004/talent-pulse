import streamlit as st
import requests

st.set_page_config(
    page_title="TalentPulse | Candidate Intelligence",
    page_icon="🎯",
    layout="wide"
)

# Custom header styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #e9ecef;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 TalentPulse: AI Candidate Screening Engine")
st.caption("Automated parsing, structured rubric matching, and gap analysis for technical hiring.")

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.subheader("1. Submission Details")
    uploaded_file = st.file_uploader("Upload Candidate Resume (PDF only)", type=["pdf"])
    
    jd_input = st.text_area(
        "Job Description & Role Requirements",
        height=260,
        placeholder="Paste role description here (e.g., Senior Backend Engineer: Python, FastAPI, Docker, PostgreSQL, 4+ years exp)..."
    )

    api_endpoint = st.text_input(
        "API Gateway URL",
        value="http://localhost:8000/api/v1/screen",
        help="Target backend address for evaluation requests"
    )

    evaluate_btn = st.button("Evaluate Candidate", type="primary", use_container_width=True)

with right_col:
    st.subheader("2. Intelligence Report")

    if evaluate_btn:
        if not uploaded_file:
            st.error("Please provide a resume PDF.")
        elif not jd_input.strip():
            st.error("Please provide a job description.")
        else:
            with st.spinner("Extracting candidate data and running rubric analysis..."):
                try:
                    files = {
                        "resume": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
                    }
                    data = {"job_description": jd_input}

                    response = requests.post(api_endpoint, files=files, data=data, timeout=60)

                    if response.status_code == 200:
                        payload = response.json()
                        cand = payload["candidate"]
                        eval_rep = payload["evaluation"]

                        # Top-level indicators
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Match Score", f"{eval_rep['match_score']}/100")
                        m2.metric("Recommendation", eval_rep["recommendation"])
                        m3.metric("Experience", f"{cand['total_experience_years']} yrs")

                        # Summary
                        st.info(f"**Executive Summary:** {eval_rep['reasoning']}")

                        # Candidate parsed profile
                        with st.expander("👤 Extracted Profile Info", expanded=False):
                            st.write(f"**Name:** {cand.get('full_name') or 'N/A'}")
                            st.write(f"**Email:** {cand.get('email') or 'N/A'}")
                            st.write(f"**Education:** {', '.join(cand['education']) if cand['education'] else 'N/A'}")
                            st.write(f"**Primary Skills:** {', '.join(cand['primary_skills']) if cand['primary_skills'] else 'N/A'}")

                        st.markdown("---")

                        # Strengths & Gaps
                        col_str, col_gap = st.columns(2)
                        with col_str:
                            st.markdown("#### ✅ Key Strengths")
                            for s in eval_rep["key_strengths"]:
                                st.success(s)

                        with col_gap:
                            st.markdown("#### ⚠️ Missing / Gaps")
                            for g in eval_rep["critical_gaps"]:
                                st.warning(g)

                        # Questions
                        st.markdown("#### 💡 Screening Questions")
                        for q in eval_rep["interview_questions"]:
                            st.markdown(f"- {q}")

                    else:
                        st.error(f"Backend returned error {response.status_code}: {response.text}")

                except requests.exceptions.ConnectionError:
                    st.error("Could not reach the FastAPI server. Make sure it is running on http://localhost:8000.")
                except Exception as ex:
                    st.error(f"Evaluation error: {str(ex)}")
    else:
        st.info("Upload a PDF resume and paste a job description on the left to generate an analysis.")