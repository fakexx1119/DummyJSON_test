from __future__ import annotations

import pytest

import allure

from tests.assertions import assert_has_keys, assert_status


@pytest.mark.system
@allure.feature("系统")
class TestSystem:
    @pytest.mark.smoke
    @allure.story("连通性检查（GET /test）")
    @allure.title("系统-连通性检查")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_test_route(self, services):
        resp = services["system"].test_route()
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["status", "method"])

    @allure.story("获取客户端IP（GET /ip）")
    @allure.title("系统-获取客户端IP与UA")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ip(self, services):
        resp = services["system"].ip()
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["ip", "userAgent"])

    @allure.story("Mock HTTP 响应（GET /http/{code}/{message?}）")
    @allure.title("系统-Mock HTTP 状态码与消息")
    @allure.severity(allure.severity_level.MINOR)
    def test_http_mock(self, services):
        resp1 = services["system"].http_mock(code=200)
        assert_status(resp1, 200)
        assert str(resp1.json().get("status")) == "200"

        resp2 = services["system"].http_mock(code=404, message="Hello_Peter")
        assert_status(resp2, 404)
        assert resp2.json().get("message") == "Hello_Peter"

    @allure.story("生成占位图片（GET /image/...）")
    @allure.title("系统-占位图片生成（PNG/WebP）")
    @allure.severity(allure.severity_level.MINOR)
    def test_image_placeholder_png(self, services):
        resp = services["system"].image(
            size="50",
            text="Hello",
            type="png",
            fontFamily="poppins",
            fontSize=14,
        )
        assert_status(resp, 200)
        assert (resp.headers.get("Content-Type") or "").lower().startswith("image/")
        assert len(resp.content) > 10

        resp2 = services["system"].image(
            size="60x30",
            background="282828",
            color="ffffff",
            text="WebP",
            type="webp",
        )
        assert_status(resp2, 200)
        assert (resp2.headers.get("Content-Type") or "").lower().startswith("image/")
        assert len(resp2.content) > 10

    @allure.story("生成 identicon（GET /icon/{hash}/{size}）")
    @allure.title("系统-生成 identicon（SVG）")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_icon_svg(self, services):
        resp = services["system"].icon(hash="abc123", size=64, type="svg")
        assert_status(resp, 200)
        ct = (resp.headers.get("Content-Type") or "").lower()
        assert "svg" in ct or "xml" in ct
        assert b"<svg" in resp.content[:200].lower()

