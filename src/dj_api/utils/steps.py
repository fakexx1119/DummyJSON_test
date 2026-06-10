from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator


def _safe_import_allure():
    try:
        import allure  # type: ignore

        return allure
    except Exception:
        return None


@contextmanager
def step(title: str) -> Iterator[None]:
    allure = _safe_import_allure()
    if allure:
        with allure.step(title):
            yield
    else:
        yield

