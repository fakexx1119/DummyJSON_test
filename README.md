# DummyJSON 接口自动化测试框架

<div align="center">

**基于 Pytest + Allure 的企业级 API 自动化测试解决方案**

采用 POM（Page Object Model）架构设计，针对 [DummyJSON](https://dummyjson.com) 免费 REST API 构建的完整接口自动化测试项目。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-8.3+-green.svg)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.35+-orange.svg)](https://allurereport.org/)

</div>

---

## ⚡ 快速启动

**一行命令运行测试并自动打开 Allure 报告：**

```bash
python scripts/run_tests_and_allure.py
```

该脚本会自动：
1. ✅ 执行所有 pytest 测试用例
2. ✅ 生成 Allure 测试结果
3. ✅ 启动 Allure 服务并自动在浏览器中打开报告

> 💡 **提示**：首次使用前请先安装依赖（见下方[快速开始](#-快速开始)章节）

---

## 📋 目录

- [项目简介](#项目简介)
- [核心特性](#核心特性)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [架构设计](#架构设计)
- [使用示例](#使用示例)
- [报告展示](#报告展示)
- [最佳实践](#最佳实践)

---

## 🎯 项目简介

本项目是一个**可交付的企业级接口自动化测试框架**，展示了如何构建高质量、可维护的 API 自动化测试体系。

### 核心价值

✅ **完整的 POM 架构实现** - 每个业务模块对应一个 Service，方法与接口一一对应  
✅ **参数模型化设计** - 所有 Query 参数和 Request Body 均使用 Pydantic 模型封装  
✅ **企业级报告增强** - Allure 报告包含请求/响应详情、cURL 命令、耗时统计等  
✅ **智能重试机制** - 自动处理网络抖动、429、5xx 错误（指数退避策略）  
✅ **模块化测试组织** - 按业务域拆分测试用例，支持标记分类（smoke/regression）  
✅ **一键运行脚本** - 自动执行测试并生成/打开 Allure 报告  

---

## ✨ 核心特性

### 1️⃣ 参数与请求体模型化

使用 Pydantic 定义类型安全的参数模型：

```python
# Query 参数模型
pagination = PaginationQuery(limit=5, skip=0)
select = SelectQuery(select=["id", "title", "price"])
sort = SortQuery(sortBy="title", order="asc")

# Request Body 模型
payload = ProductUpsertPayload(
    title="BMW Pencil",
    description="接口自动化演示数据",
    category="smartphones",
    price=9.99,
    stock=10
)
```

### 2️⃣ Allure 报告深度集成

- ✅ 自动附加请求/响应详情（状态码、Headers、Body）
- ✅ 生成可复制的 cURL 命令（便于问题复现）
- ✅ 记录请求耗时（性能分析）
- ✅ 支持图片附件展示
- ✅ 中文化套件名称（parentSuite/suite/subSuite）
- ✅ 失败分类统计（HTTP 4xx/5xx、断言失败、用例异常）
- ✅ 环境信息展示（Python 版本、操作系统、接口地址）

### 3️⃣ 智能重试机制

遇到以下情况自动重试：
- 网络超时或连接错误
- HTTP 429（限流）
- HTTP 5xx（服务端错误）

采用**指数退避 + 随机抖动**策略，避免雪崩效应。

### 4️⃣ 统一的断言封装

```python
# 状态码断言（支持单个值或多个值）
assert_status(resp, 200)
assert_status(resp, (200, 201))

# 字段存在性断言
assert_has_keys(data, ["id", "title", "price"])
```

所有断言结果自动附加到 Allure 报告中。

### 5️⃣ 灵活的配置管理

通过 `.env` 文件管理环境变量，支持不同环境切换：

```bash
DUMMYJSON_BASE_URL=https://dummyjson.com
DUMMYJSON_USERNAME=emilys
DUMMYJSON_PASSWORD=emilyspass
HTTP_TIMEOUT_SECONDS=30
HTTP_RETRY_ATTEMPTS=2
```

---

## 🛠 技术栈

| 类别 | 技术 | 版本 |
|------|------|------|
| **测试框架** | pytest | >= 8.3.3 |
| **报告工具** | allure-pytest | >= 2.13.5 |
| **HTTP 客户端** | requests | >= 2.32.3 |
| **数据模型** | pydantic | >= 2.10.6 |
| **配置管理** | python-dotenv | >= 1.0.1 |
| **重试机制** | tenacity | >= 9.0.0 |
| **配置文件** | PyYAML | >= 6.0.2 |

---

## 📁 项目结构

```
DummyJSON-API-Automation/
├── src/dj_api/                  # 框架核心代码
│   ├── config.py                # 全局配置管理（从 .env 读取）
│   ├── http/                    # HTTP 层
│   │   ├── client.py            # 统一 HTTP 客户端（重试/Allure 集成）
│   │   ├── models.py            # Query 参数模型（Pydantic）
│   │   └── payloads.py          # Request Body 模型（Pydantic）
│   ├── services/                # API Service 层（POM 核心）
│   │   ├── base.py              # BaseService（通用方法）
│   │   ├── auth.py              # 认证服务
│   │   ├── products.py          # 商品服务
│   │   ├── carts.py             # 购物车服务
│   │   ├── users.py             # 用户服务
│   │   ├── posts.py             # 帖子服务
│   │   ├── comments.py          # 评论服务
│   │   ├── todos.py             # 待办事项服务
│   │   ├── quotes.py            # 名言服务
│   │   ├── recipes.py           # 菜谱服务
│   │   └── system.py            # 系统接口（IP/HTTP 测试等）
│   └── utils/                   # 工具类
│       ├── allure_attach.py     # Allure 附件封装
│       ├── steps.py             # Allure 步骤装饰器
│       ├── json_tools.py        # JSON 工具
│       └── response.py          # 响应处理工具
├── tests/                       # 测试用例
│   ├── conftest.py              # pytest fixtures（共享资源）
│   ├── assertions.py            # 通用断言封装
│   ├── test_auth.py             # 认证接口测试
│   ├── test_products.py         # 商品接口测试
│   ├── test_carts.py            # 购物车接口测试
│   ├── test_users.py            # 用户接口测试
│   ├── test_posts.py            # 帖子接口测试
│   ├── test_comments.py         # 评论接口测试
│   ├── test_todos.py            # 待办事项测试
│   ├── test_quotes.py           # 名言接口测试
│   ├── test_recipes.py          # 菜谱接口测试
│   └── test_system.py           # 系统接口测试
├── allure/                      # Allure 配置
│   └── categories.json          # 失败分类配置
├── scripts/                     # 自动化脚本
│   ├── run_tests_and_allure.py  # Python 一键运行脚本
│   └── run_tests_and_allure.ps1 # PowerShell 一键运行脚本
├── allure-results/              # Allure 原始结果（自动生成）
├── allure-report/               # Allure 静态报告（自动生成）
├── docs/                        # 文档
├── .env.example                 # 环境变量模板
├── pytest.ini                   # pytest 配置
├── requirements.txt             # Python 依赖
└── README.md                    # 项目说明
```

---

## 🚀 快速开始

### 前置要求

- Python 3.8+
- Allure Commandline 2.35+（用于生成报告）
  - 下载地址：https://github.com/allure-framework/allure2/releases
  - Windows：解压后配置 `ALLURE_PATH` 环境变量或加入 PATH

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 2️⃣ 配置环境变量（可选）

复制 `.env.example` 为 `.env`，根据实际需求修改配置：

```bash
cp .env.example .env
```

主要配置项说明：

```bash
# API 基础地址
DUMMYJSON_BASE_URL=https://dummyjson.com

# 测试账号（DummyJSON 公开用户）
DUMMYJSON_USERNAME=emilys
DUMMYJSON_PASSWORD=emilyspass

# Allure 配置
ALLURE_RESULTS_DIR=allure-results
ALLURE_PATH=F:\allure-commandline-2.35.1\allure-2.35.1\bin\allure.bat  # Windows 示例

# HTTP 配置
HTTP_TIMEOUT_SECONDS=30              # 请求超时时间（秒）
HTTP_RETRY_ATTEMPTS=2                # 重试次数（含首次）
HTTP_RETRY_BACKOFF_BASE_SECONDS=0.3  # 重试退避基数（秒）
```

### 3️⃣ 运行测试

#### 方式一：使用一键运行脚本（推荐）

```bash
# Python 脚本（跨平台，不依赖 PowerShell 执行策略）
python scripts/run_tests_and_allure.py
```

该脚本会自动：
1. 执行 pytest 测试
2. 生成 Allure 原始结果
3. 启动 Allure 服务并自动打开浏览器

#### 方式二：手动执行

```bash
# 步骤 1：运行测试并生成 Allure 原始结果
pytest -s --alluredir=allure-results

# 步骤 2a：启动本地 Allure 服务（实时查看）
allure serve allure-results

# 步骤 2b：或生成静态 HTML 报告（可发送给他人）
allure generate allure-results -o allure-report --clean
```

#### 方式三：生成静态报告（适合分享）

```bash
# Windows PowerShell
$env:ALLURE_MODE="generate"
python scripts/run_tests_and_allure.py

# Linux/Mac
export ALLURE_MODE="generate"
python scripts/run_tests_and_allure.py
```

生成的静态报告位于 `allure-report/` 目录，可直接用浏览器打开 `index.html`。

### 4️⃣ 运行特定测试

```bash
# 运行冒烟测试
pytest -m smoke -s --alluredir=allure-results

# 运行商品模块测试
pytest -m products -s --alluredir=allure-results

# 运行指定文件
pytest tests/test_products.py -s --alluredir=allure-results

# 运行指定用例
pytest tests/test_products.py::TestProducts::test_list_products_with_params -v
```

---

## 🏗 架构设计

### POM（Page Object Model）架构图

```
┌─────────────────────────────────────────────┐
│           tests/ (测试用例层)                 │
│  - test_products.py / test_users.py ...      │
│  - 使用 pytest markers 分类                  │
│  - 调用 Service 层方法                       │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│        services/ (API Service 层)            │
│  - ProductsService / UsersService ...        │
│  - 封装接口调用逻辑                          │
│  - 参数模型化（Pydantic）                    │
│  - Allure 步骤装饰                           │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│         http/ (HTTP 客户端层)                │
│  - APIClient：统一请求入口                   │
│  - 自动重试（指数退避）                      │
│  - Allure 附件自动附加                       │
│  - cURL 命令生成                             │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│         DummyJSON API (目标接口)             │
│  https://dummyjson.com                       │
└─────────────────────────────────────────────┘
```

### 核心设计原则

#### 1. 单一职责

- **APIClient**：只负责发送 HTTP 请求，不关心业务逻辑
- **Service**：封装业务接口，处理参数组装
- **Tests**：只负责断言验证，不直接调用 HTTP

#### 2. 参数模型化

所有接口参数使用 Pydantic 模型定义：

```python
# Query 参数模型（src/dj_api/http/models.py）
class PaginationQuery(BaseModel):
    limit: Optional[int] = Field(default=None, ge=0)
    skip: Optional[int] = Field(default=None, ge=0)
    
    def to_params(self) -> Dict[str, Any]:
        params = {}
        if self.limit is not None:
            params["limit"] = self.limit
        if self.skip is not None:
            params["skip"] = self.skip
        return params

# Request Body 模型（src/dj_api/http/payloads.py）
class ProductUpsertPayload(FlexibleModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    # ... 其他字段
```

#### 3. 分层调用示例

```python
# 测试层（tests/test_products.py）
@allure.story("商品列表")
def test_list_products(services):
    resp = services["products"].list_products(
        pagination=PaginationQuery(limit=5, skip=0),
        select=SelectQuery(select=["id", "title", "price"]),
        sort=SortQuery(sortBy="title", order="asc")
    )
    assert_status(resp, 200)
    data = resp.json()
    assert_has_keys(data, ["products", "total"])

# Service 层（src/dj_api/services/products.py）
def list_products(
    self,
    *,
    pagination: Optional[PaginationQuery] = None,
    select: Optional[SelectQuery] = None,
    sort: Optional[SortQuery] = None,
) -> requests.Response:
    params = merge_params(
        (pagination or PaginationQuery()).to_params(),
        (select or SelectQuery()).to_params(),
        (sort or SortQuery()).to_params(),
    )
    with step("商品: 获取商品列表（GET /products）"):
        return self.client.request("GET", "/products", params=params)

# HTTP 层（src/dj_api/http/client.py）
def request(self, method: str, path: str, *, params: dict, ...) -> Response:
    # 自动重试、Allure 附件、cURL 生成等
    ...
```

---

## 💡 使用示例

### 示例 1：查询商品列表

```python
import pytest
import allure
from dj_api.http.models import PaginationQuery, SelectQuery, SortQuery
from tests.assertions import assert_status, assert_has_keys

@pytest.mark.products
@allure.feature("商品")
class TestProducts:
    @allure.story("商品列表")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_products(self, services):
        """测试商品列表接口，带分页、字段筛选、排序"""
        resp = services["products"].list_products(
            pagination=PaginationQuery(limit=5, skip=0),
            select=SelectQuery(select=["id", "title", "price"]),
            sort=SortQuery(sortBy="title", order="asc")
        )
        
        # 断言状态码
        assert_status(resp, 200)
        
        # 断言响应数据结构
        data = resp.json()
        assert_has_keys(data, ["products", "total", "skip", "limit"])
        assert isinstance(data["products"], list)
        assert len(data["products"]) <= 5
```

### 示例 2：新增商品

```python
from dj_api.http.payloads import ProductUpsertPayload

@allure.story("新增商品")
def test_add_product(self, services):
    """测试新增商品接口"""
    payload = ProductUpsertPayload(
        title="BMW Pencil",
        description="接口自动化演示数据",
        category="smartphones",
        price=9.99,
        stock=10,
        brand="BMW",
        tags=["demo", "automation"]
    )
    
    resp = services["products"].add_product(payload=payload)
    assert_status(resp, (200, 201))
    
    data = resp.json()
    assert_has_keys(data, ["id", "title"])
    assert data["title"] == "BMW Pencil"
```

### 示例 3：需要认证的接口

```python
@allure.story("用户信息")
def test_get_user_profile(self, services, tokens):
    """测试获取用户信息（需要 Bearer Token）"""
    user_id = tokens["user_id"]
    access_token = tokens["access"]
    
    resp = services["users"].get_user(
        user_id=int(user_id),
        token=access_token
    )
    
    assert_status(resp, 200)
    data = resp.json()
    assert data["username"] == tokens["username"]
```

### 示例 4：自定义重试配置

在 `.env` 文件中调整重试策略：

```bash
# 遇到网络问题时最多重试 3 次
HTTP_RETRY_ATTEMPTS=3

# 退避基数 0.5 秒（第一次等待 ~0.5s，第二次 ~1s，第三次 ~2s）
HTTP_RETRY_BACKOFF_BASE_SECONDS=0.5

# 请求超时 60 秒
HTTP_TIMEOUT_SECONDS=60
```

---

## 📊 报告展示

### Allure 报告亮点

#### 1. 概览仪表板

- ✅ 测试通过率统计
- ✅ 用例执行趋势图
- ✅ 失败分类饼图（HTTP 4xx/5xx、断言失败、用例异常）
- ✅ 环境信息（Python 版本、操作系统、接口地址）

#### 2. 用例详情

每个用例包含：

- **请求信息**：方法、URL、Query 参数、Headers、Body
- **cURL 命令**：可直接复制粘贴复现问题
- **响应信息**：状态码、Headers、Body（JSON 格式化）
- **耗时统计**：单次请求耗时、总耗时
- **断言结果**：期望值 vs 实际值
- **重试记录**：如有重试，显示重试次数、原因、等待时间

#### 3. 中文化套件视图

```
DummyJSON接口自动化 (parentSuite)
├── 商品 (suite)
│   ├── 商品接口用例 (subSuite)
│   │   ├── 商品-商品列表（分页/字段筛选/延迟/排序）
│   │   ├── 商品-获取单个商品（字段筛选）
│   │   └── 商品-搜索商品（关键字）
├── 用户 (suite)
│   ├── 用户接口用例 (subSuite)
│   │   ├── 用户-获取用户列表
│   │   └── 用户-获取单个用户信息
└── ...
```

#### 4. 失败分类

自动将失败用例归类：

- 🔴 HTTP 5xx（服务端错误）
- 🟡 HTTP 4xx（请求/权限/参数错误）
- 🔵 断言失败（业务/字段校验）
- ⚫ 用例异常（脚本/依赖问题）

---

## 🎓 最佳实践

### 1. 测试用例编写规范

✅ **推荐做法**：

```python
@allure.story("功能描述")
@allure.severity(allure.severity_level.CRITICAL)  # 设置优先级
def test_xxx(self, services):
    """清晰的文档字符串"""
    # 1. 准备数据
    payload = XxxPayload(...)
    
    # 2. 调用接口
    resp = services["xxx"].method(payload=payload)
    
    # 3. 断言验证
    assert_status(resp, 200)
    data = resp.json()
    assert_has_keys(data, ["expected_field"])
```

❌ **避免做法**：

```python
# 不要在测试中直接构造 URL
resp = requests.get("https://dummyjson.com/products/1")

# 不要硬编码断言
assert resp.status_code == 200
assert "title" in resp.json()
```

### 2. 标记使用指南

```python
# 冒烟测试（核心功能，每次必跑）
@pytest.mark.smoke

# 回归测试（完整测试集）
@pytest.mark.regression

# 按业务模块标记
@pytest.mark.products
@pytest.mark.users
@pytest.mark.auth

# 组合使用
@pytest.mark.smoke
@pytest.mark.products
```

运行示例：

```bash
# 只跑冒烟测试
pytest -m smoke

# 跑商品模块的回归测试
pytest -m "regression and products"
```

### 3. 参数模型复用

```python
# 在多个测试中复用相同的参数配置
DEFAULT_PAGINATION = PaginationQuery(limit=10, skip=0)
DEFAULT_SELECT = SelectQuery(select=["id", "title"])

def test_case_1(self, services):
    resp = services["products"].list_products(
        pagination=DEFAULT_PAGINATION,
        select=DEFAULT_SELECT
    )
    ...

def test_case_2(self, services):
    resp = services["products"].search_products(
        q="phone",
        pagination=DEFAULT_PAGINATION
    )
    ...
```

### 4. Fixture 共享

```python
# conftest.py 中定义的 fixture 可在所有测试中使用
@pytest.fixture(scope="session")
def tokens(services):
    """获取认证 tokens（会话级别，只登录一次）"""
    auth = services["auth"]
    resp = auth.login_auth(username="...", password="...")
    return resp.json()

# 测试文件中直接使用
def test_authenticated_api(self, services, tokens):
    access_token = tokens["access"]
    ...
```

### 5. 断言最佳实践

```python
# ✅ 使用封装的断言方法（自动附加到 Allure）
assert_status(resp, 200)
assert_has_keys(data, ["id", "title"])

# ❌ 避免原生 assert（报告中信息不完整）
assert resp.status_code == 200
assert "id" in data
```

### 6. 环境隔离

```bash
# 开发环境 .env.dev
DUMMYJSON_BASE_URL=https://dummyjson.com
HTTP_RETRY_ATTEMPTS=2

# 测试环境 .env.test
DUMMYJSON_BASE_URL=https://test-api.example.com
HTTP_RETRY_ATTEMPTS=3
HTTP_TIMEOUT_SECONDS=60

# 使用时指定
cp .env.test .env
pytest -s --alluredir=allure-results
```

---

## 🔧 常见问题

### Q1: 找不到 allure 命令？

**解决方案**：

1. 下载 Allure Commandline：https://github.com/allure-framework/allure2/releases
2. 解压到任意目录（如 `F:\allure-commandline-2.35.1`）
3. 在 `.env` 中配置路径：
   ```bash
   ALLURE_PATH=F:\allure-commandline-2.35.1\allure-2.35.1\bin\allure.bat
   ```
4. 或使用一键运行脚本（自动读取配置）：
   ```bash
   python scripts/run_tests_and_allure.py
   ```

### Q2: 如何跳过某些测试？

```python
# 方法 1：使用 pytest.mark.skip
@pytest.mark.skip(reason="临时跳过")
def test_xxx(self):
    ...

# 方法 2：命令行排除
pytest -k "not test_xxx"
```

### Q3: 如何调试单个测试？

```bash
# 使用 -s 参数保留 print 输出
pytest tests/test_products.py::TestProducts::test_list_products -v -s

# 使用 pdb 断点
import pdb; pdb.set_trace()  # Python 3.6-
breakpoint()  # Python 3.7+
```

### Q4: 如何查看完整的请求/响应日志？

Allure 报告中已自动包含：
- 请求方法、URL、Headers、Body
- 响应状态码、Headers、Body
- cURL 命令（可直接复制执行）

如需控制台输出，添加 `-v` 参数：

```bash
pytest -v -s --alluredir=allure-results
```

### Q5: 如何自定义重试策略？

在 `.env` 中配置：

```bash
# 重试次数（含首次请求）
HTTP_RETRY_ATTEMPTS=3

# 退避基数（秒），实际等待时间 = base * 2^(attempt-1) + random(0, base)
HTTP_RETRY_BACKOFF_BASE_SECONDS=0.5
```

---

## 📝 扩展开发

### 添加新的业务模块

以添加 "订单" 模块为例：

#### 步骤 1：创建 Service

```python
# src/dj_api/services/orders.py
from dj_api.services.base import BaseService
from dj_api.utils.steps import step

class OrdersService(BaseService):
    def list_orders(self, *, pagination=None):
        with step("订单: 获取订单列表"):
            return self.client.request("GET", "/orders", params=pagination)
    
    def get_order(self, *, order_id: int):
        with step(f"订单: 获取订单详情（{order_id}）"):
            return self.client.request("GET", f"/orders/{order_id}")
```

#### 步骤 2：注册 Service

```python
# src/dj_api/services/__init__.py
from dj_api.services.orders import OrdersService

__all__ = [
    # ... 其他 service
    "OrdersService",
]
```

#### 步骤 3：添加 pytest marker

```ini
# pytest.ini
[pytest]
markers =
  # ... 其他 marker
  orders: 订单相关
```

#### 步骤 4：创建测试文件

```python
# tests/test_orders.py
import pytest
import allure
from tests.assertions import assert_status

@pytest.mark.orders
@allure.feature("订单")
class TestOrders:
    @allure.story("订单列表")
    def test_list_orders(self, services):
        resp = services["orders"].list_orders()
        assert_status(resp, 200)
```

#### 步骤 5：在 conftest.py 中注册

```python
# tests/conftest.py
from dj_api.services import OrdersService

@pytest.fixture(scope="session")
def services(api_client):
    return {
        # ... 其他 service
        "orders": OrdersService(api_client),
    }
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交 PR 前请检查：

- [ ] 代码符合 PEP 8 规范
- [ ] 添加了必要的单元测试
- [ ] 更新了相关文档
- [ ] 所有测试用例通过

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [DummyJSON](https://dummyjson.com) - 提供免费测试 API
- [Pytest](https://docs.pytest.org/) - 强大的 Python 测试框架
- [Allure Report](https://allurereport.org/) - 美观的测试报告工具
- [Pydantic](https://docs.pydantic.dev/) - 数据验证库

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**

Made with ❤️ by Python Automation Team

</div>

