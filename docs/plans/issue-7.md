# 技术实现方案：导出按钮字体颜色修改为红色

> GitHub Issue: #7
> 关联 PRD: docs/prds/issue-7.md
> 创建日期: 2025-02-10

## 1. 需求概述

将标签管理页面中两个导出按钮（"Export Protobuf" 和 "Export CSV"）的字体颜色修改为红色，使导出功能在界面上更加醒目。

## 2. 技术方案

### 2.1 方案选择

经过分析，有两种实现方案：

**方案 A：新增专用 CSS 类**
- 创建新的 `.btn-export` 类，继承 `btn-info` 的样式但将字体颜色设为红色
- 优点：样式集中管理，可复用
- 缺点：需要修改 HTML 和 CSS 两个文件

**方案 B：内联样式**
- 直接在 HTML 按钮元素上添加 `style="color: #ff3b30;"`
- 优点：修改简单直接，只涉及一个文件
- 缺点：样式分散，不易维护

**选择：方案 A（新增 CSS 类）**
- 更符合项目现有的代码风格（所有按钮样式都通过 CSS 类管理）
- 便于后续维护和复用
- 保持关注点分离（样式在 CSS，结构在 HTML）

### 2.2 具体实现

#### 修改文件 1: `src/static/css/main.css`

在 `.btn-info` 样式之后添加新的 `.btn-export` 类：

```css
.btn-export {
    background: #e3f2ff;
    color: #ff3b30;  /* 红色字体 */
    border: 1px solid #b8dcff;
}

.btn-export:hover {
    background: #d0e8ff;
    border-color: #9fceff;
}
```

#### 修改文件 2: `src/templates/tags.html`

将两个导出按钮的类名从 `btn-info` 改为 `btn-export`：

```html
<!-- 修改前 -->
<button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-info" id="export-csv-btn">Export CSV</button>

<!-- 修改后 -->
<button class="btn btn-export" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-export" id="export-csv-btn">Export CSV</button>
```

### 2.3 样式说明

- **背景色**: 保持 `#e3f2ff`（浅蓝色），与原来的 `btn-info` 一致
- **字体颜色**: 改为 `#ff3b30`（红色），与项目中其他红色元素（如 `.btn-danger`、`.stat-value.unavailable`）保持一致
- **边框**: 保持 `#b8dcff`，与背景色协调
- **悬停效果**: 保持原有的悬停状态样式，仅背景色和边框色微调

## 3. 影响范围

### 3.1 受影响的文件

| 文件路径 | 变更类型 | 说明 |
|---------|---------|------|
| `src/static/css/main.css` | 新增 | 添加 `.btn-export` 和 `.btn-export:hover` 样式 |
| `src/templates/tags.html` | 修改 | 更改两个按钮的 class 属性 |

### 3.2 不受影响的方面

- 按钮的点击功能和事件处理逻辑（JavaScript 不受影响）
- 其他按钮的样式
- 页面布局和响应式设计
- 后端 API

## 4. 测试计划

### 4.1 手动测试步骤

1. 启动应用，访问标签列表页面
2. 验证 "Export Protobuf" 按钮字体显示为红色
3. 验证 "Export CSV" 按钮字体显示为红色
4. 验证按钮背景色仍为浅蓝色
5. 验证鼠标悬停时按钮样式变化正常
6. 验证点击按钮仍能正常触发导出功能
7. 验证其他按钮样式未受影响

### 4.2 浏览器兼容性

- 使用标准 CSS 属性，兼容所有现代浏览器
- 已在项目现有 CSS 中使用相同的颜色值，无兼容性问题

## 5. 回滚方案

如需回滚，只需：
1. 删除 `main.css` 中添加的 `.btn-export` 样式
2. 将 `tags.html` 中按钮的类名改回 `btn-info`

## 6. 验收标准检查清单

- [ ] "Export Protobuf" 按钮的字体颜色为红色
- [ ] "Export CSV" 按钮的字体颜色为红色
- [ ] 按钮的其他样式（背景色、边框、悬停效果等）保持不变
- [ ] 按钮功能（点击导出）不受影响
