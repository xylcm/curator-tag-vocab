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

### 5. Testing & Validation
- **Manual Testing**:
  - Start the Flask app: `python src/app_tagging.py`
  - Test all new endpoints via browser or curl
  - Verify UI changes render correctly
  - Test edge cases and error scenarios
  
- **Check for errors**:
  - Review Flask console output for errors
  - Check browser console for JavaScript errors
  - Verify database operations complete successfully

### 6. Code Quality
- Ensure code is readable and well-commented
- Follow PEP 8 style guidelines for Python
- Remove any debug print statements
- Ensure no hardcoded credentials or sensitive data

### 7. Commit Changes
```bash
git add .
git commit -m "feat: implement {feature_name} (#ISSUE_NUMBER)

- Added {list key changes}
- Updated {list updated components}
- Tested {list testing done}"
```

### 8. Push and Create PR
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

### 9. Update Original Issue
Comment on the issue with:
```markdown
✅ **Feature implementation completed!**

I've created PR #{PR_NUMBER} with the following changes:
- {Brief summary of implementation}

**Testing Results**: All manual tests passed ✓

Please review the code changes and test the functionality.
```

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

## Remember
- **Be autonomous**: Make reasonable technical decisions without asking for permission on every detail
- **Be thorough**: Test extensively before submitting
- **Be clear**: Write detailed commit messages and PR descriptions
- **Be responsible**: Don't push broken code or skip testing
