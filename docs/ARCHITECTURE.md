# 项目架构文档

## 概述

本项目采用分层架构设计，遵循关注点分离原则，将代码组织为清晰的层次结构。

## 架构分层

```
┌─────────────────────────────────────────────────────────────┐
│                      路由层 (Routers)                        │
│                  处理 HTTP 请求/响应                          │
├─────────────────────────────────────────────────────────────┤
│                      服务层 (Services)                       │
│                  业务逻辑处理                                 │
├─────────────────────────────────────────────────────────────┤
│                      数据访问层 (DAO)                        │
│                  数据库操作封装                               │
├─────────────────────────────────────────────────────────────┤
│                      模型层 (Models)                         │
│                  实体定义和数据结构                            │
└─────────────────────────────────────────────────────────────┘
```

## 目录结构

```
src/
├── __init__.py
├── app_tagging.py          # 应用入口
├── models/                 # 模型层
│   ├── __init__.py
│   ├── tag.py             # 标签实体
│   └── category.py        # 分类实体
├── dao/                    # 数据访问层
│   ├── __init__.py
│   ├── base.py            # 数据库连接管理
│   └── tag_dao.py         # 标签数据访问
├── services/               # 服务层
│   ├── __init__.py
│   ├── tag_service.py     # 标签业务逻辑
│   ├── category_service.py # 分类业务逻辑
│   └── export_service.py  # 导出业务逻辑
├── routers/                # 路由层
│   ├── __init__.py
│   └── tag_manager.py     # 标签管理路由
├── templates/              # HTML 模板
├── static/                 # 静态资源
└── protobuf/              # Protobuf 定义

tests/                      # 测试目录
├── conftest.py            # 测试配置
├── test_models.py         # 模型层测试
├── test_dao.py            # DAO层测试
├── test_services.py       # 服务层测试
└── test_api.py            # API集成测试
```

## 各层职责

### 1. 模型层 (Models)

**文件**: `src/models/`

**职责**:
- 定义实体数据结构
- 数据验证和转换
- 序列化/反序列化

**主要类**:
- `Tag`: 标签实体，包含所有标签属性
- `TagTranslations`: 翻译数据结构
- `Category`: 分类实体

**示例**:
```python
from src.models import Tag, TagTranslations

tag = Tag(
    tag="example",
    translations=TagTranslations(zh_CN="示例"),
    available=True
)
tag_dict = tag.to_dict()  # 转换为API响应格式
```

### 2. 数据访问层 (DAO)

**文件**: `src/dao/`

**职责**:
- 数据库连接管理
- SQL 查询执行
- 结果集映射到模型

**主要类**:
- `DatabaseConnection`: 数据库连接上下文管理器
- `TagDAO`: 标签数据访问对象

**示例**:
```python
from src.dao import DatabaseConnection, TagDAO

db = DatabaseConnection()
tag_dao = TagDAO(db)
tag = tag_dao.get_by_id(1)
tags, total = tag_dao.list_tags(page=1, limit=10)
```

### 3. 服务层 (Services)

**文件**: `src/services/`

**职责**:
- 业务逻辑实现
- 事务协调
- 跨实体操作

**主要类**:
- `TagService`: 标签业务服务
- `CategoryService`: 分类业务服务
- `ExportService`: 导出业务服务

**示例**:
```python
from src.services import TagService
from src.dao import TagDAO

tag_service = TagService(tag_dao)
tag_id = tag_service.create_tag(tag="new", available=True)
stats = tag_service.get_stats()
```

### 4. 路由层 (Routers)

**文件**: `src/routers/`

**职责**:
- HTTP 请求处理
- 参数解析和验证
- 响应格式化
- 错误处理

**示例**:
```python
@bp.route('/api/tags', methods=['POST'])
def create_tag():
    tag_service, _, _ = _get_services()
    data = request.json
    tag_id = tag_service.create_tag(**data)
    return jsonify({'success': True, 'id': tag_id})
```

## 数据流

```
HTTP Request
    ↓
Router (参数解析)
    ↓
Service (业务逻辑)
    ↓
DAO (数据访问)
    ↓
Database
    ↓
DAO (结果映射)
    ↓
Model (数据封装)
    ↓
Service (业务处理)
    ↓
Router (响应格式化)
    ↓
HTTP Response
```

## 依赖关系

```
routers → services → dao → models
            ↓           ↓
      category_service  database
            ↓
      config files
```

## 设计原则

1. **单一职责**: 每个类/模块只负责一个功能领域
2. **依赖倒置**: 高层模块不依赖低层模块，都依赖抽象
3. **关注点分离**: 数据访问、业务逻辑、请求处理分离
4. **可测试性**: 各层可独立测试，支持 Mock

## 测试策略

- **单元测试**: 模型层、DAO层、服务层独立测试
- **集成测试**: API 端点完整测试
- **覆盖率**: 核心逻辑全覆盖

## 扩展指南

### 添加新实体

1. 在 `src/models/` 创建实体类
2. 在 `src/dao/` 创建对应的 DAO 类
3. 在 `src/services/` 创建对应的服务类
4. 在 `src/routers/` 添加路由（如需要）

### 添加新功能

1. 在对应的服务类中添加业务方法
2. 在 DAO 中添加数据访问方法（如需要）
3. 在路由中添加 API 端点（如需要）
4. 编写对应的测试
