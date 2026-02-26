# 导出按钮背景色调整

> GitHub Issue: #48
> 创建日期: 2025-01-21
> 状态: Draft

## 概述
将导出按钮（Export Protobuf 和 Export CSV）的背景色从当前的蓝色调整为更浅的颜色，以改善视觉层次和界面一致性。

## 当前行为
- 导出按钮（Export Protobuf、Export CSV）使用 `btn-info` 样式
- 背景色为浅蓝色（#e3f2ff），文字颜色为蓝色（#007aff）
- 与主操作按钮（Load Tags 的 `btn-primary`）视觉上难以区分

## 期望行为
- 导出按钮使用更浅的背景色，降低视觉权重
- 与主操作按钮形成清晰的视觉层次
- 建议改为使用 `btn-secondary` 样式（灰色系：背景 #f5f5f5，文字 #6e6e73）

## 验收标准
- [ ] Export Protobuf 按钮背景色调整为浅色（如灰色系）
- [ ] Export CSV 按钮背景色调整为浅色（如灰色系）
- [ ] 按钮 hover 状态保持正常的交互反馈
- [ ] 按钮文字保持清晰可读
