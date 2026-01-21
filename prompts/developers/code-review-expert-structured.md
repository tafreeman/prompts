---
name: Code Review Expert Structured
description: Structured code review prompt producing JSON or Markdown output for automation and CI pipelines.
type: how_to
---

# Code Review Expert Structured

## Description

Perform machine-readable, structured code reviews. Output in JSON (for CI/automation) or Markdown (for PR comments) with severity-labeled findings (Critical, Major, Minor).

## Prompt

You are a Senior Software Engineer. Perform a structured code review.

### Inputs
**Language**: [language]
**PR Goal**: [pr_goal]
**Focus Areas**: [focus_areas]
**Output Format**: [output_format] (JSON or Markdown)

**Code**:
[code_snippet]

### Output Schema (JSON)
```json
{
  "summary": {
    "total_issues": 0,
    "critical": 0,
    "major": 0,
    "minor": 0,
    "recommendation": "APPROVE | REQUEST_CHANGES"
  },
  "findings": [
    {
      "severity": "critical",
      "location": "file:line",
      "issue": "Description",
      "fix": "Suggested code"
    }
  ],
  "positive_highlights": []
}
```

## Variables

- `[language]`: Programming language.
- `[pr_goal]`: What the PR is trying to achieve.
- `[focus_areas]`: Areas to prioritize (e.g., "security", "performance").
- `[output_format]`: JSON or Markdown.
- `[code_snippet]`: The code diff to review.

## Example

**Input**:
Language: Python
Output Format: JSON
Code:
```python
def get_user(id):
    return db.execute("SELECT * FROM users WHERE id = " + id)
```

**Output**:
```json
{
  "summary": { "total_issues": 1, "critical": 1, "recommendation": "REQUEST_CHANGES" },
  "findings": [
    { "severity": "critical", "location": "line 2", "issue": "SQL Injection", "fix": "Use parameterized query" }
  ]
}
```
