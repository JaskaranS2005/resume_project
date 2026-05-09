# CAPSTONE PROJECT REPORT

**Project Term:** January-May 2026

## Resume Matcher: Intelligent Resume-to-Job Description Matching with Explainable Feedback

Submitted by

| Name of Student | Registration Number |
| --- | --- |
| Jaskaran Singh | __________________ |
| Name of Student 2 | __________________ |
| Name of Student 3 | __________________ |
| Name of Student 4 | __________________ |

Project Group Number: __________________

Course Code: __________________

Under the Guidance of

Name of faculty mentor with designation: __________________

School of Computer Science and Engineering

---

## DECLARATION

We hereby declare that the project work entitled **Resume Matcher: Intelligent Resume-to-Job Description Matching with Explainable Feedback** is an authentic record of our own work carried out as requirements of Capstone Project for the award of B.Tech Computer Science and Engineering from Lovely Professional University, Phagwara, under the guidance of **Name of Faculty Mentor**, during January-May 2026. All the information furnished in this capstone project report is based on our own intensive work and is genuine.

Project Group Number: __________________

| Student | Registration Number | Signature | Date |
| --- | --- | --- | --- |
| Jaskaran Singh | __________________ | __________________ | __________________ |
| Name of Student 2 | __________________ | __________________ | __________________ |
| Name of Student 3 | __________________ | __________________ | __________________ |
| Name of Student 4 | __________________ | __________________ | __________________ |

---

## CERTIFICATE

This is to certify that the declaration statement made by this group of students is correct to the best of my knowledge and belief. They have completed this Capstone Project under my guidance and supervision. The present work is the result of their original investigation, effort and study. No part of the work has ever been submitted for any other degree at any University. The Capstone Project is fit for submission and partial fulfillment of the conditions for the award of B.Tech Computer Science and Engineering from Lovely Professional University, Phagwara.

Signature and Name of the Mentor: __________________

Designation: __________________

School of Computer Science and Engineering, Lovely Professional University, Phagwara

Date: __________________

---

## ACKNOWLEDGEMENT

We express sincere gratitude to our faculty mentor, the School of Computer Science and Engineering, and Lovely Professional University, Phagwara for their guidance and support throughout the development of this project. We also thank our peers and evaluators for their suggestions, which helped improve the clarity, usability, and technical quality of the system.

---

## TABLE OF CONTENTS

- Inner first page ...... i
- PAC form ...... ii
- Declaration ...... iii
- Certificate ...... iv
- Acknowledgement ...... v
- Table of Contents ...... vi
- 1. INTRODUCTION ...... 1
- 2. PROFILE OF THE PROBLEM, RATIONALE AND SCOPE OF THE STUDY ...... 3
- 3. EXISTING SYSTEM ...... 5
- 4. PROBLEM ANALYSIS ...... 8
- 5. SOFTWARE REQUIREMENT ANALYSIS ...... 11
- 6. DESIGN ...... 15
- 7. TESTING ...... 22
- 8. IMPLEMENTATION ...... 27
- 9. PROJECT LEGACY ...... 31
- 10. USER MANUAL ...... 34
- 11. SOURCE CODE AND SYSTEM SNAPSHOTS ...... 39
- 12. BIBLIOGRAPHY ...... 45

---

## 1. INTRODUCTION

Resume Matcher is a Python and Streamlit based software project designed to compare a candidate resume with a target job description. The system extracts text from uploaded resume files, preprocesses both resume and job description text, computes a deterministic match score, and generates improvement-oriented feedback through a configurable LLM provider.

The project addresses a practical problem in modern recruitment. Candidates often submit resumes without knowing whether their skills, keywords, project experience, and proficiency depth match the expectations of a specific role. Recruiters, meanwhile, need fast early-stage screening support without losing transparency. Resume Matcher provides a lightweight and explainable bridge between these needs.

The system is not intended to replace human judgment. Its purpose is to help users identify alignment gaps, improve resume quality, and understand why a job description may or may not match their current profile. The design keeps the scoring layer deterministic and treats AI feedback as an optional explanation layer.

### 1.1. OBJECTIVES OF THE PROJECT

- To develop an interactive application for resume and job description comparison.
- To extract text from PDF and image resumes.
- To normalize noisy resume and job description text before matching.
- To calculate a match score using TF-IDF cosine similarity and a depth-gap penalty.
- To generate practical feedback through Groq, OpenRouter, or Gemini when configured.
- To keep the application modular, testable, and suitable for academic evaluation.

### 1.2. TECHNOLOGY USED

- Frontend and application framework: Streamlit.
- Programming language: Python.
- Text processing and scoring: scikit-learn, TF-IDF, cosine similarity.
- Document extraction: PyPDF2 for PDF files and pytesseract with Pillow for images.
- Configuration: python-dotenv and environment variables.
- Testing: pytest-based unit and workflow tests.

---

## 2. PROFILE OF THE PROBLEM, RATIONALE AND SCOPE OF THE STUDY

A resume is usually the first structured representation of a candidate's academic background, technical skills, experience, and project work. However, the same resume may be strong for one job and weak for another because every job description emphasizes different tools, skills, experience levels, and responsibilities. This creates uncertainty for candidates and makes resume improvement difficult.

The problem becomes more serious in technical hiring, where small terminology gaps can reduce visibility in screening systems. A candidate may know Python, machine learning, or databases, but if the resume does not express those skills with the depth and wording expected by the job description, the candidate may appear less suitable than they actually are.

### 2.1. PROBLEM STATEMENT

Candidates need a reliable way to understand how well their resume matches a given job description and what improvements should be made before applying. Existing keyword-based tools often provide shallow results, while purely AI-based tools may produce feedback without transparent scoring. This project studies and develops an explainable software system that combines deterministic text similarity with optional AI guidance.

### 2.2. RATIONALE OF THE STUDY

- The rationale for this study is to build a practical tool that improves decision-making for job applicants. By showing a score, depth gap, detected signals, and improvement suggestions, the system helps users revise resumes in a targeted way.
- The study is also academically useful because it demonstrates applied natural language processing, OCR/PDF extraction, modular software design, error handling, provider-based API integration, and test-driven quality improvement.

### 2.3. SCOPE OF THE STUDY

- The study includes resume uploads in PDF, PNG, JPG, and JPEG formats.
- The study includes custom job descriptions and role-template based job descriptions.
- The study includes local scoring using cleaned text features and TF-IDF similarity.
- The study includes optional feedback generation through configured LLM providers.
- The study does not include production ATS integration, user accounts, database storage, or multi-resume recruiter ranking.

---

## 3. EXISTING SYSTEM

Existing resume screening approaches can be grouped into manual review, keyword matching systems, applicant tracking systems, and AI resume review tools. Each approach solves part of the problem but also introduces limitations.

### 3.1. INTRODUCTION

Manual resume review is accurate when performed carefully but is slow and subjective. Keyword tools are fast but may ignore context and proficiency depth. Commercial ATS platforms are useful for recruiters but are usually not transparent to candidates. AI writing tools can generate suggestions but may not explain the scoring method.

### 3.2. EXISTING SOFTWARE

- Keyword resume scanners compare terms but often miss semantic intent.
- Applicant tracking systems filter and rank applicants but provide limited feedback to candidates.
- Generic AI assistants can rewrite resumes but may not quantify role fit consistently.
- Online resume analyzers may require external uploads, creating privacy concerns.

### 3.3. DFD FOR PRESENT SYSTEM

- In a typical existing process, the candidate submits a resume, a recruiter or ATS reads the resume, keywords are checked against job criteria, and the candidate is shortlisted or rejected. Feedback is usually absent or generic.
- Candidate -> Resume Submission -> Manual/ATS Screening -> Shortlist Decision -> Limited Feedback

### 3.4. WHAT IS NEW IN THE SYSTEM TO BE DEVELOPED

- The proposed system gives candidates an immediate score and improvement feedback.
- The deterministic score is separate from LLM feedback, improving explainability.
- The system supports multiple LLM providers without making the core score dependent on them.
- Depth-related terms such as basic, familiar, advanced, and expert are considered in the scoring logic.
- The application remains usable even when AI provider keys are missing or provider APIs fail.

---

## 4. PROBLEM ANALYSIS

Problem analysis identifies the product definition, feasibility, and plan for development. The main challenge is to design a system that is simple enough to run locally but meaningful enough to provide useful matching insight.

### 4.1. PRODUCT DEFINITION

- Resume Matcher is an interactive software tool where the user uploads a resume and provides a job description. The system extracts text, preprocesses content, computes a match score, displays score components, and optionally generates feedback.
- Primary users are students, job seekers, and early-career professionals preparing role-specific resumes.

### 4.2. FEASIBILITY ANALYSIS

- Technical feasibility: Python, Streamlit, scikit-learn, PyPDF2, and pytesseract provide the needed implementation support.
- Operational feasibility: The interface is simple enough for non-technical users to upload files and read results.
- Economic feasibility: The local scoring pipeline has negligible cost; LLM costs are optional and provider-dependent.
- Schedule feasibility: A modular pipeline allows development, testing, and improvement in separate phases.

### 4.3. PROJECT PLAN

- Phase 1: Requirement analysis and project setup.
- Phase 2: Resume extraction and preprocessing implementation.
- Phase 3: Similarity scoring and depth-gap logic.
- Phase 4: Streamlit UI development.
- Phase 5: LLM provider integration.
- Phase 6: Testing, bug fixing, documentation, and report preparation.

---

## 5. SOFTWARE REQUIREMENT ANALYSIS

Software Requirement Analysis defines the expected behavior, constraints, and qualities of the system. The requirements were chosen to keep the application useful, explainable, and easy to run in a local academic environment.

### 5.1. INTRODUCTION

- The system must accept resume input, collect a job description, process text, calculate score, and present feedback.
- The system should degrade gracefully when optional dependencies or provider APIs are unavailable.

### 5.2. GENERAL DESCRIPTION

- The application is a single-user local web application.
- The user interacts with the system through a Streamlit interface.
- The application does not permanently store uploaded resumes.
- Provider secrets are loaded from environment variables rather than hardcoded in source code.

### 5.3. SPECIFIC REQUIREMENTS

- FR1: The user shall be able to upload a PDF or image resume.
- FR2: The user shall be able to select or enter a job description.
- FR3: The system shall extract text from the uploaded resume.
- FR4: The system shall preprocess resume and job description text.
- FR5: The system shall compute similarity, depth gap, and final score.
- FR6: The system shall display detected depth signals.
- FR7: The system shall request AI feedback when a provider is configured.
- NFR1: The system shall avoid crashes for empty extracted text.
- NFR2: The system shall keep scoring deterministic for the same inputs.
- NFR3: The system shall keep API keys outside committed source files.

| Requirement ID | Description | Priority |
| --- | --- | --- |
| FR1 | Upload PDF or image resume | High |
| FR2 | Enter or select job description | High |
| FR3 | Extract and preprocess text | High |
| FR4 | Compute final score and depth gap | High |
| FR5 | Generate optional AI feedback | Medium |
| NFR1 | Graceful handling of empty or invalid input | High |

---

## 6. DESIGN

The design follows a layered architecture. Each module handles one main concern so that the project is easier to test, debug, and extend.

### 6.1. SYSTEM DESIGN

- Presentation Layer: app.py renders the Streamlit interface and coordinates the workflow.
- CLI Layer: main.py supports a simple terminal-based workflow.
- Extraction Layer: utils/file_extractor.py converts PDF and image resumes into text.
- Preprocessing Layer: preprocessing/preprocessing_pipeline.py cleans text and extracts depth signals.
- Scoring Layer: model/model.py computes similarity and final score.
- Feedback Layer: utils/llm_helper.py routes prompts to the configured LLM provider.

| Layer | Module | Responsibility |
| --- | --- | --- |
| Presentation | app.py | Streamlit UI and workflow coordination |
| Extraction | utils/file_extractor.py | Text extraction from PDF and images |
| Preprocessing | preprocessing_pipeline.py | Text cleaning and feature creation |
| Scoring | model/model.py | TF-IDF similarity and score calculation |
| Feedback | utils/llm_helper.py | LLM provider routing and feedback |

### 6.2. DESIGN NOTATIONS

- External entity: User and external LLM provider.
- Process: Extraction, preprocessing, scoring, and feedback generation.
- Data flow: Resume text, job description text, score, and feedback.
- Data store: Temporary uploaded file and environment configuration.

### 6.3. DETAILED DESIGN

- The UI validates input and passes uploaded files to extraction functions.
- The extraction module returns plain text or an empty string for recoverable failures.
- The preprocessing module normalizes text and produces structured features.
- The scoring module uses TF-IDF vectorization and cosine similarity.
- The feedback module constructs a role-aware prompt and returns recommendations or a controlled error message.

### 6.4. FLOWCHART

- Start -> Upload Resume -> Enter Job Description -> Extract Text -> Preprocess Text -> Compute Score -> Generate Feedback -> Display Result -> End
- Decision points include file type validation, empty text handling, and provider availability.

### 6.5. PSEUDO CODE

- Receive resume file and job description.
- If resume file is PDF, extract text using PDF parser; otherwise extract text using OCR.
- Clean resume text and job description text.
- Build TF-IDF vectors for both documents.
- Compute cosine similarity.
- Calculate depth gap and apply penalty.
- Clamp final score between 0 and 1.
- Request AI feedback if provider settings are available.
- Display score, signals, extracted text preview, and recommendations.

---

## 7. TESTING

Testing was performed to validate extraction, preprocessing, scoring, and provider error handling behavior. The project includes pytest-based tests for deterministic verification.

### 7.1. FUNCTIONAL TESTING

- Resume upload and text extraction were checked for supported file types.
- Job description input was checked through template and custom text paths.
- Score output was checked for valid numeric range.
- Provider failure messages were checked for controlled error rendering.

### 7.2. STRUCTURAL TESTING

- Core functions were tested independently from the UI.
- The scoring model was tested for empty input handling.
- Preprocessing functions were tested for normalization behavior.
- Optional imports were guarded to avoid import-time application crashes.

### 7.3. LEVELS OF TESTING

- Unit testing: individual preprocessing and scoring functions.
- Integration testing: extraction, preprocessing, scoring, and feedback path.
- System testing: complete Streamlit workflow using representative resumes and job descriptions.
- Regression testing: tests added after bug fixes to prevent repeat failures.

### 7.4. TESTING THE PROJECT

- The test suite can be executed using pytest -q.
- Expected result: all deterministic tests should pass in a correctly configured environment.
- Manual testing should include PDF resume, image resume, empty resume, missing API key, and invalid provider key cases.

| Test Area | File | Expected Outcome |
| --- | --- | --- |
| Scoring | test_model.py | Valid score range and empty text handling |
| Preprocessing | test_preprocessing.py | Cleaned features and normalized tokens |
| PDF extraction | test_pdf.py | PDF text extraction path works |
| Image extraction | test_image.py | OCR extraction path works when dependencies exist |

---

## 8. IMPLEMENTATION

Implementation was completed as a modular Python project. The system uses Streamlit for the web interface and separate Python modules for extraction, preprocessing, scoring, and LLM feedback.

### 8.1. IMPLEMENTATION OF THE PROJECT

- app.py implements the user interface and main workflow.
- main.py provides a simple command-line workflow.
- utils/file_extractor.py handles PDF and image text extraction.
- preprocessing/preprocessing_pipeline.py cleans text and extracts depth signals.
- model/model.py calculates similarity and final score.
- utils/llm_helper.py integrates Groq, OpenRouter, and Gemini provider paths.

### 8.2. CONVERSION PLAN

- The project can be moved from local prototype to hosted deployment by containerizing the app.
- Secrets should be moved from local .env files to deployment environment variables.
- OCR dependencies should be installed in the deployment image if image resume support is required.
- Future versions can add database storage only after privacy and consent controls are designed.

### 8.3. POST-IMPLEMENTATION AND SOFTWARE MAINTENANCE

- Maintain tests for scoring and preprocessing whenever logic changes.
- Update provider handling when API SDKs or endpoints change.
- Review .env.example and requirements.txt after dependency changes.
- Add logging for extraction failures and provider response failures.
- Keep uploaded resume handling privacy-preserving and temporary.

---

## 9. PROJECT LEGACY

Project legacy records the current state of the project, remaining concerns, and learning outcomes. This is important because the system can be extended into a stronger resume coaching platform in future work.

### 9.1. CURRENT STATUS OF THE PROJECT

- The current project supports resume upload, job description input, text extraction, preprocessing, scoring, and optional AI feedback.
- The repository includes documentation, environment examples, and test files.
- Important runtime failures such as empty-vocabulary scoring crashes and fragile provider imports have been addressed.

### 9.2. REMAINING AREAS OF CONCERN

- OCR quality may vary for low-resolution images.
- TF-IDF similarity may miss deeper semantic similarity between differently worded experience.
- LLM feedback quality depends on provider availability, model quality, and prompt behavior.
- The system does not yet include authentication, persistent history, or recruiter-side batch ranking.

### 9.3. TECHNICAL AND MANAGERIAL LESSONS LEARNT

- A transparent baseline model is easier to debug than a fully black-box model.
- Optional dependencies should be guarded so one missing library does not break the whole application.
- Error messages should be controlled and user-readable.
- Tests are most valuable when they cover known failure modes.
- Clear documentation improves reproducibility and project handover.

---

## 10. USER MANUAL

This user manual explains how to install, run, and use the Resume Matcher application.

### 10.1. INSTALLATION

- Install Python 3.10 or later.
- Create a virtual environment using python -m venv .venv.
- Activate the virtual environment.
- Install dependencies using pip install -r requirements.txt.
- For image OCR, install Tesseract on the system.

### 10.2. CONFIGURATION

- Copy .env.example to .env.
- Set LLM_PROVIDER to groq, openrouter, or gemini.
- Add the matching API key for the selected provider.
- If no provider is configured, deterministic scoring can still be used.

### 10.3. RUNNING THE APPLICATION

- Open a terminal in the project directory.
- Run streamlit run app.py.
- Open the local Streamlit URL shown in the terminal.
- Upload a resume and enter or select a job description.
- Click the matching action and review the score and feedback.

### 10.4. INTERPRETING RESULTS

- Final score shows overall resume-job fit as a percentage.
- Similarity score shows raw text similarity between resume and job description.
- Depth gap shows difference between expected and demonstrated proficiency depth.
- AI feedback suggests missing skills, phrasing improvements, and resume strengthening steps.

---

## 11. SOURCE CODE AND SYSTEM SNAPSHOTS

The source code is organized into clearly separated modules. Important files are listed below.

### 11.1. SOURCE CODE STRUCTURE

- app.py: Streamlit user interface and workflow coordination.
- main.py: Command-line workflow.
- model/model.py: Similarity and final scoring logic.
- preprocessing/preprocessing_pipeline.py: Text cleaning and feature construction.
- utils/file_extractor.py: PDF and image text extraction.
- utils/llm_helper.py: LLM provider routing and feedback generation.
- test_model.py, test_preprocessing.py, test_pdf.py, test_image.py: test files.

### 11.2. SYSTEM SNAPSHOTS

- Snapshot 1: Home page with resume upload and job description input.
- Snapshot 2: Match score dashboard showing score, similarity, and depth gap.
- Snapshot 3: Extracted resume text preview.
- Snapshot 4: AI feedback panel with recommendations.
- Actual screenshots can be inserted in this chapter after running the Streamlit application.

---

## 12. BIBLIOGRAPHY

Streamlit Documentation. https://docs.streamlit.io/

scikit-learn Documentation. https://scikit-learn.org/stable/

Python Documentation. https://docs.python.org/3/

PyPDF2 Documentation. https://pypdf2.readthedocs.io/

Tesseract OCR Documentation. https://tesseract-ocr.github.io/

OpenAI, Groq, Gemini, and OpenRouter provider documentation for LLM API integration concepts.

Project source files and local documentation from the Resume Matcher repository.

---
