# 导出按钮背景色修改 — 技术方案

> GitHub Issue: #75
> PRD: docs/prds/issue-75.md
> 创建日期: 2025-01-20
> 状态: Draft

## 1. 概述

根据 PRD 要求，将标签管理页面中两个导出按钮（"Export Protobuf" 和 "Export CSV"）的背景色从浅蓝色（`#e3f2ff`）修改为淡黄色（`#fff8e1`），以提升视觉识别度和用户体验。

## 2. 方案设计

### 2.1 整体思路

这是一个纯 CSS 样式变更，只需修改 `.btn-info` 类的颜色定义。导出按钮使用 `btn-info` 类，通过更新该类的配色方案即可实现需求。

### 2.2 详细设计

#### 颜色变更对照表

**根据审核反馈，仅修改背景色，保持文字色和边框色不变。**

| 状态 | 属性 | 当前值 | 新值 | 是否变更 |
|------|------|--------|------|----------|
| 默认 | 背景色 | `#e3f2ff`（浅蓝） | `#fff8e1`（淡黄） | ✅ 是 |
| 默认 | 文字色 | `#007aff`（蓝色） | `#007aff`（蓝色） | ❌ 否 |
| 默认 | 边框色 | `#b8dcff`（浅蓝） | `#b8dcff`（浅蓝） | ❌ 否 |
| Hover | 背景色 | `#d0e8ff`（浅蓝） | `#ffecb3`（浅黄） | ✅ 是 |
| Hover | 边框色 | `#9fceff`（浅蓝） | `#9fceff`（浅蓝） | ❌ 否 |

#### CSS 变更详情

**文件**: `src/static/css/main.css`

**当前代码**（第 149-158 行）：
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

**变更后代码**（仅修改背景色）：
```css
.btn-info {
    background: #fff8e1;
    color: #007aff;
    border: 1px solid #b8dcff;
}

.btn-info:hover {
    background: #ffecb3;
    border-color: #9fceff;
}
```

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/static/css/main.css` | 修改 | 更新 `.btn-info` 类样式定义（第 149-158 行） |

**影响范围评估**：
- 仅影响使用 `.btn-info` 类的元素
- 根据代码库分析，`.btn-info` 仅用于导出按钮（"Export Protobuf" 和 "Export CSV"）
- 无其他功能或样式受影响

## 4. 实现步骤

1. **修改 CSS 文件**
   - 打开 `src/static/css/main.css`
   - 定位到第 149-158 行的 `.btn-info` 和 `.btn-info:hover` 定义
   - 按照详细设计中的颜色值进行替换

2. **本地验证**
   - 启动 Flask 应用
   - 访问标签管理页面
   - 确认导出按钮显示为淡黄色背景
   - 确认 hover 状态显示为深一点的淡黄色
   - 确认文字颜色与背景对比度良好

## 5. 测试策略

- **视觉测试**: 在浏览器中验证按钮颜色显示正确
- **交互测试**: 验证 hover 状态颜色变化正常
- **对比度测试**: 确认文字颜色 `#007aff` 在背景 `#fff8e1` 上可读性良好（蓝色文字在淡黄色背景上）
- **回归测试**: 确认其他按钮样式（`.btn-primary`, `.btn-success`, `.btn-danger`, `.btn-secondary`）未受影响

## 6. 风险与待决事项

**风险**: 极低
- 纯 CSS 样式变更，无功能影响
- 仅修改颜色值，无结构变更

**待决事项**: 无
- 颜色方案已在 PRD 中确认
