"""
Resume Analyzer & Job Matcher — Training Data + Skill Normalization
====================================================================
Dataset: 20 labeled (resume, job_description) pairs
Skill Map: 50+ synonym → normalized-skill mappings
"""

# ─────────────────────────────────────────────
# SECTION 1: LABELED TRAINING DATASET
# ─────────────────────────────────────────────

dataset = [

    # ── LABEL 1: GOOD MATCHES ─────────────────────────────────────────

    {
        "resume": (
            "Frontend developer with 3 years of experience in React.js and Redux. "
            "Built responsive UIs using Tailwind CSS and integrated REST APIs. "
            "Familiar with Git, Agile workflows, and basic Node.js."
        ),
        "job_description": (
            "Looking for a React developer to build dynamic web interfaces. "
            "Must know Redux for state management and REST API integration. "
            "Experience with CSS frameworks and Git is required."
        ),
        "label": 1,
    },

    {
        "resume": (
            "Data scientist with expertise in Python, Pandas, and Scikit-learn. "
            "Worked on classification models and customer churn prediction. "
            "Comfortable with Jupyter Notebooks, SQL, and data visualization using Matplotlib."
        ),
        "job_description": (
            "Seeking a data scientist proficient in Python and ML libraries. "
            "Role involves building predictive models and analyzing structured data. "
            "SQL knowledge and visualization skills are a plus."
        ),
        "label": 1,
    },

    {
        "resume": (
            "Backend engineer with 4 years of Node.js and Express.js experience. "
            "Designed RESTful APIs and worked with MongoDB and PostgreSQL. "
            "Familiar with Docker, CI/CD pipelines, and JWT authentication."
        ),
        "job_description": (
            "Backend developer needed with strong Node and Express skills. "
            "Will design and maintain REST APIs connected to NoSQL databases. "
            "Docker knowledge and experience with auth flows preferred."
        ),
        "label": 1,
    },

    {
        "resume": (
            "Full-stack developer experienced in MERN stack applications. "
            "Built e-commerce platforms with user authentication and payment integration. "
            "Proficient in TypeScript, Jest for testing, and AWS S3."
        ),
        "job_description": (
            "Full-stack role requiring React, Node.js, MongoDB, and Express. "
            "Candidate should have experience with TypeScript and cloud storage. "
            "Testing knowledge using Jest or Mocha is a bonus."
        ),
        "label": 1,
    },

    {
        "resume": (
            "Machine learning engineer skilled in TensorFlow and Keras. "
            "Developed CNN models for image classification and NLP pipelines. "
            "Worked with AWS SageMaker and MLflow for model deployment."
        ),
        "job_description": (
            "ML engineer needed to build deep learning models using TensorFlow. "
            "Experience with NLP or computer vision is highly valued. "
            "Cloud deployment experience (AWS or GCP) required."
        ),
        "label": 1,
    },

    {
        "resume": (
            "DevOps engineer with hands-on experience in Docker and Kubernetes. "
            "Set up CI/CD pipelines using Jenkins and GitHub Actions. "
            "Managed cloud infrastructure on AWS and automated deployments."
        ),
        "job_description": (
            "Looking for a DevOps specialist comfortable with container orchestration. "
            "Must know Kubernetes, Docker, and at least one CI/CD tool. "
            "AWS infrastructure management experience is essential."
        ),
        "label": 1,
    },

    {
        "resume": (
            "Data analyst with strong SQL and Excel skills. "
            "Created dashboards in Tableau and Power BI for business stakeholders. "
            "Experience in Python scripting for data cleaning and automation."
        ),
        "job_description": (
            "Data analyst needed for reporting and dashboard creation. "
            "Proficiency in SQL, Tableau, or Power BI is mandatory. "
            "Python scripting ability is a strong advantage."
        ),
        "label": 1,
    },

    {
        "resume": (
            "Android developer with 2 years of experience in Kotlin and Java. "
            "Built apps with MVVM architecture and integrated Firebase for backend. "
            "Published 3 apps on Play Store with 10k+ downloads."
        ),
        "job_description": (
            "Android developer needed with Kotlin experience. "
            "Must understand MVVM design pattern and Firebase integration. "
            "Play Store publishing experience is a plus."
        ),
        "label": 1,
    },

    {
        "resume": (
            "NLP engineer with experience in Hugging Face Transformers and spaCy. "
            "Fine-tuned BERT models for sentiment analysis and named entity recognition. "
            "Familiar with Python, PyTorch, and RESTful API deployment using FastAPI."
        ),
        "job_description": (
            "Seeking an NLP specialist to work on text classification and entity extraction. "
            "Experience with transformer models and Hugging Face library required. "
            "FastAPI or Flask deployment knowledge is expected."
        ),
        "label": 1,
    },

    {
        "resume": (
            "Cloud engineer with AWS certifications and 3 years of hands-on experience. "
            "Provisioned infrastructure using Terraform and managed Lambda functions. "
            "Worked with S3, RDS, EC2, and CloudWatch for monitoring."
        ),
        "job_description": (
            "Cloud infrastructure engineer needed with AWS expertise. "
            "Role involves IaC using Terraform and serverless architecture. "
            "Knowledge of S3, EC2, and monitoring tools is required."
        ),
        "label": 1,
    },

    # ── LABEL 0: POOR MATCHES ─────────────────────────────────────────

    {
        "resume": (
            "Graphic designer with expertise in Adobe Photoshop, Illustrator, and InDesign. "
            "Designed brand identities, print media, and social media creatives. "
            "No programming experience."
        ),
        "job_description": (
            "Frontend developer needed with React.js and CSS skills. "
            "Must build interactive web apps and integrate APIs. "
            "Experience with JavaScript frameworks is required."
        ),
        "label": 0,
    },

    {
        "resume": (
            "Java backend developer with Spring Boot and Hibernate experience. "
            "Worked with MySQL and Oracle databases in enterprise environments. "
            "Familiar with Maven, JUnit, and microservices."
        ),
        "job_description": (
            "Data scientist role requiring Python, Pandas, and Scikit-learn. "
            "Candidate must build ML models and analyze large datasets. "
            "Experience with TensorFlow or PyTorch preferred."
        ),
        "label": 0,
    },

    {
        "resume": (
            "iOS developer skilled in Swift and SwiftUI. "
            "Built finance and fitness apps with Core Data and CloudKit integration. "
            "No web development experience."
        ),
        "job_description": (
            "Full-stack web developer needed for MERN stack product. "
            "Must work on React frontend and Node.js backend services. "
            "MongoDB and REST API skills are essential."
        ),
        "label": 0,
    },

    {
        "resume": (
            "Business analyst with experience in requirement gathering and stakeholder communication. "
            "Proficient in MS Excel, PowerPoint, and JIRA for project tracking. "
            "No technical coding skills."
        ),
        "job_description": (
            "Backend Node.js developer needed to build scalable APIs. "
            "Must know Express, Redis, and PostgreSQL. "
            "Experience with WebSockets is a bonus."
        ),
        "label": 0,
    },

    {
        "resume": (
            "SEO specialist with 4 years of experience in search engine optimization. "
            "Proficient with Google Analytics, Ahrefs, and SEMrush. "
            "Strong content strategy and keyword research skills."
        ),
        "job_description": (
            "DevOps engineer needed with Docker and Kubernetes expertise. "
            "Must automate CI/CD pipelines and manage cloud infrastructure. "
            "Experience with Terraform and Ansible is required."
        ),
        "label": 0,
    },

    {
        "resume": (
            "Data entry specialist with fast typing skills and Excel proficiency. "
            "Experience with CRM tools like Salesforce for data management. "
            "No programming or ML background."
        ),
        "job_description": (
            "Machine learning engineer to develop NLP models and pipelines. "
            "Requires Python, PyTorch, and experience with large language models. "
            "Deployment using Docker and AWS is expected."
        ),
        "label": 0,
    },

    {
        "resume": (
            "Content writer with expertise in technical writing and blog creation. "
            "Experienced in WordPress, SEO writing, and CMS tools. "
            "No software development or database skills."
        ),
        "job_description": (
            "Database administrator needed with MySQL and PostgreSQL expertise. "
            "Must handle query optimization, backups, and schema design. "
            "Redis caching knowledge is a plus."
        ),
        "label": 0,
    },

    {
        "resume": (
            "Network engineer with Cisco CCNA certification. "
            "Managed LAN/WAN infrastructure, VPN configurations, and firewall rules. "
            "No experience with web development or programming languages."
        ),
        "job_description": (
            "React.js developer needed for a SaaS dashboard product. "
            "Must have strong TypeScript and GraphQL skills. "
            "Experience with testing libraries like Jest or RTL is preferred."
        ),
        "label": 0,
    },

    {
        "resume": (
            "Unity game developer with C# expertise. "
            "Developed 2D/3D mobile games with physics simulations and AR features. "
            "No background in web APIs or cloud services."
        ),
        "job_description": (
            "Cloud solutions architect required with AWS and GCP experience. "
            "Must design multi-cloud architectures and lead migration projects. "
            "Terraform and Kubernetes knowledge is mandatory."
        ),
        "label": 0,
    },

    {
        "resume": (
            "HR manager with 6 years of experience in recruitment and employee relations. "
            "Skilled in HRMS tools, onboarding, and performance management. "
            "No technical or data science skills."
        ),
        "job_description": (
            "Data engineer needed to build ETL pipelines using Apache Spark. "
            "Must know Python, Airflow, and cloud data warehouses like BigQuery. "
            "Experience with Kafka for real-time streaming is preferred."
        ),
        "label": 0,
    },
]


# ─────────────────────────────────────────────
# SECTION 2: SKILL SYNONYM → NORMALIZED MAPPING
# ─────────────────────────────────────────────

skill_normalization_map = {

    # ── WEB DEVELOPMENT: JavaScript / Frameworks ──────────────────────
    "react":                   "react",
    "react.js":                "react",
    "reactjs":                 "react",
    "react js":                "react",
    "react framework":         "react",

    "vue":                     "vue",
    "vue.js":                  "vue",
    "vuejs":                   "vue",

    "angular":                 "angular",
    "angularjs":               "angular",
    "angular.js":              "angular",
    "angular 2+":              "angular",

    "next.js":                 "nextjs",
    "nextjs":                  "nextjs",
    "next js":                 "nextjs",

    "javascript":              "javascript",
    "js":                      "javascript",
    "es6":                     "javascript",
    "es2015":                  "javascript",
    "vanilla js":              "javascript",
    "ecmascript":              "javascript",

    "typescript":              "typescript",
    "ts":                      "typescript",

    "html":                    "html",
    "html5":                   "html",

    "css":                     "css",
    "css3":                    "css",

    "tailwind":                "tailwind",
    "tailwind css":            "tailwind",
    "tailwindcss":             "tailwind",

    "bootstrap":               "bootstrap",
    "bootstrap 5":             "bootstrap",

    "graphql":                 "graphql",
    "graph ql":                "graphql",

    # ── WEB DEVELOPMENT: Stacks ───────────────────────────────────────
    "mern":                    "react node mongodb express",
    "mern stack":              "react node mongodb express",
    "mean":                    "angular node mongodb express",
    "mean stack":              "angular node mongodb express",
    "lamp":                    "linux apache mysql php",
    "jamstack":                "javascript api markup",
    "full stack":              "frontend backend",
    "fullstack":               "frontend backend",

    # ── BACKEND ───────────────────────────────────────────────────────
    "node":                    "nodejs",
    "node.js":                 "nodejs",
    "nodejs":                  "nodejs",

    "express":                 "expressjs",
    "express.js":              "expressjs",
    "expressjs":               "expressjs",

    "django":                  "django",
    "flask":                   "flask",
    "fastapi":                 "fastapi",
    "fast api":                "fastapi",

    "spring":                  "spring",
    "spring boot":             "spring",
    "springboot":              "spring",

    "laravel":                 "laravel",
    "symfony":                 "symfony",

    "rest":                    "rest_api",
    "rest api":                "rest_api",
    "restful":                 "rest_api",
    "restful api":             "rest_api",
    "api development":         "rest_api",

    # ── DATABASES ─────────────────────────────────────────────────────
    "mongo":                   "mongodb",
    "mongodb":                 "mongodb",
    "mongo db":                "mongodb",

    "mysql":                   "mysql",
    "my sql":                  "mysql",

    "postgres":                "postgresql",
    "postgresql":              "postgresql",
    "postgres sql":            "postgresql",

    "sqlite":                  "sqlite",
    "sqlite3":                 "sqlite",

    "redis":                   "redis",
    "redis cache":             "redis",

    "elasticsearch":           "elasticsearch",
    "elastic search":          "elasticsearch",

    "cassandra":               "cassandra",
    "apache cassandra":        "cassandra",

    "oracle":                  "oracle_db",
    "oracle db":               "oracle_db",
    "oracle database":         "oracle_db",

    "sql":                     "sql",
    "structured query language": "sql",
    "nosql":                   "nosql",
    "no-sql":                  "nosql",

    "bigquery":                "bigquery",
    "google bigquery":         "bigquery",

    "snowflake":               "snowflake",

    # ── DATA SCIENCE & ML ─────────────────────────────────────────────
    "python":                  "python",
    "py":                      "python",

    "pandas":                  "pandas",
    "numpy":                   "numpy",
    "np":                      "numpy",

    "scikit-learn":            "sklearn",
    "sklearn":                 "sklearn",
    "scikit learn":            "sklearn",

    "tensorflow":              "tensorflow",
    "tf":                      "tensorflow",

    "pytorch":                 "pytorch",
    "torch":                   "pytorch",

    "keras":                   "keras",

    "hugging face":            "huggingface",
    "huggingface":             "huggingface",
    "transformers":            "huggingface",

    "bert":                    "bert",
    "gpt":                     "gpt",
    "llm":                     "large_language_model",
    "large language model":    "large_language_model",

    "spacy":                   "spacy",
    "nltk":                    "nltk",

    "mlflow":                  "mlflow",
    "sagemaker":               "aws_sagemaker",
    "aws sagemaker":           "aws_sagemaker",

    "jupyter":                 "jupyter",
    "jupyter notebook":        "jupyter",
    "ipynb":                   "jupyter",

    "matplotlib":              "matplotlib",
    "seaborn":                 "seaborn",

    "tableau":                 "tableau",
    "power bi":                "powerbi",
    "powerbi":                 "powerbi",

    "apache spark":            "spark",
    "pyspark":                 "spark",
    "spark":                   "spark",

    "apache kafka":            "kafka",
    "kafka":                   "kafka",

    "airflow":                 "airflow",
    "apache airflow":          "airflow",

    # ── CLOUD & DEVOPS ────────────────────────────────────────────────
    "aws":                     "aws",
    "amazon web services":     "aws",

    "gcp":                     "gcp",
    "google cloud":            "gcp",
    "google cloud platform":   "gcp",

    "azure":                   "azure",
    "microsoft azure":         "azure",

    "docker":                  "docker",
    "containers":              "docker",

    "kubernetes":              "kubernetes",
    "k8s":                     "kubernetes",

    "terraform":               "terraform",
    "iac":                     "infrastructure_as_code",
    "infrastructure as code":  "infrastructure_as_code",

    "jenkins":                 "jenkins",
    "github actions":          "github_actions",
    "ci/cd":                   "cicd",
    "cicd":                    "cicd",
    "continuous integration":  "cicd",

    # ── MOBILE ───────────────────────────────────────────────────────
    "react native":            "react_native",
    "flutter":                 "flutter",
    "swift":                   "swift",
    "kotlin":                  "kotlin",
    "android":                 "android",
    "ios":                     "ios",
}


# ─────────────────────────────────────────────
# SECTION 3: QUICK STATS
# ─────────────────────────────────────────────

if __name__ == "__main__":
    labels = [d["label"] for d in dataset]
    print(f"Total examples     : {len(dataset)}")
    print(f"Good matches (1)   : {labels.count(1)}")
    print(f"Poor matches (0)   : {labels.count(0)}")
    print(f"Skill mappings     : {len(skill_normalization_map)}")
    print()

    # Pretty-print a few examples
    for i, item in enumerate(dataset[:3], 1):
        print(f"─── Example {i} {'(Match)' if item['label'] else '(No Match)'} ───")
        print(f"  Resume : {item['resume'][:80]}...")
        print(f"  Job    : {item['job_description'][:80]}...")
        print(f"  Label  : {item['label']}")
        print()

    # Demo normalization
    print("─── Skill Normalization Demos ───")
    test_terms = ["React.js", "MERN", "node.js", "scikit-learn", "k8s", "hugging face"]
    for term in test_terms:
        normalized = skill_normalization_map.get(term.lower(), "NOT FOUND")
        print(f"  '{term}' → '{normalized}'")
