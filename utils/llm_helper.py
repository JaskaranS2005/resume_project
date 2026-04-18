import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


def _load_env_file():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_env_file()


def _build_prompt(resume_text, jd, score, resume_max_chars=1200, jd_max_chars=1000):
    resume_slice = (resume_text or "")[: max(200, int(resume_max_chars))]
    jd_slice = (jd or "")[: max(200, int(jd_max_chars))]

    return f"""
You are a career assistant.

Resume:
{resume_slice}

Job Description:
{jd_slice}

Match Score: {score}%

Task:
- Briefly explain why this score was assigned.
- Compare the resume against the job requirements and identify missing skills/experience.
- Highlight the top weakness areas that are reducing the score most.
- Provide a prioritized practice plan to improve the candidate in those areas.
- Suggest concrete projects, exercises, and learning topics specific to the missing skills.
- Estimate potential score improvement after completing each priority area.
- Keep the response concise and use bullet points with clear section titles.
"""


def _generate_with_openrouter(prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    model = os.getenv("OPENROUTER_MODEL", "qwen/qwen3.6-plus:free")
    site_url = os.getenv("OPENROUTER_SITE_URL", "")
    app_name = os.getenv("OPENROUTER_APP_NAME", "")

    if not api_key:
        return "Error: OPENROUTER_API_KEY is not set. Add it in your .env file."

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a career assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if site_url:
        headers["HTTP-Referer"] = site_url
    if app_name:
        headers["X-Title"] = app_name

    request = Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urlopen(request, timeout=60) as response:
            response_data = json.loads(response.read().decode("utf-8"))

        return response_data["choices"][0]["message"]["content"]
    except HTTPError as e:
        details = e.read().decode("utf-8", errors="ignore")
        return f"Error: OpenRouter API request failed ({e.code}). {details}"
    except URLError as e:
        return f"Error: Could not connect to OpenRouter API. {e.reason}"
    except Exception as e:
        return f"Error: {str(e)}"


def _generate_with_groq(resume_text, jd, score):
    api_key = os.getenv("GROQ_API_KEY")
    base_url = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    model = os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
    reasoning_effort = os.getenv("GROQ_REASONING_EFFORT", "medium")
    max_completion_tokens = int(os.getenv("GROQ_MAX_COMPLETION_TOKENS", "1024"))
    resume_prompt_max_chars = int(os.getenv("GROQ_RESUME_PROMPT_MAX_CHARS", "1200"))
    jd_prompt_max_chars = int(os.getenv("GROQ_JD_PROMPT_MAX_CHARS", "1000"))
    fallback_models_raw = os.getenv(
        "GROQ_FALLBACK_MODELS",
        "meta-llama/llama-4-scout-17b-16e-instruct,llama-3.3-70b-versatile,llama-3.1-8b-instant,openai/gpt-oss-20b",
    )

    if not api_key:
        return "Error: GROQ_API_KEY is not set. Add it in your .env file."

    fallback_models = [m.strip() for m in fallback_models_raw.split(",") if m.strip()]
    candidate_models = []
    for candidate in [model, *fallback_models]:
        if candidate and candidate not in candidate_models:
            candidate_models.append(candidate)

    last_error = "Error: Groq request failed."

    prompt_budgets = [
        (resume_prompt_max_chars, jd_prompt_max_chars),
        (int(resume_prompt_max_chars * 0.7), int(jd_prompt_max_chars * 0.7)),
        (int(resume_prompt_max_chars * 0.45), int(jd_prompt_max_chars * 0.45)),
    ]

    for budget_index, (resume_budget, jd_budget) in enumerate(prompt_budgets):
        prompt = _build_prompt(resume_text, jd, score, resume_budget, jd_budget)
        hit_tpm_limit = False

        for idx, candidate_model in enumerate(candidate_models):
            payload = {
                "model": candidate_model,
                "messages": [
                    {"role": "system", "content": "You are a career assistant."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
                "top_p": 1,
                "max_completion_tokens": max_completion_tokens,
            }
            if candidate_model.startswith("openai/gpt-oss"):
                payload["reasoning_effort"] = reasoning_effort

            request = Request(
                f"{base_url.rstrip('/')}/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )

            try:
                with urlopen(request, timeout=60) as response:
                    response_data = json.loads(response.read().decode("utf-8"))
                return response_data["choices"][0]["message"]["content"]

            except HTTPError as e:
                details = e.read().decode("utf-8", errors="ignore")
                lower_details = details.lower()

                if e.code == 401 or "invalid api key" in lower_details or "invalidapikey" in lower_details:
                    return "Error: GROQ_API_KEY is invalid. Generate a new Groq key and update .env."

                if "error code: 101" in lower_details:
                    return (
                        "Error: Groq request was blocked (403 / code 101). "
                        "This is usually a network/IP or account access restriction. "
                        "Try another network and check Groq account/project limits."
                    )

                if e.code == 413 or "tokens per minute" in lower_details or "request too large" in lower_details:
                    last_error = (
                        f"Error: Groq request exceeded token limits for model `{candidate_model}`. {details}"
                    )
                    hit_tpm_limit = True
                    break

                last_error = f"Error: Groq API request failed ({e.code}) for model `{candidate_model}`. {details}"

                model_blocked = (
                    e.code == 403
                    and (
                        "model_permission_blocked_org" in lower_details
                        or "model_permission_blocked_project" in lower_details
                        or "blocked at the organization level" in lower_details
                        or "blocked at the project level" in lower_details
                        or "permissions_error" in lower_details
                        or "forbidden" in lower_details
                    )
                )
                model_not_found = e.code == 404 and ("model" in lower_details or "not found" in lower_details)

                should_retry = idx < len(candidate_models) - 1 and (model_blocked or model_not_found)
                if should_retry:
                    continue

                if model_blocked:
                    return (
                        f"{last_error} "
                        "Enable the model in Groq console under Settings -> Organization/Projects -> Limits, "
                        "or change GROQ_MODEL in .env."
                    )

                return last_error
            except URLError as e:
                return f"Error: Could not connect to Groq API. {e.reason}"
            except Exception as e:
                return f"Error: {str(e)}"

        if hit_tpm_limit and budget_index < len(prompt_budgets) - 1:
            continue

    return (
        f"{last_error} "
        "Tried fallback models and progressively smaller prompt budgets but none succeeded."
    )


def _generate_with_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    base_url = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")
    model = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

    if not api_key:
        return "Error: GEMINI_API_KEY is not set. Add it in your .env file."

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3},
    }

    endpoint = f"{base_url.rstrip('/')}/models/{model}:generateContent?key={quote_plus(api_key)}"
    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=60) as response:
            response_data = json.loads(response.read().decode("utf-8"))

        candidates = response_data.get("candidates", [])
        if not candidates:
            return "Error: Gemini returned no candidates."

        parts = candidates[0].get("content", {}).get("parts", [])
        text_segments = [part.get("text", "") for part in parts if part.get("text")]
        if not text_segments:
            return "Error: Gemini response did not include text output."

        return "\n".join(text_segments)
    except HTTPError as e:
        details = e.read().decode("utf-8", errors="ignore")
        if "API_KEY_INVALID" in details or "API key expired" in details:
            return (
                "Error: Gemini API key is invalid or expired. "
                "Update GEMINI_API_KEY in .env with a newly generated key."
            )
        return f"Error: Gemini API request failed ({e.code}). {details}"
    except URLError as e:
        return f"Error: Could not connect to Gemini API. {e.reason}"
    except Exception as e:
        return f"Error: {str(e)}"


def generate_feedback(resume_text, jd, score):
    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()

    if provider == "groq":
        return _generate_with_groq(resume_text, jd, score)
    if provider == "gemini":
        prompt = _build_prompt(resume_text, jd, score)
        return _generate_with_gemini(prompt)

    prompt = _build_prompt(resume_text, jd, score)
    return _generate_with_openrouter(prompt)
