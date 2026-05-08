import os
import sys
import json
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs):
        return False

load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT / "react_app" / ".env")

from model.model import compute_final_score
from preprocessing.preprocessing_pipeline import build_feature_vector
from utils.file_extractor import extract_image_text, extract_pdf_text
from utils.llm_helper import generate_feedback, chat_with_groq

JOB_OPTIONS = {
    "Frontend Developer": "Looking for a frontend developer with React, JavaScript, Redux, and API integration experience",
    "Backend Developer": "Looking for backend developer with Node.js, Express, databases, and API development",
    "Data Scientist": "Looking for Python, Machine Learning, Pandas, NumPy, and data analysis experience",
    "Full Stack Developer": "Looking for MERN stack developer with React, Node.js, MongoDB and API experience",
    "Custom": "",
}

SUPPORTED_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg"}

RESOURCE_TOOLS = {
    "resume-checklist": {
        "env": "GROQ_RESUME_CHECKLIST_KEY",
        "title": "Resume checklist",
        "instruction": (
            "Create a practical resume checklist from the analysis. Focus on concrete resume edits, "
            "missing evidence, keyword alignment, metrics, formatting, and what to rewrite first."
        ),
    },
    "skill-gap-map": {
        "env": "GROQ_SKILL_GAP_MAP_KEY",
        "title": "Skill gap map",
        "instruction": (
            "Map the candidate's gaps into skill groups. Identify what is present, what is weak or missing, "
            "priority level, and the fastest practice path for each gap."
        ),
    },
    "project-prompts": {
        "env": "GROQ_PROJECT_PROMPTS_KEY",
        "title": "Project prompts",
        "instruction": (
            "Generate project ideas that prove the missing skills. Each project should include goal, stack, "
            "features, proof points, and resume bullets the candidate can write after building it."
        ),
    },
    "interview-prep": {
        "env": "GROQ_INTERVIEW_PREP_KEY",
        "title": "Interview prep",
        "instruction": (
            "Convert the analysis into interview preparation. Include likely questions, strong talking points, "
            "gap explanations, STAR-style answer outlines, and a short practice plan."
        ),
    },
}

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


class ResourceRequest(BaseModel):
    analysis: dict
    job_description: str | None = None
    role_template: str | None = None


def call_groq(resource_id, payload):
    tool = RESOURCE_TOOLS.get(resource_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Resource tool not found.")

    api_key = os.getenv(tool["env"], "").strip()
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail=f"Missing {tool['env']} in .env. Add it locally before running this resource.",
        )

    analysis = payload.analysis or {}
    prompt = f"""
You are powering the "{tool['title']}" page in a resume analysis app.

Task:
{tool['instruction']}

Use this latest analysis as the only source of truth:
Role template: {payload.role_template or analysis.get("role_template") or "Unknown"}
Match score: {analysis.get("score")}
Match status: {analysis.get("status")}
Semantic similarity: {analysis.get("similarity")}
Depth gap: {analysis.get("depth_gap")}
Resume signals: {analysis.get("resume_signals")}
Job description signals: {analysis.get("jd_signals")}
Resume preview:
{analysis.get("resume_preview", "")}

API feedback:
{analysis.get("feedback", "")}

Job description:
{payload.job_description or ""}

Return valid JSON only, no markdown fences, with this shape:
{{
  "summary": "one concise overview sentence",
  "sections": [
    {{
      "title": "section title",
      "items": [
        {{
          "label": "short label",
          "detail": "specific recommendation",
          "priority": "High|Medium|Low"
        }}
      ]
    }}
  ],
  "next_steps": ["short action", "short action", "short action"]
}}
""".strip()

    body = {
        "model": os.getenv("GROQ_RESOURCE_MODEL", "llama-3.3-70b-versatile"),
        "messages": [
            {"role": "system", "content": "Return concise, structured, valid JSON for a resume improvement UI."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.35,
        "response_format": {"type": "json_object"},
    }

    request = Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise HTTPException(status_code=error.code, detail=f"Groq request failed: {detail}") from error
    except URLError as error:
        raise HTTPException(status_code=502, detail=f"Groq request failed: {error.reason}") from error
    except TimeoutError as error:
        raise HTTPException(status_code=504, detail="Groq request timed out.") from error

    content = data.get("choices", [{}])[0].get("message", {}).get("content", "{}")
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {
            "summary": "The model returned a text response instead of structured JSON.",
            "sections": [
                {
                    "title": tool["title"],
                    "items": [{"label": "Raw response", "detail": content, "priority": "Medium"}],
                }
            ],
            "next_steps": ["Review the raw response", "Re-run the resource if needed"],
        }

    return {
        "resource": tool["title"],
        "result": parsed,
    }


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/roles")
def roles():
    return {"roles": JOB_OPTIONS}


@app.post("/api/resources/{resource_id}")
def generate_resource(resource_id: str, payload: ResourceRequest):
    return call_groq(resource_id, payload)


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
            "resume_text": (resume_text or "")[:12000],
        }
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


class ChatRequest(BaseModel):
    resume_text: str
    job_description: str
    messages: List[Dict[str, str]]

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    try:
        messages = []
        for msg in (req.messages or [])[-12:]:
            role = msg.get("role")
            content = str(msg.get("content", "")).strip()
            if role in {"user", "assistant"} and content:
                messages.append({"role": role, "content": content})
        if not req.resume_text.strip():
            raise HTTPException(status_code=400, detail="Resume text is required for chat.")
        if not messages:
            raise HTTPException(status_code=400, detail="Add at least one chat message.")

        reply = chat_with_groq(req.resume_text, req.job_description, messages)
        return {"reply": reply}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
