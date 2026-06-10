from __future__ import annotations

from typing import Optional

import requests

from dj_api.http.models import DelayQuery, PaginationQuery, merge_params
from dj_api.services.base import BaseService
from dj_api.utils.steps import step


class QuotesService(BaseService):
    def list_quotes(
        self,
        *,
        pagination: Optional[PaginationQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /quotes Query: limit,skip,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step("名言: 获取名言列表（GET /quotes）"):
            return self.client.request("GET", "/quotes", params=params)

    def get_quote(self, *, quote_id: int, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /quotes/{id} Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        with step(f"名言: 获取单条名言（GET /quotes/{quote_id}）"):
            return self.client.request("GET", f"/quotes/{quote_id}", params=params)

    def random_quote(self, *, length: Optional[int] = None, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /quotes/random 或 /quotes/random/{length} Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        path = "/quotes/random" if length is None else f"/quotes/random/{length}"
        with step("名言: 获取随机名言（GET /quotes/random）"):
            return self.client.request("GET", path, params=params)

