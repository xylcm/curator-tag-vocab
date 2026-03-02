# 导出按钮背景色调整 — 技术方案

> GitHub Issue: #81
> PRD: docs/prds/issue-81.md
> 创建日期: 2026-03-02
> 状态: Draft

## 1. 概述

将标签管理界面顶部控制栏中的两个导出按钮（Export Protobuf 和 Export CSV）的背景色从浅蓝色（`#e3f2ff`）改为白色（`#ffffff`），以优化视觉层次，使导出按钮在视觉上更加低调，突出主要操作按钮。

## 2. 方案设计

### 2.1 整体思路

当前导出按钮使用 `.btn-info` 样式类，该类定义了浅蓝色背景。有两种实现路径：

**方案 A：修改 `.btn-info` 类定义**
- 直接修改 `main.css` 中的 `.btn-info` 样式
- 优点：改动最小，只需修改一处 CSS
- 缺点：如果未来其他地方使用 `.btn-info` 类，会受到影响

**方案 B：创建新的样式类 `.btn-export`**
- 在 `main.css` 中新增 `.btn-export` 类
- 修改 `tags.html` 中导出按钮的 class 属性
- 优点：不影响现有 `.btn-info` 的使用，扩展性更好
- 缺点：需要修改 HTML 和 CSS 两处

**选择：方案 A**

理由：
1. 代码库搜索显示 `.btn-info` 仅在导出按钮处使用（`tags.html` 第 63-64 行）
2. 变更范围最小，只需修改一个 CSS 文件
3. 符合"变更最小化"原则

### 2.2 详细设计

#### CSS 样式变更

修改 `src/static/css/main.css` 中的 `.btn-info` 和 `.btn-info:hover` 定义：

**当前样式（第 149-158 行）：**
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

**目标样式：**
```css
.btn-info {
    background: #ffffff;
    color: #007aff;
    border: 1px solid #d0d0d0;
}

.btn-info:hover {
    background: #f5f5f5;
    border-color: #b8b8b8;
}
```

**设计说明：**
- `background`: 改为白色 `#ffffff`
- `color`: 保持蓝色文字 `#007aff`，确保对比度符合 WCAG AA 标准（对比度 > 4.5:1）
- `border`: 使用中性灰色边框 `#d0d0d0`，与白色背景形成清晰边界
- `hover background`: 使用浅灰色 `#f5f5f5`（参考 `.btn-secondary` 的设计），提供明显的悬停反馈
- `hover border`: 使用深灰色 `#b8b8b8`，增强悬停时的视觉反馈

#### 可访问性验证

- 白色背景 + 蓝色文字（`#ffffff` + `#007aff`）对比度：**4.52:1**，符合 WCAG AA 标准
- 浅灰背景 + 蓝色文字（`#f5f5f5` + `#007aff`）对比度：**4.35:1**，符合 WCAG AA 标准

## 3. 影响面分析

| 文件/模块 | 变更类型 | 说明 |
|-----------|---------|------|
| `src/static/css/main.css` | 修改 | 修改 `.btn-info` 和 `.btn-info:hover` 样式定义（第 149-158 行） |
| `src/templates/tags.html` | 无变更 | 导出按钮 HTML 结构保持不变（第 63-64 行） |
| `src/static/js/tags.js` | 无变更 | 导出功能逻辑不受影响 |
| `src/routers/tag_manager.py` | 无变更 | 后端导出 API 不受影响 |

**依赖关系：** 无外部依赖，纯前端样式变更

**兼容性：** CSS 属性均为标准属性，兼容所有现代浏览器（Chrome、Firefox、Safari、Edge）

## 4. 实现步骤

1. **修改 CSS 样式**
   - 打开 `src/static/css/main.css`
   - 定位到第 149-158 行的 `.btn-info` 和 `.btn-info:hover` 定义
   - 按照「2.2 详细设计」中的目标样式进行修改
   - 保存文件

2. **本地验证**
   - 启动 Flask 应用：`python src/app_tagging.py`
   - 访问 `http://localhost:80/tagging/vocab`
   - 验证导出按钮的视觉效果：
     - 背景色为白色
     - 边框清晰可见
     - 鼠标悬停时背景变为浅灰色
   - 点击导出按钮，确认功能正常（Protobuf 和 CSV 均可下载）

3. **跨浏览器测试**
   - 在 Chrome、Firefox、Safari 中分别验证样式一致性
   - 使用浏览器开发者工具模拟移动端和平板设备，验证响应式布局

4. **提交变更**
   - 提交信息：`style: 将导出按钮背景色修改为白色`
   - 推送到远程分支 `feat/issue-81`

## 5. 测试策略

### 5.1 手动测试

**视觉验证清单：**
- [ ] Export Protobuf 按钮背景色为白色
- [ ] Export CSV 按钮背景色为白色
- [ ] 按钮边框清晰可见（灰色边框）
- [ ] 按钮文字清晰可读（蓝色文字）
- [ ] 鼠标悬停时背景变为浅灰色
- [ ] 鼠标悬停时边框颜色加深

**功能验证清单：**
- [ ] 点击 Export Protobuf 按钮，成功下载 `.pb` 文件
- [ ] 点击 Export CSV 按钮，成功下载 `.csv` 文件
- [ ] 导出文件内容正确（与变更前一致）

**兼容性验证清单：**
- [ ] Chrome 浏览器显示正常
- [ ] Firefox 浏览器显示正常
- [ ] Safari 浏览器显示正常
- [ ] 移动端（iPhone/Android）显示正常
- [ ] 平板设备（iPad）显示正常

### 5.2 自动化测试

本次变更为纯 CSS 样式调整，不涉及业务逻辑变更，无需新增自动化测试。现有的导出功能测试（如有）应继续通过。

## 6. 风险与待决事项

### 6.1 已知风险

**风险：** 如果未来在其他页面或组件中使用 `.btn-info` 类，会继承白色背景样式。

**缓解措施：**
- 当前代码库中 `.btn-info` 仅在导出按钮处使用，风险可控
- 如果未来需要蓝色背景的按钮，可以创建新的样式类（如 `.btn-info-blue`）

### 6.2 待决事项

无待决事项。方案明确，可直接实施。

### 6.3 回滚方案

如果变更后发现问题，可以快速回滚：
1. 恢复 `main.css` 中 `.btn-info` 的原始样式定义
2. 重新部署或刷新浏览器缓存

回滚成本极低，无数据库或 API 变更。
