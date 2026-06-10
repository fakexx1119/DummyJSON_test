from __future__ import annotations

import pytest

import allure

from dj_api.http.models import PaginationQuery
from dj_api.http.payloads import CartProductItem, CartUpsertPayload
from tests.assertions import assert_has_keys, assert_status


@pytest.mark.carts
@allure.feature("购物车")
class TestCarts:
    @pytest.mark.smoke
    @allure.story("购物车列表（GET /carts）")
    @allure.title("购物车-购物车列表")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_carts(self, services):
        resp = services["carts"].list_carts(pagination=PaginationQuery(limit=5, skip=0))
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["carts", "total", "skip", "limit"])

    @allure.story("获取单个购物车（GET /carts/{id}）")
    @allure.title("购物车-获取单个购物车")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_cart(self, services):
        resp = services["carts"].get_cart(cart_id=1)
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["id", "products", "userId"])

    @allure.story("查询用户购物车（GET /carts/user/{userId}）")
    @allure.title("购物车-查询用户购物车")
    @allure.severity(allure.severity_level.NORMAL)
    def test_carts_by_user(self, services):
        resp = services["carts"].carts_by_user(user_id=5)
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["carts", "total"])

    @allure.story("新增/更新/删除购物车（模拟）（POST/PUT/PATCH/DELETE）")
    @allure.title("购物车-新增/更新/删除（模拟写接口）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_update_delete_cart(self, services):
        add_resp = services["carts"].add_cart(
            payload=CartUpsertPayload(
                userId=1,
                products=[
                    CartProductItem(id=144, quantity=4),
                    CartProductItem(id=98, quantity=1),
                ],
            )
        )
        assert_status(add_resp, (200, 201))
        assert_has_keys(add_resp.json(), ["id", "products", "userId"])

        update_resp = services["carts"].update_cart(
            cart_id=1,
            method="PUT",
            payload=CartUpsertPayload(merge=True, products=[CartProductItem(id=1, quantity=1)]),
        )
        assert_status(update_resp, 200)
        assert_has_keys(update_resp.json(), ["id", "products"])

        del_resp = services["carts"].delete_cart(cart_id=1)
        assert_status(del_resp, 200)
        assert del_resp.json().get("isDeleted") is True

