# 导出按钮位置和样式调整 — 技术方案

> GitHub Issue: #87
> PRD: docs/prds/issue-87.md
> 创建日期: 2026-03-04
> 状态: Draft

## 1. 概述

调整标签管理页面控制栏中导出按钮的布局和视觉样式，将 Export Protobuf 和 Export CSV 按钮从第一行移至第二行，并应用黄色高亮样式以提升视觉区分度。

## 2. 方案设计

### 2.1 整体思路

本次变更为纯前端样式调整，不涉及后端逻辑或数据库变更。核心策略：

1. **HTML 结构调整**：在现有 `.controls` 容器内新增一个独立的 `<div>` 包裹两个导出按钮，利用 flexbox 的 `flex-wrap: wrap` 特性使其自动换行到第二行
2. **CSS 样式新增**：创建新的 `.btn-export` 样式类，定义黄色高亮配色方案
3. **响应式适配**：确保在移动端（768px 以下）导出按钮布局正常

**设计决策**：
- 选择在现有 `.controls` 容器内新增子容器，而非创建独立的第二行容器，原因是：
  - 保持 sticky 定位的完整性（避免两个独立的 sticky 容器）
  - 利用现有的 `flex-wrap: wrap` 机制，代码改动最小
  - 保持控制栏的视觉统一性

### 2.2 详细设计

#### 2.2.1 HTML 结构变更

**当前结构**（`src/templates/tags.html` L29-66）：
```html
<div class="controls-wrapper">
    <div class="controls">
        <!-- 搜索框和筛选器 -->
        <input type="text" id="search-input" ...>
        <select id="deleted-select">...</select>
        <!-- ... 其他筛选器 ... -->

        <!-- 操作按钮 -->
        <button class="btn btn-primary" id="load-btn">Load Tags</button>
        <button class="btn btn-success" id="add-btn">Add Tag</button>
        <button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
        <button class="btn btn-info" id="export-csv-btn">Export CSV</button>
    </div>
</div>
```

**调整后结构**：
```html
<div class="controls-wrapper">
    <div class="controls">
        <!-- 搜索框和筛选器 -->
        <input type="text" id="search-input" ...>
        <select id="deleted-select">...</select>
        <!-- ... 其他筛选器 ... -->

        <!-- 第一行操作按钮 -->
        <button class="btn btn-primary" id="load-btn">Load Tags</button>
        <button class="btn btn-success" id="add-btn">Add Tag</button>

        <!-- 第二行导出按钮（独立容器） -->
        <div class="export-buttons">
            <button class="btn btn-export" id="export-protobuf-btn">Export Protobuf</button>
            <button class="btn btn-export" id="export-csv-btn">Export CSV</button>
        </div>
    </div>
</div>
```

**关键点**：
- 新增 `.export-buttons` 容器包裹两个导出按钮
- 将按钮样式类从 `btn-info` 改为 `btn-export`
- 保持按钮 ID 不变，确保 JavaScript 事件绑定不受影响

#### 2.2.2 CSS 样式新增

**新增样式类**（添加到 `src/static/css/main.css` 的按钮样式区域，约 L159 之后）：

```css
/* 导出按钮黄色高亮样式 */
.btn-export {
    background: #f7ff07;
    color: #007aff;
    border: 1px solid #eeffb8;
}

.btn-export:hover {
    background: #e8f500;
    border-color: #d4dae0;
}

/* 导出按钮容器 */
.export-buttons {
    display: flex;
    gap: 12px;
    width: 100%;
    flex-basis: 100%;
}
```

**样式说明**：
- `.btn-export`：
  - 背景色 `#f7ff07`（亮黄色，符合 PRD 要求）
  - 文字颜色 `#007aff`（蓝色，与现有按钮文字颜色一致）
  - 边框颜色 `#eeffb8`（淡黄色系，与背景协调）
  - hover 状态背景色微调为 `#e8f500`（稍深的黄色，提供视觉反馈）

- `.export-buttons`：
  - `display: flex`：使两个按钮水平排列
  - `gap: 12px`：与 `.controls` 的 gap 保持一致
  - `width: 100%` 和 `flex-basis: 100%`：强制容器占据整行宽度，触发父容器的 flex-wrap 换行

#### 2.2.3 响应式适配

现有的媒体查询（`main.css` L680-744）已对 `.controls` 容器做了响应式处理，新增的 `.export-buttons` 容器会自动继承这些规则。

**验证点**：
- 在 768px 以下屏幕宽度，导出按钮应保持在第二行
- 在 480px 以下屏幕宽度，如果空间不足，两个导出按钮可能会垂直堆叠（由 flexbox 自动处理）

**可选增强**（如测试发现移动端布局问题）：
```css
@media (max-width: 480px) {
    .export-buttons {
        flex-direction: column;
        gap: 8px;
    }
}
```

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/templates/tags.html` | 修改 | 调整控制栏按钮结构，新增 `.export-buttons` 容器 |
| `src/static/css/main.css` | 新增 | 添加 `.btn-export` 和 `.export-buttons` 样式类 |
| `src/static/js/tags.js` | 无变更 | 按钮 ID 保持不变，事件绑定无需修改 |
| `src/routers/tag_manager.py` | 无变更 | 后端导出逻辑不受影响 |

**依赖关系**：
- 无外部依赖变更
- 无数据库 schema 变更
- 无 API 接口变更

## 4. 实现步骤

1. **修改 HTML 结构**
   - 编辑 `src/templates/tags.html`
   - 在 L63-64 的两个导出按钮外包裹 `<div class="export-buttons">` 容器
   - 将按钮样式类从 `btn-info` 改为 `btn-export`

2. **新增 CSS 样式**
   - 编辑 `src/static/css/main.css`
   - 在 L159（`.btn-info` 样式之后）插入 `.btn-export` 和 `.export-buttons` 样式定义

3. **本地测试验证**
   - 启动应用：`python src/app_tagging.py`
   - 访问 `http://localhost:80/tagging/vocab`
   - 验证导出按钮在第二行且样式正确
   - 测试响应式布局（调整浏览器窗口宽度至 768px、480px）
   - 点击导出按钮确认功能正常

4. **提交变更**
   - 提交 HTML 和 CSS 变更
   - 推送到远程分支

## 5. 测试策略

### 5.1 视觉验证

**桌面端（>768px）**：
- [ ] 导出按钮在第二行，位于控制栏左侧
- [ ] 两个导出按钮水平相邻，间距 12px
- [ ] 背景色为亮黄色（`#f7ff07`），文字为蓝色（`#007aff`）
- [ ] 鼠标悬停时背景色变为 `#e8f500`
- [ ] 按钮圆角、内边距与其他按钮一致

**平板端（768px）**：
- [ ] 导出按钮保持在第二行
- [ ] 布局无错位或重叠

**移动端（480px）**：
- [ ] 导出按钮布局正常（可能垂直堆叠）
- [ ] 按钮可点击，无遮挡

### 5.2 功能验证

- [ ] 点击 "Export Protobuf" 按钮，触发 Protobuf 文件下载
- [ ] 点击 "Export CSV" 按钮，触发 CSV 文件下载
- [ ] 其他按钮（Load Tags、Add Tag）功能不受影响
- [ ] 筛选器和搜索框功能正常

### 5.3 兼容性验证

- [ ] Chrome/Edge（最新版）
- [ ] Firefox（最新版）
- [ ] Safari（最新版）

## 6. 风险与待决事项

### 6.1 已知风险

**低风险**：
- **样式冲突**：新增的 `.btn-export` 样式可能与未来的按钮样式冲突
  - **缓解措施**：使用语义化命名，遵循现有样式系统的命名规范

- **移动端布局**：在极小屏幕（<400px）上，导出按钮可能显示异常
  - **缓解措施**：实现步骤 3 中包含移动端测试，如发现问题可添加媒体查询修正

### 6.2 待决事项

无。本方案为纯前端样式调整，技术路径明确，无需额外决策。

### 6.3 备选方案（已否决）

**方案 A：创建独立的第二行容器**
```html
<div class="controls-wrapper">
    <div class="controls">
        <!-- 第一行内容 -->
    </div>
    <div class="export-controls">
        <!-- 第二行导出按钮 -->
    </div>
</div>
```

**否决理由**：
- 需要调整 `.controls-wrapper` 的 sticky 定位逻辑
- 增加 CSS 复杂度（需为 `.export-controls` 单独定义样式）
- 不符合"变更最小化"原则

---

**方案确认**：本方案已就绪，可进入编码实现阶段。
