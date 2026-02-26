# 导出按钮背景色调整 — 技术方案

> GitHub Issue: #48
> PRD: docs/prds/issue-48.md
> 创建日期: 2025-01-21
> 状态: Draft

## 1. 概述

将导出按钮（Export Protobuf 和 Export CSV）的样式从 `btn-info` 调整为 `btn-secondary`，使用更浅的灰色背景，降低视觉权重，与主操作按钮形成清晰的视觉层次。

## 2. 方案设计

### 2.1 整体思路

这是一个纯前端样式调整，只需修改 HTML 模板中按钮的 CSS 类名。将两个导出按钮从 `btn-info` 改为 `btn-secondary`，利用已定义的灰色系样式。

### 2.2 详细设计

**当前状态：**
- Export Protobuf 按钮：`class="btn btn-info"`
- Export CSV 按钮：`class="btn btn-info"`
- `btn-info` 样式：背景 #e3f2ff（浅蓝），文字 #007aff（蓝色）

**目标状态：**
- Export Protobuf 按钮：`class="btn btn-secondary"`
- Export CSV 按钮：`class="btn btn-secondary"`
- `btn-secondary` 样式：背景 #f5f5f5（浅灰），文字 #6e6e73（灰色）

**CSS 样式对比：**

| 样式类 | 背景色 | 文字色 | 边框色 |
|--------|--------|--------|--------|
| btn-info | #e3f2ff（浅蓝） | #007aff（蓝） | #b8dcff |
| btn-secondary | #f5f5f5（浅灰） | #6e6e73（灰） | #e0e0e0 |

**Hover 状态：**
- `btn-secondary:hover`：背景 #e8e8e8，边框 #d0d0d0

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| src/templates/tags.html | 修改 | 第 63-64 行，将两个导出按钮的 `btn-info` 改为 `btn-secondary` |
| src/static/css/main.css | 无变更 | `btn-secondary` 样式已存在，无需修改 |

## 4. 实现步骤

1. 修改 `src/templates/tags.html`，将 Export Protobuf 按钮的类名从 `btn btn-info` 改为 `btn btn-secondary`
2. 修改 `src/templates/tags.html`，将 Export CSV 按钮的类名从 `btn btn-info` 改为 `btn btn-secondary`
3. 本地启动应用，验证按钮样式正确显示
4. 验证按钮 hover 状态正常

## 5. 测试策略

- **视觉测试**: 手动验证按钮显示为灰色背景、灰色文字
- **交互测试**: 验证 hover 时背景色变为 #e8e8e8
- **回归测试**: 确认其他按钮（Load Tags、Add Tag）样式不受影响

## 6. 风险与待决事项

- **无风险**：此变更仅修改 CSS 类名，使用已存在的样式，无功能影响
- **无依赖**：不涉及后端或 JavaScript 变更
