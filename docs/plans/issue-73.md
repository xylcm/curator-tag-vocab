# 导出按钮背景色调整 — 技术方案

> GitHub Issue: #73
> PRD: docs/prds/issue-73.md
> 创建日期: 2026-02-28
> 状态: Draft

## 1. 概述

根据 PRD 要求，将导出按钮（"Export Protobuf" 和 "Export CSV"）的背景色从当前的 `#e3f2ff` 调整为更浅的蓝色 `#e8f4ff`，hover 状态从 `#d0e8ff` 调整为 `#d6ecff`，使按钮在控制栏中更加柔和且易于识别。

## 2. 方案设计

### 2.1 整体思路

导出按钮当前使用 `btn-info` CSS 类（见 `src/templates/tags.html` 第 63-64 行），样式定义位于 `src/static/css/main.css` 第 149-158 行。

需要修改 `.btn-info` 和 `.btn-info:hover` 的背景色值，保持文字颜色 `#007aff` 和边框颜色 `#b8dcff` 不变。

### 2.2 详细设计

**CSS 变更**（`src/static/css/main.css`）:

```css
/* 当前样式 */
.btn-info {
    background: #e3f2ff;        /* 需要改为 #e8f4ff */
    color: #007aff;
    border: 1px solid #b8dcff;
}

.btn-info:hover {
    background: #d0e8ff;        /* 需要改为 #d6ecff */
    border-color: #9fceff;
}
```

**修改后样式**:

```css
.btn-info {
    background: #e8f4ff;
    color: #007aff;
    border: 1px solid #b8dcff;
}

.btn-info:hover {
    background: #d6ecff;
    border-color: #9fceff;
}
```

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/static/css/main.css` | 修改 | 更新 `.btn-info` 和 `.btn-info:hover` 的背景色值 |
| `src/templates/tags.html` | 无变更 | 按钮 HTML 结构保持不变，继续使用 `btn-info` 类 |

**影响范围说明**:
- 当前代码库中只有导出按钮（Export Protobuf、Export CSV）使用 `btn-info` 类
- 修改仅涉及颜色值变更，不影响布局、交互逻辑或功能
- 无其他组件或页面依赖此样式

## 4. 实现步骤

1. **修改 CSS 文件**
   - 打开 `src/static/css/main.css`
   - 将 `.btn-info` 的 `background` 从 `#e3f2ff` 改为 `#e8f4ff`
   - 将 `.btn-info:hover` 的 `background` 从 `#d0e8ff` 改为 `#d6ecff`

2. **本地验证**
   - 启动 Flask 应用
   - 访问页面确认导出按钮显示新的背景色
   - 验证 hover 状态颜色正确

## 5. 测试策略

- **视觉验证**: 手动检查浏览器中导出按钮的背景色是否为 `#e8f4ff`
- **交互验证**: 鼠标悬停在按钮上，确认 hover 状态背景色为 `#d6ecff`
- **回归验证**: 确认按钮文字颜色仍为 `#007aff`，边框颜色仍为 `#b8dcff`

## 6. 风险与待决事项

- **风险**: 极低。纯 CSS 颜色值变更，无功能影响。
- **待决事项**: 无。需求明确，实现路径清晰。
