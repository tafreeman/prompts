# Phase 3: Testing & Documentation Review

## Scope Calibration (Local-Only Learning Platform)

This is a local-developer-workstation learning platform. All **testing** findings remain fully relevant. Many **documentation** findings are production-ops concerns and are re-ranked below.

---

## Summary

- **Testing (3A):** 4 Critical, 9 High, 10 Medium, 5 Low
- **Documentation (3B, after calibration):** 2 Critical, 5 High, 10 Medium, 9 Low

---

## Test Coverage Findings (Phase 3A) — no re-ranking needed

### Critical

- **C1** No test for sanitization middleware fail-open (Sec C2). `tests/test_middleware_integration.py`, `tests/test_auth.py`. Inject exploding detector; assert 500 not 200 (xfail until fix lands).
- **C2** No shell-blocklist bypass corpus (Sec C1). Only `rm -rf /` literal in `test_phase2d_tools.py:255`. Add parametrized fixture `tests/fixtures/shell_bypass_corpus.py` with double-space/abs-path/unicode-fullwidth/command-substitution/chained vectors.
- **C3** Eval expression injection escapes untested (Sec H4). `tests/test_expressions.py:353-378` only covers `__import__`/`print`/`lambda`. Missing: `__class__.__mro__[1].__subclasses__()`, `{}.__class__.__mro__[-1].__subclasses__()`, `().__class__.__base__`, `__builtins__`, `__globals__`.
- **C4** Zero concurrent-run tests for the engine (Perf C2, H4, H5, H7). Grep for `asyncio.gather|concurrent|cross.contaminat` in engine tests returns 0. Add `tests/slo/test_concurrent_runs.py` with 20 parallel runs + distinct `timeout_seconds`, assert no crosstalk.

### High

- **H1** Subpackages with no test file: `agentic_v2/config/`, `agentic_v2/integrations/mcp/discovery/`, `integrations/mcp/adapters/resource|prompt`, `integrations/mcp/runtime/manager.py`, `integrations/mcp/transports/{websocket,stdio}.py`, `agents/implementations/claude_{agent,sdk_agent}.py`.
- **H2** Path containment default-open assumption untested. `tests/test_settings.py:14` shows `AGENTIC_FILE_BASE_DIR` default None; no test asserts file_ops refuses absolute paths when unset.
- **H3** Auth default-open: `tests/test_auth.py:187-197` asserts the *opposite* of Sec H2 ask — that no API key allows all. **Locally fine; still worth a regression guard if an allow-unauth flag is introduced.**
- **H4** Code-execution sandbox escape vectors — no tests for `getattr/__class__/__mro__`, `__builtins__['__import__']`, f-string introspection, env-var exfil via `os.environ` in the sandbox. Only `os.system`/`import subprocess` literal scans covered.
- **H5** `run_id` path traversal untested. `tests/test_server_workflow_routes.py` has 0 hits for `traversal|passwd|\.\.`. Parametrize `run_id="../../etc/passwd"`, `"..\\..\\windows"`, `"a/b/c"`, `"\x00xyz"` → expect 400/422.
- **H6** `tests/slo/` directory exists in scope but empty. No p95/p99 latency gates, no vectorstore-query regression threshold, no embedding throughput bound. Create `tests/slo/test_latency_budgets.py` with explicit budgets.
- **H7** Stream backpressure only partially tested (Perf M7/M8). `test_websocket.py:170-182` uses instant `AsyncMock` — no slow-consumer test where `send_json` awaits 10s while fast consumer must not block.
- **H8** Multi-worker stats divergence untested (Perf C3). **Informational for local-only use, but two-instance merge test is still useful for correctness.**
- **H9** `test_code_safety:65-69` locks in regrettable behavior (syntax errors pass safety check). Replace with AST-based detection positive tests.

### Medium

- **M1** E2E footprint is 1 file. Add `tests/e2e/test_workflow_full_run.py` with `AGENTIC_NO_LLM=1`, full run + WS connection + event sequence assert.
- **M2** Five test files exceed 700 LOC: `test_evaluation_scoring.py` (1,121), `test_langchain_engine.py` (1,044), `test_engine.py` (898), `test_server_judge.py` (826), `test_server_evaluation.py` (792), `test_rag_memory.py` (782), `test_rate_limit_tracker.py` (732), `test_expressions.py` (628). Four over the 800-line rule.
- **M3** `_reset_llm_client` autouse fixture doesn't reset `SmartModelRouter`; easy to miss in new tests → bleed under `-n auto`.
- **M4** `tests/integrations/mcp/conftest.py:18-22` custom `event_loop` fixture is deprecated pattern on pytest-asyncio 0.21+ with `asyncio_mode="auto"`.
- **M5** 10 test files contain `asyncio.sleep`/`time.sleep` — 18 occurrences. `test_rate_limit_tracker.py:54` clock math band is CI-GC-sensitive.
- **M6** `test_http_post_tool`/`test_http_get_tool` — verify `http_test_server_base_url` fixture is local aiohttp, not `httpbin.org`. If remote, mark `@pytest.mark.integration`.
- **M7** `except` pass paths lack `caplog` assertions that a structured log is emitted.
- **M8** No accessibility tests in `ui/`; no `jest-axe`; no Storybook visual regression.
- **M9** WebSocket origin allowlist test minimal: no null-origin, subdomain confusion, protocol downgrade, CRLF-in-Origin.
- **M10** Single golden snapshot (`tests/golden/code_review_output.json`). No full run-trace JSON snapshot for `workflow_start`→`workflow_end` events.

### Low

- **L1** `test_tier0.py` mixes 5 concerns in 408 lines — split.
- **L2** `test_expressions.py:453` uses `== None` (intentional `_NullSafe.__eq__` probe) — add `# noqa: E711`.
- **L3** `_mock_load_config` duplicated 6× in `test_server_workflow_routes.py` — extract fixture.
- **L4** Heavy `MagicMock` usage (231 occurrences across 40 files). Sweep for "tests that test mocks" per ADR-008.
- **L5** Vitest coverage export — confirm `vitest run --coverage` is in CI.

### Testing Strengths

1. Excellent fixture hygiene for singleton isolation; xdist-aware `conftest.py`.
2. `tests/test_schema_drift.py` snapshot discipline on 16 Pydantic contracts.
3. Dedicated `AGENTIC_NO_LLM=1` tests (`tests/models/test_no_llm_mode.py`, `tests/langchain/test_no_llm_mode_langchain.py`) — 94 refs across 8 files.
4. Parametrized injection/unicode/secrets corpora drive detectors — good template for closing C2/C3 gaps.
5. Schema-validated WebSocket broadcast (`test_websocket.py:202-212`).
6. Deep `_NullSafe`/`coalesce` Tier-1 tests in `test_expressions.py`.
7. 20+ auth middleware cases in `test_auth.py`.
8. `tests/e2e/test_cross_package.py` import-coherence gate.

---

## Documentation Findings (Phase 3B) — calibrated for local-only use

### Critical (retained)

**D1 — FastAPI endpoints lack OpenAPI metadata; `/docs` is thin**
`agentic_v2/server/routes/*.py`. Grep finds only 16 `summary=`/`description=`/`responses=` across ~20 endpoints. For a learning platform, the live `/docs` page is a primary teaching surface — fix this. Promote the richly written `docs/api-contracts-runtime.md` content into route decorators; commit `docs/openapi.json` snapshot with drift gate.

**D2 — Engine consolidation migration path is incomplete (ADR-013)**
`docs/MIGRATIONS.md §4`. Learners importing from `agentic_v2.langchain` have no concrete API mapping (`langchain.WorkflowRunner` → `AdapterRegistry.get("native")`) or feature-parity table. Also, `agentic-workflows-v2/README.md` still lists `langchain` as a base install extra with no deprecation note.

### High (retained — teaching-quality concerns)

**D3 — Install path divergence**
Root README says `just setup`; dev guide says `uv sync` + `pip install -e "..."`; docs disagree. Pick one, make others defer.

**D4 — Cross-language coherence (ADR-014) not mentioned in UI contributor guide**
`ui/README.md` doesn't mention the events codegen flow (`tests/schemas/events.schema.json` → `events.generated.ts`). `KNOWN_LIMITATIONS.md §1.3` says "hand-maintained" but `CONTRIBUTING.md` says "must never be hand-edited" — contradictory. Resolve.

**D5 — ADR frontmatter inconsistency + index count off**
ADR-001-002-003 combined; ADRs 007-012 "Proposed" with non-zero implementation %; ADR-INDEX.md line 5 says 14 ADRs but lists 13.

**D6 — CHANGELOG missing version-diff links and date discipline in `[Unreleased]`**

**D7 — Onboarding references commands that may not exist**
`agentic list adapters` (not in CLI); `uvicorn agentic_v2.server.app:create_app --factory` vs. `agentic_v2.server.app:app` inconsistency; `agentic compare` in CLAUDE.md not in README CLI section. Generate a single `docs/CLI_REFERENCE.md` from `typer --help`.

**D8 — `AGENTIC_NO_LLM=1` onboarding contradiction**
`docs/NO_LLM_MODE.md` exists and is good, but root README says "at least one provider required"; `KNOWN_LIMITATIONS.md §3.1` still says no placeholder mode exists. Resolve; add `AGENTIC_NO_LLM=1` to Quick Start as the zero-config path.

**D9 — ML-practices rules don't match repo reality**
`.claude/rules/common/ml-practices.md` mandates DVC/MLflow/pandera/model cards — none exist in this repo (it's an agentic-orchestration platform, not an ML training shop). Trim the rule or retitle to "Agentic Reproducibility."

### Medium (retained for learner UX)

- **D10** `AGENTS.md` references `decks-generated/CLAUDE.md` (legacy/extracted).
- **D11** Dual `ARCHITECTURE.md` (`agentic-workflows-v2/docs/ARCHITECTURE.md` is stale vs. `docs/ARCHITECTURE.md` umbrella).
- **D12** Hard-coded count drift: root README says "78+ test files" (actual 100+); `tools/README.md` says 10 providers, root says 8+.
- **D13** Glossary doesn't cover wire-format/sanitization/scoring terms (floor violation, RRF, BM25, circuit-breaker states, DORA scoring).
- **D14** DAG executor lacks inline algorithm-stepping comments mapping to README description.
- **D15** Pydantic `Field(description=...)` sparse in `contracts/events.py` — loses TS JSDoc on generated types.
- **D16** Workflow YAML lacks top-level purpose/rationale comments — a missed pedagogical opportunity.
- **D17** Agent persona prompts don't all follow the required sections (Expertise/Boundaries/Critical rules/Output format).
- **D18** Deep-dive docs have "Generated: 2026-04-17" LOC counts — drift likely.
- **D19** No `docs/LEARNING_PATH.md` ordering onboarding → architecture → worked walkthrough → pattern catalog → ADR reading order.

### Low (kept)

- **D20** `.env.example` has rate-limit comments for Gemini/Anthropic but not OpenAI/Azure/GitHub Models — normalize or move all to `docs/RATE_LIMITS.md`.
- **D21** No documented dependency management policy (when to `uv sync`, when to commit `uv.lock`).
- **D22** `CONTRIBUTING.md §8` links `SECURITY.md` at root but file is under `agentic-workflows-v2/`.
- **D23** UI README `n/j/k` shortcuts "(reserved)" — state planned vs. unbound clearly.
- **D24** `CODE_OF_CONDUCT.md` only at package, not repo root (GitHub health).
- **D25** UI README backend proxy default says `:8000`; rest of docs use `:8010`.
- **D26** Storybook mentioned in CLAUDE.md + deployment-guide but "Not installed by default" — resolve whether extracted.
- **D27** `docs/DEMO.md` — dry-run the three commands; update if any fail.
- **D28** Nested READMEs lack "Parent docs: [link]" breadcrumbs.

### De-scoped for local-only use (moved out of findings)

The following Phase 3B findings are **production-operations concerns** and do not apply to a local-developer-workstation learning platform. They are documented here for completeness but should not drive remediation work:

- Default-open auth warning at entry points
- SSE authentication story
- Multi-worker / concurrency constraint doc
- Tool safety model as an operator-facing threat-model doc (the learner-facing tool reference is still in scope — see D16/D19)
- Operational runbooks / on-call / incident response
- CORS and WebSocket origin model as security doc
- Compliance / data-retention / GDPR docs
- Security headers (CSP/HSTS) documentation

### Documentation Strengths (retained)

1. `CONTRIBUTING.md` — genuine enabler; PR checklist, docs-mapping table, ADR rubric, CI-gate contract.
2. `CHANGELOG.md [0.3.0]` — honest Epic breakdown including "Epic 4 tombstone".
3. `KNOWN_LIMITATIONS.md` — brave structured Status/Workaround/Upstream-fix per entry.
4. `MIGRATIONS.md` — clean per-entry structure, `presentation/` extraction is exemplary.
5. ADR-013 and ADR-014 — well-written decision records.
6. `docs/ARCHITECTURE.md` umbrella + per-package deep-dive pattern.
7. `docs/NO_LLM_MODE.md` — thorough operator-oriented reference.
8. `.env.example` — richly commented.
9. `prompts/coder.md` persona — sentinel blocks, stack-adaptation table, few-shot examples; model for other personas.
10. `docs/api-contracts-runtime.md` — detailed; gap is only that it's not reflected in the live OpenAPI spec (D1).
11. Onboarding "5 minutes / 1 hour" scoped structure.
