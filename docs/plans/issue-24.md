# 技术方案：导出按钮背景颜色修改为白色

> GitHub Issue: #24
> 关联 PRD: docs/prds/issue-24.md
> 创建日期: 2026-02-11
> 状态: Draft

## 1. 需求概述

将标签管理页面中两个导出按钮（"Export Protobuf" 和 "Export CSV"）的背景颜色从蓝色（`.btn-info` 样式）修改为白色，同时保持蓝色文字和边框，使界面视觉更加协调。

## 2. 技术现状分析

### 2.1 当前实现

- **文件位置**: `src/templates/tags.html` 第 63-64 行
- **当前样式类**: `btn btn-info`
- **当前 CSS 定义**: `src/static/css/main.css` 第 149-158 行

```css
.btn-info {
    background: #e3f2ff;  /* 浅蓝色背景 */
    color: #007aff;
    border: 1px solid #b8dcff;
}

.btn-info:hover {
    background: #d0e8ff;
    border-color: #9fceff;
}
```

### 2.2 目标样式

根据 PRD 要求，新的按钮样式应为：

- **默认状态**：
  - 背景色：`#FFFFFF`（白色）
  - 文字颜色：`#007AFF`（蓝色）
  - 边框：`1px solid #007AFF`（蓝色边框）
- **悬停状态**：
  - 背景色：`#E3F2FF`（浅蓝色）
  - 文字颜色：`#007AFF`（蓝色）

## 3. 技术方案

### 方案选择

有两个可选方案：

| 方案 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| A | 修改 `.btn-info` 样式 | 简单直接，无需修改 HTML | 影响所有使用 `.btn-info` 的按钮 |
| B | 创建新的样式类 `.btn-export` | 不影响其他按钮，更灵活 | 需要修改 HTML 中的 class 属性 |

**决策**: 选择方案 B（创建新样式类 `.btn-export`）

理由：
1. `.btn-info` 是一个通用样式类，未来可能在其他地方使用
2. 创建专用样式类更符合单一职责原则
3. 便于后续维护和扩展

### 3.1 具体实现步骤

#### 步骤 1: 修改 HTML 模板

**文件**: `src/templates/tags.html`

将第 63-64 行的：
```html
<button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-info" id="export-csv-btn">Export CSV</button>
```

修改为：
```html
<button class="btn btn-export" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-export" id="export-csv-btn">Export CSV</button>
```

#### 步骤 2: 添加 CSS 样式

**文件**: `src/static/css/main.css`

在 `.btn-info` 样式之后（第 158 行之后）添加新的样式类：

```css
.btn-export {
    background: #ffffff;
    color: #007aff;
    border: 1px solid #007aff;
}

.btn-export:hover {
    background: #e3f2ff;
    border-color: #007aff;
}
```

## 4. 测试计划

### 4.1 视觉验证清单

- [ ] "Export Protobuf" 按钮默认状态显示白色背景
- [ ] "Export CSV" 按钮默认状态显示白色背景
- [ ] 两个导出按钮的文字颜色保持蓝色（`#007AFF`）
- [ ] 两个导出按钮的边框为蓝色（`#007AFF`）
- [ ] 悬停时按钮背景变为浅蓝色（`#E3F2FF`）
- [ ] 按钮的其他样式（边框、圆角、内边距）保持不变

### 4.2 回归测试

- [ ] 其他按钮（Load Tags、Add Tag 等）样式不受影响
- [ ] 页面整体布局正常
- [ ] 按钮点击功能正常

## 5. 风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 样式冲突 | 低 | 中 | 使用新样式类，避免修改现有类 |
| 其他页面受影响 | 低 | 低 | 仅修改 tags.html 模板 |

## 6. 实施计划

1. 修改 `src/templates/tags.html` - 更新按钮 class
2. 修改 `src/static/css/main.css` - 添加 `.btn-export` 样式
3. 本地验证样式效果
4. 提交代码并推送

## 7. 回滚方案

如需回滚，只需：
1. 将 HTML 中的 `btn-export` 改回 `btn-info`
2. 删除 `.btn-export` CSS 样式
