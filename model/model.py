from __future__ import annotations

import math
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _safe_text(value: str | None) -> str:
    return (value or "").strip()


def _tfidf_cosine(texts: list[str], **kwargs) -> float:
    if not texts[0] and not texts[1]:
        return 0.0
    try:
        matrix = TfidfVectorizer(**kwargs).fit_transform(texts)
    except ValueError:
        return 0.0
    return float(cosine_similarity(matrix[0], matrix[1])[0][0])


def _token_set_score(resume_text: str, jd_text: str) -> float:
    resume_tokens = set(re.findall(r"\b[a-z0-9][a-z0-9+\-.#]{1,}\b", resume_text.lower()))
    jd_tokens = set(re.findall(r"\b[a-z0-9][a-z0-9+\-.#]{1,}\b", jd_text.lower()))
    if not resume_tokens or not jd_tokens:
        return 0.0
    overlap = len(resume_tokens & jd_tokens)
    recall = overlap / len(jd_tokens)
    dice = (2 * overlap) / (len(resume_tokens) + len(jd_tokens))
    return (recall * 0.72) + (dice * 0.28)


def compute_similarity(resume_text, jd_text):
    texts = [_safe_text(resume_text), _safe_text(jd_text)]
    if not texts[0] and not texts[1]:
        return 0.0

    word_score = _tfidf_cosine(
        texts,
        lowercase=True,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
        max_df=1.0,
        norm="l2",
    )
    char_score = _tfidf_cosine(
        texts,
        lowercase=True,
        analyzer="char_wb",
        ngram_range=(3, 5),
        sublinear_tf=True,
        min_df=1,
        norm="l2",
    )
    token_score = _token_set_score(texts[0], texts[1])

    calibrated = (word_score * 0.48) + (char_score * 0.22) + (token_score * 0.30)
    # Two-document TF-IDF is naturally conservative. This monotonic calibration
    # keeps weak matches weak while allowing solid industry resumes to reach a
    # realistic shortlist range when skills and evidence also align.
    return round(min(1.0, math.sqrt(max(0.0, calibrated)) * 0.92), 4)


def _coverage(matched: list[str], required: list[str], fallback: float = 0.0) -> float:
    required_set = set(required or [])
    if not required_set:
        return fallback
    return len(set(matched or []) & required_set) / len(required_set)


def _keyword_coverage(fv: dict) -> float:
    jd_keywords = set(fv.get("jd_keywords") or [])
    if not jd_keywords:
        return 0.0
    return len(set(fv.get("matched_keywords") or []) & jd_keywords) / len(jd_keywords)


def compute_score_breakdown(fv: dict) -> dict:
    similarity = compute_similarity(fv.get("clean_resume", ""), fv.get("clean_jd", ""))
    skill_coverage = _coverage(fv.get("matched_skills", []), fv.get("jd_skills", []), fallback=similarity)
    keyword_coverage = _keyword_coverage(fv)
    quality = fv.get("resume_quality") or {}
    ats_score = float(quality.get("ats_score", 0.0))
    evidence_score = float(quality.get("evidence_score", 0.0))
    depth_gap = float(fv.get("depth_gap", 0.0) or 0.0)
    depth_penalty = min(0.08, max(0.0, depth_gap) * 0.035)

    raw_score = (
        similarity * 0.30
        + skill_coverage * 0.34
        + keyword_coverage * 0.17
        + evidence_score * 0.10
        + ats_score * 0.09
        - depth_penalty
    )
    if skill_coverage >= 0.85 and keyword_coverage >= 0.65:
        raw_score += 0.08
    elif skill_coverage >= 0.70 and keyword_coverage >= 0.50:
        raw_score += 0.04

    final_score = max(0.0, min(raw_score, 1.0))

    return {
        "semantic_similarity": round(similarity, 4),
        "skill_coverage": round(skill_coverage, 4),
        "keyword_coverage": round(keyword_coverage, 4),
        "evidence_score": round(evidence_score, 4),
        "ats_score": round(ats_score, 4),
        "depth_penalty": round(depth_penalty, 4),
        "final_score": round(final_score, 4),
    }


def compute_final_score(fv):
    breakdown = compute_score_breakdown(fv)
    similarity = breakdown["semantic_similarity"]
    depth_gap = fv["depth_gap"]
    return round(breakdown["final_score"] * 100, 2), similarity, depth_gap
