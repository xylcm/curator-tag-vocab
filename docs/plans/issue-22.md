# 技术方案：导出按钮背景颜色修改

## 需求概述

将导出按钮（Export Protobuf 和 Export CSV）的背景颜色从蓝色改为白色，以提升界面协调性。

## 现状分析

当前导出按钮使用 `.btn-info` 样式类，其 CSS 定义如下：

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

该样式使按钮呈现浅蓝色背景，与整体界面风格不够协调。

## 技术实现方案

### 方案选择

采用**修改现有样式类**的方案，直接更新 `.btn-info` 的样式定义。

**理由**：
- `.btn-info` 类仅用于导出按钮（Export Protobuf 和 Export CSV），无其他用途
- 修改样式类比修改 HTML 结构更简单、风险更低
- 保持代码一致性，避免引入新的样式类

### 具体变更

修改文件：`src/static/css/main.css`

将 `.btn-info` 的样式从蓝色主题改为白色主题：

| 状态 | 背景色 | 文字色 | 边框色 |
|------|--------|--------|--------|
| 默认 | `#ffffff` | `#007aff` | `#d0d0d0` |
| Hover | `#f5f5f7` | `#007aff` | `#b0b0b0` |

### CSS 变更详情

```css
/* 修改前 */
.btn-info {
    background: #e3f2ff;
    color: #007aff;
    border: 1px solid #b8dcff;
}

.btn-info:hover {
    background: #d0e8ff;
    border-color: #9fceff;
}

/* 修改后 */
.btn-info {
    background: #ffffff;
    color: #007aff;
    border: 1px solid #d0d0d0;
}

.btn-info:hover {
    background: #f5f5f7;
    border-color: #b0b0b0;
}
```

## 影响范围

- **受影响元素**：Export Protobuf 按钮、Export CSV 按钮
- **文件变更**：`src/static/css/main.css`（仅 6 行样式变更）
- **无 JavaScript 变更**
- **无 HTML 结构变更**
- **无后端 API 变更**

## 测试验证

1. **视觉验证**：
   - 导出按钮默认状态显示白色背景
   - 鼠标悬停时背景变为浅灰色
   - 文字保持蓝色，与界面其他蓝色元素协调

2. **功能验证**：
   - 点击导出按钮功能正常
   - 导出流程不受样式变更影响

## 回滚方案

如需回滚，只需将 CSS 代码恢复为修改前的状态即可。

## 实施步骤

1. 修改 `src/static/css/main.css` 中的 `.btn-info` 和 `.btn-info:hover` 样式
2. 本地验证样式效果
3. 提交并推送变更
