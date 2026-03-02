# 导出按钮背景色调整 — 技术方案

> GitHub Issue: #83
> PRD: docs/prds/issue-83.md
> 创建日期: 2026-03-02
> 状态: Draft

## 1. 概述

将标签词汇管理页面顶部的两个导出按钮（Export Protobuf 和 Export CSV）的背景色从浅蓝色改为浅白色/浅灰色，降低视觉权重，使其与页面整体风格更协调。

## 2. 方案设计

### 2.1 整体思路

当前导出按钮使用 `.btn-info` 样式类，该类定义了浅蓝色背景（`#e3f2ff`），与主操作按钮 `.btn-primary` 颜色相同，导致视觉层级不清晰。

**实现方案**：修改 `.btn-info` 类的样式定义，将背景色改为浅白色/浅灰色，参考现有 `.btn-secondary` 的配色方案（`#f5f5f5` 背景，`#e0e0e0` 边框）。

**方案选择理由**：
- `.btn-info` 在代码库中仅用于两个导出按钮，修改该类不会影响其他组件
- 复用现有样式类，避免引入新的 CSS 类名，保持代码简洁
- 参考 `.btn-secondary` 的配色，确保与现有设计系统一致

### 2.2 详细设计

#### 修改前（当前样式）

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

#### 修改后（目标样式）

```css
.btn-info {
    background: #f5f5f5;
    color: #6e6e73;
    border: 1px solid #e0e0e0;
}

.btn-info:hover {
    background: #e8e8e8;
    border-color: #d0d0d0;
}
```

**配色说明**：
- 背景色：`#f5f5f5`（浅灰色，与 `.btn-secondary` 一致）
- 文字色：`#6e6e73`（深灰色，确保可读性）
- 边框色：`#e0e0e0`（浅灰边框）
- Hover 背景：`#e8e8e8`（稍深的灰色，提供交互反馈）
- Hover 边框：`#d0d0d0`（稍深的边框）

**对比度验证**：
- 文字色 `#6e6e73` 与背景色 `#f5f5f5` 的对比度约为 4.6:1，满足 WCAG AA 标准（要求 ≥ 4.5:1）

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/static/css/main.css` | 修改 | 修改 `.btn-info` 和 `.btn-info:hover` 的样式定义（第 149-158 行） |
| `src/templates/tags.html` | 无变更 | HTML 结构和类名保持不变 |
| `src/routers/tag_manager.py` | 无变更 | 后端逻辑不受影响 |
| `src/static/js/tags.js` | 无变更 | JavaScript 交互逻辑不受影响 |

**影响范围**：
- 仅影响两个导出按钮的视觉样式
- 不影响按钮的功能行为（点击导出仍正常工作）
- 不影响其他按钮样式（`.btn-primary`、`.btn-success`、`.btn-secondary` 等）

## 4. 实现步骤

1. **修改 CSS 样式**
   - 打开 `src/static/css/main.css`
   - 定位到第 149-158 行的 `.btn-info` 和 `.btn-info:hover` 定义
   - 将背景色、文字色、边框色替换为目标配色

2. **本地验证**
   - 启动应用：`python src/app_tagging.py`
   - 访问 `http://localhost:80/tagging/vocab`
   - 检查导出按钮的视觉效果：
     - 背景色为浅灰色
     - 文字清晰可读
     - Hover 状态有明显反馈
     - 其他按钮样式未受影响

3. **功能测试**
   - 点击 "Export Protobuf" 按钮，验证文件下载正常
   - 点击 "Export CSV" 按钮，验证文件下载正常

## 5. 测试策略

### 视觉回归测试
- **测试内容**：在浏览器中打开页面，目视检查按钮样式
- **验证点**：
  - 导出按钮背景色为浅灰色（`#f5f5f5`）
  - 文字颜色为深灰色（`#6e6e73`），清晰可读
  - Hover 状态背景色变为 `#e8e8e8`
  - 其他按钮（Load Tags、Add Tag）样式不变

### 功能测试
- **测试内容**：点击导出按钮，验证导出功能正常
- **验证点**：
  - 点击 "Export Protobuf" 能下载 `.pb` 文件
  - 点击 "Export CSV" 能下载 `.csv` 文件
  - 文件内容正确（与修改前一致）

### 响应式测试
- **测试内容**：在不同屏幕尺寸下检查按钮样式
- **验证点**：
  - 桌面端（> 768px）：按钮正常显示
  - 平板端（480px - 768px）：按钮正常显示
  - 移动端（< 480px）：按钮正常显示

## 6. 风险与待决事项

### 风险评估

**低风险**：
- 变更范围极小，仅修改一个 CSS 类的样式属性
- `.btn-info` 在代码库中仅用于两个导出按钮，无其他依赖
- 不涉及 HTML 结构、JavaScript 逻辑或后端代码
- 配色参考现有 `.btn-secondary`，与设计系统一致

### 待决事项

无。方案明确，无需进一步决策。

### 回滚方案

如需回滚，只需将 `src/static/css/main.css` 中的 `.btn-info` 样式恢复为原值：

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
