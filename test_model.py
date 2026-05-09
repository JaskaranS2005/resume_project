from model.model import compute_final_score, compute_similarity
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


def test_industry_aligned_resume_reaches_strong_range():
    resume = """
    Alex Morgan
    alex@example.com | +1 555 123 4567 | github.com/alex | linkedin.com/in/alex
    Summary
    Frontend developer with 3 years of experience building React dashboards, reusable components,
    responsive UI, Redux state management, TypeScript forms, REST API integrations, authentication
    flows, Git workflows, and Jest testing.
    Experience
    Built and deployed a React analytics dashboard used by 5,000 users, reducing page load time by 32%.
    Integrated REST APIs with loading, validation, and error states.
    Projects
    Created a TypeScript React project with Redux, routing, responsive design, API integration, and tests.
    Education
    B.Tech Computer Science
    Skills
    React, JavaScript, TypeScript, Redux, REST APIs, HTML, CSS, Git, Testing, Responsive UI
    """
    jd = """
    Frontend Developer role requiring React, JavaScript, TypeScript, Redux, REST API integration,
    responsive UI, reusable components, Git, testing, forms, authentication, and performance optimization.
    """
    fv = build_feature_vector(resume, jd)
    score, similarity, depth_gap = compute_final_score(fv)

    assert score >= 85
    assert similarity > 0.35
    assert depth_gap >= 0


def test_unrelated_resume_stays_low():
    resume = """
    Jamie Lee
    jamie@example.com | +1 555 333 2222
    Experience
    Managed retail store inventory, customer service, cash handling, and daily shift schedules.
    Education
    Bachelor of Arts
    Skills
    Communication, sales, merchandising, vendor coordination.
    """
    jd = "Backend developer requiring Node.js, Express, PostgreSQL, REST APIs, authentication, Docker, and CI CD."
    fv = build_feature_vector(resume, jd)
    score, _, _ = compute_final_score(fv)

    assert score < 55
