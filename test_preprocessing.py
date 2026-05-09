from preprocessing.preprocessing_pipeline import build_feature_vector


def test_build_feature_vector_contains_expected_keys():
    fv = build_feature_vector(
        "Rea ct dev | 2 yrs | basic Redu x | REST api | no backend",
        "React developer with strong Redux and API experience required",
    )

    expected_keys = {
        "clean_resume",
        "clean_jd",
        "resume_depth",
        "jd_depth",
        "depth_gap",
        "resume_signals",
        "jd_signals",
        "resume_skills",
        "jd_skills",
        "matched_skills",
        "missing_skills",
        "resume_quality",
    }
    assert expected_keys.issubset(fv.keys())


def test_depth_gap_is_non_negative():
    fv = build_feature_vector("python developer", "python developer")
    assert fv["depth_gap"] >= 0


def test_skill_aliases_are_normalized():
    fv = build_feature_vector(
        "Built React.js UI with JS, REST APIs, GitHub, and Jest tests.",
        "Frontend role needs React, JavaScript, API integration, Git, and testing.",
    )
    assert "react" in fv["matched_skills"]
    assert "javascript" in fv["matched_skills"]
    assert "testing" in fv["matched_skills"]


def test_depth_signals_are_normalized_not_raw_adjectives():
    fv = build_feature_vector(
        "Experienced frontend developer with 3 years of experience. Built and deployed React dashboards.",
        "Frontend developer with React delivery experience.",
    )
    assert "experienced" not in fv["resume_signals"]
    assert "hands-on delivery" in fv["resume_signals"]
    assert "advanced production evidence" in fv["resume_signals"]
