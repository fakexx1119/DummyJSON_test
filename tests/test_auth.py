from __future__ import annotations

import pytest

import allure

from tests.assertions import assert_has_keys, assert_status


@pytest.mark.auth
@allure.feature("认证")
class TestAuth:
    @pytest.mark.smoke
    @allure.story("登录并获取当前用户（POST /auth/login + GET /auth/me）")
    @allure.title("认证-登录并获取当前用户信息")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_auth_login_and_me(self, services, tokens):
        assert tokens["access"], "未获取到 accessToken"
        resp = services["auth"].me_auth(access_token=tokens["access"])
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["id", "username", "email"])

    @allure.story("刷新会话（POST /auth/refresh）")
    @allure.title("认证-刷新 accessToken/refreshToken")
    @allure.severity(allure.severity_level.NORMAL)
    def test_auth_refresh(self, services, tokens):
        resp = services["auth"].refresh_auth(refreshToken=tokens["refresh"], expiresInMins=30)
        assert_status(resp, 200)
        data = resp.json()
        assert_has_keys(data, ["accessToken", "refreshToken"])

    @allure.story("兼容登录与当前用户（POST /user/login + GET /user/me）")
    @allure.title("认证-兼容接口登录并获取当前用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_login_and_me_compat(self, services):
        # 这里复用 conftest 里的账号
        from dj_api.config import settings

        login_resp = services["auth"].login_user(
            username=settings.username,
            password=settings.password,
            expiresInMins=30,
        )
        assert_status(login_resp, 200)
        login_data = login_resp.json()
        assert_has_keys(login_data, ["accessToken", "refreshToken", "username"])

        me_resp = services["auth"].me_user(access_token=login_data["accessToken"])
        assert_status(me_resp, 200)
        me_data = me_resp.json()
        assert_has_keys(me_data, ["id", "email"])

