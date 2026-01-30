```instructions
# GitHub Copilot instructions for the `prompts` repository

This file is a lightweight compatibility pointer and quick reference. The authoritative, repo-wide guidance is in:

- `.github/instructions/prompts-repo.instructions.md` — guardrails, checklists, and authoring conventions
- `.github/copilot-instructions.md` — comprehensive developer guidance and workflows

Quick reminders:

- Keep diffs small and reviewable; avoid bulk rewrites.
- Prompt files live under `prompts/` and must follow the frontmatter schema in `docs/reference/frontmatter-schema.md`.
- Use templates in `prompts/templates/` when creating new prompts.
- Validate prompt edits with the repo tasks or `python -m tools.validate_prompts --all` and run tests with `python -m pytest testing/` when changing tooling.

Refer to `prompts-repo.instructions.md` for full rules and examples.
```