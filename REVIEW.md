# Post-Merge Review — 2026-02-21

## Verdict: PARTIAL

> Core functionality works but 4 backend tests fail and evaluation code has critical linting errors that block test execution.

---

## Merge Context

- **Branch / commit**: `fde9626 Multi agent (#81)`
- **Packages changed**: Multi-agent implementations, workflow YAML definitions, frontend components, build configuration
- **High-risk areas**: `agentic_v2/server/evaluation.py` (undefined names + test failures), pyproject.toml (fixed duplicate langchain key)

---

## Results Summary

| Check | Status | Notes |
|-------|--------|-------|
| Environment | PASS | Python 3.13.7, Node v22.19.0, venv present |
| Import health | PASS (8/9 modules OK) | agentic_v2_eval not installed (expected) |
| Backend tests | PARTIAL | 643 passed, **4 failed**, 18 skipped |
| Tools tests | N/A | tools/tests/ directory does not exist |
| UI tests | PASS | 29 passed, 0 failed |
| UI build | PASS | ~161KB gzip, chunk size warning (non-blocking) |
| Lint (ruff) | FAIL | 48+ issues, many in evaluation.py (undefined names) |
| Workflow YAMLs | PASS | 9/9 workflows load successfully |

---

## Issues Found

### Critical (blocks tests & runtime)

1. **ISSUE: `agentic_v2/server/evaluation.py` — Massive undefined names**
   - Lines 91-125: Multiple undefined variables (`floor_violations`, `grade`, `hard_gates`, `weighted_score`, `threshold`, `payload`, `json`)
   - Appears to be a merge conflict or incomplete refactor — critical refactoring happened here
   - **Impact**: 4 test failures all from this file
   - **Fix needed**: Review lines 85-130 and restore proper variable definitions

2. **ISSUE: `agentic_v2/server/evaluation.py` — Function redefinitions**
   - Lines 24-25, 143, 190: `_pick_first`, `_materialize_file_input`, `adapt_sample_to_workflow_inputs` defined twice
   - Suggests incomplete merge resolution or copy-paste during refactor
   - **Fix needed**: Remove duplicate definitions

### High (test failures)

3. **FAIL: `test_server_evaluation.py::test_adapt_sample_to_workflow_inputs_materializes_file`**
   - Error: `TypeError: argument of type 'NoneType' is not iterable` at line 108
   - Undefined `hard_gates` or similar variable

4. **FAIL: `test_server_evaluation.py::test_hard_gate_release_build_verification_failed`**
   - Error: `AttributeError: 'HardGateResult' object has no attribute 'release_build_verified'`
   - API mismatch — HardGateResult schema changed but test not updated

5. **FAIL: `test_server_evaluation.py::test_adapt_sample_to_workflow_inputs_extracts_feature_spec_from_messages`**
   - Error: `TypeError: 'NoneType' object is not subscriptable` at line 409
   - Related to undefined variables in evaluation.py

6. **FAIL: `test_server_evaluation.py::test_hard_gate_release_build_verification_overrides_pass`**
   - Error: `assert True is False` at line 603
   - Logic error in test or implementation

### Medium (warnings, code quality)

7. **WARN: Unused imports** (8 files)
   - `json`, `asyncio`, `typing.AsyncIterator`, `typing.Iterator`, etc.
   - Low impact, easy to fix

8. **WARN: Module-level imports not at top** (3 files)
   - E402 errors in `engine/context.py`, `engine/executor.py`, `integrations/langchain.py`, `integrations/otel.py`
   - Likely conditional imports for optional dependencies

9. **WARN: Unused variables** (3 instances)
   - `last_user_msg` (coder.py:164), `model_id` (agent_loader.py:104), `last_error` (step.py:428)

### Low (informational)

10. **INFO: pyproject.toml had duplicate langchain key** (FIXED)
    - Lines 40-53 had two `[project.optional-dependencies]` langchain sections
    - Fixed by merging into single definition
    - This was causing pytest config error

11. **INFO: 18 skipped tests**
    - Mostly in `test_langchain_integration.py` — likely auth/integration tests requiring live services

12. **INFO: Frontend build chunk size warning**
    - Bundle is 519KB (161KB gzip) — above recommended 500KB limit
    - Not critical, consider lazy-loading if bundle grows further

---

## What Still Works

✓ **Core imports**: All 8 main package modules import successfully
✓ **DAG executor**: Full DAG test suite passes (8/8)
✓ **LangChain engine**: Integration and compilation tests mostly pass (32/36, 4 skipped)
✓ **Workflow definitions**: All 9 YAML workflows load and validate correctly
✓ **Frontend**: Complete test suite passes (29/29), React components render
✓ **CLI**: CLI tests pass (24/24)
✓ **Model routing**: Model router tests pass (40/40)
✓ **Agents**: All agent implementations pass (32/32 new agents, 18 orchestrator, 32 base agents)

---

## Recommended Next Steps

1. **IMMEDIATE**: Fix `agentic_v2/server/evaluation.py`
   - Review lines 85-130 for context of undefined variables
   - Remove duplicate function definitions (lines 24-25, 143, 190)
   - Restore proper variable initialization
   - Likely caused by incomplete merge conflict resolution

2. **HIGH**: Update `HardGateResult` API or test expectations
   - Verify if `release_build_verified` attribute was renamed or moved
   - Update test assertions to match current API

3. **MEDIUM**: Clean up ruff warnings
   - Remove unused imports (8 files) — safe to delete
   - Move E402 imports to top of files
   - Remove unused variables

4. **LOW**: Consider frontend bundle optimization
   - Track chunk sizes as UI grows
   - Implement lazy-loading if bundle exceeds 200KB gzip

---

## Next Sprint Actions

- [ ] Fix evaluation.py before merging to main
- [ ] Re-run full test suite to confirm 4 failures resolved
- [ ] Run ruff --fix to auto-clean unused imports
- [ ] Verify deployment pipeline doesn't break on lint
