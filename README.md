# Resume Matcher

Resume Matcher is a Python + Streamlit application that compares a resume against a job description, computes a match score, and generates practical improvement feedback using a configurable LLM provider.

## Core Features

- Upload resume as PDF or image (`png`, `jpg`, `jpeg`)
- Extract resume text locally
- Clean and normalize resume/JD text with a lightweight preprocessing pipeline
- Compute match quality using TF-IDF cosine similarity and depth-gap penalty
- Generate coaching feedback through `groq`, `openrouter`, or `gemini`
- Visual dashboard with score breakdown and signal review

## Tech Stack

- Python
- Streamlit
- scikit-learn
- PyPDF2
- pytesseract + Pillow
- python-dotenv

## Project Structure

```text
resume_project/
├── app.py
├── main.py
├── model/
│   └── model.py
├── preprocessing/
│   └── preprocessing_pipeline.py
├── utils/
│   ├── file_extractor.py
│   └── llm_helper.py
├── dataset/
├── test_groq_api.py
├── test_image.py
├── test_model.py
├── test_pdf.py
├── test_preprocessing.py
├── requirements.txt
├── .env.example
└── README.md
```

## How It Works

1. User uploads resume and provides/selects a job description.
2. Text is extracted from file:
   - PDF: `PyPDF2`
   - Image: `pytesseract` + `Pillow`
3. Both texts pass through preprocessing (`build_feature_vector`).
4. Matching score is computed in `model/model.py`.
5. Provider-specific AI feedback is generated in `utils/llm_helper.py`.
6. Streamlit displays match score, similarity, depth gap, and recommendations.

## Scoring Logic

```python
similarity = cosine_similarity(resume_vector, jd_vector)
final_score = similarity - (0.15 * depth_gap)
```

The score is clamped to `[0, 1]` then shown as percentage.

## Environment Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

For OCR support (image resumes), install Tesseract:

```bash
brew install tesseract
```

## Environment Variables

Copy `.env.example` to `.env` and fill your provider key(s):

```bash
cp .env.example .env
```

Minimal example:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_key
```

You can switch provider by changing `LLM_PROVIDER` to:

- `groq`
- `openrouter`
- `gemini`

## Run

Streamlit app:

```bash
streamlit run app.py
```

CLI mode:

```bash
python main.py
```

## Tests

Run test suite:

```bash
pytest -q
```

## Bug Fixes Included

The latest cleanup includes:

- Safe handling for empty-text TF-IDF cases (no crash on empty vocabulary)
- Optional dependency guards for extractor modules
- Lazy import for Groq SDK so non-Groq providers keep working
- Consistent `Error:` messages for UI error rendering
- Converted interactive demo scripts into real pytest tests
- Updated `.env.example`, `.gitignore`, and dependency list

## Notes

- If provider API keys are missing or invalid, scoring still runs, but feedback returns a controlled error message.
- Keep `.env` private. It is excluded via `.gitignore`.
