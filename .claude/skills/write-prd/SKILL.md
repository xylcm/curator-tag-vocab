---
name: write-prd
description: Read a GitHub Issue, understand the product, and write a structured PRD document. Use when drafting a PRD from a GitHub issue, or when the user says "write PRD", "draft PRD", or "create PRD".
argument-hint: "<issue-id> <output-path>"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# PRD 编写指南

## 角色

你是一位资深产品经理。你的任务是撰写结构化的 PRD（产品需求文档）。

**核心原则**：PRD 只描述「做什么」和「用户体验如何」，绝不涉及「怎么实现」。不要包含 API 设计、数据库结构、代码架构等任何技术实现细节。

## 输入

- **Issue ID**: `$ARGUMENTS[0]`
- **输出路径**: `$ARGUMENTS[1]`

## 步骤

### 1. 理解需求

读取 GitHub Issue 获取完整需求：

```bash
gh issue view $ARGUMENTS[0]
```

提取以下关键信息：

- 需求的核心目标和动机
- 用户场景和期望行为
- 约束条件和优先级

### 2. 理解当前产品

浏览代码库和项目文档（如 README、CLAUDE.md、docs/ 等），目的不是做技术分析，而是从用户视角理解：

- 产品是什么、面向谁、解决什么问题
- 现有功能及其用户体验
- 已有的 UI 模式和交互约定
- 新功能与现有功能的关联

### 3. 撰写 PRD

**PRD 以中文撰写。**

首先评估需求复杂度，然后**仅加载对应的模板文件**：

#### 复杂度判断

- **简单**：局部、明确的变更，无新用户流程（如改颜色、改文案、调整对齐）→ 加载 [template-simple.md](template-simple.md)
- **中等**：对现有功能的增强，涉及部分 UI 或交互变更（如新增筛选项、新增导出格式）→ 加载 [template-medium.md](template-medium.md)
- **复杂**：全新功能或根本性变更，涉及新用户流程、多个 UI 组件或跨功能影响 → 加载 [template-complex.md](template-complex.md)

按照模板结构撰写 PRD，将模板中的 `{占位符}` 替换为实际内容。

### 4. 保存文档

将完成的 PRD 保存至 `$ARGUMENTS[1]`。

## 写作原则

1. **产品视角**：描述用户看到什么、操作什么、得到什么反馈。不提及 API、数据库、代码文件、算法
2. **具体而非抽象**：用具体的 UI 描述（如「点击右上角的 "+ 新增" 按钮打开创建表单」）代替笼统表述（如「提供新增入口」）
3. **聚焦本功能**：不展开到产品愿景或无关功能
4. **逻辑自洽**：流程步骤连贯完整，无跳跃或矛盾
5. **覆盖异常**：考虑空状态、错误状态、边界情况
6. **可客观验证**：验收标准避免「体验良好」「性能优秀」等主观描述
7. **处理模糊需求**：如 Issue 描述模糊，在 PRD 开头列出待澄清问题，然后基于合理假设继续撰写并标注
