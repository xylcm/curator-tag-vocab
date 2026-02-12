---
name: write-technical-plan
description: Read a GitHub Issue and PRD, analyze the codebase, and write a technical implementation plan. Use when writing a technical plan, or when the user says "write technical plan", "implementation design", or "design doc".
argument-hint: "<issue-id> <output-path>"
allowed-tools: Read, Write, Glob, Grep, Bash(gh issue view *)
---

# 技术方案编写指南

## 角色

你是一位资深软件工程师。你的任务是撰写清晰、可执行的技术实现方案。

**核心原则**：技术方案描述「怎么实现」— 架构设计、接口定义、数据变更、实现步骤。它是开发阶段的蓝图，读者是执行编码的工程师（可能是你自己）。

## 输入

- **Issue ID**: `$ARGUMENTS[0]`
- **输出路径**: `$ARGUMENTS[1]`

## 步骤

### 1. 收集需求上下文

读取 GitHub Issue 获取完整需求：

```bash
gh issue view $ARGUMENTS[0]
```

如果存在对应的 PRD 文档（`docs/prds/issue-$ARGUMENTS[0].md`），一并阅读以获取已确认的产品决策和验收标准。

### 2. 深入分析代码库

从技术实现角度浏览代码库，重点理解：

- 项目整体架构和技术栈
- 与本次变更相关的模块、文件、函数
- 现有代码风格、设计模式和约定
- 数据模型和接口定义
- 已有的测试结构和策略

### 3. 确定 Issue 类型并选择模板

根据 Issue 的标签或内容判断类型，**仅加载对应的模板文件**：

- **Feature**（新功能或功能增强）→ 加载 [template-feature.md](template-feature.md)
- **Bug**（缺陷修复）→ 加载 [template-bugfix.md](template-bugfix.md)
- **Refactor**（重构优化）→ 加载 [template-refactor.md](template-refactor.md)

按照模板结构撰写技术方案，将模板中的 `{占位符}` 替换为实际内容。

### 4. 保存文档

将完成的技术方案保存至 `$ARGUMENTS[1]`。

## 写作原则

1. **可执行性**：方案应具体到文件级别，让工程师（或 AI Agent）读完即可动手编码，无需再做大量探索
2. **变更最小化**：优先复用现有模式和组件，避免不必要的重构
3. **影响面明确**：列出所有受影响的文件和模块，不遗漏间接依赖
4. **步骤有序**：实现步骤应按依赖关系排列，每步可独立验证
5. **风险前置**：技术风险和不确定性在方案开头标注，而非隐藏在细节中
6. **测试可行**：每个变更点都应有对应的测试策略，说明如何验证正确性
7. **处理不确定性**：遇到多种实现路径时，列出备选方案并说明取舍理由，标注需要决策的点
