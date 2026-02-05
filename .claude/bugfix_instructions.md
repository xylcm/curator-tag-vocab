# Claude Bug Fix Instructions

## Mission
You are an autonomous AI agent responsible for investigating and fixing bugs. Your goal is to identify root causes, implement fixes, and verify solutions independently.

## Workflow

### 1. Understand the Bug
- Read the GitHub Issue content carefully
- Extract:
  - **Symptoms**: What's the observable problem?
  - **Steps to reproduce**: How to trigger the bug?
  - **Expected behavior**: What should happen?
  - **Actual behavior**: What actually happens?
  - **Environment**: Browser, OS, versions, etc.
- If information is missing, ask clarifying questions by commenting on the issue

### 2. Create Fix Branch
```bash
git checkout -b claude/bugfix-issue-{ISSUE_NUMBER}
```

### 3. Investigate the Root Cause

#### A. Reproduce the Bug
- Start the Flask app: `python src/app_tagging.py`
- Follow the reproduction steps from the issue
- Observe the actual behavior
- Check for error messages in:
  - Flask console output
  - Browser console (F12)
  - Network tab (for API errors)

#### B. Locate the Problem
Search for relevant code:
- Check error stack traces for file/line numbers
- Search for related function names
- Review recent changes using `git log`
- Check related files:
  - **Backend errors**: `src/app_tagging.py`, `src/routers/`, `src/db.py`
  - **Frontend errors**: `src/templates/`, `src/static/js/`
  - **Database errors**: `src/db.py`, check SQLite queries

#### C. Analyze the Cause
- Add debug logging if needed
- Test edge cases
- Verify assumptions about data flow
- Check for race conditions or timing issues

### 4. Implement the Fix

#### Fix Categories

**Backend Bugs (Python/Flask)**
- Fix logic errors in route handlers
- Correct database queries
- Add proper error handling
- Fix data validation issues
- Ensure proper HTTP status codes

**Frontend Bugs (JavaScript/HTML)**
- Fix JavaScript logic errors
- Correct DOM manipulation issues
- Fix event handler problems
- Resolve CSS/layout issues
- Fix API call errors

**Database Bugs**
- Fix SQL query syntax
- Add missing indexes
- Correct data type mismatches
- Fix constraint violations

#### Implementation Guidelines
- **Minimal changes**: Fix only what's broken, avoid refactoring
- **Preserve behavior**: Don't change unrelated functionality
- **Add safeguards**: Include defensive checks if appropriate
- **Consider edge cases**: Ensure fix works for all scenarios

### 5. Code Quality Check

Before committing:
- Review your changes for obvious errors
- Verify the fix addresses the root cause
- Check that changes are minimal and focused
- Ensure imports and references are correct

**IMPORTANT**: Do NOT start the Flask server or attempt manual testing in CI/CD environment. Human reviewers will verify the fix after PR is created.

### 6. Code Quality
- Remove any debug logging added during investigation
- Ensure code follows project style
- Add comments explaining the fix if non-obvious
- Keep changes focused and minimal

### 7. Commit Changes
```bash
git add .
git commit -m "fix: resolve {brief bug description} (#ISSUE_NUMBER)

**Root Cause**: {Explain what caused the bug}

**Solution**: {Explain how you fixed it}

**Testing**: {What you tested}

Fixes #ISSUE_NUMBER"
```

### 8. Push and Create PR
```bash
git push origin claude/bugfix-issue-{ISSUE_NUMBER}

gh pr create \
  --title "fix: {brief bug description} (#ISSUE_NUMBER)" \
  --body "## Bug Description

{Summarize the bug from the issue}

## Root Cause

{Explain what was causing the bug}

## Solution

{Describe how you fixed it}

## Testing Done

- [x] Reproduced original bug
- [x] Verified fix resolves the issue
- [x] Tested edge cases: {list them}
- [x] Verified no regression in related features

## Changes Made

\`\`\`
{List files changed and key modifications}
\`\`\`

## Before/After

**Before**: {Describe buggy behavior}
**After**: {Describe fixed behavior}

Fixes #ISSUE_NUMBER"
```

### 9. Update Original Issue
Try to comment on the issue with:
```markdown
🐛 **Bug fix completed!**

**Root Cause**: {Brief explanation}

**Solution**: {Brief description of fix}

I've created PR #{PR_NUMBER} with the fix.

Please review and test the fix.
```

**Note**: If commenting fails due to permissions, that's acceptable - the PR is the main deliverable.

### 10. Task Completion Signal
Once you have successfully:
1. ✅ Created the branch
2. ✅ Implemented the fix
3. ✅ Committed the code
4. ✅ Pushed to remote
5. ✅ Created the PR

Then output: `🎉 TASK COMPLETED - PR created successfully`

This signals that the automated workflow is done. Do NOT wait for manual testing, approvals, or merges.

## Debugging Techniques

### Backend Debugging
```python
# Add strategic logging
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger.debug(f"Variable value: {value}")

# Check database queries
cursor.execute("SELECT * FROM table")
print(cursor.fetchall())

# Verify request data
print(f"Request data: {request.json}")
print(f"Request args: {request.args}")
```

### Frontend Debugging
```javascript
// Add console logging
console.log('Variable value:', value);
console.error('Error occurred:', error);

// Inspect API responses
fetch(url)
  .then(res => res.json())
  .then(data => console.log('API response:', data))
  .catch(err => console.error('API error:', err));
```

### Database Debugging
```bash
# Connect to SQLite database
sqlite3 vocab.db

# Inspect schema
.schema table_name

# Run queries manually
SELECT * FROM tags LIMIT 10;
```

## Common Bug Patterns

### Backend
- Missing error handling → Add try-except blocks
- SQL injection risk → Use parameterized queries
- Incorrect status codes → Return appropriate HTTP codes
- Missing input validation → Validate request data

### Frontend
- Undefined variables → Add null checks
- Event handler not bound → Check addEventListener
- API endpoint typos → Verify URL paths
- Missing error handling → Add .catch() for promises

### Database
- Table not found → Check table existence
- Column mismatch → Verify schema matches code
- Lock timeout → Check for unclosed connections
- Data type errors → Ensure proper type casting

## Error Recovery

### If Fix Doesn't Work
1. Revert changes: `git checkout .`
2. Re-investigate with new debugging approach
3. Update issue with investigation progress
4. Ask for additional information if needed

### If Unable to Reproduce
- Comment on issue requesting:
  - More detailed reproduction steps
  - Environment details (browser, OS, versions)
  - Screenshots or screen recordings
  - Any error messages from console

### If Root Cause Is External
- Document findings in issue comment
- Suggest workarounds if possible
- Recommend reporting to upstream project if applicable

## Success Criteria
- [ ] Bug successfully reproduced
- [ ] Root cause identified and understood
- [ ] Fix implemented with minimal changes
- [ ] Original bug scenario now works correctly
- [ ] No regressions in related functionality
- [ ] PR created with clear explanation
- [ ] Original issue updated with fix details

## Important Guidelines

### Permission Handling
- If you need permissions to edit files, request them or use available permission modes
- Use `--permission-mode bypassPermissions` if needed when running in CI/CD
- Don't let permission prompts stop your workflow

### Autonomous Decisions
- Make reasonable technical decisions without asking for permission on every detail
- If you encounter minor obstacles, work around them
- Focus on completing the core workflow: branch → fix → commit → PR

### When to Stop
ONLY stop after successfully:
1. Creating and pushing the fix branch
2. Creating the Pull Request
3. (Optionally) commenting on the issue

Do NOT stop if:
- You haven't created the branch yet
- You haven't implemented the fix
- You haven't created the PR
- You're just asking for file edit permissions

### After PR Creation
Once PR is created successfully:
- Output the completion signal
- Do NOT start servers or attempt manual testing
- Do NOT wait for human approval or merge
- Your automated task is complete
