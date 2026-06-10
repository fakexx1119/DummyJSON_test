from __future__ import annotations

from typing import Optional

import requests

from dj_api.http.models import DelayQuery, PaginationQuery, SelectQuery, SortQuery, merge_params
from dj_api.http.payloads import UserUpsertPayload
from dj_api.services.base import BaseService
from dj_api.utils.steps import step


class UsersService(BaseService):
    def list_users(
        self,
        *,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
        sort: Optional[SortQuery] = None,
    ) -> requests.Response:
        """GET /users Query: limit,skip,select,delay,sortBy,order"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
            (sort or SortQuery()).to_params(),
        )
        with step("用户: 获取用户列表（GET /users）"):
            return self.client.request("GET", "/users", params=params)

    def get_user(
        self,
        *,
        user_id: int,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /users/{id} Query: select,delay"""
        params = merge_params(
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"用户: 获取单个用户（GET /users/{user_id}）"):
            return self.client.request("GET", f"/users/{user_id}", params=params)

    def search_users(
        self,
        *,
        q: str,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /users/search Query: q,limit,skip,select,delay"""
        params = merge_params(
            {"q": q},
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step("用户: 搜索用户（GET /users/search）"):
            return self.client.request("GET", "/users/search", params=params)

    def filter_users(
        self,
        *,
        key: str,
        value: str,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /users/filter Query: key,value,limit,skip,select,delay"""
        params = merge_params(
            {"key": key, "value": value},
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step("用户: 过滤用户（GET /users/filter）"):
            return self.client.request("GET", "/users/filter", params=params)

    def user_carts(self, *, user_id: int, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /users/{id}/carts Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        with step(f"用户: 获取用户购物车（GET /users/{user_id}/carts）"):
            return self.client.request("GET", f"/users/{user_id}/carts", params=params)

    def user_posts(self, *, user_id: int, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /users/{id}/posts Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        with step(f"用户: 获取用户帖子（GET /users/{user_id}/posts）"):
            return self.client.request("GET", f"/users/{user_id}/posts", params=params)

    def user_todos(self, *, user_id: int, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /users/{id}/todos Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        with step(f"用户: 获取用户待办（GET /users/{user_id}/todos）"):
            return self.client.request("GET", f"/users/{user_id}/todos", params=params)

    def add_user(self, *, payload: UserUpsertPayload) -> requests.Response:
        """POST /users/add Body: 用户字段（模拟）"""
        with step("用户: 新增用户（模拟）（POST /users/add）"):
            return self.client.request(
                "POST",
                "/users/add",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def update_user(
        self,
        *,
        user_id: int,
        payload: UserUpsertPayload,
        method: str = "PUT",  # or PATCH
    ) -> requests.Response:
        """PUT/PATCH /users/{id} Body: 更新字段（模拟）"""
        with step(f"用户: 更新用户（模拟）（{method} /users/{user_id}）"):
            return self.client.request(
                method,
                f"/users/{user_id}",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def delete_user(self, *, user_id: int) -> requests.Response:
        """DELETE /users/{id}"""
        with step(f"用户: 删除用户（模拟）（DELETE /users/{user_id}）"):
            return self.client.request("DELETE", f"/users/{user_id}")

