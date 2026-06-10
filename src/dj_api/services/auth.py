from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from dj_api.services.base import BaseService
from dj_api.utils.steps import step


class AuthService(BaseService):
    def login_auth(
        self,
        *,
        username: str,
        password: str,
        expiresInMins: Optional[int] = None,
    ) -> requests.Response:
        """
        POST /auth/login
        Body: username, password, expiresInMins(可选)
        """
        body: Dict[str, Any] = {"username": username, "password": password}
        if expiresInMins is not None:
            body["expiresInMins"] = expiresInMins
        with step("Auth: /auth/login 登录获取token"):
            return self.client.request(
                "POST",
                "/auth/login",
                headers=self.json_content_type(),
                json_body=body,
            )

    def me_auth(self, *, access_token: str) -> requests.Response:
        """GET /auth/me Header: Authorization=Bearer <access_token>"""
        with step("Auth: /auth/me 获取当前登录用户"):
            return self.client.request("GET", "/auth/me", headers=self.bearer(access_token))

    def refresh_auth(
        self,
        *,
        refreshToken: Optional[str] = None,
        expiresInMins: Optional[int] = None,
    ) -> requests.Response:
        """POST /auth/refresh Body: refreshToken(可选), expiresInMins(可选)"""
        body: Dict[str, Any] = {}
        if refreshToken is not None:
            body["refreshToken"] = refreshToken
        if expiresInMins is not None:
            body["expiresInMins"] = expiresInMins
        with step("Auth: /auth/refresh 刷新token"):
            return self.client.request(
                "POST",
                "/auth/refresh",
                headers=self.json_content_type(),
                json_body=body if body else {},
            )

    # 兼容 Users 文档里出现的 /user/login 与 /user/me
    def login_user(
        self,
        *,
        username: str,
        password: str,
        expiresInMins: Optional[int] = None,
    ) -> requests.Response:
        """POST /user/login Body: username, password, expiresInMins(可选)"""
        body: Dict[str, Any] = {"username": username, "password": password}
        if expiresInMins is not None:
            body["expiresInMins"] = expiresInMins
        with step("User: /user/login 登录获取token（兼容接口）"):
            return self.client.request(
                "POST",
                "/user/login",
                headers=self.json_content_type(),
                json_body=body,
            )

    def me_user(self, *, access_token: str) -> requests.Response:
        """GET /user/me Header: Authorization=Bearer <access_token>"""
        with step("User: /user/me 获取当前登录用户（兼容接口）"):
            return self.client.request("GET", "/user/me", headers=self.bearer(access_token))

