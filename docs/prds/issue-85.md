# PRD: 页面视觉样式调整 - 下载按钮位置和样式

## 关联 Issue
- Issue: #85
- Figma 设计稿: https://www.figma.com/design/YrPkyRO7owyGGO9iWGJs4M/Curator-Tag-Vocabulary---Admin-Panel?node-id=1-4157

---

## 1. 需求概述

调整标签管理页面的下载按钮（Export Protobuf 和 Export CSV）的位置和样式，使其符合新的视觉设计规范。

---

## 2. 现状分析

### 2.1 当前布局
当前所有按钮都在同一行排列：
- Search tags... (输入框)
- Deleted 筛选下拉框
- Filter 筛选下拉框
- Category 筛选下拉框
- Sort 排序下拉框
- Order 排序下拉框
- Load Tags 按钮
- Add Tag 按钮
- Export Protobuf 按钮
- Export CSV 按钮

### 2.2 当前样式
Export 按钮当前使用 `.btn-info` 类：
- 背景色: `#e3f2ff`
- 文字颜色: `#007aff`
- 边框: `1px solid #b8dcff`

---

## 3. 目标设计

### 3.1 布局调整
将控制区域分为两行：

**第一行（筛选控制区）**：
- Search tags... (输入框)
- Deleted 筛选下拉框
- Filter 筛选下拉框
- Category 筛选下拉框
- Sort 排序下拉框
- Order 排序下拉框
- Load Tags 按钮
- Add Tag 按钮

**第二行（导出按钮区）**：
- Export Protobuf 按钮
- Export CSV 按钮

### 3.2 样式调整

#### Export Protobuf 按钮
| 属性 | 当前值 | 目标值 |
|------|--------|--------|
| 背景色 | `#e3f2ff` | `#f7ff07` (亮黄色) |
| 文字颜色 | `#007aff` | `#007aff` (保持不变) |
| 边框 | `1px solid #b8dcff` | `1px solid #d4dae0` |
| 圆角 | `6px` | `6px` (保持不变) |
| 内边距 | `10px 20px` | `11px 21px` |
| 字体大小 | `14px` | `14px` (保持不变) |

#### Export CSV 按钮
| 属性 | 当前值 | 目标值 |
|------|--------|--------|
| 背景色 | `#e3f2ff` | `#f7ff07` (亮黄色) |
| 文字颜色 | `#007aff` | `#007aff` (保持不变) |
| 边框 | `1px solid #b8dcff` | `1px solid rgba(238,255,184,0.69)` |
| 圆角 | `6px` | `6px` (保持不变) |
| 内边距 | `10px 20px` | `11px 21px` |
| 字体大小 | `14px` | `14px` (保持不变) |

---

## 4. 技术实现要点

### 4.1 HTML 结构调整
- 将 `.controls` 容器内的按钮重新分组
- 创建两个子容器：`.controls-row-primary` 和 `.controls-row-secondary`
- 或使用 flex 布局的 `flex-wrap` 配合适当的间距实现换行

### 4.2 CSS 样式新增
- 新增 `.btn-export` 类用于导出按钮的黄色样式
- 确保新样式与现有按钮样式保持一致的 hover 和 active 状态

### 4.3 响应式考虑
- 确保在移动端第二行按钮也能正确换行显示
- 保持与现有响应式断点的一致性

---

## 5. 验收标准

- [ ] Export Protobuf 和 Export CSV 按钮显示在第二行
- [ ] 按钮背景色为亮黄色 (#f7ff07)
- [ ] 按钮边框颜色符合设计规范
- [ ] 按钮内边距调整为 11px 21px
- [ ] 按钮 hover 和 active 状态正常
- [ ] 移动端显示正常

---

## 6. 非功能性需求

- **兼容性**: 保持与现有浏览器兼容性一致
- **性能**: 纯样式调整，无性能影响
- **可访问性**: 保持按钮的可点击性和键盘导航支持
