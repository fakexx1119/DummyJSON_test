from __future__ import annotations

import pytest

import allure

from dj_api.http.models import PaginationQuery
from dj_api.http.payloads import TodoUpsertPayload
from tests.assertions import assert_has_keys, assert_status


@pytest.mark.todos
@allure.feature("待办")
class TestTodos:
    @pytest.mark.smoke
    @allure.story("待办列表（GET /todos）")
    @allure.title("待办-待办列表")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_todos(self, services):
        resp = services["todos"].list_todos(pagination=PaginationQuery(limit=5, skip=0))
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["todos", "total"])

    @allure.story("获取单个待办（GET /todos/{id}）")
    @allure.title("待办-获取单个待办")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_todo(self, services):
        resp = services["todos"].get_todo(todo_id=1)
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["id", "todo", "completed", "userId"])

    @allure.story("随机待办（GET /todos/random 可选 /random/{length}）")
    @allure.title("待办-随机待办（单个/批量）")
    @allure.severity(allure.severity_level.MINOR)
    def test_random_todo(self, services):
        resp = services["todos"].random_todo()
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["id", "todo"])

        resp2 = services["todos"].random_todo(length=10)
        assert_status(resp2, 200)
        data2 = resp2.json()
        assert isinstance(data2, list)
        assert 1 <= len(data2) <= 10
        for item in data2:
            assert_has_keys(item, ["id", "todo", "completed", "userId"])

    @allure.story("按用户查询待办（GET /todos/user/{userId}）")
    @allure.title("待办-按用户查询待办")
    @allure.severity(allure.severity_level.NORMAL)
    def test_todos_by_user(self, services):
        resp = services["todos"].todos_by_user(user_id=5)
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["todos", "total"])

    @allure.story("新增/更新/删除待办（模拟）（POST/PUT/PATCH/DELETE）")
    @allure.title("待办-新增/更新/删除（模拟写接口）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_update_delete_todo(self, services):
        add_resp = services["todos"].add_todo(payload=TodoUpsertPayload(todo="在项目中使用 DummyJSON", completed=False, userId=5))
        assert_status(add_resp, (200, 201))
        assert_has_keys(add_resp.json(), ["id", "todo", "completed", "userId"])

        update_resp = services["todos"].update_todo(todo_id=1, method="PATCH", payload=TodoUpsertPayload(completed=False))
        assert_status(update_resp, 200)
        assert update_resp.json().get("completed") in (True, False)

        del_resp = services["todos"].delete_todo(todo_id=1)
        assert_status(del_resp, 200)
        assert del_resp.json().get("isDeleted") is True

