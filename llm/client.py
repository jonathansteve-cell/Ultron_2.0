import os
import requests
from dotenv import load_dotenv
from llm.schemas import LLMMessage, LLMResponse

load_dotenv("config/.env")

def call_llm(system_prompt: str, user_message: str) -> LLMResponse:
    provider = os.getenv("LLM_PROVIDER", "mock").lower()
    key = os.getenv("GOOGLE_API_KEY", "")
    if provider == "google" and key and not key.startswith("YOUR_"):
        base = os.getenv("LLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta").rstrip("/")
        model = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
        response = requests.post(
            f"{base}/models/{model}:generateContent", params={"key": key},
            json={"system_instruction": {"parts": [{"text": system_prompt}]},
                  "contents": [{"role": "user", "parts": [{"text": user_message}]}],
                  "generationConfig": {"temperature": 0.2, "maxOutputTokens": 512}}, timeout=30)
        response.raise_for_status()
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return LLMResponse(message=LLMMessage(role="assistant", content=text))
    return LLMResponse(message=LLMMessage(role="assistant", content=f"[Local mode] You said: {user_message}"))
