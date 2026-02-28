# 导出按钮背景色变更为紫色 — 技术方案

> GitHub Issue: #79
> PRD: docs/prds/issue-79.md
> 创建日期: 2026-02-28
> 状态: Draft

## 1. 概述

将标签管理页面中两个导出按钮（"Export Protobuf" 和 "Export CSV"）的背景色从当前的蓝色（`.btn-info` 样式）改为紫色，以提升视觉区分度和用户体验。

## 2. 方案设计

### 2.1 整体思路

根据 PRD 定义的颜色规范，在 CSS 中新增 `.btn-purple` 样式类，然后将模板中两个导出按钮的类名从 `.btn-info` 修改为 `.btn-purple`。

### 2.2 详细设计

#### CSS 样式变更

在 `src/static/css/main.css` 中新增 `.btn-purple` 样式类，定义如下：

```css
.btn-purple {
    background: #f3e8ff;
    color: #9333ea;
    border: 1px solid #e0c3fc;
}

.btn-purple:hover {
    background: #e0c3fc;
    border-color: #d4a5f9;
}
```

#### HTML 模板变更

在 `src/templates/tags.html` 中修改两个导出按钮的类名：

```html
<!-- 修改前 -->
<button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-info" id="export-csv-btn">Export CSV</button>

<!-- 修改后 -->
<button class="btn btn-purple" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-purple" id="export-csv-btn">Export CSV</button>
```

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/static/css/main.css` | 新增 | 新增 `.btn-purple` 和 `.btn-purple:hover` 样式定义 |
| `src/templates/tags.html` | 修改 | 将两个导出按钮的类名从 `btn-info` 改为 `btn-purple` |

## 4. 实现步骤

1. **新增紫色按钮样式**
   - 在 `src/static/css/main.css` 的 `.btn-info` 样式之后添加 `.btn-purple` 样式定义
   - 确保颜色值与 PRD 定义一致

2. **更新按钮类名**
   - 在 `src/templates/tags.html` 中找到两个导出按钮
   - 将 `class="btn btn-info"` 改为 `class="btn btn-purple"`

3. **本地验证**
   - 启动应用并访问页面
   - 确认两个导出按钮显示为紫色背景
   - 验证 hover 状态样式正确

## 5. 测试策略

- **视觉测试**: 手动访问页面，确认两个导出按钮显示为紫色背景（#f3e8ff）和紫色文字（#9333ea）
- **交互测试**: 验证按钮的 hover 状态背景色变为 #e0c3fc
- **回归测试**: 确认其他按钮（Load Tags、Add Tag）的样式未受影响

## 6. 风险与待决事项

- **无风险**: 此变更为纯前端样式调整，不影响后端逻辑和数据
- **兼容性**: 新样式类 `.btn-purple` 为新增类，不影响现有样式
