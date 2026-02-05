# Claude Auto-Dev Agent 测试指南

## 🎯 测试目标

验证 Claude Auto-Dev Agent 能够：
1. ✅ 正确识别标签并触发 workflow
2. ✅ 自主完成功能开发或 Bug 修复
3. ✅ 创建合格的 Pull Request
4. ✅ 更新 Issue 状态

## 📝 测试步骤

### 测试 1: PRD 功能开发

#### 1. 创建 Issue
1. 进入 GitHub 项目页面
2. 点击 `Issues` → `New issue`
3. 复制 `.github/ISSUE_TEMPLATE_TEST_PRD.md` 的内容（从 "---" 后面开始）
4. 粘贴到 Issue 正文
5. Issue 标题：`[TEST] 添加标签搜索计数显示`

#### 2. 添加标签
- 在 Labels 区域添加标签：`gsd:prd`
- 添加后会自动触发 workflow

#### 3. 观察执行过程
1. 进入 `Actions` 标签页
2. 找到最新的 `Claude Auto-Dev Agent` workflow
3. 点击 `prd-development` job
4. 查看实时日志输出

#### 4. 验证结果
等待 workflow 完成后，检查：
- [ ] 创建了新分支（名称类似 `claude/prd-issue-{N}`）
- [ ] 创建了 Pull Request
- [ ] PR 包含清晰的描述和改动说明
- [ ] Claude 在原 Issue 下评论并提供 PR 链接
- [ ] 代码改动符合需求

#### 5. 代码审查
1. 打开创建的 PR
2. 检查文件改动：
   - `src/templates/tags.html` - 是否添加了计数显示元素
   - `src/static/js/tags.js` - 是否添加了计数逻辑
3. 代码质量检查：
   - 代码风格是否一致
   - 是否有注释说明
   - 逻辑是否正确

#### 6. 功能测试
```bash
# 启动应用
python src/app_tagging.py

# 访问
open http://localhost:80/tagging/vocab
```

测试项目：
- [ ] 页面加载时显示总标签数
- [ ] 输入搜索关键词，计数实时更新
- [ ] 清空搜索框，恢复总数显示
- [ ] 样式合理，不影响布局

---

### 测试 2: Bug 修复

#### 1. 创建 Issue
1. 进入 GitHub 项目页面
2. 点击 `Issues` → `New issue`
3. 复制 `.github/ISSUE_TEMPLATE_TEST_BUGFIX.md` 的内容（从 "---" 后面开始）
4. 粘贴到 Issue 正文
5. Issue 标题：`[TEST] 修复搜索框特殊字符处理问题`

#### 2. 添加标签
- 在 Labels 区域添加标签：`gsd:bugfix`
- 添加后会自动触发 workflow

#### 3. 观察执行过程
1. 进入 `Actions` 标签页
2. 找到最新的 `Claude Auto-Dev Agent` workflow
3. 点击 `bugfix` job
4. 查看实时日志输出

#### 4. 验证结果
等待 workflow 完成后，检查：
- [ ] 创建了新分支（名称类似 `claude/bugfix-issue-{N}`）
- [ ] 创建了 Pull Request
- [ ] PR 说明了根本原因和解决方案
- [ ] Claude 在原 Issue 下评论说明修复情况
- [ ] 代码改动针对性强，不影响其他功能

#### 5. 代码审查
1. 打开创建的 PR
2. 检查文件改动：
   - 主要应该在 `src/static/js/tags.js`
   - 是否正确处理了特殊字符转义
3. 查看 commit message：
   - 是否说明了根本原因
   - 是否描述了解决方案

#### 6. Bug 验证
```bash
# 启动应用
python src/app_tagging.py

# 访问
open http://localhost:80/tagging/vocab
```

测试项目：
- [ ] 输入 `test(1)` 不报错
- [ ] 输入 `path/to/tag` 能正常搜索
- [ ] 输入 `tag[0]` 能正常搜索
- [ ] 浏览器控制台无错误
- [ ] 现有搜索功能正常

---

## 📊 测试检查清单

### Workflow 层面
- [ ] 正确的标签触发正确的 job（prd-development 或 bugfix）
- [ ] workflow 成功完成，无错误
- [ ] 日志清晰，可以追踪 Claude 的执行过程

### Claude 执行层面
- [ ] Claude 正确理解了需求/问题
- [ ] 创建了合适命名的分支
- [ ] 代码修改符合项目规范
- [ ] 进行了必要的测试
- [ ] commit message 清晰准确

### PR 质量
- [ ] PR 标题描述清楚
- [ ] PR 正文包含必要信息（改动、测试、截图等）
- [ ] 代码改动最小化，只改必要的部分
- [ ] 没有引入明显的 bug

### Issue 更新
- [ ] Claude 在原 Issue 下评论
- [ ] 评论包含 PR 链接
- [ ] 说明了完成情况

### 代码质量
- [ ] 代码风格与项目一致
- [ ] 适当的注释
- [ ] 没有硬编码的临时值
- [ ] 没有遗留的 debug 代码

---

## 🔍 故障排查

### Workflow 没有触发
**可能原因：**
- 标签名称不正确（必须完全匹配 `gsd:prd` 或 `gsd:bugfix`）
- workflow 文件有语法错误
- self-hosted runner 未运行

**解决方案：**
```bash
# 检查 workflow 语法
gh workflow list

# 查看 runner 状态
# 在 GitHub Settings → Actions → Runners
```

### Claude 执行失败
**可能原因：**
- ANTHROPIC_API_KEY 未配置或无效
- Claude CLI 未安装或版本不对
- 指令文件路径错误

**解决方案：**
```bash
# 检查 Claude CLI
which claude
claude --version

# 验证 API Key
export ANTHROPIC_API_KEY="your-key"
claude "test" --non-interactive

# 检查指令文件
ls -la .claude/
```

### PR 创建失败
**可能原因：**
- GH_PAT_TOKEN 权限不足
- 分支已存在
- 没有改动可以提交

**解决方案：**
```bash
# 检查 gh CLI
gh auth status

# 手动测试 PR 创建
gh pr create --title "test" --body "test"

# 检查分支
git branch -a | grep claude
```

### Claude 说需求不清晰
**这是正常的！** Claude 会在 Issue 中评论询问，回答问题后它会继续。

---

## 📈 性能指标

记录以下数据以评估 Agent 性能：

| 指标 | PRD 测试 | BugFix 测试 |
|------|----------|-------------|
| 触发时间 | | |
| 完成时间 | | |
| 总耗时 | | |
| 代码行数变化 | | |
| 是否一次成功 | ✅/❌ | ✅/❌ |
| 需要人工修改 | ✅/❌ | ✅/❌ |
| PR 合并状态 | | |

---

## 🎓 后续优化

根据测试结果：

### 如果测试成功
1. 可以开始使用真实的功能需求
2. 调整 `.claude/` 指令文件以优化行为
3. 添加更多标签类型（如 `gsd:refactor`）

### 如果测试失败
1. 检查日志找出失败原因
2. 调整 workflow 配置
3. 优化指令文件的描述
4. 确保环境配置正确

### 持续改进
- 收集 Claude 的成功率和失败模式
- 优化指令文件中的指导语
- 添加更多项目特定的上下文
- 建立代码审查标准

---

## 💡 最佳实践

1. **从简单开始**：先测试简单功能，再尝试复杂需求
2. **清晰描述**：Issue 描述越清晰，Claude 执行越准确
3. **及时反馈**：如果 Claude 询问问题，及时回复
4. **代码审查**：始终人工审查 Claude 的代码
5. **渐进式信任**：根据成功率决定自动化程度

---

**祝测试顺利！🚀**

如有问题，请查看 `.github/CLAUDE_AGENT_USAGE.md` 完整文档。
