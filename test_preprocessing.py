from preprocessing.preprocessing_pipeline import build_feature_vector

resume = "Rea ct dev | 2 yrs | basic Redu x | REST api | no backend"
jd = "React developer with strong Redux and API experience required"

fv = build_feature_vector(resume, jd)

print("\n--- CLEANED OUTPUT ---")
print("Resume:", fv["clean_resume"])
print("Job Desc:", fv["clean_jd"])

print("\n--- DEPTH INFO ---")
print("Resume Depth:", fv["resume_depth"])
print("JD Depth:", fv["jd_depth"])
print("Depth Gap:", fv["depth_gap"])

print("\n--- SIGNALS ---")
print("Resume Signals:", fv["resume_signals"])
print("JD Signals:", fv["jd_signals"])
