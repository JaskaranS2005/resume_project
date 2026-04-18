from preprocessing.preprocessing_pipeline import build_feature_vector
from model.model import compute_similarity

resume = "Rea ct dev | 2 yrs | basic Redu x | REST api | no backend"
jd = "React developer with strong Redux and API experience required"

fv = build_feature_vector(resume, jd)

score = compute_similarity(fv["clean_resume"], fv["clean_jd"])

print("\n--- SIMILARITY SCORE ---")
print(score)
