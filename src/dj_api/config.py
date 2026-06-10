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
    
    # 从环境变量读取配置（无默认值，必须使用环境变量）
    base_url = os.getenv("DUMMYJSON_BASE_URL")
    username = os.getenv("DUMMYJSON_USERNAME")
    password = os.getenv("DUMMYJSON_PASSWORD")
    allure_results_dir = os.getenv("ALLURE_RESULTS_DIR", "allure-results")
    allure_path = os.getenv("ALLURE_PATH")
    timeout_seconds = os.getenv("HTTP_TIMEOUT_SECONDS", "30")
    retry_attempts = os.getenv("HTTP_RETRY_ATTEMPTS", "2")
    retry_backoff_base_seconds = os.getenv("HTTP_RETRY_BACKOFF_BASE_SECONDS", "0.3")
    
    # 检查必需的环境变量
    if not base_url:
        raise ValueError(
            "❌ 缺少必需的环境变量: DUMMYJSON_BASE_URL\n"
            "请创建 .env 文件（本地开发）或在 GitHub Secrets 中配置"
        )
    if not username:
        raise ValueError(
            "❌ 缺少必需的环境变量: DUMMYJSON_USERNAME\n"
            "请创建 .env 文件（本地开发）或在 GitHub Secrets 中配置"
        )
    if not password:
        raise ValueError(
            "❌ 缺少必需的环境变量: DUMMYJSON_PASSWORD\n"
            "请创建 .env 文件（本地开发）或在 GitHub Secrets 中配置"
        )
    
    return Settings(
        base_url=base_url.rstrip("/"),
        username=username,
        password=password,
        allure_results_dir=allure_results_dir,
        allure_path=allure_path,
        timeout_seconds=float(timeout_seconds),
        retry_attempts=int(retry_attempts),
        retry_backoff_base_seconds=float(retry_backoff_base_seconds),
    )


settings = load_settings()

