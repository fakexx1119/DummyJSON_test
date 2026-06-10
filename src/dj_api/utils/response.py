from __future__ import annotations

from typing import Any, Dict

import requests


def as_json(resp: requests.Response) -> Dict[str, Any]:
    try:
        data = resp.json()
    except Exception as e:
        raise AssertionError(f"响应不是JSON：status={resp.status_code}, text={resp.text[:500]}") from e
    if not isinstance(data, dict):
        # DummyJSON部分接口返回数组/字符串，这里保持一致：统一包成 dict 便于断言与Allure展示
        return {"_": data}
    return data

