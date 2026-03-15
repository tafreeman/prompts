# Code Review

Review uncommitted changes for security, quality, and correctness.

## Steps

1. Get changed files: `git diff --name-only HEAD`
2. Dispatch the **code-reviewer** agent to analyze each file
3. If Python files changed, also dispatch **security-reviewer** agent
4. Report findings grouped by file, severity first (CRITICAL > HIGH > MEDIUM > LOW)
5. Block commit if CRITICAL or HIGH issues found

## Severity Rules

- **CRITICAL**: Security vulnerabilities (secrets, injection, auth bypass) — must fix
- **HIGH**: Logic errors, missing error handling, >50-line functions — must fix
- **MEDIUM**: Mutation patterns, missing tests, style issues — fix when possible
- **LOW**: Minor suggestions — optional

Detailed review criteria are defined in `rules/common/security.md` and `rules/common/coding-style.md`.
