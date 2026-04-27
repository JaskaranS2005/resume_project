# Resume Matcher Project Report

## Title

**Resume Matcher: Intelligent Resume-to-Job Description Matching with Explainable Feedback**

## Author

Jaskaran Singh  
Department: Computer Science / Software Engineering  
Project Type: Applied ML + NLP + Product Engineering  
Submission Date: April 2026

---

## Abstract

This report presents the design, implementation, testing, and improvement of **Resume Matcher**, a practical software system that compares candidate resumes against target job descriptions and generates both a quantitative score and qualitative improvement feedback. The core problem addressed is the mismatch between resume content and role requirements, which is a frequent cause of candidate rejection in technical hiring pipelines.

The system combines three major components: (1) text extraction from PDF/image resumes, (2) preprocessing and feature engineering for normalized comparison, and (3) a scoring and feedback layer that blends deterministic similarity metrics with LLM-based guidance. The scoring pipeline uses TF-IDF cosine similarity with a custom depth-gap penalty to account for differences in proficiency expression (for example, “basic” vs “advanced”).

In addition to functionality, the project emphasizes robustness and maintainability. During the bug-fix phase, major runtime failures were addressed: empty-vocabulary crashes in similarity computation, provider-import coupling issues, fragile test scripts, and inconsistent error signaling to the UI. The test suite was converted into deterministic pytest-based tests and validated with full passing results.

The final result is an end-to-end, user-facing tool that is lightweight, extensible to multiple LLM providers (Groq, OpenRouter, Gemini), and suitable for further deployment and academic extension. This report documents architecture decisions, algorithmic tradeoffs, implementation details, test outcomes, and future improvement opportunities.

---

## 1. Introduction

Recruitment systems today rely heavily on digital resumes and role-specific screening criteria. Candidates often struggle to understand whether their resume aligns with a job description, while recruiters face high-volume filtering problems. Manual review does not scale effectively, and opaque screening systems leave users without actionable feedback.

Resume Matcher was built as a middle path: a transparent, explainable, and locally computable matching system that gives practical guidance instead of only a raw score. The goal is not to replace recruiters but to support candidates in iterative resume improvement and support initial signal extraction in hiring workflows.

Unlike black-box ranking models, this project keeps core scoring interpretable. Similarity is computed over cleaned and normalized text; depth indicators provide an explicit adjustment term; and LLM feedback is treated as an explanatory layer, not a scoring authority. This separation improves trust and debugging capacity.

The application is implemented using Python and Streamlit for rapid UI delivery, with modular folders for extraction, preprocessing, model scoring, and provider integrations. This modularity made it possible to improve quality late in development without rewriting the whole stack.

The project is both educational and practical: it demonstrates applied NLP engineering, software quality improvements, API integration design, and product-focused UX thinking under realistic constraints.

---

## 2. Problem Statement

Candidates commonly ask three questions before applying to a role:

1. How strong is my resume fit for this job?
2. Which specific skills or experiences are missing?
3. What should I improve first to raise my chances?

Most available tools answer poorly:

- Some provide only keyword counts with low semantic value.
- Some use generic AI text generation without reproducible scoring logic.
- Some fail on noisy resumes (broken words, OCR artifacts, abbreviation-heavy content).

The problem addressed by this project is to design a resume-job matching system that is:

- **Explainable** in its numeric scoring,
- **Practical** in its improvement recommendations,
- **Resilient** to common text noise and API failures,
- **Usable** as a web application by non-technical users.

The system should support different LLM providers without breaking scoring if API keys are missing or provider endpoints fail. This requirement became critical during development when provider-level failures (invalid keys, 503 upstream issues, rate limits) were observed.

The project therefore treats matching as a hybrid pipeline:

- deterministic local scoring for reliability,
- optional AI guidance for personalized interpretation.

This architecture ensures that even with AI unavailable, the user still gets meaningful output.

---

## 3. Objectives

### Primary Objectives

- Build an interactive app to upload resumes and compare them with job descriptions.
- Compute a score reflecting textual alignment and skill-depth mismatch.
- Generate improvement-oriented feedback aligned with the target role.

### Technical Objectives

- Support PDF and image extraction paths.
- Normalize noisy text through an extensible preprocessing pipeline.
- Integrate multiple LLM providers through environment-based routing.
- Handle provider errors gracefully without crashing the UI.

### Quality Objectives

- Convert ad-hoc scripts into deterministic tests.
- Eliminate import-time crashes from optional dependencies.
- Document setup and architecture clearly for reproducibility.
- Clean unnecessary project artifacts and improve repository hygiene.

### Evaluation Objectives

- Verify that core pipeline functions execute on noisy inputs.
- Ensure all test cases pass under standard local setup.
- Confirm the app returns controlled errors for missing/invalid API settings.

These objectives were progressively achieved through iterative development and a dedicated bug-fix phase.

---

## 4. Scope and Constraints

### Scope Included

- Resume text extraction from PDF and images.
- Rule-based text cleaning and normalization for resume/JD input.
- Similarity-based scoring with depth penalty.
- LLM-based explanation via selectable providers.
- Web UI for upload, scoring display, and feedback presentation.

### Scope Excluded

- ATS integration with external hiring systems.
- Candidate ranking across multiple resumes.
- Deep learning embedding models for semantic search.
- Persistent database and user account management.
- Production-grade cloud deployment automation.

### Constraints

- Limited compute budget favored lightweight classical NLP (TF-IDF) over transformer encoders.
- OCR quality depends on input image quality and local Tesseract installation.
- LLM output quality and availability vary by provider/model access.
- API quota/rate limitations required robust fallback and error handling.

The project intentionally favors transparency, reliability, and maintainability over model complexity.

---

## 5. System Requirements

### Functional Requirements

- User uploads a resume file (`pdf`, `png`, `jpg`, `jpeg`).
- User selects a role template or enters a custom job description.
- System extracts resume text from the uploaded file.
- System preprocesses resume and job text.
- System computes and displays score, similarity, depth gap.
- System displays depth signal summaries.
- System requests AI feedback from configured provider.
- System shows safe error message when provider fails.

### Non-Functional Requirements

- UI responsiveness suitable for local usage.
- Deterministic scoring behavior for same inputs.
- Graceful degradation when APIs are unavailable.
- Modularity for easy provider switching.
- Readable codebase with test coverage for core paths.

### Environment Requirements

- Python 3.10+
- Tesseract installed for image OCR
- Dependencies from `requirements.txt`

---

## 6. High-Level Architecture

The application follows a layered architecture:

1. **Presentation Layer** (`app.py`)  
   Streamlit UI handles user interaction, file input, role selection, and output rendering.

2. **Extraction Layer** (`utils/file_extractor.py`)  
   Converts uploaded files into plain text using parser/OCR tools.

3. **Preprocessing Layer** (`preprocessing/preprocessing_pipeline.py`)  
   Normalizes text with a deterministic multi-step cleaning pipeline.

4. **Scoring Layer** (`model/model.py`)  
   Computes cosine similarity and final score adjustment.

5. **Feedback Layer** (`utils/llm_helper.py`)  
   Routes to configured provider and generates actionable guidance.

This separation improves maintainability and testing. Most importantly, the scoring layer remains independent from feedback APIs, enabling local scoring even during provider outages.

---

## 7. Resume Text Extraction Module

The extraction module provides two functions:

- `extract_pdf_text(file_path)` using `PyPDF2`
- `extract_image_text(image_path)` using `pytesseract` + `Pillow`

### Design Choices

- Keep extraction simple and synchronous to reduce complexity.
- Return empty string on recoverable failures instead of raising hard exceptions in UI flow.
- Guard optional imports so missing OCR/PDF libraries do not crash module import.

### Reliability Improvements

During bug fixes, import-time failures were eliminated by wrapping optional imports in `try/except ImportError`. This is critical because the app imports extraction utilities even when users may only upload one file type.

### Limitations

- Scanned PDFs with low text quality may produce poor extraction.
- OCR quality is dependent on Tesseract language settings and image clarity.

Despite limitations, the extraction layer provides a practical baseline and integrates smoothly into the preprocessing stage.

---

## 8. Preprocessing Pipeline Design

The preprocessing pipeline is intentionally rule-based and transparent. It includes:

- lowercase/unicode normalization,
- delimiter cleanup,
- informal term expansion,
- tech abbreviation normalization,
- broken-word repair,
- punctuation cleanup,
- skill normalization,
- stopword reduction,
- depth signal extraction.

The objective is to convert noisy real-world text into comparable token space while preserving role-relevant semantics.

### Why Rule-Based?

Rule-based cleaning gives:

- predictable behavior,
- easy debugging,
- low runtime overhead,
- direct extensibility via dictionaries and regex maps.

This approach suits resume text, where domain abbreviations and formatting artifacts are common.

### Output

`build_feature_vector()` returns:

- cleaned resume text,
- cleaned JD text,
- resume/JD depth scores,
- absolute depth gap,
- extracted signal lists.

These outputs are consumed by both scoring and UI interpretation.

---

## 9. Scoring Model and Formula

Scoring combines textual alignment with skill-depth consistency.

### Similarity

TF-IDF vectorization transforms cleaned texts into sparse vectors, then cosine similarity is computed.

### Depth Penalty

Final score applies a penalty proportional to depth mismatch:

`final_score = similarity - (0.15 * depth_gap)`

The value is clamped between 0 and 1 and shown as percentage.

### Strengths

- Interpretable and easy to explain.
- Fast and suitable for local runtime.
- Stable under moderate text noise due to preprocessing.

### Weaknesses

- May underperform on semantic paraphrases where terms differ heavily.
- Depth scoring is heuristic and dictionary-based.

### Key Bug Fix

An important crash was fixed by handling empty-vocabulary edge cases in similarity computation. Previously, empty or near-empty cleaned texts could raise `ValueError` and break user flow.

---

## 10. LLM Feedback Module

The LLM helper supports three providers:

- Groq
- OpenRouter
- Gemini

Provider selection is environment-driven through `LLM_PROVIDER`.

### Prompt Strategy

Prompt asks for:

- reason behind score,
- gap analysis against JD,
- prioritized improvement roadmap,
- concrete learning/project suggestions,
- expected score lift by area.

This format turns output into coaching, not generic commentary.

### Provider Resilience

- OpenRouter includes fallback model retries and optional reasoning toggles.
- Gemini uses direct REST endpoint with key in query.
- Groq path now imports SDK lazily to avoid non-Groq crashes.

### Error Policy

All provider failures return explicit strings prefixed with `Error:` so the UI can consistently render warning/error states.

---

## 11. Streamlit UI and UX Flow

The UI was built with a branded, high-contrast style and a guided workflow:

- role selection and JD input panel,
- resume upload panel,
- “Run analysis” action,
- score dashboard,
- feedback and signal sections,
- extracted text preview.

### Usability Characteristics

- Immediate validation when inputs are missing.
- Clear metric presentation (overall score, similarity, depth gap).
- AI feedback isolated from deterministic score.

### Improvement Opportunities

- Add loading-state step indicators.
- Add downloadable report export (PDF/Markdown).
- Add optional plain/minimal theme for lower visual density.

The current UI balances rich presentation and functional output for student portfolio demonstration and practical usage.

---

## 12. Error Handling Strategy

A robust user-facing system must treat failures as expected states.

### Error Classes Managed

- Missing API key
- Invalid/expired key
- Provider upstream unavailability
- Rate or model availability restrictions
- Missing local libraries (OCR/PDF/SDK)
- Empty extracted text / low-information input

### Principles Applied

- Never crash app for recoverable failures.
- Prefer controlled fallback output over exception traces.
- Preserve core score workflow even if AI fails.
- Surface concise actionable messages.

This strategy significantly improved reliability and user trust.

---

## 13. Testing Strategy

The test layer was converted from interactive scripts to deterministic pytest tests.

### Current Test Coverage

- similarity function behavior for empty and normal inputs,
- preprocessing output contract and depth-gap sanity,
- extraction fallback behavior for missing files,
- provider-key validation path for Groq feedback.

### Why This Matters

Previously, tests included `input()` prompts and live API dependencies, which are unsuitable for CI and unstable across environments. The revised suite is repeatable and fast.

### Result

All tests pass:

- `8 passed`

This validates both functionality and bug-fix stability.

---

## 14. Bug Fix Log (Implemented)

### Fixed

1. Empty vocabulary crash in TF-IDF scoring.
2. Hard import dependency on Groq even for other providers.
3. Inconsistent non-error return string from Groq failure path.
4. Fragile extraction imports causing collection/import errors.
5. Interactive scripts mislabeled as tests.
6. Environment example and docs mismatch.
7. Project hygiene improvements (`.gitignore`, cleanup of accidental Node artifacts).

### Impact

- Improved runtime stability
- Cleaner testing and development workflow
- Better onboarding experience for new contributors

---

## 15. Project Hygiene and Maintenance Improvements

Cleanup steps performed:

- Removed accidental Node package artifacts (`package.json`, `package-lock.json`, `node_modules`).
- Expanded `.gitignore` for Python project patterns.
- Updated `requirements.txt` to include `pytest` and remove unused `pymupdf`.
- Updated `.env.example` to reflect real provider options and key configuration.
- Rewrote README to match implemented architecture.

These changes reduce confusion and align repository state with actual runtime dependencies.

---

## 16. Security and Secrets Management

The project uses `.env` for secret management and excludes it from version control.

### Security Practices Applied

- API keys are loaded from environment variables.
- `.env` is ignored via `.gitignore`.
- Error paths avoid printing keys.

### Operational Recommendation

If a key is exposed in logs or chat history, rotate immediately and issue a fresh key from provider console.

### Further Hardening

- Add startup validation for provider config completeness.
- Add optional secret scanner in pre-commit hooks.

---

## 17. Performance Considerations

### Current Performance Profile

- Preprocessing: lightweight regex/string operations.
- Scoring: 2-document TF-IDF + cosine (very fast).
- Bottlenecks: OCR extraction and network LLM call latency.

### Optimization Ideas

- Cache cleaned JD when unchanged.
- Cache role template expansions.
- Use async provider call abstraction for better UI responsiveness.

The current design is sufficient for local single-user workflows.

---

## 18. Extensibility Plan

The modular design allows direct extension in several directions:

- Add embedding-based semantic similarity models.
- Add JD domain-specific weighting (hard requirements vs nice-to-have).
- Add multi-resume comparison mode.
- Add recruiter dashboard and candidate ranking view.
- Add generated interview question suggestions based on gaps.

Because extraction, preprocessing, scoring, and feedback are already separated, each extension can be developed with low coupling.

---

## 19. Deployment Considerations

For deployment, the following should be prepared:

- containerized runtime with Tesseract installed,
- environment variable injection through secret manager,
- provider failover policy,
- request-level logging with PII-safe redaction,
- basic health checks.

Potential deployment targets:

- Streamlit Community Cloud (limited custom binary support)
- Render/railway with custom Docker
- VPS/cloud VM with reverse proxy

Production deployment should include rate limiting and usage guardrails for AI calls.

---

## 20. Limitations

- TF-IDF is lexical and can miss deeper semantic equivalence.
- OCR quality can degrade with poor scans.
- Skill-depth inference is heuristic, not probabilistic.
- LLM feedback quality varies by model and provider health.
- No persistent storage for user sessions/history.

These limitations are acceptable for an academic/portfolio-grade v1 but should be addressed in v2.

---

## 21. Future Work

### Technical

- Move to hybrid scoring: TF-IDF + sentence embeddings.
- Add confidence score and explanation traceability.
- Add structured feedback schema (JSON output + UI renderer).

### Product

- Add guided resume improvement checklist.
- Add skill coverage heatmap by JD category.
- Add exportable candidate improvement report.

### Engineering

- Add CI pipeline with linting and tests.
- Introduce typed settings/config module.
- Add provider abstraction interface with plugin pattern.

---

## 22. Lessons Learned

Key lessons from this project:

1. **Deterministic core logic is essential.** AI should explain, not define, base score.
2. **Small reliability bugs create major UX breakage.** Empty-input crashes and import-time failures matter more than visual polish.
3. **Tests must be non-interactive and environment-safe.** Demo scripts are not tests.
4. **Provider integrations need fallback design.** Availability and quotas vary constantly.
5. **Documentation drift is real.** README must be updated with implementation changes.

These lessons substantially shaped the bug-fix strategy and final architecture quality.

---

## 23. Project Outcome Summary

The final system successfully delivers:

- End-to-end resume matching workflow
- Explainable numerical scoring
- Actionable AI feedback with provider flexibility
- Robust fallback/error behavior
- Passing automated tests
- Cleaner and better-documented repository

From an academic perspective, the project demonstrates practical NLP system design, reliable software engineering, and iterative quality improvement under real constraints.

---

## 24. Conclusion

Resume Matcher demonstrates that a useful hiring-assist application can be built with transparent classical NLP methods and selectively integrated modern LLM feedback. The strongest engineering decision in this project is the clear separation between deterministic scoring and provider-dependent explanation.

The bug-fix cycle significantly increased system maturity by addressing reliability at module boundaries: extraction, scoring, provider imports, and test architecture. The result is a more trustworthy tool that fails gracefully and remains productive even when external APIs are unstable.

While there is clear room for model sophistication and deployment hardening, the current system already meets core goals: helping users understand resume-job fit and improve strategically.

This report can also serve as a baseline reference for future versions, where advanced semantic models, analytics, and enterprise integrations may be layered on top of the current architecture.

---

## 25. Appendix

### A. Command Reference

```bash
# setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run app
streamlit run app.py

# run tests
pytest -q

# run CLI
python main.py
```

### B. Environment Template

```env
LLM_PROVIDER=groq

GROQ_API_KEY=your_groq_key
GROQ_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
GROQ_MAX_COMPLETION_TOKENS=1024

OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=openai/gpt-oss-120b:free
OPENROUTER_REASONING_ENABLED=true
OPENROUTER_MAX_COMPLETION_TOKENS=1024

GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-3-flash-preview
```

### C. Suggested Viva Questions

1. Why did you choose TF-IDF over embeddings initially?
2. How do you justify the depth-gap penalty coefficient?
3. How does the app behave when API providers are down?
4. What are the risks of OCR-based extraction in production?
5. How would you improve semantic matching in v2?

### D. Suggested Metrics for Next Iteration

- Extraction quality score (manual benchmark)
- Match score calibration against recruiter judgments
- Feedback usefulness rating by users
- Latency breakdown by pipeline stage
- API failure rate by provider/model


---

## 26. Literature and Industry Context

Resume screening has historically evolved through three broad paradigms: manual review, keyword-matching systems, and modern semantic/AI-assisted screening. Manual review provides nuance but does not scale for high applicant volume. Keyword systems scale but often produce false negatives when candidate wording differs from job description vocabulary. AI-assisted systems improve semantic coverage but can become opaque and difficult to audit.

This project is positioned intentionally between keyword-only and black-box AI approaches. It keeps deterministic scoring local and explainable while using AI to contextualize and improve communication of results. This hybrid architecture reflects current practical industry patterns where teams want both interpretability (for compliance and trust) and flexibility (for natural-language feedback).

In many real organizations, ATS systems still perform initial lexical filtering before any advanced ranking. That means candidate outcome is strongly influenced by text quality and alignment. A tool like Resume Matcher can improve candidate readiness by exposing likely mismatch areas before application submission.

From a research perspective, the project demonstrates a useful pattern for applied NLP products: use robust classical features for core scoring, then layer generative models for user-facing explanation. This separation can reduce operational risk and simplify testing, because deterministic components can be benchmarked independently from provider-driven text generation.

---

## 27. Detailed Methodology

The methodology follows an input-to-output pipeline with explicit transformations at each stage.

### Stage 1: Input Acquisition

- Resume file received via upload.
- Job description selected from templates or manually entered.

### Stage 2: Text Acquisition

- If file type is PDF, text extraction uses page iteration through PDF parser.
- If file type is image, OCR extracts approximate textual representation.

### Stage 3: Text Normalization

The preprocessing pipeline applies ordered transformations to reduce noise and improve matching reliability:

- lexical normalization,
- delimiter normalization,
- abbreviation expansion,
- broken token repair,
- skill canonicalization,
- stopword reduction,
- depth signal extraction.

Each transformation is deterministic and inspectable, allowing reproducibility.

### Stage 4: Feature Construction

A feature dictionary combines:

- cleaned resume text,
- cleaned JD text,
- depth indicators,
- depth-gap magnitude,
- raw signal lists.

### Stage 5: Scoring

TF-IDF vectorization is fit on the two cleaned documents, then cosine similarity is computed. Depth-gap penalty adjusts final score to reflect proficiency mismatch.

### Stage 6: Explanation

Prompted LLM call generates practical next steps. If provider fails, deterministic score remains available.

This methodology emphasizes reliability and user interpretability rather than model novelty.

---

## 28. Algorithmic Walkthrough with Pseudocode

### Preprocessing and Feature Build

```text
function build_feature_vector(resume_text, jd_text):
    clean_resume, resume_meta = preprocess(resume_text, return_metadata=True)
    clean_jd, jd_meta = preprocess(jd_text, return_metadata=True)

    return {
        clean_resume,
        clean_jd,
        resume_depth=resume_meta.depth_score,
        jd_depth=jd_meta.depth_score,
        depth_gap=abs(resume_meta.depth_score - jd_meta.depth_score),
        resume_signals=resume_meta.signals,
        jd_signals=jd_meta.signals
    }
```

### Similarity and Final Score

```text
function compute_similarity(clean_resume, clean_jd):
    if both empty:
        return 0.0
    try:
        vec = TFIDF.fit_transform([clean_resume, clean_jd])
        return cosine(vec[0], vec[1])
    except ValueError:
        return 0.0
```

```text
function compute_final_score(feature_vector):
    sim = compute_similarity(feature_vector.clean_resume, feature_vector.clean_jd)
    final = sim - 0.15 * feature_vector.depth_gap
    final = clamp(final, 0.0, 1.0)
    return percentage(final), sim, feature_vector.depth_gap
```

### Feedback Routing

```text
if provider == "groq":
    generate_with_groq()
elif provider == "gemini":
    generate_with_gemini()
else:
    generate_with_openrouter()
```

This algorithmic structure keeps scoring deterministic and enables provider-level evolution without destabilizing core logic.

---

## 29. Dataset and Input Characteristics

The project includes synthetic/noisy dataset files used for experimentation and pipeline validation. These files include examples of:

- typo-heavy resumes,
- abbreviation-heavy technical descriptions,
- mixed depth indicators,
- partial skill overlap scenarios,
- overqualified/underqualified edge cases.

These examples are valuable for pipeline stress testing because real resumes are often inconsistent in formatting and terminology. For example, one candidate may write “React.js”, another “React”, another “rea ct”, and all should ideally map to comparable skill tokens.

The preprocessing pipeline’s value becomes clear under such variation. Without normalization, lexical matching alone would underestimate candidate relevance. By converting related expressions into canonical forms, the system improves both fairness and scoring consistency.

For future scientific rigor, this synthetic corpus can be extended with a labeled benchmark dataset where recruiter judgments are used as ground-truth reference. That would allow quantitative calibration of both similarity and depth-penalty coefficients.

---

## 30. UI/UX Design Rationale

Although backend logic is central, UI design strongly affects user trust. Resume Matcher’s UI is structured to guide users through one primary workflow:

1. define target role,
2. upload candidate resume,
3. run analysis,
4. review metrics and recommendations.

The dashboard emphasizes metric clarity:

- overall match (decision metric),
- semantic similarity (textual relevance),
- depth gap (proficiency mismatch).

Separating these avoids over-reliance on one number and helps users understand *why* a score was produced.

Signal review and extracted-text preview further improve transparency. Users can inspect what the system actually read and whether key proficiency cues were detected. This is useful for diagnosing OCR failures or poorly structured resume content.

From a usability perspective, the app prioritizes immediate feedback and constrained interactions rather than deeply nested controls. This is ideal for an iterative document-improvement workflow.

Future UX improvements may include scenario presets, interactive recommendation checklists, and downloadable feedback plans.

---

## 31. API Provider Engineering Tradeoffs

Supporting multiple LLM providers increases resilience but introduces integration complexity.

### Benefits

- Fallback if one provider is unavailable.
- Price/performance flexibility across models.
- Easier experimentation with prompt behavior.

### Challenges

- Provider-specific parameters differ (`reasoning`, token fields, model naming).
- Error payloads vary in structure.
- Authentication and quota semantics are inconsistent.

### Engineering Approach

The project uses a single routing entrypoint with provider-specific generator functions. This centralizes API selection while allowing tailored request payloads per provider.

OpenRouter integration includes model fallback and retry behavior for temporary upstream failures. Groq integration uses lazy SDK import to avoid hard dependency failure in non-Groq setups. Gemini integration uses direct REST requests and explicit invalid-key messaging.

This design limits provider coupling to one module and keeps the application core provider-agnostic.

---

## 32. Failure Mode and Effects Analysis (FMEA)

### Failure Mode 1: Empty Extraction

- **Cause:** unreadable file or OCR failure
- **Effect:** meaningless or empty cleaned text
- **Mitigation:** similarity returns 0.0 instead of crash; preview allows user verification

### Failure Mode 2: Missing SDK/Library

- **Cause:** dependency not installed
- **Effect:** import-time crash
- **Mitigation:** optional import guards with controlled fallback

### Failure Mode 3: Invalid API Key

- **Cause:** stale/revoked key
- **Effect:** provider error responses
- **Mitigation:** provider-specific explicit error messages

### Failure Mode 4: Provider Outage

- **Cause:** upstream 503/no healthy backend
- **Effect:** feedback generation failure
- **Mitigation:** OpenRouter fallback model retries; score remains available

### Failure Mode 5: Test Instability

- **Cause:** interactive/network test scripts
- **Effect:** non-reproducible CI results
- **Mitigation:** deterministic pytest conversion

This FMEA-driven perspective guided bug prioritization.

---

## 33. Testing Matrix and Results

### Unit Test Categories

- Similarity logic tests
- Preprocessing contract tests
- Extractor fallback behavior tests
- Provider error-path tests

### Execution Summary

- Test runner: `pytest`
- Result: `8 passed`
- Runtime: low (under 2 seconds in local run)

### Confidence Interpretation

The current tests validate baseline correctness and resilience paths. They do not yet include:

- OCR accuracy benchmarking,
- provider response-quality evaluation,
- UI snapshot tests.

Still, they significantly improve regression detection for core runtime logic.

### Recommended Additions

- parameterized tests for multiple noisy text patterns,
- mock-based tests for provider success payload formats,
- contract tests for environment variable parsing,
- static linting/format checks in CI.

---

## 34. DevOps and Version Control Practices

The repository now follows cleaner version-control hygiene:

- sensitive config excluded (`.env`),
- generated caches ignored,
- accidental non-Python artifacts removed,
- testable dependency list maintained.

A recommended CI baseline would include:

1. dependency install,
2. syntax check (`py_compile`),
3. test run (`pytest -q`),
4. optional static checks.

For team collaboration, branching strategy can be simplified as:

- `main` for stable code,
- feature branches for changes,
- pull request review with test pass requirement.

This reduces integration risk and ensures reproducibility for academic review or portfolio demonstrations.

---

## 35. Ethical and Fairness Considerations

Automated resume analysis can unintentionally influence candidate perception and decision-making. Therefore, it is important to frame this system as advisory rather than authoritative.

### Ethical Principles Applied

- Transparency in scoring method.
- User visibility into extracted text and detected signals.
- Separation of deterministic score from generative suggestions.

### Potential Risks

- Overfitting resume content to keyword style rather than true competency.
- Bias introduced by JD wording style.
- False confidence from LLM-generated recommendations.

### Mitigation Recommendations

- Clearly label score as heuristic guidance.
- Encourage manual review and human judgment.
- Add disclaimers for AI-generated advice.
- Continuously evaluate on diverse job-role language.

In future iterations, fairness audits using varied linguistic and demographic proxy patterns should be included.

---

## 36. Cost and Resource Analysis

### Compute Cost

Local preprocessing and TF-IDF scoring are low-cost and suitable for commodity systems.

### API Cost

LLM cost depends on provider/model usage:

- token limits,
- model pricing tier,
- fallback retries frequency.

### Operational Insight

Keeping core score local minimizes cloud dependency and controls costs. LLM feedback is additive, not mandatory. This architecture is economically efficient and suitable for student projects and small deployments.

### Cost Optimization Paths

- reduce prompt size intelligently,
- cap completion tokens by default,
- cache identical feedback requests for repeated inputs,
- offer lower-cost model defaults in `.env.example`.

---

## 37. Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Provider outage | Medium | Medium | Retry + fallback + keep local scoring |
| OCR inconsistency | High | Medium | Show extracted preview, support manual correction |
| Key leakage | Medium | High | `.env` ignore + key rotation process |
| Drift in docs/config | Medium | Medium | Update README and `.env.example` each release |
| Regression from rapid changes | Medium | High | Keep pytest suite and add CI |

This register should be reviewed at each release milestone.

---

## 38. Proposed Timeline for Version 2

### Phase 1 (Weeks 1–2)

- Add configuration validation and startup diagnostics.
- Expand test coverage for provider payload parsing.

### Phase 2 (Weeks 3–5)

- Introduce embedding-based similarity as optional scoring mode.
- Build evaluation script comparing lexical vs semantic scoring.

### Phase 3 (Weeks 6–7)

- Add exportable PDF/Markdown feedback report.
- Add user-selectable strictness modes (junior/mid/senior).

### Phase 4 (Weeks 8–9)

- CI pipeline + containerized deployment.
- Document production deployment checklist.

### Phase 5 (Week 10)

- User testing round and scoring calibration updates.

This plan keeps scope controlled while delivering measurable quality improvements.

---

## 39. Viva/Defense Preparation Notes

If presenting this project in viva or interview, the strongest talking points are:

- clear architecture separation (score vs explanation),
- practical handling of real-world failures,
- deterministic testing improvements,
- meaningful bug-fix impact on user reliability.

Suggested short defense structure:

1. **Problem:** candidates lack actionable alignment feedback.
2. **Approach:** extract → preprocess → score → explain.
3. **Why TF-IDF first:** explainability, low cost, controllable behavior.
4. **Reliability work:** empty-vocabulary fix, optional imports, test refactor.
5. **Outcome:** stable app with passing tests and multi-provider support.

Demonstration suggestion:

- run one successful analysis,
- run one failure scenario (missing key) to show graceful behavior,
- highlight extracted text preview and signal panel.

This demonstrates both functionality and engineering maturity.

---

## 40. Extended Conclusion

Resume Matcher now stands as a strong applied software-engineering project: practical, explainable, testable, and extensible. Its evolution shows an important engineering truth: product quality is shaped less by initial implementation speed and more by iterative bug fixing, test discipline, and documentation alignment.

The project successfully addresses a common candidate pain point while illustrating modern integration realities: provider instability, API parameter drift, and environment configuration variability. By designing around these realities instead of ignoring them, the final system remains useful under imperfect conditions.

In academic terms, the work integrates NLP preprocessing, classical IR-style similarity, software architecture modularity, UI product design, and reliability engineering into one coherent deliverable. In practical terms, it provides immediate user value and a clear path to future enhancements.

This report, along with the cleaned codebase, can be directly used for submission, demonstration, and future iteration planning.


---

## 41. Detailed Component Responsibility Breakdown

A major engineering strength in this project is clear ownership of responsibility at the module level. This section provides a deeper breakdown.

### `app.py`

- Manages user flow and layout rendering.
- Owns transient file handling and session state for results.
- Should avoid heavy business logic.

### `utils/file_extractor.py`

- Owns only file-to-text conversion.
- Handles optional dependency availability.
- Returns clean fallback output on failure.

### `preprocessing/preprocessing_pipeline.py`

- Owns all deterministic text transformation.
- Produces both cleaned text and explanatory metadata.

### `model/model.py`

- Owns similarity computation and score finalization.
- Should remain provider-agnostic and fast.

### `utils/llm_helper.py`

- Owns provider routing, payload preparation, and API error handling.
- Must not impact deterministic scoring stability.

This separation allows easier debugging and evolution. If an issue appears in one layer, it can often be fixed there without cascading changes across the codebase.

---

## 42. Why Classical NLP Was a Good V1 Choice

Choosing TF-IDF for a first release can look simplistic compared to embeddings, but in this project context it was a practical and defensible decision.

### Advantages in This Scenario

- Fast inference on local machines.
- No additional model hosting complexity.
- Fully transparent output behavior.
- Easy to explain during academic evaluation.

### Tradeoff Awareness

TF-IDF may miss conceptual similarity when wording differs significantly. However, the preprocessing pipeline (abbreviation expansion, canonicalization, token repair) compensates partially by reducing lexical fragmentation.

### Pedagogical Value

For a student/portfolio project, a transparent baseline often demonstrates stronger engineering judgment than adding a complex model stack without testability or error controls.

### Planned Upgrade Path

A v2 embedding layer can be introduced as an optional mode while keeping TF-IDF as a fallback baseline. This supports comparative evaluation and avoids sudden regressions.

---

## 43. Observability and Debugging Recommendations

As this project scales, structured observability will become more important.

### Suggested Logging Events

- extraction started/completed
- cleaned text length metrics
- score computation inputs and outputs (without raw PII dumps)
- provider selected
- provider response success/failure category

### Suggested Metrics

- average extraction time
- average provider latency
- provider error rate by model
- ratio of “empty extraction” events
- score distribution over sessions

### Debugging Playbook

1. If score is unexpectedly low, inspect cleaned text and signal lists.
2. If feedback fails, inspect provider configuration and key validity.
3. If extraction is empty, inspect input quality and OCR dependencies.

This playbook shortens issue resolution cycles and improves developer confidence.

---

## 44. Data Privacy and PII Handling

Resumes contain sensitive personal data. Even in local projects, privacy-aware design is essential.

### Current Protective Design

- Local processing for extraction/preprocessing/scoring.
- No database persistence by default.
- Keys not committed to git.

### Remaining Risks

- Sending resume snippets to external LLM providers.
- Potential accidental logging of sensitive content.

### Recommendations

- Add provider opt-in notice in UI.
- Add “local-only mode” toggle that skips AI feedback entirely.
- Mask obvious PII tokens before provider calls.
- Add retention policy note for external provider usage.

These changes would improve trust and align with responsible AI product expectations.

---

## 45. Comparative Evaluation Framework (Future)

To improve rigor, future versions should evaluate scoring quality against human judgment.

### Proposed Dataset

- 200–500 resume-JD pairs
- human labels: strong/moderate/weak
- optional rationale annotations for top skill gaps

### Metrics

- correlation between model score and human label
- class-level precision/recall if thresholded
- inter-rater agreement among human reviewers

### Experiment Tracks

- TF-IDF baseline
- TF-IDF + depth-gap tuning
- embedding similarity
- hybrid weighted ensemble

### Outcome Goal

Quantitatively justify scoring method and depth penalty rather than relying solely on heuristic intuition.

---

## 46. Maintenance Checklist for Contributors

For future collaborators, a maintenance checklist prevents silent drift.

### Before Changing Code

- run `pytest -q`
- inspect `.env.example` for config alignment
- verify README references are still accurate

### After Changing Provider Logic

- confirm error messages start with `Error:`
- verify fallback logic does not trigger duplicate expensive calls
- update provider section in README

### After Changing Extraction/Preprocessing

- add/adjust tests for regressions
- validate one PDF and one image sample manually

### Before Commit

- ensure `.env` is not tracked
- ensure no accidental large artifact folders are included
- run syntax check and tests

This lightweight process keeps quality high with low overhead.

---

## 47. Suggested Submission Artifacts

To strengthen academic/project submission, include:

1. Source code repository (clean main branch)
2. This full report (`PROJECT_REPORT.md`)
3. Short demo video (3–5 minutes)
4. Sample input files and expected output screenshots
5. Test execution screenshot (`8 passed`)

### Demo Video Flow

- show problem statement slide
- run app live with one sample resume
- show score + feedback + signal interpretation
- show error handling when provider key missing
- close with roadmap and lessons learned

This combination demonstrates both technical implementation and communication quality.

---

## 48. Final Reflection

This project reflects a complete software engineering cycle: ideation, implementation, integration, bug discovery, stabilization, documentation, and delivery. The final code is more reliable than earlier iterations not because of a single feature, but because of cumulative quality decisions.

Most notably:

- deterministic scoring is stable under edge cases,
- provider-specific fragility is isolated and controlled,
- test architecture is now automation-friendly,
- documentation matches implementation,
- repository hygiene supports collaboration.

From a career perspective, this project demonstrates readiness for roles involving practical ML integration, backend reliability, and product-facing engineering. It also provides a strong base for future research or startup-style feature expansion in career-tech tooling.


---

## 49. Extended Case Study Scenarios

To evaluate practical usefulness, consider five representative scenarios.

### Scenario A: Keyword Match but Low Depth

A candidate includes all required skills but writes only beginner-level qualifiers. The model similarity can still be moderate-to-high, but depth-gap penalty reduces final score. This helps avoid false optimism.

### Scenario B: Strong Experience but Missing Terminology

A candidate has relevant experience but describes it differently (for example, product terms vs stack terms). Preprocessing may recover some alignment, but lexical gaps can still reduce score. This is where AI feedback can suggest terminology alignment.

### Scenario C: OCR-Degraded Resume

Image extraction produces fragmented text. Similarity drops due noisy tokens, and signal extraction may under-report skill depth. The extracted text preview helps user diagnose and re-upload a better file.

### Scenario D: Provider Unavailable

Scoring still completes; feedback module returns controlled error. User still receives quantitative signal and can proceed.

### Scenario E: Highly Generic Resume

Resume contains broad statements and minimal technical detail. Score naturally trends low due sparse overlap and weak depth evidence. Feedback highlights missing specificity and recommends concrete projects.

These scenarios show the system’s behavior under realistic variation and demonstrate robustness of the deterministic-first design.

---

## 50. Rubric Mapping for Academic Evaluation

Many academic projects are graded on multiple dimensions. This section maps Resume Matcher outcomes to common rubric categories.

### Problem Definition

- Clear and relevant real-world problem (resume-job mismatch).
- Well-scoped objective for a semester-scale project.

### Technical Design

- Layered architecture with separation of concerns.
- Multi-provider integration with environment-driven routing.
- Deterministic scoring + explainable penalty model.

### Implementation Quality

- Working Streamlit application.
- Modular utility and model components.
- Error handling improvements and optional dependency support.

### Testing and Validation

- Automated test suite with passing status.
- Coverage of edge conditions for critical functions.

### Documentation

- Updated README with accurate setup and behavior.
- Comprehensive report including methodology, results, and roadmap.

### Innovation and Practical Relevance

- Hybrid explainable-scoring + AI guidance approach.
- Useful in real career-preparation contexts.

This mapping can help during project defense, report assessment, or mentor review.

---

## 51. Implementation Checklist (Reproducible Build)

Use this section to rebuild the project from scratch in a clean environment.

### Step 1: Clone and Enter Project

```bash
git clone <repo-url>
cd resume_project
```

### Step 2: Setup Python Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your provider key
```

### Step 5: Validate with Tests

```bash
pytest -q
```

### Step 6: Launch App

```bash
streamlit run app.py
```

### Step 7: Functional Smoke Test

- Upload one PDF resume.
- Use one template JD.
- Confirm score dashboard appears.
- Confirm feedback appears or controlled provider error appears.

This reproducible flow ensures submission evaluators can validate functionality quickly.

---

## 52. Suggested Improvement Backlog (Prioritized)

### Priority 1 (High Impact, Low Effort)

- Add explicit “No extractable text found” warning before scoring.
- Add provider health indicator in UI.
- Add test for OpenRouter/Gemini missing-key path.

### Priority 2 (High Impact, Medium Effort)

- Add embedding-based alternate score mode.
- Add configurable penalty coefficient in `.env`.
- Add downloadable markdown report from current analysis.

### Priority 3 (Medium Impact, Medium Effort)

- Add language detection and multilingual preprocessing hooks.
- Add typo correction dictionary expansion.
- Add richer model-specific provider settings.

### Priority 4 (Long-Term)

- Recruiter-mode batch ranking.
- JD requirement extraction by section (must-have/nice-to-have).
- A/B evaluation framework against human labels.

Prioritizing in this way preserves system stability while increasing practical value.

---

## 53. Executive Summary (One-Page Equivalent)

Resume Matcher is an end-to-end resume analysis application built with Python and Streamlit. It helps users understand resume-to-job fit by computing a transparent match score and generating targeted feedback for improvement.

The pipeline is modular:

- extraction from PDF/images,
- deterministic preprocessing and feature construction,
- TF-IDF similarity with depth-gap penalty,
- optional AI explanation through Groq/OpenRouter/Gemini.

A dedicated bug-fix phase significantly improved reliability:

- prevented empty-input crashes,
- removed hard dependency coupling,
- standardized provider error handling,
- converted interactive scripts into proper automated tests,
- cleaned repository artifacts and updated documentation.

The current test suite passes, and the app remains functional even when LLM providers fail, because scoring is local and independent.

Key strengths:

- explainability,
- robustness under common failures,
- practical user value,
- clear architecture suitable for extension.

Key next steps:

- semantic embedding-based optional scoring,
- improved privacy controls for provider calls,
- CI pipeline and deployment hardening,
- evaluation against labeled recruiter judgments.

In summary, the project demonstrates practical applied NLP engineering with strong software-quality improvements and is suitable for academic submission, portfolio demonstration, and iterative product development.

