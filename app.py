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


st.set_page_config(
    page_title="Resume Matcher", layout="wide", initial_sidebar_state="expanded"
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #0f172a;            /* Slate 900 */
    --surface: #1e293b;       /* Slate 800 */
    --text: #f8fafc;          /* Slate 50 */
    --muted: #94a3b8;         /* Slate 400 */
    --border: #334155;        /* Slate 700 */
    --primary: #6366f1;       /* Indigo 500 */
    --primary-hover: #818cf8; /* Indigo 400 */
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.5);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4), 0 2px 4px -2px rgb(0 0 0 / 0.4);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.4), 0 4px 6px -4px rgb(0 0 0 / 0.4);
    --radius-md: 12px;
    --radius-lg: 16px;
}

[data-testid="stAppViewContainer"] {
    background-color: var(--bg);
}

/* Hide Streamlit UI Elements */
[data-testid="stHeader"],
[data-testid="stToolbar"],
#MainMenu {
    display: none !important;
    visibility: hidden !important;
}

.main .block-container {
    max-width: 1200px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

html, body, [class*="css"], .stMarkdown {
    font-family: 'Inter', sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--text) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

p, label, li, div {
    color: var(--text);
}

/* Inputs, Textareas, Selectboxes */
div[data-baseweb="select"] > div,
.stTextArea textarea,
.stTextInput input,
.stFileUploader > section,
.stFileUploader > div {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    background: var(--surface) !important;
    box-shadow: var(--shadow-sm);
    transition: all 0.2s ease-in-out;
}

.stTextArea textarea:focus,
.stTextInput input:focus,
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
}

/* Dropdown Menu Fix */
div[data-baseweb="popover"] > div,
ul[role="listbox"],
[data-baseweb="menu"] {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-md) !important;
}

ul[role="listbox"] li {
    color: var(--text) !important;
    transition: background-color 0.1s ease;
}

ul[role="listbox"] li:hover,
ul[role="listbox"] li[aria-selected="true"] {
    background-color: rgba(99, 102, 241, 0.15) !important;
    color: var(--primary) !important;
}

/* Main Action Buttons (Exclude Secondary/File Uploader Buttons) */
.stButton > button:not([data-testid="stBaseButton-secondary"]),
.stFormSubmitButton > button {
    border-radius: var(--radius-md) !important;
    border: none !important;
    background: linear-gradient(135deg, var(--primary), #818cf8) !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.5rem 1.5rem !important;
    min-height: 48px !important;
    box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39) !important;
    transition: all 0.3s ease !important;
    transform: translateY(0);
}

.stButton > button:not([data-testid="stBaseButton-secondary"]):hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, var(--primary-hover), var(--primary)) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.23) !important;
    transform: translateY(-2px) !important;
    color: #ffffff !important;
}

.stButton > button:not([data-testid="stBaseButton-secondary"]):active {
    transform: translateY(0) !important;
}

/* File Uploader Button & Secondary Buttons */
[data-testid="stFileUploader"] button,
[data-testid="stBaseButton-secondary"] {
    background: var(--border) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    transform: none !important;
    padding: 0.25rem 0.75rem !important;
    min-height: auto !important;
}

[data-testid="stFileUploader"] button:hover,
[data-testid="stBaseButton-secondary"]:hover {
    border-color: var(--primary) !important;
    color: var(--primary) !important;
    background: transparent !important;
    box-shadow: none !important;
    transform: none !important;
}

/* Metric Cards */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: var(--shadow-md);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--primary);
    border-top-left-radius: var(--radius-lg);
    border-bottom-left-radius: var(--radius-lg);
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.metric-label {
    color: var(--muted);
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 2.5rem;
    line-height: 1.2;
    font-weight: 700;
    color: var(--text);
}

/* Status Badges */
.status-box {
    display: inline-block;
    border-radius: 9999px; /* Pill shape */
    padding: 6px 16px;
    font-weight: 600;
    font-size: 0.875rem;
    border: 1px solid transparent;
    box-shadow: var(--shadow-sm);
    text-align: center;
}

.status-strong {
    background-color: rgba(16, 185, 129, 0.15); /* Soft glowing emerald */
    border-color: rgba(16, 185, 129, 0.3);
    color: #34d399;
}

.status-moderate {
    background-color: rgba(245, 158, 11, 0.15); /* Soft glowing amber */
    border-color: rgba(245, 158, 11, 0.3);
    color: #fbbf24;
}

.status-weak {
    background-color: rgba(239, 68, 68, 0.15); /* Soft glowing red */
    border-color: rgba(239, 68, 68, 0.3);
    color: #f87171;
}

/* Expander */
[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    background: var(--surface);
    box-shadow: var(--shadow-sm);
}
[data-testid="stExpander"] summary {
    font-weight: 600;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding-top: 2rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}

/* File Uploader Dropzone polish */
[data-testid="stFileUploadDropzone"] {
    border: 2px dashed #475569 !important;
    border-radius: var(--radius-lg) !important;
    background-color: var(--bg) !important;
    padding: 2rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: var(--primary) !important;
    background-color: var(--surface) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("✨ Resume Matcher")
st.markdown(
    "<p style='font-size: 1.1rem; color: #64748b; margin-bottom: 2rem;'>Upload a resume, match it against a role, and review practical AI-powered feedback.</p>",
    unsafe_allow_html=True,
)

# Move Inputs to Sidebar for a Professional Dashboard Feel
with st.sidebar:
    st.header("🎯 Target Role")
    st.selectbox(
        "Select a template or custom role",
        list(JOB_OPTIONS.keys()),
        key="selected_role",
        on_change=sync_jd_from_role,
    )
    jd = st.text_area(
        "Job description",
        key="jd_text",
        height=300,
        placeholder="Paste the target job description here...",
        help="The AI will compare the resume against this description.",
    )
    st.markdown("---")
    st.markdown(
        "💡 **Tip**: Be as specific as possible in the job description to get the most accurate match score."
    )


# Main Content Area
st.subheader("📄 Document Upload")
uploaded_file = st.file_uploader(
    "Upload candidate resume",
    type=["pdf", "png", "jpg", "jpeg"],
    help="Supported formats: PDF, PNG, JPG, JPEG",
)

st.markdown("<br>", unsafe_allow_html=True)

submitted = st.button("Run AI Analysis", use_container_width=True)


if submitted:
    if uploaded_file is None or not jd.strip():
        st.warning(
            "⚠️ Please upload a resume and ensure the job description is provided in the sidebar."
        )
    else:
        with st.spinner("🤖 Analyzing resume against job description..."):
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
    st.markdown("<br><hr>", unsafe_allow_html=True)

    st.markdown("## 📊 Analysis Dashboard")

    status_text, status_class = get_match_status(analysis["score"])

    # Metrics Row
    score_col, similarity_col, gap_col = st.columns(3, gap="large")
    with score_col:
        st.markdown(
            f"""
<div class="metric-card">
  <div class="metric-label">Overall Match</div>
  <div class="metric-value">{analysis["score"]}%</div>
  <div class="status-box {status_class}" style="margin-top: 16px;">{status_text}</div>
</div>
""",
            unsafe_allow_html=True,
        )
    with similarity_col:
        st.markdown(
            f"""
<div class="metric-card">
  <div class="metric-label">Semantic Similarity</div>
  <div class="metric-value">{analysis["similarity"]:.2f}</div>
</div>
""",
            unsafe_allow_html=True,
        )
    with gap_col:
        st.markdown(
            f"""
<div class="metric-card">
  <div class="metric-label">Depth Gap</div>
  <div class="metric-value">{analysis["depth_gap"]}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Content Row
    feedback_col, signals_col = st.columns([1.5, 1], gap="large")

    with feedback_col:
        st.markdown("### 🧠 AI Feedback")
        st.info(
            "Skill depth meaning: basic/introductory = beginner, learning = improving, advanced = strong.",
            icon="ℹ️",
        )

        with st.container(border=True):
            if isinstance(analysis["feedback"], str) and analysis["feedback"].startswith(
                "Error:"
            ):
                st.error(analysis["feedback"])
            else:
                st.markdown(analysis["feedback"])

        with st.expander("🔍 Preview Extracted Resume Text"):
            if analysis["resume_preview"].strip():
                st.write(analysis["resume_preview"])
            else:
                st.write("No text extracted from the uploaded file.")

    with signals_col:
        st.markdown("### 📡 Signal Review")

        with st.container(border=True):
            st.markdown("#### Resume Signals")
            resume_signals = sorted(set(analysis["resume_signals"]))
            if resume_signals:
                for signal in resume_signals:
                    st.markdown(f"✅ `{signal}`")
            else:
                st.warning("No resume depth signals detected.")

            st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

            st.markdown("#### Job Description Signals")
            jd_signals = analysis["jd_signals"]
            if jd_signals:
                for signal in jd_signals:
                    st.markdown(f"🎯 `{signal}`")
            else:
                st.warning("No job description signals detected.")