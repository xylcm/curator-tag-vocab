# Technical Plan: 导出按钮背景色修改为浅色

> Issue: #9
> PRD: docs/prds/issue-9.md
> Date: 2025-01-21

## 1. Approach

根据 PRD 要求，将导出按钮的背景色从蓝色（`.btn-info`）改为接近纯白色的柔和颜色（#fafafa）。

**方案选择**：
- **方案 A**: 修改 `.btn-info` 样式 — 会影响所有使用 `.btn-info` 的按钮
- **方案 B**: 为导出按钮添加新的 CSS 类 `.btn-export` — 仅影响导出按钮，不影响其他可能使用 `.btn-info` 的按钮

**采用方案 B**：为导出按钮创建独立的 `.btn-export` 样式类，这样可以：
1. 精确控制导出按钮的样式，不影响其他按钮
2. 未来如需调整导出按钮样式，无需担心副作用
3. 符合单一职责原则，样式语义更清晰

## 2. Changes

### New Files

无

### Modified Files

| File | Changes |
|------|---------|
| `src/static/css/main.css` | 添加 `.btn-export` 样式类，定义浅色背景、文字颜色和 hover 状态 |
| `src/templates/tags.html` | 将导出按钮的 `btn-info` 类改为 `btn-export` 类 |

## 3. Implementation Steps

1. **修改 `src/static/css/main.css`**
   - 在 `.btn-info` 样式之后添加 `.btn-export` 样式类
   - 背景色: #fafafa（接近纯白色的柔和颜色）
   - 文字颜色: #6e6e73（灰色，与浅色背景形成对比）
   - 边框: 1px solid #e0e0e0（与页面其他元素边框一致）
   - hover 状态: 背景色 #f0f0f0，边框色 #d0d0d0

2. **修改 `src/templates/tags.html`**
   - 将 `id="export-protobuf-btn"` 的按钮类从 `btn-info` 改为 `btn-export`
   - 将 `id="export-csv-btn"` 的按钮类从 `btn-info` 改为 `btn-export`

## 4. Testing Strategy

### Unit Tests

无（纯 UI 样式变更，不涉及业务逻辑）

### Integration Tests

无（纯 UI 样式变更，不涉及后端 API）

### Manual Verification

- [ ] 打开标签管理页面，确认「Export Protobuf」按钮显示为浅色背景（#fafafa）
- [ ] 确认「Export CSV」按钮显示为浅色背景（#fafafa）
- [ ] 鼠标悬停在导出按钮上，确认 hover 状态有视觉反馈
- [ ] 确认导出按钮文字颜色为 #6e6e73，清晰可读
- [ ] 确认「Load Tags」和「Add Tag」按钮保持原有蓝色/绿色样式不变
- [ ] 点击导出按钮，确认功能正常工作

## 5. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 新样式与页面其他元素不协调 | 低 | 选择 #fafafa 作为背景色，与页面整体浅灰色调保持一致；边框使用 #e0e0e0，与现有 `.btn-secondary` 样式一致 |
| hover 状态不够明显 | 低 | hover 背景色使用 #f0f0f0，比正常状态深一级，提供清晰的交互反馈 |
