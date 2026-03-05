# 导出按钮位置和样式调整 — 技术方案

> GitHub Issue: #95
> PRD: docs/prds/issue-95.md
> 创建日期: 2026-03-05
> 状态: Draft

## 1. 概述

根据 PRD 要求，调整标签管理页面中导出按钮的位置和样式：
1. 将导出按钮（Export Protobuf、Export CSV）从第一行移至独立的第二行
2. 为导出按钮应用亮黄色背景和蓝色文字的醒目样式
3. 第二行按钮右对齐，与第一行按钮区域对齐

## 2. 方案设计

### 2.1 整体思路

这是一个纯前端 UI 调整任务，涉及 HTML 结构修改和 CSS 样式添加：

1. **HTML 结构调整**：将 `.controls` 容器内的导出按钮移至新的 `.export-controls` 行
2. **CSS 样式添加**：新增导出按钮专用样式类 `.btn-export`，应用亮黄色背景和蓝色文字
3. **布局调整**：使用 Flexbox 实现第二行右对齐，保持与第一行按钮区域对齐

### 2.2 详细设计

#### HTML 结构变更（tags.html）

当前结构：
```html
<div class="controls-wrapper">
    <div class="controls">
        <!-- 搜索框、筛选器 -->
        <button class="btn btn-primary" id="load-btn">Load Tags</button>
        <button class="btn btn-success" id="add-btn">Add Tag</button>
        <button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
        <button class="btn btn-info" id="export-csv-btn">Export CSV</button>
    </div>
</div>
```

调整后结构：
```html
<div class="controls-wrapper">
    <div class="controls-row controls-main">
        <!-- 搜索框、筛选器 -->
        <button class="btn btn-primary" id="load-btn">Load Tags</button>
        <button class="btn btn-success" id="add-btn">Add Tag</button>
    </div>
    <div class="controls-row controls-export">
        <button class="btn btn-export" id="export-protobuf-btn">Export Protobuf</button>
        <button class="btn btn-export" id="export-csv-btn">Export CSV</button>
    </div>
</div>
```

#### CSS 样式变更（main.css）

1. 修改 `.controls-wrapper` 支持多行布局：
```css
.controls-wrapper {
    display: flex;
    flex-direction: column;
    gap: 12px;
    /* 保留原有样式 */
}
```

2. 新增 `.controls-row` 类：
```css
.controls-row {
    display: flex;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 32px;
    width: 100%;
}
```

3. 新增导出按钮样式：
```css
.btn-export {
    background: #f7ff07;
    color: #007aff;
    border: 1px solid #d4dae0;
    height: 38px;
    padding: 10px 21px;
    border-radius: 6px;
}

.btn-export:hover {
    background: #e8f000;
    border-color: #c0c6cc;
}
```

4. 导出按钮行右对齐：
```css
.controls-export {
    justify-content: flex-end;
}
```

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| src/templates/tags.html | 修改 | 调整 controls 结构，将导出按钮移至独立行 |
| src/static/css/main.css | 修改 | 添加 .controls-row、.btn-export 样式，调整 .controls-wrapper 布局 |

## 4. 实现步骤

1. **修改 HTML 结构**
   - 将 `.controls` 重命名为 `.controls-row controls-main`
   - 移除导出按钮
   - 新增 `.controls-row controls-export` 容器放置导出按钮
   - 为导出按钮添加 `.btn-export` 类

2. **修改 CSS 样式**
   - 更新 `.controls-wrapper` 为 flex 纵向布局
   - 新增 `.controls-row` 通用行样式
   - 新增 `.btn-export` 按钮样式（亮黄色背景 #f7ff07，蓝色文字 #007aff）
   - 添加 `.controls-export` 右对齐样式
   - 保留原有 `.controls` 类以确保向后兼容（可选）

3. **验证响应式布局**
   - 检查移动端（< 768px）和桌面端的显示效果
   - 确保导出按钮在窄屏下正确换行

## 5. 测试策略

- **视觉测试**：
  - 验证导出按钮显示在第二行
  - 验证第一行仅显示搜索框、筛选器、Load Tags、Add Tag
  - 验证导出按钮背景色为 #f7ff07（亮黄色）
  - 验证导出按钮文字颜色为 #007aff（蓝色）
  - 验证第二行按钮右对齐

- **功能测试**：
  - 验证 Export Protobuf 按钮点击后正常导出 protobuf 文件
  - 验证 Export CSV 按钮点击后正常导出 CSV 文件

- **响应式测试**：
  - 验证在 768px 以下屏幕正常显示
  - 验证在 480px 以下屏幕正常显示

## 6. 风险与待决事项

- **无技术风险**：此变更仅涉及前端 UI 调整，不涉及后端逻辑或数据模型变更
- **向后兼容**：导出按钮的 ID 保持不变（`export-protobuf-btn`、`export-csv-btn`），JS 事件绑定不受影响
- **样式冲突**：新增的 `.btn-export` 类名在现有代码中不存在，无冲突风险
