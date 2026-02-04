# 图片标签词库 Web 管理后台

一个基于 Flask 的图片标签词库管理后台，用于管理 SQLite3 数据库中的标签词汇。

## 功能特性

- 标签的增删改查
- 标签分类管理
- 标签翻译管理
- 标签可用性状态管理
- 数据统计与筛选

## 安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd curator-tag-vocab
```

### 2. 安装依赖

使用可编辑模式安装（推荐开发使用）：

```bash
pip install -e .
```

或者使用 requirements.txt：

```bash
pip install -r requirements.txt
```

## 运行

```bash
python src/app_tagging.py
```

默认访问地址：`http://localhost:80/tagging/vocab`

您也可以通过环境变量指定端口：

```bash
PORT=5000 python src/app_tagging.py
```

## 项目结构

```
curator-tag-vocab/
├── src/
│   ├── __init__.py
│   ├── app_tagging.py      # Flask 应用入口
│   ├── db.py               # 数据库操作封装
│   ├── routers/            # 路由模块
│   │   ├── __init__.py
│   │   └── tag_manager.py  # 标签管理路由
│   └── templates/          # HTML 模板
│       └── tag_manager.html
├── vocab.db                # SQLite 数据库文件
├── pyproject.toml          # 项目配置文件
├── requirements.txt        # 依赖列表
└── README.md
```

## API 接口

- `GET /tagging/vocab/` - 管理界面
- `GET /tagging/vocab/api/tags` - 获取标签列表
- `POST /tagging/vocab/api/tags` - 创建标签
- `PUT /tagging/vocab/api/tags/<id>` - 更新标签
- `DELETE /tagging/vocab/api/tags/<id>` - 删除标签
- `GET /tagging/vocab/api/stats` - 获取统计信息
- `GET /tagging/vocab/api/categories` - 获取分类列表
- `GET /tagging/vocab/api/export/protobuf` - 导出 Protobuf 格式
- `GET /tagging/vocab/api/export/csv` - 导出 CSV 格式

## 开发

项目以可编辑模式安装后，修改代码会立即生效，无需重新安装。

## 技术栈

- **Web 框架**: Flask 2.3+
- **数据库**: SQLite3
- **Python**: 3.8+
