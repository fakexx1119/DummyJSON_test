from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass
from typing import Any, Dict, Mapping, MutableMapping, Optional
from urllib.parse import urljoin
from uuid import uuid4

import requests

from dj_api.config import settings
from dj_api.utils.allure_attach import (
    attach_bytes,
    attach_json,
    attach_kv_table,
    attach_response,
    attach_text,
)


@dataclass(frozen=True)
class RequestResult:
    method: str
    url: str
    status_code: int
    elapsed_ms: int
    headers: Mapping[str, Any]
    body_text: str


class APIClient:
    def __init__(
        self,
        base_url: str,
        *,
        timeout_seconds: float = 30,
        default_headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if default_headers:
            self.session.headers.update(dict(default_headers))

    def _full_url(self, path: str) -> str:
        path = path.lstrip("/")
        return urljoin(self.base_url, path)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        json_body: Any = None,
        data: Any = None,
        files: Any = None,
        allow_redirects: bool = True,
    ) -> requests.Response:
        url = self._full_url(path)

        req_headers: MutableMapping[str, str] = {}
        if headers:
            req_headers.update(dict(headers))

        request_id = uuid4().hex
        # 统一加一个 trace id，便于排查与报告串联
        req_headers.setdefault("X-Request-Id", request_id)

        def _build_curl(full_url: str) -> str:
            # 尽量生成“可复制粘贴”的 curl（偏通用）
            parts = ["curl", "-X", method.upper(), f"\"{full_url}\""]
            for k, v in req_headers.items():
                parts += ["-H", f"\"{k}: {v}\""]
            if json_body is not None:
                try:
                    body = json.dumps(json_body, ensure_ascii=False)
                except Exception:
                    body = str(json_body)
                parts += ["-H", "\"Content-Type: application/json\"", "-d", f"'{body}'"]
            return " ".join(parts)

        max_attempts = max(1, int(getattr(settings, "retry_attempts", 1)))
        backoff_base = float(getattr(settings, "retry_backoff_base_seconds", 0.3))
        retry_statuses = {429, 500, 502, 503, 504}

        last_exc: Optional[BaseException] = None
        resp: Optional[requests.Response] = None
        start_all = time.perf_counter()
        for attempt in range(1, max_attempts + 1):
            start = time.perf_counter()
            try:
                resp = self.session.request(
                    method=method.upper(),
                    url=url,
                    params=dict(params) if params else None,
                    headers=req_headers if req_headers else None,
                    json=json_body,
                    data=data,
                    files=files,
                    timeout=self.timeout_seconds,
                    allow_redirects=allow_redirects,
                )
                elapsed_ms = int((time.perf_counter() - start) * 1000)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                last_exc = e
                elapsed_ms = int((time.perf_counter() - start) * 1000)
                attach_text("重试.请求ID", request_id)
                attach_text("重试.第几次", f"{attempt}/{max_attempts}")
                attach_text("重试.异常", repr(e))
                attach_text("重试.本次耗时(ms)", str(elapsed_ms))
                if attempt < max_attempts:
                    sleep_s = backoff_base * (2 ** (attempt - 1)) + random.uniform(0, backoff_base)
                    attach_text("重试.等待(秒)", f"{sleep_s:.2f}")
                    time.sleep(sleep_s)
                    continue
                raise

            attach_text("请求.请求ID", request_id)
            attach_text("请求.第几次", f"{attempt}/{max_attempts}")

            # 需要重试的状态码
            if resp.status_code in retry_statuses and attempt < max_attempts:
                attach_text("重试.触发原因", f"HTTP {resp.status_code}")
                sleep_s = backoff_base * (2 ** (attempt - 1)) + random.uniform(0, backoff_base)
                attach_text("重试.等待(秒)", f"{sleep_s:.2f}")
                time.sleep(sleep_s)
                continue
            break

        assert resp is not None
        total_elapsed_ms = int((time.perf_counter() - start_all) * 1000)

        # Allure：把“可复现的信息”尽量挂上去（领导看报告会更完整）
        attach_text("请求.方法", method.upper())
        full_url = resp.request.url if resp.request else url
        attach_text("请求.URL", full_url)
        if params:
            attach_kv_table("请求.Query参数", dict(params))
        if req_headers:
            attach_kv_table("请求.请求头", dict(req_headers))
        if json_body is not None:
            attach_json("请求.请求体(JSON)", json_body)
        attach_text("请求.cURL", _build_curl(full_url))

        content_type = (resp.headers.get("Content-Type") or "").lower()
        if content_type.startswith("image/"):
            attach_text("响应.说明", f"二进制图片（{content_type}），字节数={len(resp.content)}")
            attach_bytes("响应.图片附件", resp.content, mime=content_type)
            attach_response(
                "响应",
                status_code=resp.status_code,
                headers=dict(resp.headers),
                body_text="<<binary image omitted>>",
            )
        else:
            attach_response(
                "响应",
                status_code=resp.status_code,
                headers=dict(resp.headers),
                body_text=resp.text,
            )
        attach_text("响应.总耗时(ms)", str(total_elapsed_ms))

        return resp

