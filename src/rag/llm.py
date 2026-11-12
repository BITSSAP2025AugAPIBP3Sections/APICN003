import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URLS = {
    "slm": os.getenv("SLM_BASE_URL", "http://localhost:11434/v1"),
    "groq": "https://api.groq.com/openai/v1",
    "openai": "https://api.openai.com/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "anthropic": "https://api.anthropic.com/v1",
}

SYSTEM_PROMPT = (
    "You are an Indian Income Tax assistant for a student assignment. "
    "Answer ONLY from the provided context. If the context does not contain the answer, say you cannot find it in the corpus. "
    "Cite the source document name (and page if present) for key claims."
)


def _strip_think_tags(text: str) -> str:
    """Remove <think>...</think> reasoning blocks emitted by some models (Qwen3, DeepSeek-R1)."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def _openai_compatible(base: str, api_key: str, model: str, messages: list[dict], max_tokens: int) -> str:
    resp = requests.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.2},
        timeout=120,
    )
    if not resp.ok:
        print("Groq error:", resp.status_code, resp.text)
    resp.raise_for_status()
    return _strip_think_tags(resp.json()["choices"][0]["message"]["content"])


def _anthropic(api_key: str, model: str, messages: list[dict], max_tokens: int) -> str:
    system_text = "\n".join(m["content"] for m in messages if m["role"] == "system")
    chat = [m for m in messages if m["role"] != "system"]
    resp = requests.post(
        f"{BASE_URLS['anthropic']}/messages",
        headers={"x-api-key": api_key, "anthropic-version": "2023-06-01"},
        json={"model": model, "system": system_text, "messages": chat, "max_tokens": max_tokens},
        timeout=120,
    )
    resp.raise_for_status()
    return _strip_think_tags(resp.json()["content"][0]["text"])


def llm() -> tuple[str, str, str]:
    provider = os.getenv("LLM_PROVIDER", "slm")
    if provider not in BASE_URLS:
        raise SystemExit(f"LLM_PROVIDER={provider!r} not in {sorted(BASE_URLS)}")
    model = os.getenv("LLM_MODEL") or {
        "slm": "llama3.1:8b",
        "groq": "llama-3.3-70b-versatile",
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-haiku-20241022",
        "openrouter": "meta-llama/llama-3.1-8b-instruct",
    }[provider]
    keys = {"slm": "SLM_API_KEY", "groq": "GROQ_API_KEY", "openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY", "openrouter": "OPENROUTER_API_KEY"}
    return provider, model, os.getenv(keys[provider], "")


def chat(question: str, context: str, history: list[dict] | None = None, max_tokens: int = 2000) -> str:
    provider, model, api_key = llm()
    system_msg = {"role": "system", "content": SYSTEM_PROMPT}
    user_msg = {"role": "user", "content": f"Context from corpus:\n{context}\n\nQuestion: {question}"}
    history_msgs = [m for m in (history or []) if m.get("role") != "system"]
    messages = [system_msg] + history_msgs + [user_msg]
    if provider == "anthropic":
        return _anthropic(api_key, model, messages, max_tokens)
    return _openai_compatible(BASE_URLS[provider], api_key or "ollama", model, messages, max_tokens)
