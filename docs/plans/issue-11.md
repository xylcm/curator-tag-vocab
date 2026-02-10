# 技术方案：导出按钮背景颜色修改

> GitHub Issue: #11
> 关联 PRD: docs/prds/issue-11.md
> 创建日期: 2025-02-10

## 概述

本方案描述如何将导出按钮（Export Protobuf 和 Export CSV）的背景颜色修改为浅蓝色。

## 技术背景

### 当前实现
- 导出按钮使用 `.btn-info` CSS 类
- 当前样式定义在 `src/static/css/main.css` 中：
  ```css
  .btn-info {
      background: #e3f2ff;
      color: #007aff;
      border: 1px solid #b8dcff;
  }
  ```

### 按钮位置
- Export Protobuf 按钮：位于 `src/templates/tags.html` 的 controls 区域
- Export CSV 按钮：位于 `src/templates/tags.html` 的 controls 区域

## 技术方案

### 方案一：修改 `.btn-info` 样式（推荐）

直接修改 `.btn-info` 类的背景颜色为更明显的浅蓝色。

**优点：**
- 简单直接，只修改一处
- 所有使用 `.btn-info` 的按钮都会统一更新

**缺点：**
- 如果其他按钮也使用 `.btn-info` 类，会被一并修改

**实现步骤：**
1. 打开 `src/static/css/main.css`
2. 修改 `.btn-info` 的背景色为更明显的浅蓝色，例如 `#b3d9ff`
3. 相应调整悬停状态的背景色为 `#9cceff`

### 方案二：为导出按钮添加专属类

为导出按钮添加 `.btn-export` 专属类，单独设置样式。

**优点：**
- 不影响其他使用 `.btn-info` 的按钮
- 更精细的控制

**缺点：**
- 需要修改 HTML 和 CSS 两处
- 对于当前需求略显过度设计

## 最终决策

采用**方案一**：修改 `.btn-info` 样式。

理由：
1. 当前项目中 `.btn-info` 仅用于导出按钮
2. 修改简单，风险低
3. 符合 PRD 需求

## 具体修改

### 文件：`src/static/css/main.css`

**修改前：**
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

**修改后：**
```css
.btn-info {
    background: #b3d9ff;
    color: #007aff;
    border: 1px solid #8ac5ff;
}

.btn-info:hover {
    background: #9cceff;
    border-color: #73b8ff;
}
```

## 验收标准检查清单

- [ ] `.btn-info` 背景颜色修改为 `#b3d9ff`（更明显的浅蓝色）
- [ ] `.btn-info:hover` 悬停状态颜色相应调整
- [ ] 按钮文字颜色保持 `#007aff` 确保对比度
- [ ] Export Protobuf 按钮显示新的背景色
- [ ] Export CSV 按钮显示新的背景色

## 风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 颜色对比度不足 | 低 | 中 | 使用 WCAG 对比度检查工具验证 |
| 与其他按钮样式冲突 | 低 | 低 | 确认 `.btn-info` 仅用于导出按钮 |

## 测试计划

1. 视觉检查：确认导出按钮背景色已变为更明显的浅蓝色
2. 悬停测试：确认鼠标悬停时颜色变化正常
3. 对比度检查：确认文字与背景对比度符合可读性标准
