import os

from dotenv import load_dotenv
from openai import OpenAI

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def _api_base_url(api_key: str) -> str | None:
    configured_url = os.getenv("OPENAI_BASE_URL", "").strip()
    if configured_url:
        return configured_url
    if api_key.startswith("sk-or-"):
        return OPENROUTER_BASE_URL
    return None


def openai_client_erstellen() -> OpenAI:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY fehlt. Lege den Schlüssel in der .env-Datei fest.")

    base_url = _api_base_url(api_key)
    return OpenAI(api_key=api_key, base_url=base_url)


def modellname_ermitteln(variable: str, standard: str) -> str:
    load_dotenv()
    model = os.getenv(variable, "").strip() or standard
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = _api_base_url(api_key)
    if base_url and "openrouter.ai" in base_url.lower() and "/" not in model:
        return f"openai/{model}"
    return model