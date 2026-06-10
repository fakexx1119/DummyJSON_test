from __future__ import annotations

import pytest

import allure

from dj_api.http.models import PaginationQuery
from dj_api.http.payloads import CommentUpsertPayload
from tests.assertions import assert_has_keys, assert_status


@pytest.mark.comments
@allure.feature("评论")
class TestComments:
    @pytest.mark.smoke
    @allure.story("评论列表（GET /comments）")
    @allure.title("评论-评论列表")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_comments(self, services):
        resp = services["comments"].list_comments(pagination=PaginationQuery(limit=5, skip=0))
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["comments", "total"])

    @allure.story("获取单个评论（GET /comments/{id}）")
    @allure.title("评论-获取单个评论")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_comment(self, services):
        resp = services["comments"].get_comment(comment_id=1)
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["id", "body", "postId", "user"])

    @allure.story("按帖子查询评论（GET /comments/post/{postId}）")
    @allure.title("评论-按帖子查询评论")
    @allure.severity(allure.severity_level.NORMAL)
    def test_comments_by_post(self, services):
        resp = services["comments"].comments_by_post(post_id=6)
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["comments", "total"])

    @allure.story("新增/更新/删除评论（模拟）（POST/PUT/PATCH/DELETE）")
    @allure.title("评论-新增/更新/删除（模拟写接口）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_update_delete_comment(self, services):
        add_resp = services["comments"].add_comment(
            payload=CommentUpsertPayload(body="这个观点我完全赞同！", postId=3, userId=5)
        )
        assert_status(add_resp, (200, 201))
        assert_has_keys(add_resp.json(), ["id", "body", "postId", "user"])

        update_resp = services["comments"].update_comment(
            comment_id=1, method="PATCH", payload=CommentUpsertPayload(body="I think I should shift to the moon")
        )
        assert_status(update_resp, 200)
        assert update_resp.json().get("body")

        del_resp = services["comments"].delete_comment(comment_id=1)
        assert_status(del_resp, 200)
        assert del_resp.json().get("isDeleted") is True

