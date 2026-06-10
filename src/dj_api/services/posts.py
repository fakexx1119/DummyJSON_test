from __future__ import annotations

from typing import Optional

import requests

from dj_api.http.models import DelayQuery, PaginationQuery, SelectQuery, SortQuery, merge_params
from dj_api.http.payloads import PostUpsertPayload
from dj_api.services.base import BaseService
from dj_api.utils.steps import step


class PostsService(BaseService):
    def list_posts(
        self,
        *,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
        sort: Optional[SortQuery] = None,
    ) -> requests.Response:
        """GET /posts Query: limit,skip,select,delay,sortBy,order"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
            (sort or SortQuery()).to_params(),
        )
        with step("帖子: 获取帖子列表（GET /posts）"):
            return self.client.request("GET", "/posts", params=params)

    def get_post(
        self,
        *,
        post_id: int,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /posts/{id} Query: select,delay"""
        params = merge_params(
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"帖子: 获取单个帖子（GET /posts/{post_id}）"):
            return self.client.request("GET", f"/posts/{post_id}", params=params)

    def search_posts(
        self,
        *,
        q: str,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /posts/search Query: q,limit,skip,select,delay"""
        params = merge_params(
            {"q": q},
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step("帖子: 搜索帖子（GET /posts/search）"):
            return self.client.request("GET", "/posts/search", params=params)

    def tags(self, *, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /posts/tags Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        with step("帖子: 获取标签详情（GET /posts/tags）"):
            return self.client.request("GET", "/posts/tags", params=params)

    def tag_list(self, *, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /posts/tag-list Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        with step("帖子: 获取标签列表（GET /posts/tag-list）"):
            return self.client.request("GET", "/posts/tag-list", params=params)

    def posts_by_tag(
        self,
        *,
        slug: str,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /posts/tag/{slug} Query: limit,skip,select,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"帖子: 按标签获取帖子（GET /posts/tag/{slug}）"):
            return self.client.request("GET", f"/posts/tag/{slug}", params=params)

    def posts_by_user(
        self,
        *,
        user_id: int,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /posts/user/{userId} Query: limit,skip,select,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"帖子: 按用户获取帖子（GET /posts/user/{user_id}）"):
            return self.client.request("GET", f"/posts/user/{user_id}", params=params)

    def post_comments(
        self,
        *,
        post_id: int,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /posts/{id}/comments Query: limit,skip,select,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"帖子: 获取帖子评论（GET /posts/{post_id}/comments）"):
            return self.client.request("GET", f"/posts/{post_id}/comments", params=params)

    def add_post(self, *, payload: PostUpsertPayload) -> requests.Response:
        """POST /posts/add Body: title,userId,其他字段（模拟）"""
        with step("帖子: 新增帖子（模拟）（POST /posts/add）"):
            return self.client.request(
                "POST",
                "/posts/add",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def update_post(
        self,
        *,
        post_id: int,
        payload: PostUpsertPayload,
        method: str = "PUT",  # or PATCH
    ) -> requests.Response:
        """PUT/PATCH /posts/{id} Body: 更新字段（模拟）"""
        with step(f"帖子: 更新帖子（模拟）（{method} /posts/{post_id}）"):
            return self.client.request(
                method,
                f"/posts/{post_id}",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def delete_post(self, *, post_id: int) -> requests.Response:
        """DELETE /posts/{id}"""
        with step(f"帖子: 删除帖子（模拟）（DELETE /posts/{post_id}）"):
            return self.client.request("DELETE", f"/posts/{post_id}")

