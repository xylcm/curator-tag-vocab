# 导出按钮位置调整 — 技术方案

> GitHub Issue: #41
> PRD: docs/prds/issue-41.md
> 创建日期: 2025-02-24
> 状态: Draft

## 1. 概述

将导出按钮（Export Protobuf 和 Export CSV）从筛选控制区域移动到页面右上角，与标题 "Curator Tag Vocabulary" 水平对齐，优化页面布局并提升用户体验。

## 2. 方案设计

### 2.1 整体思路

通过调整 HTML 结构和 CSS 样式，将导出按钮从 `.controls` 区域迁移到 `.header` 区域。采用 Flexbox 布局实现标题与按钮的水平对齐，保持按钮原有样式和功能不变。

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
        <!-- 筛选控件 -->
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
        <!-- 筛选控件（移除导出按钮） -->
    </div>
</div>
```

#### CSS 样式变更

**新增样式：**
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

**响应式适配：**
```css
@media (max-width: 768px) {
    .header-top {
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
    }

    .header-actions {
        width: 100%;
        justify-content: flex-start;
    }
}
```

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/templates/tags.html` | 修改 | 调整 header 结构，添加 `header-top` 和 `header-actions` 容器，移动导出按钮 |
| `src/static/css/main.css` | 修改 | 新增 `.header-top` 和 `.header-actions` 样式，添加响应式适配 |
| `src/static/js/tags.js` | 无变更 | 按钮 ID 保持不变，事件绑定无需修改 |

## 4. 实现步骤

1. **修改 HTML 结构** (`src/templates/tags.html`)
   - 在 `.header` 内添加 `.header-top` 容器
   - 将 `h1` 标题和导出按钮移入 `.header-top`
   - 从 `.controls` 中移除两个导出按钮

2. **添加 CSS 样式** (`src/static/css/main.css`)
   - 添加 `.header-top` Flexbox 布局样式
   - 添加 `.header-actions` 按钮容器样式
   - 调整 `.header-top h1` 的 margin
   - 在媒体查询中添加响应式适配

3. **验证功能**
   - 确认导出按钮点击功能正常
   - 确认页面在桌面端和移动端显示正常

## 5. 测试策略

- **视觉测试**: 验证按钮位置与标题水平对齐，靠右展示
- **功能测试**: 验证 Export Protobuf 和 Export CSV 按钮点击后正常下载文件
- **响应式测试**: 验证在 768px 以下和 480px 以下屏幕布局正常
- **回归测试**: 验证其他按钮（Load Tags, Add Tag）功能正常

## 6. 风险与待决事项

- **无技术风险**: 本次变更为纯前端布局调整，不涉及后端逻辑或数据变更
- **兼容性**: 使用标准 Flexbox 布局，兼容所有现代浏览器
