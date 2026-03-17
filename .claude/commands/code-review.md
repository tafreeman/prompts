# Code Review

Review uncommitted changes with the canonical code-review workflow.

## Flow

1. Get changed files: `git diff --name-only HEAD`
2. Dispatch the **code-reviewer** agent to analyze the diff
3. If changes touch Python, auth, secrets, or external integrations, also dispatch **security-reviewer**
4. Report findings grouped by file, severity first
5. Stop before commit or merge if any CRITICAL or HIGH issues remain

## Canonical Guidance

- Use `.claude/skills/code-review/SKILL.md` for feedback handling, review requests, and verification gates.
- Use `.claude/rules/common/security.md` and `.claude/rules/common/testing.md` for review criteria.
- Use `.claude/rules/common/agents.md` for agent selection and orchestration.
