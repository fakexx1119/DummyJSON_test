from __future__ import annotations

from typing import Optional

import requests

from dj_api.http.models import DelayQuery, PaginationQuery, SelectQuery, merge_params
from dj_api.http.payloads import CommentUpsertPayload
from dj_api.services.base import BaseService
from dj_api.utils.steps import step


class CommentsService(BaseService):
    def list_comments(
        self,
        *,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /comments Query: limit,skip,select,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step("评论: 获取评论列表（GET /comments）"):
            return self.client.request("GET", "/comments", params=params)

    def get_comment(
        self,
        *,
        comment_id: int,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /comments/{id} Query: select,delay"""
        params = merge_params(
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"评论: 获取单个评论（GET /comments/{comment_id}）"):
            return self.client.request("GET", f"/comments/{comment_id}", params=params)

    def comments_by_post(
        self,
        *,
        post_id: int,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /comments/post/{postId} Query: limit,skip,select,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"评论: 按帖子查询评论（GET /comments/post/{post_id}）"):
            return self.client.request("GET", f"/comments/post/{post_id}", params=params)

    def add_comment(self, *, payload: CommentUpsertPayload) -> requests.Response:
        """POST /comments/add Body: body,postId,userId（模拟）"""
        with step("评论: 新增评论（模拟）（POST /comments/add）"):
            return self.client.request(
                "POST",
                "/comments/add",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def update_comment(
        self,
        *,
        comment_id: int,
        payload: CommentUpsertPayload,
        method: str = "PUT",  # or PATCH
    ) -> requests.Response:
        """PUT/PATCH /comments/{id} Body: 更新字段（模拟）"""
        with step(f"评论: 更新评论（模拟）（{method} /comments/{comment_id}）"):
            return self.client.request(
                method,
                f"/comments/{comment_id}",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def delete_comment(self, *, comment_id: int) -> requests.Response:
        """DELETE /comments/{id}"""
        with step(f"评论: 删除评论（模拟）（DELETE /comments/{comment_id}）"):
            return self.client.request("DELETE", f"/comments/{comment_id}")

