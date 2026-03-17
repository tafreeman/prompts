# Code Quality Audit

**Date:** 2026-03-17
**Auditor:** Claude Code (automated)
**Scope:** Dangling references, import correctness, exception handling, test coverage

---

## Findings Summary

| # | Severity | Finding | Impact |
|---|----------|---------|--------|
| CQ-1 | CRITICAL | `prompts/__init__.py` exports 7 constants for deleted `.md` files | ImportError at runtime |
| CQ-2 | HIGH | `agents.yaml` references 12 non-existent prompt files | Agent instantiation fails |
| CQ-3 | HIGH | 42 presentation `.tsx` files import from wrong relative path | Production build will fail |
| CQ-4 | HIGH | `content-registry.ts` imports `.js` structure files | Rollup production build will fail |
| CQ-5 | MEDIUM | 40+ bare `except Exception:` handlers | Swallows unexpected errors |
| CQ-6 | LOW | 2 `print()` calls in production code | Bypasses structured logging |

---

## Detailed Findings

### CQ-1: Stale Prompt Exports in `__init__.py` (CRITICAL)

**File:** `agentic-workflows-v2/agentic_v2/prompts/__init__.py`

The module exports 7 constants that attempt to load content from deleted markdown files:

| Constant | Expected File | Status |
|----------|--------------|--------|
| `ANALYST` | `analyst.md` | DELETED |
| `DEBUGGER` | `debugger.md` | DELETED |
| `JUDGE` | `judge.md` | DELETED |
| `REASONER` | `reasoner.md` | DELETED |
| `RESEARCHER` | `researcher.md` | DELETED |
| `VISION` | `vision.md` | DELETED |
| `WRITER` | `writer.md` | DELETED |

These files were removed in commit `d921ba0f` but the exports were not cleaned up. Any code importing these constants will get an empty string or raise a `FileNotFoundError` depending on the loader implementation.

A grep of the codebase confirms none of these 7 constants are referenced anywhere outside `__init__.py` itself.

**Fix:** Remove all 7 constants from `prompts/__init__.py`. A script exists at `scripts/fix-stale-prompt-exports.py`.

### CQ-2: Broken Agent YAML References (HIGH)

**File:** `agentic-workflows-v2/agentic_v2/agents.yaml`

12 of 18 agent entries in the registry reference prompt files that no longer exist on disk:

| Agent Entry | Referenced Prompt | Exists? |
|-------------|------------------|---------|
| analyst | `prompts/analyst.md` | No |
| debugger | `prompts/debugger.md` | No |
| judge | `prompts/judge.md` | No |
| reasoner | `prompts/reasoner.md` | No |
| researcher | `prompts/researcher.md` | No |
| vision | `prompts/vision.md` | No |
| writer | `prompts/writer.md` | No |
| linter | `prompts/linter.md` | No |
| summarizer | `prompts/summarizer.md` | No |
| validator | `prompts/validator.md` | No |
| developer | `prompts/developer.md` | No |
| assembler | `prompts/assembler.md` | No |

**Impact:** Instantiating any of these 12 agents will either fail or produce agents with empty system prompts, depending on error handling in the agent loader.

**Fix:** Remove the 12 stale entries from `agents.yaml`, or restore the prompt files if the agents are still needed.

### CQ-3: Wrong Relative Import Paths in Presentation (HIGH)

**Path:** `presentation/src/components/**/*.tsx` (42 files)

42 `.tsx` component files import hooks using an incorrect relative path:
```typescript
import { useTheme } from "../hooks/useTheme.js";
```

The actual hook files live at `./hooks/` relative to the component, not `../hooks/`. Vite's dev server resolves this automatically through its module resolution, but Rollup (used for production builds) does NOT perform this resolution. The production build will fail with unresolved import errors.

**Fix:** Update all 42 import paths. A script exists at `scripts/fix-presentation-imports.py`.

### CQ-4: `.js` Extension Imports in TypeScript (HIGH)

**File:** `presentation/src/content/content-registry.ts`

The content registry imports structure definition files using `.js` extensions:
```typescript
import { advocacyStructure } from "./structures/advocacy.js";
import { sprintStructure } from "./structures/sprint.js";
// ... 6 more
```

The actual files are `.ts`. Vite dev server auto-resolves `.js` to `.ts`, but Rollup production builds do not. This is a known gotcha documented in the project's own CLAUDE.md.

**Fix:** Change all `.js` import extensions to `.ts` in `content-registry.ts`. This is also flagged in git status as a modified file.

### CQ-5: Broad Exception Handling (MEDIUM)

40+ instances of bare `except Exception:` (or `except Exception as e:` with only logging) across the codebase. Key locations:

| File | Line(s) | Context |
|------|---------|---------|
| `cli/display.py` | 189, 225 | CLI rendering |
| `workflows/artifact_extractor.py` | 57 | Artifact parsing |
| `server/app.py` | multiple | Request handlers |
| `langchain/tools.py` | multiple | Tool execution |
| `engine/executor.py` | multiple | Step execution |

The project's coding standards require specific exception types. Bare `except Exception:` masks bugs, swallows unexpected errors, and makes debugging difficult.

**Fix:** Replace with specific exception types on a case-by-case basis. This requires judgment -- not fully scriptable.

### CQ-6: `print()` in Production Code (LOW)

| File | Line | Content |
|------|------|---------|
| `claude_sdk_agent.py` | 28 | Debug print in agent initialization |
| `code_execution.py` | 194 | Status print in code runner |

The project uses structured logging (`structlog`/`loguru`). These 2 `print()` calls bypass the logging pipeline, won't appear in log aggregators, and violate the coding standard against print statements.

**Fix:** Replace with appropriate `logger.debug()` or `logger.info()` calls. A script exists at `scripts/fix-print-to-logging.py`.

---

## Test Coverage Assessment

Overall test coverage is adequate:
- **1,396 tests** passing across the main test suite
- RAG module coverage at ~92% (gate: 80%)
- 3 pre-existing test failures (known, tracked)
- 17 tests skipped (integration/slow markers)

No immediate test coverage gaps identified beyond the stale references above.

---

## Recommended Priority

1. **Immediate (blocks production build):** CQ-3 (fix import paths), CQ-4 (fix `.js` extensions)
2. **Immediate (runtime failures):** CQ-1 (remove stale exports), CQ-2 (clean agents.yaml)
3. **Next sprint:** CQ-5 (narrow exception handlers)
4. **Backlog:** CQ-6 (replace print with logging)
