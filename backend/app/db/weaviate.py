from __future__ import annotations

from typing import List, Dict
import json
import http.client
from urllib.parse import urlparse

from ..config import WEAVIATE_URL, LLM_TIMEOUT


def _http_post_json(url: str, payload: dict, headers: dict) -> dict:
    parsed = urlparse(url)
    conn_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    conn = conn_cls(parsed.hostname, parsed.port, timeout=LLM_TIMEOUT)
    try:
        path = parsed.path or "/"
        if parsed.query:
            path += f"?{parsed.query}"
        body = json.dumps(payload)
        conn.request("POST", path, body=body, headers=headers)
        resp = conn.getresponse()
        data = resp.read()
        if resp.status >= 400:
            raise RuntimeError(f"Weaviate HTTP {resp.status}: {data.decode('utf-8', 'ignore')}")
        return json.loads(data)
    finally:
        conn.close()


def weaviate_bm25_search(class_name: str, query: str, limit: int = 5) -> List[Dict]:
    # Minimal GraphQL BM25 search using Weaviate REST endpoint
    url = WEAVIATE_URL.rstrip("/") + "/v1/graphql"
    headers = {"Content-Type": "application/json"}
    gql = {
        "query": (
            "query Get($near: String!, $limit: Int!) {\n"
            f"  Get {{ {class_name} (bm25: {{ query: $near }}, limit: $limit) {{\n"
            "      _additional { id score }\n"
            "      text\n"
            "    }}\n"
            "  }}\n"
            "}"
        ),
        "variables": {"near": query, "limit": limit},
    }
    try:
        data = _http_post_json(url, gql, headers)
        items = data.get("data", {}).get("Get", {}).get(class_name, [])
        return items or []
    except Exception:
        return []
