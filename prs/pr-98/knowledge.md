# PR #98 Knowledge Document

## Status

**当前阶段**: stage:planning (技术方案) - 已完成，等待人工审核
**已完成**: PRD 文档、技术方案
**下一步**: 等待技术方案审核通过后，进入 stage:implementation 编码实现

## Task Code Map

### 涉及文件

| 文件 | 作用 | 变更预期 |
|------|------|----------|
| `src/templates/tags.html` | 主页面模板 | 调整导出按钮位置 |
| `src/static/css/main.css` | 样式文件 | 添加 header 右侧布局样式 |
| `src/static/js/tags.js` | 前端交互逻辑 | 无需修改，按钮 ID 保持不变 |

### 关键代码区域

**当前导出按钮位置** (`tags.html` 第 63-64 行):
```html
<button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
<button class="btn btn-info" id="export-csv-btn">Export CSV</button>
```

位于 `.controls` div 内，与搜索、筛选按钮在同一行。

**目标位置**: `.header` div 内，与标题 `<h1>` 同级，靠右对齐。

**技术方案中的新结构**:
```html
<div class="header-main">
    <h1>Curator Tag Vocabulary</h1>
    <div class="header-actions">
        <!-- 导出按钮移至此处 -->
    </div>
</div>
```

## Decisions & Rejected Alternatives

### 技术方案决策

**选择方案**: 使用 `.header-main` 容器包裹标题和按钮组
- 采用 flex 布局 `justify-content: space-between` 实现左右分布
- 新增 `.header-actions` 容器专门放置导出按钮
- 保持按钮原有 `btn-info` 样式不变

**未考虑的替代方案**:
- 使用 absolute positioning（需要处理响应式适配，更复杂）
- 将按钮放在 stats 区域右侧（视觉层级不匹配）

## Cross-Stage Notes

### 来自 PRD 的约束

1. **视觉样式**: 必须保持 `btn-info` 类，维持原有按钮外观
2. **交互行为**: 点击后的加载状态和提示保持不变
3. **响应式**: 在常见屏幕分辨率下布局正常显示
4. **功能完整性**: 其他功能（搜索、筛选、添加标签）不受影响

### 技术实现提示

- 按钮 ID 保持不变 (`export-protobuf-btn`, `export-csv-btn`)，JS 事件绑定无需修改
- 需要调整 `.header h1` 的 margin-bottom，将其移至父容器 `.header-main`
- 移动端需添加响应式样式，使按钮在窄屏幕下垂直排列

## Non-Obvious Discoveries

- 当前 `.header` 没有使用 flex 布局，标题和统计信息是块级堆叠
- 导出功能通过 JS 事件监听实现，只要保持按钮 ID 不变，功能不受影响
- `.controls` 区域使用 sticky 定位，移除按钮后需要确认布局仍正常
