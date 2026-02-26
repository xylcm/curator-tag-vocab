# 图片标签词库 Web 管理后台

一个基于 Flask 的图片标签词库管理后台，用于管理 SQLite3 数据库中的标签词汇。

## 功能特性

- 标签的增删改查
- 标签分类管理
- 标签翻译管理
- 标签可用性状态管理
- 数据统计与筛选
- Protobuf/CSV 数据导出

## 安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd curator-tag-vocab
```

### 2. 安装依赖

使用可编辑模式安装（推荐开发使用）：

```bash
pip install -e ".[dev]"
```

或者使用最小依赖：

```bash
pip install -e .
```

## 运行

```bash
python -m curator_tag_vocab.app
```

或使用入口脚本：

```bash
curator-tag-vocab
```

默认访问地址：`http://localhost:80/tagging/vocab`

您也可以通过环境变量指定端口：

```bash
PORT=5000 python -m curator_tag_vocab.app
```

## 项目结构

```
curator-tag-vocab/
├── curator_tag_vocab/      # 主应用包
│   ├── __init__.py
│   ├── app.py              # Flask 应用工厂
│   ├── config.py           # 配置管理
│   ├── models/             # 数据模型层
│   │   ├── __init__.py
│   │   ├── tag.py          # 标签模型
│   │   └── category.py     # 分类模型
│   ├── repositories/       # 数据访问层 (Repository Pattern)
│   │   ├── __init__.py
│   │   ├── database.py     # 数据库连接管理
│   │   └── tag_repository.py  # 标签数据访问
│   ├── services/           # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── tag_service.py      # 标签业务逻辑
│   │   ├── category_service.py # 分类业务逻辑
│   │   └── export_service.py   # 导出业务逻辑
│   ├── api/                # API 路由层
│   │   ├── __init__.py
│   │   └── routes.py       # API 端点定义
│   ├── utils/              # 工具函数
│   │   ├── __init__.py
│   │   ├── error_handlers.py   # 错误处理
│   │   └── logging_config.py   # 日志配置
│   ├── templates/          # HTML 模板
│   ├── static/             # 静态资源
│   └── protobuf/           # Protobuf 定义
├── tests/                  # 测试套件
│   ├── unit/               # 单元测试
│   └── integration/        # 集成测试
├── config/                 # 配置文件
│   └── categories.json     # 分类配置
├── vocab.db                # SQLite 数据库文件
├── pyproject.toml          # 项目配置
└── README.md
```

## 架构设计

本项目采用分层架构设计，遵循单一职责原则和依赖倒置原则：

### 1. 模型层 (Models)
定义数据结构和业务实体：
- `Tag`: 标签实体，包含属性验证和序列化
- `Category`: 分类实体
- `TagCreate`/`TagUpdate`/`TagFilter`: DTO 对象

### 2. 数据访问层 (Repositories)
封装数据库操作，提供数据持久化抽象：
- `DatabaseConnection`: 数据库连接管理
- `TagRepository`: 标签 CRUD 操作

### 3. 业务逻辑层 (Services)
实现核心业务逻辑，处理业务规则和流程：
- `TagService`: 标签管理服务
- `CategoryService`: 分类配置服务
- `ExportService`: 数据导出服务

### 4. API 层 (API/Routes)
处理 HTTP 请求和响应：
- 输入验证
- 调用业务服务
- 格式化输出

### 5. 工具层 (Utils)
横切关注点：
- 错误处理
- 日志配置

## API 接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/tagging/vocab/` | 管理界面 |
| GET | `/tagging/vocab/api/tags` | 获取标签列表（支持分页、筛选、排序） |
| POST | `/tagging/vocab/api/tags` | 创建标签 |
| PUT | `/tagging/vocab/api/tags/<id>` | 更新标签 |
| DELETE | `/tagging/vocab/api/tags/<id>` | 删除标签（软删除） |
| GET | `/tagging/vocab/api/stats` | 获取统计信息 |
| GET | `/tagging/vocab/api/categories` | 获取分类列表 |
| GET | `/tagging/vocab/api/categories/config` | 获取完整分类配置 |
| GET | `/tagging/vocab/api/export/protobuf` | 导出 Protobuf 格式 |
| GET | `/tagging/vocab/api/export/csv` | 导出 CSV 格式 |

### 查询参数示例

```bash
# 分页和排序
GET /tagging/vocab/api/tags?page=1&limit=50&sort=tag&order=asc

# 筛选
GET /tagging/vocab/api/tags?available=available&category=People&search=test

# 统计
GET /tagging/vocab/api/stats?deleted=active
```

## 测试

运行测试套件：

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 带覆盖率报告
pytest --cov=curator_tag_vocab
```

## 配置

配置通过环境变量或 `config.py` 管理：

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `FLASK_ENV` | `development` | 运行环境 |
| `SECRET_KEY` | `dev-secret-key...` | Flask 密钥 |
| `DATABASE_PATH` | `vocab.db` | 数据库路径 |
| `PORT` | `80` | 服务端口 |
| `HOST` | `0.0.0.0` | 绑定地址 |

## 开发

项目以可编辑模式安装后，修改代码会立即生效，无需重新安装。

### 添加新功能

1. **模型层**: 在 `models/` 定义数据结构
2. **数据层**: 在 `repositories/` 实现数据访问
3. **业务层**: 在 `services/` 实现业务逻辑
4. **API 层**: 在 `api/routes.py` 添加端点
5. **测试**: 在 `tests/` 编写测试用例

## 技术栈

- **Web 框架**: Flask 2.3+
- **数据库**: SQLite3
- **架构模式**: Repository Pattern, Service Layer
- **测试框架**: pytest
- **Python**: 3.8+

## 重构说明

本次重构主要改进：

1. **分层架构**: 从单层结构改为清晰的分层架构
2. **依赖注入**: 通过构造函数注入依赖，便于测试
3. **错误处理**: 统一的错误处理和日志记录
4. **配置管理**: 环境驱动的配置管理
5. **测试覆盖**: 完整的单元测试和集成测试
6. **类型提示**: 添加类型注解提高代码可维护性
