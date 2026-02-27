# 导出按钮背景色修改 — 技术方案

> GitHub Issue: #65
> PRD: docs/prds/issue-65.md
> 创建日期: 2025-01-21
> 状态: Draft

## 1. 概述

将导出按钮（Export Protobuf 和 Export CSV）的背景色从当前使用 `btn-info` 类的青色/蓝绿色修改为浅蓝色，以提升视觉一致性和用户体验。

## 2. 方案设计

### 2.1 整体思路

当前导出按钮使用 `btn-info` 类（第 63-64 行），其样式定义在 `main.css` 第 149-158 行。根据 PRD 要求，需要将背景色改为浅蓝色。

分析现有代码：
- `.btn-info` 当前颜色：`background: #e3f2ff; color: #007aff;` - 这已经是浅蓝色调
- 问题可能在于实际渲染效果或设计期望的浅蓝色与当前有差异

方案：创建一个新的 `.btn-export` 类，使用更明显的浅蓝色背景，确保满足设计要求。

### 2.2 详细设计

#### CSS 变更

在 `src/static/css/main.css` 中添加新的按钮样式类：

```css
.btn-export {
    background: #cce5ff;  /* 更明显的浅蓝色 */
    color: #004085;       /* 深蓝色文字，确保对比度 */
    border: 1px solid #b3d7ff;
}

.btn-export:hover {
    background: #b3d7ff;
    border-color: #99caff;
}
```

#### HTML 变更

在 `src/templates/tags.html` 中修改导出按钮的类：

```html
<!-- 修改前 -->
<button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-info" id="export-csv-btn">Export CSV</button>

<!-- 修改后 -->
<button class="btn btn-export" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-export" id="export-csv-btn">Export CSV</button>
```

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/static/css/main.css` | 新增 | 添加 `.btn-export` 和 `.btn-export:hover` 样式 |
| `src/templates/tags.html` | 修改 | 将导出按钮的类从 `btn-info` 改为 `btn-export` |

## 4. 实现步骤

1. **添加 CSS 样式**：在 `main.css` 中 `.btn-info` 样式之后添加 `.btn-export` 类定义
2. **修改 HTML**：在 `tags.html` 中将两个导出按钮的 `btn-info` 类替换为 `btn-export`
3. **验证**：启动应用，检查导出按钮显示为浅蓝色，悬停效果正常

## 5. 测试策略

- **视觉测试**：手动验证两个导出按钮显示为浅蓝色背景
- **对比度测试**：确保文字与背景对比度符合可读性标准（WCAG 4.5:1）
- **交互测试**：验证悬停状态视觉反馈正常
- **回归测试**：确保其他按钮样式不受影响

## 6. 风险与待决事项

- **颜色精确度**：浅蓝色的具体色值（#cce5ff）可能需要根据实际视觉效果微调
- **设计一致性**：如果项目中其他页面也使用导出按钮，需要确认是否需要同步修改
