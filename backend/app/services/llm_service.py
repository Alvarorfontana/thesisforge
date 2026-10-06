import json
import httpx
from app.core.config import settings

def stream_module(prompt: str):
    """Streaming del módulo generado. OpenRouter (gratis) por defecto."""
    if settings.llm_provider == "gemini":
        yield from _stream_gemini(prompt)
    elif settings.llm_provider == "claude":
        yield from _stream_claude(prompt)
    else:
        yield from _stream_openrouter(prompt)

def _stream_openrouter(prompt: str):
    """OpenRouter con modelo gratuito (ej: llama-3.3-70b-instruct:free)."""
    if not settings.openrouter_api_key:
        yield "Error: configurá OPENROUTER_API_KEY en el .env (gratis en https://openrouter.ai/keys)."
        return
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.openrouter_model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }
    try:
        with httpx.Client(timeout=180) as client:
            with client.stream("POST", url, headers=headers, json=payload) as r:
                if r.status_code == 401:
                    yield "Error 401: key de OpenRouter inválida. Verificá OPENROUTER_API_KEY."
                    return
                if r.status_code == 429:
                    yield "Error 429: límite de cuota del modelo gratuito alcanzado. Probá en unos minutos u otro modelo :free."
                    return
                if r.status_code != 200:
                    yield f"Error de OpenRouter (HTTP {r.status_code})."
                    return
                for line in r.iter_lines():
                    if not line.startswith("data: "):
                        continue
                    data_str = line[6:].strip()
                    if data_str == "[DONE]":
                        return
                    try:
                        data = json.loads(data_str)
                    except json.JSONDecodeError:
                        continue
                    for choice in data.get("choices", []):
                        delta = choice.get("delta", {})
                        if delta.get("content"):
                            yield delta["content"]
    except httpx.TimeoutException:
        yield "Error: la generación tardó demasiado. Probá de nuevo."
    except Exception as e:
        yield f"Error de conexión con OpenRouter: {e}"

def _stream_gemini(prompt: str):
    if not settings.gemini_api_key:
        yield "Error: configurá GEMINI_API_KEY en el .env (gratis en https://aistudio.google.com)."
        return
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{settings.gemini_model}:streamGenerateContent"
           f"?alt=sse&key={settings.gemini_api_key}")
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        with httpx.Client(timeout=180) as client:
            with client.stream("POST", url, json=payload) as r:
                if r.status_code != 200:
                    yield f"Error de Gemini (HTTP {r.status_code}): verificá la API key."
                    return
                for line in r.iter_lines():
                    if not line.startswith("data: "):
                        continue
                    try:
                        data = json.loads(line[6:])
                    except json.JSONDecodeError:
                        continue
                    for cand in data.get("candidates", []):
                        for part in cand.get("content", {}).get("parts", []):
                            if "text" in part:
                                yield part["text"]
    except httpx.TimeoutException:
        yield "Error: la generación tardó demasiado. Probá de nuevo."
    except Exception as e:
        yield f"Error de conexión con Gemini: {e}"

def _stream_claude(prompt: str):
    if not settings.anthropic_api_key:
        yield "Error: configurá ANTHROPIC_API_KEY en el .env (o usá OpenRouter/Gemini, son gratis)."
        return
    import anthropic
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            yield text
