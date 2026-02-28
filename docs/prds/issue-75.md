# PRD: 导出按钮背景色修改为淡黄色

## Issue 信息
- **Issue**: #75
- **标题**: 将导出按钮的背景色修改为淡黄色
- **类型**: UI 优化

## 需求概述

将标签管理页面中的两个导出按钮（"Export Protobuf" 和 "Export CSV"）的背景色从当前的浅蓝色修改为淡黄色，以提升视觉识别度和用户体验。

## 当前状态

### 按钮位置
位于 `src/templates/tags.html` 第 63-64 行：
```html
<button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-info" id="export-csv-btn">Export CSV</button>
```

### 当前样式
位于 `src/static/css/main.css` 第 149-158 行：
```css
.btn-info {
    background: #e3f2ff;
    color: #007aff;
    border: 1px solid #b8dcff;
}

.btn-info:hover {
    background: #d0e8ff;
    border-color: #9fceff;
}
```

当前 `.btn-info` 类使用浅蓝色配色方案（background: #e3f2ff）。

## 需求详情

### 目标
将导出按钮的背景色从浅蓝色改为淡黄色，使导出功能在视觉上更加突出，便于用户快速识别。

### 配色方案建议

采用淡黄色系，与现有按钮风格保持一致：

| 状态 | 背景色 | 文字色 | 边框色 |
|------|--------|--------|--------|
| 默认 | `#fff8e1` | `#f9a825` | `#ffecb3` |
| Hover | `#ffecb3` | `#f9a825` | `#ffe082` |

### 变更范围

仅修改 `src/static/css/main.css` 中的 `.btn-info` 类样式，不涉及：
- HTML 结构变更
- JavaScript 逻辑变更
- 其他按钮样式变更
- 功能逻辑变更

## 验收标准

- [ ] "Export Protobuf" 按钮显示为淡黄色背景
- [ ] "Export CSV" 按钮显示为淡黄色背景
- [ ] 按钮 hover 状态显示为深一点的淡黄色
- [ ] 按钮文字颜色与背景对比度良好，易于阅读
- [ ] 不影响其他使用 `.btn-info` 类的元素（如有）
- [ ] 响应式布局不受影响

## 技术约束

- 保持现有 CSS 类结构（`.btn-info`）
- 保持现有设计系统的一致性（圆角、阴影、过渡动画等）
- 确保颜色对比度符合可访问性标准

## 相关文件

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `src/static/css/main.css` | 修改 | 更新 `.btn-info` 样式定义 |

## 备注

这是一个纯 UI 样式变更，不涉及功能修改，风险较低。
