from utils.file_extractor import extract_pdf_text
from preprocessing.preprocessing_pipeline import build_feature_vector
from model.model import compute_final_score

print("==== Resume Analyzer ====\n")

resume_path = input("Enter Resume PDF path: ")
jd = input("Enter Job Description: ")

# Extract text from PDF
resume_text = extract_pdf_text(resume_path)

# Process
fv = build_feature_vector(resume_text, jd)

# Compute score
final_score, similarity, depth_gap = compute_final_score(fv)

print("\n========== RESULT ==========")
print(f"Match Score: {final_score}%")
print(f"Similarity Score: {round(similarity,2)}")
print(f"Depth Gap: {depth_gap}")

print("\n--- ANALYSIS ---")
if final_score > 70:
    print("✅ Strong Match")
elif final_score > 50:
    print("⚠️ Moderate Match")
else:
    print("❌ Weak Match")

print("\n--- DETAILS ---")
print("Resume Signals:", fv["resume_signals"])
print("JD Signals:", fv["jd_signals"])
