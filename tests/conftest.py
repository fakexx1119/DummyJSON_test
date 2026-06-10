from __future__ import annotations

import json
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Iterator

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dj_api.config import settings  # noqa: E402
from dj_api.http.client import APIClient  # noqa: E402
from dj_api.services import (  # noqa: E402
    AuthService,
    CartsService,
    CommentsService,
    PostsService,
    ProductsService,
    QuotesService,
    RecipesService,
    SystemService,
    TodosService,
    UsersService,
)


def _ensure_allure_meta(results_dir: Path) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)

    # categories.json（优先使用仓库里的）
    src_categories = ROOT / "allure" / "categories.json"
    if src_categories.exists():
        shutil.copyfile(src_categories, results_dir / "categories.json")

    # environment.properties
    env_lines = [
        f"接口地址={settings.base_url}",
        f"Python版本={platform.python_version()}",
        f"操作系统={platform.platform()}",
    ]
    (results_dir / "environment.properties").write_text("\n".join(env_lines), encoding="utf-8")

    # executor.json（让报告里显示“执行器信息”）
    executor = {
        "name": "本地-pytest",
        "type": "pytest",
        "buildName": "DummyJSON API 自动化",
        "buildUrl": "",
        "reportUrl": "",
    }
    (results_dir / "executor.json").write_text(json.dumps(executor, ensure_ascii=False, indent=2), encoding="utf-8")


def pytest_sessionstart(session: pytest.Session) -> None:
    results_dir = Path(os.getenv("ALLURE_RESULTS_DIR", settings.allure_results_dir))
    _ensure_allure_meta(results_dir)


def pytest_runtest_setup(item: pytest.Item) -> None:
    """
    让 Allure 的 Suites 视图尽量中文化：
    - parentSuite: DummyJSON接口自动化
    - suite: 按模块（系统/认证/商品/...）
    - subSuite: 按测试文件（中文）
    """
    try:
        import allure  # type: ignore

        allure.dynamic.parent_suite("DummyJSON接口自动化")

        module_map = {
            "system": "系统",
            "auth": "认证",
            "products": "商品",
            "carts": "购物车",
            "users": "用户",
            "posts": "帖子",
            "comments": "评论",
            "todos": "待办",
            "quotes": "名言",
            "recipes": "菜谱",
        }
        suite = "其他"
        for key, cn in module_map.items():
            if item.get_closest_marker(key):
                suite = cn
                break
        allure.dynamic.suite(suite)

        file_cn_map = {
            "test_system.py": "系统接口用例",
            "test_auth.py": "认证接口用例",
            "test_products.py": "商品接口用例",
            "test_carts.py": "购物车接口用例",
            "test_users.py": "用户接口用例",
            "test_posts.py": "帖子接口用例",
            "test_comments.py": "评论接口用例",
            "test_todos.py": "待办接口用例",
            "test_quotes.py": "名言接口用例",
            "test_recipes.py": "菜谱接口用例",
        }
        filename = os.path.basename(str(item.fspath))
        allure.dynamic.sub_suite(file_cn_map.get(filename, filename))
    except Exception:
        # 不影响测试执行
        return


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient(base_url=settings.base_url, timeout_seconds=settings.timeout_seconds)


@pytest.fixture(scope="session")
def services(api_client: APIClient) -> Dict[str, Any]:
    return {
        "system": SystemService(api_client),
        "auth": AuthService(api_client),
        "products": ProductsService(api_client),
        "carts": CartsService(api_client),
        "users": UsersService(api_client),
        "posts": PostsService(api_client),
        "comments": CommentsService(api_client),
        "todos": TodosService(api_client),
        "quotes": QuotesService(api_client),
        "recipes": RecipesService(api_client),
    }


@pytest.fixture(scope="session")
def tokens(services: Dict[str, Any]) -> Dict[str, str]:
    """
    DummyJSON：公开用户可登录获取 accessToken/refreshToken。
    """
    auth: AuthService = services["auth"]
    resp = auth.login_auth(username=settings.username, password=settings.password, expiresInMins=30)
    assert resp.status_code == 200, f"login失败 status={resp.status_code}, body={resp.text}"
    data = resp.json()
    return {
        "access": data.get("accessToken", ""),
        "refresh": data.get("refreshToken", ""),
        "user_id": str(data.get("id", "")),
        "username": str(data.get("username", "")),
    }

