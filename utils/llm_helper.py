import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from dotenv import load_dotenv
import groq

load_dotenv()


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
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-120b:free")
    site_url = os.getenv("OPENROUTER_SITE_URL", "")
    app_name = os.getenv("OPENROUTER_APP_NAME", "")
    temperature = float(os.getenv("OPENROUTER_TEMPERATURE", "0.3"))
    max_completion_tokens_raw = os.getenv("OPENROUTER_MAX_COMPLETION_TOKENS", "").strip()
    reasoning_enabled = os.getenv("OPENROUTER_REASONING_ENABLED", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    reasoning_effort = os.getenv("OPENROUTER_REASONING_EFFORT", "").strip()
    fallback_models_raw = os.getenv(
        "OPENROUTER_FALLBACK_MODELS",
        "meta-llama/llama-3.1-70b-instruct:free,mistralai/mistral-small-3.2-24b-instruct:free,openai/gpt-oss-20b:free",
    )

    if not api_key:
        return "Error: OPENROUTER_API_KEY is not set. Add it in your .env file."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if site_url:
        headers["HTTP-Referer"] = site_url
    if app_name:
        headers["X-Title"] = app_name

    fallback_models = [m.strip() for m in fallback_models_raw.split(",") if m.strip()]
    candidate_models = []
    for candidate in [model, *fallback_models]:
        if candidate and candidate not in candidate_models:
            candidate_models.append(candidate)

    last_error = "Error: OpenRouter request failed."

    for candidate_model in candidate_models:
        for use_reasoning in ([True, False] if reasoning_enabled else [False]):
            payload = {
                "model": candidate_model,
                "messages": [
                    {"role": "system", "content": "You are a career assistant."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature,
            }
            if max_completion_tokens_raw:
                payload["max_completion_tokens"] = int(max_completion_tokens_raw)
            if use_reasoning:
                reasoning_block = {"enabled": True}
                if reasoning_effort:
                    reasoning_block["effort"] = reasoning_effort
                payload["reasoning"] = reasoning_block

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
                lower_details = details.lower()

                if e.code == 401 or "invalid api key" in lower_details:
                    return "Error: OPENROUTER_API_KEY is invalid. Update it in .env."

                no_upstream = e.code == 503 and (
                    "no healthy upstream" in lower_details or "provider returned error" in lower_details
                )
                model_unavailable = e.code in (404, 429, 503)
                if no_upstream or model_unavailable:
                    last_error = (
                        f"Error: OpenRouter model `{candidate_model}` is currently unavailable ({e.code}). {details}"
                    )
                    continue

                return f"Error: OpenRouter API request failed ({e.code}). {details}"
            except URLError as e:
                return f"Error: Could not connect to OpenRouter API. {e.reason}"
            except Exception as e:
                return f"Error: {str(e)}"

    return (
        f"{last_error} "
        "Tried fallback models and reasoning-off retries. "
        "Please try again shortly or switch OPENROUTER_MODEL in .env."
    )


def _generate_with_groq(resume_text, jd, score):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY is not set. Add it in your .env file."

    try:
        client = groq.Groq(api_key=api_key)
        model = os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
        prompt = _build_prompt(resume_text, jd, score)
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a career assistant."},
                {"role": "user", "content": prompt},
            ],
            model=model,
            temperature=0.7,
            max_completion_tokens=int(os.getenv("GROQ_MAX_COMPLETION_TOKENS", "1024"))
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq API Error: {e}")
        return "AI feedback is currently unavailable due to an API error. Your match score is still valid."


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
