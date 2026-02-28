# PRD: 导出按钮背景色修改

## 需求概述

将导出按钮（Export Protobuf 和 Export CSV）的背景色从当前的浅蓝色修改为浅白色。

## 当前状态

- **位置**: `src/templates/tags.html` 第 63-64 行
- **当前样式**: 使用 `btn-info` 类，背景色为 `#e3f2ff`（浅蓝色）
- **涉及按钮**:
  - Export Protobuf 按钮
  - Export CSV 按钮

## 目标状态

- **目标背景色**: 浅白色（如 `#f5f5f5` 或 `#fafafa`）
- **样式类**: 使用 `btn-secondary` 类或自定义样式

## 视觉设计

### 当前样式
```css
.btn-info {
    background: #e3f2ff;
    color: #007aff;
    border: 1px solid #b8dcff;
}
```

### 目标样式
```css
.btn-secondary {
    background: #f5f5f5;
    color: #6e6e73;
    border: 1px solid #e0e0e0;
}
```

## 验收标准

1. Export Protobuf 按钮背景色显示为浅白色
2. Export CSV 按钮背景色显示为浅白色
3. 按钮文字颜色与背景色有足够对比度，确保可读性
4. 按钮悬停效果正常工作

## 影响范围

- **文件**: `src/templates/tags.html`
- **行号**: 第 63-64 行
- **变更类型**: 将 `btn-info` 类改为 `btn-secondary` 类

## 兼容性

- 无破坏性变更
- 与其他按钮样式保持一致
- 不影响现有功能
