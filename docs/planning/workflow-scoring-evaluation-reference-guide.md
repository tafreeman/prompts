# Workflow Scoring & Evaluation Reference Guide

Status: Implementation reference
Date: 2026-02-08
Audience: Architects and implementers building workflow scoring, validation, and eval pipelines

## 1) Why this guide exists

This guide defines a production scoring framework for workflow systems (single-turn, workflow DAGs, single-agent, multi-agent) with a hard requirement:

- Validation and hard gates are authoritative.
- Weighted scores are secondary and cannot override failed hard gates.

This aligns with the approved repo direction that scoring and validation are release-blocking.

## 2) Core design principles

1. Evaluate in layers, not one number.
2. Prefer executable/objective metrics where possible.
3. Use rubric/judge scoring for quality dimensions objective metrics cannot capture.
4. Normalize metrics into a common scale only after per-metric validation.
5. Calibrate automated scoring against humans on a recurring cadence.
6. Track bias and variance for LLM-as-judge.

## 3) Four-layer scoring model

## Layer 0: Validation and hard gates (binary)

Hard gates determine eligibility to pass.

Required gates:

- `required_outputs_present`
- `overall_status_success`
- `no_critical_step_failures`
- `schema_contract_valid`
- `dataset_workflow_compatible`

Optional workflow-specific gates:

- `tests_fail_to_pass_all_green`
- `tests_pass_to_pass_threshold_met`
- `citations_present_for_claims`
- `tool_call_schema_valid`

Rule:

- `passed = hard_gates_passed AND weighted_score >= pass_threshold`

## Layer 1: Objective metrics (preferred)

Examples:

- Executable tests, pass@k, fail-to-pass rate, pass-to-pass rate
- Tool call validity and argument correctness
- Retrieval ranking metrics (nDCG/MAP/MRR) and retrieval coverage
- Latency, retries, failure rate

## Layer 2: Rubric / judge metrics

Used for:

- Coherence, instruction following quality, completeness, code review quality
- Documentation and communication quality

Use structured scoring with anchored definitions (1-5 or 0-5), then normalize.

## Layer 3: Efficiency/cost/operations

Examples:

- p50/p95 runtime
- token/cost budgets
- retry amplification
- infrastructure stability

## 4) Recommended score scales

Use one internal canonical scale:

- Canonical per-criterion: `0.0..1.0`
- Canonical overall: `0..100`

Accepted raw scales before normalization:

- Binary: `0|1`
- Likert: `1..5` or `-2..2`
- Continuous: `0..1`
- Pairwise win rate: `0..1`

Normalize with explicit formulas per metric type and store both raw and normalized values.

## 4.1) Normalization formulas (implementation default)

Use a formula registry (`formula_id`) so every normalized metric is reproducible.

Definitions:

- `clamp(x) = min(1, max(0, x))`
- All normalized outputs must be `0.0..1.0`

Default formulas:

- Binary (`0|1`):
  - `norm = raw`
- Likert `1..5`:
  - `norm = (raw - 1) / 4`
- Likert `-2..2`:
  - `norm = (raw + 2) / 4`
- Pairwise with ties:
  - `norm = (wins + 0.5 * ties) / (wins + losses + ties)`
- Cost/latency/retries (lower is better):
  - `norm = clamp((slo_bad - raw) / (slo_bad - slo_good))`
  - Example: if latency SLO is good=`8s`, bad=`30s`, then `raw=12s` gives `norm=(30-12)/(30-8)=0.818`
- Retrieval metrics already in `0..1` (nDCG/MAP/MRR/Recall@k):
  - `norm = clamp(raw)`
- SWE-style test metrics:
  - `fail_to_pass = passed_fail_to_pass / total_fail_to_pass`
  - `pass_to_pass = passed_pass_to_pass / total_pass_to_pass`
  - Enforce hard gates separately: `fail_to_pass == 1.0` and `pass_to_pass >= 0.95`

Recommended reliability adjustment for low sample counts:

- `adjusted_norm = (n * norm + k * prior) / (n + k)`
- Defaults: `prior=0.5`, `k=20` (reduce noisy swings for tiny samples)
- Store both `norm` and `adjusted_norm`; use `adjusted_norm` for promotion decisions.

## 5) Grading scale and placement logic

## Letter grade bands (post-normalization)

- `A`: `90-100`
- `B`: `80-89.99`
- `C`: `70-79.99`
- `D`: `60-69.99`
- `F`: `<60`

## Placement rules (important)

1. If any hard gate fails, force `passed=false` and `grade=F` for release gating (retain weighted score for diagnostics).
2. Apply criterion floors for critical dimensions:
- `correctness` floor: `>=0.70`
- `safety/validation` floor: `>=0.80`
3. If floor is missed, cap grade at `D` even if aggregate score is higher.
4. Record gate failure reasons in payload for root-cause analysis.

## 5.1) Deterministic grading algorithm

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

## 5.2) Scale placement guide (what determines grade placement)

Use this as the implementation checklist for explaining why a run landed in a grade band.

- `A (90-100)`: all hard gates pass, all critical floors pass with margin (`>= floor + 0.10`), no severe validation/safety defects, low judge disagreement.
- `B (80-89.99)`: all hard gates pass, floors pass, limited non-critical defects, objective metrics strong but not best-in-class.
- `C (70-79.99)`: all hard gates pass, floors pass near boundary, acceptable baseline quality with clear improvement items.
- `D (60-69.99)`: at least one critical floor failed (grade-capped) or multiple material quality gaps.
- `F (<60 or any hard-gate failure)`: release-blocking failure.

Tie-breakers when two runs have near-equal weighted scores (`abs(diff) < 1.0`):

1. Lower hard-gate failure count.
2. Higher objective correctness score.
3. Higher safety/validation score.
4. Lower p95 latency and cost.

## 6) Workflow-family scoring profiles

Decision context: repo uses workflow-level rubrics (not one universal rubric).

## Profile A: Code repair / SWE-style iterative workflows

Primary use: issue resolution against real repositories.

Hard gates:

- patch applies cleanly
- `FAIL_TO_PASS == 1.0`
- `PASS_TO_PASS >= 0.95`
- no sandbox/security policy violations

Weighted profile (default suggestion):

- objective tests: `0.60`
- judge quality rubric: `0.25`
- patch similarity/semantic diff quality: `0.10`
- efficiency/cost: `0.05`

Key note:

- This profile is test-dominant by design.

## Profile B: DAG generation/review workflows (non-executable dominant)

Primary use: design/review/generation where direct execution is partial.

Hard gates:

- required outputs present and parseable
- critical steps succeeded
- output schema valid

Weighted profile (default suggestion):

- correctness rubric: `0.35`
- completeness rubric: `0.25`
- tool/data precision: `0.20`
- documentation quality: `0.10`
- efficiency: `0.10`

## Profile C: RAG workflows

Hard gates:

- answer grounded in retrieved context
- citation/link requirements met
- high-severity hallucination checks clear

Weighted profile (default suggestion):

- faithfulness/groundedness: `0.35`
- response relevance: `0.25`
- context precision: `0.20`
- context recall/coverage: `0.10`
- efficiency: `0.10`

## Profile D: Agentic tool-use and routing workflows

Hard gates:

- tool call JSON/schema valid
- no forbidden tool invoked
- handoff graph rules respected

Weighted profile (default suggestion):

- tool selection accuracy: `0.25`
- argument correctness/F1: `0.25`
- handoff accuracy: `0.20`
- final task correctness: `0.20`
- efficiency: `0.10`

## 7) Rubric authoring standard

Each rubric criterion must include:

- `name`
- `definition`
- `evidence_required`
- `scale` (e.g., `1..5`)
- anchor descriptions for each score point
- `weight`
- `critical_floor` (optional)

## Recommended anchored 1..5 semantic scale

- `1`: fails core requirement, major errors
- `2`: partially correct, significant gaps
- `3`: acceptable baseline, clear issues remain
- `4`: strong quality, minor issues
- `5`: excellent, complete and robust

## Example YAML shape

```yaml
rubric_id: fullstack_generation_v1
version: 1
criteria:
  - name: correctness
    scale: [1, 5]
    weight: 0.35
    critical_floor: 3
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
```

## 8) LLM-as-judge protocol (bias-aware)

Required controls:

1. Prefer pairwise or constrained rubric scoring tasks rather than free-form judgments.
2. Randomize candidate order.
3. Run swapped-order adjudication for pairwise tasks.
4. Treat inconsistent swapped outcomes as tie or trigger adjudication rerun.
5. Use low temperature and strict structured output schema.
6. Maintain calibration set with human labels and track drift.

Optional stronger controls:

- Majority vote across judge families/models
- Few-shot judge prompt for consistency
- Adversarial anti-verbosity checks

## 9) What to log for implementation

Per run:

- workflow id/version
- dataset id/version/sample id
- hard gate results and failure reasons
- per-criterion raw + normalized score
- final weighted score and grade
- judge model/version/prompt version
- tool call traces and validation outcomes
- runtime/cost/retries

Per step/agent:

- step status
- duration
- retries
- model/tier used
- step-level score outputs

## 10) Statistical reliability and release policy

## Minimum reporting bundle

- pass rate
- weighted score mean and standard deviation
- hard-gate failure rate by gate type
- per-criterion distribution
- top failure reasons

## Promotion policy (recommended)

A candidate version promotes only if all hold:

1. Hard-gate failure rate is not worse than baseline by threshold.
2. Weighted score improves or is non-inferior within tolerance.
3. No critical criterion floor regression.
4. No increase in severe validation/security failures.

## 11) Practical implementation map for this repo

## Phase 0 (first)

- Implement hard gates in `agentic-workflows-v2/src/agentic_v2/server/evaluation.py`
- Enforce pass formula in evaluation result
- Add hard-gate details to SSE payload in `agentic-workflows-v2/src/agentic_v2/server/routes/workflows.py`
- Ensure required output resolution failure cannot silently pass in `agentic-workflows-v2/src/agentic_v2/workflows/runner.py`
- Add/extend tests in `agentic-workflows-v2/tests/test_server_evaluation.py`

## Phase 0.5

- Add dataset/workflow compatibility checks and 422 failure reason surface
- Add workflow-level rubric metadata loading (decision D1=C)

## Phase 1+

- Introduce strategy-specific execution and scoring profile selection
- Introduce full per-agent scoring payload (decision D5=A)

## Phase 5+

- Add Microsoft Agent Framework adapter scoring parity tests against LangChain adapter

## 12) Test matrix

## Unit tests

- hard gate logic
- normalization math
- grading rules + floor/cap behavior
- rubric schema validation
- swapped-order consistency handling

## Integration tests

- compatible/incompatible dataset-workflow runs
- SSE payload schema with hard gates
- run log schema completeness
- workflow-level rubric selection and override

## Regression tests

- fixed fixture set for determinism checks
- benchmark smoke runs by workflow family

## 13) Ready-to-use default thresholds

These are operational defaults; tune with calibration data.

- `pass_threshold`: `70`
- `correctness floor`: `0.70`
- `validation/safety floor`: `0.80`
- `PASS_TO_PASS floor` for SWE-style: `0.95`
- `FAIL_TO_PASS` for SWE-style: `1.00`
- `inconsistent pairwise judge rate` warning threshold: `>0.10`

## 14) Common anti-patterns to avoid

- using only one generic score for every workflow type
- allowing weighted score to override failed hard gates
- treating BLEU/ROUGE-only as sufficient quality signal
- relying on uncalibrated judge outputs with no human checks
- ignoring order bias in pairwise judging
- no dataset/workflow compatibility guardrails

---

## Source-backed references

1. OpenAI evaluation best practices (design process, evaluator types, calibration guidance, architecture-specific eval points):
- https://platform.openai.com/docs/guides/evaluation-best-practices

2. OpenAI Evals API reference (eval object model and per-criteria results structure):
- https://platform.openai.com/docs/api-reference/evals/getRuns

3. HumanEval harness and safety note (functional correctness, pass@k usage, sandbox warning):
- https://github.com/openai/human-eval

4. Codex / HumanEval paper with unbiased pass@k estimator and sandbox rationale:
- https://arxiv.org/abs/2107.03374
- https://ar5iv.labs.arxiv.org/html/2107.03374

5. SWE-bench official repo (benchmark framing, Docker harness, operational constraints):
- https://github.com/SWE-bench/SWE-bench

6. SWE-bench Verified details (`FAIL_TO_PASS` + `PASS_TO_PASS`, requirement that both pass):
- https://openai.com/index/introducing-swe-bench-verified/

7. MT-Bench / Chatbot Arena LLM-as-judge findings (human agreement and known biases):
- https://arxiv.org/abs/2306.05685
- https://ar5iv.labs.arxiv.org/html/2306.05685

8. G-Eval (rubric-like structured judging with CoT/form-filling; human-correlation and bias caveat):
- https://arxiv.org/abs/2303.16634
- https://ar5iv.labs.arxiv.org/html/2303.16634

9. Position bias deep study and mitigation discussion for LLM judges:
- https://arxiv.org/abs/2406.07791
- https://ar5iv.labs.arxiv.org/html/2406.07791

10. HELM (multi-metric evaluation framing beyond accuracy):
- https://arxiv.org/abs/2211.09110

11. Vertex AI evaluation docs (pointwise/pairwise framing, supported scales, tool-call metrics):
- https://cloud.google.com/vertex-ai/generative-ai/docs/models/eval-python-sdk/determine-eval
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/evaluation
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/eval-python-sdk/view-evaluation

12. BEIR (retrieval benchmark diversity and robustness context):
- https://arxiv.org/abs/2104.08663
- https://ar5iv.labs.arxiv.org/html/2104.08663

13. RAGAS (reference-free RAG metric framing and metric families):
- https://arxiv.org/abs/2309.15217
- https://docs.ragas.io/en/latest/concepts/metrics/

14. EvalPlus benchmark rationale (expanded tests for stricter code evaluation):
- https://evalplus.github.io/
