# Test Coverage Analysis & Testing Strategy

**Date:** 2026-03-02
**Scope:** Full monorepo — `agentic-workflows-v2`, `agentic-v2-eval`, `tools/`, UI
**Audited:** 60+ test files, ~1,100 test functions, ~40,000 lines of production code

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Test Inventory](#current-test-inventory)
3. [Part A: Tests to Remove or Consolidate](#part-a-tests-to-remove-or-consolidate)
4. [Part B: Coverage Gaps — Modules Needing New Tests](#part-b-coverage-gaps--modules-needing-new-tests)
5. [Part C: Testing Strategy & Priorities](#part-c-testing-strategy--priorities)

---

## Executive Summary

This audit identified **~95 tests** across the backend that should be **removed, consolidated, or rewritten**. These fall into four categories:

| Category | Count | Impact |
|----------|-------|--------|
| Duplicate files (entire files to delete) | 2 files (~35 tests) | Eliminates maintenance burden of two completely redundant test files |
| Cross-file duplications | ~30 tests | Tests that re-test behavior already covered in another file |
| Low-value tests | ~25 tests | Tests that only assert constructor defaults, enum values, or Python language guarantees |
| Broken / no-op tests | 4 tests | Tests that can never fail due to tautological assertions or broken mocking |

Separately, **9 critical source modules totaling ~8,500 lines have zero test coverage**, and **6 modules totaling ~5,600 lines have under 30% coverage**.

The UI test suite (6 files) and eval test suite (11 files) are clean — no quality issues found.

---

## Current Test Inventory

| Package | Source Lines | Test Functions | Test Files | Quality |
|---------|-------------|---------------|-----------|---------|
| agentic-workflows-v2 (backend) | ~27,000 | ~1,000 | 49 | Mixed |
| agentic-v2-eval | ~4,200 | ~230 | 11 | Good |
| tools/ (shared) | ~12,400 | ~50 | 3 | Poor — only 3 of 35+ modules tested |
| UI (React) | ~3,000 | ~29 | 6 | Good — clean and behavioral |
| E2E | — | 1 | 1 | Minimal |

---

## Part A: Tests to Remove or Consolidate

### A1. Duplicate Files — Delete Entirely

#### `tests/test_server_auth.py` → DELETE

This file is a **complete duplicate** of `tests/test_auth.py`. Both test the same module (`agentic_v2.server.auth`) with the same functionality (`_extract_token` and `APIKeyMiddleware`).

| test_auth.py | test_server_auth.py | Verdict |
|---|---|---|
| `test_bearer_token_extracted` | `test_bearer_token_extracted` | Duplicate |
| `test_bearer_case_insensitive` | `test_bearer_case_insensitive` | Duplicate |
| `test_x_api_key_header_extracted` | `test_x_api_key_extracted` | Duplicate |
| `test_bearer_takes_precedence_over_x_api_key` | `test_bearer_takes_precedence_over_x_api_key` | Duplicate |
| `test_no_token_returns_none` | `test_no_headers_returns_none` | Duplicate |
| `test_bearer_with_extra_whitespace` | `test_whitespace_stripped_from_bearer` | Duplicate |
| `test_non_bearer_auth_returns_none` | `test_authorization_without_bearer_returns_none` | Duplicate |
| `test_no_api_key_env_allows_all_requests` | `test_api_request_allowed_without_key` | Duplicate |
| `test_valid_bearer_token_passes` | `test_correct_bearer_token_allowed` | Duplicate |
| `test_valid_x_api_key_header_passes` | `test_correct_x_api_key_allowed` | Duplicate |
| `test_invalid_token_returns_401` | `test_wrong_key_returns_401` | Duplicate |
| `test_missing_token_returns_401` | `test_no_auth_returns_401` | Duplicate |
| `test_health_endpoint_bypasses_auth` | `test_health_endpoint_bypasses_auth` | Duplicate |
| `test_non_api_routes_bypass_auth` | `test_non_api_route_bypasses_auth` | Duplicate |
| — | `test_whitespace_stripped_from_x_api_key` | **Unique — migrate to test_auth.py first** |

**Action:** Migrate `test_whitespace_stripped_from_x_api_key` to `test_auth.py`, then delete `test_server_auth.py`.

**Why keep test_auth.py:** Uses proper `Request` objects via ASGI scope, uses `monkeypatch` instead of manual setup/teardown, avoids `sys.modules` stub hacks.

---

#### `tests/test_server_websocket.py` → DELETE

Complete duplicate of `tests/test_websocket.py`. Both test `ConnectionManager` from `agentic_v2.server.websocket`.

| test_websocket.py | test_server_websocket.py | Verdict |
|---|---|---|
| `test_connect_adds_to_connections` | `test_connect_registers_under_run_id` | Duplicate |
| `test_connect_accepts_websocket` | `test_connect_accepts_websocket` | Duplicate |
| `test_multiple_connections_same_run` | `test_multiple_clients_same_run` | Duplicate |
| `test_disconnect_removes_connection` | `test_disconnect_cleans_empty_run` | Duplicate |
| `test_disconnect_cleans_up_empty_run` | `test_disconnect_removes_client` | Duplicate |
| `test_disconnect_nonexistent_run_no_error` | `test_disconnect_unknown_run_is_safe` | Duplicate |
| `test_broadcast_sends_to_all_connections` | `test_broadcast_sends_to_connected_ws` | Duplicate |
| `test_broadcast_buffers_events` | `test_broadcast_buffers_event` | Duplicate |
| `test_broadcast_pushes_to_sse_listeners` | `test_broadcast_to_sse_listener` | Duplicate |
| `test_broadcast_handles_full_sse_queue` | `test_full_sse_queue_does_not_raise` | Duplicate |
| `test_broadcast_no_connections_no_error` | `test_broadcast_no_listeners_is_safe` | Duplicate |
| `test_replay_sends_buffered_events` | `test_replay_sends_buffered_events` | Duplicate |
| `test_replay_no_buffer_no_error` | `test_replay_empty_buffer_sends_nothing` | Duplicate |
| `test_broadcast_buffer_respects_max_size` | `test_buffer_enforces_max_size` | Duplicate |
| `test_register_sse_listener` | `test_register_sse_listener` | Duplicate |
| `test_unregister_sse_listener` | `test_unregister_sse_listener` | Duplicate |
| `test_unregister_nonexistent_no_error` | `test_unregister_unknown_run_is_safe` | Duplicate |
| `test_clear_buffer` | `test_clear_buffer_removes_events` | Duplicate |
| `test_clear_buffer_nonexistent_no_error` | `test_clear_buffer_unknown_run_is_safe` | Duplicate |
| `test_replay_stops_on_send_error` | — | **Unique — keep** |
| — | `test_broadcast_tolerates_failed_ws` | **Unique — migrate to test_websocket.py first** |

**Action:** Migrate `test_broadcast_tolerates_failed_ws` to `test_websocket.py`, then delete `test_server_websocket.py`.

**Why keep test_websocket.py:** Uses proper `@pytest.mark.asyncio` decorators (the server version is missing them), uses `AsyncMock` correctly, avoids `sys.modules` hacks.

---

### A2. File to Consolidate — `test_agents_integration.py`

This file (8 tests, 320 lines) overlaps heavily with `test_agents.py` and `test_agents_orchestrator.py`. Specific duplications:

| test_agents_integration.py | Already covered in | Issue |
|---|---|---|
| `test_agent_to_step_creates_valid_step` | `test_agents.py::test_agent_to_step_conversion` AND `test_agents_orchestrator.py::test_agent_step_has_required_fields` | Triple-covered |
| `test_orchestrator_creates_dag_from_subtasks` | `test_agents.py::test_register_agents` AND `test_agents_orchestrator.py::test_register_agent` | Misleading name — only tests registration |
| `test_dag_executor_handles_dependencies` | `test_agents_orchestrator.py::TestDAGExecutorWithAgentSteps` | Duplicate |
| `test_executor_runs_agent_steps` | `test_agents_orchestrator.py::test_executor_runs_agent_steps` | Duplicate |
| `test_multiple_agents_in_dag` | DAG executor tests | Duplicate with mock handlers |

**Action:** Review for any unique tests, migrate them to `test_agents_orchestrator.py`, then delete `test_agents_integration.py`.

Also remove from `test_agents.py`:
- `TestOrchestratorAgent.test_register_agents` (duplicate of dedicated orchestrator tests)
- `TestAgentIntegration.test_agent_to_step_conversion` (triple-covered)
- `TestAgentIntegration.test_multi_agent_workflow` (less thorough version of orchestrator tests)

---

### A3. Cross-File Duplications in LangChain Tests

When focused unit test files were extracted from `test_langchain_engine.py`, the original tests were **not removed**. This created 18+ duplicated tests:

**Remove from `test_langchain_engine.py`** (all duplicated in dedicated unit test files):

| Test class/function in test_langchain_engine.py | Already covered in |
|---|---|
| `TestExpressions::test_simple_variable` | `test_langchain_expressions.py::test_simple_path` |
| `TestExpressions::test_nested_path` | `test_langchain_expressions.py::test_simple_path` |
| `TestExpressions::test_condition_true` | `test_langchain_expressions.py::test_not_equal` |
| `TestExpressions::test_condition_false` | `test_langchain_expressions.py::test_variable_comparison_false` |
| `TestExpressions::test_in_operator` | `test_langchain_expressions.py::test_in_operator` |
| `TestExpressions::test_missing_path_returns_none` | `test_langchain_expressions.py::test_missing_path_returns_none` |
| `TestExpressions::test_empty_expression_is_true` | `test_langchain_expressions.py::test_empty_string_returns_true` |
| `TestCoalesceExpression::test_coalesce_returns_first_non_none` | `test_langchain_expressions.py::test_coalesce` |
| `TestCoalesceExpression::test_coalesce_three_args_first_wins` | `test_langchain_expressions.py::test_coalesce_first_available` |
| `TestCoalesceExpression::test_coalesce_in_condition` | Same as above — no distinct coverage |
| `TestCompositeExpressions::test_resolve_dict_of_expressions` | `test_langchain_expressions.py::test_dict_recursive_resolution` |
| `TestCompositeExpressions::test_resolve_list_of_expressions` | `test_langchain_expressions.py::test_list_recursive_resolution` |
| `TestCompositeExpressions::test_non_string_passthrough` | `test_langchain_expressions.py::test_non_string_passthrough` |
| `TestConfigLoader::test_list_workflows` | `test_langchain_config.py::test_lists_yaml_files` |
| `TestConfigLoader::test_load_nonexistent_raises` | `test_langchain_config.py::test_load_nonexistent_raises_file_not_found` |
| `TestModelRegistry::test_retryable_model_error_detects_rate_limits` | `test_langchain_models_unit.py::test_rate_limit_in_message_is_retryable` |
| `TestModelRegistry::test_env_model_override_with_fallback` | `test_langchain_models_unit.py::test_env_var_with_fallback` |
| `TestModelRegistry::test_env_model_override_uses_env_value` | `test_langchain_models_unit.py::test_env_var_resolved` |
| `TestModelRegistry::test_model_candidates_keep_explicit_override` | `test_langchain_models_unit.py::test_override_takes_precedence` |

**Action:** Delete the `TestExpressions`, `TestCoalesceExpression`, `TestCompositeExpressions` classes and the listed `TestConfigLoader` and `TestModelRegistry` tests from `test_langchain_engine.py`. Keep the unique graph compilation, workflow runner, response parsing, per-step model override, conditional fan-out, loop iteration, and LangSmith tracing tests.

---

### A4. Cross-File Duplications in `test_langchain_integration.py`

| Test | Already covered in | Action |
|---|---|---|
| `test_workflow_result_metadata` | `test_simple_workflow_invocation` (same file) | Remove — same invocation, same assertions |
| `test_stream_node_updates` | `test_stream_execution` (same file) | Remove — strictly weaker assertions |
| `test_compiled_graph_async_execution` | `test_compiled_graph_execution` (same file) | Remove — tests LangGraph's async wrapper, not application code |
| `test_workflow_list` | `test_langchain_engine.py` and `test_langchain_config.py` | Remove — triple-covered |
| `test_load_different_workflows` | `test_langchain_engine.py::test_load_code_review` | Remove |

---

### A5. Cross-File Duplications in Evaluation/Scoring Tests

`test_server_evaluation.py` and `test_evaluation_scoring.py` have significant overlap — the former tests hard gates through the `score_workflow_result()` facade, the latter tests `compute_hard_gates()` directly. Since the facade is trivial delegation, these are redundant:

| test_server_evaluation.py | test_evaluation_scoring.py | Action |
|---|---|---|
| `test_hard_gate_null_output_fails` | `test_required_outputs_missing_fails_gate` | Remove from server_evaluation |
| `test_hard_gate_failed_status_fails` | `test_failed_status_fails_gate` | Remove from server_evaluation |
| `test_hard_gate_critical_step_failure` | `test_failed_step_fails_critical_gate` | Remove from server_evaluation |
| `test_hard_gate_schema_contract_invalid` | `test_schema_contract_validated_when_payload_provided` | Remove from server_evaluation |
| `test_hard_gate_dataset_incompatible` | `test_dataset_workflow_compatible_propagated` | Remove from server_evaluation |
| `test_score_result_contains_gate_fields` | Multiple tests already assert these keys | Remove from server_evaluation |
| `test_hard_gate_release_build_verification_failed` | Also tests same path via different entry point | Remove one |

---

### A6. Cross-File Duplications in DAG Tests

`test_dag.py` and `test_dag_executor.py` overlap on core DAG execution behavior:

| test_dag.py | test_dag_executor.py | Action |
|---|---|---|
| `test_max_concurrency_respected` | `test_max_concurrency_limit` | Remove from test_dag.py — identical |
| `test_step_failure_stops_dependents` | `test_step_failure_cascades_to_dependents` | Remove from test_dag.py — executor version also tests grandchild cascade |
| `test_expression_evaluator_with_step_results` | `test_expressions.py` covers `${ctx.enabled}` | Remove from test_dag.py — misleading setup, tests nothing new |

---

### A7. Low-Value Tests — Remove or Consolidate

These tests only assert constructor defaults, enum string values, or Python language guarantees:

#### Constructor / Default Value Tests (pure dataclass/Pydantic testing)

| File | Test | What it asserts |
|------|------|-----------------|
| `test_agents.py` | `test_default_config` | `config.name == "agent"`, `default_tier == TIER_2` |
| `test_agents.py` | `test_custom_config` | `config.name == "custom"` after `name="custom"` |
| `test_new_agents.py` | `TestArchitectAgent::test_default_config` | `name == "architect"`, `default_tier == TIER_3` |
| `test_new_agents.py` | `TestArchitectAgent::test_custom_config` | Custom values stored correctly |
| `test_new_agents.py` | `TestArchitectAgent::test_initial_state` | `state == CREATED` |
| `test_new_agents.py` | `TestTestAgent::test_default_config` | Default config values |
| `test_new_agents.py` | `TestTestAgent::test_custom_config` | Custom values stored correctly |
| `test_new_agents.py` | `TestTestFile::test_creation` | Dataclass stores constructor values |
| `test_new_agents.py` | `TestFactoryFunctions::test_create_architect_agent` | `isinstance(agent, ArchitectAgent)` |
| `test_new_agents.py` | `TestFactoryFunctions::test_create_test_agent` | `isinstance(agent, TestAgent)` |
| `test_agents_orchestrator.py` | `test_subtask_creation` | Constructor values stored |
| `test_agents_orchestrator.py` | `test_subtask_defaults` | Default values |
| `test_agents_orchestrator.py` | `test_orchestrator_initialization` | `config.name == "test-orchestrator"` |
| `test_agents_orchestrator.py` | `test_input_defaults` | Default values |
| `test_agents_orchestrator.py` | `test_output_defaults` | Default values |
| `test_server_models.py` | `test_dag_node_defaults` | Pydantic default values |
| `test_server_models.py` | `test_agent_info` | Constructor values stored |
| `test_server_models.py` | `test_list_agents_response` | `len == 1` after wrapping one agent |
| `test_server_models.py` | `test_run_summary_defaults` | Default values |
| `test_server_models.py` | `test_runs_summary_response_defaults` | Default values |
| `test_evaluation_scoring.py` | `test_stores_fields` (CriterionFloorResult) | Dataclass field assignment |
| `test_model_router.py` | `test_create_stats` | Zero-initialized counters |
| `test_model_router.py` | `test_create_client` | `backend is None`, `enable_cache` default |

#### Enum / Type Tests (testing Python language guarantees)

| File | Test | What it asserts |
|------|------|-----------------|
| `test_step_state.py` | `test_state_values` | Enum member `.value` strings |
| `test_step_state.py` | `test_state_is_string_enum` | `isinstance(StepState.PENDING, str)` |
| `test_new_agents.py` | `TestTestType::test_values` | `TestType.UNIT.value == "unit"` |
| `test_expressions.py` | `test_step_result_view_fields` | Dataclass stores constructor values |

#### Protocol / API Surface Tests (testing Python runtime, not application logic)

| File | Test | What it asserts |
|------|------|-----------------|
| `test_cross_tier_and_protocol.py` | `test_protocol_used_as_type_hint` | `callable(function)` — always true |
| `test_cross_tier_and_protocol.py` | `test_custom_engine_satisfies_protocol` | Python Protocol `isinstance` check |
| `test_cross_tier_and_protocol.py` | `test_non_conforming_class_fails_check` | Python Protocol `isinstance` check |
| `test_agents_orchestrator.py` | `test_execute_as_dag_exists` | `hasattr` + `callable` — API existence |

#### Trivial / Tautological Assertions

| File | Test | What it asserts |
|------|------|-----------------|
| `test_workflow_runner.py` | `test_run_workflow_loads_builtin` (line 487) | `isinstance(result, type(result))` — always true |
| `test_runner_ui.py` | `test_empty_string_input` | `isinstance(result, str)` on `-> str` function |
| `test_runner_ui.py` | `test_get_flat_model_list_returns_list` | `isinstance(result, list)` on `-> list` function |
| `test_code_execution.py` | `test_tool_properties` | `tool.name == "execute_python"` — static constant |
| `test_phase2d_tools.py` | `test_tool_tiers` | Static tier constants equal themselves |
| `test_cli.py` | `test_server_app_imports_cleanly` | `app is not None` — trivial |

---

### A8. Broken / No-Op Tests — Must Fix or Remove

| File | Test | Problem |
|------|------|---------|
| `test_runner_ui.py` | `test_returns_empty_dict_when_file_missing_and_probe_unavailable` | Test body is a no-op. `with patch(...): pass` with broken mocking. Asserts nothing. |
| `test_provider_adapters.py` | `test_resolves_to_onnx_directory` | Mocking never completed. Assertion `result is None or isinstance(result, Path)` is vacuously true. |
| `test_cli.py` | `test_no_arguments` | Asserts `exit_code == 2 or exit_code == 0` — accepts both success and failure, can never fail. |
| `test_cli.py` | `test_orchestrate_shows_note` | Very loose `or` assertion that accommodates both configured and unconfigured states. |

---

### A9. Outdated / Descoped Tests

| File | Test | Problem |
|------|------|---------|
| `test_agents_orchestrator.py` | `test_execute_as_pipeline_deprecated` | Tests existence of a deprecated API. Should be removed or converted to a proper deprecation warning test. |
| `test_langchain_engine.py` | `TestModelRegistry::test_tier_env_var_override` | Uses `importlib.reload()` to mutate global state — fragile, can cause test-order dependencies. |

---

### A10. Source Code Issue Discovered

**Dead code in `agentic_v2/server/evaluation.py` (lines 102-120):** Unreachable code after a `return` statement. Contains leftover logic (`no_floor_violations`, `grade_capped`, `hard_gates`, `payload` updates) from before the refactoring to `evaluation_scoring.py`. Should be cleaned up.

---

### A11. Consolidation Opportunities (Parametrize)

These test groups should be consolidated into `@pytest.mark.parametrize` tests:

| File | Tests | Consolidation |
|------|-------|---------------|
| `test_step_state.py` | 7 individual `test_valid_transition_*` tests | Single parametrized test with transition table |
| `test_scoring_profiles.py` | `TestProfileE` (4 tests) | Already covered by `TestAllProfilesValid` parametrized tests |
| `test_scoring_profiles.py` | 3 `test_returns_default_for_*` tests | Single parametrized test |
| `test_multidimensional_scoring.py` | `test_elite_above` + `test_low_zero` + `test_high_just_below_elite` | Consolidate boundary tests |
| `test_expressions.py` | `test_evaluate_string_true` + `test_evaluate_string_false` | Single parametrized test |

---

### A12. Misplaced Tests

| File | Test | Should be in |
|------|------|-------------|
| `test_cli.py` | `TestServerApp.test_server_app_imports_cleanly` | `test_server_app.py` or `test_server_routes_health.py` |
| `test_cli.py` | `TestServerApp.test_server_api_routes_registered` | `test_server_app.py` or `test_server_routes_health.py` |

---

## Part B: Coverage Gaps — Modules Needing New Tests

### B1. Critical — Zero Tests, High Complexity

| # | Module | Lines | Risk | Description |
|---|--------|-------|------|-------------|
| 1 | `engine/agent_resolver.py` | 979 | **CRITICAL** | Bridges YAML workflows to LLM execution. Multi-turn tool loops, JSON parsing, prompt assembly. |
| 2 | `tools/llm/model_probe.py` | 2,313 | **CRITICAL** | Model availability detection. Persistent cache, error classification, retry logic. |
| 3 | `tools/agents/benchmarks/llm_evaluator.py` | 777 | **CRITICAL** | Rubric-based 0.0-10.0 scoring. Core evaluation logic. |
| 4 | `tools/agents/benchmarks/evaluation_pipeline.py` | 320 | HIGH | Evaluation orchestration. |
| 5 | `tools/agents/benchmarks/workflow_pipeline.py` | 394 | HIGH | Workflow execution for benchmarks. |
| 6 | `tools/agents/benchmarks/datasets.py` | 310 | HIGH | 10+ benchmark definitions (SWE-bench, HumanEval, etc.). |
| 7 | `tools/agents/benchmarks/loader.py` | 556 | HIGH | On-demand dataset loading. |
| 8 | `tools/agents/benchmarks/registry.py` | 261 | HIGH | Configuration presets. |
| 9 | `tools/core/tool_init.py` | 501 | MEDIUM | Plugin/tool initialization framework. |
| 10 | `tools/core/local_media.py` | 464 | MEDIUM | Media file handling and encoding. |
| 11 | `tools/llm/model_inventory.py` | 528 | MEDIUM | Per-provider API limits, token budgets. |
| 12 | `tools/llm/model_bakeoff.py` | 633 | MEDIUM | Model comparison framework. |
| 13 | `workflows/artifact_extractor.py` | 137 | MEDIUM | Workflow artifact extraction. |
| 14 | `integrations/langchain.py` | 246 | MEDIUM | LangChain integration adapter. |
| 15 | `integrations/otel.py` | 199 | MEDIUM | OpenTelemetry tracing integration. |

### B2. Severely Undertested — Existing but Thin Coverage

| # | Module | Lines | Current Tests | Target | Gap |
|---|--------|-------|--------------|--------|-----|
| 1 | `server/routes/workflows.py` | 1,247 | 9 | 40+ | Streaming, datasets, error paths, pagination |
| 2 | `server/evaluation_scoring.py` | 1,141 | 18 | 50+ | 23 helper functions, multi-stage pipeline |
| 3 | `models/backends.py` | 824 | 11 | 40+ | Per-backend auth, rate limits, streaming, errors |
| 4 | `server/judge.py` | 561 | 4 | 25+ | Calibration, consistency, structured output |
| 5 | `server/datasets.py` | 858 | 0 (dedicated) | 25+ | Needs dedicated test file |
| 6 | `models/model_stats.py` | 380 | 0 (dedicated) | 15+ | Health tracking, circuit state |
| 7 | `workflows/run_logger.py` | 227 | 3 | 12+ | JSON replay logging |
| 8 | `tools/builtin/memory_ops.py` + `context_ops.py` | 570 | 3 | 20+ | Agent memory management |
| 9 | `langchain/models.py` | 811 | 32 | 50+ | Multi-provider model adapters |

### B3. Frontend Gaps

The existing 6 UI test files are clean and well-written, but coverage is narrow:

**Untested components:** JsonViewer, StepNode, WorkflowDAG, Sidebar, LiveStepDetails, NodeConfigOverlay, StepLogPanel, TokenCounter, RunDetail, RunList, RunSummaryCards

**Untested pages:** All 7 (DashboardPage, DatasetsPage, EvaluationsPage, LivePage, RunDetailPage, WorkflowDetailPage, WorkflowsPage)

**Untested hooks:** useRuns, useWorkflows, useNodeConfigUpdate

**Target:** 50+ additional frontend test cases.

### B4. E2E Gaps

Currently only 1 smoke test (`test_subagent_smoke.py`).

**Missing:** Full workflow execution E2E, multi-agent coordination, dataset-backed evaluation, WebSocket streaming end-to-end.

**Target:** 5-10 E2E tests covering critical user flows.

---

## Part C: Testing Strategy & Priorities

### Phase 1: Clean Up (Estimated: ~50 removals)

Remove low-value and duplicate tests to reduce noise and maintenance burden.

1. Delete `test_server_auth.py` and `test_server_websocket.py` (after migrating unique tests)
2. Delete `test_agents_integration.py` (after migrating unique tests to `test_agents_orchestrator.py`)
3. Remove 18 duplicate tests from `test_langchain_engine.py`
4. Remove 5 duplicate tests from `test_langchain_integration.py`
5. Remove 7 duplicate hard-gate tests from `test_server_evaluation.py`
6. Remove 3 duplicate tests from `test_dag.py`
7. Fix or remove 4 broken/no-op tests
8. Remove `test_execute_as_pipeline_deprecated` from `test_agents_orchestrator.py`
9. Clean up dead code in `server/evaluation.py` lines 102-120

### Phase 2: Highest-Impact New Tests

Write tests for the 3 most critical zero-coverage modules:

1. **`test_agent_resolver.py`** — Target 50+ tests covering JSON parsing, tool loops, prompt assembly, error recovery
2. **`test_model_probe.py`** — Target 40+ tests covering caching, error classification, retry logic
3. **`test_llm_evaluator.py`** + **`test_benchmark_pipeline.py`** — Target 60+ tests for scoring logic and pipeline orchestration

### Phase 3: Server Hardening

Expand existing thin test files:

4. Expand `test_server_workflow_routes.py` — 9 → 40+ tests
5. Expand `test_evaluation_scoring.py` — 18 → 50+ tests
6. Expand `test_server_judge.py` — 4 → 25+ tests
7. Expand `test_provider_adapters.py` — 11 → 40+ tests
8. Create `test_server_datasets.py` — 25+ tests

### Phase 4: Fill Remaining Gaps

9. Expand `test_memory_context_tools.py` — 3 → 20+ tests
10. Expand `test_run_logger.py` — 3 → 12+ tests
11. Create `test_tool_init.py`, `test_model_inventory.py`
12. Create `test_artifact_extractor.py`, integration tests

### Phase 5: Frontend & E2E

13. Add UI component tests (pages, hooks, DAG components)
14. Add E2E workflow execution tests

### Verification

After each phase:
```bash
# Backend coverage
cd agentic-workflows-v2 && python -m pytest tests/ -v --cov=agentic_v2 --cov-report=term-missing

# Tools coverage
cd tools && python -m pytest tests/ -v --cov --cov-report=term-missing

# Frontend
cd agentic-workflows-v2/ui && npm run test

# Target: 80% on business logic
```

---

## Appendix: Well-Tested Modules (No Action Needed)

| Module | Lines | Tests | Notes |
|--------|-------|-------|-------|
| `engine/expressions.py` | 480 | 46 | Excellent parametrized tests |
| `models/rate_limit_tracker.py` | 353 | 67 | Thorough edge case coverage |
| `langchain/graph.py` + `runner.py` | 1,355 | 76 | Good integration tests |
| `server/multidimensional_scoring.py` | 527 | 50 | Strong unit tests |
| `models/smart_router.py` + `router.py` | 1,007 | 40 | Good routing logic coverage |
| `agents/base.py` + specialized agents | 1,934 | 75+ | Lifecycle, state machine, memory |
| `contracts/messages.py` + `schemas.py` | 1,041 | 36 | Pydantic model validation |
| `server/auth.py` | 88 | 15 | Complete coverage |
| `server/websocket.py` | 208 | 20 | Complete coverage |
| `langchain/expressions.py` | 153 | 19 | Clean, focused |
| `langchain/config.py` | 285 | 13 | Well-isolated |
| `evaluation/normalization.py` | 35 | 9 | Clean |
| `engine/runtime.py` | 360 | 6 | Distinct, meaningful tests |
| agentic-v2-eval (all modules) | 4,200 | 230 | Best-covered package overall |
| UI (all 6 test files) | 462 | 29 | Clean, behavioral, current |
