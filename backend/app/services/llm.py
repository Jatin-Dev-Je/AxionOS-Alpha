from __future__ import annotations

import json
from typing import List, Dict, Any
import http.client
import os
from urllib.parse import urlparse

from ..config import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OLLAMA_HOST,
    OLLAMA_MODEL,
    LLM_TIMEOUT,
)


class LLMError(Exception):
    pass


def _http_post_json(url: str, payload: Dict[str, Any], headers: Dict[str, str], timeout: float) -> Dict[str, Any]:
    parsed = urlparse(url)
    conn_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    conn = conn_cls(parsed.hostname, parsed.port, timeout=timeout)
    try:
        path = parsed.path or "/"
        if parsed.query:
            path += f"?{parsed.query}"
        body = json.dumps(payload)
        conn.request("POST", path, body=body, headers=headers)
        resp = conn.getresponse()
        data = resp.read()
        if resp.status >= 400:
            raise LLMError(f"HTTP {resp.status}: {data.decode('utf-8', 'ignore')}")
        try:
            return json.loads(data)
        except Exception as e:
            raise LLMError(f"Invalid JSON response: {e}")
    finally:
        conn.close()


def llm_chat(messages: List[Dict[str, str]]) -> str:
    provider = (LLM_PROVIDER or "stub").lower()
    if provider == "openai":
        if not OPENAI_API_KEY:
            raise LLMError("Missing OPENAI_API_KEY")
        # Use the REST API to avoid adding SDK deps
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }
        payload = {
            "model": OPENAI_MODEL,
            "messages": messages,
            "temperature": 0.2,
            "stream": False,
        }
        data = _http_post_json(url, payload, headers, timeout=LLM_TIMEOUT)
        content = data.get("choices", [{}])[0].get("message", {}).get("content")
        if not content:
            raise LLMError("No content in OpenAI response")
        return content

    if provider == "ollama":
        base = OLLAMA_HOST.rstrip("/")
        url = f"{base}/api/chat"
        headers = {"Content-Type": "application/json"}
        payload = {"model": OLLAMA_MODEL, "messages": messages, "stream": False}
        data = _http_post_json(url, payload, headers, timeout=LLM_TIMEOUT)
        # Ollama returns entire object; try common fields
        msg = data.get("message") or {}
        content = msg.get("content") or data.get("response")
        if not content:
            raise LLMError("No content in Ollama response")
        return content

    # stub provider
    last_user = next((m["content"] for m in reversed(messages) if m.get("role") == "user"), "")
    return f"[stub llm] You said: {last_user[:200]}"
