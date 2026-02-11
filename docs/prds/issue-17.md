# 导出按钮背景颜色修改

> GitHub Issue: #17
> 创建日期: 2026-02-11
> 状态: Draft

## 概述
将导出按钮（Export Protobuf 和 Export CSV）的背景颜色从当前的蓝色（btn-info 样式）修改为绿色，以提升视觉区分度，让用户更容易识别导出功能。

## 当前行为
- 页面顶部控制栏有两个导出按钮："Export Protobuf" 和 "Export CSV"
- 这两个按钮当前使用 `btn-info` 样式，显示为蓝色背景（#e3f2ff）和蓝色文字（#007aff）
- 与旁边的 "Load Tags"（蓝色）和 "Add Tag"（绿色）按钮相比，导出按钮的视觉区分度不够明显

## 期望行为
- Export Protobuf 和 Export CSV 按钮的背景颜色改为绿色
- 使用与 "Add Tag" 按钮相同的绿色样式（`btn-success`）：
  - 背景色：#e8f8ec（悬停时 #d4f2dc）
  - 文字色：#34c759
  - 边框色：#d4f2dc（悬停时 #c0ecc8）

## 验收标准
- [ ] Export Protobuf 按钮显示为绿色背景
- [ ] Export CSV 按钮显示为绿色背景
- [ ] 按钮悬停效果正常工作（背景色变深）
- [ ] 按钮文字颜色为绿色（#34c759）
- [ ] 与其他按钮保持一致的间距和对齐
