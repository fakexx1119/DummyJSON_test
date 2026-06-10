from __future__ import annotations

from typing import Optional

import requests

from dj_api.services.base import BaseService
from dj_api.utils.steps import step


class SystemService(BaseService):
    def test_route(self) -> requests.Response:
        """GET /test"""
        with step("系统: 连通性检查（GET /test）"):
            return self.client.request("GET", "/test")

    def ip(self) -> requests.Response:
        """GET /ip"""
        with step("系统: 获取客户端IP（GET /ip）"):
            return self.client.request("GET", "/ip")

    def http_mock(self, *, code: int, message: Optional[str] = None) -> requests.Response:
        """GET /http/{code}/{optional-message}"""
        path = f"/http/{code}" if message is None else f"/http/{code}/{message}"
        with step(f"系统: Mock HTTP 响应（GET {path}）"):
            return self.client.request("GET", path)

    def image(
        self,
        *,
        size: str,
        background: Optional[str] = None,
        color: Optional[str] = None,
        text: Optional[str] = None,
        type: Optional[str] = None,  # png/jpg/webp
        fontFamily: Optional[str] = None,
        fontSize: Optional[int] = None,
    ) -> requests.Response:
        """
        GET /image/{SIZE} 或 /image/{WIDTH}x{HEIGHT}/{BACKGROUND?}/{COLOR?}
        Query: text, type, fontFamily, fontSize
        """
        path = f"/image/{size}"
        if background:
            path += f"/{background}"
        if color:
            path += f"/{color}"

        params = {}
        if text is not None:
            params["text"] = text
        if type is not None:
            params["type"] = type
        if fontFamily is not None:
            params["fontFamily"] = fontFamily
        if fontSize is not None:
            params["fontSize"] = fontSize

        with step(f"系统: 生成占位图片（GET {path}）"):
            return self.client.request("GET", path, params=params)

    def icon(self, *, hash: str, size: int, type: Optional[str] = None) -> requests.Response:
        """
        GET /icon/{HASH}/{SIZE}?type=png|svg
        """
        params = {}
        if type:
            params["type"] = type
        with step("系统: 生成 identicon（GET /icon/{hash}/{size}）"):
            return self.client.request("GET", f"/icon/{hash}/{size}", params=params)

