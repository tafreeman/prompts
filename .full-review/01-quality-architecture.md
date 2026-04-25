# Phase 1: Code Quality & Architecture Review

## Scope Calibration (Local-Only Learning Platform)

All Phase 1 findings remain relevant — code quality and architecture matter equally for a local learning platform as for production, and arguably more since learners read this code. No re-ranking needed.

## Summary

- **Code Quality (1A):** 2 Critical, 9 High, 14 Medium, 8 Low
- **Architecture (1B):** 2 Critical, 7 High, 9 Medium, 5 Low

---

## Code Quality Findings (Phase 1A)

### Critical

**C1 — Silent exception swallowing in hot paths (`except: pass`)**
*error-handling.* Project standards forbid `except: pass`; grep finds 17+ instances including:
- `agentic-workflows-v2/agentic_v2/langchain/graph_wiring.py:244-245, 255-256, 265-266` — three `except Exception: pass` blocks discard JSON-extraction failures silently.
- `agentic-workflows-v2/agentic_v2/models/smart_router.py:431-433` — `_load_stats()` swallows `JSONDecodeError`/`KeyError`; corrupted stats file silently replaced.
- `agentic-workflows-v2/agentic_v2/langchain/tools.py:434-435`, `agentic_v2/integrations/tracing.py:83-84`.
- `tools/llm/local_model.py` — 8 `except Exception: pass` blocks (229, 238, 240, 254, 265, 317, 386, 459). ONNX provider fallback silently downgrades to CPU.
- `tools/llm/llm_client.py:344-345`, `tools/llm/probe_discovery_providers.py:132, 481`.

**Fix:** Replace `pass` with `logger.debug("...", exc_info=True)` and narrow exception types.

**C2 — Duplicated error-classification logic between router and client wrapper**
*duplication/clean-code.* LLM error classifier duplicated in ≥3 places with subtle divergence:
- `agentic_v2/models/smart_router.py:459-475` (`_classify_and_record_error`) — extracts `error.headers`, updates `RateLimitTracker`.
- `agentic_v2/models/client.py:376-387` — reimplemented inline, **does not** extract headers or feed rate-limit tracker.
- `agentic_v2/langchain/models.py` (`is_retryable_model_error`).

**Fix:** Extract single `classify_llm_error(exc) -> ErrorClassification` frozen dataclass; call everywhere; shared tests.

### High

- **H1** `langchain/graph_wiring.py` exceeds 800-line cap (806); `make_step_node` is 230 lines with nested `_llm_node` (~106 lines). Split into `graph_nodes.py`, `graph_edges.py`, `graph_parsing.py`.
- **H2** `agentic_v2/models/backends_cloud.py:29-431`. Four provider backends (GitHub Models, OpenAI, Anthropic, Gemini) are near-duplicates (200+ repeated lines). Define `OpenAICompatibleBackend` ABC.
- **H3** `agentic_v2/models/client.py:270-394`. `LLMClientWrapper.complete()` is 125 lines and duplicates `call_with_fallback`. Delegate retry/selection to `router.call_with_fallback`.
- **H4** `agentic_v2/langchain/runner.py:85-550`. `WorkflowRunner.invoke/run/stream/astream/resume` replicate ~60-line sequence. Extract `_prepare_execution`/`_finalize_result`.
- **H5** `agentic_v2/engine/step.py:228-460`. `StepExecutor.execute()` is 230+ lines with 5+ levels of nesting inside the retry loop. Review-report regex recovery (`:301-341`) silently fabricates structured field.
- **H6** Eight module-level singletons with `reset_*` test hooks across `models/`, `engine/`, `adapters/`. Adopt DI via `ApplicationContainer`; deprecate `get_*()`.
- **H7** `agentic_v2/langchain/runner.py:121-128, 234-241, 320-324, 505-507`. `try/except TypeError` version-sniffing pattern repeats 5×. Feature-detect once with `inspect.signature`.
- **H8** `agentic_v2/server/evaluation_scoring.py` — 762 lines; `score_workflow_result_impl` at `:470` coordinates rubric resolution, scoring, judge, gates, payload, events. Extract `RubricResolver`, `CriterionScorer`, `HybridScorer`, `PayloadBuilder`.
- **H9** `agentic_v2/server/evaluation_scoring.py:270-281`. `_validate_rubric_weights` references `sorted(known_criteria)` inside branch where `known_criteria` may be `None` — latent `TypeError`.

### Medium

- **M1** `sha256(x).hexdigest()[:16]` hash-truncate pattern in 7+ places. Add `utils/hashing.py::short_hash()`.
- **M2** `graph_wiring.py:336-358` exposes `_create_agent_fn`/`_get_candidates_fn` as underscore-prefixed public parameters (monkeypatch leakage).
- **M3** `Any` pollution in `langchain/graph_wiring.py` (10), `models/backends_cloud.py` (8), `langchain/runner.py` (7), server dataclass-like dicts. Introduce typed `NodeStateUpdate`, `DatasetSampleMeta`, `StepView`.
- **M4** `agentic_v2/integrations/mcp/results/storage.py:76, 124` — MD5 w/ `usedforsecurity=False` has no inline rationale.
- **M5** `agentic_v2/models/smart_router.py:196-201` — `_calculate_cooldown` reaches into `stats._consecutive_failures` private attribute.
- **M6** `agentic_v2/tools/builtin/code_execution.py:207` — `print(json.dumps(output))` in production path.
- **M7** `server/evaluation_scoring.py:598` / `server/datasets.py:526, 608` — 5-exception-wide `except` tuples. Define `JudgeInvocationError` wrapper.
- **M8** `agentic_v2/server/models.py:518` — `RunEvaluationDetail.step_scores` typed as `dict[str, Any]` but callers build a `list`. Introduce `StepScore(BaseModel)`.
- **M9** `agentic_v2/agents/base.py:261-263` — bare `RuntimeError` for max iterations without context. Define `AgentMaxIterationsError`.
- **M10** `agentic-workflows-v2/ui/src/components/runs/RunConfigForm.tsx` — 680 lines, 14+ `useState`, `useEffect` dependency array with 13 items, no `AbortController` on preview fetch. Split into subsections; use `useReducer` for eval state.
- **M11** `agentic-workflows-v2/ui/src/App.tsx` — no shared `<AppLayout>`; sibling pages reimplement topbar/sidebar.
- **M12** `agentic_v2/server/execution.py:100-142` — `_merge_stream_state` mutates input (comment acknowledges but no perf rationale).
- **M13** `agentic_v2/engine/executor.py:371-373` — mutates `step_def.timeout_seconds` as side effect.
- **M14** `agentic_v2/engine/executor.py:214-215` — stores `self._engine_kwargs = kwargs` on shared instance (concurrent race).

### Low

- **L1** `tools/llm/llm_client.py:111` — `LOCAL_MODELS = dict(LOCAL_MODELS)` rebind with no comment.
- **L2** `server/datasets.py:116` — `except` tuple includes redundant `ValueError`.
- **L3** `agentic_v2/engine/step.py:43` — `RetryConfig.retry_on = (Exception,)` default is too broad.
- **L4** `langchain/graph_wiring.py:132-135` — trivial helper `next_iteration`.
- **L5** `agentic_v2/models/client.py:144-147` — `CachedResponse.age_seconds` recomputes `now()` per access.
- **L6** `RunConfigForm` — CompactInputField empty string vs unset.
- **L7** `agentic_v2/engine/step.py:48` — method-scope `import random`.
- **L8** `agentic_v2/models/client.py:221` — `_cache_key` uses `sorted(kwargs.items())` in f-string; objects with non-deterministic `__repr__` produce unstable keys.

### Code Quality Strengths

- Protocol-first design in `core/protocols.py` and `rag/protocols.py` (`@runtime_checkable`).
- Production-grade failover in `SmartModelRouter` (bulkhead semaphores, half-open probe locks, circuit breakers).
- `APIKeyMiddleware` uses `secrets.compare_digest`, supports rotation.
- Pydantic v2 models with `Field`, `field_validator`, `AliasChoices` in `server/models.py`.
- Sanitization middleware chain with `policy` decomposition and `dry_run`.
- RAG `_StoredEntry(frozen=True)`, dict-snapshot iteration, zero-vector + dim validation.
- `AdapterRegistry` clean singleton with test-reset.
- Only 2 `any`/`as any` usages across the UI.

---

## Architecture Findings (Phase 1B)

### Critical

**C1 — `core/` is not engine-agnostic — imports from `engine/`**
*boundaries.* `core/__init__.py` eagerly re-exports `ExecutionContext`, `ServiceContainer`, `EventType`, `DAG`, `CycleDetectedError`, `MissingDependencyError` from `..engine`. Inverts dependency direction; any `import agentic_v2.core` forces engine loading; "engine-agnostic" claim is false.

**Fix:** Move `ExecutionContext`/`ServiceContainer`/`EventType` into `core/context.py`; move DAG data class into `core/dag.py` or `contracts/dag.py`. Route `engine/` to import from `core/`.

**C2 — Name collision on `get_registry()` with silently wrong default**
*api-design/patterns.* Both `AdapterRegistry` (`adapters/registry.py:112`) and `ToolRegistry` (`tools/registry.py:154`) expose `get_registry()`. Top-level `agentic_v2/__init__.py:110` re-exports the tools one. Any consumer doing `from agentic_v2 import get_registry` silently gets wrong registry.

**Fix:** Rename to `get_adapter_registry()` and `get_tool_registry()`; remove top-level alias.

### High

- **H1** `server/routes/workflows.py:33-41,94,108,139` and others import YAML loaders, `compile_workflow`, `validate_workflow_document`, `probe_and_update_tier_defaults` from `..langchain`. ADR-013 makes native DAG the single supported engine; when `langchain` is removed, server fails to boot. **Fix:** Extract to neutral `agentic_v2/workflows/config.py`.
- **H2** `server/execution.py:207-218` hard-branches on engine name (`if adapter_name != "langchain"`) with two different streaming protocols. LangChain path bypasses registry. **Fix:** Unify via `SupportsStreaming.stream()`.
- **H3** Exception hierarchy bypass: `engine/dag.py:19,28` (ValueError), `engine/runtime.py:57` (RuntimeError), `workflows/loader.py:99`, `workflows/runner.py:35`, `integrations/mcp/protocol/client.py:31,37`, `langchain/dependencies.py:8`. Callers `except AgenticError:` miss them. **Fix:** Multi-inherit from `AgenticError` subclass; add regression test.
- **H4** Three overlapping `Severity` enums in `contracts/`: `schemas.py:28` (incl. INFO), `sanitization.py:17` (no INFO), `messages.py:147` (`FindingSeverity`). **Fix:** Collapse to `contracts/severity.py` superset; deprecate others.
- **H5** `server/middleware/__init__.py:60-63` — `SanitizationASGIMiddleware.dispatch` catch-alls on `Exception` and falls through to `call_next`. Silent sanitization bypass on any detector bug. **Fix:** Narrow exceptions; fail-closed by default; add CI test.
- **H6** `adapters/native/engine.py:144-164` — `NativeEngine.get_checkpoint_state` uses `ThreadPoolExecutor(max_workers=1) + asyncio.run()` to call an async store from a sync protocol. Anti-pattern; deadlock risk. **Fix:** Make `SupportsCheckpointing.get_checkpoint_state` async.
- **H7** `models/backends.py:55-62` `PREFIX_MAP` + `models/smart_router.py:20` `_DEFAULT_BULKHEAD_LIMITS` + cost defaults + fallback chains — adding a provider requires edits in ≥3 places. **Fix:** `BackendRegistry` with single `register()` API; defaults next to backend class.

### Medium

- **M1** `agentic_v2/__init__.py` re-exports ~100 symbols (`BaseAgent`, `DAGExecutor`, `SmartModelRouter`, `StepExecutor`, `ExecutionContext`, ...); forces eager subpackage import; vehicle for C2 collision. **Fix:** Trim to narrow API with `__getattr__` lazy loader.
- **M2** TS/Py wire-format drift per ADR-014 is documented but unautomated. **Fix:** `datamodel-code-generator` or `pydantic2ts` in CI.
- **M3** `models/smart_router.py` — 536 lines mixes 6 concerns. Split into `cooldown_policy.py`, `bulkhead.py`, `stats_persistence.py`.
- **M4** Server files at/near 800-line cap: `evaluation_scoring.py` (762), `models.py` (622), `datasets.py` (612), `judge.py` (578), `dataset_matching.py` (561), `multidimensional_scoring.py` (549), `execution.py` (521); plus `engine/step.py` (523), `engine/executor.py` (462).
- **M5** `server/routes/workflows.py` conflates six endpoint groups + in-route YAML validation. Split by concern.
- **M6** `adapters/native/engine.py:236-250` — `NativeEngine._dispatch` uses `isinstance` chain. Violates OCP. **Fix:** Strategy registry.
- **M7** OTEL tracing asymmetric: deep in `rag/`/`engine/`, thin in `models/`/`server/`. No span in model routing or adapter layer.
- **M8** `adapters/registry.py:75,100-103` — 3-tuple `(engine_class, kwargs, instance)` is fragile. Introduce `_AdapterEntry` frozen dataclass.
- **M9** `adapters/langchain/engine.py:62-70` — lazy `runner` property not thread-safe.

### Low

- **L1** `server/websocket.py:34` — verify `validate_event` is called on every broadcast.
- **L2** `contracts/events.py:29-57` — `StepCompleteEvent` vs `StepEndEvent` near-duplicates.
- **L3** `core/protocols.py:190` — `MemoryStore = MemoryStoreProtocol` deprecation in prose only; add `DeprecationWarning`.
- **L4** `core/protocols.py:42-46,192-223` — `VerifierProtocol`/`MiddlewareProtocol` reference `contracts.sanitization.*` lazily.
- **L5** `contracts/` — `StrEnum` vs `str, Enum` inconsistency; standardize on `StrEnum` (3.11+ baseline).

### Architecture Strengths

1. Protocol surface in `core/protocols.py` is cleanly split (`ExecutionEngine`, `SupportsStreaming`, `SupportsCheckpointing`).
2. `AdapterRegistry` with `reset_for_tests()` test hook; thread-safe lazy instantiation.
3. ADR-014 discipline: Pydantic discriminated union + CI snapshot gate.
4. RAG pipeline is well-factored: files <500 lines, protocol-driven, composable `IngestionPipeline`.
5. Cross-package decoupling — `agentic-v2-eval/src` has zero imports from `agentic_v2.*`.
6. ADR discipline: numbered, dated, supersession tracked.
7. `AgenticError` hierarchy where applied (RAG errors root in it).
8. `models/` decoupled from `rag/`; compose only in agents.

---

## Critical Issues for Phase 2 Context

These findings should inform the Security and Performance reviews:

### Security-relevant
- **Sanitization fail-open** (Arch H5): `SanitizationASGIMiddleware` silently bypasses on any exception — directly impacts security posture.
- **Silent exception swallowing** (Quality C1): 17+ instances, several in LLM response handling and stats persistence — error signals for injection/integrity issues lost.
- **MD5 without rationale** (Quality M4): needs security audit of whether the MD5 sites are purely fingerprinting.
- **Error-classification duplication** (Quality C2): divergent rate-limit handling could lead to request amplification on 429s.
- **Wire-format drift** (Arch M2): unautomated TS↔Py mirror is a data-integrity risk.
- **`print(json.dumps(output))` in code_execution** (Quality M6): may leak sensitive content to stdout.

### Performance-relevant
- **Deep nesting in `StepExecutor.execute`** (Quality H5) — hot path; review retry loop for unnecessary allocations.
- **Thread-pool per-call in `NativeEngine.get_checkpoint_state`** (Arch H6) — perf and deadlock risk.
- **Non-thread-safe `LangChainEngine.runner`** (Arch M9) — concurrency hazard.
- **Shared `_engine_kwargs` on singleton** (Quality M14) — concurrency race.
- **Mutating `step_def.timeout_seconds`** (Quality M13) — side effect in hot loop.
- **OTEL coverage gaps** (Arch M7) — can't observe model routing or adapter overhead.
- **Eight singletons + file-lock for `_save_stats`** (Quality H6) — contention; needs load-test.
- **Large files straddling 800-line cap** (Arch M4) — indirect perf/correctness through complexity.
