from utils.llm_helper import generate_feedback


def test_generate_feedback_groq_without_key_returns_error(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    feedback = generate_feedback("resume text", "job description", 50)

    assert feedback.startswith("Error:")
    assert "GROQ_API_KEY" in feedback
