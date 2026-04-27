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
    }
    assert expected_keys.issubset(fv.keys())


def test_depth_gap_is_non_negative():
    fv = build_feature_vector("python developer", "python developer")
    assert fv["depth_gap"] >= 0
