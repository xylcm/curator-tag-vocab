# 导出按钮位置调整 — 技术方案

> GitHub Issue: #97
> PRD: docs/issues/issue-97/prd.md
> 创建日期: 2026-03-05
> 状态: Draft

## 1. 概述

将导出功能按钮（Export Protobuf 和 Export CSV）从当前控制栏区域移至页面右上角标题栏区域，实现主要操作（筛选、搜索）与次要操作（导出）的视觉分离。

## 2. 方案设计

### 2.1 整体思路

本次变更为纯前端 UI 调整，不涉及后端逻辑修改。核心思路是：

1. **HTML 结构调整**：将导出按钮从 `.controls` div 移至 `.header` div
2. **CSS 样式调整**：为 `.header` 添加 flex 布局，使按钮靠右对齐
3. **保持 JS 不变**：按钮 ID 保持不变，原有事件绑定无需修改

### 2.2 详细设计

#### HTML 结构变更

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
    <div class="header-main">
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
        <!-- 导出按钮已移除，其他控件保持不变 -->
    </div>
</div>
```

#### CSS 样式变更

新增以下样式类：

```css
.header-main {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.header-main h1 {
    margin-bottom: 0;  /* 移除原有 margin-bottom */
}

.header-actions {
    display: flex;
    gap: 12px;
    align-items: center;
}
```

调整 `.header h1` 样式：
```css
.header h1 {
    font-size: 32px;
    font-weight: 700;
    color: #1d1d1f;
    letter-spacing: -0.5px;
    /* 移除 margin-bottom: 24px; */
}
```

#### 响应式适配

在 `@media (max-width: 768px)` 和 `@media (max-width: 480px)` 中添加：

```css
@media (max-width: 768px) {
    .header-main {
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
    }
}
```

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/templates/tags.html` | 修改 | 调整 header 结构，添加 `.header-main` 和 `.header-actions` 容器，移除 controls 中的导出按钮 |
| `src/static/css/main.css` | 修改 | 添加 `.header-main` 和 `.header-actions` 样式，调整 `.header h1` 的 margin |
| `src/static/js/tags.js` | 无变更 | 按钮 ID 保持不变，事件绑定无需修改 |

## 4. 实现步骤

1. **修改 HTML 结构** (`src/templates/tags.html`)
   - 在 `.header` 内添加 `.header-main` 容器包裹 `h1` 和新的 `.header-actions`
   - 将两个导出按钮移至 `.header-actions` 内
   - 从 `.controls` 中移除导出按钮

2. **添加 CSS 样式** (`src/static/css/main.css`)
   - 添加 `.header-main` 样式（flex 布局，两端对齐）
   - 添加 `.header-actions` 样式（flex 布局，按钮间距）
   - 调整 `.header h1` 样式（移除 margin-bottom）
   - 添加响应式样式（移动端垂直排列）

3. **验证功能完整性**
   - 确认导出按钮点击后正常触发导出功能
   - 确认页面其他功能（搜索、筛选、添加标签等）不受影响
   - 确认在不同屏幕分辨率下布局显示正常

## 5. 测试策略

- **功能测试**: 点击导出按钮，验证 Protobuf 和 CSV 导出功能正常工作
- **视觉测试**: 检查按钮位置、样式是否符合 PRD 要求
- **响应式测试**: 在桌面端（1920x1080、1440x900）和移动端（768px、480px）下检查布局
- **回归测试**: 验证搜索、筛选、添加标签、编辑标签等功能不受影响

## 6. 风险与待决事项

- **风险**: 无重大技术风险，仅为 UI 布局调整
- **待决事项**: 无
