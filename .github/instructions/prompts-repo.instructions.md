---
description: Repo-wide guardrails and checklists for prompts + Python tooling changes.
applyTo: "**/*"
---

# Repo guardrails + checklists (prompts)

This file is the **actionable checklist** for changes in this repo.

For repo map + canonical commands, also read: `.github/copilot-instructions.md`.

## Scope and intent

- Optimize for **small, reviewable diffs** and repo consistency.
- Prefer improving/using existing tooling over introducing new frameworks.
- Avoid bulk rewrites across many prompts unless explicitly requested.

## Before you change anything

- Identify the change type:
  - **Prompt-only** (`prompts/**`)
  - **Docs-only** (`docs/**`, `README.md`, etc.)
  - **Python tooling / tests** (`tools/**`, `prompttools/**`, `testing/**`)
  - **Mixed**
- If the request implies new folders, new CLIs, or new workflows, sanity-check that the repo already has a natural home for it.

## Prompt changes (`prompts/**`)

- Follow:
  - Template: `prompts/templates/prompt-template.md`
  - Frontmatter schema: `docs/reference/frontmatter-schema.md`
- Keep placeholders as `[BRACKETED_VALUES]` and document them under “Variables”.
- Prefer adding:
  - Concrete examples
  - Clear input/output expectations
  - Edge-case handling guidance
- After changes, run prompt validation.
  - If you skip validation, explicitly say **what you skipped** and **why** (e.g., “docs-only change”).

## Python tooling changes (`tools/**`, `prompttools/**`, `testing/**`)

- Keep changes small and testable.
- Add or update unit tests when behavior changes.
- Run the test suite.
  - If you skip tests, explicitly say **what you skipped** and **why** (e.g., “comment-only change in docstring”).
- If you change a shared function/CLI:
  - Update call sites
  - Update docs that show usage examples

## Docs changes (`docs/**`, `README.md`, etc.)

- Ensure command examples match real entrypoints.
- Prefer pointing to existing Tasks/CLIs instead of inventing new scripts.
- You may skip running tests/validation for purely editorial changes, but note the skip and rationale.

## Always avoid

- Inventing repo components that don’t exist (apps, deployment folders, DBs).
- Hardcoding secrets.
- Renaming/moving large folder structures unless explicitly requested.