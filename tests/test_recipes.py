from __future__ import annotations

import pytest

import allure

from dj_api.http.models import PaginationQuery, SelectQuery, SortQuery
from dj_api.http.payloads import RecipeUpsertPayload
from tests.assertions import assert_has_keys, assert_status


@pytest.mark.recipes
@allure.feature("菜谱")
class TestRecipes:
    @pytest.mark.smoke
    @allure.story("菜谱列表（分页/字段/排序）（GET /recipes）")
    @allure.title("菜谱-菜谱列表（分页/字段筛选/排序）")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_recipes(self, services):
        resp = services["recipes"].list_recipes(
            pagination=PaginationQuery(limit=5, skip=0),
            select=SelectQuery(select=["id", "name", "image"]),
            sort=SortQuery(sortBy="name", order="asc"),
        )
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["recipes", "total"])

    @allure.story("获取单个菜谱（GET /recipes/{id}）")
    @allure.title("菜谱-获取单个菜谱")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_recipe(self, services):
        resp = services["recipes"].get_recipe(recipe_id=1)
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["id", "name", "ingredients", "instructions"])

    @allure.story("搜索菜谱（GET /recipes/search?q=...）")
    @allure.title("菜谱-搜索菜谱（关键字）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_recipes(self, services):
        resp = services["recipes"].search_recipes(q="Margherita")
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["recipes", "total"])

    @allure.story("菜谱标签（GET /recipes/tags）")
    @allure.title("菜谱-获取标签列表")
    @allure.severity(allure.severity_level.MINOR)
    def test_tags(self, services):
        resp = services["recipes"].tags()
        assert_status(resp, 200)
        assert isinstance(resp.json(), list)

    @allure.story("按标签获取菜谱（GET /recipes/tag/{tag}）")
    @allure.title("菜谱-按标签获取菜谱")
    @allure.severity(allure.severity_level.NORMAL)
    def test_recipes_by_tag(self, services):
        resp = services["recipes"].recipes_by_tag(tag="Pakistani")
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["recipes", "total"])

    @allure.story("按餐型获取菜谱（GET /recipes/meal-type/{mealType}）")
    @allure.title("菜谱-按餐型获取菜谱")
    @allure.severity(allure.severity_level.NORMAL)
    def test_recipes_by_meal_type(self, services):
        resp = services["recipes"].recipes_by_meal_type(meal_type="snack")
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["recipes", "total"])

    @allure.story("新增/更新/删除菜谱（模拟）（POST/PUT/PATCH/DELETE）")
    @allure.title("菜谱-新增/更新/删除（模拟写接口）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_update_delete_recipe(self, services):
        add_resp = services["recipes"].add_recipe(
            payload=RecipeUpsertPayload(
                name="美味披萨",
                ingredients=["披萨饼底", "番茄酱"],
                instructions=["烘烤后即可食用"],
                difficulty="Easy",
                cuisine="Italian",
                tags=["披萨", "演示"],
                mealType=["Dinner"],
                servings=2,
            )
        )
        assert_status(add_resp, (200, 201))
        assert_has_keys(add_resp.json(), ["id", "name"])

        update_resp = services["recipes"].update_recipe(recipe_id=1, method="PATCH", payload=RecipeUpsertPayload(name="Tasty Pizza"))
        assert_status(update_resp, 200)
        assert update_resp.json().get("name")

        del_resp = services["recipes"].delete_recipe(recipe_id=1)
        assert_status(del_resp, 200)
        assert del_resp.json().get("isDeleted") is True

