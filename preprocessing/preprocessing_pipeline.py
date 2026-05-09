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

SKILL_ALIASES = {
    "react": {"react", "reactjs", "frontend components", "component based"},
    "javascript": {"javascript", "js", "es6", "ecmascript"},
    "typescript": {"typescript", "ts"},
    "html": {"html", "semantic html"},
    "css": {"css", "scss", "sass", "tailwind", "responsive design", "responsive ui"},
    "redux": {"redux", "state management", "zustand", "context api"},
    "nodejs": {"nodejs", "node", "node.js"},
    "expressjs": {"expressjs", "express", "express.js"},
    "python": {"python", "py"},
    "java": {"java", "springboot", "spring boot"},
    "sql": {"sql", "mysql", "postgresql", "postgres", "database queries"},
    "mongodb": {"mongodb", "mongo", "nosql"},
    "rest api": {"rest api", "rest", "api integration", "apis", "http api"},
    "graphql": {"graphql", "graph ql"},
    "authentication": {"authentication", "authorization", "auth", "jwt", "oauth", "session"},
    "testing": {"testing", "unit testing", "integration testing", "jest", "pytest", "selenium", "playwright", "cypress"},
    "git": {"git", "github", "version control", "pull request", "branching"},
    "docker": {"docker", "container", "containerization"},
    "kubernetes": {"kubernetes", "k8s"},
    "aws": {"aws", "amazon web services", "ec2", "s3", "rds", "lambda"},
    "gcp": {"gcp", "google cloud platform", "cloud run"},
    "ci cd": {"ci cd", "cicd", "github actions", "continuous integration", "continuous deployment"},
    "machine learning": {"machine learning", "ml", "model training", "model evaluation"},
    "data analysis": {"data analysis", "eda", "exploratory analysis", "analytics", "dashboard"},
    "pandas": {"pandas"},
    "numpy": {"numpy"},
    "sklearn": {"sklearn", "scikit-learn", "scikit learn"},
    "tensorflow": {"tensorflow", "tf"},
    "pytorch": {"pytorch", "torch"},
    "power bi": {"power bi", "powerbi"},
    "tableau": {"tableau"},
    "figma": {"figma", "wireframe", "prototype", "design system"},
}

RESUME_SECTION_TERMS = {
    "experience", "work experience", "education", "skills", "projects", "certifications",
    "summary", "objective", "achievements", "contact", "portfolio",
}

EVIDENCE_TERMS = {
    "built", "developed", "implemented", "designed", "deployed", "optimized", "improved",
    "integrated", "automated", "tested", "launched", "reduced", "increased", "created",
    "managed", "led", "owned", "delivered", "migrated", "debugged", "refactored",
}

IMPACT_PATTERN = re.compile(
    r"(\b\d+(\.\d+)?\s*(%|percent|x|k|m|ms|sec|seconds|users|requests|projects|apis|features|hours|days)\b|"
    r"\b(reduced|increased|improved|optimized|saved|boosted|cut|raised)\b)",
    flags=re.IGNORECASE,
)


def extract_skills(text: str) -> list[str]:
    normalised = step7_normalise_skills(step4_expand_tech_abbreviations(step1_lowercase_and_normalise(text or "")))
    padded = f" {normalised} "
    found = []
    for canonical, aliases in SKILL_ALIASES.items():
        if any(re.search(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", padded) for alias in aliases):
            found.append(canonical)
    return sorted(set(found))


def extract_role_keywords(clean_text: str) -> list[str]:
    tokens = [token for token in clean_text.split() if len(token) > 2 and not token.isdigit()]
    ignored = STOPWORDS | {"developer", "engineer", "intern", "candidate", "experience", "skills", "responsibilities"}
    keywords = []
    for token in tokens:
        if token not in ignored and token not in keywords:
            keywords.append(token)
    return keywords[:80]


def compute_resume_quality(raw_resume: str) -> dict:
    text = raw_resume or ""
    lowered = text.lower()
    words = re.findall(r"\b[a-zA-Z][a-zA-Z+\-.#]*\b", text)
    word_count = len(words)
    section_hits = sorted(section for section in RESUME_SECTION_TERMS if section in lowered)
    evidence_hits = sorted(term for term in EVIDENCE_TERMS if re.search(rf"\b{re.escape(term)}\b", lowered))
    impact_hits = IMPACT_PATTERN.findall(text)
    has_email = bool(re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", text, re.IGNORECASE))
    has_phone = bool(re.search(r"(?:\+?\d[\s().-]*){9,}\d", text))
    has_link = bool(re.search(r"(linkedin|github|portfolio|https?://|www\.)", lowered))

    length_score = min(1.0, word_count / 420) if word_count else 0.0
    section_score = min(1.0, len(section_hits) / 5)
    contact_score = min(1.0, (int(has_email) + int(has_phone) + int(has_link)) / 2)
    evidence_score = min(1.0, (len(evidence_hits) / 8) + (len(impact_hits) / 8))
    ats_score = round((length_score * 0.28) + (section_score * 0.32) + (contact_score * 0.18) + (evidence_score * 0.22), 4)

    return {
        "word_count": word_count,
        "section_hits": section_hits,
        "evidence_terms": evidence_hits,
        "impact_count": len(impact_hits),
        "has_email": has_email,
        "has_phone": has_phone,
        "has_link": has_link,
        "ats_score": ats_score,
        "evidence_score": round(evidence_score, 4),
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
    resume_skills = extract_skills(resume)
    jd_skills = extract_skills(job_desc)
    matched_skills = sorted(set(resume_skills) & set(jd_skills))
    missing_skills = sorted(set(jd_skills) - set(resume_skills))
    resume_keywords = extract_role_keywords(clean_resume)
    jd_keywords = extract_role_keywords(clean_jd)
    matched_keywords = sorted(set(resume_keywords) & set(jd_keywords))
    resume_quality = compute_resume_quality(resume)

    return {
        "clean_resume":    clean_resume,
        "clean_jd":        clean_jd,
        "resume_depth":    r_meta["depth_score"],
        "jd_depth":        j_meta["depth_score"],
        "depth_gap":       round(abs(r_meta["depth_score"] - j_meta["depth_score"]), 2),
        "resume_signals":  r_meta["signals_found"],
        "jd_signals":      j_meta["signals_found"],
        "resume_skills":   resume_skills,
        "jd_skills":       jd_skills,
        "matched_skills":  matched_skills,
        "missing_skills":  missing_skills,
        "resume_keywords": resume_keywords,
        "jd_keywords":     jd_keywords,
        "matched_keywords": matched_keywords,
        "resume_quality":  resume_quality,
    }
