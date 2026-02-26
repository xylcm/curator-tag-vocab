# 导出按钮位置调整 — 技术方案

> GitHub Issue: #46
> 创建日期: 2025-01-20
> 状态: Draft

## 1. 概述

将导出按钮（Export Protobuf 和 Export CSV）从当前的 controls 区域移动到页面右上角，与标题 "Curator Tag Vocabulary" 水平对齐并靠右展示，以提升界面布局的清晰度和操作便捷性。

## 2. 方案设计

### 2.1 整体思路

通过调整 HTML 结构和 CSS 样式，将导出按钮从 controls-wrapper 区域分离，放置到 header 区域的右侧，与标题保持水平对齐。使用 Flexbox 布局实现标题左对齐、按钮右对齐的效果。

### 2.2 详细设计

#### HTML 结构调整 (`src/templates/tags.html`)

当前 header 结构：
```html
<div class="header">
    <h1>Curator Tag Vocabulary</h1>
    <div class="stats">...</div>
</div>
```

调整后结构：
```html
<div class="header">
    <div class="header-top">
        <h1>Curator Tag Vocabulary</h1>
        <div class="header-actions">
            <button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
            <button class="btn btn-info" id="export-csv-btn">Export CSV</button>
        </div>
    </div>
    <div class="stats">...</div>
</div>
```

同时从 controls 中移除导出按钮（第 63-64 行）。

#### CSS 样式调整 (`src/static/css/main.css`)

新增样式：
```css
.header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.header-top h1 {
    margin-bottom: 0;  /* 移除原有的 margin-bottom */
}

.header-actions {
    display: flex;
    gap: 12px;
}
```

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/templates/tags.html` | 修改 | 1. 在 header 内新增 header-top 容器包裹标题和导出按钮<br>2. 从 controls 中移除导出按钮 |
| `src/static/css/main.css` | 修改 | 新增 header-top 和 header-actions 样式类，调整标题 margin |

## 4. 实现步骤

1. **修改 HTML 结构**
   - 在 `src/templates/tags.html` 中，将 `<h1>` 和导出按钮包裹在新增的 `header-top` div 中
   - 从 `controls` div 中移除两个导出按钮

2. **添加 CSS 样式**
   - 在 `src/static/css/main.css` 中添加 `.header-top` 和 `.header-actions` 样式定义
   - 调整 `.header-top h1` 的 margin，去除底部间距

3. **验证布局效果**
   - 启动应用，检查导出按钮是否正确显示在右上角
   - 验证标题和按钮水平对齐
   - 测试响应式布局在不同屏幕尺寸下的表现

## 5. 测试策略

- **视觉验证**: 手动检查按钮位置是否与标题水平对齐且靠右展示
- **功能验证**: 确认导出按钮点击功能正常工作（Protobuf 和 CSV 导出）
- **响应式测试**: 验证在 768px 和 480px 以下屏幕宽度的布局表现

## 6. 风险与待决事项

- 无重大技术风险，此变更为纯前端 UI 调整
- 需确保导出按钮的 JavaScript 事件绑定不受影响（按钮 ID 保持不变）
