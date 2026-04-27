from model.model import compute_similarity
from preprocessing.preprocessing_pipeline import build_feature_vector


def test_compute_similarity_handles_empty_inputs():
    assert compute_similarity("", "") == 0.0


def test_compute_similarity_returns_reasonable_score():
    resume = "React developer building frontend dashboards and API integrations."
    jd = "Frontend role requiring React, APIs, and JavaScript."
    score = compute_similarity(resume, jd)

    assert 0.0 <= score <= 1.0
    assert score > 0.0


def test_compute_similarity_with_preprocessed_text():
    resume = "Rea ct dev | 2 yrs | basic Redu x | REST api | no backend"
    jd = "React developer with strong Redux and API experience required"

    fv = build_feature_vector(resume, jd)
    score = compute_similarity(fv["clean_resume"], fv["clean_jd"])

    assert 0.0 <= score <= 1.0
