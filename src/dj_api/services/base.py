from __future__ import annotations

from typing import Any, Dict, Optional

from dj_api.http.client import APIClient


class BaseService:
    def __init__(self, client: APIClient) -> None:
        self.client = client

    @staticmethod
    def bearer(token: Optional[str]) -> Dict[str, str]:
        if not token:
            return {}
        return {"Authorization": f"Bearer {token}"}

    @staticmethod
    def json_content_type() -> Dict[str, str]:
        return {"Content-Type": "application/json"}

