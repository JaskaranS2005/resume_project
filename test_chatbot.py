import sys
from types import SimpleNamespace

from utils.llm_helper import chat_with_groq


class FakeCompletions:
    def __init__(self):
        self.messages = None

    def create(self, messages, **_kwargs):
        self.messages = messages
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content="Here is a normal chatbot reply.")
                )
            ]
        )


class FakeGroqClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.chat = SimpleNamespace(completions=FakeCompletions())


def test_chatbot_does_not_block_unrelated_questions(monkeypatch):
    fake_groq_module = SimpleNamespace(Groq=FakeGroqClient)
    monkeypatch.setitem(sys.modules, "groq", fake_groq_module)
    monkeypatch.setenv("GROQ_API_KEY", "test-key")

    reply = chat_with_groq(
        "Python developer resume with projects and education.",
        "Python developer role",
        [{"role": "user", "content": "Tell me a joke"}],
    )

    assert reply == "Here is a normal chatbot reply."
