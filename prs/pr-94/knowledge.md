# PR #94 Knowledge Document

## Task Code Map

### Relevant Files for Export Button Changes

| File | Purpose | What to Change |
|------|---------|----------------|
| `src/templates/tags.html` | 主页面模板 | 调整导出按钮 HTML 结构，从第一行移至第二行 |
| `src/static/css/main.css` | 样式文件 | 新增/修改导出按钮样式类（黄色背景等） |

### Current Button Structure (tags.html)
```html
<div class="controls-wrapper">
    <div class="controls">
        <!-- 第一行：搜索、筛选、Load Tags、Add Tag -->
        <input type="text" id="search-input" ...>
        <select id="deleted-select">...</select>
        <select id="filter-select">...</select>
        <select id="category-select">...</select>
        <select id="sort-select">...</select>
        <select id="order-select">...</select>
        <button class="btn btn-primary" id="load-btn">Load Tags</button>
        <button class="btn btn-success" id="add-btn">Add Tag</button>
        <!-- 当前导出按钮在第一行 -->
        <button class="btn btn-info" id="export-protobuf-btn">Export Protobuf</button>
        <button class="btn btn-info" id="export-csv-btn">Export CSV</button>
    </div>
</div>
```

### Current Button Styles (main.css)
- `.btn-info` 类定义：背景色 #e3f2ff，边框 #b8dcff，文字 #007aff
- 需要新增 `.btn-export` 类或修改现有类实现黄色样式

## Non-Obvious Discoveries

### Figma 设计稿细节
- Export Protobuf 按钮边框：#d4dae0
- Export CSV 按钮边框：rgba(238,255,184,0.69)（注意是半透明）
- 两个按钮背景色相同：#f7ff07
- 按钮位置在第二行，与第一行按钮水平对齐（left: 1098.5px 和 1249.5px）

### 布局考虑
- 当前 `.controls` 使用 `flex-wrap: wrap`，按钮会自动换行
- 但导出按钮需要明确在第二行，可能需要结构调整（如两个 controls 容器或嵌套结构）

## Decisions & Rejected Alternatives

### 布局方案选择
| 方案 | 描述 | 状态 |
|------|------|------|
| 单容器 flex-wrap | 依赖自动换行 | ❌ 不精确控制 |
| 两个 controls 容器 | 第一行和第二行分开 | ✅ 推荐 |
| 嵌套 div | 在第一行内嵌套第二行 | ❌ 结构复杂 |

### 样式方案选择
| 方案 | 描述 | 状态 |
|------|------|------|
| 修改 .btn-info | 直接改现有类 | ❌ 影响其他可能使用 .btn-info 的地方 |
| 新增 .btn-export | 专门用于导出按钮 | ✅ 推荐 |
| 行内样式 | 直接在 HTML 写 style | ❌ 不符合项目规范 |

## Cross-Stage Notes

### PRD 阶段承诺
- 保持按钮功能和交互行为不变
- 响应式布局需保持正常
- 按钮文字颜色保持 #007aff

### 待办（下一阶段）
1. 创建新的 `.btn-export` CSS 类
2. 调整 HTML 结构，将导出按钮移至第二行
3. 确保移动端响应式正常
4. 测试导出功能仍然正常工作

## Status

**当前阶段**: `stage:requirements` ✅ 已完成

**已完成**:
- [x] 分析 Figma 设计稿
- [x] 编写 PRD 文档
- [x] 提交并推送
- [x] 添加 `human:review-needed` 标签
- [x] 在 PR 上评论请求审核

**下一阶段**: `stage:planning` - 等待人工审核通过后自动进入
