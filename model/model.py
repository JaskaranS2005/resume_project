from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()


def compute_similarity(resume_text, jd_text):
    texts = [(resume_text or "").strip(), (jd_text or "").strip()]

    # Avoid runtime crash when both documents are empty/invalid for TF-IDF.
    if not texts[0] and not texts[1]:
        return 0.0

    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
    except ValueError:
        return 0.0

    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return float(score)


def compute_final_score(fv):
    similarity = compute_similarity(fv["clean_resume"], fv["clean_jd"])
    depth_gap = fv["depth_gap"]

    # Base score
    final_score = similarity - (0.15 * depth_gap)

    # Clamp between 0 and 1
    final_score = max(0, min(final_score, 1))

    return round(final_score * 100, 2), similarity, depth_gap
