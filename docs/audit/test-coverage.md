# Test Coverage Audit — 2026-04-14

**Git SHA (audit):** 0252c88ce93792d05d13613e0b1f431d3193d006
**Git SHA (after fixes):** 7f1ae0f
**Status:** ⚠️ Issues Found (duplicate files and slow test markers resolved)

## Implementation Status (2026-04-14)

| Finding | Status | Commit |
|---------|--------|--------|
| Duplicate `test_server_auth.py` / `test_server_websocket.py` | ✅ Already deleted (audit snapshot stale) | — |
| `time.sleep` tests missing `@pytest.mark.slow` | ✅ Fixed: `test_timeout_handling` and `test_shell_tool_timeout` marked | `e07a991` |
| 4 vacuously passing tests | Open | — |
| ~35 untested modules in `agentic_v2` | Open — Strategic item S-2 | — |
| `tools/` package <10% coverage | Open — Strategic item S-2 | — |
| `model_probe.py` (2,313 lines, 0 tests) | Open — Strategic item S-2 | — |
| `llm_evaluator.py` (777 lines, 0 tests) | Open — Strategic item S-2 | — |

> Note: A prior coverage analysis exists at `docs/TEST_COVERAGE_ANALYSIS.md` (dated 2026-03-02). This audit
> refreshes that report against current HEAD, incorporating new test files added since then (91 vs 60+
> previously) and re-examining the quality patterns that have since been addressed or introduced.

---

## Findings

### Critical

- **`tools/` package severely undertested.** 10 test files cover only 3 of 35+ source modules.
  The highest-risk zero-coverage modules are `tools/llm/model_probe.py` (~2,313 lines), which
  implements model availability detection with persistent cache and retry logic, and
  `tools/agents/benchmarks/llm_evaluator.py` (~777 lines), which is the core rubric-scoring engine
  used by the evaluation pipeline. These modules carry the highest defect risk.
- **Coverage gate set at 80% (`fail_under = 80` in pyproject.toml) but cannot be verified.**
  The pytest coverage run was not executed during this audit due to environment constraints;
  actual line coverage is unknown. Given the zero-coverage modules listed below, the gate is
  likely failing or currently bypassed.
- **No timeout marker on `test_code_execution.py` or `test_phase2d_tools.py`** despite containing
  subprocess invocations that can block (e.g., `time.sleep(60)` inside a tested command string,
  `time.sleep(10)` in a shell subprocess). If pytest-timeout is not configured globally these
  tests can hang CI indefinitely.

### High

- **Duplicate test files not yet deleted.** The March 2026 audit identified `test_server_auth.py`
  and `test_server_websocket.py` as complete duplicates of `test_auth.py` and `test_websocket.py`.
  Both duplicate files still exist in the repository. The migration of unique tests and deletion
  of the duplicates has not been completed.
- **Broken / vacuously passing tests still present.** Four tests identified in the prior audit
  remain unfixed:
  - `test_runner_ui.py::test_returns_empty_dict_when_file_missing_and_probe_unavailable` — `with patch(...): pass`, asserts nothing.
  - `test_provider_adapters.py::test_resolves_to_onnx_directory` — assertion `result is None or isinstance(result, Path)` is always true.
  - `test_cli.py::test_no_arguments` — asserts `exit_code == 2 or exit_code == 0` (covers both success and failure).
  - `test_cli.py::test_orchestrate_shows_note` — loose `or` assertion accepts both configured and unconfigured states.
- **`engine/agent_resolver.py` (979 lines) has no dedicated test file.** This module bridges
  YAML workflow definitions to LLM execution, handling multi-turn tool loops, JSON parsing, and
  prompt assembly. It is the highest-risk untested module in the main `agentic_v2` package.
  Note: `test_agent_resolver.py` appeared in the current file list — this should be verified to
  confirm it provides meaningful coverage rather than only structure tests.
- **`server/datasets.py` (~858 lines) has no dedicated test file.** The prior audit flagged this;
  it remains uncovered as of this audit.
- **18+ duplicate tests in `test_langchain_engine.py`** not yet removed after focused unit test
  files (`test_langchain_expressions.py`, `test_langchain_config.py`, `test_langchain_models_unit.py`)
  were extracted. These inflate test counts without adding coverage.

### Medium

- **`time.sleep()` used in 3 test files for timing-dependent assertions.** `test_rag_tracing.py`
  uses `time.sleep(0.01)` to assert latency >= 5ms. This is a flaky pattern — if the system is
  under load the assertion may fail, and if not under load the 10ms sleep wastes CI time.
  Prefer injecting a fake clock or mocking the timer.
- **`test_workflow_editor_routes.py` and `test_langchain_dependency_guards.py` have only 3-4
  tests each.** These are likely incomplete stubs; the modules they cover have significant surface
  area not exercised.
- **No fixture scoping used across any test file.** All fixtures default to `function` scope.
  For expensive setup (e.g., RAG vectorstores, LLM client instantiation), `module` or `session`
  scope would substantially reduce test runtime without losing isolation.
- **`test_rag_tracing.py::test_context_manager_tracks_latency`** uses `time.sleep(0.01)` and
  asserts `latency_ms >= 5.0` — relies on real wall-clock time, inherently flaky under CI load.
- **Dead code in `server/evaluation.py` (lines 102-120)** — unreachable code after a `return`
  statement identified in prior audit, not yet cleaned up.

### Low

- **25+ low-value tests** (constructor defaults, enum `.value` checks, `isinstance` on typed
  return values) still present. See prior audit Part A7 for the full list. These inflate the
  test count without catching real bugs and add maintenance overhead.
- **`test_agents_integration.py` not yet consolidated.** The prior audit recommended migrating
  unique tests to `test_agents_orchestrator.py` and deleting the file; it remains.
- **`test_langchain_integration.py` contains 5 duplicate tests** that should be removed per the
  prior audit (Part A4). These remain.

---

## Metrics

| Metric | Value | Gate | Status |
|--------|-------|------|--------|
| Test files (agentic-workflows-v2) | 91 | — | — |
| Test files (agentic-v2-eval) | 10 | — | — |
| Test files (tools/) | 10 | — | — |
| Test functions (agentic-workflows-v2) | ~1,443 | — | — |
| Test functions (agentic-v2-eval) | ~233 | — | — |
| Test functions (tools/) | ~282 | — | — |
| Coverage (agentic_v2 backend) | Not measured | 80% | ❓ Unknown |
| Coverage (tools/ package) | Not measured | 80% | 🔴 Likely failing |
| Duplicate test files | 2 identified, not deleted | 0 | 🔴 |
| Broken/vacuous tests | 4 confirmed | 0 | ⚠️ |
| Zero-coverage critical modules | 2+ (model_probe, llm_evaluator) | 0 | 🔴 |
| pytest asyncio_mode | auto | auto | ✅ |
| pytest-timeout configured | Yes (dev extra) | required | ✅ |
| Coverage fail_under | 80% (pyproject.toml) | 80% | ✅ (configured) |
| Integration marker defined | Yes | required | ✅ |
| Slow marker defined | Yes | required | ✅ |

---

## Untested Modules (agentic_v2 package — no dedicated test file)

Modules are assessed against the test file listing. Indirect coverage may exist via integration
tests but has not been instrumented.

| Module | Has Dedicated Test? | Risk |
|--------|---------------------|------|
| `engine/agent_resolver.py` | Partial (`test_agent_resolver.py` exists, quality unknown) | CRITICAL |
| `engine/llm_output_parsing.py` | No | HIGH |
| `engine/prompt_assembly.py` | No | HIGH |
| `engine/tool_execution.py` | No | HIGH |
| `engine/verification.py` | No | HIGH |
| `engine/pipeline.py` | No | MEDIUM |
| `engine/protocol.py` | No | MEDIUM |
| `engine/context.py` | No | MEDIUM |
| `server/datasets.py` | No | HIGH |
| `server/dataset_matching.py` | No | MEDIUM |
| `server/result_normalization.py` | No | MEDIUM |
| `server/routes/evaluation_routes.py` | No | MEDIUM |
| `server/routes/runs.py` | No | MEDIUM |
| `server/execution.py` | No | HIGH |
| `integrations/mcp/adapters/prompt_adapter.py` | No | MEDIUM |
| `integrations/mcp/adapters/resource_adapter.py` | No | MEDIUM |
| `integrations/mcp/discovery/prompts.py` | No | LOW |
| `integrations/mcp/discovery/resources.py` | No | LOW |
| `integrations/mcp/results/budget.py` | No | MEDIUM |
| `integrations/mcp/results/storage.py` | No | MEDIUM |
| `integrations/mcp/runtime/backoff.py` | No (fixture exists for ExponentialBackoff in test_agents.py) | LOW |
| `integrations/tracing.py` | No | LOW |
| `agents/implementations/claude_sdk_agent.py` | No | HIGH |
| `agents/json_extraction.py` | No | HIGH |
| `models/backends_base.py` | No (covered partially by test_model_backends.py) | MEDIUM |
| `models/backends_cloud.py` | No (covered partially) | MEDIUM |
| `models/backends_local.py` | No (covered partially) | MEDIUM |
| `models/model_stats.py` | No | MEDIUM |
| `middleware/response_sanitizer.py` | No | MEDIUM |
| `middleware/detectors/base.py` | No | LOW |
| `tools/builtin/build_ops.py` | No | LOW |
| `tools/builtin/code_analysis.py` | No | MEDIUM |
| `tools/builtin/git_ops.py` | No | MEDIUM |
| `tools/builtin/http_ops.py` | No | MEDIUM |
| `tools/builtin/search_ops.py` | No | LOW |
| `tools/builtin/shell_ops.py` | No | HIGH (high-risk ops) |
| `cli/display.py` | No | LOW |
| `cli/helpers.py` | No | LOW |
| `cli/rag_commands.py` | No | LOW |

## Untested Modules (tools/ package — critical gaps)

| Module | Has Test? | Risk |
|--------|-----------|------|
| `tools/llm/model_probe.py` (~2,313 lines) | No | CRITICAL |
| `tools/agents/benchmarks/llm_evaluator.py` (~777 lines) | No | CRITICAL |
| `tools/agents/benchmarks/evaluation_pipeline.py` (~320 lines) | No | HIGH |
| `tools/agents/benchmarks/workflow_pipeline.py` (~394 lines) | No | HIGH |
| `tools/agents/benchmarks/datasets.py` (~310 lines) | No | HIGH |
| `tools/agents/benchmarks/loader.py` (~556 lines) | No | HIGH |
| `tools/agents/benchmarks/registry.py` (~261 lines) | No | HIGH |
| `tools/core/tool_init.py` (~501 lines) | No | MEDIUM |
| `tools/core/local_media.py` (~464 lines) | No | MEDIUM |
| `tools/llm/model_inventory.py` (~528 lines) | No | MEDIUM |
| `tools/llm/model_bakeoff.py` (~633 lines) | No | MEDIUM |

---

## Flaky Test Patterns

| Pattern | Files | Finding |
|---------|-------|---------|
| `time.sleep()` in test execution | `test_rag_tracing.py` | Real `sleep(0.01)` used to assert latency — flaky under load |
| `time.sleep()` in tested command strings | `test_code_execution.py`, `test_phase2d_tools.py` | Subprocess invocations with embedded sleeps; need `@pytest.mark.slow` and timeout |
| Unmocked network calls | None detected | No bare `requests.get`/`httpx.get` in test files — ✅ |
| Tests with no assertions | 3 files with `time.sleep` usage checked | `test_rag_tracing.py` has assertions; `test_code_execution.py` and `test_phase2d_tools.py` use sleep in test payloads, not in test logic itself |

---

## Test Quality Assessment

### Strengths

- `asyncio_mode = "auto"` is correctly configured — no manual `@pytest.mark.asyncio` needed.
- `pytest-timeout` is included in the `dev` extra — runtime timeouts can be applied.
- Markers for `integration`, `slow`, and `security` are defined.
- The eval package (`agentic-v2-eval`) and UI test suite (Vitest) are clean with good behavioral coverage.
- Well-tested modules: `engine/expressions.py`, `models/rate_limit_tracker.py`, `langchain/graph.py`,
  `server/multidimensional_scoring.py`, `server/auth.py`, `server/websocket.py`.
- No raw network calls detected in test files without mocking.

### Weaknesses

- No `scope=` used on any `@pytest.fixture` — all default to `function`. Heavy fixtures
  (vectorstores, model clients) should use `module` or `session` scope.
- 4 vacuously passing tests that can never fail.
- 2 duplicate test files consuming maintenance bandwidth.
- Test count inflation from ~25 low-value constructor/enum tests.
- No coverage measurement tooling run in CI confirmed; the 80% gate exists in config but
  enforcement in CI pipelines was not verified in this audit.

---

## Recommendations

### Immediate (Before Next Merge)

1. **Delete `test_server_auth.py`** — after migrating `test_whitespace_stripped_from_x_api_key`
   to `test_auth.py`. This is a complete duplicate confirmed by the prior audit.
2. **Delete `test_server_websocket.py`** — after migrating `test_broadcast_tolerates_failed_ws`
   to `test_websocket.py`. Complete duplicate confirmed.
3. **Fix or remove 4 vacuous tests** in `test_runner_ui.py`, `test_provider_adapters.py`, and
   `test_cli.py` (see Critical findings above).
4. **Add `@pytest.mark.slow` and `pytest.ini` timeout** to `test_code_execution.py` and
   `test_phase2d_tools.py` to prevent CI hangs from subprocess sleeps.

### Short-Term (Next Sprint)

5. **Write `test_server_datasets.py`** — `server/datasets.py` is ~858 lines with zero dedicated
   tests. Target: 20+ tests covering CRUD operations, pagination, error paths.
6. **Expand `test_server_judge.py`** — currently only 4 tests for a 561-line module.
   Target: 25+ tests covering calibration, consistency, structured output parsing.
7. **Remove 18 duplicate tests from `test_langchain_engine.py`** (expressions, config, model
   registry classes already covered in focused unit test files).
8. **Remove 5 duplicate tests from `test_langchain_integration.py`** (per prior audit Part A4).
9. **Add module-scoped fixtures** for expensive setup in RAG and model backend tests.
10. **Clean dead code in `server/evaluation.py` lines 102-120** — unreachable after `return`.

### Medium-Term (Next Quarter)

11. **Write tests for `tools/llm/model_probe.py`** — 2,313 lines with zero tests. This is the
    highest-risk untested module in the entire monorepo. Target: 40+ tests.
12. **Write `test_llm_evaluator.py`** — 777 lines of core rubric scoring logic with zero tests.
    Target: 30+ tests covering all rubric dimensions and edge cases.
13. **Write tests for `engine/tool_execution.py`**, `engine/verification.py`,
    `agents/implementations/claude_sdk_agent.py`, and `agents/json_extraction.py`.
14. **Add `test_server_execution.py`** — `server/execution.py` has no dedicated coverage.
15. **Replace `time.sleep()` latency assertion in `test_rag_tracing.py`** with injected clock
    or mock timer to eliminate flakiness.
16. **Verify 80% coverage gate enforcement in CI** — confirm `--cov-fail-under=80` is passed
    in the CI pipeline (not just configured in pyproject.toml).
17. **Add UI component tests** for the 11 untested React components and 7 untested pages
    (JsonViewer, WorkflowDAG, DashboardPage, RunDetailPage, etc.).
18. **Add 4-9 E2E tests** beyond the current single smoke test — full workflow execution,
    multi-agent coordination, WebSocket streaming.

---

## Reference

- Prior coverage analysis: `/c/Users/tandf/source/prompts/docs/TEST_COVERAGE_ANALYSIS.md` (2026-03-02)
- pyproject.toml coverage config: `agentic-workflows-v2/pyproject.toml` (`fail_under = 80`)
- Test directory: `agentic-workflows-v2/tests/` (91 files, ~1,443 test functions)
- Eval test directory: `agentic-v2-eval/tests/` (10 files, ~233 test functions)
- Tools test directory: `tools/tests/` (10 files, ~282 test functions)
