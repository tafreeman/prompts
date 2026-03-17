# ADR Implementation Review

**Date:** 2026-03-17
**Scope:** Canonical ADRs in [`docs/adr/ADR-INDEX.md`](../adr/ADR-INDEX.md) plus ADR-named historical artifacts in `docs/adr/`
**Method:** Parallel evidence passes across engine/adapters, model routing, scoring, testing, evaluation API, and UI code. Conclusions are based on current repository state, not prior audit snapshots.

## Executive Summary

| ADR | Repo Status | Current Reality | Alignment | Verdict |
| --- | --- | --- | --- | --- |
| ADR-001 | Accepted | Protocol/adapters are real and exercised, but capability-based engine selection is incomplete | ~65% | Partially implemented |
| ADR-002 | Accepted | Most hardening landed; some production-grade resilience pieces are still missing | ~80% | Substantially implemented |
| ADR-003 | Superseded | Legacy CI logic exists as utility code, but the end-to-end workflow described by the ADR is not present | ~20% | Historical fragments only |
| ADR-007 | Proposed | Multidimensional gate exists in code and tests, but is not the default and is not wired into a live deep-research workflow | ~50% | Partially implemented |
| ADR-008 | Proposed | Test cleanup started, but the taxonomy/rules are not yet the canonical enforced workflow | ~35% | Partially implemented |
| ADR-009 | Accepted | Core library changes are in place and tested; runtime adoption is still narrower than the ADR narrative suggests | ~85% | Mostly implemented |
| ADR-010 | Proposed | Reusable primitives exist, but the commit-driven harness itself does not exist | ~10% | Not implemented |
| ADR-011 | Proposed | A few adjacent API primitives exist, but the compare API and eval streaming interface do not | ~15% | Not implemented |
| ADR-012 | Proposed | The current Evaluations page remains a passive table; the comparison hub is not built | ~10% | Not implemented |

## Canonical ADRs

### ADR-001: Dual execution engine

**Decision accuracy**

- Accurate that the repo maintains two execution paths with overlapping intent.
- The decision to introduce a shared abstraction is reflected in current code.

**Implemented evidence**

- `ExecutionEngine`, `SupportsStreaming`, and `SupportsCheckpointing` are defined in `agentic-workflows-v2/agentic_v2/core/protocols.py`.
- The backward-compatible shim in `agentic-workflows-v2/agentic_v2/engine/protocol.py` keeps old imports working.
- The native adapter exists in `agentic-workflows-v2/agentic_v2/adapters/native/engine.py`.
- The LangChain adapter exists in `agentic-workflows-v2/agentic_v2/adapters/langchain/engine.py`.
- The singleton registry exists in `agentic-workflows-v2/agentic_v2/adapters/registry.py`.
- CLI and server adapter selection are real surfaces:
  - `agentic-workflows-v2/agentic_v2/cli/main.py`
  - `agentic-workflows-v2/agentic_v2/server/routes/workflows.py`
- Conformance and adapter tests exist:
  - `agentic-workflows-v2/tests/test_core_protocols.py`
  - `agentic-workflows-v2/tests/test_adapter_registry.py`
  - `agentic-workflows-v2/tests/test_langchain_adapter.py`

**Gaps**

- The ADR called for capability-based routing via an engine selector. No `engine_selector.py`-style dispatch layer exists.
- `OrchestratorAgent.execute_as_dag()` still falls back to constructing `DAGExecutor()` directly when no engine is injected, in `agentic-workflows-v2/agentic_v2/agents/orchestrator.py`.
- The common interface is only partially normalized. The native adapter accepts `DAG`/`Pipeline` objects while the LangChain adapter accepts workflow-name strings, so callers still need engine-specific knowledge.
- No shadow-execution or differential-conformance harness is present.

**Technical soundness**

- Strong on interface design: structural typing plus thin adapters is a sound migration pattern.
- Weaker on operational rigor: without selector logic and conformance checks, behavioral drift between engines remains a live risk.

**Best-practice assessment**

- Good: narrow protocols, adapter registry, checkpoint capability split, optional LangChain import handling.
- Missing: capability-driven dispatch, end-to-end contract tests, and a clearer retirement plan for direct executor bypasses.

### ADR-002: SmartModelRouter hardening

**Decision accuracy**

- The risk model in the ADR still matches the codebase well.
- The implementation has moved materially closer to the ADR than the February audit reported.

**Implemented evidence**

- Monotonic cooldown and recovery timing are implemented in `agentic-workflows-v2/agentic_v2/models/model_stats.py`.
- Provider-aware dual token buckets are implemented in `agentic-workflows-v2/agentic_v2/models/rate_limit_tracker.py`.
- Per-provider bulkhead semaphores and probe locks are implemented in `agentic-workflows-v2/agentic_v2/models/smart_router.py`.
- Cross-tier degradation is implemented in `_cross_tier_search()` and `get_model_for_tier()` in `agentic-workflows-v2/agentic_v2/models/smart_router.py`.
- Extensive tests exist in `agentic-workflows-v2/tests/test_rate_limit_tracker.py` and `agentic-workflows-v2/tests/test_cross_tier_and_protocol.py`.

**Gaps**

- Persistence is still JSON-file based in `SmartModelRouter._save_stats()`, not SQLite/WAL or another multi-process-safe store.
- `Retry-After` parsing only supports delta seconds; HTTP-date handling is still absent.
- There is no explicit adaptive-throttling formula or global system-health load shedding policy.
- Cross-tier fallback returns a lower-tier model, but there is no first-class `degraded_mode` contract surfaced back to callers.
- Capacity-aware redistribution is still approximate; health scoring exists, but explicit provider-capacity weighting does not.

**Technical soundness**

- Good overall. The monotonic-clock fix, bulkheads, probe serialization, and token-bucket modeling are all technically solid.
- The remaining weaknesses are mostly production-hardening gaps rather than design flaws.

**Best-practice assessment**

- Good: monotonic timing, bounded concurrency, provider parsing, focused unit coverage.
- Needs follow-through: multi-process persistence, richer rate-limit parsing, and explicit degraded-service signaling.

### ADR-003: Deep research supervisor / CI gating

**Decision accuracy**

- Historically coherent, but now superseded by ADR-007 for good reasons.
- The old ADR overstates the amount of deep-research workflow machinery that exists today.

**Implemented evidence**

- Legacy CI utilities exist in `agentic-workflows-v2/agentic_v2/workflows/lib/ci_calculator.py`.
- Legacy-gate compatibility still exists in `agentic-workflows-v2/agentic_v2/server/multidimensional_scoring.py`.

**Gaps**

- The `deep_research.yaml` workflow described by the ADR is not present in `agentic-workflows-v2/agentic_v2/workflows/definitions/`.
- Repository docs still claim `deep_research` exists:
  - `agentic-workflows-v2/docs/WORKFLOWS.md`
  - `agentic-workflows-v2/MASTER_MANIFEST.md`
- There is no observable end-to-end supervisor state machine, bounded round graph, targeted remediation round, or `coalesce()`-driven workflow execution path matching the ADR narrative.

**Technical soundness**

- The weighted-CI gate was always vulnerable to compensability problems, and the supersession by ADR-007 is technically justified.
- What remains in code is useful as a scoring utility, not as a faithful implementation of the original supervisor design.

**Best-practice assessment**

- Treat this ADR as historical context, not an active architecture target.

### ADR-007: Multidimensional classification matrix

**Decision accuracy**

- The scoring design described by ADR-007 is reflected well in the scoring module.
- The repo status remains overstated if interpreted as a live workflow capability rather than a library capability.

**Implemented evidence**

- The multidimensional engine exists in `agentic-workflows-v2/agentic_v2/server/multidimensional_scoring.py`.
- Feature-flag and thresholds exist in `agentic-workflows-v2/agentic_v2/config/defaults/evaluation.yaml`.
- Gate, coalesce, and wiring tests exist:
  - `agentic-workflows-v2/tests/test_multidimensional_scoring.py`
  - `agentic-workflows-v2/tests/test_multidimensional_scoring_wiring.py`
  - `agentic-workflows-v2/tests/test_scoring_profiles.py`

**Gaps**

- `evaluation.deep_research.scoring_engine` still defaults to `legacy`.
- The deep-research workflow that should consume this gate is not present in the workflow definitions directory.
- The ADR’s domain-adaptive freshness story is only partially realized. The scoring engine can consume recency inputs, but the end-to-end research workflow that should generate those inputs is missing.
- Sensitivity analysis and confidence/error-bar treatment remain documented open work, not implemented safeguards.

**Technical soundness**

- Stronger than ADR-003. The non-compensatory gate is a sound quality-control approach for research outputs.
- End-to-end completeness is the issue, not the gate math itself.

**Best-practice assessment**

- Good: explicit per-dimension tiers, contradiction veto, separation of gate vs tiebreaker.
- Missing: rollout completion, calibration evidence, and operational integration into a real workflow.

### ADR-008: Testing approach overhaul

**Decision accuracy**

- The ADR correctly identified test-bloat and coverage-gap problems.
- The implementation status in supporting docs is too optimistic if interpreted as “policy is now enforced.”

**Implemented evidence**

- The audit source document exists at `docs/TEST_COVERAGE_ANALYSIS.md`.
- Some duplicate cleanup has clearly happened:
  - duplicate files like `test_server_auth.py`, `test_server_websocket.py`, and `test_agents_integration.py` are gone
  - `agentic-workflows-v2/tests/test_langchain_engine.py` explicitly notes several tests were moved during ADR-008 cleanup
- CI coverage floors are real in `.github/workflows/ci.yml`.

**Gaps**

- The canonical testing rule in `.claude/rules/common/testing.md` still contains only generic guidance; it does not codify the ADR-008 taxonomy or review rules.
- The roadmap still describes key ADR-008 tasks as work to do, in `docs/IMPLEMENTATION_ROADMAP.md`.
- The critical targeted tests called out by the ADR are still absent:
  - no repo tests named `test_agent_resolver.py`
  - no repo tests named `test_model_probe.py`
  - no repo tests named `test_llm_evaluator.py`
  - no repo tests named `test_benchmark_pipeline.py` or `test_workflow_pipeline.py`
- No automated taxonomy enforcement or pre-commit rule was found.

**Technical soundness**

- The ADR itself is strong. It focuses on defect-detection value instead of test count theater.
- Current implementation is still doc-led rather than tool-enforced.

**Best-practice assessment**

- Good strategy, incomplete operationalization.
- The biggest gap is not test philosophy; it is lack of enforcement and lack of follow-through on the highest-risk uncovered modules.

### ADR-009: Scoring enhancements

**Decision accuracy**

- This ADR is materially accurate. The promised improvements are present in code.

**Implemented evidence**

- Immutable constants, recency decay, and config-driven windows are implemented in `agentic-workflows-v2/agentic_v2/workflows/lib/ci_calculator.py`.
- Lexicographic round selection is implemented in `agentic-workflows-v2/agentic_v2/server/multidimensional_scoring.py`.
- Config entries exist in `agentic-workflows-v2/agentic_v2/config/defaults/evaluation.yaml`.
- Tests exist in:
  - `agentic-workflows-v2/tests/test_ci_calculator.py`
  - `agentic-workflows-v2/tests/test_multidimensional_scoring.py`
  - `agentic-workflows-v2/tests/test_multidimensional_scoring_wiring.py`

**Gaps**

- The recency-decay improvements are available as library functionality, but there is no live deep-research workflow proving end-to-end use.
- The ADR’s “implemented and verified” language is somewhat broader than the actual deployment surface.

**Technical soundness**

- Strong. Immutability, config-driven behavior, and deterministic tie-breaking are all sensible improvements.

**Best-practice assessment**

- Good design and good testing discipline.
- Remaining gap is activation, not core implementation quality.

### ADR-010: Commit-driven A/B evaluation harness

**Decision accuracy**

- The methodology is coherent, but the ADR is aspirational rather than implemented.

**Implemented evidence**

- Reusable primitives exist:
  - LLM judge: `tools/agents/benchmarks/llm_evaluator.py`
  - Rubric scorer: `agentic-v2-eval/src/agentic_v2_eval/scorer.py`
  - Reporters: `agentic-v2-eval/src/agentic_v2_eval/reporters/`

**Gaps**

- There is no `tools/commit_eval/` package.
- No `CommitExtractor`, `SandboxManager`, `Comparator`, or compare CLI exists.
- No commit-driven worktree harness or gold-patch comparison flow exists in code.

**Technical soundness**

- Conceptually strong: commit-as-ground-truth is a sound evaluation pattern.
- The “no Docker” decision is acceptable for local experimentation, but would need tighter reproducibility controls for repeatable CI-grade benchmarking.

**Best-practice assessment**

- Good benchmark design direction.
- Missing before adoption: environment capture, deterministic setup, artifact persistence, and security boundaries for untrusted patch execution.

### ADR-011: Eval harness API and interface

**Decision accuracy**

- The intended architecture is reasonable, but it is mostly not present in the repo.

**Implemented evidence**

- A partial evaluation namespace already exists in `agentic-workflows-v2/agentic_v2/server/routes/evaluation_routes.py`.
- The UI client already has `listEvaluationDatasets()` in `agentic-workflows-v2/ui/src/api/client.ts`.
- `connectExecutionStream()` already supports a `pathPrefix` option in `agentic-workflows-v2/ui/src/api/websocket.ts`.

**Gaps**

- No compare endpoints exist (`POST /eval/compare`, `GET /eval/runs`, `GET /eval/runs/{run_id}`).
- No `/ws/eval/{run_id}` backend route exists.
- No comparison-specific Pydantic/API contracts were found.
- No shared `Comparator.run()` core exists to sit behind CLI and API adapters.

**Technical soundness**

- The hexagonal direction is sound.
- The implementation is too incomplete to assess operational behavior.

**Best-practice assessment**

- Reusing the websocket helper is good.
- The backend still needs explicit event contracts, persistence, and a background-job model before this can be considered production-ready.

### ADR-012: UI evaluation hub

**Decision accuracy**

- The current-state audit in the ADR is still directionally right: the Evaluations page is thin.
- The proposed overhaul has not landed.

**Implemented evidence**

- `agentic-workflows-v2/ui/src/pages/EvaluationsPage.tsx` is still a passive scored-runs table.
- The existing page list still centers around the original set of pages in `agentic-workflows-v2/ui/src/pages/`.
- Real-time workflow streaming is already proven in:
  - `agentic-workflows-v2/ui/src/hooks/useWorkflowStream.ts`
  - `agentic-workflows-v2/ui/src/api/websocket.ts`
  - `agentic-workflows-v2/ui/src/pages/LivePage.tsx`

**Gaps**

- No comparison wizard page exists.
- No comparison run page exists.
- No `useEvalStream` hook exists.
- No eval-specific components directory exists.
- No compare routes were added to the UI router.

**Technical soundness**

- Reusing the existing streaming pattern is a good UI architecture choice.
- The proposal remains unproven because it has not been built.

**Best-practice assessment**

- Good additive UX plan.
- Still needs implementation, accessibility review, and responsive validation once built.

## Historical / Non-Canonical ADR-Named Artifacts

These files live in `docs/adr/`, but they are not part of the canonical ADR index and should not be treated as active source-of-truth architecture records.

| Artifact | Current Assessment |
| --- | --- |
| `docs/adr/ADR-002-RAG-Pipeline-Architecture.pdf` | Historical / non-canonical. Not listed in `ADR-INDEX.md`. No current repo-owned implementation program maps cleanly back to it. |
| `docs/adr/ADR-003-Modular-Abstraction-Layer.pdf` | Historical / non-canonical. Appears to overlap with the execution-engine abstraction effort, but the active source of truth is now the indexed markdown ADR set plus current code. |
| `docs/adr/RAG-pipeline-blueprint.md` | Supporting blueprint, not a canonical ADR. It should be evaluated as a design proposal or implementation plan, not as an accepted architecture decision. |
| `docs/adr/DsourcepromptsdocsadrADR-002-RAG-Pi.txt` | OCR/session artifact, not an ADR. Keep as archival context only if it is still needed. |

**Tooling note:** the PDF artifacts could not be inspected line-by-line in this environment because no PDF extraction toolchain is installed. Their classification here is based on repository context, naming, and references rather than full text review.

## Key Repo-Level Mismatches Found During ADR Review

- `agentic-workflows-v2/docs/WORKFLOWS.md` and `agentic-workflows-v2/MASTER_MANIFEST.md` still claim `deep_research.yaml` exists, but it is absent from `agentic-workflows-v2/agentic_v2/workflows/definitions/`.
- `docs/adr/ADR-INDEX.md` still reflected the older February/March audit snapshot before this review.
- ADR-010 through ADR-012 remain design intent, while several supporting docs read more like implementation records.

## Recommended Follow-Up Order

1. Fix documentation drift around `deep_research` before doing more scoring-design work.
2. Finish ADR-001 by adding selector/conformance coverage or explicitly narrowing the intended architecture.
3. Finish ADR-002 persistence and degraded-mode contracts.
4. Decide whether ADR-007 should become the live default; if yes, wire it into a real workflow before more scoring refinements.
5. Either operationalize ADR-008 in canonical testing rules and CI enforcement, or reduce its status claims.
6. Treat ADR-010 through ADR-012 as backlog/spec work until the harness core actually exists.
