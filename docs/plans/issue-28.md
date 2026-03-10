# 导出按钮背景色修改技术方案

> GitHub Issue: #28
> 关联 PRD: docs/prds/issue-28.md
> 创建日期: 2026-02-11

## 1. 概述

将标签管理页面中导出按钮（Export Protobuf、Export CSV）的背景颜色从蓝色修改为白色。

## 2. 技术现状分析

### 2.1 当前实现

导出按钮位于 `src/templates/tags.html` 第 63-64 行：

```html
<button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-info" id="export-csv-btn">Export CSV</button>
```

### 2.2 当前样式

按钮使用 `.btn-info` 类，定义在 `src/static/css/main.css` 第 149-158 行：

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

### 2.3 其他按钮样式

- `.btn-primary`（Load Tags）：浅蓝背景 `#e3f2ff`
- `.btn-success`（Add Tag）：浅绿背景 `#e8f8ec`

## 3. 技术方案

### 3.1 方案选择

**方案一：修改 `.btn-info` 类（推荐）**

直接修改 `.btn-info` 类的样式，影响所有使用该类的按钮。

**方案二：新增专用类**

为导出按钮新增 `.btn-export` 类，保持 `.btn-info` 不变。

**决策**：选择方案一，因为：
1. 当前只有导出按钮使用 `.btn-info` 类
2. 需求明确要求将导出按钮改为白色背景
3. 方案一改动最小，风险最低

### 3.2 具体修改

修改文件：`src/static/css/main.css`

将 `.btn-info` 样式从：

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

修改为：

```css
.btn-info {
    background: #ffffff;
    color: #007aff;
    border: 1px solid #b8dcff;
}

.btn-info:hover {
    background: #f5f5f7;
    border-color: #b8dcff;
}
```

### 3.3 样式变更对照表

| 属性 | 当前值 | 新值 |
|------|--------|------|
| 背景色 | `#e3f2ff` | `#ffffff` |
| 文字颜色 | `#007aff` | `#007aff`（不变） |
| 边框颜色 | `#b8dcff` | `#b8dcff`（不变） |
| 悬停背景色 | `#d0e8ff` | `#f5f5f7` |
| 悬停边框颜色 | `#9fceff` | `#b8dcff`（不变） |

## 4. 验收标准验证

- [ ] "Export Protobuf" 按钮背景色为 `#ffffff`（白色）
- [ ] "Export CSV" 按钮背景色为 `#ffffff`（白色）
- [ ] 按钮文字颜色保持 `#007aff`（蓝色）
- [ ] 按钮边框颜色为 `#b8dcff`（浅蓝色）
- [ ] 悬停状态背景色为 `#f5f5f7`（浅灰色）
- [ ] Load Tags 按钮（`.btn-primary`）样式不受影响
- [ ] Add Tag 按钮（`.btn-success`）样式不受影响

## 5. 风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 其他页面使用 `.btn-info` 类 | 低 | 中 | 全局搜索确认只有导出按钮使用 |
| 样式优先级冲突 | 低 | 低 | 保持选择器简单，避免嵌套 |

## 6. 实施步骤

1. 修改 `src/static/css/main.css` 中的 `.btn-info` 样式
2. 本地验证按钮显示效果
3. 确认其他按钮样式未受影响
4. 提交代码
