# Claude Auto-Dev Agent 故障排查

## 问题：Claude 命令一直运行不结束

### 症状
- 执行 `claude` 命令后，任务一直在运行
- PR 已经成功创建
- 但命令没有退出

### 根本原因
Claude 可能在：
1. 等待手动测试完成（启动服务器、浏览器测试等）
2. 尝试评论 Issue 但遇到权限或 API 问题
3. 等待某些异步操作完成
4. 没有收到明确的"任务完成"信号

### 立即解决方案

#### 1. 手动停止当前任务
```bash
# 找到 claude 进程
ps aux | grep claude

# 停止进程（替换 PID）
kill <PID>

# 或者使用 Ctrl+C
```

#### 2. 检查 PR 是否创建成功
```bash
# 使用 gh CLI 检查
gh pr list

# 或访问 GitHub 网页查看
```

如果 PR 已创建，说明 Claude 的主要工作已完成 ✅

### 已修复

更新后的指令文件（`.claude/prd_instructions.md` 和 `.claude/bugfix_instructions.md`）现在包含：

1. **明确的退出指令**
   ```
   ### 10. Task Completion
   Once the PR is created and pushed successfully:
   - Exit immediately
   ```

2. **简化的测试步骤**
   - 移除了手动启动服务器的要求
   - 移除了浏览器测试的要求
   - 只进行代码审查和静态检查

3. **容错的 Issue 评论**
   - 如果评论失败，不会阻塞流程
   - PR 创建成功即视为任务完成

### 如何验证修复

重新运行命令测试：
```bash
claude -p "@.claude/prd_instructions.md Handle GitHub Issue #<NUMBER>" --permission-mode bypassPermissions
```

预期行为：
1. ✅ 创建分支
2. ✅ 实现功能/修复
3. ✅ 提交代码
4. ✅ 创建 PR
5. ✅ （尝试）评论 Issue
6. ✅ **立即退出** ← 这是关键

### 常见问题

#### Q1: 如何判断 Claude 是否卡住了？

**观察方法：**
```bash
# 查看进程状态
ps aux | grep claude

# 如果进程存在但长时间没有输出，可能卡住了
```

**时间参考：**
- 简单功能：5-10 分钟
- 中等复杂度：10-20 分钟
- 如果超过 30 分钟仍无输出，很可能卡住

#### Q2: PR 创建成功但命令没退出，怎么办？

**这是安全的，可以：**
1. 用 `Ctrl+C` 或 `kill` 停止进程
2. PR 已经创建，代码已经推送
3. 检查 PR 内容是否符合预期
4. 如果符合，直接审查和合并 PR

**不会丢失工作成果**，因为代码已经推送到远程。

#### Q3: 如何避免这个问题？

使用更新后的指令文件：
```bash
# 确保使用最新的指令文件
git pull origin main

# 重新运行命令
claude -p "@.claude/prd_instructions.md Handle GitHub Issue #<NUMBER>"
```

#### Q4: GitHub Actions 中如何防止超时？

workflow 文件已添加超时保护：
```yaml
timeout-minutes: 30
```

如果 Claude 30 分钟没有完成，会自动终止。

### 调试技巧

#### 1. 添加调试输出
在指令文件中添加进度标记：
```markdown
After each major step, output:
- "✅ Step X completed: [description]"
```

#### 2. 使用超时命令
```bash
# 设置最大执行时间（例如 20 分钟）
timeout 20m claude -p "@.claude/prd_instructions.md Handle GitHub Issue #7"
```

#### 3. 监控文件变化
在另一个终端监控：
```bash
# 监控 git 状态
watch -n 5 git status

# 监控文件变化
fswatch -l 1 . | while read file; do echo "Changed: $file"; done
```

### 预防措施

#### 1. 在 workflow 中使用超时
```yaml
- name: Claude PRD Development
  timeout-minutes: 30
  run: |
    claude -p "@.claude/prd_instructions.md ..."
```

#### 2. 重定向输入
防止 Claude 等待用户输入：
```bash
claude -p "@.claude/prd_instructions.md ..." < /dev/null
```

#### 3. 后台运行并记录日志
```bash
# 后台运行
claude -p "@.claude/prd_instructions.md Handle GitHub Issue #7" > claude.log 2>&1 &

# 记录 PID
echo $! > claude.pid

# 监控日志
tail -f claude.log

# 需要时停止
kill $(cat claude.pid)
```

### 紧急处理

如果 GitHub Actions 中的 job 卡住了：

#### 方案 A: 在 GitHub 网页上取消
1. 进入 Actions 标签页
2. 找到运行中的 workflow
3. 点击 "Cancel workflow"

#### 方案 B: 在 Mac 上强制终止
```bash
# 停止 claude 进程
pkill -f claude

# 停止 runner worker（谨慎）
pkill -f "Runner.Worker"
```

#### 方案 C: 重启 runner
```bash
cd ~/actions-runner
./svc.sh stop
./svc.sh start
```

### 联系支持

如果问题持续：
1. 收集日志：`~/actions-runner/_diag/Worker_*.log`
2. 检查 Claude CLI 版本：`claude --version`
3. 查看 Claude 文档或社区支持

---

## 总结

**核心原则：**
- ✅ PR 创建成功 = 主要工作完成
- ✅ 可以安全停止卡住的进程
- ✅ 使用更新后的指令文件避免问题
- ✅ 设置超时保护机制

**记住：** 自动化的目标是提高效率，不是完全无人值守。人工审查和测试仍然是必要的。
