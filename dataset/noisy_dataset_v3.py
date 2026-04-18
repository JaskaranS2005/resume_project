"""
Resume Analyzer & Job Matcher — Noisy Real-World Dataset v3
============================================================
10 challenging examples simulating:
  - Noisy / broken text          - Keyword stuffing
  - Ambiguous partial matches    - Misleading depth signals
  - Transferable skill gaps      - Mixed domain profiles
  - Overqualification edge cases - Missing 1 critical skill
"""

noisy_dataset_v3 = [

    # ── 1. NOISY TEXT + BASIC DEPTH (Hard negative) ─────────────────────────────
    {
        "id": 1,
        "resume": (
            "Rea ct dev | 2 yrs | built UI screens, forms, landing pages | "
            "basic Redu x | REST api calls done | no backend"
        ),
        "job_description": (
            "React developer for a large-scale fintech SaaS dashboard. "
            "Must have strong Redux, memoization, and performance optimisation experience. "
            "Complex state trees and code-splitting knowledge required."
        ),
        "label": 0,
        "reason": (
            "Noisy formatting masks shallow depth. Candidate has basic Redux only; "
            "job demands advanced state management and performance tuning at scale. "
            "Skill-level mismatch despite keyword overlap."
        ),
    },

    # ── 2. KEYWORD STUFFING — Misleading positive signal (Hard negative) ────────
    {
        "id": 2,
        "resume": (
            "Skills: Python, ML, TensorFlow, PyTorch, Keras, Scikit-learn, NLP, CV, "
            "BERT, GPT, Transformers, Hugging Face, Docker, AWS, Spark, Kafka. "
            "Experience: 1 yr internship — ran pre-built Jupyter notebooks."
        ),
        "job_description": (
            "ML engineer to own end-to-end model development and deployment. "
            "Must build, fine-tune, and ship models to production independently. "
            "3+ years hands-on experience required."
        ),
        "label": 0,
        "reason": (
            "Classic keyword stuffing — breadth without depth. "
            "All terms present but experience is 1 internship running existing notebooks. "
            "Production ownership requirement is unmet."
        ),
    },

    # ── 3. NOISY TEXT + TRANSFERABLE SKILLS (Borderline negative) ───────────────
    {
        "id": 3,
        "resume": (
            "C++ eng | 6 yrs | game-engine dev | mem mgmt, threading, perf tuning. "
            "Py — learnt 8 months | 2 personal projects (FastAPI CRUD, data scripts). "
            "no prod Python exp."
        ),
        "job_description": (
            "Python backend engineer for a low-latency trading platform. "
            "Requires strong async Python, production deployment, and concurrency expertise. "
            "Systems programming mindset is a strong plus."
        ),
        "label": 0,
        "reason": (
            "Transferable systems mindset (concurrency, perf) is highly relevant, "
            "but 8 months of Python with no production deployment is insufficient "
            "for a latency-critical trading system. Borderline but negative."
        ),
    },

    # ── 4. AMBIGUOUS — Missing exactly 1 critical skill (Borderline negative) ───
    {
        "id": 4,
        "resume": (
            "Node.js backend dev | 3 yrs | REST APIs, Express, JWT auth. "
            "MongoDB + PostgreSQL experience. CI/CD with GitHub Actions. "
            "No Kubernetes experience; deployed on Heroku and basic EC2 only."
        ),
        "job_description": (
            "Backend Node.js engineer for a cloud-native microservices platform. "
            "Kubernetes orchestration is mandatory — team runs 40+ services on K8s. "
            "Express, PostgreSQL, and CI/CD experience required."
        ),
        "label": 0,
        "reason": (
            "Strong match on 4 out of 5 criteria. "
            "Kubernetes is listed mandatory and non-negotiable for a 40-service K8s cluster. "
            "Single critical gap disqualifies an otherwise strong candidate."
        ),
    },

    # ── 5. NOISY + MIXED DOMAIN (Misleading match) ──────────────────────────────
    {
        "id": 5,
        "resume": (
            "6 yrs exp — iOS (Swift/ObjC) + some web work. "
            "React Native: 2 apps shipped (iOS only, Android untested). "
            "Redux familiar | REST ok | no TypeScript."
        ),
        "job_description": (
            "React Native developer for a cross-platform healthcare app. "
            "Must support iOS AND Android in production. TypeScript required throughout. "
            "Redux Toolkit and accessibility compliance (WCAG) experience needed."
        ),
        "label": 0,
        "reason": (
            "Candidate has shipped RN apps but iOS-only — Android untested in production. "
            "TypeScript absent; healthcare apps require strict typing. "
            "Two non-negotiable gaps despite strong mobile background."
        ),
    },

    # ── 6. OVERQUALIFIED + NOISY FORMAT (Hard positive edge case) ───────────────
    {
        "id": 6,
        "resume": (
            "Principal eng | 10 yrs | distributed sys, AWS arch, K8s at scale, "
            "Terraform IaC, Kafka, Go/Python. Led teams of 12. "
            "happy 2 take IC role | open to smaller scope"
        ),
        "job_description": (
            "Mid-level DevOps engineer needed. Docker, basic Kubernetes, "
            "and one CI/CD tool required. AWS familiarity is a plus. "
            "Small startup — must be hands-on."
        ),
        "label": 1,
        "reason": (
            "Heavily overqualified but explicitly open to IC/smaller scope. "
            "Every technical requirement is met with room to spare. "
            "Overqualification is a retention risk, not a skill disqualifier — label 1."
        ),
    },

    # ── 7. SKILL DEPTH SIGNAL — 'Familiar with' vs 'Expert in' ─────────────────
    {
        "id": 7,
        "resume": (
            "Data scientist | 4 yrs | expert in Python, XGBoost, Scikit-learn. "
            "Familiar with Spark — ran a few PySpark jobs under supervision. "
            "Deployed models via Flask; no Airflow or pipeline orchestration exp."
        ),
        "job_description": (
            "Senior data scientist — Python ML modelling + Spark for large-scale feature engineering. "
            "Airflow pipeline ownership preferred but not mandatory. "
            "Flask or FastAPI deployment experience required."
        ),
        "label": 1,
        "reason": (
            "Core ML + deployment skills match strongly. "
            "Spark is 'familiar with' vs job's 'large-scale' need — partial gap. "
            "Airflow listed as preferred, not required. Net result: positive match."
        ),
    },

    # ── 8. AMBIGUOUS — Transferable domain, close but not quite (Borderline) ────
    {
        "id": 8,
        "resume": (
            "Data analyst → aspiring data engineer. "
            "Expert in SQL (5 yrs), Tableau, Excel. Python intermediate — "
            "built ETL scripts w/ Pandas. No Spark, Airflow, or cloud DWH experience."
        ),
        "job_description": (
            "Junior data engineer to build and maintain ETL pipelines. "
            "Python + SQL required. Spark or Airflow experience a plus, not required. "
            "Willingness to learn cloud tools (BigQuery/Snowflake) essential."
        ),
        "label": 1,
        "reason": (
            "Job is junior-level and explicitly marks Spark/Airflow as optional. "
            "Candidate's SQL depth, ETL scripting, and transition trajectory align. "
            "'Willingness to learn' signals culture fit over tool checklist. Borderline positive."
        ),
    },

    # ── 9. NOISY + MISLEADING DOMAIN MIX (Hard negative) ────────────────────────
    {
        "id": 9,
        "resume": (
            "Full stk dev | React, Node, Mongo | also: SEO, Google Analytics, "
            "content writing, Wordpress mgmt, email campaigns. "
            "3 yrs agency work — wore many hats."
        ),
        "job_description": (
            "Senior full-stack engineer for a product team. "
            "Deep expertise in React architecture, Node.js microservices, and system design. "
            "Must lead technical decisions and mentor junior engineers."
        ),
        "label": 0,
        "reason": (
            "Mixed-domain profile signals broad but shallow engineering depth. "
            "Agency 'many hats' experience rarely builds the system-design and "
            "architecture skills required for a senior product engineering lead role."
        ),
    },

    # ── 10. MISSING 1 SOFT-CRITICAL SKILL + NOISY TEXT (Borderline positive) ────
    {
        "id": 10,
        "resume": (
            "NLP eng | 3 yrs | HuggingFace, BERT fine-tuning, spaCy, FastAPI. "
            "Deployed models via Docker + AWS Lambda. "
            "no MLflow / experiment tracking — used custom logging scripts."
        ),
        "job_description": (
            "NLP engineer to build and ship text classification pipelines. "
            "Hugging Face + FastAPI deployment required. "
            "MLflow for experiment tracking preferred; AWS experience essential."
        ),
        "label": 1,
        "reason": (
            "All hard requirements met: HuggingFace, FastAPI, Docker, AWS. "
            "MLflow is 'preferred' — candidate uses custom logging as a substitute. "
            "Missing soft-preferred tool doesn't outweigh strong core alignment."
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# NOISE PATTERN CATALOGUE  (useful for data-augmentation later)
# ─────────────────────────────────────────────────────────────────────────────

noise_patterns_used = {
    1:  ["broken_word_spacing", "pipe_delimiter", "no_backend_flag"],
    2:  ["keyword_stuffing", "depth_mismatch", "experience_inflation"],
    3:  ["abbreviation_heavy", "no_prod_signal", "transferable_gap"],
    4:  ["single_critical_gap", "otherwise_strong", "mandatory_keyword"],
    5:  ["platform_gap_iOS_only", "missing_typescript", "mixed_domain"],
    6:  ["overqualified", "informal_language", "scope_openness"],
    7:  ["depth_qualifier_familiar", "depth_qualifier_expert", "optional_skill"],
    8:  ["transition_candidate", "junior_role_match", "learn_signal"],
    9:  ["mixed_domain_pollution", "agency_breadth", "seniority_gap"],
    10: ["substitute_tool", "preferred_not_required", "custom_logging"],
}


if __name__ == "__main__":
    labels = [d["label"] for d in noisy_dataset_v3]

    print("=" * 60)
    print(" NOISY REAL-WORLD DATASET v3 — SUMMARY")
    print("=" * 60)
    print(f"  Total examples     : {len(noisy_dataset_v3)}")
    print(f"  Good matches (1)   : {labels.count(1)}")
    print(f"  Poor matches (0)   : {labels.count(0)}")
    print()
    print("  Noise patterns used per example:")
    for eid, patterns in noise_patterns_used.items():
        print(f"    #{eid}: {', '.join(patterns)}")
    print()

    print("=" * 60)
    print(" FULL DATASET  (strict output format)")
    print("=" * 60)
    for d in noisy_dataset_v3:
        print(f"\nResume: {d['resume']}")
        print(f"Job Description: {d['job_description']}")
        print(f"Label: {d['label']}")
        print(f"Reason: {d['reason']}")
        print("-" * 58)
