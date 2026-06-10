from __future__ import annotations

import pytest

import allure

from dj_api.http.models import PaginationQuery
from tests.assertions import assert_has_keys, assert_status


@pytest.mark.quotes
@allure.feature("名言")
class TestQuotes:
    @pytest.mark.smoke
    @allure.story("名言列表（GET /quotes）")
    @allure.title("名言-名言列表")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_quotes(self, services):
        resp = services["quotes"].list_quotes(pagination=PaginationQuery(limit=5, skip=0))
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["quotes", "total"])

    @allure.story("获取单条名言（GET /quotes/{id}）")
    @allure.title("名言-获取单条名言")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_quote(self, services):
        resp = services["quotes"].get_quote(quote_id=1)
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["id", "quote", "author"])

    @allure.story("随机名言（GET /quotes/random 可选 /random/{length}）")
    @allure.title("名言-随机名言（单条/多条）")
    @allure.severity(allure.severity_level.MINOR)
    def test_random_quote(self, services):
        resp = services["quotes"].random_quote()
        assert_status(resp, 200)
        assert_has_keys(resp.json(), ["id", "quote", "author"])

        resp2 = services["quotes"].random_quote(length=3)
        assert_status(resp2, 200)
        data2 = resp2.json()
        assert isinstance(data2, list)
        assert len(data2) == 3
        for item in data2:
            assert_has_keys(item, ["id", "quote", "author"])

