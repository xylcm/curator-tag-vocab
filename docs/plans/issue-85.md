# 技术方案：页面视觉样式调整 - 下载按钮位置和样式

## 关联 Issue
- Issue: #85
- PRD: `docs/prds/issue-85.md`

---

## 1. 概述

本方案描述如何将标签管理页面的下载按钮（Export Protobuf 和 Export CSV）从第一行移至第二行，并应用新的黄色样式。

---

## 2. 变更范围

### 2.1 受影响文件

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `src/templates/tags.html` | 修改 | 调整按钮 HTML 结构，将导出按钮移至新的容器 |
| `src/static/css/main.css` | 修改 | 新增 `.btn-export` 样式类，调整布局容器样式 |

### 2.2 不变更的文件
- `src/static/js/tags.js` - 按钮点击事件处理逻辑保持不变
- `src/routers/tag_manager.py` - 后端导出 API 保持不变

---

## 3. 技术实现

### 3.1 HTML 结构调整

**当前结构（第 29-66 行）：**
```html
<div class="controls-wrapper">
    <div class="controls">
        <!-- 所有控件在同一行 -->
        <input type="text" id="search-input" ...>
        <select id="deleted-select">...</select>
        ...
        <button class="btn btn-primary" id="load-btn">Load Tags</button>
        <button class="btn btn-success" id="add-btn">Add Tag</button>
        <button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
        <button class="btn btn-info" id="export-csv-btn">Export CSV</button>
    </div>
</div>
```

**目标结构：**
```html
<div class="controls-wrapper">
    <!-- 第一行：筛选控制区 -->
    <div class="controls controls-row-primary">
        <input type="text" id="search-input" ...>
        <select id="deleted-select">...</select>
        ...
        <button class="btn btn-primary" id="load-btn">Load Tags</button>
        <button class="btn btn-success" id="add-btn">Add Tag</button>
    </div>
    <!-- 第二行：导出按钮区 -->
    <div class="controls controls-row-secondary">
        <button class="btn btn-export" id="export-protobuf-btn">Export Protobuf</button>
        <button class="btn btn-export" id="export-csv-btn">Export CSV</button>
    </div>
</div>
```

### 3.2 CSS 样式新增

**新增 `.btn-export` 类（在 `.btn-info` 之后）：**
```css
.btn-export {
    background: #f7ff07;
    color: #007aff;
    border: 1px solid #d4dae0;
    padding: 11px 21px;
}

.btn-export:hover {
    background: #e8f007;
    border-color: #c8d0d6;
}
```

**调整 `.controls-wrapper` 布局：**
```css
.controls-wrapper {
    position: sticky;
    top: 0;
    z-index: 100;
    background: #f5f5f7;
    border-bottom: 1px solid #e0e0e0;
    padding: 16px 0;
    margin-bottom: 24px;
    /* 新增：支持多行布局 */
    display: flex;
    flex-direction: column;
    gap: 12px;
}
```

**调整 `.controls-row-secondary` 右对齐：**
```css
.controls-row-secondary {
    justify-content: flex-end;
}
```

### 3.3 响应式适配

**保持现有断点（768px 和 480px）：**
- 在移动端，两个控制行都会自动换行
- 导出按钮行保持右对齐或根据空间自适应

---

## 4. 实现步骤

1. **修改 `src/templates/tags.html`**
   - 将 `.controls` 内的两个导出按钮移至新的 `.controls` 容器
   - 将导出按钮的类从 `btn btn-info` 改为 `btn btn-export`
   - 为第一行容器添加 `controls-row-primary` 类
   - 为第二行容器添加 `controls-row-secondary` 类

2. **修改 `src/static/css/main.css`**
   - 在 `.btn-info` 样式后添加 `.btn-export` 类定义
   - 修改 `.controls-wrapper` 添加 `display: flex; flex-direction: column; gap: 12px;`
   - 添加 `.controls-row-secondary { justify-content: flex-end; }`

---

## 5. 测试策略

### 5.1 视觉验证
- [ ] Export Protobuf 和 Export CSV 按钮显示在第二行
- [ ] 按钮背景色为亮黄色 (#f7ff07)
- [ ] 按钮文字颜色为蓝色 (#007aff)
- [ ] 按钮边框颜色符合设计规范
- [ ] 按钮内边距为 11px 21px
- [ ] 按钮 hover 状态正常（背景色略深）
- [ ] 按钮 active 状态正常（scale 0.98）

### 5.2 功能验证
- [ ] 点击 Export Protobuf 按钮正常触发下载
- [ ] 点击 Export CSV 按钮正常触发下载
- [ ] 其他按钮（Load Tags, Add Tag）功能不受影响

### 5.3 响应式验证
- [ ] 桌面端（>768px）显示正常
- [ ] 平板端（768px）显示正常
- [ ] 移动端（480px）显示正常

---

## 6. 风险与回滚

### 6.1 风险
- **低风险**：纯前端样式调整，不影响数据逻辑
- **潜在影响**：如果 `.btn-info` 类在其他地方被使用，本次不修改该类，无影响

### 6.2 回滚方案
如需回滚，只需恢复两个文件的修改即可。

---

## 7. 验收标准

- [ ] Export Protobuf 和 Export CSV 按钮显示在第二行（右对齐）
- [ ] 按钮背景色为亮黄色 (#f7ff07)
- [ ] 按钮边框颜色符合设计规范
- [ ] 按钮内边距调整为 11px 21px
- [ ] 按钮 hover 和 active 状态正常
- [ ] 移动端显示正常
