import os
import tempfile
from html import escape

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


def render_signal_pills(signals):
    unique_signals = sorted(set(signals))
    if not unique_signals:
        return '<p class="empty-copy">No depth signals detected.</p>'

    pills = "".join(
        f'<span class="signal-pill">{escape(str(signal))}</span>'
        for signal in unique_signals
    )
    return f'<div class="signal-list">{pills}</div>'


if "selected_role" not in st.session_state:
    st.session_state.selected_role = "Frontend Developer"
if "jd_text" not in st.session_state:
    st.session_state.jd_text = JOB_OPTIONS[st.session_state.selected_role]


st.set_page_config(
    page_title="Resume Matcher", layout="wide", initial_sidebar_state="collapsed"
)

st.markdown(
    """
<style>
:root {
    --ink: #08040e;
    --night: #0b0611;
    --panel: rgba(255, 255, 255, 0.075);
    --panel-strong: rgba(255, 255, 255, 0.12);
    --line: rgba(255, 255, 255, 0.14);
    --text: #ffffff;
    --muted: #bcb4c7;
    --paper: #fbfafc;
    --paper-text: #100b17;
    --paper-muted: #665f6d;
    --purple: #9b2cff;
    --purple-soft: #eadcf8;
    --purple-deep: #35134d;
    --success: #72d79b;
    --warning: #e7bd67;
    --danger: #ff7777;
    --radius: 14px;
    --font: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
}

html {
    scroll-behavior: smooth;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 72% 22%, rgba(155, 44, 255, 0.24), transparent 28%),
        radial-gradient(circle at 28% 8%, rgba(118, 62, 180, 0.16), transparent 24%),
        linear-gradient(180deg, #0a0610 0%, #0a0610 100%);
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu {
    display: none !important;
    visibility: hidden !important;
}

.main .block-container {
    max-width: 1280px;
    padding: 0 44px 64px;
}

html,
body,
[class*="css"],
.stMarkdown {
    font-family: var(--font) !important;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: inherit !important;
    letter-spacing: 0;
}

p,
label,
li,
div {
    color: inherit;
}

.site-nav {
    align-items: center;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 24px;
    padding: 34px 0 70px;
}

a.brand {
    align-items: center;
    color: var(--text) !important;
    display: flex;
    gap: 12px;
    font-size: 22px;
    font-weight: 760;
    text-decoration: none !important;
}

a.brand:visited,
a.brand:hover {
    color: var(--text) !important;
    text-decoration: none !important;
}

div[data-testid="stMarkdownContainer"] a.brand,
div[data-testid="stMarkdownContainer"] a.hero-cta,
div[data-testid="stMarkdownContainer"] a.nav-button,
div[data-testid="stMarkdownContainer"] a.chip-link,
div[data-testid="stMarkdownContainer"] a.feature-link,
div[data-testid="stMarkdownContainer"] .nav-links a {
    text-decoration: none !important;
}

div[data-testid="stMarkdownContainer"] a.brand {
    color: var(--text) !important;
}

div[data-testid="stMarkdownContainer"] a.hero-cta {
    color: #0f0716 !important;
}

.brand-mark {
    color: var(--purple);
    font-size: 34px;
    font-weight: 850;
    line-height: 1;
}

.nav-links {
    align-items: center;
    display: flex;
    gap: 56px;
}

.nav-links a,
.nav-actions a,
.hero-cta,
.chip-link,
.feature-link {
    text-decoration: none !important;
}

.nav-links a {
    color: rgba(255, 255, 255, 0.64) !important;
    font-size: 16px;
    font-weight: 560;
}

.nav-links a:hover {
    color: #ffffff !important;
}

.nav-actions {
    align-items: center;
    display: flex;
    gap: 16px;
    justify-content: flex-end;
}

.nav-button {
    align-items: center;
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 999px;
    color: #ffffff !important;
    display: inline-flex;
    font-size: 15px;
    font-weight: 680;
    min-height: 46px;
    padding: 0 24px;
}

.nav-button:hover {
    background: rgba(255, 255, 255, 0.08);
}

.nav-button.light {
    background: #ffffff;
    border-color: rgba(255, 255, 255, 0.45);
    color: #13091d !important;
    gap: 14px;
    padding-right: 8px;
}

.arrow-dot {
    align-items: center;
    background: var(--purple);
    border-radius: 999px;
    color: #ffffff;
    display: inline-flex;
    font-size: 24px;
    height: 38px;
    justify-content: center;
    line-height: 1;
    width: 38px;
}

.hero {
    min-height: 780px;
    position: relative;
}

.hero-grid {
    display: grid;
    gap: 42px;
    grid-template-columns: minmax(0, 0.96fr) minmax(360px, 0.74fr);
}

.hero-title {
    color: var(--text);
    font-size: clamp(58px, 6.3vw, 104px);
    font-weight: 760;
    letter-spacing: 0;
    line-height: 1.05;
    margin: 0 0 28px;
    max-width: 790px;
}

.hero-title span {
    color: #ead7ff;
}

.hero-copy {
    color: rgba(255, 255, 255, 0.68);
    font-size: 19px;
    line-height: 1.55;
    margin: 0 0 38px;
    max-width: 620px;
}

.hero-cta {
    align-items: center;
    background: #ffffff;
    border: 8px solid rgba(255, 255, 255, 0.12);
    border-radius: 999px;
    color: #0f0716 !important;
    display: inline-flex;
    font-size: 18px;
    font-weight: 760;
    gap: 18px;
    padding: 8px 10px 8px 26px;
}

.hero-cta:hover {
    box-shadow: 0 0 44px rgba(155, 44, 255, 0.32);
}

.floating-chips {
    min-height: 500px;
    position: relative;
}

.chip-link {
    align-items: center;
    backdrop-filter: blur(18px);
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 999px;
    color: rgba(255, 255, 255, 0.72) !important;
    display: inline-flex;
    font-size: 16px;
    font-weight: 620;
    gap: 12px;
    padding: 15px 22px;
    position: absolute;
    box-shadow: 0 18px 52px rgba(155, 44, 255, 0.12);
    transform: translate3d(0, 0, 0);
    white-space: nowrap;
}

.chip-link:hover {
    background: rgba(255, 255, 255, 0.12);
    color: #ffffff !important;
}

.chip-link span {
    color: var(--purple);
    font-size: 22px;
}

.chip-1 {
    right: 118px;
    top: 38px;
}

.chip-2 {
    right: 0;
    top: 184px;
}

.chip-3 {
    right: 190px;
    top: 318px;
}

.hero-art {
    bottom: -44px;
    max-width: 560px;
    opacity: 0.86;
    position: absolute;
    right: 0;
    width: 42vw;
}

.matcher-shell {
    background:
        linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.035)),
        rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 26px;
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.24);
    color: var(--text);
    margin: 0 -44px;
    padding: 56px 44px 28px;
}

.section-kicker {
    background: #ffffff;
    border: 1px solid #eadcf8;
    border-radius: 999px;
    color: #7d3fba;
    display: inline-flex;
    font-size: 15px;
    font-weight: 720;
    margin: 0 auto 18px;
    padding: 10px 18px;
}

.section-heading {
    color: var(--text);
    font-size: clamp(36px, 4vw, 64px);
    font-weight: 760;
    line-height: 1.08;
    margin: 0 auto 16px;
    max-width: 900px;
    text-align: center;
}

.section-heading span {
    color: #ead7ff;
}

.section-copy {
    color: rgba(255,255,255,0.68);
    font-size: 18px;
    line-height: 1.5;
    margin: 0 auto 36px;
    max-width: 650px;
    text-align: center;
}

.matcher-header {
    align-items: center;
    display: flex;
    flex-direction: column;
    margin: 0 auto 24px;
    max-width: 880px;
    text-align: center;
}

.panel-heading {
    color: var(--text);
    font-size: 21px;
    font-weight: 760;
    margin: 0 0 10px;
}

.panel-note {
    color: rgba(255,255,255,0.66);
    font-size: 15px;
    line-height: 1.5;
    margin: 0 0 18px;
}

div[data-baseweb="select"] > div,
.stTextArea textarea,
.stTextInput input,
.stFileUploader > section,
.stFileUploader > div {
    background: #ffffff !important;
    border: 1px solid #e5dbea !important;
    border-radius: var(--radius) !important;
    box-shadow: 0 20px 60px rgba(42, 24, 58, 0.08) !important;
    color: var(--paper-text) !important;
}

.stTextArea textarea:focus,
.stTextInput input:focus,
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--purple) !important;
    box-shadow: 0 0 0 3px rgba(155, 44, 255, 0.14) !important;
}

.stTextArea textarea,
.stTextInput input {
    color: var(--paper-text) !important;
}

.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #9a93a0 !important;
}

div[data-baseweb="popover"] > div,
ul[role="listbox"],
[data-baseweb="menu"] {
    background-color: #ffffff !important;
    border: 1px solid #e5dbea !important;
    border-radius: var(--radius) !important;
    box-shadow: 0 18px 48px rgba(42, 24, 58, 0.16) !important;
}

ul[role="listbox"] li {
    color: var(--paper-text) !important;
}

ul[role="listbox"] li:hover,
ul[role="listbox"] li[aria-selected="true"] {
    background-color: #f3e9ff !important;
    color: #6c24a8 !important;
}

.stButton > button:not([data-testid="stBaseButton-secondary"]),
.stFormSubmitButton > button {
    background: #111111 !important;
    border: 1px solid #111111 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: 720 !important;
    min-height: 52px !important;
    transition: background-color 150ms ease, border-color 150ms ease !important;
}

.stButton > button:not([data-testid="stBaseButton-secondary"]):hover,
.stFormSubmitButton > button:hover {
    background: var(--purple) !important;
    border-color: var(--purple) !important;
    color: #ffffff !important;
}

[data-testid="stFileUploader"] button,
[data-testid="stBaseButton-secondary"] {
    background: #f4eef7 !important;
    border: 1px solid #e5dbea !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    color: #4b4053 !important;
    font-weight: 650 !important;
}

[data-testid="stFileUploader"] button:hover,
[data-testid="stBaseButton-secondary"]:hover {
    background: #eadcf8 !important;
    border-color: #d9c2ec !important;
    color: #6c24a8 !important;
}

[data-testid="stFileUploadDropzone"] {
    background: #ffffff !important;
    border: 1px dashed #cfc0d9 !important;
    border-radius: var(--radius) !important;
    min-height: 164px;
    padding: 2rem !important;
}

[data-testid="stFileUploadDropzone"]:hover {
    background: #fbf7ff !important;
    border-color: var(--purple) !important;
}

.results-title {
    color: var(--text);
    font-size: 30px;
    font-weight: 780;
    margin: 54px 0 18px;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #eadcf8;
    border-radius: 18px;
    box-shadow: 0 18px 56px rgba(48, 30, 64, 0.1);
    min-height: 148px;
    padding: 26px 28px;
}

.metric-label {
    color: #7b7283;
    font-size: 14px;
    margin-bottom: 14px;
}

.metric-value {
    color: var(--paper-text);
    font-size: 46px;
    font-weight: 780;
    line-height: 1;
}

.status-box {
    border-radius: 8px;
    display: inline-block;
    font-size: 13px;
    font-weight: 720;
    margin-top: 18px;
    padding: 8px 11px;
}

.status-strong {
    background: rgba(114, 215, 155, 0.14);
    border: 1px solid rgba(114, 215, 155, 0.34);
    color: #187345;
}

.status-moderate {
    background: rgba(231, 189, 103, 0.16);
    border: 1px solid rgba(231, 189, 103, 0.36);
    color: #8c5e09;
}

.status-weak {
    background: rgba(255, 119, 119, 0.14);
    border: 1px solid rgba(255, 119, 119, 0.32);
    color: #a92a2a;
}

.empty-copy {
    color: var(--paper-muted);
    font-size: 14px;
    margin: 8px 0 0;
}

.signal-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}

.signal-pill {
    background: #f4eef7;
    border: 1px solid #e7d9ef;
    border-radius: 8px;
    color: #4d275f;
    font-size: 13px;
    padding: 7px 9px;
}

[data-testid="stExpander"] {
    background: #ffffff;
    border: 1px solid #eadcf8;
    border-radius: 14px;
    box-shadow: none;
}

[data-testid="stExpander"] summary {
    color: var(--paper-text);
    font-weight: 650;
}

.stAlert {
    background: #ffffff !important;
    border: 1px solid #eadcf8 !important;
    border-radius: 14px !important;
}

.feature-band {
    background: var(--paper);
    color: var(--paper-text);
    margin: 0 -44px;
    padding: 48px 44px 72px;
}

.feature-band > div:first-child {
    align-items: center;
    display: flex;
    flex-direction: column;
    text-align: center;
}

.feature-band .section-heading {
    color: var(--paper-text);
}

.feature-band .section-heading span {
    color: #7f3eb2;
}

.feature-band .section-copy {
    color: var(--paper-muted);
    max-width: 760px;
}

.feature-grid {
    display: grid;
    gap: 22px;
    grid-template-columns: repeat(3, minmax(0, 1fr));
}

.feature-card {
    background: #ffffff;
    border: 1px solid #eee5f4;
    border-radius: 18px;
    box-shadow: 0 18px 56px rgba(48, 30, 64, 0.09);
    min-height: 310px;
    overflow: hidden;
    padding: 28px;
}

.feature-art {
    align-items: center;
    background: linear-gradient(180deg, #fbf7ff 0%, #ffffff 100%);
    border: 1px solid #f0e7f6;
    border-radius: 14px;
    display: flex;
    height: 126px;
    justify-content: center;
    margin-bottom: 26px;
}

.feature-card h3 {
    color: var(--paper-text) !important;
    font-size: 24px;
    margin: 0 0 12px;
}

.feature-card p {
    color: var(--paper-muted);
    font-size: 16px;
    line-height: 1.48;
    margin: 0;
}

.feature-link {
    color: #7b33b6;
}

.how-band {
    background: #09050d;
    color: #ffffff;
    margin: 0 -44px -64px;
    padding: 76px 44px 86px;
}

.how-grid {
    align-items: center;
    display: grid;
    gap: 48px;
    grid-template-columns: 0.95fr 1.05fr;
}

.how-title {
    font-size: clamp(42px, 5vw, 78px);
    font-weight: 760;
    line-height: 1.05;
    margin: 0 0 20px;
}

.how-title span {
    color: #ead7ff;
}

.how-copy {
    color: rgba(255,255,255,0.66);
    font-size: 18px;
    line-height: 1.55;
    margin: 0;
    max-width: 620px;
}

.step-card {
    backdrop-filter: blur(16px);
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    margin-bottom: 16px;
    padding: 22px 24px;
}

.step-card strong {
    color: #ffffff;
    display: block;
    font-size: 18px;
    margin-bottom: 8px;
}

.step-card span {
    color: rgba(255,255,255,0.65);
    display: block;
    font-size: 15px;
    line-height: 1.48;
}

.contact-card {
    background: #ffffff;
    border: 1px solid #eadcf8;
    border-radius: 18px;
    color: var(--paper-text);
    margin-top: 24px;
    padding: 24px 26px;
}

@media (max-width: 940px) {
    .main .block-container {
        padding: 0 18px 44px;
    }

    .site-nav,
    .hero-grid,
    .feature-grid,
    .how-grid {
        grid-template-columns: 1fr;
    }

    .site-nav {
        gap: 22px;
        padding-bottom: 42px;
    }

    .nav-links,
    .nav-actions {
        justify-content: flex-start;
        flex-wrap: wrap;
        gap: 14px;
    }

    .floating-chips {
        min-height: auto;
    }

    .chip-link {
        position: static;
        margin: 0 10px 12px 0;
    }

    .hero-art {
        margin-top: 12px;
        position: static;
        width: 100%;
    }

    .matcher-shell,
    .feature-band,
    .how-band {
        margin-left: -18px;
        margin-right: -18px;
        padding-left: 18px;
        padding-right: 18px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero" id="intro">
  <nav class="site-nav" aria-label="Main navigation">
    <a class="brand" href="#intro" style="color:#ffffff !important; text-decoration:none !important;"><span class="brand-mark">V</span><span>Resume AI</span></a>
    <div class="nav-links">
      <a href="#matcher">Analyzer</a>
      <a href="#features">Features</a>
      <a href="#how-it-works">How it works</a>
    </div>
    <div class="nav-actions">
      <a class="nav-button" href="#contact" style="text-decoration:none !important;">Contact us</a>
      <a class="nav-button light" href="#matcher" style="text-decoration:none !important;">Start <span class="arrow-dot">-></span></a>
    </div>
  </nav>
  <div class="hero-grid">
    <div>
      <h1 class="hero-title">Stop guessing. Start matching <span>resumes.</span></h1>
      <p class="hero-copy">
        Compare a candidate resume with a target job description using local ML scoring,
        then review concise AI feedback for gaps, signals, and next steps.
      </p>
      <a class="hero-cta" href="#matcher" style="color:#0f0716 !important; text-decoration:none !important;">Try it now <span class="arrow-dot">-></span></a>
    </div>
    <div class="floating-chips">
      <a class="chip-link chip-1" href="#features" style="text-decoration:none !important;"><span>*</span> Local score, API feedback</a>
      <a class="chip-link chip-2" href="#matcher" style="text-decoration:none !important;"><span>v</span> PDF and image resume upload</a>
      <a class="chip-link chip-3" href="#how-it-works" style="text-decoration:none !important;"><span>^</span> Skill-depth signal review</a>
      <svg class="hero-art" viewBox="0 0 560 430" role="img" aria-label="Resume analysis illustration">
        <defs>
          <linearGradient id="portal" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0" stop-color="#ffffff" stop-opacity="0.9"/>
            <stop offset="1" stop-color="#9b2cff" stop-opacity="0.18"/>
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="8" result="blur"/>
            <feMerge>
              <feMergeNode in="blur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        <path d="M70 342 C142 280 199 312 264 348 C344 391 427 378 520 314" fill="none" stroke="#9b2cff" stroke-width="24" stroke-linecap="round" opacity="0.5" filter="url(#glow)"/>
        <rect x="92" y="88" width="160" height="210" rx="34" fill="rgba(255,255,255,0.09)" stroke="rgba(255,255,255,0.25)"/>
        <rect x="126" y="124" width="92" height="128" rx="18" fill="url(#portal)" opacity="0.9"/>
        <rect x="160" y="270" width="76" height="74" rx="12" fill="rgba(255,255,255,0.22)" stroke="rgba(255,255,255,0.34)"/>
        <path d="M181 306 L196 321 L222 290" fill="none" stroke="#e8b6ff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="338" cy="184" r="35" fill="rgba(255,255,255,0.72)"/>
        <path d="M302 270 C307 230 368 230 374 270 C360 286 319 286 302 270 Z" fill="rgba(255,255,255,0.62)"/>
        <circle cx="458" cy="152" r="32" fill="rgba(255,255,255,0.55)"/>
        <path d="M424 236 C430 199 486 199 492 236 C478 251 440 251 424 236 Z" fill="rgba(255,255,255,0.42)"/>
      </svg>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<section class="matcher-shell" id="matcher">
  <div class="matcher-header">
    <div class="section-kicker">Resume analyzer</div>
    <h2 class="section-heading">Run the actual match here.</h2>
    <p class="section-copy">
      This is the main workflow: upload the resume, choose or paste the role, and run the local ML scorer.
    </p>
  </div>
</section>
""",
    unsafe_allow_html=True,
)

job_col, upload_col = st.columns([0.95, 1.05], gap="large")

with job_col:
    st.markdown(
        """
<div class="panel-heading">Target role</div>
<p class="panel-note">Choose a starter role or paste the exact job description you want to compare against.</p>
""",
        unsafe_allow_html=True,
    )
    st.selectbox(
        "Role template",
        list(JOB_OPTIONS.keys()),
        key="selected_role",
        on_change=sync_jd_from_role,
    )
    jd = st.text_area(
        "Job description",
        key="jd_text",
        height=248,
        placeholder="Paste the target job description here.",
    )

with upload_col:
    st.markdown(
        """
<div class="panel-heading">Candidate resume</div>
<p class="panel-note">Upload a PDF or image resume. The app extracts text locally before scoring.</p>
""",
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Resume file",
        type=["pdf", "png", "jpg", "jpeg"],
        help="Supported formats: PDF, PNG, JPG, JPEG",
    )
    submitted = st.button("Run analysis", use_container_width=True)


if submitted:
    if uploaded_file is None or not jd.strip():
        st.warning(
            "Please upload a resume and add a job description before running analysis."
        )
    else:
        with st.spinner("Analyzing resume against job description..."):
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
    st.markdown('<div class="results-title" id="results">Analysis dashboard</div>', unsafe_allow_html=True)

    status_text, status_class = get_match_status(analysis["score"])

    score_col, similarity_col, gap_col = st.columns(3, gap="large")
    with score_col:
        st.markdown(
            f"""
<div class="metric-card">
  <div class="metric-label">Overall Match</div>
  <div class="metric-value">{analysis["score"]}%</div>
  <div class="status-box {status_class}">{status_text}</div>
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
  <p class="empty-copy">TF-IDF cosine similarity</p>
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
  <p class="empty-copy">Skill depth mismatch penalty</p>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    feedback_col, signals_col = st.columns([1.5, 1], gap="large")

    with feedback_col:
        st.markdown('<div class="panel-heading">AI feedback</div>', unsafe_allow_html=True)
        st.info(
            "Skill depth meaning: basic/introductory = beginner, learning = improving, advanced = strong.",
        )

        with st.container(border=True):
            if isinstance(analysis["feedback"], str) and analysis["feedback"].startswith(
                "Error:"
            ):
                st.error(analysis["feedback"])
            else:
                st.markdown(analysis["feedback"])

        with st.expander("Preview extracted resume text"):
            if analysis["resume_preview"].strip():
                st.write(analysis["resume_preview"])
            else:
                st.write("No text extracted from the uploaded file.")

    with signals_col:
        st.markdown('<div class="panel-heading">Signal review</div>', unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("#### Resume signals")
            st.markdown(
                render_signal_pills(analysis["resume_signals"]),
                unsafe_allow_html=True,
            )

            st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

            st.markdown("#### Job description signals")
            st.markdown(
                render_signal_pills(analysis["jd_signals"]),
                unsafe_allow_html=True,
            )

st.markdown(
    """
<section class="feature-band" id="features">
  <div style="text-align:center;">
    <div class="section-kicker">Main features</div>
    <h2 class="section-heading">Power up your <span>resume review</span></h2>
    <p class="section-copy">
      The extra sections below explain what the app does without pushing the real analyzer out of the way.
    </p>
  </div>
  <div class="feature-grid">
    <a class="feature-link" href="#matcher">
      <article class="feature-card">
        <div class="feature-art">
          <svg width="170" height="90" viewBox="0 0 170 90" aria-hidden="true">
            <path d="M8 48 H58 V24 H118" fill="none" stroke="#813bb2" stroke-width="4"/>
            <path d="M58 48 V72 H142" fill="none" stroke="#d7c6e5" stroke-width="3" stroke-dasharray="7 7"/>
            <circle cx="58" cy="48" r="8" fill="#813bb2"/>
            <circle cx="118" cy="24" r="8" fill="#d7c6e5"/>
            <circle cx="142" cy="72" r="8" fill="#d7c6e5"/>
          </svg>
        </div>
        <h3>Smart matching</h3>
        <p>TF-IDF similarity compares the cleaned resume and role text locally before feedback is requested.</p>
      </article>
    </a>
    <a class="feature-link" href="#results">
      <article class="feature-card">
        <div class="feature-art">
          <svg width="170" height="90" viewBox="0 0 170 90" aria-hidden="true">
            <rect x="18" y="54" width="22" height="24" rx="5" fill="#eadcf8"/>
            <rect x="52" y="36" width="22" height="42" rx="5" fill="#9b2cff"/>
            <rect x="86" y="18" width="22" height="60" rx="5" fill="#d8b5ff"/>
            <path d="M122 64 L138 78 L158 34" fill="none" stroke="#813bb2" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h3>Score dashboard</h3>
        <p>Overall match, semantic similarity, and skill depth gap stay visible after each analysis run.</p>
      </article>
    </a>
    <a class="feature-link" href="#how-it-works">
      <article class="feature-card">
        <div class="feature-art">
          <svg width="170" height="90" viewBox="0 0 170 90" aria-hidden="true">
            <rect x="32" y="18" width="72" height="54" rx="10" fill="#eadcf8"/>
            <path d="M48 36 H88 M48 50 H76" stroke="#813bb2" stroke-width="5" stroke-linecap="round"/>
            <circle cx="124" cy="45" r="25" fill="#9b2cff" opacity="0.18"/>
            <path d="M114 46 L123 55 L140 34" fill="none" stroke="#813bb2" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h3>Signal review</h3>
        <p>Depth cues such as basic, learning, advanced, and expert are surfaced for easier interpretation.</p>
      </article>
    </a>
  </div>
  <div class="contact-card" id="contact">
    <strong>Need to tune the analysis?</strong>
    <p class="empty-copy">Use the role template and job description above to make the score more specific to the position.</p>
  </div>
</section>

<section class="how-band" id="how-it-works">
  <div class="how-grid">
    <div>
      <div class="section-kicker" style="background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.14); color: #e6cfff;">How it works</div>
      <h2 class="how-title">From upload to <span>matched signal.</span></h2>
      <p class="how-copy">
        The app keeps the important workflow local first, then uses an LLM only to explain the result in plain language.
      </p>
    </div>
    <div>
      <div class="step-card"><strong>01. Extract text</strong><span>PDF and image resumes are converted into text for analysis.</span></div>
      <div class="step-card"><strong>02. Clean and normalize</strong><span>Resume and job-description text are preprocessed into comparable feature text.</span></div>
      <div class="step-card"><strong>03. Score and explain</strong><span>The local model computes the percentage match, then API feedback explains the gaps.</span></div>
    </div>
  </div>
</section>
""",
    unsafe_allow_html=True,
)
