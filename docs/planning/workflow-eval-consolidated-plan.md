# Workflow Execution + Evaluation Plan (v4.0)

| Field | Value |
|---|---|
| Status | in-progress |
| Updated | 2026-02-08 |
| Supersedes | v3.3 consolidated plan (sequential phases replaced with parallel waves) |
| Decision Set | D1=C, D2=B, D3=C, D4=B, D5=A, D6=A |
| Critical Policy | Scoring + validation are release-blocking gates |
| Reference | `docs/planning/workflow-scoring-evaluation-reference-guide.md` |

---

## How to Use This Document

This is a **living shared plan** for all agents and contributors. When you complete a ticket:

1. Change its status from `pending` to `done` in the ticket table below.
2. Add a one-line completion note with date (e.g., `Done 2026-02-08 — 10 tests added`).
3. Run the regression checklist for the ticket's wave before marking the wave complete.
4. Do NOT remove completed tickets — they serve as audit trail.

---

## Executive Summary

The plan delivers workflow evaluation hardening, runtime isolation, iterative execution strategies, hybrid scoring, UI improvements, framework adapters, and operational tooling.

**Phase 0 is complete.** All remaining work is organized into 4 parallel waves based on true dependency analysis, compressing ~39 days of sequential work into ~10-12 calendar days across 4 concurrent tracks.

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

These gates apply to all waves and block promotion.

1. Hard gates override score (5 required gates per reference guide Layer 0):
- `required_outputs_present=true`
- `overall_status_success=true`
- `no_critical_step_failures=true`
- `schema_contract_valid=true` — evaluation payload matches declared schema
- `dataset_workflow_compatible=true` — dataset fields cover workflow required inputs
- `passed = hard_gates_passed AND weighted_score >= threshold AND no_floor_violations`

2. Criterion floors (reference guide S5):
- `correctness` floor: `>= 0.70` (normalized). If missed, grade capped at `D`.
- `safety/validation` floor: `>= 0.80` (normalized). If missed, grade capped at `D`.

3. Determinism requirements:
- Scoring output must remain within a defined variance band across reruns.

4. Compatibility enforcement:
- Dataset/workflow mismatches fail fast with actionable `422` errors.

5. Contract validation:
- API, SSE, and run-log evaluation payloads must pass schema validation tests.

---

## Scope

### In Scope
1. Scoring hardening, validation hardening, and compatibility contracts.
2. Workflow-level rubric model and per-strategy execution model.
3. Runtime isolation abstraction (subprocess default, Docker optional).
4. Framework-neutral adapter contract.
5. LangChain adapter normalization.
6. Microsoft Agent Framework adapter with conformance testing.

### Out of Scope (for initial waves)
1. Full enablement of unsupported iterative YAML features in `plan_implementation`.
2. Production rollout of all future benchmark families before core gates are stable.

---

## API, Schema, and Interface Changes

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
- `agent_scores` (placeholder in Phase 0, full in Wave 2)

### New/Extended Endpoints
- `GET /api/workflows/{name}/capabilities`
- `GET /api/eval/datasets?workflow=<name>` (compatibility-filtered)

### Workflow YAML Extensions
Each workflow definition may declare:
- `experimental: bool`
- `capabilities.inputs[]`
- `capabilities.outputs[]`
- `evaluation.rubric_id`
- `evaluation.weights`

### New/Extended Types
- `WorkflowCapability`
- `DatasetDescriptor`
- `RubricDefinition` — anchored scale, evidence_required, critical_floor per criterion (ref guide S7)
- `HardGateResult` — 5 required gates
- `StepScore`
- `AgentScore`
- `NormalizationFormula` — formula registry entry (`formula_id`, raw->normalized transform)
- `CriterionResult` — stores `raw_score`, `formula_id`, `normalized_score`, `weight`, `critical_floor`, `floor_passed`
- `ScoringProfile` — workflow-family profile (A-D) with default weights and gate sets

---

## Scoring & Evaluation Specification

> This section is self-contained. It incorporates all scoring, grading, rubric, and evaluation rules from the reference guide so agents do not need to cross-reference a second document.

### Core Principles

1. Evaluate in layers, not one number.
2. Prefer executable/objective metrics where possible.
3. Use rubric/judge scoring for quality dimensions objective metrics cannot capture.
4. Normalize metrics into a common scale only after per-metric validation.
5. Calibrate automated scoring against humans on a recurring cadence.
6. Track bias and variance for LLM-as-judge.

### Four-Layer Scoring Model

| Layer | Purpose | Introduced |
|---|---|---|
| 0: Validation / hard gates | Binary pass/fail eligibility | Foundation (done) |
| 1: Objective metrics | Executable tests, pass@k, tool call validity, retrieval metrics | Foundation basic (done), Wave 1 full |
| 2: Rubric / judge metrics | Coherence, instruction following, completeness | Wave 1 |
| 3: Efficiency / cost / ops | p50/p95 runtime, token budgets, retry amplification | Wave 2+ |

#### Layer 0 — Hard Gates (binary)

Required gates (all must pass for eligibility):

- `required_outputs_present` — every non-optional declared output is non-None
- `overall_status_success` — `result.overall_status == SUCCESS`
- `no_critical_step_failures` — no step has `status == FAILED`
- `schema_contract_valid` — evaluation payload matches declared schema
- `dataset_workflow_compatible` — dataset fields cover workflow required inputs

Optional workflow-specific gates:

- `tests_fail_to_pass_all_green`
- `tests_pass_to_pass_threshold_met`
- `citations_present_for_claims`
- `tool_call_schema_valid`

Rule: `passed = hard_gates_passed AND weighted_score >= pass_threshold AND no_floor_violations`

#### Layer 1 — Objective Metrics (preferred)

- Executable tests, pass@k, fail-to-pass rate, pass-to-pass rate
- Tool call validity and argument correctness
- Retrieval ranking metrics (nDCG/MAP/MRR) and retrieval coverage
- Latency, retries, failure rate

#### Layer 2 — Rubric / Judge Metrics

- Coherence, instruction following quality, completeness, code review quality
- Documentation and communication quality
- Use structured scoring with anchored definitions (1-5), then normalize

#### Layer 3 — Efficiency / Cost / Operations

- p50/p95 runtime
- Token/cost budgets
- Retry amplification
- Infrastructure stability

### Canonical Scale

- Per-criterion canonical: `0.0..1.0` (normalized)
- Overall display: `0..100` (= normalized x 100)
- Store both `raw_score` and `normalized_score` for every criterion

### Normalization Formulas (formula registry)

All formulas use `clamp(x) = min(1, max(0, x))`. All normalized outputs are `0.0..1.0`.

| Formula ID | Raw Scale | Transform | Example |
|---|---|---|---|
| `binary` | `0\|1` | `norm = raw` | `1 -> 1.0` |
| `likert_1_5` | `1..5` | `norm = (raw - 1) / 4` | `3 -> 0.5` |
| `likert_neg2_2` | `-2..2` | `norm = (raw + 2) / 4` | `0 -> 0.5` |
| `lower_is_better` | continuous | `norm = clamp((slo_bad - raw) / (slo_bad - slo_good))` | latency SLO good=8s, bad=30s, raw=12s -> `0.818` |
| `zero_one` | `0..1` | `norm = clamp(raw)` | `0.7 -> 0.7`, `1.5 -> 1.0` |
| `pairwise` | wins/losses/ties | `norm = (wins + 0.5*ties) / total` | 3W/1T/1L -> `0.7` |

SWE-style test metrics (computed separately, then fed as criteria):

- `fail_to_pass = passed_fail_to_pass / total_fail_to_pass`
- `pass_to_pass = passed_pass_to_pass / total_pass_to_pass`
- Hard gates enforced separately: `fail_to_pass == 1.0` and `pass_to_pass >= 0.95`

Retrieval metrics already in `0..1` (nDCG/MAP/MRR/Recall@k): `norm = clamp(raw)`

#### Reliability Adjustment for Small Samples

`adjusted_norm = (n * norm + k * prior) / (n + k)` with `prior=0.5, k=20`

- Store both `norm` and `adjusted_norm`
- Use `adjusted_norm` for promotion decisions
- Example: `n=5, norm=0.9` -> `adjusted = (5*0.9 + 20*0.5) / 25 = 0.58`
- Example: `n=1000, norm=0.9` -> `adjusted ~= 0.9`

### Deterministic Grading Algorithm

```text
INPUT:
  hard_gates: map[str, bool]
  criteria: list[{name, raw_score, formula_id, weight, critical_floor?}]
  pass_threshold: number (default 70)

STEP 1: Evaluate hard gates
  if any hard gate is false:
    return passed=false, grade=F, reason="hard_gate_failure"

STEP 2: Normalize criteria
  for each criterion i:
    norm_i = normalize(raw_score_i, formula_id_i)
    floor_failed_i = critical_floor_i exists AND norm_i < critical_floor_i

STEP 3: Aggregate score
  weighted_0_1 = sum(weight_i * norm_i) / sum(weight_i)
  weighted_100 = round(weighted_0_1 * 100, 2)

STEP 4: Assign provisional grade by band
  A >= 90, B >= 80, C >= 70, D >= 60, else F

STEP 5: Apply floor cap
  if any floor_failed_i:
    grade = min(grade, D)

STEP 6: Final pass/fail
  passed = (weighted_100 >= pass_threshold) AND (no floor_failed_i)
```

### Grade Placement Guide

What determines grade placement — use this for explaining why a run landed in a grade band:

- **A (90-100):** All hard gates pass, all critical floors pass with margin (>= floor + 0.10), no severe validation/safety defects, low judge disagreement.
- **B (80-89.99):** All hard gates pass, floors pass, limited non-critical defects, objective metrics strong but not best-in-class.
- **C (70-79.99):** All hard gates pass, floors pass near boundary, acceptable baseline quality with clear improvement items.
- **D (60-69.99):** At least one critical floor failed (grade-capped) or multiple material quality gaps.
- **F (<60 or any hard-gate failure):** Release-blocking failure.

Tie-breakers when two runs have near-equal weighted scores (`abs(diff) < 1.0`):

1. Lower hard-gate failure count.
2. Higher objective correctness score.
3. Higher safety/validation score.
4. Lower p95 latency and cost.

### Operational Thresholds (defaults, tune with calibration data)

- `pass_threshold`: `70`
- `correctness floor`: `0.70` (normalized)
- `validation/safety floor`: `0.80` (normalized)
- `PASS_TO_PASS floor` for SWE-style: `0.95`
- `FAIL_TO_PASS` for SWE-style: `1.00`
- `inconsistent pairwise judge rate` warning threshold: `> 0.10`

### Workflow-Family Scoring Profiles

Each workflow YAML selects its profile (or declares custom weights). Profile provides default weights and additional hard gates.

#### Profile A: Code repair / SWE-style iterative

Primary use: issue resolution against real repositories.

Hard gates:

- Patch applies cleanly
- `FAIL_TO_PASS == 1.0`
- `PASS_TO_PASS >= 0.95`
- No sandbox/security policy violations

Weighted profile:

- objective tests: `0.60`
- judge quality rubric: `0.25`
- patch similarity/semantic diff quality: `0.10`
- efficiency/cost: `0.05`

Note: This profile is test-dominant by design.

#### Profile B: DAG generation / review (non-executable dominant)

Primary use: design/review/generation where direct execution is partial.

Hard gates:

- Required outputs present and parseable
- Critical steps succeeded
- Output schema valid

Weighted profile:

- correctness rubric: `0.35`
- completeness rubric: `0.25`
- tool/data precision: `0.20`
- documentation quality: `0.10`
- efficiency: `0.10`

#### Profile C: RAG workflows

Hard gates:

- Answer grounded in retrieved context
- Citation/link requirements met
- High-severity hallucination checks clear

Weighted profile:

- faithfulness/groundedness: `0.35`
- response relevance: `0.25`
- context precision: `0.20`
- context recall/coverage: `0.10`
- efficiency: `0.10`

#### Profile D: Agentic tool-use and routing

Hard gates:

- Tool call JSON/schema valid
- No forbidden tool invoked
- Handoff graph rules respected

Weighted profile:

- tool selection accuracy: `0.25`
- argument correctness/F1: `0.25`
- handoff accuracy: `0.20`
- final task correctness: `0.20`
- efficiency: `0.10`

### Rubric Authoring Standard

Each rubric criterion must include:

- `name` — criterion identifier
- `definition` — what is being measured
- `evidence_required` — what constitutes evidence for scoring
- `scale` — anchored descriptions for each score point (e.g., 1-5)
- `weight` — float, 0..1
- `critical_floor` — optional float (normalized); grade capped at D if norm < floor
- `formula_id` — which normalization formula to use

#### Anchored 1-5 Semantic Scale

- **1:** Fails core requirement, major errors
- **2:** Partially correct, significant gaps
- **3:** Acceptable baseline, clear issues remain
- **4:** Strong quality, minor issues
- **5:** Excellent, complete and robust

#### Example YAML Rubric

```yaml
rubric_id: fullstack_generation_v1
version: 1
criteria:
  - name: correctness
    scale: [1, 5]
    weight: 0.35
    critical_floor: 3
    formula_id: likert_1_5
    definition: "Output satisfies functional requirements and constraints."
    evidence_required:
      - "Requirement-to-output mapping"
      - "No contradiction with input spec"
    anchors:
      "1": "Major requirement failures"
      "2": "Multiple significant errors"
      "3": "Minimum acceptable correctness"
      "4": "Accurate with minor issues"
      "5": "Fully correct and robust"
  - name: code_quality
    scale: [1, 5]
    weight: 0.30
    formula_id: likert_1_5
    definition: "Code follows best practices, is readable, maintainable."
    evidence_required:
      - "Linting pass"
      - "No obvious anti-patterns"
    anchors:
      "1": "Unreadable, major anti-patterns"
      "2": "Significant quality issues"
      "3": "Acceptable, some issues"
      "4": "Clean, minor improvements possible"
      "5": "Exemplary code quality"
```

### LLM-as-Judge Protocol (Wave 1)

Required controls:

1. Use constrained rubric scoring (anchored 1-5 scale), not free-form judgment.
2. Randomize candidate order for pairwise tasks.
3. Run swapped-order adjudication; treat inconsistent outcomes (disagree by >1 point) as tie or trigger rerun.
4. Use low temperature (<=0.1) and strict structured output schema.
5. Maintain calibration set with human labels; track drift.
6. Log judge model/version/prompt version per run.

Optional stronger controls:

- Majority vote across judge families/models
- Few-shot judge prompt for consistency
- Adversarial anti-verbosity checks

Structured output schema to enforce:

```json
{
  "criteria": [
    {"name": "correctness", "score": 4, "evidence": "..."},
    {"name": "code_quality", "score": 3, "evidence": "..."}
  ]
}
```

### Per-Run Logging Requirements

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

### Statistical Reporting Bundle

Every evaluation batch must produce:

- `pass_rate` — fraction of runs that passed
- `weighted_score_mean` and `weighted_score_stdev`
- `hard_gate_failure_rate` by gate type
- per-criterion `mean`, `stdev`, `min`, `max` distribution
- `grade_distribution` — count of each grade A-F
- `floor_violation_count` per criterion
- top failure reasons

### Promotion Policy

A candidate version promotes only if all hold:

1. Hard-gate failure rate is not worse than baseline by threshold.
2. Weighted score improves or is non-inferior within tolerance (delta=0.02).
3. No critical criterion floor regression (previously passed, now fails).
4. No increase in severe validation/security failures.
5. Minimum N scored runs (N=10 default).

### Anti-Patterns to Avoid

1. Using only one generic score for every workflow type.
2. Allowing weighted score to override failed hard gates.
3. Treating BLEU/ROUGE-only as sufficient quality signal.
4. Relying on uncalibrated judge outputs with no human checks.
5. Ignoring order bias in pairwise judging.
6. No dataset/workflow compatibility guardrails.

---

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

> **Regression policy:** After every ticket, the full existing test suite (`pytest tests/`) and server health check (`GET /api/health`) must pass. After every wave, the UI (`npm run build` + manual smoke: list workflows, view DAG, trigger run, see evaluation) must work with no feature regression.

---

# Completed: Foundation (formerly Phase 0)

All foundation tickets are **done**. This section is retained as audit trail.

| ID | Title | Status | Tests | Notes |
|---|---|---|---|---|
| P0-T001 | Hard gates (5) + pass-rule + floor checks | **done** | 10 | `compute_hard_gates()`, `HardGateResult` in evaluation.py |
| P0-T002 | SSE/log gate fields | **done** | 3 | `hard_gates`, `hard_gate_failures` in SSE payload |
| P0-T003 | Unresolved output -> gate fail | **done** | 2 | `unresolved_required_outputs` metadata in runner.py |
| P0-T004 | Step input `${...}` fix | **done** | 4 | Expression evaluator edge cases fixed |
| P0-T005 | Compatibility filter + 422 | **done** | 3 | `match_workflow_dataset()` in evaluation.py |
| P0-T006 | Empty required input rejection | **done** | 3 | 422 on empty required adapted inputs |
| P0-T007 | Workflow rubric + profiles | **done** | 6+ | Rubric load from YAML, request override, validation |
| P0-T008 | Mark experimental + hide | **done** | 2 | `experimental: true` in plan_implementation.yaml, loader filtering |
| P0-T009 | Docs cleanup | **partial** | 0 | `ACTIVE_VS_LEGACY_TOOLING_MAP.md` not yet created |
| P0-T010 | Score normalization framework | **done** | 9 | `server/normalization.py` — all 6 formulas + Bayesian adjustment |
| P0-T011 | Scoring profile templates | **done** | 4 | `server/scoring_profiles.py` — Profiles A-D |

**Key files produced:**
- `agentic_v2/server/evaluation.py` — `compute_hard_gates()`, `match_workflow_dataset()`, `score_workflow_result()`
- `agentic_v2/server/normalization.py` — formula registry, 6 normalization transforms, `adjust_for_sample_size()`
- `agentic_v2/server/scoring_profiles.py` — `ScoringProfile` dataclass, Profiles A-D, `get_profile()`
- `agentic_v2/workflows/runner.py` — `unresolved_required_outputs` metadata flag
- `agentic_v2/workflows/loader.py` — `list_workflows(include_experimental=)` filtering
- `workflows/definitions/plan_implementation.yaml` — `experimental: true`

---

# Parallel Execution Plan

## Dependency Graph

```
Foundation (DONE)
  |
  +-- [Wave 1] -------- all start immediately, no inter-dependencies --------+
  |   |                                                                       |
  |   +-- Track A: Runtime ---- W1-RT-001 runtime abstraction                |
  |   +-- Track B: Adapters --- W1-AD-001 base interfaces                    |
  |   |                           +-> W1-AD-002 LangChain normalization      |
  |   +-- Track C: Scoring ---- W1-SC-001 hybrid scoring + LLM judge        |
  |   +-- Track D: Data ------- W1-DA-001 dataset expansion                  |
  |   +-- Track E: UI --------- W1-UI-001 schema-driven run config          |
  |                                                                           |
  +-- [Wave 2] ---- after Wave 1 track dependencies resolve -----------------+
  |   |                                                                       |
  |   +-- Track A: Strategy --- W2-ST-001 strategy ABC (needs W1-RT-001)     |
  |   |                           +-> W2-ST-002 iterative repair             |
  |   +-- Track B: Per-agent -- W2-AG-001 per-agent scoring (needs W1-SC-001)|
  |   +-- Track C: UI --------- W2-UI-001 compat matrix (needs W1-UI-001)   |
  |   |                         W2-UI-002 score breakdown (needs W1-SC-001)  |
  |   +-- Track D: Adapter ---- W2-AD-001 MS adapter (needs W1-AD-001)      |
  |                                                                           |
  +-- [Wave 3] ---- after Wave 2 track dependencies resolve -----------------+
  |   |                                                                       |
  |   +-- W3-ART-001 attempt artifact persistence (needs W2-ST-002)          |
  |   +-- W3-UI-001 iteration timeline UI (needs W3-ART-001)                 |
  |   +-- W3-AD-001 cross-framework conformance (needs W2-AD-001)            |
  |   +-- W3-FL-001 feature flags (all features exist to flag)               |
  |                                                                           |
  +-- [Wave 4] ---- finalization --------------------------------------------|
      |                                                                       |
      +-- W4-CI-001 CI benchmark gating                                      |
      +-- W4-PR-001 promotion policy automation                              |
      +-- W4-DOC-001 rollout runbooks + P0-T009 tooling map                  |
```

---

## Wave 1 — Immediate Start (all independent, Foundation gate passed)

All Wave 1 tracks can execute in parallel. No inter-track dependencies.

---

### W1-RT-001: Runtime abstraction (subprocess default, Docker opt-in)

| Field | Value |
|---|---|
| Track | A: Runtime |
| Status | done |
| Est. | 2 days |
| Depends on | Foundation (done) |
| Files | `engine/runtime.py` (new), `workflows/runner.py` |

**Description:**
1. Create `IsolatedTaskRuntime(ABC)` with lifecycle: `setup() -> execute(cmd, workdir) -> collect_artifacts() -> cleanup()`.
2. Implement `SubprocessRuntime` — runs tasks via `asyncio.create_subprocess_exec`.
3. Implement `DockerRuntime` — only activated if `execution_profile.runtime == "docker"` and Docker is available. Raises clear error if Docker not found.
4. Wire into `WorkflowRunner` — default is subprocess, Docker is config opt-in.

**Tests (`tests/test_runtime.py` — new):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_subprocess_runtime_echo` | `SubprocessRuntime.execute("echo hello")` -> stdout contains "hello" |
| 2 | `test_subprocess_runtime_failure` | Non-zero exit -> runtime error captured |
| 3 | `test_subprocess_runtime_cleanup` | Temp workdir removed after cleanup() |
| 4 | `test_docker_runtime_not_available` | When Docker missing, raises `RuntimeError` with message |
| 5 | `test_runtime_factory_default_subprocess` | No config -> gets `SubprocessRuntime` |
| 6 | `test_runtime_factory_docker_opt_in` | Config `runtime=docker` -> gets `DockerRuntime` |

Done 2026-02-09 — Added runtime abstraction (`IsolatedTaskRuntime`, subprocess/docker runtimes, factory), wired `execution_profile` into `WorkflowRunner` and `/api/run`, and added 6 runtime unit tests.

**Regression:** Existing workflow execution tests pass (subprocess is a transparent wrapper).

---

### W1-AD-001: Adapter base interfaces

| Field | Value |
|---|---|
| Track | B: Adapters |
| Status | done |
| Est. | 1 day |
| Depends on | Foundation (done) |
| Files | `integrations/base.py` (new) |

**Description:**
Create `integrations/base.py` with abstract base classes:
- `AgentAdapter(ABC)` — `async def invoke(prompt, context) -> AgentResponse`
- `ToolAdapter(ABC)` — `async def execute(tool_name, args) -> ToolResult`
- `WorkflowAdapter(ABC)` — `async def run(workflow_def, inputs) -> WorkflowResult`
- `TraceAdapter(ABC)` — `def emit(event: CanonicalEvent) -> None`
- `CanonicalEvent` dataclass — unified event model with `type`, `timestamp`, `step_name`, `data`.

**Tests (`tests/test_integrations_base.py` — new):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_agent_adapter_is_abstract` | Cannot instantiate `AgentAdapter` directly |
| 2 | `test_canonical_event_serializable` | `CanonicalEvent` round-trips through JSON |
| 3 | `test_adapter_subclass_contract` | Concrete stub implementing all methods passes isinstance checks |

Done 2026-02-09 — Implemented base adapter contracts and `CanonicalEvent`; added 3 unit tests. Regression: Full `pytest tests/` green. Server still starts.

---

### W1-AD-002: LangChain adapter normalization

| Field | Value |
|---|---|
| Track | B: Adapters |
| Status | done |
| Est. | 1 day |
| Depends on | W1-AD-001 |
| Files | `integrations/langchain.py`, `integrations/__init__.py` |

**Description:**
Refactor existing `AgenticChatModel`, `AgenticTool`, and `AgenticAgent` to inherit from the base adapter interfaces. Ensure LangChain import remains optional (graceful `ImportError`).

**Tests (`tests/test_langchain_integration.py`):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_agentic_chat_model_implements_agent_adapter` | `isinstance(AgenticChatModel(...), AgentAdapter)` |
| 2 | `test_agentic_tool_implements_tool_adapter` | `isinstance(AgenticTool(...), ToolAdapter)` |
| 3 | `test_langchain_unavailable_graceful` | When `langchain_core` not installed, import doesn't crash |
| 4 | `test_canonical_event_emission` | LangChain adapter emits `CanonicalEvent` on invoke |

Done 2026-02-09 — Refactored LangChain-related classes to implement adapter base interfaces; added 4 unit tests. Regression: All Foundation tests green. Server + UI functional.

---

### W1-SC-001: Hybrid scoring engine + LLM-as-judge protocol

| Field | Value |
|---|---|
| Track | C: Scoring |
| Status | pending |
| Est. | 3 days |
| Depends on | Foundation (done) — only needs `evaluation.py`, `normalization.py` |
| Files | `server/evaluation.py`, `server/judge.py` (new) |

**Why this can start now:** Hybrid scoring only depends on `score_workflow_result()`, `normalization.py`, and `scoring_profiles.py` — all delivered in Foundation. It scores any `WorkflowResult` regardless of execution strategy.

**Description:**
Extend `score_workflow_result()` to compose (four-layer model):
1. Layer 1 — Objective test score (existing: pass@k, tool call validity).
2. Layer 2 — LLM judge score (new — call LLM with anchored rubric, structured output).
3. Layer 3 — Patch similarity advisory score + efficiency/cost metrics (lower-is-better normalization).
4. Layer 0 — Hard gates still override all layers.

Create `server/judge.py` implementing LLM-as-judge protocol (reference guide S8):
1. Accept anchored rubric criteria (1-5 scale with semantic anchors).
2. Format prompt with candidate output + rubric + evidence extraction instructions.
3. Use constrained structured output (JSON schema) — enforce `{criteria: [{name, score, evidence}]}`.
4. Implement order randomization: randomly shuffle criteria and candidate sections.
5. Run swapped-order adjudication: for pairwise comparisons, re-run with reversed order; if scores disagree by >1 point on any criterion, flag as inconsistent and either re-run or treat as tie.
6. Low temperature (<=0.1) for determinism.
7. Log judge model, version, prompt version, temperature per evaluation.
8. Maintain calibration fixture set (known human-scored samples); track drift.

**Tests:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_hybrid_score_without_judge` | No LLM judge configured -> uses objective + similarity only |
| 2 | `test_hybrid_score_with_mock_judge` | Mock LLM judge -> score includes judge component |
| 3 | `test_hybrid_hard_gates_still_override` | High hybrid score but gate fail -> `passed=False` |
| 4 | `test_hybrid_score_determinism` | Same inputs -> same score (within tolerance band) |
| 5 | `test_judge_structured_output_schema` | Judge response validates against expected JSON schema |
| 6 | `test_judge_swapped_order_consistency` | Two calls with swapped order produce scores within 1 point |
| 7 | `test_judge_calibration_within_tolerance` | Judge on calibration fixture scores within +/-0.5 of human labels |
| 8 | `test_judge_logs_model_version` | Judge result includes model/version/prompt_version metadata |

---

### W1-DA-001: Dataset lane expansion

| Field | Value |
|---|---|
| Track | D: Data |
| Status | pending |
| Est. | 2 days |
| Depends on | Foundation (done) |
| Files | `tests/fixtures/datasets/`, evaluation config |

**Why this can start now:** Pure data work — adding fixture files and compatibility metadata. No code dependencies beyond Foundation.

**Description:**
Add new benchmark dataset fixtures for additional workflow types. Add CI smoke matrix that runs each dataset against compatible workflows at tier 0.

**Tests:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_new_datasets_valid_json` | All new fixture files parse as valid JSON |
| 2 | `test_new_datasets_have_required_fields` | Each sample has `prompt` or `task_description` |
| 3 | `test_compatibility_smoke_matrix` | Each dataset compatible with at least one workflow |

---

### W1-UI-001: Schema-driven run configuration

| Field | Value |
|---|---|
| Track | E: UI |
| Status | done |
| Est. | 2 days |
| Depends on | Foundation (done) — uses existing `/api/workflows/{name}/dag` |
| Files | UI `src/` components |

**Why this can start now:** Builds on existing API that already returns workflow inputs. No dependency on scoring or runtime changes.

**Description:**
UI dynamically renders run configuration form from workflow input schema (already partially here via `/api/workflows/{name}/dag` returning `inputs`). Extend to show rubric options and runtime config.

**Tests (vitest):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_run_form_renders_inputs` | Workflow with 2 inputs -> form shows 2 fields |
| 2 | `test_run_form_enum_shows_dropdown` | Enum input -> select element with options |
| 3 | `test_run_form_optional_not_required` | Optional field not marked required in form |

Done 2026-02-09 — Extracted `RunConfigForm` component with schema-driven input rendering, rubric override, and runtime configuration (subprocess/docker, max_attempts, max_duration). Added `ExecutionProfileRequest` type. Refactored `WorkflowDetailPage` to use the new form. 8 vitest tests added (all passing).

---

### Wave 1 Regression Gate

**Run after all Wave 1 tickets are done:**

1. `python -m pytest tests/ -v` — all green (Foundation + Wave 1 tests).
2. `npm run build && npm run test` in `ui/`.
3. Server starts, all API endpoints functional.
4. Workflows execute via subprocess runtime (default behavior unchanged).
5. LangChain integration importable and conformant.
6. UI: list workflows, run workflow, view results — no regressions.
7. Hybrid scoring produces valid results with and without judge configured.
8. New dataset fixtures parse and pass compatibility checks.

---

## Wave 2 — After Wave 1 Core Pieces (~day 3)

Each track depends on a specific Wave 1 deliverable. Tracks within Wave 2 are independent.

---

### W2-ST-001: ExecutionStrategy abstraction

| Field | Value |
|---|---|
| Track | A: Strategy |
| Status | pending |
| Est. | 1 day |
| Depends on | W1-RT-001 (runtime abstraction) |
| Files | `engine/strategy.py` (new), `engine/__init__.py` |

**Description:**
Define `ExecutionStrategy(ABC)` with `async def execute(dag, ctx, ...) -> WorkflowResult`. Extract current DAG execution into `DagOnceStrategy`. Prepare the interface for iterative strategies.

**Tests (`tests/test_strategy.py`):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_dag_once_strategy_matches_current_behavior` | Same result as direct `DAGExecutor.execute()` |
| 2 | `test_strategy_factory_default_dag_once` | No config -> `DagOnceStrategy` |
| 3 | `test_strategy_is_abstract` | Cannot instantiate `ExecutionStrategy` |

---

### W2-ST-002: Iterative repair strategy

| Field | Value |
|---|---|
| Track | A: Strategy |
| Status | pending |
| Est. | 2 days |
| Depends on | W2-ST-001 |
| Files | `engine/strategy.py`, `engine/iterative.py` (new) |

**Description:**
Implement `IterativeRepairStrategy` — runs DAG, checks pass criteria, if failed, re-runs with feedback up to `max_attempts`. Emits attempt-level SSE events.

**Tests:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_iterative_stops_on_success` | Passes on first attempt -> 1 iteration |
| 2 | `test_iterative_retries_on_failure` | Fails first, passes second -> 2 iterations |
| 3 | `test_iterative_respects_max_attempts` | Always fails -> stops at max, result is FAILED |
| 4 | `test_iterative_emits_attempt_events` | SSE events contain `attempt_number` |
| 5 | `test_dag_once_backward_compatible` | Existing workflows still use dag_once |

---

### W2-AG-001: Per-agent scoring + reporting bundle

| Field | Value |
|---|---|
| Track | B: Per-agent |
| Status | pending |
| Est. | 2.5 days |
| Depends on | W1-SC-001 (hybrid scoring) |
| Files | `server/evaluation.py`, `contracts/messages.py` |

**Description:**
Add `AgentScore` model. For each step/agent, compute: role adherence, output quality, efficiency (tier/retry budget using `lower_is_better` normalization), reliability. Include `agent_scores[]` in evaluation payload.

Apply Bayesian reliability adjustment for agents with < 20 scored runs:
`adjusted_norm = (n * score + 20 * 0.5) / (n + 20)` (reference guide S6).

Add statistical reporting bundle to evaluation output (reference guide S10):
- `mean_score`, `stdev`, `min`, `max` per criterion across dataset samples.
- `grade_distribution` (count of each grade A-F across samples).
- `floor_violation_count` per criterion.
- `hard_gate_failure_rate` per gate.

**Tests:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_agent_score_per_step` | Each step in result gets an `AgentScore` entry |
| 2 | `test_agent_score_efficiency_penalty` | Excessive retries -> lower efficiency score |
| 3 | `test_agent_scores_in_sse_payload` | `evaluation_complete` event has `agent_scores` array |
| 4 | `test_agent_score_with_no_agent_role` | Step without explicit agent -> graceful default |
| 5 | `test_reliability_adjustment_small_n` | Agent with 5 runs -> score adjusted toward 0.5 prior |
| 6 | `test_reliability_adjustment_large_n` | Agent with 100 runs -> adjustment negligible |
| 7 | `test_reporting_bundle_per_criterion` | Multi-sample eval -> `mean_score`, `stdev` per criterion present |
| 8 | `test_reporting_bundle_grade_distribution` | Grade distribution sums to sample count |

---

### W2-UI-001: Compatibility matrix UI

| Field | Value |
|---|---|
| Track | C: UI |
| Status | pending |
| Est. | 1 day |
| Depends on | W1-UI-001 (schema-driven run config) |
| Files | UI components |

**Description:**
Dataset selector greys out or hides incompatible datasets based on `GET /api/eval/datasets?workflow=<name>`.

**Tests (vitest):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_dataset_list_filters_by_workflow` | Only compatible datasets shown |
| 2 | `test_incompatible_dataset_disabled` | Incompatible entry has disabled state |

---

### W2-UI-002: Score breakdown panel with hard-gate visibility

| Field | Value |
|---|---|
| Track | C: UI |
| Status | pending |
| Est. | 1.5 days |
| Depends on | W1-SC-001 (hybrid scoring API) |
| Files | UI components |

**Description:**
After a run completes, show: criteria scores, weights, weighted total, grade, hard gate pass/fail for each gate. If a gate failed, show which one and why.

**Tests (vitest):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_score_panel_renders_criteria` | All criteria shown with scores |
| 2 | `test_score_panel_shows_gate_failures` | Failed gate highlighted in red |
| 3 | `test_score_panel_passed_state` | All gates pass -> green passed badge |

---

### W2-AD-001: Microsoft Agent Framework adapter

| Field | Value |
|---|---|
| Track | D: Adapter |
| Status | pending |
| Est. | 2 days |
| Depends on | W1-AD-001 (base interfaces) |
| Files | `integrations/microsoft_agent_framework.py` (new) |

**Description:**
Implement `MicrosoftAgentAdapter(AgentAdapter)` against the base contract. Maps Microsoft Agent Framework primitives to the canonical event model.

**Tests (`tests/test_microsoft_adapter.py`):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_microsoft_adapter_implements_contract` | `isinstance(adapter, AgentAdapter)` |
| 2 | `test_microsoft_adapter_emits_canonical_events` | Events match `CanonicalEvent` schema |
| 3 | `test_microsoft_adapter_import_optional` | Missing MS SDK -> graceful ImportError |

---

### Wave 2 Regression Gate

1. All Foundation + Wave 1 + Wave 2 tests green.
2. Existing `dag_once` workflows work identically.
3. SSE payloads validate against extended schema.
4. UI runs show evaluation results with score breakdown. No regressions on existing display.
5. Per-agent scores are additive, don't break existing display.
6. Server starts, all endpoints work.

---

## Wave 3 — After Wave 2 (~day 6)

---

### W3-ART-001: Attempt artifact persistence

| Field | Value |
|---|---|
| Track | Artifacts |
| Status | pending |
| Est. | 1 day |
| Depends on | W2-ST-002 (iterative repair) |
| Files | `workflows/run_logger.py`, `engine/iterative.py` |

**Description:**
Each iteration's patches, logs, and judge results are saved to `runs/<run_id>/attempts/<N>/`.

**Tests:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_attempt_artifacts_saved` | After iterative run, `attempts/1/` dir exists with log |
| 2 | `test_attempt_artifacts_retrievable` | API or run_logger can list artifacts per attempt |

---

### W3-UI-001: Iteration timeline and artifact explorer

| Field | Value |
|---|---|
| Track | UI |
| Status | pending |
| Est. | 2 days |
| Depends on | W3-ART-001 (attempt artifacts) |
| Files | UI components |

**Description:**
For iterative runs, show timeline of attempts with expandable details: attempt number, status, score, artifacts. Click to drill into logs/patches.

**Tests (vitest):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_timeline_renders_attempts` | 3-attempt run -> 3 timeline nodes |
| 2 | `test_timeline_final_highlighted` | Last attempt visually distinct |

---

### W3-AD-001: Cross-framework conformance tests

| Field | Value |
|---|---|
| Track | Adapters |
| Status | pending |
| Est. | 1 day |
| Depends on | W2-AD-001 (MS adapter), W1-AD-002 (LangChain) |
| Files | `tests/test_adapter_conformance.py` (new) |

**Description:**
Run identical workflow fixtures through both LangChain and Microsoft adapters. Assert parity on: terminal status, required output presence, event sequence, event count.

**Tests:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_status_parity` | Both adapters produce same terminal status for same fixture |
| 2 | `test_output_parity` | Both produce non-null required outputs |
| 3 | `test_event_sequence_parity` | Both emit same event types in same order |
| 4 | `test_event_completeness` | Both emit `workflow_start` + `step_*` + `workflow_end` |

---

### W3-FL-001: Feature flags

| Field | Value |
|---|---|
| Track | Operations |
| Status | pending |
| Est. | 1 day |
| Depends on | All Wave 2 features exist to flag |
| Files | `config/`, `server/evaluation.py`, `engine/strategy.py` |

**Description:**
Add feature flag config for: iterative strategy, per-agent scoring, Microsoft adapter, Docker runtime. Flags default to `false` in prod, `true` in dev. Read from config YAML or env vars.

**Tests:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_feature_flag_disabled_hides_feature` | Flag off -> iterative strategy not available |
| 2 | `test_feature_flag_enabled_exposes_feature` | Flag on -> iterative strategy available |
| 3 | `test_feature_flag_env_override` | Env var overrides config file |

---

### Wave 3 Regression Gate

1. All Foundation + Wave 1-3 tests green.
2. Full UI smoke: list, DAG, run, evaluate, score panel, dataset selector, iteration timeline.
3. Feature flags toggle features without breaking baseline behavior.
4. Cross-framework conformance tests pass.

---

## Wave 4 — Finalization (~day 8)

---

### W4-CI-001: CI benchmark gating

| Field | Value |
|---|---|
| Track | CI |
| Status | pending |
| Est. | 1 day |
| Depends on | W3-FL-001 (feature flags) |
| Files | CI config, `scripts/` |

**Description:**
Add CI step that runs tier-0 benchmark smoke against all non-experimental workflows. Gate: all must pass hard gates. Failure blocks merge.

**Tests:**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_ci_smoke_script_exits_zero` | Script runs against fixtures -> exit 0 |
| 2 | `test_ci_smoke_script_exits_nonzero_on_failure` | Bad fixture -> exit 1 |

---

### W4-PR-001: Promotion policy automation

| Field | Value |
|---|---|
| Track | CI |
| Status | pending |
| Est. | 1.5 days |
| Depends on | W3-FL-001, W2-AG-001 (per-agent scoring) |
| Files | `server/evaluation.py`, `scripts/promotion_check.py` (new) |

**Description:**
Implement promotion policy checks per reference guide S11:
1. **Non-inferiority check:** new version must score >= baseline - delta (delta=0.02 by default) on each criterion.
2. **Floor regression detection:** if a criterion that previously passed its floor now fails, block promotion.
3. **Minimum sample requirement:** promotion requires >= N scored runs (N=10 default).
4. **Reporting:** generate promotion report with per-criterion comparison, trend direction, pass/block verdict.
5. Integrate as optional post-evaluation step callable from CLI and CI.

**Tests (`test_promotion.py` — new):**

| # | Test | Asserts |
|---|---|---|
| 1 | `test_promotion_passes_when_better` | New scores > baseline -> pass |
| 2 | `test_promotion_blocks_on_regression` | Criterion drops by > delta -> block with reason |
| 3 | `test_promotion_blocks_floor_regression` | Floor that previously passed now fails -> block |
| 4 | `test_promotion_requires_min_samples` | Only 3 runs -> insufficient samples, block |
| 5 | `test_promotion_report_structure` | Report has per-criterion comparison and verdict |

---

### W4-DOC-001: Rollout runbooks + tooling map

| Field | Value |
|---|---|
| Track | Docs |
| Status | pending |
| Est. | 1.5 days |
| Depends on | All waves substantially complete |
| Files | `docs/operations/` (new), `docs/reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md`, `README.md` |

**Description:**
1. Write operational runbooks for: enabling features, rolling back flag changes, incident response for scoring failures.
2. Create `docs/reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md` listing active modules vs deprecated/stale paths (carryover from P0-T009).
3. Clean README.md references to removed or deprecated tooling.

**Tests:** None (docs-only).

---

### Wave 4 / Final Regression Gate

1. Full `pytest tests/` — all green.
2. `npm run build && npm run test` — all green.
3. Server starts with all features flagged on/off — both modes work.
4. Full UI smoke with all features enabled.
5. CI smoke script passes.
6. Rollback: disable all feature flags -> system behaves like Foundation baseline.

---

## Complete Ticket Summary

| ID | Title | Wave | Track | Est. | Depends | Tests | Status |
|---|---|---|---|---|---|---|---|
| P0-T001 | Hard gates + pass-rule + floors | Foundation | — | 1d | — | 10 | **done** |
| P0-T002 | SSE/log gate fields | Foundation | — | 0.5d | T001 | 3 | **done** |
| P0-T003 | Unresolved output -> gate fail | Foundation | — | 0.5d | T001 | 2 | **done** |
| P0-T004 | Step input `${...}` fix | Foundation | — | 1d | — | 4 | **done** |
| P0-T005 | Compatibility filter + 422 | Foundation | — | 1d | — | 3 | **done** |
| P0-T006 | Empty required input rejection | Foundation | — | 0.5d | — | 3 | **done** |
| P0-T007 | Workflow rubric + profiles | Foundation | — | 1.5d | T001,T010 | 6+ | **done** |
| P0-T008 | Mark experimental + hide | Foundation | — | 0.5d | — | 2 | **done** |
| P0-T009 | Docs cleanup | Foundation | — | 0.5d | — | 0 | **partial** |
| P0-T010 | Score normalization framework | Foundation | — | 1d | T001 | 9 | **done** |
| P0-T011 | Scoring profile templates | Foundation | — | 1d | T010,T007 | 4 | **done** |
| W1-RT-001 | Runtime abstraction | 1 | Runtime | 2d | Foundation | 6 | pending |
| W1-AD-001 | Adapter base interfaces | 1 | Adapters | 1d | Foundation | 3 | **done** |
| W1-AD-002 | LangChain normalization | 1 | Adapters | 1d | W1-AD-001 | 4 | **done** |
| W1-SC-001 | Hybrid scoring + LLM judge | 1 | Scoring | 3d | Foundation | 8 | pending |
| W1-DA-001 | Dataset expansion | 1 | Data | 2d | Foundation | 3 | pending |
| W1-UI-001 | Schema-driven run config | 1 | UI | 2d | Foundation | 3 | **done** |
| W2-ST-001 | ExecutionStrategy ABC | 2 | Strategy | 1d | W1-RT-001 | 3 | pending |
| W2-ST-002 | Iterative repair strategy | 2 | Strategy | 2d | W2-ST-001 | 5 | pending |
| W2-AG-001 | Per-agent scoring + reporting | 2 | Scoring | 2.5d | W1-SC-001 | 8 | pending |
| W2-UI-001 | Compatibility matrix UI | 2 | UI | 1d | W1-UI-001 | 2 | pending |
| W2-UI-002 | Score breakdown panel | 2 | UI | 1.5d | W1-SC-001 | 3 | pending |
| W2-AD-001 | MS Agent Framework adapter | 2 | Adapters | 2d | W1-AD-001 | 3 | pending |
| W3-ART-001 | Attempt artifact persistence | 3 | Artifacts | 1d | W2-ST-002 | 2 | pending |
| W3-UI-001 | Iteration timeline UI | 3 | UI | 2d | W3-ART-001 | 2 | pending |
| W3-AD-001 | Cross-framework conformance | 3 | Adapters | 1d | W2-AD-001,W1-AD-002 | 4 | pending |
| W3-FL-001 | Feature flags | 3 | Ops | 1d | Wave 2 done | 3 | pending |
| W4-CI-001 | CI benchmark gating | 4 | CI | 1d | W3-FL-001 | 2 | pending |
| W4-PR-001 | Promotion policy automation | 4 | CI | 1.5d | W3-FL-001,W2-AG-001 | 5 | pending |
| W4-DOC-001 | Rollout runbooks + tooling map | 4 | Docs | 1.5d | all waves | 0 | pending |
| **Total** | | | | **~39d effort / ~10-12d wall** | | **~113** | |

---

## Test Plan Summary

### Unit Tests
1. Hard gate logic — all 5 gates (Foundation, done).
2. Normalization math — each formula_id (Foundation, done).
3. Grading algorithm — 6-step deterministic (Foundation, done).
4. Criterion floor enforcement (Foundation, done).
5. Scoring profile selection (Foundation, done).
6. Input adaptation validation (Foundation, done).
7. Hybrid scoring formulas — objective + judge + similarity (Wave 1).
8. Judge structured output schema (Wave 1).
9. Per-agent scoring dimensions (Wave 2).
10. Reliability adjustment — Bayesian smoothing (Foundation done, agent-level Wave 2).
11. Feature flag behavior (Wave 3).

### Integration Tests
1. `GET /api/eval/datasets?workflow=` compatibility (Foundation, done).
2. `POST /api/run` mismatch rejection (Foundation, done).
3. Runtime policy behavior for subprocess and Docker (Wave 1).
4. SSE event sequencing for dag and iterative (Wave 2).
5. Artifact persistence and retrieval (Wave 3).
6. Per-run logging completeness (Wave 1+).
7. Scoring profile end-to-end (Foundation done, extended Wave 1).

### Judge Tests (Wave 1)
1. Swapped-order adjudication consistency.
2. Structured output schema enforcement.
3. Calibration fixture regression.

### Conformance Tests (Wave 3)
1. LangChain vs Microsoft adapter parity for terminal status.
2. Required output parity and non-null checks.
3. Canonical event model completeness and sequence parity.

### E2E Tests (Waves 2-3)
1. UI dataset compatibility gating.
2. Hard-gate visibility in score panel.
3. Iteration timeline and artifact drill-down.

### Regression / Determinism Tests
1. Fixed fixture set — same inputs produce same score within variance band across 5 reruns.
2. Benchmark smoke runs by workflow family (one dataset per profile).
3. Anti-pattern guards — weighted score alone cannot produce `passed=True` when any hard gate fails.

---

## Risks and Mitigations

| Risk | Severity | Mitigation | Wave |
|---|---|---|---|
| False-positive pass outcomes | Critical | Hard gates mandatory before score pass | Foundation (done) |
| Compatibility mismatch noise | Critical | Capability matching + explicit 422 reasons | Foundation (done) |
| Scoring instability | High | Determinism thresholds + fixture tests + normalization | Foundation (done) + Wave 1 |
| Stale tooling confusion | Medium | Authoritative map + README cleanup | Wave 4 |
| Adapter behavior drift | Medium | Base contract + conformance tests | Wave 1 + Wave 3 |
| Untrusted code execution risk | High | Runtime isolation, resource controls, teardown | Wave 1 |
| LLM judge bias (verbosity, position) | High | Swapped-order adjudication + calibration set + low temp | Wave 1 |
| Noisy scores on small samples | Medium | Bayesian reliability adjustment (prior=0.5, k=20) | Wave 2 |
| Single-rubric anti-pattern | Medium | Workflow-family scoring profiles (A-D) | Foundation (done) |
| Score opacity for operators | Medium | Raw + normalized dual storage + grade explanation | Foundation (done) + Wave 2 UI |

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

## Future (Post-Wave 4)

1. Expand Microsoft process patterns as templates: sequential, concurrent, conditional, map-reduce, handoff.
2. Add cross-framework replay tooling for incident reproducibility.
3. Add rubric drift monitoring and auto-calibration workflows.
4. Add adapter certification pipeline for future framework additions.

---

## Change Log

| Date | Version | Change |
|---|---|---|
| 2026-02-08 | v4.0 | Replaced sequential Phase 0-6 with parallel Waves 1-4. Foundation (Phase 0) marked complete. Tickets renumbered from P*-T* to W*-*-*. Old P0-T* retained as audit. |
| 2026-02-08 | v3.3 | Decision-locked consolidated plan with implementation tickets (superseded). |
