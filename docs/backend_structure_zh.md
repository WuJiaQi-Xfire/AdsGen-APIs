# AdsGem 后端结构

本文档概述了 AdsGem 后端项目的结构和组织，提供了每个组件及其用途的概览。

## 项目结构

```
backend/
├── alembic/                  # 数据库迁移工具
│   ├── env.py                # Alembic 环境配置
│   └── script.py.mako        # 迁移脚本模板
├── container/                # Docker 配置
│   ├── docker-compose.yml    # Docker Compose 配置
│   └── Dockerfile            # Docker 镜像定义
├── ngrok/                    # Ngrok 隧道配置
│   ├── ngrok_config.json     # Ngrok 配置
│   └── ngrok_daemon.py       # Ngrok 守护进程
├── requirements.txt          # Python 依赖
└── src/                      # 源代码
    ├── api/                  # API 路由和依赖
    │   ├── deps.py           # API 依赖
    │   └── v1/               # API 版本 1
    │       └── endpoints/    # API 端点
    │           ├── auth.py   # 认证端点
    │           ├── default.py # 默认端点
    │           ├── generate.py # 生成端点
    │           ├── templates.py # 模板端点
    │           ├── test.py   # 测试端点
    │           └── users.py  # 用户管理端点
    ├── celery/               # Celery 任务队列
    │   ├── tasks.py          # 任务定义
    │   └── worker.py         # Celery worker 配置
    ├── core/                 # 核心功能
    │   ├── celery_utils.py   # Celery 工具
    │   ├── config.py         # 应用配置
    │   ├── dependencies.py   # 核心依赖
    │   ├── init_db.py        # 数据库初始化
    │   └── security.py       # 安全工具
    ├── crud/                 # CRUD 操作
    │   ├── base.py           # 基础 CRUD 类
    │   ├── item.py           # 项目 CRUD 操作
    │   └── user.py           # 用户 CRUD 操作
    ├── db/                   # 数据库配置
    │   ├── base.py           # 基础数据库模型
    │   └── session.py        # 数据库会话配置
    ├── main.py               # 应用入口点
    ├── models/               # 数据库模型
    │   ├── generation.py     # 生成模型
    │   ├── lora.py           # LoRA 模型
    │   ├── template.py       # 模板模型
    │   └── user.py           # 用户模型
    ├── schemas/              # Pydantic 模式
    │   ├── generation.py     # 生成模式
    │   ├── template.py       # 模板模式
    │   └── user.py           # 用户模式
    ├── services/             # 外部服务
    │   ├── image_service.py  # 图像处理服务
    │   └── llm_service.py    # 语言模型服务
    ├── tests/                # 测试
    │   ├── test_db.py        # 数据库测试
    │   └── test_user.py      # 用户测试
    └── utils/                # 工具
        ├── file_utils.py     # 文件工具
        ├── ngrok_client.py   # Ngrok 客户端
        └── ngrok_manager.py  # Ngrok 管理器
```

## 关键组件

### API 层 (`src/api/`)

API 层处理 HTTP 请求和响应，定义客户端可以交互的端点。

- **deps.py**: 定义 API 依赖和通用 CRUD 路由，用于创建标准 CRUD 端点。
- **v1/endpoints/**: 包含不同资源的 API 端点定义。

### 数据库层 (`src/db/`, `src/models/`, `src/crud/`)

数据库层管理数据持久化和检索。

- **db/**: 包含数据库配置和会话管理。
- **models/**: 定义代表数据库表的 SQLAlchemy ORM 模型。
- **crud/**: 实现每个模型的 CRUD（创建、读取、更新、删除）操作。

### 模式层 (`src/schemas/`)

模式层定义用于请求验证和响应序列化的 Pydantic 模型。

- 每个模式文件对应一个特定资源（例如，用户、模板、生成）。
- 模式定义 API 请求和响应的数据结构。

### 核心层 (`src/core/`)

核心层包含应用程序的基本功能和配置。

- **config.py**: 应用程序配置设置。
- **security.py**: 与安全相关的工具（认证、密码哈希）。
- **init_db.py**: 数据库初始化逻辑。

### 服务层 (`src/services/`)

服务层与外部服务集成并实现业务逻辑。

- **image_service.py**: 处理图像处理操作。
- **llm_service.py**: 与语言模型集成，用于文本生成。

### 工具层 (`src/utils/`)

工具层提供辅助函数和工具。

- **file_utils.py**: 文件处理工具。
- **ngrok_client.py**: 与 Ngrok 隧道服务交互的客户端。
- **ngrok_manager.py**: Ngrok 隧道管理。

### 任务队列 (`src/celery/`)

任务队列处理异步和后台处理。

- **tasks.py**: 定义 Celery 任务。
- **worker.py**: 配置 Celery worker。

### 测试 (`src/tests/`)

测试目录包含应用程序的测试用例。

- **test_db.py**: 数据库操作测试。
- **test_user.py**: 用户相关功能测试。

## 应用流程

1. 应用程序从 `main.py` 开始，初始化 FastAPI 应用程序。
2. API 路由在 `api/v1/endpoints/` 目录中定义。
3. 请求使用 `schemas/` 目录中的 Pydantic 模式进行验证。
4. 业务逻辑在 CRUD 操作和服务中实现。
5. 数据使用 SQLAlchemy ORM 模型持久化。
6. 后台任务由 Celery 处理。

## 主要特性

- **用户管理**: 注册、认证和用户资料管理。
- **模板管理**: 创建和管理模板。
- **内容生成**: 使用语言模型生成内容。
- **Ngrok 集成**: 将本地服务暴露到公共互联网，用于测试和开发。
- **异步数据库操作**: 使用 SQLAlchemy 的异步功能进行高效的数据库访问。
- **后台处理**: 使用 Celery 处理长时间运行的任务。

## 开发设置

应用程序可以使用 Python 本地运行，也可以使用 Docker 运行。它连接到 PostgreSQL 数据库，并且可以使用 Ngrok 将服务暴露到互联网，用于测试和开发目的。
