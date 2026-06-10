from __future__ import annotations

from typing import Any, Mapping

from dj_api.utils.json_tools import to_pretty_json, try_parse_json


def _safe_import_allure():
    try:
        import allure  # type: ignore

        return allure
    except Exception:
        return None


def attach_text(name: str, text: str) -> None:
    allure = _safe_import_allure()
    if not allure:
        return
    allure.attach(text, name=name, attachment_type=allure.attachment_type.TEXT)


def attach_bytes(name: str, data: bytes, *, mime: str) -> None:
    allure = _safe_import_allure()
    if not allure:
        return
    # Allure attachment_type 枚举有限，这里按 mime 做一个常用映射
    mime_lower = (mime or "").lower()
    if "png" in mime_lower:
        at = allure.attachment_type.PNG
    elif "jpeg" in mime_lower or "jpg" in mime_lower:
        at = allure.attachment_type.JPG
    elif "svg" in mime_lower:
        at = allure.attachment_type.SVG
    elif "webp" in mime_lower:
        # 没有专用类型时用 extension 兜底
        allure.attach(data, name=name, extension="webp")
        return
    else:
        # 兜底：用 extension 挂原始二进制
        ext = (mime_lower.split("/")[-1] if "/" in mime_lower else "bin") or "bin"
        allure.attach(data, name=name, extension=ext)
        return
    allure.attach(data, name=name, attachment_type=at)


def attach_json(name: str, obj: Any) -> None:
    allure = _safe_import_allure()
    if not allure:
        return
    allure.attach(to_pretty_json(obj), name=name, attachment_type=allure.attachment_type.JSON)


def attach_kv_table(name: str, mapping: Mapping[str, Any]) -> None:
    # 用 JSON 形式展示更直观
    attach_json(name, dict(mapping))


def attach_response(name: str, status_code: int, headers: Mapping[str, Any], body_text: str) -> None:
    attach_text(f"{name}.状态码", str(status_code))
    attach_kv_table(f"{name}.响应头", headers)
    parsed = try_parse_json(body_text)
    if parsed is not None:
        attach_json(f"{name}.响应体(JSON)", parsed)
    else:
        attach_text(f"{name}.响应体(文本)", body_text)

