# 导出按钮布局和样式调整 — 技术方案

> GitHub Issue: #31
> PRD: docs/prds/issue-31.md
> 创建日期: 2025-01-21
> 状态: Draft

## 1. 概述

将导出按钮（Export Protobuf、Export CSV）从控制栏区域移动到页面右上角，与标题 "Curator Tag Vocabulary" 水平对齐并靠右展示，使页面布局更加清晰合理。

## 2. 方案设计

### 2.1 整体思路

通过调整 HTML 结构和 CSS 样式，将导出按钮从 `.controls` 区域移出，放置到 `.header` 区域内，与标题形成左右分布布局。使用 Flexbox 布局实现标题左对齐、按钮右对齐的效果。

### 2.2 详细设计

#### 2.2.1 HTML 结构变更

**当前结构：**
```html
<div class="header">
    <h1>Curator Tag Vocabulary</h1>
    <div class="stats">...</div>
</div>

<div class="controls-wrapper">
    <div class="controls">
        <!-- 其他控件 -->
        <button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
        <button class="btn btn-info" id="export-csv-btn">Export CSV</button>
    </div>
</div>
```

**调整后结构：**
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
        <!-- 其他控件（不含导出按钮） -->
    </div>
</div>
```

#### 2.2.2 CSS 样式变更

新增 `.header-top` 和 `.header-actions` 样式：

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
    align-items: center;
}
```

#### 2.2.3 响应式适配

在媒体查询中添加响应式处理：

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

@media (max-width: 480px) {
    .header-actions {
        width: 100%;
        flex-wrap: wrap;
    }

    .header-actions .btn {
        flex: 1;
        min-width: 120px;
    }
}
```

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/templates/tags.html` | 修改 | 调整 header 结构，添加 header-top 和 header-actions 容器；从 controls 中移除导出按钮 |
| `src/static/css/main.css` | 修改 | 新增 .header-top 和 .header-actions 样式；添加响应式适配规则 |
| `src/static/js/tags.js` | 无变更 | 导出按钮的点击事件绑定通过 ID 实现，HTML 结构调整不影响 JS 功能 |

## 4. 实现步骤

1. **修改 HTML 结构**
   - 在 `src/templates/tags.html` 中，将 `<h1>` 和导出按钮包裹在 `.header-top` 容器中
   - 将导出按钮从 `.controls` 移动到 `.header-actions`
   - 保持按钮的 ID 和 class 不变以确保 JS 功能正常

2. **添加 CSS 样式**
   - 在 `src/static/css/main.css` 中添加 `.header-top` 和 `.header-actions` 样式
   - 调整 `.header h1` 的 margin-bottom（在 .header-top 中已处理）
   - 在媒体查询中添加响应式适配规则

3. **验证功能完整性**
   - 确认导出按钮点击事件正常工作
   - 确认页面布局符合预期
   - 确认响应式布局在各种屏幕尺寸下正常

## 5. 测试策略

- **视觉测试**: 验证导出按钮显示在页面右上角，与标题水平对齐
- **功能测试**: 验证 Export Protobuf 和 Export CSV 按钮点击后正常触发下载
- **响应式测试**: 在 768px 和 480px 以下屏幕尺寸验证布局不重叠、按钮可点击

## 6. 风险与待决事项

- 无已知技术风险，此变更为纯前端布局和样式调整，不涉及后端逻辑或数据变更
