from __future__ import annotations

import pytest

import allure

from dj_api.http.models import PaginationQuery, SelectQuery, SortQuery
from dj_api.http.payloads import UserUpsertPayload
from tests.assertions import assert_has_keys, assert_status


@pytest.mark.users
@allure.feature("用户")
class TestUsers:
    @pytest.mark.smoke
    @allure.story("用户列表（分页/字段/排序）（GET /users）")
    @allure.title("用户-用户列表（分页/字段筛选/排序）")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_users(self, services):
        resp = services["users"].list_users(
            pagination=PaginationQuery(limit=5, skip=10),
            select=SelectQuery(select=["id", "firstName", "age"]),
            sort=SortQuery(sortBy="firstName", order="asc"),
        )
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["users", "total", "skip", "limit"])

    @allure.story("获取单个用户（GET /users/{id}）")
    @allure.title("用户-获取单个用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user(self, services):
        resp = services["users"].get_user(user_id=1)
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["id", "firstName", "username"])

    @allure.story("搜索用户（GET /users/search?q=...）")
    @allure.title("用户-搜索用户（关键字）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_users(self, services):
        resp = services["users"].search_users(q="John", pagination=PaginationQuery(limit=3, skip=0))
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["users", "total"])

    @allure.story("过滤用户（GET /users/filter?key=...&value=...）")
    @allure.title("用户-过滤用户（key/value）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_users(self, services):
        resp = services["users"].filter_users(key="hair.color", value="Brown", pagination=PaginationQuery(limit=3, skip=0))
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["users", "total"])

    @allure.story("用户关联资源（购物车/帖子/待办）（GET /users/{id}/...）")
    @allure.title("用户-关联资源（购物车/帖子/待办）")
    @allure.severity(allure.severity_level.MINOR)
    def test_user_nested_resources(self, services):
        carts = services["users"].user_carts(user_id=6)
        assert_status(carts, 200)
        assert_has_keys(carts.json(), ["carts", "total"])

        posts = services["users"].user_posts(user_id=5)
        assert_status(posts, 200)
        assert_has_keys(posts.json(), ["posts", "total"])

        todos = services["users"].user_todos(user_id=5)
        assert_status(todos, 200)
        assert_has_keys(todos.json(), ["todos", "total"])

    @allure.story("新增/更新/删除用户（模拟）（POST/PUT/PATCH/DELETE）")
    @allure.title("用户-新增/更新/删除（模拟写接口）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_update_delete_user(self, services):
        add_resp = services["users"].add_user(
            payload=UserUpsertPayload(firstName="Muhammad", lastName="Ovi", age=250, email="demo@x.dummyjson.com")
        )
        assert_status(add_resp, (200, 201))
        assert_has_keys(add_resp.json(), ["id", "firstName"])

        update_resp = services["users"].update_user(user_id=2, method="PATCH", payload=UserUpsertPayload(lastName="Owais"))
        assert_status(update_resp, 200)
        assert update_resp.json().get("lastName") == "Owais"

        del_resp = services["users"].delete_user(user_id=1)
        assert_status(del_resp, 200)
        assert del_resp.json().get("isDeleted") is True

