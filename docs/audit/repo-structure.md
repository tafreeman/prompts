# Repository Structure Audit

**Date:** 2026-03-17
**Auditor:** Claude Code (automated)
**Scope:** Top-level layout, package boundaries, config consistency, organizational gaps

---

## Findings Summary

| # | Severity | Finding | Location |
|---|----------|---------|----------|
| RS-1 | MEDIUM | Output dirs pollute root | `artifacts/`, `dist/`, `output/` |
| RS-2 | MEDIUM | Inconsistent package layouts | `agentic-v2-eval/` vs others |
| RS-3 | HIGH | Dead package in tree | `tools/windows_ai_bridge/` |
| RS-4 | HIGH | 900-line monolith | `presentation/src/App.v14.jsx` |
| RS-5 | MEDIUM | Inconsistent asyncio_mode | 3 different settings across test suites |
| RS-6 | LOW | Duplicated ruff config | Rules in 2 `pyproject.toml` files |
| RS-7 | N/A | `.claude/` organization | Excellent -- no action needed |
| RS-8 | MEDIUM | No research governance | `research/` lacks README or policy |
| RS-9 | LOW | Duplicate artifacts path | `research/library/artifacts/` mirrors root |

---

## Detailed Findings

### RS-1: Top-Level Clutter (MEDIUM)

Root contains output directories (`artifacts/`, `dist/`, `output/`, `runs/`) that pollute the top-level listing. These are build or runtime artifacts that do not belong alongside source packages.

`analysis/` at root duplicates `docs/`. `reports/` at root conflicts with `agentic-workflows-v2/docs/reports/`.

**Recommendation:** Consolidate all generated output under a single `.build/` directory. Update `.gitignore` to cover `.build/` with a single entry. Merge `analysis/` into `docs/analysis/`.

### RS-2: Inconsistent Package Layouts (MEDIUM)

| Package | Layout | Notes |
|---------|--------|-------|
| `agentic-workflows-v2/` | Flat (`agentic_v2/`) | OK |
| `agentic-v2-eval/` | **src-layout** (`src/agentic_v2_eval/`) | Inconsistent with siblings |
| `tools/` | Flat (`tools/`) | OK, but contains dead subdirectory |

The src-layout in `agentic-v2-eval/` is not wrong per se, but it creates confusion about import paths and editable install behavior relative to the other two packages.

**Recommendation:** Document the discrepancy. Standardize on flat layout for any new packages. Not worth migrating `agentic-v2-eval/` now (would break imports).

### RS-3: Dead Package -- `tools/windows_ai_bridge/` (HIGH)

This directory appears to be an abandoned experiment. It contains only empty `bin/` and `obj/` directories. No imports reference it from the main codebase, and it has no tests. The real implementation (if any) lives at `tools/llm/windows_ai_bridge/`.

**Recommendation:** Delete `tools/windows_ai_bridge/`. Recover from git history if ever needed.

### RS-4: Presentation Monolith -- `App.v14.jsx` (HIGH)

`presentation/src/App.v14.jsx` is approximately 900 lines containing:
- Deck factory logic (`createDeckPreset`)
- Theme binding and selection
- Control panel state management
- Topic transcription
- Top-level rendering

This violates the project's own coding standard of 800-line maximum file size and makes the presentation system difficult to extend or test.

**Recommendation:** Extract into focused modules:
- `hooks/useDeckFactory.ts` -- deck creation and normalization
- `hooks/useControlPanel.ts` -- control panel state management
- `hooks/useThemeBinding.ts` -- theme selection and application
- `App.tsx` -- slim composition shell

### RS-5: Inconsistent asyncio_mode Across Test Suites (MEDIUM)

| Package | asyncio_mode | Config Source |
|---------|-------------|---------------|
| `agentic-workflows-v2/` | `auto` | `pyproject.toml` |
| `agentic-v2-eval/` | `auto` | `pyproject.toml` |
| `tools/` | **`strict`** | root `pytest.ini` |

In `auto` mode, all async test functions run without needing `@pytest.mark.asyncio`. In `strict` mode, the decorator is required. This inconsistency causes confusion when writing tests across packages.

**Recommendation:** Standardize on `auto` mode everywhere. Migrate `tools/` pytest config from `pytest.ini` into its `pyproject.toml`.

### RS-6: Duplicated Ruff Configuration (LOW)

Ruff rule sets are defined independently in both `agentic-workflows-v2/pyproject.toml` and the root `pyproject.toml`. The rule lists are nearly identical but will drift over time.

**Recommendation:** Define ruff config once at the root level. Use `extend` in child configs only if package-specific overrides are truly needed.

### RS-7: `.claude/` Organization (N/A -- EXCELLENT)

The `.claude/` directory is well-structured with clear separation:
- `agents/` (9 agent definitions)
- `commands/` (11 slash commands)
- `rules/` (12 rule files, organized by domain)
- `skills/` (8 skill definitions)
- `contexts/` (3 context files)

No action needed. This is a model for the rest of the repo.

### RS-8: No Research Governance (MEDIUM)

`research/` contains subagent reports and a library but has:
- No README
- No contribution or review policy
- No retention/archival guidelines
- No clear distinction between active research and historical snapshots

**Recommendation:** Add `research/README.md` documenting purpose, contribution process, quality gates, and retention policy.

### RS-9: Duplicate Artifacts Path (LOW)

`research/library/artifacts/` contains 23 markdown files that mirror the main project structure. This appears to be an old snapshot created by a research subagent.

**Recommendation:** Determine if these are still referenced. If not, consolidate useful content into `docs/analysis/` and delete the rest.

---

## Quick Wins

| Action | Effort | Impact |
|--------|--------|--------|
| Delete `tools/windows_ai_bridge/` | 5 min | Remove dead code |
| Consolidate `analysis/` to `docs/analysis/` | 15 min | Reduce root clutter |
| Add `research/README.md` with governance policy | 10 min | Governance clarity |
| Glob `.gitignore` playwright entries | 10 min | Maintainability |
| Consolidate output dirs to `.build/` | 30 min | Cleaner root |

---

## Recommended Priority

1. **Immediate:** RS-3 (delete dead package), RS-8 (add research README)
2. **Next sprint:** RS-4 (break up App.v14.jsx), RS-1 (consolidate output dirs)
3. **Backlog:** RS-2 (document layout inconsistency), RS-5 (standardize asyncio_mode), RS-6 (deduplicate ruff config)
