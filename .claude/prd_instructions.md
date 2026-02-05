# Claude PRD Feature Development Instructions

## Mission
You are an autonomous AI agent responsible for implementing new features based on Product Requirement Documents (PRD). Your goal is to complete the entire development cycle independently.

## Workflow

### 1. Understand the Requirement
- Read the GitHub Issue content carefully (it contains the PRD)
- Extract key requirements, acceptance criteria, and technical specifications
- If requirements are unclear or ambiguous, ask clarifying questions by commenting on the issue

### 2. Create Development Branch
```bash
git checkout -b claude/prd-issue-{ISSUE_NUMBER}
```

### 3. Analyze the Codebase
- Review project structure in `src/`
- Check existing patterns in:
  - `src/app_tagging.py` - Flask app entry point
  - `src/routers/tag_manager.py` - Routing patterns
  - `src/db.py` - Database operations
  - `src/templates/` - Frontend templates
  - `src/static/js/` - JavaScript logic
- Identify where changes need to be made

### 4. Implementation Guidelines

#### Backend (Python/Flask)
- Follow existing code style and patterns
- Use the database wrapper in `src/db.py`
- Add new routes in appropriate router modules under `src/routers/`
- Implement proper error handling with try-except blocks
- Use SQLite3 for database operations
- Return JSON responses for API endpoints
- Follow RESTful conventions

#### Frontend (HTML/JS)
- Follow existing template structure in `src/templates/`
- Use consistent CSS classes and styling
- Implement responsive UI components
- Add JavaScript logic in `src/static/js/`
- Ensure proper error handling and user feedback

#### Database Changes
- If schema changes are needed, create migration scripts
- Update `src/db.py` with new database operations
- Ensure backward compatibility when possible

### 5. Code Quality Check

Before committing, do a quick review:
- Check your changes for syntax errors
- Verify logic is correct
- Ensure code follows project patterns
- No hardcoded sensitive data

**IMPORTANT**: Do NOT start the Flask server or attempt manual browser testing in CI/CD environment. Human reviewers will test after PR is created.

### 6. Commit Changes
```bash
git add .
git commit -m "feat: implement {feature_name} (#ISSUE_NUMBER)

- Added {list key changes}
- Updated {list updated components}
- Tested {list testing done}"
```

### 7. Push and Create PR
```bash
git push origin claude/prd-issue-{ISSUE_NUMBER}

gh pr create \
  --title "feat: {brief feature description} (#ISSUE_NUMBER)" \
  --body "## Summary
  
This PR implements the feature requested in #ISSUE_NUMBER.

## Changes Made
- {List major changes}
- {Include any technical decisions}

## Testing Done
- {List what you tested}
- {Include any manual testing steps}

## Screenshots (if UI changes)
{Add screenshots if applicable}

## Notes
{Any important notes for reviewers}"
```

### 8. Update Original Issue
Try to comment on the issue with:
```markdown
✅ **Feature implementation completed!**

I've created PR #{PR_NUMBER} with the following changes:
- {Brief summary of implementation}

Please review the code changes and test the functionality.
```

**Note**: If commenting fails due to permissions, that's acceptable - the PR is the main deliverable.

### 9. Task Completion Signal
Once you have successfully:
1. ✅ Created the branch
2. ✅ Implemented the changes
3. ✅ Committed the code
4. ✅ Pushed to remote
5. ✅ Created the PR

Then output: `🎉 TASK COMPLETED - PR created successfully`

This signals that the automated workflow is done. Do NOT wait for manual testing, approvals, or merges.

## Project-Specific Context

### Tech Stack
- **Backend**: Flask 2.3+, Python 3.8+
- **Database**: SQLite3 (file: `vocab.db`)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3

### Key Files
- `src/app_tagging.py` - Flask application entry
- `src/db.py` - Database operations
- `src/routers/tag_manager.py` - Main routing logic
- `src/templates/tags.html` - Main UI template
- `src/static/js/tags.js` - Frontend logic
- `config/categories.json` - Category configuration

### API Endpoint Pattern
- Base URL: `/tagging/vocab/`
- API prefix: `/tagging/vocab/api/`
- Return format: JSON

### Database Schema
Check existing schema by examining `src/db.py` or querying the database directly.

## Error Handling

### If Tests Fail
- Debug and fix issues before creating PR
- Add error details to issue comments
- Don't create PR until functionality works

### If Requirements Are Unclear
- Comment on the issue asking for clarification
- List specific questions or ambiguities
- Wait for response before implementing

### If Blocked by External Dependencies
- Document the blocker in issue comments
- Suggest alternatives if possible
- Don't proceed with incomplete implementation

## Success Criteria
- [ ] Feature fully implements PRD requirements
- [ ] All manual tests pass
- [ ] No errors in Flask console or browser console
- [ ] Code follows project conventions
- [ ] PR created with clear description
- [ ] Original issue updated with PR link

## Important Guidelines

### Permission Handling
- If you need permissions to edit files, request them or use available permission modes
- Use `--permission-mode bypassPermissions` if needed when running in CI/CD
- Don't let permission prompts stop your workflow

### Autonomous Decisions
- Make reasonable technical decisions without asking for permission on every detail
- If you encounter minor obstacles, work around them
- Focus on completing the core workflow: branch → code → commit → PR

### When to Stop
ONLY stop after successfully:
1. Creating and pushing the feature branch
2. Creating the Pull Request
3. (Optionally) commenting on the issue

Do NOT stop if:
- You haven't created the branch yet
- You haven't implemented the changes
- You haven't created the PR
- You're just asking for file edit permissions

### After PR Creation
Once PR is created successfully:
- Output the completion signal
- Do NOT start servers or attempt manual testing
- Do NOT wait for human approval or merge
- Your automated task is complete
