# 导出按钮位置和样式调整

> GitHub Issue: #93
> 创建日期: 2026-03-04
> 状态: Draft

## 概述

根据 Figma 视觉稿调整导出按钮的位置和样式。将导出按钮从第一行控件区域移至第二行，并更新按钮背景色为黄色（#f7ff07），使界面布局更清晰，导出功能更突出。

## 当前行为

- 导出按钮（"Export Protobuf" 和 "Export CSV"）位于控件区域的第一行，与搜索框、筛选器、"Load Tags" 和 "Add Tag" 按钮在同一行
- 按钮使用 `.btn-info` 样式，背景色为浅蓝色（#e3f2ff）
- 当控件较多时，第一行空间拥挤，用户体验不佳

## 期望行为

- 导出按钮移至控件区域第二行，位于 "Load Tags" 和 "Add Tag" 按钮下方
- 按钮背景色更新为黄色（#f7ff07），边框颜色为 #d4dae0（Protobuf）和 rgba(238,255,184,0.69)（CSV）
- 按钮文字颜色保持蓝色（#007aff）
- 保持按钮原有功能和交互行为

## 视觉参考

参考 Figma 设计稿：https://www.figma.com/design/YrPkyRO7owyGGO9iWGJs4M/Curator-Tag-Vocabulary---Admin-Panel?node-id=1-4157

设计稿显示：
- 第一行：搜索框、筛选下拉框、Load Tags 按钮、Add Tag 按钮
- 第二行：Export Protobuf 按钮（黄色背景）、Export CSV 按钮（黄色背景）

## 验收标准

- [ ] "Export Protobuf" 和 "Export CSV" 按钮从第一行移至第二行
- [ ] 按钮背景色改为黄色（#f7ff07）
- [ ] Export Protobuf 按钮边框颜色为 #d4dae0
- [ ] Export CSV 按钮边框颜色为 rgba(238,255,184,0.69)
- [ ] 按钮文字颜色保持 #007aff
- [ ] 按钮点击功能和导出行为保持不变
- [ ] 响应式布局在移动端正常显示
