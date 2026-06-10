from __future__ import annotations

import pytest

import allure

from dj_api.http.models import PaginationQuery
from dj_api.http.payloads import PostUpsertPayload
from tests.assertions import assert_has_keys, assert_status


@pytest.mark.posts
@allure.feature("帖子")
class TestPosts:
    @pytest.mark.smoke
    @allure.story("帖子列表（GET /posts）")
    @allure.title("帖子-帖子列表")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_posts(self, services):
        resp = services["posts"].list_posts(pagination=PaginationQuery(limit=5, skip=0))
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["posts", "total"])

    @allure.story("获取单个帖子（GET /posts/{id}）")
    @allure.title("帖子-获取单个帖子")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_post(self, services):
        resp = services["posts"].get_post(post_id=1)
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["id", "title", "userId"])

    @allure.story("搜索帖子（GET /posts/search?q=...）")
    @allure.title("帖子-搜索帖子（关键字）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_posts(self, services):
        resp = services["posts"].search_posts(q="love")
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["posts", "total"])

    @allure.story("帖子标签（GET /posts/tags + /posts/tag-list）")
    @allure.title("帖子-标签获取（两种接口）")
    @allure.severity(allure.severity_level.MINOR)
    def test_tags(self, services):
        resp1 = services["posts"].tags()
        assert_status(resp1, 200)
        assert isinstance(resp1.json(), list)

        resp2 = services["posts"].tag_list()
        assert_status(resp2, 200)
        assert isinstance(resp2.json(), list)

    @allure.story("按标签获取帖子（GET /posts/tag/{slug}）")
    @allure.title("帖子-按标签获取帖子")
    @allure.severity(allure.severity_level.NORMAL)
    def test_posts_by_tag(self, services):
        resp = services["posts"].posts_by_tag(slug="life")
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["posts", "total"])

    @allure.story("按用户获取帖子（GET /posts/user/{userId}）")
    @allure.title("帖子-按用户获取帖子")
    @allure.severity(allure.severity_level.NORMAL)
    def test_posts_by_user(self, services):
        resp = services["posts"].posts_by_user(user_id=5)
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["posts", "total"])

    @allure.story("获取帖子评论（GET /posts/{id}/comments）")
    @allure.title("帖子-获取帖子评论列表")
    @allure.severity(allure.severity_level.NORMAL)
    def test_post_comments(self, services):
        resp = services["posts"].post_comments(post_id=1)
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["comments", "total"])

    @allure.story("新增/更新/删除帖子（模拟）（POST/PUT/PATCH/DELETE）")
    @allure.title("帖子-新增/更新/删除（模拟写接口）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_update_delete_post(self, services):
        add_resp = services["posts"].add_post(payload=PostUpsertPayload(title="我喜欢一个人。", userId=5))
        assert_status(add_resp, (200, 201))
        assert_has_keys(add_resp.json(), ["id", "title", "userId"])

        update_resp = services["posts"].update_post(post_id=1, method="PATCH", payload=PostUpsertPayload(title="I think I should shift to the moon"))
        assert_status(update_resp, 200)
        assert update_resp.json().get("title")

        del_resp = services["posts"].delete_post(post_id=1)
        assert_status(del_resp, 200)
        assert del_resp.json().get("isDeleted") is True

