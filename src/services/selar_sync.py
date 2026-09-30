from typing import Any, Dict, List

import requests

from src.config import SELAR_API_KEY, SELAR_API_URL


def sync_selar_products(url: str | None = None, api_key: str | None = None) -> List[Dict[str, Any]]:
    target_url = url or SELAR_API_URL
    token = api_key or SELAR_API_KEY

    if not target_url:
        return []

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(target_url, headers=headers, timeout=20)
        response.raise_for_status()
        payload = response.json()

        if isinstance(payload, dict) and "products" in payload:
            return payload["products"]
        if isinstance(payload, list):
            return payload
        return []
    except Exception:
        return []
