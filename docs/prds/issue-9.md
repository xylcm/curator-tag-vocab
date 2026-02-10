# 导出按钮背景色修改为浅色

> GitHub Issue: #9
> 创建日期: 2025-01-21
> 状态: Draft

## 概述

将标签管理页面中「Export Protobuf」和「Export CSV」两个导出按钮的背景色从当前的蓝色改为浅色，使界面视觉层次更加清晰，导出按钮与主要操作按钮（Load Tags、Add Tag）形成视觉区分。

## 当前行为

- 「Export Protobuf」和「Export CSV」按钮使用 `.btn-info` 样式
- 按钮背景色为浅蓝色（#e3f2ff），文字为蓝色（#007aff）
- 导出按钮与「Load Tags」按钮视觉上难以区分优先级

## 期望行为

- 导出按钮背景色改为纯白色（#ffffff）
- 导出按钮视觉上从属于主要操作按钮
- 保持按钮的可点击性和可读性

## 验收标准

- [ ] 「Export Protobuf」按钮背景色改为纯白色（#ffffff）
- [ ] 「Export CSV」按钮背景色改为纯白色（#ffffff）
- [ ] 按钮文字颜色保持清晰可见（建议使用 #6e6e73）
- [ ] 按钮 hover 状态保持适当的视觉反馈
- [ ] 按钮边框样式与整体设计风格保持一致
