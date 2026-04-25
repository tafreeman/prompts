# Repository Guidelines

## Project Structure & Module Organization

This repository is a Python `uv` workspace with a React UI and shared tooling.
Core runtime code lives in `agentic-workflows-v2/agentic_v2/`; its FastAPI,
workflow, examples, scripts, and tests are under the same package directory.
The dashboard is in `agentic-workflows-v2/ui/`. Evaluation tooling lives in
`agentic-v2-eval/src/agentic_v2_eval/` with tests in `agentic-v2-eval/tests/`.
Root-level shared utilities are in `tools/`, cross-package tests in `tests/`,
and contributor documentation in `docs/`. Agent and automation surfaces are
tracked in `.claude/` and `.github/agents/`.

## Build, Test, and Development Commands

Run commands from the repository root unless noted.

- `just setup` creates `.venv`, installs editable Python packages, and installs UI dependencies.
- `just test` runs runtime, eval, E2E, and UI test suites.
- `just docs` validates documentation references.
- `just dev` starts the backend and Vite UI; `just dev-stop` stops them.
- `pre-commit run --all-files` runs formatting, linting, docs formatting, and secret checks.
- `npm --prefix agentic-workflows-v2/ui run build` type-checks and builds the UI.

## Coding Style & Naming Conventions

Python targets 3.11, uses 88-column formatting, and is formatted by Black,
isort, Ruff, and docformatter. Add type hints to new public functions and keep
imports explicit. Python modules and functions use `snake_case`; classes use
`PascalCase`. UI code uses TypeScript, React 19, Vite, and Tailwind; prefer
component names in `PascalCase` and hooks/utilities in `camelCase`.

## Testing Guidelines

Use `pytest` for Python tests and Vitest/Playwright for UI tests. Name Python
tests `test_*.py` and keep tests near their package (`agentic-workflows-v2/tests/`,
`agentic-v2-eval/tests/`, or root `tests/e2e/`). Coverage floors are 80% for
Python packages and 60% for the UI. For UI-only changes, run
`npm --prefix agentic-workflows-v2/ui test` and, when relevant,
`npm --prefix agentic-workflows-v2/ui run test:e2e`.

## Commit & Pull Request Guidelines

Use Conventional Commits: `<type>(<scope>): <subject>`, for example
`fix(server): paginate dataset sample endpoints`. Common types are `feat`,
`fix`, `docs`, `test`, `refactor`, `chore`, `ci`, and `perf`. Branch from
`main` with names like `feature/...`, `fix/...`, `docs/...`, or `chore/...`.
PRs should cover one concern, include summary/changes/testing sections, link
issues when applicable, update docs and `CHANGELOG.md` for user-visible changes,
and include screenshots for UI changes.

## Security & Configuration Tips

Never commit `.env`, tokens, or provider keys; use `.env.example` as the
template. Runtime secrets should flow through the project secret helpers rather
than direct environment access. Run `pre-commit run --all-files` before pushing
so `detect-secrets` can catch accidental credentials.
