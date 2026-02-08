# Workflow Execution + Evaluation Overhaul Plan (v3.0)

| Field | Value |
|---|---|
| Status | draft-ready-for-execution |
| JSON Source | docs/planning/workflow-eval-multiagent-execution-plan.json |
| Markdown File | docs/planning/workflow-eval-multiagent-execution-plan.md |
| Update Mode | replace-markdown-content-with-v3-structure |

## Summary

Redesign UI-driven workflow execution and evaluation for extensibility across dataset schemas, add SWE-style iterative bug-fix workflows in isolated Docker environments, and score with a hybrid policy emphasizing requirement satisfaction.

### Scope

Python SWE-first for v1; preserve existing DAG UX while adding iterative run-and-score features.

### Success Criteria

- Capability-driven workflow/dataset compatibility
- Execution-strategy abstraction for dag_once and iterative_repair
- Containerized repo checkout/build/test/patch loop
- Hybrid score with objective test dominance
- Live UI iteration timeline and artifact explorer
- Backward compatibility for existing workflows and endpoints

## Locked Decisions

| Decision | Value |
|---|---|
| Scope | python-swe-first |
| Isolation Runtime | docker-per-task |
| Scoring Mode | hybrid-weighted |
| Scoring Weights | tests=0.6, llm_judge=0.3, patch_similarity=0.1 |
| Repository Source Policy | git-mirrors-with-local-cache-and-commit-pinning |

## Current State Review

### Workflows Present

- code_review
- fullstack_generation
- plan_implementation

### Evaluation API Present

- GET /api/eval/datasets
- POST /api/run (evaluation payload)
- SSE streaming with evaluation_start/evaluation_complete

### Repository Datasets Current

- swe-bench
- swe-bench-lite
- swe-bench-verified
- humaneval
- humaneval-plus
- mbpp
- mbpp-sanitized
- codeclash

### Local Datasets Current

- agentic-workflows-v2/tests/fixtures/datasets/code_instructions_120k.json
- agentic-workflows-v2/tests/fixtures/datasets/code_review_instruct.json
- agentic-workflows-v2/tests/fixtures/datasets/codeparrot_apps.json
- agentic-workflows-v2/tests/fixtures/datasets/humaneval.json
- agentic-workflows-v2/tests/fixtures/datasets/mbpp.json
- agentic-workflows-v2/tests/fixtures/datasets/python_code_instructions_18k.json
- agentic-workflows-v2/tests/fixtures/datasets/react_code_instructions.json
- agentic-workflows-v2/tests/fixtures/datasets/swe_bench_lite.json
- agentic-workflows-v2/tests/fixtures/datasets/swe_bench_verified.json

### Known Gaps

- No native iterative repair strategy in engine
- No integrated containerized SWE execution lifecycle in /api/run path
- No workflow capability endpoint for compatibility reasoning
- No first-class artifact manifest endpoint
- Current scoring does not enforce objective repo test outcomes as primary pass gate

## Multi-Pass Structure

### Discovery and Capability Baseline

#### Outcomes

- Canonical capability model
- Dataset adapter contract
- Execution strategy taxonomy
- Hybrid scoring contract
- No unresolved interface decisions

#### Gate

Pass 2 can start only if all interface-level decisions are closed

### Architecture and Interfaces

#### Outcomes

- Public API and shared type definitions
- Runtime strategy and isolation specifications
- Scoring formula and gate semantics
- Live event protocol and UI integration contracts

#### Gate

Pass 3 can start only if API/types are versioned and testable

### Delivery, Testing, Rollout

#### Outcomes

- Phased implementation and acceptance gates
- Comprehensive test matrix
- Security and operations controls
- Rollout and observability plan

#### Gate

Execution-ready with no open design decisions

## Architecture

### Components

- WorkflowCapabilityRegistry
- DatasetAdapterRegistry
- ExecutionStrategyEngine
- IsolatedTaskRuntimeDocker
- HybridEvaluationOrchestrator
- RunArtifactStore
- LiveEventPublisher

### Execution Strategies

#### dag_once

Current DAG flow for existing workflows.

Compatibility goal: Backward compatible behavior and payloads.

#### iterative_repair

SWE bug-fix loop with retry until pass criteria or limits reached.

Flow:
- Normalize dataset sample into workflow inputs
- Create isolated workspace
- Clone from mirror and checkout base_commit
- Generate candidate patch
- Apply patch and run build/tests
- Evaluate attempt and decide continue/stop
- Persist artifacts and best result

Defaults:

| Field | Value |
|---|---|
| max_attempts | 5 |
| max_duration_minutes | 45 |

### Data Flow

- UI selects workflow, dataset, strategy, and evaluation policy
- Backend validates capability compatibility
- Execution strategy runs (dag_once or iterative_repair)
- Events stream to UI in real-time
- Artifacts and score persisted
- Run detail and artifacts queryable post-run

## API Changes

### New Endpoints

- `GET /api/workflows/{name}/capabilities`: Expose workflow capability contracts for compatibility and UI generation.
- `GET /api/runs/{run_id}/artifacts`: Retrieve patch, logs, judge rationale, and runtime metadata.

### Extended Endpoints

- `GET /api/eval/datasets`
  - dataset_family
  - schema_version
  - languages
  - requires_container
  - supports_gold_patch
  - required_workflow_capabilities
- `POST /api/run`
  - execution_profile
  - dataset_selection
  - evaluation_policy
  - `execution_profile`
    - strategy
    - max_attempts
    - max_duration_minutes
    - container_image
    - resource_limits
  - `dataset_selection`
    - dataset_id
    - sample_index
    - adapter_id
  - `evaluation_policy`
    - weights
    - pass_criteria
    - judge_profile

### Event Stream Additions

- iteration_start
- iteration_patch_generated
- iteration_patch_apply_result
- iteration_build_result
- iteration_test_result
- iteration_judge_result
- iteration_end
- run_artifact_ready

## Types and Interfaces

### New Types

- WorkflowCapability
- DatasetDescriptor
- DatasetSampleNormalized
- ExecutionProfile
- EvaluationPolicy
- PatchArtifact
- HybridEvaluationResult
- RunArtifactManifest
- IterationEvent

### Compatibility Rules

- Each workflow declares required capabilities and accepted dataset families.
- Each dataset declares schema family and runtime requirements.
- Run request fails fast with explicit compatibility errors when mismatched.

## Scoring Policy

| Field | Value |
|---|---|
| Mode | hybrid_weighted |
| Weights | tests=0.6, llm_judge=0.3, patch_similarity=0.1 |
| Test Score Formula | `test_score = 100 * (0.7 * f2p_rate + 0.3 * p2p_rate)` |
| Final Score Formula | `final_score = 0.60 * test_score + 0.30 * llm_judge_score + 0.10 * patch_similarity_score` |
| Soft Gate | `final_score >= 70` |

### Hard Gates

- `f2p_rate == 1.0`
- `p2p_rate >= 0.95`

### Notes

- Golden patch similarity is advisory and not a hard pass criterion.
- Requirement satisfaction is prioritized over exact gold-patch equivalence.

## Docker Isolation Specification

### Security Defaults

- No privileged containers
- Restricted network by default
- Explicit CPU/memory/time limits
- Ephemeral workspace with guaranteed cleanup
- No arbitrary host path access

### Runtime Requirements

- Docker engine on workers
- Pinned image versions
- Mirror-based repo source retrieval

## Workflow Portfolio

| Workflow | Priority | Strategy | Datasets | Primary Metric |
|---|---:|---|---|---|
| `swe_bugfix_iterative` | 1 | `iterative_repair` | swe-bench-lite, swe-bench-verified | hard-gate test pass rate with hybrid score reporting |
| `function_codegen_tested` | 2 | `iterative_with_tests` | humaneval-plus, mbpp-sanitized, apps | pass@k and deterministic test outcomes |
| `repo_code_review_quality` | 2 | `dag_once` | code_review_instruct, python_code_instructions_18k | quality rubric with evidence-backed scoring |
| `fullstack_feature_delivery` | 3 | `staged_generation_with_validation` | codeclash, local feature specs | requirement completion and integration test pass |

## Delivery Phases

### Phase 0: Contracts and Compatibility Foundation

#### Tasks

- Add capability and dataset descriptors
- Add compatibility validator
- Version shared API contracts

#### Exit Criteria

- Schema-level tests pass
- Mismatches return explicit actionable errors

### Phase 1: Isolated Runtime Foundation

#### Tasks

- Implement Docker task runtime
- Implement mirror+cache repo fetcher
- Add secure workspace lifecycle manager

#### Exit Criteria

- Fixture repo clone/checkouts deterministic
- Container security checks pass

### Phase 2: Iterative Repair Strategy

#### Tasks

- Integrate iterative_repair strategy
- Implement attempt loop controls
- Persist attempt-level artifacts

#### Exit Criteria

- Loop converges or exits cleanly by policy
- Artifacts queryable per attempt

### Phase 3: Hybrid Evaluation Engine

#### Tasks

- Compute objective test score
- Run judge rubric scoring
- Compute patch similarity and final score

#### Exit Criteria

- Score math deterministic and tested
- Hard/soft gate behavior verified

### Phase 4: UI Extensibility Overhaul

#### Tasks

- Build schema-driven run configuration UI
- Add compatibility matrix
- Add live iteration timeline and artifact explorer

#### Exit Criteria

- Current live execution feel preserved
- New iterative views function end-to-end

### Phase 5: Dataset Expansion and Validation Packs

#### Tasks

- Productionize SWE lanes
- Add function-level rigorous eval lanes
- Prepare rolling real-world benchmark lane

#### Exit Criteria

- Benchmark smoke matrix green
- Adapters validated for each dataset family

### Phase 6: Rollout and Operations

#### Tasks

- Feature-flag rollout by strategy and dataset family
- Observability dashboards and alerting
- Runbooks and rollback drills

#### Exit Criteria

- Release readiness gate accepted
- On-call docs complete

## Test Plan

### Unit

- Dataset adapter normalization for all supported schemas
- Capability compatibility and mismatch reason generation
- Hybrid scoring formulas and gate logic
- Patch similarity determinism
- Event payload schema validation

### Integration

- SWE iterative loop on fixture repos
- Docker lifecycle and cleanup
- Mirror cache hit/miss and commit pin behavior
- Artifact persistence and retrieval
- SSE event sequencing

### E2E Ui

- Workflow + dataset + strategy selection path
- Live iteration timeline rendering
- Score breakdown and rationale display
- Patch and log artifact inspection
- Backwards-compatible dag_once run path

### Non Functional

- Security hardening checks for sandbox and path traversal
- Resource limit enforcement
- Latency and throughput under parallel load
- Judge failure/fallback behavior

### Acceptance Gates

- Gate A: contracts and compatibility accepted
- Gate B: isolated runtime and strategy accepted
- Gate C: scoring and evidence accepted
- Gate D: UI and e2e accepted
- Gate E: CI/security/release readiness accepted

## Dataset Recommendations

### V1

- SWE-bench Lite
- SWE-bench Verified
- HumanEval+ (EvalPlus)
- MBPP+ / MBPP sanitized

### V1.5

- SWE-bench-Live
- LiveCodeBench
- RepoBench (repo-level retrieval/completion checks)

### V2

- BugsInPy
- Defects4J
- SWE-bench Multilingual / Multi-SWE-bench

## Risks and Mitigations

- Risk: Flaky upstream repo tests create unstable scoring.
  - Mitigation: Introduce flaky-test quarantine profile and repeatable verification mode.
- Risk: Mirror/source drift undermines reproducibility.
  - Mitigation: Commit pinning and immutable cache metadata.
- Risk: Judge model variability impacts score consistency.
  - Mitigation: Low-temperature fixed prompts and optional adjudication run.
- Risk: Execution cost escalation from iterative retries.
  - Mitigation: Attempt/time caps and early-stop policies.
- Risk: Security exposure when running untrusted repo code.
  - Mitigation: Strict container policy, restricted network, no privileged mode, ephemeral teardown.

## Assumptions

- Docker is available in evaluation environments.
- Git mirror infrastructure is available and maintained.
- Python-first scope is acceptable for v1 timelines.
- Golden patch exact match is not a product requirement.
- Existing workflows must remain backward compatible under dag_once.

## References

1. SWE-bench paper: https://arxiv.org/abs/2310.06770
2. SWE-bench website: https://www.swebench.com/
3. SWE-bench Lite: https://www.swebench.com/lite.html
4. SWE-bench Live: https://swe-bench-live.github.io/
5. SWE-bench Verified dataset: https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified
6. LiveCodeBench: https://arxiv.org/abs/2403.07974
7. EvalPlus (HumanEval+/MBPP+): https://arxiv.org/abs/2305.01210
8. APPS benchmark: https://arxiv.org/abs/2105.09938
9. BugsInPy: https://github.com/soarsmu/BugsInPy
10. Defects4J: https://github.com/rjust/defects4j
11. RepoBench: https://arxiv.org/abs/2306.03091
12. SWE-bench Multilingual: https://www.swebench.com/multilingual
13. Multi-SWE-bench: https://arxiv.org/abs/2504.02605
