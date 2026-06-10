from __future__ import annotations

from typing import Optional

import requests

from dj_api.http.models import DelayQuery, PaginationQuery, SelectQuery, merge_params
from dj_api.http.payloads import CartUpsertPayload
from dj_api.services.base import BaseService
from dj_api.utils.steps import step


class CartsService(BaseService):
    def list_carts(
        self,
        *,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /carts Query: limit,skip,select,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step("购物车: 获取购物车列表（GET /carts）"):
            return self.client.request("GET", "/carts", params=params)

    def get_cart(
        self,
        *,
        cart_id: int,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /carts/{id} Query: select,delay"""
        params = merge_params(
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"购物车: 获取单个购物车（GET /carts/{cart_id}）"):
            return self.client.request("GET", f"/carts/{cart_id}", params=params)

    def carts_by_user(
        self,
        *,
        user_id: int,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /carts/user/{userId} Query: limit,skip,select,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"购物车: 查询用户购物车（GET /carts/user/{user_id}）"):
            return self.client.request("GET", f"/carts/user/{user_id}", params=params)

    def add_cart(self, *, payload: CartUpsertPayload) -> requests.Response:
        """POST /carts/add Body: userId + products[{id,quantity}]"""
        with step("购物车: 新增购物车（模拟）（POST /carts/add）"):
            return self.client.request(
                "POST",
                "/carts/add",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def update_cart(
        self,
        *,
        cart_id: int,
        payload: CartUpsertPayload,
        method: str = "PUT",  # or PATCH
    ) -> requests.Response:
        """PUT/PATCH /carts/{id} Body: merge(可选) + products(可选)"""
        with step(f"购物车: 更新购物车（模拟）（{method} /carts/{cart_id}）"):
            return self.client.request(
                method,
                f"/carts/{cart_id}",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def delete_cart(self, *, cart_id: int) -> requests.Response:
        """DELETE /carts/{id}"""
        with step(f"购物车: 删除购物车（模拟）（DELETE /carts/{cart_id}）"):
            return self.client.request("DELETE", f"/carts/{cart_id}")

