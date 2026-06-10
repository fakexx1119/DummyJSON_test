from __future__ import annotations

import json
from typing import Any


def try_parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except Exception:
        return None


def to_pretty_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True, default=str)

