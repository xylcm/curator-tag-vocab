# 导出按钮背景色调整 — 技术方案

> GitHub Issue: #67
> PRD: docs/prds/issue-67.md
> 创建日期: 2026-02-27
> 状态: Draft

## 1. 概述

将导出按钮（Export Protobuf 和 Export CSV）的背景色从当前的浅蓝色（`#e3f2ff`）调整为浅白色（`#f5f5f5`），使界面视觉风格与分页按钮等其他辅助操作按钮保持一致。

## 2. 方案设计

### 2.1 整体思路

修改 CSS 中 `.btn-info` 类的样式定义，将其背景色从浅蓝色改为浅白色，同时保持文字颜色（`#007aff`）和悬停效果不变。这是一个纯样式变更，不涉及 JavaScript 或 HTML 结构修改。

### 2.2 详细设计

当前 `.btn-info` 样式定义（`src/static/css/main.css` 第 149-158 行）：

```css
.btn-info {
    background: #e3f2ff;
    color: #007aff;
    border: 1px solid #b8dcff;
}

.btn-info:hover {
    background: #d0e8ff;
    border-color: #9fceff;
}
```

目标样式（与 `.btn-secondary` 保持一致）：

```css
.btn-info {
    background: #f5f5f5;
    color: #007aff;
    border: 1px solid #e0e0e0;
}

.btn-info:hover {
    background: #e8e8e8;
    border-color: #d0d0d0;
}
```

变更点：
- 背景色：`#e3f2ff` → `#f5f5f5`
- 边框色：`#b8dcff` → `#e0e0e0`
- 悬停背景：`#d0e8ff` → `#e8e8e8`
- 悬停边框：`#9fceff` → `#d0d0d0`
- 文字颜色：保持 `#007aff` 不变

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/static/css/main.css` | 修改 | 更新 `.btn-info` 和 `.btn-info:hover` 的样式定义 |

**注意**：`.btn-info` 类目前仅用于导出按钮（Export Protobuf 和 Export CSV），变更后这两个按钮的视觉风格将与分页按钮（`.btn-secondary`）保持一致。

## 4. 实现步骤

1. 修改 `src/static/css/main.css` 中的 `.btn-info` 样式定义
   - 将 `background` 从 `#e3f2ff` 改为 `#f5f5f5`
   - 将 `border-color` 从 `#b8dcff` 改为 `#e0e0e0`
   - 将 `.btn-info:hover` 的 `background` 从 `#d0e8ff` 改为 `#e8e8e8`
   - 将 `.btn-info:hover` 的 `border-color` 从 `#9fceff` 改为 `#d0d0d0`

2. 本地验证
   - 启动 Flask 应用
   - 访问页面确认导出按钮显示为浅白色背景
   - 验证悬停效果正常工作

## 5. 测试策略

- **视觉验证**: 手动检查 Export Protobuf 和 Export CSV 按钮的背景色是否为 `#f5f5f5`
- **交互验证**: 验证按钮悬停时背景色变为 `#e8e8e8`
- **一致性验证**: 确认导出按钮与分页按钮的视觉风格一致

## 6. 风险与待决事项

无已知风险。此变更为纯 CSS 样式调整，不影响功能逻辑。
