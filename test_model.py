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


def test_backend_resume_is_not_marked_weak_for_backend_jd():
    resume = """
    Backend developer with Node.js, Express, MongoDB, PostgreSQL, JWT authentication,
    REST API routes, validation middleware, Git, Postman testing, Docker deployment,
    and logging. Built CRUD services and optimized database queries.
    """
    jd = """
    Backend Developer requiring Node.js, Express, REST APIs, authentication, SQL or
    NoSQL databases, validation, testing, deployment workflows, and API documentation.
    """
    fv = build_feature_vector(resume, jd)
    score, _, _ = compute_final_score(fv)

    assert score >= 50


def test_data_resume_is_not_marked_weak_for_data_jd():
    resume = """
    Data scientist using Python, Pandas, NumPy, SQL, Jupyter notebooks, data cleaning,
    EDA, feature engineering, scikit-learn model training, model evaluation metrics,
    Matplotlib, Seaborn, Plotly dashboards, and business insight presentations.
    """
    jd = """
    Data Scientist role needing Python, Pandas, NumPy, SQL, exploratory analysis,
    feature engineering, machine learning with scikit-learn, model evaluation,
    visualization, and communication of insights.
    """
    fv = build_feature_vector(resume, jd)
    score, _, _ = compute_final_score(fv)

    assert score >= 50


def test_full_stack_resume_is_not_marked_weak_for_full_stack_jd():
    resume = """
    Full-stack MERN developer building React forms and responsive UI, Node.js and
    Express REST APIs, MongoDB database CRUD, JWT login, GitHub workflows, testing,
    deployment, and end-to-end dashboard features.
    """
    jd = """
    Full Stack Developer requiring React, JavaScript, Node.js, Express, REST APIs,
    MongoDB or SQL databases, authentication, forms, routing, Git, testing, and deployment.
    """
    fv = build_feature_vector(resume, jd)
    score, _, _ = compute_final_score(fv)

    assert score >= 50
