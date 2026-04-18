"""
Resume Analyzer & Job Matcher — Preprocessing Pipeline
=======================================================
Lightweight, CPU-friendly text cleaning pipeline for noisy resume/JD data.
No deep learning. No heavy NLP. Just regex, string ops, and simple logic.

Pipeline Steps:
  1. Lowercase & Unicode normalisation
  2. Pipe / bullet delimiter → sentence conversion
  3. Informal language & number-word substitution
  4. Abbreviation expansion
  5. Broken-word correction
  6. Punctuation & whitespace cleanup
  7. Skill normalisation  (integrates v1 skill map)
  8. Stopword removal  (lightweight custom list)
  9. Depth-signal tagging  (expert / familiar / basic)
 10. Final token assembly

Author : Resume Analyzer Project
"""

import re
import unicodedata
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 — LOWERCASE & UNICODE NORMALISATION
# ═══════════════════════════════════════════════════════════════════════════════

def step1_lowercase_and_normalise(text: str) -> str:
    """
    Convert to lowercase and strip non-ASCII / smart-quote characters.
    Handles copy-paste artefacts from PDFs and Word docs.

    Input  → "React.js | Nod•e JS — 'Senior' Engineer"
    Output → "react.js | nod e js - 'senior' engineer"
    """
    # Normalise unicode (NFKD decomposes ligatures, accented chars etc.)
    text = unicodedata.normalize("NFKD", text)
    # Encode to ASCII ignoring unmappable chars, then decode back
    text = text.encode("ascii", "ignore").decode("ascii")
    # Lowercase everything
    text = text.lower()
    # Replace smart dashes / curly quotes with plain equivalents
    text = re.sub(r"[–—]", "-", text)
    text = re.sub(r"[''`]", "'", text)
    text = re.sub(r"[\"\"]", '"', text)
    return text


# ─── Demo ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    raw = "React.js | Nod•e JS — 'Senior' Engíneer"
    print("STEP 1")
    print(f"  IN  : {raw}")
    print(f"  OUT : {step1_lowercase_and_normalise(raw)}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 — PIPE / BULLET DELIMITER → SENTENCE CONVERSION
# ═══════════════════════════════════════════════════════════════════════════════

DELIMITER_PATTERN = re.compile(r"\s*[|•·▸▶►\-–—/]\s*")

def step2_delimiters_to_spaces(text: str) -> str:
    """
    Replace pipe, bullet, slash, and dash delimiters with spaces.
    Preserves hyphens inside compound words (e.g., 'full-stack').

    Input  → "react | node | mongo | 3 yrs exp"
    Output → "react  node  mongo  3 yrs exp"
    """
    # Protect known hyphenated tech terms before stripping dashes
    protected = {
        "full-stack": "FULLSTACK",
        "open-source": "OPENSOURCE",
        "end-to-end": "ENDTOEND",
        "state-of-the-art": "STATEOFTHEART",
        "cross-platform": "CROSSPLATFORM",
        "real-time": "REALTIME",
        "large-scale": "LARGESCALE",
    }
    for term, token in protected.items():
        text = text.replace(term, token)

    # Replace delimiter characters with a space
    text = DELIMITER_PATTERN.sub(" ", text)

    # Restore protected terms
    for term, token in protected.items():
        text = text.replace(token, term)

    return text


if __name__ == "__main__":
    raw = "react | node.js | mongo | full-stack dev / 3 yrs"
    s1  = step1_lowercase_and_normalise(raw)
    s2  = step2_delimiters_to_spaces(s1)
    print("STEP 2")
    print(f"  IN  : {s1}")
    print(f"  OUT : {s2}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 — INFORMAL LANGUAGE & NUMBER-WORD SUBSTITUTION
# ═══════════════════════════════════════════════════════════════════════════════

INFORMAL_MAP = {
    # Internet shorthand
    r"\b2\b":          "to",
    r"\b4\b":          "for",
    r"\bw/\b":         "with",
    r"\bw/o\b":        "without",
    r"\bb/w\b":        "between",
    r"\bidk\b":        "i do not know",
    r"\bimo\b":        "in my opinion",
    r"\bbtw\b":        "by the way",
    r"\bfyi\b":        "for your information",
    r"\bexp\b":        "experience",
    r"\byrs\b":        "years",
    r"\byr\b":         "year",
    r"\bdev\b":        "developer",
    r"\beng\b":        "engineer",
    r"\bmgmt\b":       "management",
    r"\badmin\b":      "administration",
    r"\bprod\b":       "production",
    r"\bperf\b":       "performance",
    r"\bauth\b":       "authentication",
    r"\bdepl\b":       "deployment",
    r"\bdeploy\b":     "deployment",
    r"\bmem\b":        "memory",
    r"\bopt\b":        "optimisation",
    r"\barch\b":       "architecture",
    r"\binfra\b":      "infrastructure",
    r"\borg\b":        "organisation",
    r"\bic\b":         "individual contributor",
    r"\bswe\b":        "software engineer",
    r"\bfe\b":         "frontend",
    r"\bbe\b":         "backend",
    r"\bfs\b":         "full-stack",
    r"\bstk\b":        "stack",
    r"\btechstk\b":    "tech stack",
    r"\bcs\b":         "computer science",
    r"\bml\b":         "machine learning",
    r"\bdl\b":         "deep learning",
    r"\bnlp\b":        "natural language processing",
    r"\bcv\b":         "computer vision",
    r"\bllm\b":        "large language model",
    r"\bdbms\b":       "database management system",
    r"\bos\b":         "operating system",
    r"\bpy\b":         "python",
    r"\bjs\b":         "javascript",
    r"\bts\b":         "typescript",
    r"\bk8s\b":        "kubernetes",
    r"\biac\b":        "infrastructure as code",
    r"\bdwh\b":        "data warehouse",
    r"\betl\b":        "extract transform load",
    r"\bci/cd\b":      "continuous integration continuous deployment",
    r"\brest\b":       "rest api",
    r"\bapi\b":        "api",
    r"\bjwt\b":        "json web token",
    r"\bsql\b":        "sql",
    r"\bnosql\b":      "nosql",
    r"\bokay\b":       "ok",   # normalise variant
    r"\bhappy\s+2\b":  "willing to",
    r"\bopen\s+2\b":   "open to",
}

def step3_expand_informal(text: str) -> str:
    """
    Replace internet slang, abbreviations, and number-words.

    Input  → "happy 2 take ic role | 3 yrs exp | py dev"
    Output → "willing to take individual contributor role  3 years experience  python developer"
    """
    for pattern, replacement in INFORMAL_MAP.items():
        text = re.sub(pattern, replacement, text)
    return text


if __name__ == "__main__":
    raw = "happy 2 take ic role | 3 yrs exp | py dev | k8s & iac"
    s1  = step1_lowercase_and_normalise(raw)
    s2  = step2_delimiters_to_spaces(s1)
    s3  = step3_expand_informal(s2)
    print("STEP 3")
    print(f"  IN  : {s2}")
    print(f"  OUT : {s3}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4 — ABBREVIATION EXPANSION (tech-specific)
# ═══════════════════════════════════════════════════════════════════════════════

TECH_ABBREVIATIONS = {
    # Languages
    r"\bc\+\+\b":          "cpp",
    r"\bc#\b":             "csharp",
    r"\bobj-c\b":          "objective-c",
    r"\bobjc\b":           "objective-c",
    # Frameworks / tools
    r"\bnext\.?js\b":      "nextjs",
    r"\bnuxt\.?js\b":      "nuxtjs",
    r"\bexpress\.?js\b":   "expressjs",
    r"\breact\.?js\b":     "react",
    r"\bvue\.?js\b":       "vue",
    r"\bangular\.?js\b":   "angular",
    r"\bnode\.?js\b":      "nodejs",
    r"\bpostgre\b":        "postgresql",
    r"\bpostgres\b":       "postgresql",
    r"\bmongo\b":          "mongodb",
    r"\bpg\b":             "postgresql",
    r"\btf\b":             "tensorflow",
    r"\bsk-?learn\b":      "scikit-learn",
    r"\bsklearn\b":        "scikit-learn",
    r"\bhf\b":             "huggingface",
    # Cloud / DevOps
    r"\baws\b":            "amazon web services",
    r"\bgcp\b":            "google cloud platform",
    r"\bec2\b":            "aws ec2",
    r"\bs3\b":             "aws s3",
    r"\brds\b":            "aws rds",
    r"\bgke\b":            "google kubernetes engine",
    r"\bcr\b":             "cloud run",
    r"\bghactions\b":      "github actions",
    r"\bgh\s+actions\b":   "github actions",
}

def step4_expand_tech_abbreviations(text: str) -> str:
    """
    Expand known tech abbreviations to their canonical forms.

    Input  → "node.js + pg + tf + sk-learn"
    Output → "nodejs  postgresql  tensorflow  scikit-learn"
    """
    for pattern, replacement in TECH_ABBREVIATIONS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


if __name__ == "__main__":
    raw = "node.js + pg + tf + sk-learn | react.js | aws | gcp"
    s1  = step1_lowercase_and_normalise(raw)
    s2  = step2_delimiters_to_spaces(s1)
    s3  = step3_expand_informal(s2)
    s4  = step4_expand_tech_abbreviations(s3)
    print("STEP 4")
    print(f"  IN  : {s3}")
    print(f"  OUT : {s4}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5 — BROKEN-WORD CORRECTION
# ═══════════════════════════════════════════════════════════════════════════════

# Known broken-word patterns specific to tech resumes
BROKEN_WORD_MAP = {
    r"\brea\s+ct\b":         "react",
    r"\bnod\s+e\s*js\b":     "nodejs",
    r"\bnod\s+e\b":          "node",
    r"\bpyth\s+on\b":        "python",
    r"\bdjang\s+o\b":        "django",
    r"\bkubern\s+etes\b":    "kubernetes",
    r"\btype\s+script\b":    "typescript",
    r"\bjava\s+script\b":    "javascript",
    r"\bpost\s+gres\b":      "postgresql",
    r"\bmong\s+odb\b":       "mongodb",
    r"\btensor\s+flow\b":    "tensorflow",
    r"\bscikit\s+learn\b":   "scikit-learn",
    r"\bgraph\s+ql\b":       "graphql",
    r"\bcloud\s+watch\b":    "cloudwatch",
    r"\bgit\s+hub\b":        "github",
    r"\bdata\s+base\b":      "database",
    r"\bback\s+end\b":       "backend",
    r"\bfront\s+end\b":      "frontend",
    r"\bwork\s+flow\b":      "workflow",
    r"\bframe\s+work\b":     "framework",
    r"\bmicro\s+service\b":  "microservice",
    r"\bopen\s+ai\b":        "openai",
    r"\bhugging\s+face\b":   "huggingface",
    r"\bfast\s+api\b":       "fastapi",
    r"\bspring\s+boot\b":    "springboot",
    r"\belastic\s+search\b": "elasticsearch",
}

def step5_fix_broken_words(text: str) -> str:
    """
    Rejoin broken technical terms split by spurious spaces.

    Input  → "rea ct dev with nod e js and kube rnetes"
    Output → "react dev with nodejs and kubernetes"
    """
    for pattern, replacement in BROKEN_WORD_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


if __name__ == "__main__":
    noisy = "rea ct dev | nod e js | kube rnetes | type script"
    s1 = step1_lowercase_and_normalise(noisy)
    s2 = step2_delimiters_to_spaces(s1)
    s5 = step5_fix_broken_words(s2)
    print("STEP 5")
    print(f"  IN  : {s2}")
    print(f"  OUT : {s5}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6 — PUNCTUATION & WHITESPACE CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════

def step6_clean_punctuation_and_whitespace(text: str) -> str:
    """
    Strip residual punctuation, collapse multiple spaces, and trim.
    Keeps alphanumeric, spaces, hyphens (compound words), and dots (version nums).

    Input  → "python!!  (3 yrs),,,  expert...   "
    Output → "python 3 yrs expert"
    """
    # Remove parentheses and their common surrounding whitespace
    text = re.sub(r"\(.*?\)", " ", text)
    # Keep only: letters, digits, spaces, hyphens, dots, +
    text = re.sub(r"[^a-z0-9\s\.\-\+]", " ", text)
    # Remove standalone dots not used as version separators
    text = re.sub(r"(?<!\d)\.(?!\d)", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


if __name__ == "__main__":
    messy = "python!!  (3 yrs),,,  expert...   react -- node.js!!  "
    s1 = step1_lowercase_and_normalise(messy)
    s6 = step6_clean_punctuation_and_whitespace(s1)
    print("STEP 6")
    print(f"  IN  : {s1}")
    print(f"  OUT : {s6}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 7 — SKILL NORMALISATION  (integrates v1 skill map)
# ═══════════════════════════════════════════════════════════════════════════════

# Condensed version of the 153-entry map from dataset v1
SKILL_NORM_MAP = {
    "react.js": "react",    "reactjs": "react",
    "vue.js": "vue",        "vuejs": "vue",
    "angular.js": "angular","angularjs": "angular",
    "javascript": "javascript", "es6": "javascript", "ecmascript": "javascript",
    "node.js": "nodejs",    "node": "nodejs",
    "express.js": "expressjs", "express": "expressjs",
    "mern": "react nodejs mongodb expressjs",
    "mean": "angular nodejs mongodb expressjs",
    "scikit-learn": "sklearn", "scikit learn": "sklearn",
    "tensorflow": "tensorflow", "tf": "tensorflow",
    "pytorch": "pytorch",   "torch": "pytorch",
    "hugging face": "huggingface", "transformers": "huggingface",
    "postgres": "postgresql","pg": "postgresql",
    "mongo": "mongodb",     "mongo db": "mongodb",
    "k8s": "kubernetes",
    "amazon web services": "aws",
    "google cloud platform": "gcp",
    "ci/cd": "cicd",        "continuous integration": "cicd",
    "infrastructure as code": "iac", "terraform": "terraform",
    "extract transform load": "etl",
    "apache spark": "spark","pyspark": "spark",
    "apache kafka": "kafka",
    "apache airflow": "airflow",
}

def step7_normalise_skills(text: str) -> str:
    """
    Replace skill synonyms and variant spellings with canonical tokens.
    Applies longest-match first to avoid partial replacements.

    Input  → "mern developer with scikit-learn and k8s"
    Output → "react nodejs mongodb expressjs developer with sklearn and kubernetes"
    """
    # Sort by length descending (longest match first)
    for variant in sorted(SKILL_NORM_MAP.keys(), key=len, reverse=True):
        canonical = SKILL_NORM_MAP[variant]
        text = re.sub(rf"\b{re.escape(variant)}\b", canonical, text)
    return text


if __name__ == "__main__":
    raw = "mern developer with scikit-learn and k8s experience"
    s7  = step7_normalise_skills(raw)
    print("STEP 7")
    print(f"  IN  : {raw}")
    print(f"  OUT : {s7}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 8 — STOPWORD REMOVAL (lightweight, no NLTK)
# ═══════════════════════════════════════════════════════════════════════════════

# Domain-tuned stopword list — keeps tech verbs ('build', 'deploy') intentionally
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "up", "about", "into", "through", "during",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "should", "may", "might",
    "this", "that", "these", "those", "it", "its", "we", "our", "you", "your",
    "he", "she", "they", "their", "i", "my", "me",
    "also", "just", "only", "as", "so", "if", "not", "no", "nor",
    "candidate", "position", "role", "job", "company", "team", "work",
    "looking", "seeking", "needed", "required", "must", "need",
    "able", "please", "plus", "given", "well", "strong",
}

def step8_remove_stopwords(text: str) -> str:
    """
    Remove generic stopwords while preserving domain-meaningful tokens.

    Input  → "looking for a react developer with strong node skills"
    Output → "react developer node skills"
    """
    tokens = text.split()
    filtered = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    return " ".join(filtered)


if __name__ == "__main__":
    raw = "looking for a react developer with strong node skills and good experience"
    s8  = step8_remove_stopwords(raw)
    print("STEP 8")
    print(f"  IN  : {raw}")
    print(f"  OUT : {s8}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 9 — DEPTH-SIGNAL EXTRACTION (returns metadata, not modified text)
# ═══════════════════════════════════════════════════════════════════════════════

DEPTH_SIGNALS = {
    "expert":         3,   # Highest weight
    "extensive":      3,
    "worked extensively": 3,
    "advanced":       3,
    "senior":         3,
    "proficient":     2,   # Mid weight
    "experienced":    2,
    "intermediate":   2,
    "comfortable":    2,
    "solid":          2,
    "basic":          1,   # Low weight
    "familiar":       1,
    "some knowledge": 1,
    "beginner":       1,
    "recently":       1,
    "learning":       1,
    "introductory":   1,
    "no experience":  0,   # Absence signal
    "no .+ experience": 0,
}

def step9_extract_depth_signals(original_text: str) -> dict:
    """
    Scan original (pre-cleaned) text for skill-depth qualifiers.
    Returns a metadata dict — does NOT modify the text.
    Used downstream as an additional feature vector.

    Output: {"max_depth": 2, "min_depth": 1, "depth_score": 1.5,
             "signals_found": ["proficient", "familiar"]}
    """
    text_lower = original_text.lower()
    found      = []
    scores     = []

    for signal, score in DEPTH_SIGNALS.items():
        pattern = rf"\b{signal}\b"
        if re.search(pattern, text_lower):
            found.append(signal)
            scores.append(score)

    if not scores:
        return {"max_depth": 2, "min_depth": 2,
                "depth_score": 2.0, "signals_found": []}

    return {
        "max_depth":     max(scores),
        "min_depth":     min(scores),
        "depth_score":   round(sum(scores) / len(scores), 2),
        "signals_found": found,
    }


if __name__ == "__main__":
    text = "Expert in Python and Scikit-learn. Familiar with Spark. No Airflow experience."
    meta = step9_extract_depth_signals(text)
    print("STEP 9 (metadata — does not modify text)")
    print(f"  IN     : {text}")
    print(f"  SIGNALS: {meta}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 10 — FULL PIPELINE ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════════

def preprocess(text: str, return_metadata: bool = False):
    """
    Run all 9 transformation steps in sequence.

    Args:
        text            : Raw resume or job description string.
        return_metadata : If True, also return depth-signal metadata dict.

    Returns:
        clean_text (str)  — ready for TF-IDF vectorisation
        metadata   (dict) — optional, for feature engineering
    """
    meta        = step9_extract_depth_signals(text)   # extract BEFORE cleaning
    s1          = step1_lowercase_and_normalise(text)
    s2          = step2_delimiters_to_spaces(s1)
    s3          = step3_expand_informal(s2)
    s4          = step4_expand_tech_abbreviations(s3)
    s5          = step5_fix_broken_words(s4)
    s6          = step6_clean_punctuation_and_whitespace(s5)
    s7          = step7_normalise_skills(s6)
    s8          = step8_remove_stopwords(s7)
    clean_text  = s8

    if return_metadata:
        return clean_text, meta
    return clean_text


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION EXAMPLE — drop into existing ML pipeline
# ═══════════════════════════════════════════════════════════════════════════════

def build_feature_vector(resume: str, job_desc: str) -> dict:
    """
    Preprocess both texts and return a dict ready for ML feature extraction.
    Plug this into your TF-IDF + cosine similarity pipeline.
    """
    clean_resume,  r_meta = preprocess(resume,   return_metadata=True)
    clean_jd,      j_meta = preprocess(job_desc, return_metadata=True)

    return {
        "clean_resume":    clean_resume,
        "clean_jd":        clean_jd,
        "resume_depth":    r_meta["depth_score"],
        "jd_depth":        j_meta["depth_score"],
        "depth_gap":       round(abs(r_meta["depth_score"] - j_meta["depth_score"]), 2),
        "resume_signals":  r_meta["signals_found"],
        "jd_signals":      j_meta["signals_found"],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FULL END-TO-END DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    DIVIDER = "=" * 64

    test_cases = [
        {
            "label": "v3 Noisy — broken words + pipes",
            "resume": "Rea ct dev | 2 yrs | built UI screens | basic Redu x | REST api calls done | no backend",
            "job":    "React developer for a large-scale fintech SaaS dashboard. Must have strong Redux and performance optimisation.",
        },
        {
            "label": "v3 Keyword stuffing",
            "resume": "Skills: Python, ML, TensorFlow, PyTorch, Keras, Scikit-learn, NLP, CV, BERT. Experience: 1 yr internship — ran pre-built Jupyter notebooks.",
            "job":    "ML engineer to own end-to-end model development and deployment. Must build, fine-tune, and ship models to production independently.",
        },
        {
            "label": "v3 Informal + overqualified",
            "resume": "Principal eng | 10 yrs | distributed sys, AWS arch, K8s at scale, Terraform IaC, Kafka, Go/Python. happy 2 take IC role | open to smaller scope",
            "job":    "Mid-level DevOps engineer needed. Docker, basic Kubernetes, and one CI/CD tool required. AWS familiarity is a plus.",
        },
        {
            "label": "v3 C++ → Python transferable gap",
            "resume": "C++ eng | 6 yrs | game-engine dev | mem mgmt, threading, perf tuning. Py — learnt 8 months | 2 personal projects (FastAPI CRUD). no prod Python exp.",
            "job":    "Python backend engineer for a low-latency trading platform. Requires strong async Python, prod deployment, and concurrency expertise.",
        },
    ]

    for case in test_cases:
        print(DIVIDER)
        print(f" TEST: {case['label']}")
        print(DIVIDER)

        fv = build_feature_vector(case["resume"], case["job"])

        print(f"  RAW RESUME   : {case['resume']}")
        print(f"  CLEAN RESUME : {fv['clean_resume']}")
        print()
        print(f"  RAW JD       : {case['job']}")
        print(f"  CLEAN JD     : {fv['clean_jd']}")
        print()
        print(f"  DEPTH SCORE  : resume={fv['resume_depth']}  jd={fv['jd_depth']}  gap={fv['depth_gap']}")
        print(f"  SIGNALS      : resume={fv['resume_signals']}")
        print()
