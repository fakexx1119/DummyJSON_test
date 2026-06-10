from __future__ import annotations

import pytest

import allure

from dj_api.http.models import DelayQuery, PaginationQuery, SelectQuery, SortQuery
from dj_api.http.payloads import ProductUpsertPayload
from tests.assertions import assert_has_keys, assert_status


@pytest.mark.products
@allure.feature("商品")
class TestProducts:
    @pytest.mark.smoke
    @allure.story("商品列表（分页/字段/延迟/排序）（GET /products）")
    @allure.title("商品-商品列表（分页/字段筛选/延迟/排序）")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_products_with_params(self, services):
        resp = services["products"].list_products(
            pagination=PaginationQuery(limit=5, skip=0),
            select=SelectQuery(select=["id", "title", "price"]),
            delay=DelayQuery(delay=10),
            sort=SortQuery(sortBy="title", order="asc"),
        )
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["products", "total", "skip", "limit"])
        assert isinstance(data["products"], list)

    @allure.story("获取单个商品（GET /products/{id}）")
    @allure.title("商品-获取单个商品（字段筛选）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_product(self, services):
        resp = services["products"].get_product(product_id=1, select=SelectQuery(select="id,title,category"))
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["id", "title", "category"])

    @allure.story("搜索商品（GET /products/search?q=...）")
    @allure.title("商品-搜索商品（关键字）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_products(self, services):
        resp = services["products"].search_products(q="phone", pagination=PaginationQuery(limit=5, skip=0))
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["products", "total"])

    @allure.story("商品分类（GET /products/categories + /products/category-list）")
    @allure.title("商品-分类数据获取（两种接口）")
    @allure.severity(allure.severity_level.MINOR)
    def test_categories(self, services):
        resp1 = services["products"].categories()
        assert_status(resp1, 200)
        assert isinstance(resp1.json(), list)

        resp2 = services["products"].category_list()
        assert_status(resp2, 200)
        assert isinstance(resp2.json(), list)

    @allure.story("按分类获取商品（GET /products/category/{slug}）")
    @allure.title("商品-按分类获取商品列表")
    @allure.severity(allure.severity_level.NORMAL)
    def test_products_by_category(self, services):
        resp = services["products"].products_by_category(slug="smartphones")
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["products", "total"])

    @allure.story("新增/更新/删除商品（模拟）（POST/PUT/PATCH/DELETE）")
    @allure.title("商品-新增/更新/删除（模拟写接口）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_update_delete_product(self, services):
        add_resp = services["products"].add_product(
            payload=ProductUpsertPayload(
                title="BMW Pencil",
                description="接口自动化演示数据",
                category="smartphones",
                price=9.99,
                stock=10,
                brand="BMW",
                tags=["demo", "automation"],
                sku="DEMO-SKU-001",
                weight=2,
            )
        )
        assert_status(add_resp, (200, 201))
        add_data = add_resp.json()
        assert_has_keys(add_data, ["id", "title"])

        update_resp = services["products"].update_product(
            product_id=1,
            method="PATCH",
            payload=ProductUpsertPayload(title="iPhone Galaxy +1"),
        )
        assert_status(update_resp, 200)
        assert update_resp.json().get("title")

        del_resp = services["products"].delete_product(product_id=1)
        assert_status(del_resp, 200)
        assert del_resp.json().get("isDeleted") is True

