import os
import sys
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs):
        return False

load_dotenv(PROJECT_ROOT / ".env")

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

SUPPORTED_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg"}

app = FastAPI(title="Resume AI React API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_match_status(score):
    if score >= 70:
        return "Strong match"
    if score >= 50:
        return "Moderate match"
    return "Weak match"


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/roles")
def roles():
    return {"roles": JOB_OPTIONS}


@app.post("/api/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    jd = (job_description or "").strip()
    if not jd:
        raise HTTPException(status_code=400, detail="Job description is required.")

    suffix = Path(resume.filename or "").suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise HTTPException(
            status_code=400,
            detail="Upload a supported resume file: PDF, PNG, JPG, or JPEG.",
        )

    temp_path = None
    try:
        contents = await resume.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Uploaded resume is empty.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        if suffix == ".pdf":
            resume_text = extract_pdf_text(temp_path)
        else:
            resume_text = extract_image_text(temp_path)

        features = build_feature_vector(resume_text, jd)
        final_score, similarity, depth_gap = compute_final_score(features)
        feedback = generate_feedback(resume_text, jd, final_score)

        return {
            "score": final_score,
            "status": get_match_status(final_score),
            "similarity": round(float(similarity), 4),
            "depth_gap": depth_gap,
            "resume_signals": features.get("resume_signals", []),
            "jd_signals": features.get("jd_signals", []),
            "feedback": feedback,
            "resume_preview": (resume_text or "")[:2500],
        }
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
