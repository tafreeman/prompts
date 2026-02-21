# Refactoring Plan: Monorepo Stabilization and Quality Lift

Date: 2026-02-20

## Scope

- `agentic-workflows-v2/agentic_v2`
- `agentic-v2-eval/src/agentic_v2_eval`
- `tools`
- `agentic-workflows-v2/ui/src`

## Prioritized Tasks (Execution Order)

1. **[M] Restore critical correctness and test baseline**
   - Status: **Completed**
   - Implemented:
     - Shared path safety utilities for config/workflow loading.
     - CLI validation path compiles workflows with `validate_only=True` (no provider credentials required).
     - Fixed regression in config/workflow validation path and CLI orchestrate contract messaging.
     - Fixed missing imports causing server evaluation test failures.

2. **[S] Make coverage reporting deterministic in CI/local**
   - Status: **Completed**
   - Implemented:
     - UI coverage now works with `@vitest/coverage-v8` and `vitest` coverage config.
     - Added stable coverage commands and scripts:
       - `agentic-workflows-v2/scripts/run_coverage.sh`
       - `agentic-v2-eval/scripts/run_coverage.sh`
     - Documented deterministic commands in package READMEs.

3. **[L] Decompose `agentic_v2.server.evaluation` into cohesive modules**
   - Status: **Completed**
   - Implemented:
     - Extracted scoring engine internals to `agentic-workflows-v2/agentic_v2/server/evaluation_scoring.py`.
     - Extracted dataset logic to `agentic-workflows-v2/agentic_v2/server/datasets.py`.
     - Reduced `agentic-workflows-v2/agentic_v2/server/evaluation.py` to orchestration/compatibility wrapper (preserving public imports and monkeypatch hooks).

4. **[L] Decompose `tools.llm.llm_client` and `tools.agents.benchmarks.runner`**
   - Status: **Completed**
   - Implemented:
     - Extracted provider adapters to `tools/llm/provider_adapters.py`.
     - Centralized local model catalog in `tools/llm/local_models.py`.
     - Reduced `tools/llm/llm_client.py` to façade/dispatch + compatibility wrappers.
     - Extracted interactive runner UI/model selection to `tools/agents/benchmarks/runner_ui.py`.
     - Extracted task evaluation pipeline to `tools/agents/benchmarks/evaluation_pipeline.py`.
     - Extracted workflow data extraction/reporting to `tools/agents/benchmarks/workflow_pipeline.py`.
     - Reduced `tools/agents/benchmarks/runner.py` to orchestration loop + CLI commands only (645 lines from 1293).

5. **[M] Break component-level dependency cycles**
   - Status: **Completed**
   - Implemented:
     - Moved normalization domain logic to neutral package:
       - `agentic-workflows-v2/agentic_v2/evaluation/normalization.py`
     - `workflows/loader.py` now imports normalization from evaluation domain, not server layer.
     - `server/normalization.py` retained as backward-compatible re-export shim.
     - Removed `tools.core -> tools.llm` import path in `tools/core/tool_init.py`.

6. **[M] Centralize constants and remove hardcoded paths**
   - Status: **Completed**
   - Implemented:
     - Replaced hardcoded machine-specific path usage in agent loader with env-driven optional external path.
     - Centralized local model constants in `tools/llm/local_models.py`.

7. **[S] Eliminate high-confidence dead code and duplication**
   - Status: **Completed (targeted pass)**
   - Implemented:
     - Consolidated eval reporter summary logic into shared helper:
       - `agentic-v2-eval/src/agentic_v2_eval/reporters/_summary.py`
     - Cleaned high-confidence unused imports/unused parameter behavior:
       - removed unused `RunnableConfig` import (`integrations/langchain.py`)
       - removed unused `torch` import (`tools/core/local_media.py`)
       - applied `temperature`/`top_p` in local model generation with backward-compatible fallback (`tools/llm/local_model.py`)

8. **[M] Documentation realignment and API docs generation**
   - Status: **Completed**
   - Implemented:
     - Updated stale CLI guidance in `agentic-workflows-v2/README.md` (explicitly marks `orchestrate` as not implemented).
     - Replaced placeholder API doc with curated public export index:
       - `agentic-workflows-v2/docs/API_REFERENCE.md`
     - Annotated/updated stale references in:
       - `agentic-workflows-v2/docs/EVALUATION_MIGRATION_PLAN.md`
       - `agentic-workflows-v2/docs/reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md`
     - Added docs reference validation script:
       - `agentic-workflows-v2/scripts/check_docs_refs.py`

## Suggested Next Steps (All Completed)

All originally suggested next steps have been implemented:

1. ~~**Finalize benchmark runner decomposition** (Task 4 remainder)~~ — **Done**.
   Execution/evaluation pipeline internals extracted to `evaluation_pipeline.py`
   and `workflow_pipeline.py`.

2. ~~**Add focused tests for newly extracted modules**~~ — **Done**.
   - `agentic-workflows-v2/tests/test_evaluation_scoring.py` (17 tests)
   - `agentic-workflows-v2/tests/test_provider_adapters.py` (11 tests)
   - `agentic-workflows-v2/tests/test_runner_ui.py` (16 tests)

3. ~~**Add CI job hooks**~~ — **Done**.
   Updated `.github/workflows/ci.yml`:
   - Tests now run with `pytest-cov` (XML + term-missing reports).
   - `agentic-workflows-v2/` installed via `pip install -e` before test run.
   - `check_docs_refs.py` runs as a dedicated CI step.

## Complexity Summary

- **S**: Task 2, Task 7
- **M**: Task 1, Task 5, Task 6, Task 8
- **L**: Task 3, Task 4

## Validation Notes

- Syntax validation completed for all new/modified Python modules via `python3 -m py_compile`.
- All 44 new unit tests pass (`test_evaluation_scoring.py`, `test_provider_adapters.py`, `test_runner_ui.py`).
- Docs reference checker passes for active docs target set:
  - `cd agentic-workflows-v2 && python3 scripts/check_docs_refs.py`
- Full pytest execution was not run in this environment due missing/invalid local pytest runtime setup for the project virtualenv; targeted compatibility was preserved by keeping backward-compatible wrapper APIs.
