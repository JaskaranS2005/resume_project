"""
Resume Analyzer & Job Matcher — Advanced Training Dataset v2
=============================================================
20 realistic, challenging examples with:
  - Partial matches          - Skill level gradients
  - Synonym variation        - Edge cases (overqualified, near-miss, domain overlap)
  - Borderline/ambiguous     - Balanced labels (10 × label-1, 10 × label-0)
"""

advanced_dataset = [

    # ══════════════════════════════════════════════════════
    # BLOCK A — PARTIAL MATCHES  (hardest to classify)
    # ══════════════════════════════════════════════════════

    {
        "id": 1,
        "resume": (
            "Frontend developer with 2 years of experience in React and basic Redux. "
            "Comfortable with REST API consumption and responsive CSS. "
            "No backend experience; limited to client-side JavaScript."
        ),
        "job_description": (
            "Seeking a React developer to build and maintain a SaaS dashboard. "
            "Must handle state management with Redux and integrate backend APIs. "
            "Familiarity with Node.js for minor backend tasks is a plus, not required."
        ),
        "label": 1,
        "reason": (
            "Partial match — candidate covers core requirements (React, Redux basics, APIs). "
            "Node.js listed as optional, so absence doesn't disqualify. Borderline-positive."
        ),
    },

    {
        "id": 2,
        "resume": (
            "Python developer with strong Pandas and NumPy skills. "
            "Wrote data-cleaning scripts and automated Excel reporting. "
            "No machine learning or model-training experience."
        ),
        "job_description": (
            "Data scientist role: build predictive models using Scikit-learn and Python. "
            "Strong data wrangling with Pandas required. "
            "Prior ML experience mandatory; statistics background preferred."
        ),
        "label": 0,
        "reason": (
            "Partial skill overlap (Python, Pandas) but the critical ML requirement is missing. "
            "Data wrangling alone does not satisfy a model-building mandate."
        ),
    },

    {
        "id": 3,
        "resume": (
            "Backend developer experienced in Java Spring Boot and MySQL. "
            "Built RESTful microservices and worked with Docker for containerisation. "
            "No Node.js experience but strong REST API design knowledge."
        ),
        "job_description": (
            "Node.js backend developer needed to build REST APIs. "
            "Express.js and PostgreSQL experience required. "
            "Docker knowledge is a bonus; microservices architecture experience valued."
        ),
        "label": 0,
        "reason": (
            "Domain overlap (backend, REST, Docker, microservices) but language mismatch is critical. "
            "Job requires Node/Express; candidate only knows Java Spring. Near-miss negative."
        ),
    },

    {
        "id": 4,
        "resume": (
            "Full-stack developer with MERN stack experience. "
            "Built e-commerce apps with authentication, payments, and admin dashboards. "
            "Basic knowledge of CI/CD and AWS S3 for file storage."
        ),
        "job_description": (
            "Frontend-focused React developer needed for a fintech startup. "
            "Must have strong TypeScript skills and experience with complex state management. "
            "Backend knowledge is secondary; TypeScript is non-negotiable."
        ),
        "label": 0,
        "reason": (
            "Candidate has React but no TypeScript mentioned — which is flagged non-negotiable. "
            "MERN experience helps partially but the critical gap disqualifies."
        ),
    },

    {
        "id": 5,
        "resume": (
            "Data analyst with 3 years of SQL, Tableau, and Excel experience. "
            "Recently completed a Python for Data Science course; built a few Jupyter notebooks. "
            "No production ML experience."
        ),
        "job_description": (
            "Junior data scientist role — Python and basic Scikit-learn required. "
            "SQL for data extraction; visualisation with Matplotlib or Tableau. "
            "Candidates transitioning from analytics are welcome."
        ),
        "label": 1,
        "reason": (
            "Strong partial match. Job explicitly welcomes analytics-to-DS transitions. "
            "Candidate covers SQL, Tableau, and foundational Python. Borderline-positive."
        ),
    },

    # ══════════════════════════════════════════════════════
    # BLOCK B — SKILL LEVEL DIFFERENCES
    # ══════════════════════════════════════════════════════

    {
        "id": 6,
        "resume": (
            "Computer science graduate with basic knowledge of HTML, CSS, and introductory JavaScript. "
            "Built a static portfolio site and a to-do app following online tutorials. "
            "No professional work experience."
        ),
        "job_description": (
            "React developer needed with 1–2 years of hands-on experience. "
            "Must build reusable components, manage state with hooks, and consume REST APIs. "
            "A small take-home assignment will be part of the interview."
        ),
        "label": 0,
        "reason": (
            "Candidate has only basic HTML/CSS/JS — far below the React + hooks + API integration "
            "required for even a junior role. Skill level mismatch."
        ),
    },

    {
        "id": 7,
        "resume": (
            "Senior software engineer with 7 years of experience in distributed systems. "
            "Expert in Kubernetes, Kafka, and microservices architecture at scale. "
            "Proficient in Python, Go, and cloud-native design patterns on AWS."
        ),
        "job_description": (
            "Mid-level backend developer needed for a startup. "
            "Node.js and basic REST API development experience required. "
            "Docker knowledge helpful; team is small and fast-moving."
        ),
        "label": 1,
        "reason": (
            "Overqualified edge case — candidate far exceeds requirements. "
            "Core backend competency is unambiguously present. "
            "Label=1 since skills match; overqualification is a business decision, not a technical gap."
        ),
    },

    {
        "id": 8,
        "resume": (
            "Intermediate frontend developer with 2 years using Vue.js and Nuxt. "
            "Comfortable with Vuex state management, REST APIs, and SCSS. "
            "No React experience; has not used TypeScript in production."
        ),
        "job_description": (
            "Frontend developer needed — React or Vue.js acceptable. "
            "State management experience required (Redux, Vuex, or Pinia). "
            "TypeScript preferred but not mandatory."
        ),
        "label": 1,
        "reason": (
            "Job explicitly accepts Vue.js as an alternative to React. "
            "Candidate covers Vuex, APIs, and CSS. TypeScript gap is acceptable. Positive match."
        ),
    },

    {
        "id": 9,
        "resume": (
            "Machine learning researcher with PhD in NLP. "
            "Published papers on transformer architectures and multilingual BERT fine-tuning. "
            "Proficient in PyTorch, Hugging Face, and academic experiment pipelines."
        ),
        "job_description": (
            "ML engineer to deploy and monitor models in production. "
            "Requires MLflow, Docker, and experience with CI/CD for ML pipelines. "
            "Research background helpful but production engineering is the priority."
        ),
        "label": 0,
        "reason": (
            "Candidate has deep research skills but lacks the production engineering stack "
            "(MLflow, Docker, CI/CD). Skill depth mismatch — wrong dimension of expertise."
        ),
    },

    {
        "id": 10,
        "resume": (
            "DevOps engineer with 3 years of Docker and Jenkins experience. "
            "Set up CI/CD pipelines for medium-sized teams; familiar with basic AWS EC2 and S3. "
            "No Kubernetes experience; infrastructure managed manually."
        ),
        "job_description": (
            "DevOps engineer needed for container orchestration at scale. "
            "Kubernetes and Helm required; Terraform for infrastructure provisioning. "
            "AWS expertise and CI/CD experience essential."
        ),
        "label": 0,
        "reason": (
            "Candidate covers CI/CD and AWS basics but is missing Kubernetes and Terraform — "
            "both listed as required. Critical gaps in a technically specific role."
        ),
    },

    # ══════════════════════════════════════════════════════
    # BLOCK C — SYNONYM VARIATION & DOMAIN OVERLAP
    # ══════════════════════════════════════════════════════

    {
        "id": 11,
        "resume": (
            "MERN stack developer with experience building full-stack web applications. "
            "Worked on REST APIs, JWT auth, and responsive frontends using React hooks. "
            "Familiar with MongoDB Atlas and basic deployment on Heroku."
        ),
        "job_description": (
            "Looking for a JavaScript full-stack developer for a SaaS product. "
            "Frontend in ReactJS; backend using Express and a NoSQL database. "
            "Experience with authentication flows and cloud deployment required."
        ),
        "label": 1,
        "reason": (
            "Synonym match: MERN = React + Express + MongoDB + Node. "
            "All job requirements covered including auth and deployment. Strong match."
        ),
    },

    {
        "id": 12,
        "resume": (
            "Self-described 'frontend developer' with 4 years of experience. "
            "Expert in React, Next.js, GraphQL, and design systems. "
            "Has built and consumed APIs but limited to client-side concerns."
        ),
        "job_description": (
            "Backend API developer needed for a Node.js service. "
            "Must design schemas, write database queries in PostgreSQL, and handle server logic. "
            "Frontend skills are irrelevant to this role."
        ),
        "label": 0,
        "reason": (
            "Domain mismatch despite both being JavaScript roles. "
            "Candidate is exclusively frontend; job is exclusively backend. Label=0."
        ),
    },

    {
        "id": 13,
        "resume": (
            "Data engineer with 3 years of experience building ETL pipelines in Python. "
            "Used Apache Airflow and PySpark for batch processing; data stored in Snowflake. "
            "Familiar with dbt for data transformations and basic SQL tuning."
        ),
        "job_description": (
            "Seeking a data pipeline engineer to maintain and scale our ingestion infrastructure. "
            "Experience with Spark, Airflow, and cloud data warehouses required. "
            "Python scripting and SQL proficiency essential."
        ),
        "label": 1,
        "reason": (
            "Near-perfect match with synonym alignment: PySpark=Spark, Snowflake=cloud DWH. "
            "All required skills present. Strong positive."
        ),
    },

    {
        "id": 14,
        "resume": (
            "iOS developer with 3 years of Swift and SwiftUI experience. "
            "Knows Xcode, Core Data, and REST API integration for mobile apps. "
            "Recently explored React Native for cross-platform development (1 small project)."
        ),
        "job_description": (
            "React Native developer needed for a cross-platform mobile app. "
            "Must have shipped at least one RN app on both iOS and Android. "
            "Redux and native module integration experience required."
        ),
        "label": 0,
        "reason": (
            "Candidate has minimal React Native exposure (1 project); job demands shipped production RN apps. "
            "iOS native expertise doesn't transfer sufficiently. Near-miss negative."
        ),
    },

    {
        "id": 15,
        "resume": (
            "Cloud engineer with AWS Solutions Architect certification. "
            "Hands-on with EC2, RDS, Lambda, and VPC configuration. "
            "Used Terraform for IaC and has basic Kubernetes knowledge."
        ),
        "job_description": (
            "Cloud infrastructure engineer for a GCP-first organisation. "
            "Must know GKE, Cloud Run, and BigQuery. Terraform experience preferred. "
            "AWS background considered if candidate is willing to learn GCP quickly."
        ),
        "label": 1,
        "reason": (
            "Edge case — job prefers GCP but explicitly allows AWS candidates willing to switch. "
            "Terraform overlap and Kubernetes basics aid transferability. Borderline-positive."
        ),
    },

    # ══════════════════════════════════════════════════════
    # BLOCK D — AMBIGUOUS / BORDERLINE EDGE CASES
    # ══════════════════════════════════════════════════════

    {
        "id": 16,
        "resume": (
            "Backend developer with 5 years in Python Django and PostgreSQL. "
            "Built multi-tenant SaaS platforms with Celery task queues and Redis caching. "
            "No experience with Node.js or JavaScript ecosystems."
        ),
        "job_description": (
            "Backend engineer needed — Python or Node.js both acceptable. "
            "Must have experience with async task queues and caching layers. "
            "Database design skills and SaaS product experience are a strong plus."
        ),
        "label": 1,
        "reason": (
            "Job accepts Python as an alternative to Node. "
            "Candidate's Celery+Redis and SaaS experience directly map to requirements. "
            "Synonym/alternative path match. Positive."
        ),
    },

    {
        "id": 17,
        "resume": (
            "Frontend developer transitioning to full-stack. "
            "Strong React and TypeScript skills; currently learning Node.js via online course. "
            "Built a personal project with Express but no production backend experience."
        ),
        "job_description": (
            "Full-stack developer needed — must be comfortable owning both frontend and backend. "
            "React and Node.js experience required; TypeScript a strong plus. "
            "Startup environment; candidates must work independently."
        ),
        "label": 0,
        "reason": (
            "Frontend skills are strong but backend is self-taught with no production experience. "
            "A startup requiring independent ownership is a high bar — gap is significant. "
            "Borderline but leaning negative."
        ),
    },

    {
        "id": 18,
        "resume": (
            "Data scientist with 4 years of experience in Python, XGBoost, and Scikit-learn. "
            "Specialised in tabular data; deployed models via Flask APIs to production. "
            "No deep learning or NLP experience."
        ),
        "job_description": (
            "Data scientist needed for a recommendation system project. "
            "Experience with collaborative filtering, Scikit-learn, or similar ML libraries required. "
            "Python proficiency essential; deep learning knowledge is a bonus, not required."
        ),
        "label": 1,
        "reason": (
            "Core skills (Python, Scikit-learn, ML modelling, production deployment) match well. "
            "Deep learning listed as optional bonus only. Positive match despite NLP gap."
        ),
    },

    {
        "id": 19,
        "resume": (
            "Software engineer with 6 years primarily in C++ for game engine development. "
            "Strong understanding of memory management, multithreading, and performance optimisation. "
            "Learned Python basics recently; no web or data engineering background."
        ),
        "job_description": (
            "Backend Python developer for a high-performance trading system. "
            "Requires strong Python, async programming, and low-latency optimisation. "
            "Systems programming mindset and performance tuning experience are critical."
        ),
        "label": 0,
        "reason": (
            "Transferable mindset (performance, concurrency) but Python skills are only at beginner level. "
            "Production Python is mandatory here. Strong adjacent skills don't compensate. "
            "Ambiguous but negative due to critical Python gap."
        ),
    },

    {
        "id": 20,
        "resume": (
            "Security engineer with experience in penetration testing and OWASP vulnerability assessments. "
            "Familiar with Docker and basic cloud security on AWS; has written Python automation scripts. "
            "No formal DevOps or infrastructure engineering background."
        ),
        "job_description": (
            "DevSecOps engineer needed to embed security into CI/CD pipelines. "
            "Experience with Docker, AWS security services, and Python scripting required. "
            "Background in security or DevOps equally valued."
        ),
        "label": 1,
        "reason": (
            "Edge case: security background explicitly welcomed alongside DevOps. "
            "Candidate covers Docker, AWS security, and Python. "
            "CI/CD gap exists but isn't disqualifying given the role's dual-track hiring. Borderline-positive."
        ),
    },
]


# ─────────────────────────────────────────────────────────────
# QUICK STATS + CLASSIFICATION DIFFICULTY DISTRIBUTION
# ─────────────────────────────────────────────────────────────

DIFFICULTY_MAP = {
    1:  "partial_match",
    2:  "partial_match",
    3:  "domain_overlap",
    4:  "missing_critical_skill",
    5:  "transition_candidate",
    6:  "skill_level_gap",
    7:  "overqualified",
    8:  "synonym_variation",
    9:  "skill_dimension_mismatch",
    10: "missing_critical_skill",
    11: "synonym_variation",
    12: "domain_mismatch",
    13: "synonym_variation",
    14: "experience_depth_gap",
    15: "platform_transferability",
    16: "alternative_stack_accepted",
    17: "borderline_transition",
    18: "optional_skill_gap",
    19: "language_gap",
    20: "dual_track_hiring",
}

if __name__ == "__main__":
    from collections import Counter

    labels  = [d["label"] for d in advanced_dataset]
    types   = [DIFFICULTY_MAP[d["id"]] for d in advanced_dataset]

    print("=" * 58)
    print(" ADVANCED DATASET v2 — SUMMARY")
    print("=" * 58)
    print(f"  Total examples       : {len(advanced_dataset)}")
    print(f"  Good matches  (1)    : {labels.count(1)}")
    print(f"  Poor matches  (0)    : {labels.count(0)}")
    print()

    print("  Case-type distribution:")
    for case_type, count in Counter(types).most_common():
        print(f"    {case_type:<35} × {count}")
    print()

    # Print all examples in the required output format
    print("=" * 58)
    print(" FULL DATASET  (strict output format)")
    print("=" * 58)
    for d in advanced_dataset:
        print(f"\nResume: {d['resume']}")
        print(f"Job Description: {d['job_description']}")
        print(f"Label: {d['label']}")
        print(f"Reason: {d['reason']}")
        print("-" * 56)
