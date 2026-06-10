from __future__ import annotations

from typing import Any, Mapping, Sequence

import requests


def _safe_import_allure():
    try:
        import allure  # type: ignore

        return allure
    except Exception:
        return None


def _attach_text(name: str, text: str) -> None:
    allure = _safe_import_allure()
    if not allure:
        return
    allure.attach(text, name=name, attachment_type=allure.attachment_type.TEXT)


def assert_status(resp: requests.Response, expected: int | Sequence[int] = 200) -> None:
    if isinstance(expected, int):
        ok = resp.status_code == expected
        exp_text = str(expected)
    else:
        ok = resp.status_code in expected
        exp_text = ",".join(map(str, expected))
    _attach_text("断言.期望状态码", exp_text)
    _attach_text("断言.实际状态码", str(resp.status_code))
    assert ok, f"HTTP状态码不符合：expected={exp_text}, got={resp.status_code}, body={resp.text}"


def assert_has_keys(obj: Mapping[str, Any], keys: Sequence[str]) -> None:
    missing = [k for k in keys if k not in obj]
    _attach_text("断言.期望包含字段", ",".join(keys))
    if missing:
        _attach_text("断言.缺少字段", ",".join(missing))
    assert not missing, f"缺少字段：{missing}，实际keys={list(obj.keys())}"

