# DummyJSON 接口自动化（Pytest + Allure，POM/Service 框架）

## 目标

- 基于公开免费的 DummyJSON（`https://dummyjson.com`）构建**可交付**的接口自动化项目
- 使用 **POM 思路（API Service Object）**：每个模块一个 Service，方法与接口一一对应
- 每个接口都在脚本里体现：**路径/Query/Body 参数模型化** + 对应用例
- Allure 报告增强：请求/响应附件、步骤、标签、分类、环境信息

## 目录结构（核心）

- `src/dj_api/`：框架代码（Client、Service、参数模型、Allure附件封装）
- `tests/`：pytest 用例（按模块拆分）
- `docs/`：接口参数总表（给领导看的清单）
- `allure/`：Allure 额外配置（分类/模板）

## 快速开始

### 1) 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 2) 配置环境变量（可选）

复制 `.env.example` 为 `.env`，按需修改账号与 base_url。
如你本机没有把 `allure` 加到 PATH，可在 `.env` 里配置 `ALLURE_PATH`（示例已提供）。

### 3) 运行测试并生成 Allure 原始结果

```bash
pytest -s --alluredir=allure-results
```

### 4) 生成/查看 Allure 报告

你需要安装 Allure 命令行工具（不是 pip 包）。

- 生成静态报告：

```bash
allure generate allure-results -o allure-report --clean
```

- 启动本地查看：

```bash
allure serve allure-results
```

### 5) Windows 一键运行并自动打开 Allure（已修复“找不到 allure 命令”问题）

如果你没有把 Allure 加到 PATH，直接用项目脚本即可（会自动读取 `.env` 里的 `ALLURE_PATH`，没有则用默认值）。

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_tests_and_allure.ps1
```

### 6) Python 一键运行并自动打开 Allure（推荐：不依赖 PowerShell 执行策略）

```bash
python .\scripts\run_tests_and_allure.py
```

#### 生成“可发领导”的静态 HTML 报告（不需要本地服务）

```powershell
$env:ALLURE_MODE="generate"
python .\scripts\run_tests_and_allure.py
```

## 站点说明

DummyJSON 是公开的免费 Fake REST API，适合做接口自动化演示与框架落地：
- 文档：`https://dummyjson.com/docs`
- 模块多：Products/Carts/Users/Posts/Comments/Todos/Quotes/Recipes + System(Http/Image/IP/Test)

