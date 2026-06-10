from __future__ import annotations

import os
import subprocess
import sys
import webbrowser
from pathlib import Path

from dotenv import load_dotenv


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_env() -> None:
    root = _project_root()
    load_dotenv(root / ".env", override=False)


def _get_allure_cmd() -> list[str]:
    """
    优先级：
    1) 环境变量 ALLURE_PATH（指向 allure.bat 或 allure 可执行文件）
    2) 直接使用 'allure'（如果已加入 PATH）
    """
    allure_path = os.getenv(
        "ALLURE_PATH",
        r"F:\allure-commandline-2.35.1\allure-2.35.1\bin\allure.bat",
    ).strip()

    if allure_path:
        p = Path(allure_path)
        if p.suffix.lower() == ".bat":
            # .bat 必须通过 cmd 调用
            return ["cmd", "/c", str(p)]
        return [allure_path]

    return ["allure"]


def main() -> int:
    _load_env()

    root = _project_root()
    results_dir = os.getenv("ALLURE_RESULTS_DIR", "allure-results").strip() or "allure-results"
    mode = (os.getenv("ALLURE_MODE", "serve") or "serve").strip().lower()  # serve | generate
    report_dir = os.getenv("ALLURE_REPORT_DIR", "allure-report").strip() or "allure-report"

    env = os.environ.copy()
    env["ALLURE_RESULTS_DIR"] = results_dir  # 供 conftest 写入环境信息/分类等

    print(f"[1/3] 运行 pytest，输出到：{results_dir}")
    pytest_cmd = [sys.executable, "-m", "pytest", "-s", f"--alluredir={results_dir}"]
    r = subprocess.run(pytest_cmd, cwd=str(root), env=env)
    if r.returncode != 0:
        print(f"pytest 失败，退出码：{r.returncode}")
        return r.returncode

    allure_base = _get_allure_cmd()

    if mode == "generate":
        print(f"[2/3] 生成静态 Allure 报告：{report_dir}")
        gen_cmd = allure_base + ["generate", results_dir, "-o", report_dir, "--clean"]
        try:
            rc = subprocess.call(gen_cmd, cwd=str(root), env=env)
        except FileNotFoundError:
            print("未找到 Allure 命令行（generate 失败）。请配置 ALLURE_PATH 或加入 PATH。")
            return 1
        if rc != 0:
            print(f"allure generate 失败，退出码：{rc}")
            return rc

        index = (root / report_dir / "index.html").resolve()
        print("[3/3] 打开静态报告（浏览器）")
        webbrowser.open(index.as_uri())
        return 0

    print("[2/3] 启动 Allure（serve 会自动打开浏览器）")
    allure_cmd = allure_base + ["serve", results_dir]
    try:
        # allure serve 会阻塞当前进程（直到你 Ctrl+C 停止）
        return subprocess.call(allure_cmd, cwd=str(root), env=env)
    except FileNotFoundError:
        print("未找到 Allure 命令行。请确认：")
        print("- 已安装 Allure Commandline；或")
        print("- 在 .env / 环境变量里配置 ALLURE_PATH 指向 allure.bat；或")
        print("- 已把 allure 加入 PATH（终端里能直接执行 allure）。")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

