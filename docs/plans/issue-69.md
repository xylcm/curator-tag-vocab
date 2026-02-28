# 导出按钮背景色修改技术方案

> GitHub Issue: #69
> PRD: docs/prds/issue-69.md
> 创建日期: 2026-02-28
> 状态: Draft

## 需求概述

将标签管理页面中「Export Protobuf」和「Export CSV」两个导出按钮的背景色从浅蓝色（`#e3f2ff`）修改为白色（`#ffffff`），保持蓝色文字和边框样式不变，使按钮在视觉上更加简洁，与其他白色背景的表单元素保持一致。

## 技术实现

### 方案一：修改现有 `.btn-info` 样式（推荐）

直接修改 `src/static/css/main.css` 中的 `.btn-info` 样式类，将背景色从 `#e3f2ff` 改为 `#ffffff`。

**优点：**
- 改动最小，仅修改一个 CSS 属性
- 无需修改 HTML 模板
- 保持现有类名语义

**缺点：**
- 影响所有使用 `.btn-info` 类的按钮（当前仅两个导出按钮使用）

### 方案二：新增专用样式类

在 `src/static/css/main.css` 中新增 `.btn-export` 样式类，然后在 `src/templates/tags.html` 中将导出按钮的类名从 `btn-info` 改为 `btn-export`。

**优点：**
- 更精确的样式控制，不影响其他可能使用 `.btn-info` 的按钮
- 语义更清晰

**缺点：**
- 需要修改 HTML 和 CSS 两个文件
- 对于当前需求略显冗余

### 最终选择：方案一

选择方案一，因为：
1. 当前代码中 `.btn-info` 仅被两个导出按钮使用（通过搜索确认）
2. 改动最小，风险最低
3. 需求明确且简单，无需引入新的样式类

## 变更详情

### 文件: `src/static/css/main.css`

**修改前：**
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

**修改后：**
```css
.btn-info {
    background: #ffffff;
    color: #007aff;
    border: 1px solid #b8dcff;
}

.btn-info:hover {
    background: #f5f5f7;
    border-color: #9fceff;
}
```

**变更说明：**
- `background`: `#e3f2ff` → `#ffffff`（白色背景）
- `:hover background`: `#d0e8ff` → `#f5f5f7`（悬停时浅灰色背景，提供视觉反馈）
- `color`: 保持 `#007aff` 不变（蓝色文字）
- `border`: 保持 `#b8dcff` 不变（蓝色边框）

## 影响分析

### 受影响文件
- `src/static/css/main.css` - 修改 `.btn-info` 样式

### 无影响文件
- `src/templates/tags.html` - 无需修改，按钮已使用 `btn-info` 类
- 其他所有文件 - 无变更

## 测试策略

### 手动验证清单
- [ ] 访问 `/tagging/vocab` 页面
- [ ] 确认「Export Protobuf」按钮背景为白色
- [ ] 确认「Export CSV」按钮背景为白色
- [ ] 确认两个按钮文字仍为蓝色
- [ ] 确认按钮边框仍为蓝色
- [ ] 鼠标悬停在按钮上，确认有视觉反馈（背景变灰）
- [ ] 点击按钮，确认导出功能正常工作

### 浏览器兼容性
- 使用标准 CSS 属性，无兼容性问题
- 支持所有现代浏览器

## 风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 影响其他使用 `.btn-info` 的按钮 | 低 | 中 | 已确认当前仅导出按钮使用该样式 |
| 悬停效果不明显 | 低 | 低 | 使用 `#f5f5f7` 与白色有明显区别 |

## 实现步骤

1. 修改 `src/static/css/main.css` 中的 `.btn-info` 和 `.btn-info:hover` 样式
2. 本地启动应用验证效果
3. 提交变更

## 验收标准

- [x] 「Export Protobuf」按钮背景色为白色
- [x] 「Export CSV」按钮背景色为白色
- [x] 按钮文字颜色保持蓝色（`#007aff`），不做修改
- [x] 按钮边框保持蓝色系样式
- [x] 鼠标悬停时按钮有适当的视觉反馈
