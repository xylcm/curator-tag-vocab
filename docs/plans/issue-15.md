# 技术方案：导出按钮布局和样式调整

> GitHub Issue: #15
> PRD: docs/prds/issue-15.md
> 创建日期: 2025-01-21

## 1. 技术目标

将导出按钮（Export Protobuf、Export CSV）从控制栏区域移动到页面右上角，与标题水平对齐并靠右展示。

## 2. 变更范围

### 2.1 涉及的文件

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `src/templates/tags.html` | 修改 | 调整按钮位置，从 controls 区域移至 header 区域 |
| `src/static/css/main.css` | 修改 | 添加/修改 header 和 export-buttons 的样式 |

### 2.2 不涉及变更的文件

- JavaScript 文件（按钮点击事件逻辑保持不变）
- 后端路由和 API
- 数据库 schema

## 3. 技术方案

### 3.1 HTML 结构调整

当前结构：
```html
<div class="header">
    <h1>Curator Tag Vocabulary</h1>
    <div class="stats">...</div>
</div>
<div class="controls-wrapper">
    <div class="controls">
        <!-- 导出按钮在这里 -->
        <button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
        <button class="btn btn-info" id="export-csv-btn">Export CSV</button>
    </div>
</div>
```

调整后结构：
```html
<div class="header">
    <div class="header-top">
        <h1>Curator Tag Vocabulary</h1>
        <div class="export-buttons">
            <button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
            <button class="btn btn-info" id="export-csv-btn">Export CSV</button>
        </div>
    </div>
    <div class="stats">...</div>
</div>
<div class="controls-wrapper">
    <div class="controls">
        <!-- 导出按钮已移除 -->
    </div>
</div>
```

### 3.2 CSS 样式调整

新增样式：
```css
.header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.export-buttons {
    display: flex;
    gap: 12px;
}
```

修改 `.header h1`：
- 移除 `margin-bottom: 24px`（移至 `.header-top`）

### 3.3 响应式适配

在 `@media (max-width: 768px)` 和 `@media (max-width: 480px)` 中添加：
```css
.header-top {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
}

.export-buttons {
    width: 100%;
    justify-content: flex-start;
}
```

## 4. 验收标准验证

| 验收标准 | 验证方式 |
|----------|----------|
| 导出按钮显示在页面右上角 | 视觉检查 |
| 与标题水平对齐 | 视觉检查，使用 flex 布局确保对齐 |
| 靠右展示 | `.header-top` 使用 `justify-content: space-between` |
| 保持原有样式 | 按钮保留 `btn btn-info` 类 |
| 保持交互行为 | 按钮 ID 不变，JavaScript 事件绑定不受影响 |
| 响应式适配 | 移动端按钮移至标题下方，左对齐 |

## 5. 风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 按钮 ID 变更导致 JS 失效 | 低 | 高 | 保持按钮 ID 不变 |
| 样式冲突 | 低 | 中 | 使用新的 CSS 类名，避免与现有样式冲突 |
| 响应式布局问题 | 低 | 中 | 测试移动端显示效果 |

## 6. 实施步骤

1. 修改 `src/templates/tags.html`：
   - 添加 `.header-top` 容器包裹 h1 和导出按钮
   - 从 `.controls` 中移除导出按钮

2. 修改 `src/static/css/main.css`：
   - 添加 `.header-top` 和 `.export-buttons` 样式
   - 调整 `.header h1` 的 margin
   - 添加响应式样式

3. 验证：
   - 检查桌面端布局
   - 检查移动端响应式效果
   - 验证按钮点击功能正常
