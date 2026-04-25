# Sprint 1 — Tool Safety & Silent Failures

**Sprint Goal:** Close the agent-driven attack surface on the developer's own machine.
**Velocity assumption:** 25 pts/sprint. **Committed:** 22 pts. **Stretch:** +3 pts.
**Dependencies between tickets:** None (each ticket is independently executable).

## Backlog (sorted by V/E — ship top items first)

| # | Ticket | Points | Value | T-shirt | V/E | Persona |
|---|---|---|---|---|---|---|
| [01](01-sanitization-fail-closed.md) | Sanitization middleware fail-closed + test | 2 | 9 | S | **4.50** | Security-focused Middleware Engineer |
| [02](02-file-ops-fail-closed.md) | `file_ops` fail-closed without `AGENTIC_FILE_BASE_DIR` | 2 | 8 | S | **4.00** | Filesystem Safety Engineer |
| [03](03-run-id-traversal-test.md) | `run_id` traversal test corpus (validator already exists) | 2 | 6 | S | **3.00** | Backend Input-Validation Engineer |
| [04](04-expressions-ast-audit.md) | Audit `_validate_ast`; close attribute-escape | 3 | 8 | M | **2.67** | AST Sandbox Engineer |
| [05](05-shell-tool-allowlist.md) | Replace `ShellTool` blocklist with allowlist + corpus | 5 | 10 | L | **2.00** | Subprocess Hardening Engineer |
| [06](06-code-execution-harden.md) | Harden `code_execution.py` sandbox + env scoping | 8 | 10 | XL | **1.25** | Sandbox Hardening Engineer |
| [07](07-subprocess-env-sparse.md) *(stretch)* | Sparse env across all subprocess-spawning tools | 3 | 6 | M | **2.00** | Platform Engineer |

**High-leverage quick wins (land first):** tickets 01, 02, 03 — three S-size tickets close a Critical + two Highs in 6 pts combined.

## Pre-existing work worth triaging before starting

The working tree already contains **partial, uncommitted** progress on ticket 05 (`shell_ops.py` has `_SHELL_METACHARS` + `_split_command` scaffolding) and ticket 06 (`code_execution.py` has `_SAFE_ENV_KEYS` scaffolding). Before starting those two tickets, either:

- **a)** Adopt the pre-existing work as the starting point (review the diff, decide what's useful, build on it), or
- **b)** `git stash push -m "pre-sprint-1-wip"` and start clean from the ticket brief.

Each ticket's implementation plan notes this explicitly.

## Definition of Done (applies to every ticket)

- [ ] Code reviewed + merged to `main` via PR
- [ ] Tests added/updated for behavior changes; all new negative-test corpora green
- [ ] `ruff check` + `ruff format` green on edited files (PostToolUse hook handles this automatically for `.py`)
- [ ] `mypy` (if re-enabled for the touched directory) green
- [ ] `pre-commit run --files <changed>` green
- [ ] CI green on the PR
- [ ] `CHANGELOG.md [Unreleased]` entry if the change is user-visible
- [ ] Relevant docs synced (e.g. `.env.example` for new env vars, `SECURITY.md` for hardened surfaces)

## Sprint exit criteria

- All 6 committed tickets merged.
- One `tests/slo/test_concurrent_runs.py` smoke case green on CI (even if thin — it unblocks Sprint 2).
- No new `except: pass` introduced (ruff `S110`/`S112` stays clean in edited files).
- Security-adjacent code surface has adversarial test coverage (shell, code-exec, file-ops, expressions, run_id).

## Agent persona conventions (used in every ticket)

Each ticket assigns a **persona** — a role description for the implementer (human dev or fresh Claude subagent). Personas reference the project's built-in agents under `.claude/agents/` when the fit is clean:

- **security-reviewer** — for adversarial review *after* implementation; not an implementer itself. Every Sprint 1 ticket ends with a "Final review by security-reviewer" step.
- **tdd-guide** — invoke *before* writing implementation code; enforces write-tests-first.
- **python-reviewer** — code review of Python diffs.
- **code-reviewer** — general post-edit review.

The persona block tells the implementer *how to think about the work*; the agent references tell them *which other subagent to invoke at which phase*.

## Velocity recalibration note

After Sprint 1 retro, recompute velocity from actual points completed. If < 18, drop Sprint 2's commitment accordingly and push the stretch out.
