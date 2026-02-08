# Workflow Execution + Evaluation Consolidated Plan (v3.3)

| Field | Value |
|---|---|
| Status | approved-for-implementation |
| Date | 2026-02-08 |
| Supersedes | v3.2 draft |
| Decision Set | D1=C, D2=B, D3=C, D4=B, D5=A, D6=A |
| Critical Policy | Scoring + validation are release-blocking gates |
| Reference | `docs/planning/workflow-scoring-evaluation-reference-guide.md` |

---

## Executive Summary

This plan is decision-locked and implementation-ready for phased delivery with parallel workstreams. The execution order is intentionally strict:

1. Stabilize scoring and validation first.
2. Fix runtime correctness and compatibility enforcement.
3. Establish framework-neutral integration contracts.
4. Expand strategies/datasets.
5. Add Microsoft Agent Framework adapter with parity testing.

**Non-negotiable principle:** a workflow run can only pass if hard validation gates pass, regardless of weighted score.

---

## Final Human Decisions (Locked)

| Decision | Selected | Operational Effect |
|---|---|---|
| D1: Scoring policy scope | **C** (workflow-level rubrics) | Each workflow declares rubric/weights; engine executes rubric contract. |
| D2: `plan_implementation` status | **B** (mark experimental) | Keep excluded from default runnable list; migrate schema in parallel. |
| D3: Docker requirement | **C** (Docker optional) | Default runtime is subprocess; Docker is opt-in by config. |
| D4: Phase ordering | **B** (merge into Phase 0) | P0 scoring and validation fixes land before new features. |
| D5: Per-agent scoring priority | **A** (full in Phase 3) | Implement full per-agent evaluation in hybrid scoring phase. |
| D6: Framework integration priority | **A** (Phase 1B + 5B) | Formalize base adapter contract in Phase 1B; Microsoft adapter in Phase 5B. |

---

## Release-Blocking Quality Gates

These gates block promotion to later phases.

1. Hard gates override score (5 required gates per reference guide Layer 0):
- `required_outputs_present=true`
- `overall_status_success=true`
- `no_critical_step_failures=true`
- `schema_contract_valid=true` — evaluation payload matches declared schema
- `dataset_workflow_compatible=true` — dataset fields cover workflow required inputs
- `passed = hard_gates_passed AND weighted_score >= threshold AND no_floor_violations`

2. Criterion floors (reference guide §5):
- `correctness` floor: `>= 0.70` (normalized). If missed, grade capped at `D`.
- `safety/validation` floor: `>= 0.80` (normalized). If missed, grade capped at `D`.
- Floor failures do not override hard gates but cap the maximum achievable grade.

3. Validation-first progression:
- No Phase 1+ completion accepted unless Phase 0 scoring/validation suite is green.

4. Determinism requirements:
- Scoring output must remain within a defined variance band across reruns.

5. Compatibility enforcement:
- Dataset/workflow mismatches fail fast with actionable `422` errors.

6. Contract validation:
- API, SSE, and run-log evaluation payloads must pass schema validation tests.

---

## Scope

### In Scope
1. Scoring hardening, validation hardening, and compatibility contracts.
2. Workflow-level rubric model and per-strategy execution model.
3. Runtime isolation abstraction (subprocess default, Docker optional).
4. Framework-neutral adapter contract.
5. LangChain adapter normalization.
6. Microsoft Agent Framework adapter in later phase with conformance testing.

### Out of Scope (for initial phases)
1. Full enablement of unsupported iterative YAML features in `plan_implementation` during Phase 0.
2. Production rollout of all future benchmark families before core gates are stable.

---

## API, Schema, and Interface Changes

## API Changes

### `POST /api/run` request extensions
- `evaluation.rubric_id` (optional override)
- `evaluation.enforce_hard_gates` (default `true`)
- `execution_profile.runtime` (`subprocess|docker`, default `subprocess`)
- `execution_profile.max_attempts`
- `execution_profile.max_duration_minutes`
- `execution_profile.container_image`

### SSE `evaluation_complete` payload extensions
- `hard_gates`
- `hard_gate_failures`
- `rubric_id`
- `rubric_version`
- `step_scores`
- `agent_scores` (placeholder in Phase 0, full in Phase 3)

### New/Extended Endpoints
- `GET /api/workflows/{name}/capabilities`
- `GET /api/eval/datasets?workflow=<name>` (compatibility-filtered)

## Workflow YAML Extensions

Each workflow definition may declare:
- `experimental: bool`
- `capabilities.inputs[]`
- `capabilities.outputs[]`
- `evaluation.rubric_id`
- `evaluation.weights`

## New/Extended Types

Add or extend types in server/evaluation domain:
- `WorkflowCapability`
- `DatasetDescriptor`
- `RubricDefinition` — must include anchored scale, evidence_required, critical_floor per criterion (ref guide §7)
- `HardGateResult` — 5 required gates
- `StepScore`
- `AgentScore`
- `NormalizationFormula` — formula registry entry (`formula_id`, raw→normalized transform)
- `CriterionResult` — stores `raw_score`, `formula_id`, `normalized_score`, `weight`, `critical_floor`, `floor_passed`
- `ScoringProfile` — workflow-family profile (A-D) with default weights and gate sets

## Scoring Architecture (from Reference Guide)

### Four-Layer Model

| Layer | Purpose | Phase Introduced |
|---|---|---|
| 0: Validation / hard gates | Binary pass/fail eligibility | Phase 0 |
| 1: Objective metrics | Executable tests, pass@k, tool call validity, retrieval metrics | Phase 0 (basic), Phase 3 (full) |
| 2: Rubric / judge metrics | Coherence, instruction following, completeness | Phase 3 |
| 3: Efficiency / cost / ops | p50/p95 runtime, token budgets, retry amplification | Phase 3+ |

### Canonical Scale

- Per-criterion canonical: `0.0..1.0` (normalized)
- Overall display: `0..100` (= normalized × 100)
- Store both `raw_score` and `normalized_score` for every criterion

### Normalization Formulas (formula registry)

| Formula ID | Raw Scale | Transform |
|---|---|---|
| `binary` | `0\|1` | `norm = raw` |
| `likert_1_5` | `1..5` | `norm = (raw - 1) / 4` |
| `likert_neg2_2` | `-2..2` | `norm = (raw + 2) / 4` |
| `lower_is_better` | continuous | `norm = clamp((slo_bad - raw) / (slo_bad - slo_good))` |
| `zero_one` | `0..1` | `norm = clamp(raw)` |
| `pairwise` | wins/losses/ties | `norm = (wins + 0.5×ties) / total` |

Reliability adjustment for small samples: `adjusted_norm = (n × norm + k × prior) / (n + k)` with `prior=0.5, k=20`.

### Deterministic Grading Algorithm

```text
STEP 1: Evaluate hard gates → if any false → passed=false, grade=F
STEP 2: Normalize each criterion via formula_id → check floor violations
STEP 3: weighted_0_1 = sum(weight_i × norm_i) / sum(weight_i)
STEP 4: weighted_100 = round(weighted_0_1 × 100, 2)
STEP 5: Assign grade by band (A≥90, B≥80, C≥70, D≥60, F<60)
STEP 6: If any critical floor failed → cap grade at D
STEP 7: passed = weighted_100 >= threshold AND no floor violations
```

### Workflow-Family Scoring Profiles

| Profile | Workflow Type | Primary Weight | Key Gate |
|---|---|---|---|
| A | Code repair / SWE-style iterative | objective tests: 0.60 | FAIL_TO_PASS==1.0, PASS_TO_PASS≥0.95 |
| B | DAG generation / review | correctness rubric: 0.35 | required outputs present + parseable |
| C | RAG workflows | faithfulness: 0.35 | answer grounded, citations present |
| D | Agentic tool-use / routing | tool selection accuracy: 0.25 | tool call schema valid, no forbidden tools |

Each workflow YAML selects its profile (or declares custom weights). Profile provides default weights and additional hard gates.

### LLM-as-Judge Protocol (Phase 3)

Required controls (from reference guide §8):
1. Use constrained rubric scoring (anchored 1-5 scale), not free-form judgment.
2. Randomize candidate order for pairwise tasks.
3. Run swapped-order adjudication; treat inconsistent outcomes as tie or trigger rerun.
4. Use low temperature and strict structured output schema.
5. Maintain calibration set with human labels; track drift.
6. Log judge model/version/prompt version per run.

### Per-Run Logging Requirements (from reference guide §9)

Every scored run must log:
- workflow id/version, dataset id/version/sample id
- hard gate results and failure reasons
- per-criterion raw + normalized score + formula_id
- final weighted score, grade, passed
- judge model/version/prompt version (when applicable)
- tool call traces and validation outcomes
- runtime/cost/retries

Per step/agent:
- step status, duration, retries, model/tier used
- step-level score outputs

### Anti-Patterns to Avoid

1. Using only one generic score for every workflow type.
2. Allowing weighted score to override failed hard gates.
3. Treating BLEU/ROUGE-only as sufficient quality signal.
4. Relying on uncalibrated judge outputs with no human checks.
5. Ignoring order bias in pairwise judging.
6. No dataset/workflow compatibility guardrails.

---

## Phased Delivery Plan (Parallel Where Possible)

## Phase 0: Stabilization + Validation Foundation (Critical)

**Goal:** eliminate false-positive pass states and enforce evaluation/compatibility correctness.

### Workstream 0A: Scoring hard gates and pass/fail correctness
**Files:**
- `agentic-workflows-v2/agentic_v2/server/evaluation.py`
- `agentic-workflows-v2/agentic_v2/server/routes/workflows.py`
- `agentic-workflows-v2/tests/test_server_evaluation.py`

**Tasks:**
1. Implement hard-gate computation.
2. Enforce final pass formula using hard gates.
3. Add gate details into SSE and run logs.
4. Add deterministic test coverage for null-output and failed-status paths.

### Workstream 0B: Compatibility and input validation
**Files:**
- `agentic-workflows-v2/agentic_v2/server/evaluation.py`
- `agentic-workflows-v2/agentic_v2/server/routes/workflows.py`
- UI workflow/dataset selector components

**Tasks:**
1. Add dataset/workflow capability matching.
2. Enforce `422` on incompatible runs.
3. Enforce non-empty required adapted inputs.
4. Add workflow filter support in dataset listing endpoint.

### Workstream 0C: Workflow-level rubric foundation (Decision D1=C)
**Files:**
- `agentic-workflows-v2/agentic_v2/server/evaluation.py`
- `agentic-workflows-v2/agentic_v2/workflows/definitions/*.yaml`

**Tasks:**
1. Load rubric metadata from workflow definition.
2. Apply workflow rubric by default; allow request override.
3. Validate rubric contract at runtime with actionable errors.
4. Implement normalization formula registry and store raw + normalized scores.
5. Add criterion `critical_floor` support and grade-capping logic.
6. Add `scoring_profile` field to workflow YAML (selects Profile A-D or custom).
7. Implement deterministic grading algorithm (6-step, per reference guide §5.1).

### Workstream 0D: Runtime correctness and stale-path cleanup
**Files:**
- `agentic-workflows-v2/agentic_v2/workflows/runner.py`
- `agentic-workflows-v2/agentic_v2/engine/step.py`
- `docs/reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md`
- `README.md`

**Tasks:**
1. Fix expression resolution for step input mapping `${...}`.
2. Treat unresolved required output as gate failure (not silent success path).
3. Mark `plan_implementation` experimental and exclude from default runnable flows.
4. Clean stale references and publish authoritative tooling map.

### Phase 0 Exit Criteria (Gate A)
1. Null/empty required outputs cannot pass.
2. Incompatible dataset/workflow requests are rejected with clear reasons.
3. Evaluation SSE/log payload schema tests pass.
4. Workflow-level rubric selection works with default and override paths.
5. Scoring determinism tests pass.
6. All 5 hard gates implemented and tested (including `schema_contract_valid` and `dataset_workflow_compatible`).
7. Normalization formulas produce correct `0..1` values for all registered formula types.
8. Criterion floors enforce grade-capping (floor miss → grade capped at D).
9. Both raw and normalized scores stored in evaluation payload.
10. Per-run logging includes all fields specified in reference guide §9.

---

## Phase 1: Runtime Isolation + Adapter Contract

## Workstream 1A: Isolated runtime abstraction (D3=C)
**Objective:** subprocess default, Docker optional.

**Tasks:**
1. Define `IsolatedTaskRuntime` interface.
2. Implement `SubprocessRuntime` as default path.
3. Implement optional `DockerRuntime` with guarded configuration.
4. Add deterministic workspace lifecycle (create, execute, collect, cleanup).

## Workstream 1B: Framework-neutral integration contract (D6=A)
**Files:**
- `agentic-workflows-v2/agentic_v2/integrations/base.py`
- `agentic-workflows-v2/agentic_v2/integrations/langchain.py`

**Tasks:**
1. Define `AgentAdapter`, `ToolAdapter`, `WorkflowAdapter`, `TraceAdapter`.
2. Define canonical event model used by all adapters.
3. Align LangChain integration with the base contract.

### Phase 1 Exit Criteria (Gate B)
1. Core runtime remains framework-independent.
2. LangChain path is contract-conformant.
3. Runtime policy supports subprocess default and Docker opt-in.

---

## Phase 2: Iterative Execution Strategy

**Goal:** introduce robust iterative repair strategy with artifacted attempts.

**Tasks:**
1. Add `ExecutionStrategy` abstraction.
2. Implement `iterative_repair` strategy with policy caps.
3. Emit attempt-level SSE events.
4. Persist attempt artifacts (patches, logs, judge results).
5. Continue schema migration track for `plan_implementation` as experimental.

### Phase 2 Exit Criteria (Gate C1)
1. Iterative loops stop by policy with deterministic behavior.
2. `dag_once` remains backward compatible.

---

## Phase 3: Hybrid Scoring + Full Per-Agent Evaluation (D5=A)

**Goal:** objective-first evaluation with complete agent-level scoring.

**Scoring composition (four-layer model):**
1. Layer 1 — Objective test score (pass@k, fail-to-pass, tool call validity).
2. Layer 2 — LLM judge score with bias-aware protocol (reference guide §8).
3. Layer 3 — Patch similarity advisory score + efficiency/cost metrics.
4. Layer 0 — Hard gates remain mandatory and override all layers.

**LLM-as-Judge requirements (from reference guide §8):**
1. Use anchored rubric scoring (1-5 scale with semantic anchors), not free-form.
2. Randomize candidate order; run swapped-order adjudication for pairwise tasks.
3. Treat inconsistent swapped outcomes as tie or trigger rerun.
4. Low temperature, strict structured output schema.
5. Maintain human-label calibration set; track judge drift.
6. Log judge model/version/prompt version per run.
7. Optional: majority vote across judge models, few-shot prompt, adversarial anti-verbosity check.

**Per-agent scoring dimensions:**
1. Role adherence.
2. Output quality against step rubric (using normalized criterion scores).
3. Efficiency against tier and retry budgets (lower-is-better normalization).
4. Reliability consistency across attempts.

**Reliability adjustment:** apply Bayesian smoothing for agent scores with < 20 samples (`adjusted = (n×score + 20×0.5) / (n + 20)`).

### Phase 3 Exit Criteria (Gate C2)
1. Hybrid score deterministic and validated.
2. Full per-agent score payload available in API/UI/logs.
3. Hard gates remain authority over pass/fail.
4. LLM judge protocol implemented with swapped-order adjudication.
5. Judge calibration baseline established with at least one calibration fixture set.
6. Normalization formulas applied consistently across all scoring layers.

---

## Phase 4: UI Extensibility + Operator Experience

**Goal:** expose compatibility, gates, and iterative evidence clearly.

**Tasks:**
1. Schema-driven run configuration.
2. Compatibility matrix UI.
3. Iteration timeline and artifact explorer.
4. Score breakdown panel with hard-gate visibility.

### Phase 4 Exit Criteria (Gate D)
1. End-to-end dag + iterative run flows validated.
2. Operators can diagnose failures without log scraping.

---

## Phase 5: Dataset Expansion + Microsoft Agent Framework Adapter

## Workstream 5A: Dataset lane expansion
1. Add target benchmark lanes by staged priority.
2. Add smoke matrix checks in CI.

## Workstream 5B: Microsoft Agent Framework adapter (D6=A)
**Files:**
- `agentic-workflows-v2/agentic_v2/integrations/microsoft_agent_framework.py`
- adapter conformance tests

**Tasks:**
1. Implement adapter against base integration contract.
2. Ensure canonical event parity with LangChain path.
3. Add conformance tests on identical workflow fixtures.

### Phase 5 Exit Criteria (Gate E1)
1. Cross-framework parity tests pass for status, required outputs, event completeness.
2. Microsoft adapter documented and operationally testable.

---

## Phase 6: Rollout + Operations

**Goal:** production readiness with observability and rollback safety.

**Tasks:**
1. Add feature flags by strategy/rubric/adapter.
2. Add dashboards for gate failures and score distributions.
3. Add rollout runbooks and rollback procedures.
4. Add CI benchmark gating and incident playbooks.

### Phase 6 Exit Criteria (Gate E2)
1. Release-readiness checks passed.
2. On-call and rollback documentation complete.

---

## Immediate Parallel Task Board (First 2 Weeks)

| ID | Task | Workstream | Est. | Dependency |
|---|---|---|---|---|
| P0-T001 | Hard gates + pass-rule fix | 0A | 1 day | None |
| P0-T002 | SSE/log evaluation payload gate fields | 0A | 0.5 day | P0-T001 |
| P0-T003 | Required output unresolved -> gate fail | 0D | 0.5 day | P0-T001 |
| P0-T004 | Step input `${...}` resolution fix | 0D | 1 day | None |
| P0-T005 | Compatibility filter + mismatch reasons | 0B | 1 day | None |
| P0-T006 | Empty adapted required input rejection | 0B | 0.5 day | None |
| P0-T007 | Workflow rubric load/validation + profiles | 0C | 1.5 day | P0-T001, P0-T010 |
| P0-T008 | Mark `plan_implementation` experimental & hide default | 0D | 0.5 day | None |
| P0-T009 | Authoritative map + stale README cleanup | 0D | 0.5 day | None |
| P0-T010 | Score normalization framework | 0C | 1 day | P0-T001 |
| P0-T011 | Scoring profile templates | 0C | 1 day | P0-T010, P0-T007 |
| P1-T001 | Adapter base interfaces | 1B | 1 day | Gate A |
| P1-T002 | LangChain adapter normalization | 1B | 1 day | P1-T001 |
| P1-T003 | Runtime abstraction (subprocess default, Docker opt-in) | 1A | 2 days | Gate A |

---

## Test Plan

## Unit Tests
1. Hard gate logic — all 5 gates (null outputs, failed status, critical failures, schema contract, dataset compatibility).
2. Normalization math — each formula_id produces correct 0..1 output for boundary and typical values.
3. Grading algorithm — 6-step deterministic algorithm, floor cap behavior, tie-breaker logic.
4. Criterion floor enforcement — floor miss caps grade at D even with high aggregate.
5. Workflow-level rubric selection and override handling.
6. Scoring profile selection — Profile A-D weights applied correctly per workflow type.
7. Input adaptation validation for required non-empty fields.
8. Required output resolution behavior.
9. Expression resolution in step input mapping.
10. Payload schema validation for SSE/log/API evaluation blocks.
11. Raw + normalized score storage — both values present in evaluation output.
12. Reliability adjustment — Bayesian smoothing applied for small sample counts.

## Integration Tests
1. `GET /api/eval/datasets?workflow=` compatibility behavior.
2. `POST /api/run` mismatch rejection with actionable errors.
3. Runtime policy behavior for subprocess and Docker modes.
4. SSE event sequencing for dag and iterative strategies.
5. Artifact persistence and retrieval for iterative attempts.
6. Per-run logging completeness — all fields from reference guide §9 present in run log.
7. Scoring profile end-to-end — workflow with Profile A vs Profile B produces different weight distributions.

## Judge Tests (Phase 3)
1. Swapped-order adjudication — same inputs with swapped order produce consistent result.
2. Structured output schema enforcement — judge response validates against schema.
3. Calibration fixture regression — judge scores on calibration set within tolerance of human labels.

## Conformance Tests (Phase 5B)
1. LangChain vs Microsoft adapter parity for terminal status.
2. Required output parity and non-null checks.
3. Canonical event model completeness and sequence parity.

## E2E Tests
1. UI dataset compatibility gating.
2. Hard-gate visibility and explanation in score panel.
3. Iteration timeline and artifact drill-down for iterative runs.

## Regression / Determinism Tests
1. Fixed fixture set — same inputs produce same score within variance band across 5 reruns.
2. Benchmark smoke runs by workflow family (one dataset per profile).
3. Anti-pattern guards — weighted score alone cannot produce `passed=True` when any hard gate fails.

---

## Risks and Mitigations

| Risk | Severity | Mitigation | Phase |
|---|---|---|---|
| False-positive pass outcomes | Critical | Hard gates mandatory before score pass | 0 |
| Compatibility mismatch noise | Critical | Capability matching + explicit 422 reasons | 0 |
| Scoring instability | High | Determinism thresholds + fixture tests + normalization registry | 0-3 |
| Stale tooling confusion | Medium | Authoritative map + README cleanup | 0 |
| Adapter behavior drift | Medium | Base contract + conformance tests | 1/5 |
| Untrusted code execution risk | High | Runtime isolation, resource controls, teardown | 1+ |
| LLM judge bias (verbosity, position) | High | Swapped-order adjudication + calibration set + low temp | 3 |
| Noisy scores on small samples | Medium | Bayesian reliability adjustment (prior=0.5, k=20) | 3 |
| Single-rubric anti-pattern | Medium | Workflow-family scoring profiles (A-D) | 0 |
| Score opacity for operators | Medium | Raw + normalized dual storage + grade placement explanation | 0+ |

---

## Assumptions and Defaults

1. Decision set is final: `1C, 2B, 3C, 4B, 5A, 6A`.
2. Subprocess runtime is default unless explicitly overridden.
3. `plan_implementation` remains experimental until iterative engine parity lands.
4. Hard gates (all 5) are mandatory for pass/fail in all scoring profiles.
5. Workflow-level rubrics are source of truth unless explicitly overridden per-run.
6. Canonical internal scale is `0.0..1.0` per criterion; display scale is `0..100`.
7. Both raw and normalized scores are stored and logged.
8. Default thresholds: `pass_threshold=70`, `correctness_floor=0.70`, `validation_floor=0.80`.
9. Scoring profiles (A-D) provide defaults; workflows may override with custom weights.
10. LLM judges use low temperature and structured output; calibration set required before production use.

---

## Future Next Steps (Post-Phase 6)

1. Expand Microsoft process patterns as templates: sequential, concurrent, conditional, map-reduce, handoff.
2. Add cross-framework replay tooling for incident reproducibility.
3. Add rubric drift monitoring and auto-calibration workflows.
4. Add adapter certification pipeline for future framework additions.

---
---

# Implementation Tickets

> **Regression policy:** After every ticket, the full existing test suite (`pytest tests/`) and server health check (`GET /api/health`) must pass. After every phase, the UI (`npm run build` + manual smoke: list workflows, view DAG, trigger run, see evaluation) must work with no feature regression.

## How to Run Tests

```bash
# Backend tests (from agentic-workflows-v2/)
python -m pytest tests/ -v

# Single test file
python -m pytest tests/test_server_evaluation.py -v

# UI build check (from agentic-workflows-v2/ui/)
npm run build

# UI unit tests
npm run test

# Server smoke (start server, hit health)
uvicorn agentic_v2.server.app:app --port 8000 &
curl http://localhost:8000/api/health
```

---

## Phase 0 Tickets

### P0-T001: Hard gates + pass-rule fix

| Field | Value |
|---|---|
| Workstream | 0A |
| Est. | 1 day |
| Depends on | None |
| Files | `server/evaluation.py`, `contracts/messages.py` |

**Description:**
Add `compute_hard_gates(result: WorkflowResult, workflow_outputs: dict, eval_payload: dict) -> HardGateResult` to `evaluation.py`. Five gates (per reference guide Layer 0):
1. `required_outputs_present` — every non-optional declared output is non-None in `result.final_output`.
2. `overall_status_success` — `result.overall_status == StepStatus.SUCCESS`.
3. `no_critical_step_failures` — no step has `status == FAILED`.
4. `schema_contract_valid` — evaluation payload matches declared schema (all expected keys present, types valid).
5. `dataset_workflow_compatible` — dataset fields cover workflow required inputs (uses `match_workflow_dataset` from P0-T005).

Add criterion floor checks:
- After normalization, check `correctness >= 0.70` and `safety/validation >= 0.80`.
- If any critical floor fails, cap grade at `D` regardless of aggregate score.

Update `score_workflow_result()` so `passed = hard_gates_all_passed AND weighted_score >= threshold AND no_floor_violations`. Return `hard_gates`, `hard_gate_failures`, `floor_violations`, and `grade_capped` in the scoring dict.

Add `HardGateResult` dataclass (or Pydantic model) and `CriterionFloorResult` to contracts or evaluation module.

**Tests to add (`test_server_evaluation.py`):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_hard_gate_null_output_fails` | Result with `final_output={}` but declared required outputs → `passed=False`, `hard_gate_failures` contains `required_outputs_present` |
| 2 | `test_hard_gate_failed_status_fails` | `overall_status=FAILED`, high score → `passed=False` |
| 3 | `test_hard_gate_critical_step_failure` | One step FAILED, overall SUCCESS → gate fails |
| 4 | `test_hard_gate_schema_contract_invalid` | Payload missing expected keys → gate fails |
| 5 | `test_hard_gate_dataset_incompatible` | Dataset fields don't cover required inputs → gate fails |
| 6 | `test_hard_gate_all_pass_with_score` | All 5 gates pass + score >= threshold + no floor violations → `passed=True` |
| 7 | `test_hard_gate_all_pass_low_score` | All gates pass but score < threshold → `passed=False` |
| 8 | `test_score_result_contains_gate_fields` | `hard_gates`, `hard_gate_failures`, `floor_violations` keys exist in returned dict |
| 9 | `test_criterion_floor_correctness_caps_grade` | `correctness_norm=0.55`, high aggregate → grade capped at D |
| 10 | `test_criterion_floor_all_pass` | All floors met → grade not capped |

**Regression check:** Existing `test_score_workflow_result_includes_all_criteria` must still pass.

---

### P0-T002: SSE/log evaluation payload gate fields

| Field | Value |
|---|---|
| Workstream | 0A |
| Est. | 0.5 day |
| Depends on | P0-T001 |
| Files | `server/routes/workflows.py`, `server/models.py` |

**Description:**
In `_run_workflow_task()`, add `hard_gates`, `hard_gate_failures`, `rubric_id`, `rubric_version`, `step_scores` to the `evaluation_complete` SSE event payload. Ensure the run-logger `extra.evaluation` also includes these fields.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_sse_payload_includes_hard_gates` | Mock a run, capture the dict passed to `websocket.manager.broadcast` for `evaluation_complete`, assert `hard_gates` key present |
| 2 | `test_run_log_evaluation_has_gate_fields` | After logging, load the run JSON, assert `extra.evaluation.hard_gates` exists |
| 3 | `test_sse_payload_schema_validation` | Validate the emitted payload against a schema dict (keys, types) |

**Regression check:** `test_run_workflow_preserves_422_for_invalid_repository_dataset` still passes.

---

### P0-T003: Required output unresolved → gate fail

| Field | Value |
|---|---|
| Workstream | 0D |
| Est. | 0.5 day |
| Depends on | P0-T001 |
| Files | `workflows/runner.py` |

**Description:**
In `WorkflowRunner._resolve_outputs()`, when a non-optional output resolves to `None`, log a warning (already done) AND set a flag/metadata on the `WorkflowResult` (e.g. `result.metadata["unresolved_required_outputs"] = [name]`) so downstream hard-gate logic can pick it up.

**Tests to add (`test_workflow_runner.py`):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_unresolved_required_output_flagged` | Workflow with required output that can't resolve → `result.metadata["unresolved_required_outputs"]` contains the name |
| 2 | `test_resolved_output_no_flag` | All outputs resolve → key absent or empty |

**Regression check:** `TestWorkflowRunnerExecution` suite still green.

---

### P0-T004: Step input `${...}` resolution fix

| Field | Value |
|---|---|
| Workstream | 0D |
| Est. | 1 day |
| Depends on | None |
| Files | `engine/expressions.py`, `engine/dag_executor.py` |

**Description:**
Audit and fix edge cases in `ExpressionEvaluator._resolve_path()` for step input mapping:
- Deeply nested `${steps.X.outputs.Y.Z}` paths.
- Missing intermediate keys should return `None` (not raise).
- Ensure context-stored step data (written by `StepExecutor`) merges correctly with `step_results` param.

**Tests to add (`test_expressions.py`):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_resolve_deep_nested_step_output` | `${steps.parse_code.outputs.ast.functions[0]}` resolves to correct value |
| 2 | `test_resolve_missing_intermediate_returns_none` | `${steps.nonexistent.outputs.foo}` → `None`, no exception |
| 3 | `test_resolve_step_data_from_context_merge` | Step data in context but not in `step_results` param still resolves |
| 4 | `test_resolve_input_mapping_e2e` | Full DAG with step-to-step input wiring resolves correctly |

**Regression check:** Full `TestExpressionEvaluator*` suite passes.

---

### P0-T005: Compatibility filter + mismatch reasons

| Field | Value |
|---|---|
| Workstream | 0B |
| Est. | 1 day |
| Depends on | None |
| Files | `server/evaluation.py`, `server/routes/workflows.py`, `workflows/loader.py` |

**Description:**
1. Add `capabilities` field to `WorkflowDefinition` (loaded from YAML `capabilities.inputs[]` / `capabilities.outputs[]`).
2. Add `match_workflow_dataset(workflow_def, dataset_sample) -> (bool, list[str])` in evaluation.py — checks whether dataset fields cover workflow required inputs.
3. Add `workflow` query param to `GET /api/eval/datasets` — returns only compatible datasets.
4. In `POST /api/run`, before executing, if evaluation is enabled, call the compatibility check; return 422 with reasons on mismatch.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_match_workflow_dataset_compatible` | Dataset with all required fields → `(True, [])` |
| 2 | `test_match_workflow_dataset_missing_field` | Dataset missing required input → `(False, ["missing: code_file"])` |
| 3 | `test_eval_datasets_filtered_by_workflow` | `GET /api/eval/datasets?workflow=code_review` returns subset |
| 4 | `test_run_rejects_incompatible_dataset_422` | POST with mismatched dataset → 422 with reasons in detail |

**Regression check:** `test_list_local_datasets_includes_fixture_files` passes. UI dataset selector still loads.

---

### P0-T006: Empty adapted required input rejection

| Field | Value |
|---|---|
| Workstream | 0B |
| Est. | 0.5 day |
| Depends on | None |
| Files | `server/evaluation.py`, `server/routes/workflows.py` |

**Description:**
After `adapt_sample_to_workflow_inputs()`, check that all required workflow inputs have non-empty values. If any required input is empty/None, reject with 422 before launching the background task.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_reject_empty_required_adapted_input` | Sample that maps to empty string for required input → 422 |
| 2 | `test_accept_empty_optional_adapted_input` | Optional input empty → proceeds fine |
| 3 | `test_accept_full_adapted_inputs` | All inputs populated → 200/accepted |

**Regression check:** `test_adapt_sample_to_workflow_inputs_materializes_file` passes.

---

### P0-T007: Workflow-level rubric load/validation + scoring profiles

| Field | Value |
|---|---|
| Workstream | 0C |
| Est. | 1.5 days |
| Depends on | P0-T001, P0-T010 |
| Files | `server/evaluation.py`, `workflows/loader.py`, `workflows/definitions/*.yaml` |

**Description:**
1. Add optional `evaluation.rubric_id`, `evaluation.weights`, `evaluation.scoring_profile`, and per-criterion `evaluation.criteria[]` to workflow YAML schema.
2. Each criterion entry must support (per reference guide §7):
   - `name`, `definition`, `evidence_required` (what constitutes evidence)
   - `scale` (anchored descriptions for each point, e.g., 1="no evidence", 5="comprehensive")
   - `weight` (float, 0..1)
   - `critical_floor` (optional float, normalized; grade capped at D if norm < floor)
   - `formula_id` (which normalization formula to use)
3. When `score_workflow_result()` is called, load rubric from workflow definition as default; allow `evaluation.rubric` from request to override.
4. Validate: rubric weights must sum to ~1.0 (within tolerance), all referenced criteria must exist, formula_ids must be registered.
5. If `scoring_profile` specified (A-D), apply profile defaults for any missing weights/criteria.
6. Add `evaluation` block to `code_review.yaml` (Profile B) and `fullstack_generation.yaml` (Profile A).

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_rubric_loaded_from_workflow_yaml` | Score uses weights from YAML, not global defaults |
| 2 | `test_rubric_request_override` | Explicit rubric in request overrides YAML |
| 3 | `test_rubric_invalid_weights_rejected` | Weights summing to 0 or negative → actionable error |
| 4 | `test_rubric_missing_uses_global_default` | Workflow with no `evaluation` block → falls back to global |
| 5 | `test_rubric_unknown_formula_id_rejected` | Criterion with unregistered `formula_id` → error |
| 6 | `test_rubric_criterion_has_anchored_scale` | Loaded criterion includes `scale` with anchor descriptions |
| 7 | `test_scoring_profile_applies_defaults` | Profile A workflow → default weights match Profile A template |
| 8 | `test_scoring_profile_overridable` | Explicit weights override profile defaults |

**Regression check:** `test_score_workflow_result_includes_all_criteria` still passes (uses default rubric).

---

### P0-T008: Mark `plan_implementation` experimental & hide from default

| Field | Value |
|---|---|
| Workstream | 0D |
| Est. | 0.5 day |
| Depends on | None |
| Files | `workflows/definitions/plan_implementation.yaml`, `workflows/loader.py` |

**Description:**
1. Add `experimental: true` to `plan_implementation.yaml`.
2. In `WorkflowLoader.list_workflows()`, exclude workflows marked `experimental: true` by default. Add optional `include_experimental=False` param.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_list_workflows_excludes_experimental` | `plan_implementation` not in default list |
| 2 | `test_list_workflows_includes_experimental_flag` | With `include_experimental=True`, `plan_implementation` appears |
| 3 | `test_load_experimental_workflow_still_works` | `loader.load("plan_implementation")` still succeeds (not deleted) |

**Regression check:** `GET /api/workflows` returns `code_review` and `fullstack_generation`. UI workflow list renders.

---

### P0-T009: Authoritative map + stale README cleanup

| Field | Value |
|---|---|
| Workstream | 0D |
| Est. | 0.5 day |
| Depends on | None |
| Files | `README.md`, `docs/reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md` |

**Description:**
1. Create `docs/reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md` listing active modules vs deprecated/stale paths.
2. Clean README.md references to removed or deprecated tooling.
3. No code changes — docs only.

**Tests to add:** None (docs-only). Skipping test run is acceptable; note skip reason.

**Regression check:** N/A.

---

### P0-T010: Score normalization framework

| Field | Value |
|---|---|
| Workstream | 0C |
| Est. | 1 day |
| Depends on | P0-T001 |
| Files | `server/evaluation.py`, `server/normalization.py` (new), `contracts/messages.py` |

**Description:**
Implement normalization framework per reference guide §4:
1. Create `server/normalization.py` with formula registry — dict mapping `formula_id` → normalization function.
2. Implement all 6 core formulas: `binary`, `likert_1_5`, `likert_neg2_2`, `lower_is_better`, `zero_one`, `pairwise`.
3. Add `CriterionResult` type with fields: `raw_score`, `formula_id`, `normalized_score`, `weight`, `critical_floor`, `floor_passed`.
4. Update `score_workflow_result()` to produce `CriterionResult` per criterion, storing both raw and normalized values.
5. All downstream scoring uses normalized values; display/API shows both raw and normalized.
6. Add Bayesian reliability adjustment function: `adjust_for_sample_size(norm, n, prior=0.5, k=20)`.

**Tests to add (`test_normalization.py` — new):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_binary_normalization` | `0 → 0.0`, `1 → 1.0` |
| 2 | `test_likert_1_5_normalization` | `1 → 0.0`, `3 → 0.5`, `5 → 1.0` |
| 3 | `test_likert_neg2_2_normalization` | `-2 → 0.0`, `0 → 0.5`, `2 → 1.0` |
| 4 | `test_lower_is_better_normalization` | Cost below SLO good → 1.0, above SLO bad → 0.0 |
| 5 | `test_zero_one_passthrough_clamps` | `1.5 → 1.0`, `-0.5 → 0.0`, `0.7 → 0.7` |
| 6 | `test_pairwise_normalization` | 3 wins, 1 tie, 1 loss → `(3 + 0.5) / 5 = 0.7` |
| 7 | `test_unknown_formula_id_raises` | Unregistered formula → `KeyError` with available formulas listed |
| 8 | `test_criterion_result_stores_both_scores` | Result has distinct `raw_score` and `normalized_score` |
| 9 | `test_reliability_adjustment_pulls_toward_prior` | `n=5, norm=0.9` → adjusted significantly toward 0.5 |
| 10 | `test_reliability_adjustment_large_n_negligible` | `n=1000, norm=0.9` → adjusted ≈ 0.9 |

**Regression check:** Existing scoring tests pass (they use default `zero_one` normalization).

---

### P0-T011: Scoring profile templates

| Field | Value |
|---|---|
| Workstream | 0C |
| Est. | 1 day |
| Depends on | P0-T010, P0-T007 |
| Files | `server/evaluation.py`, `server/scoring_profiles.py` (new) |

**Description:**
Implement workflow-family scoring profiles per reference guide §3:
1. Create `server/scoring_profiles.py` with `SCORING_PROFILES` dict mapping profile ID → `ScoringProfile`.
2. Define 4 profiles:
   - **Profile A** (code repair / SWE-style): objective tests weight 0.60, code quality 0.20, efficiency 0.10, documentation 0.10. Extra gate: `FAIL_TO_PASS==1.0`.
   - **Profile B** (DAG generation / review): correctness rubric 0.35, code quality 0.30, efficiency 0.20, documentation 0.15. Extra gate: required outputs parseable.
   - **Profile C** (RAG workflows): faithfulness 0.35, relevance 0.30, citation quality 0.20, coherence 0.15. Extra gate: answer grounded.
   - **Profile D** (agentic tool-use): tool selection accuracy 0.25, task completion 0.30, efficiency 0.25, coherence 0.20. Extra gate: tool call schema valid.
3. Add `get_profile(profile_id) -> ScoringProfile` with fallback to default.
4. Integrate with P0-T007: workflow YAML `evaluation.scoring_profile` selects profile.

**Tests to add (`test_scoring_profiles.py` — new):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_profile_a_weights_sum_to_one` | Profile A weights sum to ~1.0 |
| 2 | `test_profile_b_weights_correct` | Profile B has `correctness_rubric=0.35` |
| 3 | `test_get_unknown_profile_fallback` | Unknown ID → returns default profile |
| 4 | `test_profile_extra_gates_included` | Profile A includes `fail_to_pass` gate |
| 5 | `test_workflow_yaml_selects_profile` | Workflow with `scoring_profile: A` → Profile A weights used |
| 6 | `test_explicit_weights_override_profile` | Explicit weights in YAML override profile defaults |

**Regression check:** Existing workflows without `scoring_profile` use default weights.

---

### P0-REGR: Phase 0 Regression Gate

| Field | Value |
|---|---|
| Est. | 0.5 day |
| Depends on | All P0-T00x |

**Description:**
Final Phase 0 verification before moving to Phase 1.

**Checklist:**
1. `python -m pytest tests/ -v` — all green (including all new P0 tests: hard gates, normalization, profiles, floors).
2. `npm run build` in `ui/` — succeeds.
3. `npm run test` in `ui/` — all pass.
4. Start server (`uvicorn`), confirm:
   - `GET /api/health` → 200.
   - `GET /api/workflows` → returns `code_review`, `fullstack_generation` (not `plan_implementation`).
   - `GET /api/eval/datasets` → returns options.
   - `POST /api/run` with valid workflow → run starts, SSE events include `hard_gates`, `floor_violations`, raw + normalized scores.
   - `POST /api/run` with incompatible dataset → 422 with reasons.
   - Schema contract validation fires on malformed evaluation payloads.
5. UI smoke: open browser, list workflows, click DAG view, trigger a run, observe evaluation result with gate fields.
6. Verify scoring profile selection: workflow with `scoring_profile: A` uses Profile A weights.
7. Verify normalization: criterion scores show both raw and normalized values in API response.

---

## Phase 1 Tickets

### P1-T001: Adapter base interfaces

| Field | Value |
|---|---|
| Workstream | 1B |
| Est. | 1 day |
| Depends on | Gate A (Phase 0 complete) |
| Files | `integrations/base.py` (new) |

**Description:**
Create `integrations/base.py` with abstract base classes:
- `AgentAdapter(ABC)` — `async def invoke(prompt, context) -> AgentResponse`
- `ToolAdapter(ABC)` — `async def execute(tool_name, args) -> ToolResult`
- `WorkflowAdapter(ABC)` — `async def run(workflow_def, inputs) -> WorkflowResult`
- `TraceAdapter(ABC)` — `def emit(event: CanonicalEvent) -> None`
- `CanonicalEvent` dataclass — unified event model with `type`, `timestamp`, `step_name`, `data`.

**Tests to add (`tests/test_contracts.py` or new `tests/test_integrations_base.py`):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_agent_adapter_is_abstract` | Cannot instantiate `AgentAdapter` directly |
| 2 | `test_canonical_event_serializable` | `CanonicalEvent` round-trips through JSON |
| 3 | `test_adapter_subclass_contract` | Concrete stub implementing all methods passes isinstance checks |

**Regression check:** Full `pytest tests/` green. Server still starts.

---

### P1-T002: LangChain adapter normalization

| Field | Value |
|---|---|
| Workstream | 1B |
| Est. | 1 day |
| Depends on | P1-T001 |
| Files | `integrations/langchain.py`, `integrations/__init__.py` |

**Description:**
Refactor existing `AgenticChatModel`, `AgenticTool`, and `AgenticAgent` to inherit from the base adapter interfaces. Ensure LangChain import remains optional (graceful `ImportError`).

**Tests to add (`tests/test_langchain_integration.py` or extend existing):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_agentic_chat_model_implements_agent_adapter` | `isinstance(AgenticChatModel(...), AgentAdapter)` |
| 2 | `test_agentic_tool_implements_tool_adapter` | `isinstance(AgenticTool(...), ToolAdapter)` |
| 3 | `test_langchain_unavailable_graceful` | When `langchain_core` not installed, import doesn't crash |
| 4 | `test_canonical_event_emission` | LangChain adapter emits `CanonicalEvent` on invoke |

**Regression check:** All Phase 0 tests green. Server + UI functional.

---

### P1-T003: Runtime abstraction (subprocess default, Docker opt-in)

| Field | Value |
|---|---|
| Workstream | 1A |
| Est. | 2 days |
| Depends on | Gate A |
| Files | `engine/runtime.py` (new), `workflows/runner.py` |

**Description:**
1. Create `IsolatedTaskRuntime(ABC)` with lifecycle: `setup() → execute(cmd, workdir) → collect_artifacts() → cleanup()`.
2. Implement `SubprocessRuntime` — runs tasks via `asyncio.create_subprocess_exec`.
3. Implement `DockerRuntime` — only activated if `execution_profile.runtime == "docker"` and Docker is available. Raises clear error if Docker not found.
4. Wire into `WorkflowRunner` — default is subprocess, Docker is config opt-in.

**Tests to add (`tests/test_runtime.py` — new):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_subprocess_runtime_echo` | `SubprocessRuntime.execute("echo hello")` → stdout contains "hello" |
| 2 | `test_subprocess_runtime_failure` | Non-zero exit → runtime error captured |
| 3 | `test_subprocess_runtime_cleanup` | Temp workdir removed after cleanup() |
| 4 | `test_docker_runtime_not_available` | When Docker missing, raises `RuntimeError` with message |
| 5 | `test_runtime_factory_default_subprocess` | No config → gets `SubprocessRuntime` |
| 6 | `test_runtime_factory_docker_opt_in` | Config `runtime=docker` → gets `DockerRuntime` |

**Regression check:** Existing workflow execution tests pass (subprocess is a transparent wrapper). Server + UI operational.

---

### P1-REGR: Phase 1 Regression Gate

| Field | Value |
|---|---|
| Est. | 0.5 day |
| Depends on | All P1-T00x |

**Checklist:**
1. `python -m pytest tests/ -v` — all green (P0 + P1 tests).
2. `npm run build && npm run test` in `ui/`.
3. Server starts, all API endpoints functional.
4. Workflows execute via subprocess runtime (default behavior unchanged).
5. LangChain integration importable and conformant.
6. UI: list workflows, run workflow, view results — no regressions.

---

## Phase 2 Tickets

### P2-T001: ExecutionStrategy abstraction

| Field | Value |
|---|---|
| Est. | 1 day |
| Depends on | Gate B (Phase 1 complete) |
| Files | `engine/strategy.py` (new), `engine/__init__.py` |

**Description:**
Define `ExecutionStrategy(ABC)` with `async def execute(dag, ctx, ...) -> WorkflowResult`. Extract current DAG execution into `DagOnceStrategy`. Prepare the interface for iterative strategies.

**Tests to add (`tests/test_strategy.py`):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_dag_once_strategy_matches_current_behavior` | Same result as direct `DAGExecutor.execute()` |
| 2 | `test_strategy_factory_default_dag_once` | No config → `DagOnceStrategy` |
| 3 | `test_strategy_is_abstract` | Cannot instantiate `ExecutionStrategy` |

---

### P2-T002: Iterative repair strategy

| Field | Value |
|---|---|
| Est. | 2 days |
| Depends on | P2-T001 |
| Files | `engine/strategy.py`, `engine/iterative.py` (new) |

**Description:**
Implement `IterativeRepairStrategy` — runs DAG, checks pass criteria, if failed, re-runs with feedback up to `max_attempts`. Emits attempt-level SSE events.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_iterative_stops_on_success` | Passes on first attempt → 1 iteration |
| 2 | `test_iterative_retries_on_failure` | Fails first, passes second → 2 iterations |
| 3 | `test_iterative_respects_max_attempts` | Always fails → stops at max, result is FAILED |
| 4 | `test_iterative_emits_attempt_events` | SSE events contain `attempt_number` |
| 5 | `test_dag_once_backward_compatible` | Existing workflows still use dag_once |

---

### P2-T003: Attempt artifact persistence

| Field | Value |
|---|---|
| Est. | 1 day |
| Depends on | P2-T002 |
| Files | `workflows/run_logger.py`, `engine/iterative.py` |

**Description:**
Each iteration's patches, logs, and judge results are saved to `runs/<run_id>/attempts/<N>/`.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_attempt_artifacts_saved` | After iterative run, `attempts/1/` dir exists with log |
| 2 | `test_attempt_artifacts_retrievable` | API or run_logger can list artifacts per attempt |

---

### P2-REGR: Phase 2 Regression Gate

**Checklist:**
1. All Phase 0+1+2 tests green.
2. Existing `dag_once` workflows work identically.
3. UI runs show evaluation results. No regressions on score display.
4. Server starts, all endpoints work.

---

## Phase 3 Tickets

### P3-T001: Hybrid scoring engine + LLM-as-judge protocol

| Field | Value |
|---|---|
| Est. | 3 days |
| Depends on | Gate C1 (Phase 2 complete) |
| Files | `server/evaluation.py`, `server/judge.py` (new) |

**Description:**
Extend `score_workflow_result()` to compose (four-layer model):
1. Layer 1 — Objective test score (existing: pass@k, tool call validity).
2. Layer 2 — LLM judge score (new — call LLM with anchored rubric, structured output).
3. Layer 3 — Patch similarity advisory score + efficiency/cost metrics (lower-is-better normalization).
4. Layer 0 — Hard gates still override all layers.

Create `server/judge.py` implementing LLM-as-judge protocol (reference guide §8):
1. Accept anchored rubric criteria (1-5 scale with semantic anchors).
2. Format prompt with candidate output + rubric + evidence extraction instructions.
3. Use constrained structured output (JSON schema) — enforce `{criteria: [{name, score, evidence}]}`.
4. Implement order randomization: randomly shuffle criteria and candidate sections.
5. Run swapped-order adjudication: for pairwise comparisons, re-run with reversed order; if scores disagree by >1 point on any criterion, flag as inconsistent and either re-run or treat as tie.
6. Low temperature (<=0.1) for determinism.
7. Log judge model, version, prompt version, temperature per evaluation.
8. Maintain calibration fixture set (known human-scored samples); track drift.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_hybrid_score_without_judge` | No LLM judge configured → uses objective + similarity only |
| 2 | `test_hybrid_score_with_mock_judge` | Mock LLM judge → score includes judge component |
| 3 | `test_hybrid_hard_gates_still_override` | High hybrid score but gate fail → `passed=False` |
| 4 | `test_hybrid_score_determinism` | Same inputs → same score (within tolerance band) |
| 5 | `test_judge_structured_output_schema` | Judge response validates against expected JSON schema |
| 6 | `test_judge_swapped_order_consistency` | Two calls with swapped order produce scores within 1 point |
| 7 | `test_judge_calibration_within_tolerance` | Judge on calibration fixture scores within ±0.5 of human labels |
| 8 | `test_judge_logs_model_version` | Judge result includes model/version/prompt_version metadata |

---

### P3-T002: Per-agent scoring + reporting bundle

| Field | Value |
|---|---|
| Est. | 2.5 days |
| Depends on | P3-T001 |
| Files | `server/evaluation.py`, `contracts/messages.py` |

**Description:**
Add `AgentScore` model. For each step/agent, compute: role adherence, output quality, efficiency (tier/retry budget using `lower_is_better` normalization), reliability. Include `agent_scores[]` in evaluation payload.

Apply Bayesian reliability adjustment for agents with < 20 scored runs:
`adjusted_norm = (n × score + 20 × 0.5) / (n + 20)` (reference guide §6).

Add statistical reporting bundle to evaluation output (reference guide §10):
- `mean_score`, `stdev`, `min`, `max` per criterion across dataset samples.
- `grade_distribution` (count of each grade A-F across samples).
- `floor_violation_count` per criterion.
- `hard_gate_failure_rate` per gate.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_agent_score_per_step` | Each step in result gets an `AgentScore` entry |
| 2 | `test_agent_score_efficiency_penalty` | Excessive retries → lower efficiency score |
| 3 | `test_agent_scores_in_sse_payload` | `evaluation_complete` event has `agent_scores` array |
| 4 | `test_agent_score_with_no_agent_role` | Step without explicit agent → graceful default |
| 5 | `test_reliability_adjustment_small_n` | Agent with 5 runs → score adjusted toward 0.5 prior |
| 6 | `test_reliability_adjustment_large_n` | Agent with 100 runs → adjustment negligible |
| 7 | `test_reporting_bundle_per_criterion` | Multi-sample eval → `mean_score`, `stdev` per criterion present |
| 8 | `test_reporting_bundle_grade_distribution` | Grade distribution sums to sample count |

---

### P3-REGR: Phase 3 Regression Gate

**Checklist:**
1. All Phase 0–3 tests green.
2. Scoring backwards-compatible — existing rubrics produce same ballpark scores.
3. SSE payloads validate against extended schema.
4. UI still renders evaluation results (agent_scores are additive, don't break existing display).

---

## Phase 4 Tickets

### P4-T001: Schema-driven run configuration

| Field | Value |
|---|---|
| Est. | 2 days |
| Depends on | Gate C2 (Phase 3 complete) |
| Files | UI `src/` components |

**Description:**
UI dynamically renders run configuration form from workflow input schema (already partially here via `/api/workflows/{name}/dag` returning `inputs`). Extend to show rubric options and runtime config.

**Tests to add (vitest):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_run_form_renders_inputs` | Workflow with 2 inputs → form shows 2 fields |
| 2 | `test_run_form_enum_shows_dropdown` | Enum input → select element with options |
| 3 | `test_run_form_optional_not_required` | Optional field not marked required in form |

---

### P4-T002: Compatibility matrix UI

| Field | Value |
|---|---|
| Est. | 1 day |
| Depends on | P4-T001 |
| Files | UI components |

**Description:**
Dataset selector greys out or hides incompatible datasets based on `GET /api/eval/datasets?workflow=<name>`.

**Tests to add (vitest):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_dataset_list_filters_by_workflow` | Only compatible datasets shown |
| 2 | `test_incompatible_dataset_disabled` | Incompatible entry has disabled state |

---

### P4-T003: Score breakdown panel with hard-gate visibility

| Field | Value |
|---|---|
| Est. | 1.5 days |
| Depends on | P4-T001 |
| Files | UI components |

**Description:**
After a run completes, show: criteria scores, weights, weighted total, grade, hard gate pass/fail for each gate. If a gate failed, show which one and why.

**Tests to add (vitest):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_score_panel_renders_criteria` | All criteria shown with scores |
| 2 | `test_score_panel_shows_gate_failures` | Failed gate highlighted in red |
| 3 | `test_score_panel_passed_state` | All gates pass → green passed badge |

---

### P4-T004: Iteration timeline and artifact explorer

| Field | Value |
|---|---|
| Est. | 2 days |
| Depends on | P2-T003, P4-T001 |
| Files | UI components |

**Description:**
For iterative runs, show timeline of attempts with expandable details: attempt number, status, score, artifacts. Click to drill into logs/patches.

**Tests to add (vitest):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_timeline_renders_attempts` | 3-attempt run → 3 timeline nodes |
| 2 | `test_timeline_final_highlighted` | Last attempt visually distinct |

---

### P4-REGR: Phase 4 Regression Gate

**Checklist:**
1. All backend tests green (no backend changes in Phase 4).
2. `npm run build && npm run test` — all pass.
3. Full UI smoke: list, DAG, run, evaluate, score panel, dataset selector, iteration timeline.
4. Server health + all API endpoints functional.

---

## Phase 5 Tickets

### P5A-T001: Dataset lane expansion

| Field | Value |
|---|---|
| Est. | 2 days |
| Depends on | Gate D (Phase 4 complete) |
| Files | `tests/fixtures/datasets/`, evaluation config |

**Description:**
Add new benchmark dataset fixtures for additional workflow types. Add CI smoke matrix that runs each dataset against compatible workflows at tier 0.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_new_datasets_valid_json` | All new fixture files parse as valid JSON |
| 2 | `test_new_datasets_have_required_fields` | Each sample has `prompt` or `task_description` |
| 3 | `test_compatibility_smoke_matrix` | Each dataset compatible with at least one workflow |

---

### P5B-T001: Microsoft Agent Framework adapter

| Field | Value |
|---|---|
| Est. | 2 days |
| Depends on | P1-T001, Gate D |
| Files | `integrations/microsoft_agent_framework.py` (new) |

**Description:**
Implement `MicrosoftAgentAdapter(AgentAdapter)` against the base contract. Maps Microsoft Agent Framework primitives to the canonical event model.

**Tests to add (`tests/test_microsoft_adapter.py`):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_microsoft_adapter_implements_contract` | `isinstance(adapter, AgentAdapter)` |
| 2 | `test_microsoft_adapter_emits_canonical_events` | Events match `CanonicalEvent` schema |
| 3 | `test_microsoft_adapter_import_optional` | Missing MS SDK → graceful ImportError |

---

### P5B-T002: Cross-framework conformance tests

| Field | Value |
|---|---|
| Est. | 1 day |
| Depends on | P5B-T001, P1-T002 |
| Files | `tests/test_adapter_conformance.py` (new) |

**Description:**
Run identical workflow fixtures through both LangChain and Microsoft adapters. Assert parity on: terminal status, required output presence, event sequence, event count.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_status_parity` | Both adapters produce same terminal status for same fixture |
| 2 | `test_output_parity` | Both produce non-null required outputs |
| 3 | `test_event_sequence_parity` | Both emit same event types in same order |
| 4 | `test_event_completeness` | Both emit `workflow_start` + `step_*` + `workflow_end` |

---

### P5-REGR: Phase 5 Regression Gate

**Checklist:**
1. All Phase 0–5 tests green.
2. Existing LangChain and dag_once paths unaffected.
3. Microsoft adapter documented.
4. UI still fully functional.

---

## Phase 6 Tickets

### P6-T001: Feature flags

| Field | Value |
|---|---|
| Est. | 1 day |
| Depends on | Gate E1 (Phase 5 complete) |
| Files | `config/`, `server/evaluation.py`, `engine/strategy.py` |

**Description:**
Add feature flag config for: iterative strategy, per-agent scoring, Microsoft adapter, Docker runtime. Flags default to `false` in prod, `true` in dev. Read from config YAML or env vars.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_feature_flag_disabled_hides_feature` | Flag off → iterative strategy not available |
| 2 | `test_feature_flag_enabled_exposes_feature` | Flag on → iterative strategy available |
| 3 | `test_feature_flag_env_override` | Env var overrides config file |

---

### P6-T002: Rollout runbooks and rollback procedures

| Field | Value |
|---|---|
| Est. | 1 day |
| Depends on | P6-T001 |
| Files | `docs/operations/` (new) |

**Description:**
Write operational runbooks for: enabling features, rolling back flag changes, incident response for scoring failures. Docs-only.

**Tests to add:** None (docs-only).

---

### P6-T003: CI benchmark gating

| Field | Value |
|---|---|
| Est. | 1 day |
| Depends on | P6-T001 |
| Files | CI config, `scripts/` |

**Description:**
Add CI step that runs tier-0 benchmark smoke against all non-experimental workflows. Gate: all must pass hard gates. Failure blocks merge.

**Tests to add:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_ci_smoke_script_exits_zero` | Script runs against fixtures → exit 0 |
| 2 | `test_ci_smoke_script_exits_nonzero_on_failure` | Bad fixture → exit 1 |

---

### P6-T004: Promotion policy automation

| Field | Value |
|---|---|
| Est. | 1.5 days |
| Depends on | P6-T001, P3-T002 |
| Files | `server/evaluation.py`, `scripts/promotion_check.py` (new) |

**Description:**
Implement promotion policy checks per reference guide §11:
1. **Non-inferiority check:** new version must score >= baseline − δ (δ=0.02 by default) on each criterion.
2. **Floor regression detection:** if a criterion that previously passed its floor now fails, block promotion.
3. **Minimum sample requirement:** promotion requires ≥ N scored runs (N=10 default).
4. **Reporting:** generate promotion report with per-criterion comparison, trend direction, pass/block verdict.
5. Integrate as optional post-evaluation step callable from CLI and CI.

**Tests to add (`test_promotion.py` — new):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_promotion_passes_when_better` | New scores > baseline → pass |
| 2 | `test_promotion_blocks_on_regression` | Criterion drops by > δ → block with reason |
| 3 | `test_promotion_blocks_floor_regression` | Floor that previously passed now fails → block |
| 4 | `test_promotion_requires_min_samples` | Only 3 runs → insufficient samples, block |
| 5 | `test_promotion_report_structure` | Report has per-criterion comparison and verdict |

---

### P6-REGR: Phase 6 / Final Regression Gate

**Checklist:**
1. Full `pytest tests/` — all green.
2. `npm run build && npm run test` — all green.
3. Server starts with all features flagged on/off — both modes work.
4. Full UI smoke with all features enabled.
5. CI smoke script passes.
6. Rollback: disable all Phase 1+ flags → system behaves like Phase 0 baseline.

---

## Complete Ticket Summary

| ID | Title | Phase | Est. | Depends | Test Count |
|---|---|---|---|---|---|
| P0-T001 | Hard gates (5) + pass-rule + floor checks | 0 | 1d | — | 10 |
| P0-T002 | SSE/log gate fields | 0 | 0.5d | T001 | 3 |
| P0-T003 | Unresolved output → gate fail | 0 | 0.5d | T001 | 2 |
| P0-T004 | Step input `${...}` fix | 0 | 1d | — | 4 |
| P0-T005 | Compatibility filter + 422 | 0 | 1d | — | 4 |
| P0-T006 | Empty required input rejection | 0 | 0.5d | — | 3 |
| P0-T007 | Workflow rubric + profiles | 0 | 1.5d | T001, T010 | 8 |
| P0-T008 | Mark experimental + hide | 0 | 0.5d | — | 3 |
| P0-T009 | Docs cleanup | 0 | 0.5d | — | 0 |
| P0-T010 | Score normalization framework | 0 | 1d | T001 | 10 |
| P0-T011 | Scoring profile templates | 0 | 1d | T010, T007 | 6 |
| P0-REGR | Phase 0 regression gate | 0 | 0.5d | all P0 | — |
| P1-T001 | Adapter base interfaces | 1 | 1d | Gate A | 3 |
| P1-T002 | LangChain normalization | 1 | 1d | T001 | 4 |
| P1-T003 | Runtime abstraction | 1 | 2d | Gate A | 6 |
| P1-REGR | Phase 1 regression gate | 1 | 0.5d | all P1 | — |
| P2-T001 | ExecutionStrategy ABC | 2 | 1d | Gate B | 3 |
| P2-T002 | Iterative repair strategy | 2 | 2d | T001 | 5 |
| P2-T003 | Attempt artifacts | 2 | 1d | T002 | 2 |
| P2-REGR | Phase 2 regression gate | 2 | 0.5d | all P2 | — |
| P3-T001 | Hybrid scoring + LLM judge | 3 | 3d | Gate C1 | 8 |
| P3-T002 | Per-agent scoring + reporting | 3 | 2.5d | T001 | 8 |
| P3-REGR | Phase 3 regression gate | 3 | 0.5d | all P3 | — |
| P4-T001 | Schema-driven run config UI | 4 | 2d | Gate C2 | 3 |
| P4-T002 | Compatibility matrix UI | 4 | 1d | T001 | 2 |
| P4-T003 | Score breakdown panel | 4 | 1.5d | T001 | 3 |
| P4-T004 | Iteration timeline UI | 4 | 2d | T001 | 2 |
| P4-REGR | Phase 4 regression gate | 4 | 0.5d | all P4 | — |
| P5A-T001 | Dataset expansion | 5 | 2d | Gate D | 3 |
| P5B-T001 | MS Agent Framework adapter | 5 | 2d | Gate D | 3 |
| P5B-T002 | Cross-framework conformance | 5 | 1d | T001 | 4 |
| P5-REGR | Phase 5 regression gate | 5 | 0.5d | all P5 | — |
| P6-T001 | Feature flags | 6 | 1d | Gate E1 | 3 |
| P6-T002 | Rollout runbooks | 6 | 1d | T001 | 0 |
| P6-T003 | CI benchmark gating | 6 | 1d | T001 | 2 |
| P6-T004 | Promotion policy automation | 6 | 1.5d | T001, P3-T002 | 5 |
| P6-REGR | Final regression gate | 6 | 0.5d | all P6 | — |
| **Total** | | | **~39d** | | **~113 tests** |
