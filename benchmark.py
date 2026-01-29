"""
Simple benchmark: "Are there any Rs in star"
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

PROMPT = "Are there any Rs in star"

def call_openai(model: str) -> str:
    """Call OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "ERROR: OPENAI_API_KEY not set"

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": PROMPT}],
        },
        timeout=60,
    )

    if response.status_code != 200:
        return f"ERROR: {response.status_code} - {response.text}"

    return response.json()["choices"][0]["message"]["content"]


def call_gemini(model: str) -> str:
    """Call Google Gemini API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "ERROR: GOOGLE_API_KEY not set"

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
        json={
            "contents": [{"role": "user", "parts": [{"text": PROMPT}]}],
        },
        timeout=60,
    )

    if response.status_code != 200:
        return f"ERROR: {response.status_code} - {response.text}"

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]


def call_deepseek(model: str) -> str:
    """Call DeepSeek API (OpenAI-compatible)."""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "ERROR: DEEPSEEK_API_KEY not set"

    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": PROMPT}],
        },
        timeout=60,
    )

    if response.status_code != 200:
        return f"ERROR: {response.status_code} - {response.text}"

    return response.json()["choices"][0]["message"]["content"]


def call_qwen(model: str) -> str:
    """Call Qwen API (OpenAI-compatible via DashScope)."""
    api_key = os.getenv("QWEN_API_KEY")
    if not api_key:
        return "ERROR: QWEN_API_KEY not set"

    response = requests.post(
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": PROMPT}],
        },
        timeout=60,
    )

    if response.status_code != 200:
        return f"ERROR: {response.status_code} - {response.text}"

    return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    print(f"PROMPT: {PROMPT}")
    print("=" * 50)

    print("\n[GPT-5.2]")
    print(call_openai("gpt-5.2"))

    print("\n[Gemini 3 Pro]")
    print(call_gemini("gemini-3-pro-preview"))

    print("\n[DeepSeek V3.2]")
    print(call_deepseek("deepseek-chat"))
