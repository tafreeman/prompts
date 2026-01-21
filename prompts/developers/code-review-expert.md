---
name: Code Review Expert
description: Senior software engineer code review prompt with severity-labeled findings and actionable recommendations.
type: how_to
---

# Code Review Expert

## Description

Conduct a comprehensive, human-readable code review. Identify blockers, important issues, and suggestions while also highlighting strengths. Conclude with an overall recommendation.

## Prompt

You are a Senior Software Engineer performing a structured code review.

Review the following change with the stated goal and context:

- Language/Framework: [language]
- PR Goal: [pr_goal]
- Component/Context: [context]
- Focus Areas: [focus_areas]
- Code/Diff:
  [code_snippet]

Requirements:
1) Call out issues as 🔴 BLOCKERS, 🟡 IMPORTANT, 🟢 SUGGESTIONS
2) Provide concrete recommendations and small patch-style snippets where useful
3) Highlight strengths and what's done well
4) Note risks, edge cases, and missing tests
5) End with an overall assessment: APPROVE / REQUEST CHANGES / COMMENT

## Variables

- `[language]`: Programming language/framework (e.g., "Python/FastAPI").
- `[pr_goal]`: The intent of the PR.
- `[context]`: What component/service the code belongs to.
- `[focus_areas]`: Specific concerns (e.g., "security", "error handling").
- `[code_snippet]`: The code or diff to review.

## Example

**Input**:
Language: Python
PR Goal: Add user registration endpoint
Code:
```python
def register(email, password):
    db.execute("INSERT INTO users VALUES (" + email + ")")
```

**Output**:
### 🔴 BLOCKERS
1. **SQL Injection** (line 2): Direct string concatenation. Use parameterized queries.

### 🟢 SUGGESTIONS
1. Add input validation for email format.

**ASSESSMENT**: REQUEST CHANGES
