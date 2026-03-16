---
paths:
  - "**/*.py"
  - "**/*.pyi"
---
# Python Hooks

> Extends common coding-style rules with Python-specific hook configuration.

## PostToolUse Hooks (Active)

Configured in `.claude/settings.json` (project-level, active).

After every `Edit` or `Write` on a `.py` file, the following run automatically:

- **ruff check --fix**: Auto-fix lint violations in the edited file
- **ruff format**: Auto-format the edited file to project style

## PreToolUse Hooks (Active)

Configured in `.claude/settings.json` (project-level, active).

Before any `Edit` or `Write`:

- **Block `.env` edits**: Prevents direct modification of `.env` and `.env.*` files (use environment variables or a secret manager instead)

## Warnings

- Warn about `print()` statements in edited files (use `logging` module instead)
