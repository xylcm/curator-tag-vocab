# 导出按钮位置调整 — 技术方案

> GitHub Issue: #39
> PRD: docs/prds/issue-39.md
> 创建日期: 2026-02-13
> 状态: Draft

## 1. 概述

将导出按钮（Export Protobuf、Export CSV）从控制栏区域移动到页面右上角，与页面标题 "Curator Tag Vocabulary" 水平对齐，使界面布局更加清晰合理。

## 2. 方案设计

### 2.1 整体思路

通过调整 HTML 结构和 CSS 样式，将导出按钮从 `.controls` 区域移至 `.header` 区域，使其与标题水平对齐并靠右展示。保持原有按钮样式和 JavaScript 事件绑定不变。

### 2.2 详细设计

#### HTML 结构调整

修改 `src/templates/tags.html`：

1. **修改 `.header` 区域**：添加 `header-actions` 容器用于放置导出按钮
   - 将 `.header` 改为 flex 布局，使标题和按钮组水平排列
   - 在 `.header` 内部添加 `.header-actions` div，包含两个导出按钮

2. **从 `.controls` 移除导出按钮**：
   - 删除 `id="export-protobuf-btn"` 和 `id="export-csv-btn"` 按钮

修改后的 `.header` 结构示例：
```html
<div class="header">
    <div class="header-left">
        <h1>Curator Tag Vocabulary</h1>
        <div class="stats">...</div>
    </div>
    <div class="header-actions">
        <button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
        <button class="btn btn-info" id="export-csv-btn">Export CSV</button>
    </div>
</div>
```

#### CSS 样式调整

修改 `src/static/css/main.css`：

1. **更新 `.header` 样式**：
   - 添加 `display: flex`
   - 添加 `justify-content: space-between` 实现左右分布
   - 添加 `align-items: flex-start` 顶部对齐

2. **新增 `.header-left` 样式**：
   - 使用 `flex: 1` 占据剩余空间

3. **新增 `.header-actions` 样式**：
   - 使用 `display: flex`
   - 使用 `gap: 12px` 按钮间距
   - 使用 `align-items: center` 垂直居中
   - 添加 `padding-top` 与标题对齐

4. **响应式处理**：
   - 在 `@media (max-width: 768px)` 中调整布局
   - 小屏幕下保持垂直堆叠或按钮换行

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/templates/tags.html` | 修改 | 调整 `.header` 结构，添加导出按钮；从 `.controls` 移除导出按钮 |
| `src/static/css/main.css` | 修改 | 更新 `.header` 样式，新增 `.header-left` 和 `.header-actions` 样式 |
| `src/static/js/tags.js` | 无变更 | 按钮 ID 保持不变，事件绑定无需修改 |

## 4. 实现步骤

1. **修改 HTML 结构**
   - 在 `tags.html` 中重构 `.header` 区域，添加 `.header-left` 和 `.header-actions`
   - 将导出按钮移至 `.header-actions`
   - 从 `.controls` 中移除导出按钮

2. **添加 CSS 样式**
   - 更新 `.header` 为 flex 布局
   - 添加 `.header-left` 样式
   - 添加 `.header-actions` 样式
   - 添加响应式媒体查询

3. **验证功能完整性**
   - 确认导出按钮点击后仍能正常导出数据
   - 确认响应式布局在各种屏幕尺寸下正常显示

## 5. 测试策略

- **视觉测试**: 验证导出按钮显示在页面右上角，与标题水平对齐
- **功能测试**: 验证 Export Protobuf 和 Export CSV 按钮点击后正常导出数据
- **响应式测试**: 在 768px 和 480px 宽度下验证布局不重叠、不溢出

## 6. 风险与待决事项

- **无已知风险**: 此变更为纯前端 UI 调整，不涉及后端逻辑或数据模型变更
- **样式兼容性**: 需要确保新增样式与现有设计系统保持一致
