import os
import tempfile

import streamlit as st

from model.model import compute_final_score
from preprocessing.preprocessing_pipeline import build_feature_vector
from utils.file_extractor import extract_image_text, extract_pdf_text
from utils.llm_helper import generate_feedback


JOB_OPTIONS = {
    "Frontend Developer": "Looking for a frontend developer with React, JavaScript, Redux, and API integration experience",
    "Backend Developer": "Looking for backend developer with Node.js, Express, databases, and API development",
    "Data Scientist": "Looking for Python, Machine Learning, Pandas, NumPy, and data analysis experience",
    "Full Stack Developer": "Looking for MERN stack developer with React, Node.js, MongoDB and API experience",
    "Custom": "",
}


def sync_jd_from_role():
    selected_role = st.session_state.get("selected_role", "Frontend Developer")
    if selected_role != "Custom":
        st.session_state.jd_text = JOB_OPTIONS[selected_role]


def get_match_status(score):
    if score >= 70:
        return "Strong match", "status-strong"
    if score >= 50:
        return "Moderate match", "status-moderate"
    return "Weak match", "status-weak"


if "selected_role" not in st.session_state:
    st.session_state.selected_role = "Frontend Developer"
if "jd_text" not in st.session_state:
    st.session_state.jd_text = JOB_OPTIONS[st.session_state.selected_role]


st.set_page_config(page_title="Resume Matcher", layout="wide")

st.markdown(
    """
<style>
:root {
    --bg: #faf8f5;
    --surface: #ffffff;
    --text: #451a03;
    --muted: #7c5a35;
    --border: #e7dfd2;
    --primary: #b45309;
    --primary-strong: #9a4708;
}

[data-testid="stAppViewContainer"] {
    background: var(--bg);
}

.main .block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 2.25rem;
}

html, body, [class*="css"] {
    font-family: "IBM Plex Sans", "Helvetica Neue", sans-serif;
}

h1, h2, h3 {
    color: var(--text);
    font-weight: 620;
}

p, label, li, div {
    color: var(--text);
}

div[data-baseweb="select"] > div,
.stTextArea textarea,
.stFileUploader > section,
.stFileUploader > div {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    background: var(--surface) !important;
}

.stTextArea textarea:focus,
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 1px var(--primary) !important;
}

.stButton > button,
.stFormSubmitButton > button {
    border-radius: 8px !important;
    border: 1px solid var(--primary) !important;
    background: var(--primary) !important;
    color: #fff !important;
    font-weight: 620 !important;
    height: 42px !important;
    transition: background-color 0.15s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: var(--primary-strong) !important;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
}

.metric-label {
    color: var(--muted);
    font-size: 0.9rem;
    margin-bottom: 4px;
}

.metric-value {
    font-size: 1.65rem;
    line-height: 1.15;
    font-weight: 650;
    color: var(--text);
}

.status-box {
    margin-top: 10px;
    border-radius: 8px;
    padding: 10px 12px;
    font-weight: 520;
    border: 1px solid var(--border);
}

.status-strong {
    background: #ecfdf5;
    border-color: #10b981;
    color: #065f46;
}

.status-moderate {
    background: #fffbeb;
    border-color: #d97706;
    color: #92400e;
}

.status-weak {
    background: #fef2f2;
    border-color: #dc2626;
    color: #991b1b;
}

[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: 10px;
    background: var(--surface);
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("Resume Matcher")
st.write("Upload a resume, match it against a role, and review practical feedback.")

input_col, details_col = st.columns([1, 1.4], gap="large")

with input_col:
    uploaded_file = st.file_uploader(
        "Resume file",
        type=["pdf", "png", "jpg", "jpeg"],
        help="Supported formats: PDF, PNG, JPG, JPEG",
    )

with details_col:
    st.selectbox(
        "Role template",
        list(JOB_OPTIONS.keys()),
        key="selected_role",
        on_change=sync_jd_from_role,
    )
    jd = st.text_area(
        "Job description",
        key="jd_text",
        height=170,
        placeholder="Paste the target job description here.",
    )

submitted = st.button("Analyze Resume", use_container_width=True)


if submitted:
    if uploaded_file is None or not jd.strip():
        st.warning("Upload a resume and provide a job description before running analysis.")
    else:
        with st.spinner("Running analysis..."):
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            suffix = ext if ext in {".pdf", ".png", ".jpg", ".jpeg"} else ".pdf"

            temp_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_path = temp_file.name

                if suffix == ".pdf":
                    resume_text = extract_pdf_text(temp_path)
                else:
                    resume_text = extract_image_text(temp_path)

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)

            features = build_feature_vector(resume_text, jd)
            final_score, similarity, depth_gap = compute_final_score(features)

            feedback = generate_feedback(resume_text, jd, final_score)

            st.session_state.analysis = {
                "score": final_score,
                "similarity": similarity,
                "depth_gap": depth_gap,
                "resume_signals": features.get("resume_signals", []),
                "jd_signals": features.get("jd_signals", []),
                "feedback": feedback,
                "resume_preview": resume_text[:2500],
            }


analysis = st.session_state.get("analysis")
if analysis:
    st.divider()
    st.subheader("Analysis Result")

    status_text, status_class = get_match_status(analysis["score"])

    score_col, similarity_col, gap_col = st.columns(3, gap="medium")
    with score_col:
        st.markdown(
            f"""
<div class="metric-card">
  <div class="metric-label">Match score</div>
  <div class="metric-value">{analysis["score"]}%</div>
</div>
""",
            unsafe_allow_html=True,
        )
    with similarity_col:
        st.markdown(
            f"""
<div class="metric-card">
  <div class="metric-label">Similarity</div>
  <div class="metric-value">{analysis["similarity"]:.2f}</div>
</div>
""",
            unsafe_allow_html=True,
        )
    with gap_col:
        st.markdown(
            f"""
<div class="metric-card">
  <div class="metric-label">Depth gap</div>
  <div class="metric-value">{analysis["depth_gap"]}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="status-box {status_class}">{status_text}</div>',
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1, 1.25], gap="large")

    with left_col:
        st.subheader("Signal Review")

        resume_signals = sorted(set(analysis["resume_signals"]))
        if resume_signals:
            st.write("Resume signals detected:")
            for signal in resume_signals:
                st.markdown(f"- {signal}")
        else:
            st.info("No resume depth signals detected.")

        jd_signals = analysis["jd_signals"]
        if jd_signals:
            st.write("Job description signals:")
            for signal in jd_signals:
                st.markdown(f"- {signal}")
        else:
            st.info("No job description signals detected.")

    with right_col:
        st.subheader("AI Feedback")
        if isinstance(analysis["feedback"], str) and analysis["feedback"].startswith("Error:"):
            st.warning(analysis["feedback"])
        else:
            st.markdown(analysis["feedback"])

        st.caption("Skill depth meaning: basic/introductory = beginner, learning = improving, advanced = strong.")

    with st.expander("Preview extracted resume text"):
        if analysis["resume_preview"].strip():
            st.write(analysis["resume_preview"])
        else:
            st.write("No text extracted from the uploaded file.")
