from __future__ import annotations

from typing import Optional

import requests

from dj_api.http.models import DelayQuery, PaginationQuery, SelectQuery, SortQuery, merge_params
from dj_api.http.payloads import RecipeUpsertPayload
from dj_api.services.base import BaseService
from dj_api.utils.steps import step


class RecipesService(BaseService):
    def list_recipes(
        self,
        *,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
        sort: Optional[SortQuery] = None,
    ) -> requests.Response:
        """GET /recipes Query: limit,skip,select,delay,sortBy,order"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
            (sort or SortQuery()).to_params(),
        )
        with step("菜谱: 获取菜谱列表（GET /recipes）"):
            return self.client.request("GET", "/recipes", params=params)

    def get_recipe(
        self,
        *,
        recipe_id: int,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /recipes/{id} Query: select,delay"""
        params = merge_params(
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"菜谱: 获取单个菜谱（GET /recipes/{recipe_id}）"):
            return self.client.request("GET", f"/recipes/{recipe_id}", params=params)

    def search_recipes(
        self,
        *,
        q: str,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /recipes/search Query: q,limit,skip,select,delay"""
        params = merge_params(
            {"q": q},
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step("菜谱: 搜索菜谱（GET /recipes/search）"):
            return self.client.request("GET", "/recipes/search", params=params)

    def tags(self, *, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /recipes/tags Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        with step("菜谱: 获取菜谱标签列表（GET /recipes/tags）"):
            return self.client.request("GET", "/recipes/tags", params=params)

    def recipes_by_tag(
        self,
        *,
        tag: str,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /recipes/tag/{tag} Query: limit,skip,select,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"菜谱: 按标签获取菜谱（GET /recipes/tag/{tag}）"):
            return self.client.request("GET", f"/recipes/tag/{tag}", params=params)

    def recipes_by_meal_type(
        self,
        *,
        meal_type: str,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /recipes/meal-type/{mealType} Query: limit,skip,select,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"菜谱: 按餐型获取菜谱（GET /recipes/meal-type/{meal_type}）"):
            return self.client.request("GET", f"/recipes/meal-type/{meal_type}", params=params)

    def add_recipe(self, *, payload: RecipeUpsertPayload) -> requests.Response:
        """POST /recipes/add Body: name + 其他字段（模拟）"""
        with step("菜谱: 新增菜谱（模拟）（POST /recipes/add）"):
            return self.client.request(
                "POST",
                "/recipes/add",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def update_recipe(
        self,
        *,
        recipe_id: int,
        payload: RecipeUpsertPayload,
        method: str = "PUT",  # or PATCH
    ) -> requests.Response:
        """PUT/PATCH /recipes/{id} Body: 更新字段（模拟）"""
        with step(f"菜谱: 更新菜谱（模拟）（{method} /recipes/{recipe_id}）"):
            return self.client.request(
                method,
                f"/recipes/{recipe_id}",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def delete_recipe(self, *, recipe_id: int) -> requests.Response:
        """DELETE /recipes/{id}"""
        with step(f"菜谱: 删除菜谱（模拟）（DELETE /recipes/{recipe_id}）"):
            return self.client.request("DELETE", f"/recipes/{recipe_id}")

