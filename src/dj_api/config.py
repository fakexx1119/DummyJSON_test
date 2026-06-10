from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _load_env() -> None:
    # 本地开发：允许使用 .env（可选，不强制）
    load_dotenv(override=False)


@dataclass(frozen=True)
class Settings:
    base_url: str
    username: str
    password: str
    allure_results_dir: str
    allure_path: str
    timeout_seconds: float
    retry_attempts: int
    retry_backoff_base_seconds: float


def load_settings() -> Settings:
    _load_env()
    return Settings(
        base_url=os.getenv("DUMMYJSON_BASE_URL", "https://dummyjson.com").rstrip("/"),
        username=os.getenv("DUMMYJSON_USERNAME", "emilys"),
        password=os.getenv("DUMMYJSON_PASSWORD", "emilyspass"),
        allure_results_dir=os.getenv("ALLURE_RESULTS_DIR", "allure-results"),
        allure_path=os.getenv(
            "ALLURE_PATH",
            r"F:\allure-commandline-2.35.1\allure-2.35.1\bin\allure.bat",
        ),
        timeout_seconds=float(os.getenv("HTTP_TIMEOUT_SECONDS", "30")),
        retry_attempts=int(os.getenv("HTTP_RETRY_ATTEMPTS", "2")),
        retry_backoff_base_seconds=float(os.getenv("HTTP_RETRY_BACKOFF_BASE_SECONDS", "0.3")),
    )


settings = load_settings()

