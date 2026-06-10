from __future__ import annotations

from typing import Optional

import requests

from dj_api.http.models import DelayQuery, PaginationQuery, merge_params
from dj_api.http.payloads import TodoUpsertPayload
from dj_api.services.base import BaseService
from dj_api.utils.steps import step


class TodosService(BaseService):
    def list_todos(
        self,
        *,
        pagination: Optional[PaginationQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /todos Query: limit,skip,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step("待办: 获取待办列表（GET /todos）"):
            return self.client.request("GET", "/todos", params=params)

    def get_todo(self, *, todo_id: int, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /todos/{id} Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        with step(f"待办: 获取单个待办（GET /todos/{todo_id}）"):
            return self.client.request("GET", f"/todos/{todo_id}", params=params)

    def random_todo(self, *, length: Optional[int] = None, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /todos/random 或 /todos/random/{length} Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        path = "/todos/random" if length is None else f"/todos/random/{length}"
        with step("待办: 获取随机待办（GET /todos/random）"):
            return self.client.request("GET", path, params=params)

    def todos_by_user(
        self,
        *,
        user_id: int,
        pagination: Optional[PaginationQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /todos/user/{userId} Query: limit,skip,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"待办: 按用户查询待办（GET /todos/user/{user_id}）"):
            return self.client.request("GET", f"/todos/user/{user_id}", params=params)

    def add_todo(self, *, payload: TodoUpsertPayload) -> requests.Response:
        """POST /todos/add Body: todo,completed,userId（模拟）"""
        with step("待办: 新增待办（模拟）（POST /todos/add）"):
            return self.client.request(
                "POST",
                "/todos/add",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def update_todo(
        self,
        *,
        todo_id: int,
        payload: TodoUpsertPayload,
        method: str = "PUT",  # or PATCH
    ) -> requests.Response:
        """PUT/PATCH /todos/{id} Body: 更新字段（模拟）"""
        with step(f"待办: 更新待办（模拟）（{method} /todos/{todo_id}）"):
            return self.client.request(
                method,
                f"/todos/{todo_id}",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def delete_todo(self, *, todo_id: int) -> requests.Response:
        """DELETE /todos/{id}"""
        with step(f"待办: 删除待办（模拟）（DELETE /todos/{todo_id}）"):
            return self.client.request("DELETE", f"/todos/{todo_id}")

