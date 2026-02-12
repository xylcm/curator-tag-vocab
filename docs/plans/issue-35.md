# 导出按钮布局调整 — 技术方案

> GitHub Issue: #35
> PRD: docs/prds/issue-35.md
> 创建日期: 2025-01-21
> 状态: Draft

## 1. 概述

将导出按钮（Export Protobuf 和 Export CSV）从控制栏区域移动到页面右上角，与页面标题 "Curator Tag Vocabulary" 水平对齐并靠右展示，优化界面布局层次。

## 2. 方案设计

### 2.1 整体思路

修改 `header` 区域的布局结构，将标题和导出按钮放在同一水平线上。通过 Flexbox 布局实现标题左对齐、导出按钮右对齐的效果。同时从控制栏（controls）中移除导出按钮。

### 2.2 详细设计

#### HTML 结构变更 (`src/templates/tags.html`)

**当前结构：**
```html
<div class="header">
    <h1>Curator Tag Vocabulary</h1>
    <div class="stats">...</div>
</div>

<div class="controls-wrapper">
    <div class="controls">
        <!-- 筛选控件 -->
        <button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
        <button class="btn btn-info" id="export-csv-btn">Export CSV</button>
    </div>
</div>
```

**新结构：**
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

<div class="controls-wrapper">
    <div class="controls">
        <!-- 仅保留筛选控件，移除导出按钮 -->
    </div>
</div>
```

#### CSS 样式变更 (`src/static/css/main.css`)

新增样式：
```css
.header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.header-top h1 {
    margin-bottom: 0;  /* 移除原有 margin-bottom */
}

.header-actions {
    display: flex;
    gap: 12px;
}
```

#### 响应式适配

在 `@media (max-width: 768px)` 和 `@media (max-width: 480px)` 中添加：
```css
@media (max-width: 768px) {
    .header-top {
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
    }

    .header-top h1 {
        margin-bottom: 0;
    }
}
```

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/templates/tags.html` | 修改 | 调整 header 结构，添加 header-top 和 header-actions 容器；从 controls 中移除导出按钮 |
| `src/static/css/main.css` | 修改 | 新增 .header-top 和 .header-actions 样式；添加响应式适配规则 |
| `src/static/js/tags.js` | 无变更 | 按钮的 ID 保持不变，事件绑定无需修改 |

## 4. 实现步骤

1. **修改 HTML 结构**
   - 在 `header` 内添加 `header-top` 容器包裹 `h1` 和新的 `header-actions`
   - 将导出按钮从 `controls` 移动到 `header-actions`
   - 保持按钮的 ID 和样式类不变

2. **添加 CSS 样式**
   - 添加 `.header-top` 样式：flex 布局，两端对齐，垂直居中
   - 添加 `.header-actions` 样式：flex 布局，12px 间距
   - 调整 `.header-top h1` 的 margin-bottom 为 0

3. **响应式适配**
   - 在 768px 和 480px 断点下，将 header-top 改为垂直布局
   - 确保小屏幕下标题和按钮不会重叠

4. **验证测试**
   - 检查桌面端布局：标题左对齐，导出按钮右对齐，水平对齐
   - 检查移动端布局：标题和按钮垂直排列，无重叠
   - 验证导出按钮功能正常（点击触发下载）

## 5. 测试策略

- **视觉测试**: 在桌面端（1400px+）、平板端（768px）、移动端（480px）验证布局
- **功能测试**: 验证 Export Protobuf 和 Export CSV 按钮点击后正常触发下载
- **回归测试**: 确认控制栏其他按钮（Load Tags, Add Tag）功能正常

## 6. 风险与待决事项

- 无技术风险，此变更为纯前端布局和样式调整
- 按钮 ID 保持不变，JavaScript 事件绑定无需修改
- 导出功能的后端 API 不受影响
