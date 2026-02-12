# 导出按钮背景色修改 — 技术方案

> GitHub Issue: #33
> 创建日期: 2026-02-12
> 状态: Draft

## 1. 问题描述

标签管理界面中「Export Protobuf」和「Export CSV」两个导出按钮当前使用蓝色主题（`.btn-info` 样式），需要修改为红色主题以提升视觉辨识度。

## 2. 根因分析

当前代码中，两个导出按钮使用 `.btn-info` 类：

**关键代码位置**:
- `src/templates/tags.html:63` — Export Protobuf 按钮使用 `btn-info`
- `src/templates/tags.html:64` — Export CSV 按钮使用 `btn-info`

CSS 中已定义 `.btn-danger` 类（红色主题），但按钮未使用该样式类：
- `.btn-danger` 定义于 `src/static/css/main.css:127-136`
- 背景色：`#ffebe9`（浅红色/粉色）
- 文字颜色：`#ff3b30`（红色）
- 边框：`#ffd8d5`（红色系）

## 3. 修复方案

将两个导出按钮的 CSS 类从 `btn-info` 修改为 `btn-danger`。

**具体变更**:

```html
<!-- 修改前 -->
<button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-info" id="export-csv-btn">Export CSV</button>

<!-- 修改后 -->
<button class="btn btn-danger" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-danger" id="export-csv-btn">Export CSV</button>
```

## 4. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/templates/tags.html` | 修改 | 将两个导出按钮的 `btn-info` 类改为 `btn-danger` |
| `src/static/css/main.css` | 无变更 | `.btn-danger` 样式已存在，无需修改 |

## 5. 测试策略

- **视觉验证**: 确认两个导出按钮显示为红色背景样式
- **回归测试**: 确认其他按钮（Load Tags、Add Tag）的样式保持不变
- **交互验证**: 确认按钮悬停状态保持红色系配色变化

## 6. 风险与待决事项

- 无已知风险。`.btn-danger` 样式已在 CSS 中定义并可用。
