from __future__ import annotations

from typing import Optional

import requests

from dj_api.http.models import merge_params
from dj_api.http.models import DelayQuery, PaginationQuery, SelectQuery, SortQuery
from dj_api.http.payloads import ProductUpsertPayload
from dj_api.services.base import BaseService
from dj_api.utils.steps import step


class ProductsService(BaseService):
    def list_products(
        self,
        *,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
        sort: Optional[SortQuery] = None,
    ) -> requests.Response:
        """GET /products Query: limit,skip,select,delay,sortBy,order"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
            (sort or SortQuery()).to_params(),
        )
        with step("商品: 获取商品列表（GET /products）"):
            return self.client.request("GET", "/products", params=params)

    def get_product(
        self,
        *,
        product_id: int,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /products/{id} Query: select,delay"""
        params = merge_params(
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"商品: 获取单个商品（GET /products/{product_id}）"):
            return self.client.request("GET", f"/products/{product_id}", params=params)

    def search_products(
        self,
        *,
        q: str,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /products/search Query: q,limit,skip,select,delay"""
        params = merge_params(
            {"q": q},
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step("商品: 搜索商品（GET /products/search）"):
            return self.client.request("GET", "/products/search", params=params)

    def categories(self, *, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /products/categories Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        with step("商品: 获取分类详情（GET /products/categories）"):
            return self.client.request("GET", "/products/categories", params=params)

    def category_list(self, *, delay: Optional[DelayQuery] = None) -> requests.Response:
        """GET /products/category-list Query: delay"""
        params = merge_params((delay or DelayQuery()).to_params())
        with step("商品: 获取分类列表（GET /products/category-list）"):
            return self.client.request("GET", "/products/category-list", params=params)

    def products_by_category(
        self,
        *,
        slug: str,
        pagination: Optional[PaginationQuery] = None,
        select: Optional[SelectQuery] = None,
        delay: Optional[DelayQuery] = None,
    ) -> requests.Response:
        """GET /products/category/{slug} Query: limit,skip,select,delay"""
        params = merge_params(
            (pagination or PaginationQuery()).to_params(),
            (select or SelectQuery()).to_params(),
            (delay or DelayQuery()).to_params(),
        )
        with step(f"商品: 按分类获取商品（GET /products/category/{slug}）"):
            return self.client.request("GET", f"/products/category/{slug}", params=params)

    def add_product(self, *, payload: ProductUpsertPayload) -> requests.Response:
        """POST /products/add Body: 商品字段（示例仅展示 title，其它字段允许）"""
        with step("商品: 新增商品（模拟）（POST /products/add）"):
            return self.client.request(
                "POST",
                "/products/add",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def update_product(
        self,
        *,
        product_id: int,
        payload: ProductUpsertPayload,
        method: str = "PUT",  # or PATCH
    ) -> requests.Response:
        """PUT/PATCH /products/{id} Body: 更新字段（模拟）"""
        with step(f"商品: 更新商品（模拟）（{method} /products/{product_id}）"):
            return self.client.request(
                method,
                f"/products/{product_id}",
                headers=self.json_content_type(),
                json_body=payload.to_dict(),
            )

    def delete_product(self, *, product_id: int) -> requests.Response:
        """DELETE /products/{id}"""
        with step(f"商品: 删除商品（模拟）（DELETE /products/{product_id}）"):
            return self.client.request("DELETE", f"/products/{product_id}")

