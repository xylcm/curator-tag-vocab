# 导出按钮布局和样式调整

> GitHub Issue: #31
> 创建日期: 2025-01-21
> 状态: Draft

## 概述

将导出按钮（Export Protobuf、Export CSV）从控制栏区域移动到页面右上角，与标题 "Curator Tag Vocabulary" 水平对齐并靠右展示，使页面布局更加清晰合理。

## 当前行为

导出按钮（Export Protobuf、Export CSV）位于页面中部的控制栏区域（`.controls`），与其他操作按钮（Load Tags、Add Tag）以及搜索、筛选、排序控件混在一起。这种布局使得：

- 导出功能与数据操作功能混杂，视觉层次不清晰
- 导出按钮作为次要功能，占用了主要操作区域的空间
- 页面顶部标题区域右侧留白，空间利用不充分

## 期望行为

导出按钮移动到页面右上角，与标题 "Curator Tag Vocabulary" 水平对齐：

- **位置**：页面右上角，与标题同一水平线
- **对齐方式**：靠右展示，与标题形成左右分布
- **按钮顺序**：Export Protobuf 在前，Export CSV 在后（或根据视觉需求调整）
- **视觉风格**：保持现有的按钮样式（btn-info）

目标效果示意：

```
┌─────────────────────────────────────────────────────────────┐
│  Curator Tag Vocabulary                    [Export Proto] [Export CSV]  │
│  Total: 100  Available: 80  Unavailable: 15  Deleted: 5     │
├─────────────────────────────────────────────────────────────┤
│  [Search...] [Deleted▼] [Filter▼] [Category▼] [Sort▼] [Order▼] [Load] [Add] │
```

## 验收标准

- [ ] 导出按钮（Export Protobuf、Export CSV）显示在页面右上角
- [ ] 导出按钮与标题 "Curator Tag Vocabulary" 水平对齐
- [ ] 导出按钮靠右展示，与标题形成左右分布布局
- [ ] 原控制栏区域不再显示导出按钮
- [ ] 导出按钮保持原有的视觉样式和交互功能
- [ ] 响应式布局适配：在较小屏幕尺寸下，按钮布局合理不重叠
