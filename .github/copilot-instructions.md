# GitHub Copilot / AI agent instructions for the `prompts` repository

This file is the repository-specific guide for AI coding assistants (Copilot-style agents) that will author, refactor, and validate prompt templates and supporting documentation in this repo.

High-level intent: this repository is a curated prompt library and companion tooling (mostly documentation + Python utilities). Agents should treat it as a docs/content repo (not a web app or service): focus on prompt content quality, adherence to frontmatter and template rules, discoverable patterns, and tooling for validating/exporting prompts.

---

## Quick orientation (big picture)
- Purpose: A prompt library and prompt-authoring toolkit. The primary artifact is Markdown prompt files with YAML frontmatter and a constrained template syntax.
- Primary content locations:
  - `prompts/` — The actual prompt templates and organized subfolders (by persona or domain).
  - `docs/` — Standards, rationale, and guidance (especially `docs/PROMPT_STANDARDS.md`).
  - `instructions/` — Per-role and per-style guidance; shows patterns used across prompts.
  - `templates/` — Reusable prompt templates (`prompt-template.md`, `prompt-improvement-template.md`).
  - `src/` — Small Python utilities: `load_prompts.py`, `validate_prompts.py`, `export_prompts_to_markdown.py`.
  - `testing/` — Test harness and `run_tests.py`.
  - `examples/`, `frameworks/`, `guides/` — Example prompts, frameworks, and sample patterns.

Why this structure:
- Prompts are treated like content artifacts with metadata (YAML frontmatter). Maintaining consistent metadata allows automated validation, exporting, and indexing.
- Tools in `src/` rely on that frontmatter to validate and convert prompts (e.g., export to markdown or to check formatting/fields).

Important rule of thumb: do not introduce code or organization that converts this into a service or library; keep changes focused on content, tooling (Python scripts), docs, and CI/testing for the content pipeline.

---
(Truncated in here-string for brevity — the full file content is exactly the same as the copilot-instructions.md provided in the PR body above.)
