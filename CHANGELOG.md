# Changelog

All notable changes to this project are documented here.

---

## [Unreleased]

### New Features

- **`skill-architect` agent** — New AI persona specialized in designing, extracting, and refactoring skills as reusable prompt programs. Added to the canonical agent roster with full documentation.
- **`verify-and-correct` skill** — Bounded self-correction loop: automatically runs tests, lint, and type checks after code changes, then retries fixes (up to a limit) before reporting back. Reduces back-and-forth on build failures.
- **`session-plan` skill** — Plan a focused session with 1–2 goals, explicit success criteria, and a TODO checklist. Prevents mega-sessions that hit rate limits by scoping work upfront.
- **Headless prompts** — New infrastructure for running agent prompts without an interactive session.
- **Adapter registry CLI wiring (ADR-001)** — Orchestrator, workflow runner, and CLI now route through the adapter registry, making engine backends (native DAG, LangGraph) fully swappable at runtime.
- **SmartModelRouter hardening (ADR-002)** — Added persistence across restarts, `Retry-After` header support, and degraded-mode fallback so the router stays operational when providers are rate-limited or unavailable.

### Improvements

- **CI pipeline upgrades** — Updated `actions/setup-python` from v4 → v5 across all workflows. Added cross-package E2E job, expanded security scanning with `pip-audit`, and tightened dependency review to fail on severity `moderate`.
- **Release pipeline** — New tag-triggered `deploy.yml` with build provenance for reproducible releases.
- **Performance regression detection** — Rewrote `performance-benchmark.yml` to compare against a stored baseline and fail on detected regressions.
- **Secret sanitization rule** — Always-on sanitization middleware now redacts API keys, tokens, and passwords before they reach LLM context. Covers all agent sessions by default.
- **Backlog tracking** — Added 11 new backlog tickets (rows 34–44) covering architectural debt, test gaps, and documentation tasks.

### Security

- **P0 tool-layer hardening** — `http_ops`, `search_ops`, and `shell_ops` received critical security fixes: SSRF URL validation, shell injection blocklist (20+ blocked patterns), `shlex.split` with `shell=False`, path traversal guards, and `__builtins__` restriction in the code execution sandbox.

### Bug Fixes & Documentation

- Fixed factual drift across monorepo documentation (CLAUDE.md, AGENTS.md, README files, ADRs).
- Corrected 40+ dangling references to deleted prompts and removed workflows.
- Removed 23 duplicate tests, fixed 2 broken tests as part of ADR-008 test coverage overhaul.
- Aligned stale agent config entries with the current agent roster.

### Test Coverage (ADR-008)

- Added tests for 12+ previously untested modules, including evaluation pipeline, workflow pipeline, server backends, LLM judge, and scoring.
- Hardened server test coverage for streaming backends and session handling.
- Overall test coverage for `agentic_v2` raised toward the 80% target.

### Cleanup & Refactoring

- **Presentation system extracted** — The presentation/deck builder has been moved to its own standalone repository (`present`). 245 files removed from this repo; raw-themes data and scripts are preserved in the new repo.
- Removed deprecated agent prompts, workflow definitions, Copilot config, and stale GitHub Actions workflows.
- Removed dead prompt constants, obsolete artifact files, and cleaned up `.gitignore`.

---

## Earlier History

For changes prior to March 2026, see the git log:

```
git log --oneline --before="2026-03-01"
```
