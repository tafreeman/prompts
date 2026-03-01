# ADR Compiled Registry — agentic-workflows-v2

> **Document type:** Canonical compiled ADR registry  
> **Repo:** `tafreeman/prompts → agentic-workflows-v2`  
> **Last validated:** 2026-02-22  
> **ADR authors:** Opus (Claude) — ADR-001 through ADR-003  
> **Planned ADR program:** ADR-0004 through ADR-0023 (iteration-04 governance spec)  
> **Status:** ADR-001, ADR-002, ADR-003 — Accepted · ADR-0004 through ADR-0023 — Proposed (awaiting authoring)

---

## Table of Contents

1. [ADR-001 — Dual Execution Engine: LangGraph Pregel vs. Native Kahn's DAG](#adr-001)
2. [ADR-002 — SmartModelRouter Circuit-Breaker Hardening](#adr-002)
3. [ADR-003 — Deep Research Supervisor State Machine with Composite CI Gating](#adr-003)
4. [ADR-0004 through ADR-0023 — Planned ADR Program Registry](#planned-adr-registry)
5. [References](#references)

---

## Preamble

Three critical architectural concerns face the `agentic-workflows-v2` monorepo: a dual execution engine that risks behavioral divergence, a circuit-breaker design exposed to cascade failures across LLM providers, and a supervisor state machine governing multi-round deep research with composite quality gating. Each concern carries production-reliability implications. The analysis below produces a formal ADR for each, grounded in workflow orchestration literature, distributed systems resilience patterns, and formal state machine theory.

---

<a id="adr-001"></a>
## ADR-001: Dual Execution Engine — LangGraph Pregel vs. Native Kahn's DAG

**Status:** Accepted  
**Date:** 2026-02-22  
**Deciders:** Architect, Backend Lead  
**Tags:** execution-engine, langgraph, dag, architecture  
**Supersedes:** —  
**Superseded-By:** —

### Context

The repository maintains two active execution engines serving overlapping purposes. The **LangGraph engine** (`agentic_v2/langchain/`) uses `StateGraph` compiled to a `CompiledGraph` extending `Pregel` — Google's Bulk Synchronous Parallel model adapted by LangChain. It provides integrated checkpointing at every superstep, channel-based state management with typed reducers, streaming, human-in-the-loop interrupts, and time-travel debugging. The **native DAG executor** (`agentic_v2/engine/dag_executor.py`) implements Kahn's topological sort algorithm (Kahn, 1962) with dynamic parallel scheduling via `asyncio`, `StepExecutor`, `ExecutionContext`, and `StepStateManager`. The orchestrator agent's `execute_as_dag` method explicitly constructs and dispatches workflows through this second engine.

This dual-engine situation creates three risks: **behavioral divergence** (identical YAML workflows producing different outputs through different engines), **maintenance burden** (two codepaths for execution, error handling, and state management), and **feature asymmetry** (LangGraph provides ~9 integrated capabilities — checkpointing, streaming, human-in-the-loop, time travel, subgraph support — that the native engine would need to reimplement independently).

### Options Considered

**Option A — Consolidate to LangGraph only.** Temporal.io's architecture offers the strongest precedent: a single, opinionated execution engine with strict determinism requirements produces the highest reliability. Temporal's production users report "production issues falling from once-a-week to near-zero." LangGraph's Pregel execution model provides automatic checkpointing at every superstep, fault-tolerant resume, and streaming. However, LangGraph's BSP scheduling is **conservative with parallelism**: even when a node's dependencies are satisfied, it waits until the entire current superstep completes before scheduling the next batch.

**Option B — Consolidate to native DAG only.** Kahn's algorithm delivers **optimal wavefront parallelism** — every node whose in-degree reaches zero is immediately schedulable, without waiting for unrelated nodes to complete. The algorithm runs in Θ(n + m) time. However, this path requires reimplementing checkpointing, state persistence, streaming, human-in-the-loop, time travel, conditional routing, and subgraph support. Prefect's evolution is instructive: they deliberately moved away from DAG-only execution toward richer execution models.

**Option C — Keep both with a conformance layer.** Apache Airflow provides direct precedent: since version 2.10.0, Airflow supports **multiple simultaneous executors** via comma-separated configuration, with per-task or per-DAG executor routing. This validates the pattern of maintaining parallel execution backends. However, verifying behavioral equivalence between engines is fundamentally hard — Rice's theorem establishes that proving behavioral equivalence is undecidable in general.

**Option D — Abstract behind a common `ExecutionEngine` interface.** This approach creates a facade that dispatches to either backend based on workflow characteristics, following the Strangler Fig migration pattern. Martin Fowler's updated guidance (2024) explicitly endorses transitional architecture: people often balk at building transitional architecture, but "the reduced risk and earlier value from the gradual approach outweigh its costs." The interface would expose `execute(workflow_def) → ExecutionResult` with engine selection based on workflow capabilities (cycles → LangGraph, pure DAG with max parallelism → Kahn's).

### Tradeoff Matrix

| Criterion | A: LangGraph only | B: Native DAG only | C: Both + conformance | D: Common interface |
|---|---|---|---|---|
| **Maintenance cost** | Low (single engine) | Low (single engine) | High (two engines + test layer) | Medium (interface + two engines) |
| **Feature completeness** | High (built-in) | Low (must reimplement ~9 features) | High (use each engine's strengths) | High (delegate to appropriate engine) |
| **Scheduling optimality** | Moderate (BSP conservatism) | Optimal (wavefront parallelism) | Optimal (route by need) | Optimal (route by need) |
| **Behavioral consistency** | Guaranteed (one engine) | Guaranteed (one engine) | Risk of divergence | Risk of divergence (mitigated by routing) |
| **Migration risk** | Medium (must migrate all DAG workflows) | High (must reimplement LangGraph features) | Low (no migration needed) | Low (incremental migration) |
| **Vendor coupling** | High (LangGraph API) | None | Medium | Low (abstracted) |
| **Production precedent** | Temporal.io | — | Airflow 2.10+ | Strangler Fig pattern |

### Decision

**Adopt Option D (common interface) as transitional architecture, converging toward Option A (LangGraph) over 2–3 quarters.** The `ExecutionEngine` protocol should define `async execute(workflow: WorkflowDefinition, context: ExecutionContext) → ExecutionResult` with implementations `LangGraphEngine` and `KahnDAGEngine`. Route workflows containing cycles, human-in-the-loop nodes, or checkpointing requirements to LangGraph; route pure computation DAGs where maximum parallelism matters to the Kahn's engine. As LangGraph matures and parallelism improves, migrate remaining workflows to LangGraph and retire the native engine.

### Consequences

**Positive:** Immediate risk reduction through interface abstraction. Incremental migration path. Preserves Kahn's algorithm's parallelism advantage for compute-heavy DAGs during transition. Conformance testing becomes scoped to the interface contract rather than full behavioral equivalence.

**Negative:** Transitional architecture has a carrying cost. The interface must be narrow enough to be implementable by both engines but expressive enough to expose each engine's strengths. LangGraph's Pregel API is explicitly documented as "not intended to be instantiated directly by consumers" — the abstraction must work at the `StateGraph` level, not the Pregel level.

### Code-Level Recommendations

1. **Create `agentic_v2/engine/protocol.py`** defining `ExecutionEngine(Protocol)` with `execute`, `checkpoint`, and `get_status` methods.
2. **Wrap `agentic_v2/langchain/` in `LangGraphEngine`** implementing the protocol, delegating to `StateGraph.compile().ainvoke()`.
3. **Wrap `agentic_v2/engine/dag_executor.py` in `KahnEngine`** implementing the same protocol.
4. **Add `engine_selector.py`** that inspects `WorkflowDefinition` metadata (cycles, HiTL nodes, checkpoint requirements) and dispatches to the appropriate engine.
5. **Implement shadow execution mode** in CI: run a canonical workflow suite through both engines, compare final state outputs using property-based assertions. Use `hypothesis` for property-based test generation.
6. **Refactor `orchestrator.py`'s `execute_as_dag`** to call through the protocol interface rather than directly constructing DAGs.

### Validation Plan

- `ExecutionEngine` protocol with full type annotations; `LangGraphEngine` and `KahnEngine` pass `mypy --strict`.
- `engine_selector.py` routes correctly for 5 canonical workflow types (pure DAG, cyclic, HiTL, checkpoint-requiring, streaming).
- Shadow execution CI passes: output field equality verified for all canonical workflows across both engines.
- Zero direct `dag_executor.py` instantiations remain in `orchestrator.py`.
- Conformance test suite achieves ≥ 90% branch coverage on protocol implementations.
- Migration roadmap documented with per-workflow engine assignments and quarterly consolidation checkpoints.

### References

- LangGraph Pregel concepts — https://langchain-ai.github.io/langgraph/concepts/
- Temporal.io single-engine reliability — https://temporal.io/blog/reliable-workflows
- Apache Airflow multi-executor — https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html
- Martin Fowler, Strangler Fig Application (2024) — https://martinfowler.com/bliki/StranglerFigApplication.html
- Kahn, A.B. (1962), "Topological sorting of large networks" — Communications of the ACM
- Rice's theorem on undecidability of behavioral equivalence — classical computer science

---

<a id="adr-002"></a>
## ADR-002: SmartModelRouter Circuit-Breaker Hardening for Multi-Backend LLM Routing

**Status:** Accepted  
**Date:** 2026-02-22  
**Deciders:** Backend Lead  
**Tags:** smart-router, circuit-breaker, reliability, rate-limiting, multi-provider  
**Supersedes:** —  
**Superseded-By:** —

### Context

The `SmartModelRouter` (`smart_router.py`) extends `ModelRouter` with per-model `ModelStats` tracking (EMA latency, percentile tracking from p50–p99, sliding window), a three-state circuit breaker (CLOSED → OPEN → HALF_OPEN), adaptive cooldowns via `CooldownConfig` (base 30s failure / 120s rate-limit / 60s timeout, **1.5× consecutive multiplier**, 600s max), and health-weighted model selection scoring success_rate at 60%, low latency at 20%, and recency at 20%. The fallback chain executes across **5+ providers** (GitHub Models, OpenAI, Azure OpenAI, Gemini, Anthropic, Ollama, local Phi Silica), classifying errors into rate-limit, timeout, and permanent categories.

Five specific risks threaten production reliability: cascade failures when multiple providers fail simultaneously, incorrect cooldown timing from wall-clock dependence, thundering-herd effects during half-open recovery, flat-rate cooldowns that ignore provider-specific rate-limit signals, and file-based stats persistence that breaks under multi-process deployments.

### Risk Analysis

#### (A) Cascade Failure Prevention

When one provider fails, its traffic redistributes to remaining providers. If OpenAI goes down and its load shifts entirely to Anthropic, Anthropic may become overloaded and trip its own circuit breaker — a classic cascade. Google's SRE book (Chapter 22) documents this precisely: "If cluster B fails, requests to cluster A increase to 1,200 QPS...the rate of successfully handled requests in A dips well below 1,000 QPS."

**Recommendation:** Implement **per-provider bulkhead isolation** with concurrent request limits. Each provider gets an independent semaphore (e.g., max 10 concurrent to Ollama, max 50 to OpenAI). When a provider's circuit opens, redistribute traffic proportionally across remaining providers *weighted by their remaining capacity*, not uniformly. Implement Google's **client-side adaptive throttling**: track `requests` (attempted) and `accepts` (succeeded) per provider over a 2-minute window, reject new requests with probability `max(0, (requests - K × accepts) / (requests + 1))` where K=2.

#### (B) Partial Failure Handling

The current `get_model_for_tier` returns `None` when all candidates are exhausted. Three of five providers down simultaneously is not a theoretical edge case — correlated failures happen when providers share infrastructure (e.g., Azure outages affecting both Azure OpenAI and GitHub Models).

**Recommendation:** Implement a **tiered degradation strategy**. When primary tier models are exhausted, automatically fall through to lower tiers with reduced capability rather than returning `None`. Add a `degraded_mode` flag to responses so callers know they received a lower-tier model. Keep local Ollama or Phi Silica as an **always-available last-resort** bulkhead. Add a global `system_health` metric: when >50% of providers are in OPEN state, activate load-shedding.

#### (C) Cooldown Timer Correctness

The current implementation uses `datetime.now(timezone.utc)` for cooldown comparisons. Wall clocks are subject to **NTP step corrections** that can jump forward or backward. A backward jump extends cooldowns unexpectedly; a forward jump ends them prematurely. Python's `time.monotonic()` uses `CLOCK_MONOTONIC` on Linux, which is immune to NTP steps and never runs backward.

**Recommendation:** Replace all cooldown/timeout tracking with `time.monotonic()`. Store wall-clock timestamps separately for logging and debugging only.

```python
# BEFORE (dangerous)
cooldown_end = datetime.now(timezone.utc) + timedelta(seconds=60)
is_cooled = datetime.now(timezone.utc) >= cooldown_end

# AFTER (correct)
cooldown_end = time.monotonic() + 60.0
is_cooled = time.monotonic() >= cooldown_end
```

#### (D) Half-Open Probe Strategy

The current design requires **2 successes** to transition from HALF_OPEN to CLOSED. In a multi-threaded `SmartModelRouter`, two threads could simultaneously probe a half-open provider, one succeeding and one failing, leading to inconsistent state transitions.

**Recommendation:** Implement **serialized recovery probes with a lock**. Only one request at a time should probe a HALF_OPEN provider; all others receive immediate fallback. Use an `asyncio.Lock` per provider for probe coordination. Additionally, implement **exponential backoff on the reset timeout**: if a probe fails in HALF_OPEN, return to OPEN with `reset_timeout × 1.5` (capped at max cooldown). For LLM routing where each call is expensive, **1 probe request** is more cost-effective than Resilience4j's default of 10.

#### (E) Rate-Limit Awareness

The current flat **120s cooldown** for rate limits ignores that providers communicate exactly when limits reset. OpenAI returns `x-ratelimit-reset-requests` and `x-ratelimit-reset-tokens` on every response, plus `Retry-After` on 429 errors. A 120s cooldown when the actual reset is in 3 seconds wastes 40× the provider's available capacity.

**Recommendation:** Parse provider-specific rate-limit headers and use them to set precise cooldown durations. Implement a **dual token bucket** per provider tracking both RPM (requests per minute) and TPM (tokens per minute). Fall back to exponential backoff with jitter when headers are unreliable.

### Risk Severity Matrix

| Risk | Likelihood | Severity | Current Mitigation | Recommended Mitigation |
|---|---|---|---|---|
| All providers down simultaneously | Low | Critical | Returns None | Local Ollama last-resort + load shedding |
| Cascade failure (overload redistribution) | Medium | High | None | Bulkhead semaphores + adaptive throttling |
| Thundering herd on HALF_OPEN recovery | Medium | Medium | None | Lock-based serialized probes |
| Clock skew corrupts cooldowns | Low | Medium | None | Switch to `time.monotonic()` |
| Flat rate-limit cooldown wastes capacity | High | Medium | 120s fixed cooldown | Parse Retry-After + dual token bucket |
| Stats file corruption under multi-process | Medium | Low | Atomic JSON write | SQLite WAL mode or `multiprocessing.Manager()` |
| Correlated provider failures (shared infra) | Medium | High | Independent breakers | Diversify across cloud regions |
| Half-open race conditions | Medium | Medium | None | `asyncio.Lock` per provider |

### Decision

Implement all five hardening measures (A–E) in priority order: **(C) clock correctness** first (lowest effort, prevents silent bugs), then **(E) rate-limit awareness** (highest capacity recovery), then **(D) half-open serialization** (prevents thundering herd), then **(A) cascade prevention** (bulkheads + adaptive throttling), and finally **(B) partial failure strategy** (most architectural change). Each is independently deployable.

### Consequences

**Positive:** Eliminates the five identified reliability risks. Provider-aware rate limiting recovers capacity faster — honoring a 3s `Retry-After` instead of waiting 120s yields **40× faster recovery** for rate-limited providers. Monotonic clock usage prevents all clock-skew-related timer bugs. Serialized probes eliminate half-open state races.

**Negative:** Increased complexity in `smart_router.py` and `model_stats.py`. Per-provider token buckets require parsing provider-specific header formats, creating a maintenance burden as providers change their APIs. Bulkhead semaphore limits must be tuned per-provider and per-deployment.

### Code-Level Recommendations

1. **`model_stats.py`**: Replace all `datetime.now(timezone.utc)` comparisons with `time.monotonic()` for cooldown tracking. Add a `_monotonic_reference` field for serialization.
2. **`smart_router.py`**: Add `_provider_semaphores: dict[str, asyncio.Semaphore]` for bulkhead isolation. Add `_probe_locks: dict[str, asyncio.Lock]` for half-open serialization.
3. **Create `agentic_v2/models/rate_limit_tracker.py`**: Implement `TokenBucket` class with `consume(tokens: int) → bool` and `refill_from_headers(headers: dict)`. Maintain dual buckets (RPM/TPM) per provider.
4. **`smart_router.py` `_execute_with_fallback`**: After any successful response, call `rate_limit_tracker.update_from_headers(response.headers)`. On 429, parse `Retry-After` and set cooldown to `max(retry_after_seconds, base_rate_limit_cooldown)`.
5. **`smart_router.py` `get_model_for_tier`**: When returning `None`, attempt lower-tier models before giving up. Set `response.degraded = True` flag when serving from a lower tier.
6. **`model_stats.py` persistence**: Replace JSON atomic write with SQLite using WAL mode for multi-process safety, or use `multiprocessing.Manager().dict()` for shared-memory state.

### Validation Plan

- All 5 hardening measures independently deployable and reversible.
- Unit tests for monotonic clock replacement: NTP skew simulation does not corrupt cooldowns.
- Rate-limit header parsing tests: Retry-After honored over flat 120s for sampled providers.
- Bulkhead semaphore load test: upstream provider failure does not cascade to >1 additional provider.
- Half-open lock test: concurrent probe threads do not produce split-brain state transitions.
- Multi-process stats persistence test: concurrent writes produce consistent state via SQLite WAL.

### References

- Google Site Reliability Engineering, Chapter 22 — https://sre.google/sre-book/handling-overload/
- Resilience4j Circuit Breaker — https://resilience4j.readme.io/docs/circuitbreaker
- Python `time.monotonic()` — https://docs.python.org/3/library/time.html#time.monotonic
- AWS Well-Architected Reliability Pillar — https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html
- OpenAI Rate Limit Headers — https://platform.openai.com/docs/guides/rate-limits
- Bolshakov (2025), Circuit Breaker coordination — [Tier B engineering reference]

---

<a id="adr-003"></a>
## ADR-003: Deep Research Supervisor State Machine with Composite CI Gating

**Status:** Accepted  
**Date:** 2026-02-22  
**Deciders:** Research Lead  
**Tags:** deep-research, supervisor, confidence-index, state-machine, ci-gating  
**Supersedes:** —  
**Superseded-By:** —

### Context

The `deep_research.yaml` workflow defines a **10-node pipeline** with bounded unrolled rounds R1–R4:

```
intake_scope → source_policy → [hypothesis_tree_tot → retrieval_react → analyst_ai + analyst_swe → cove_verify → coverage_confidence_audit] × R1-R4 → supervisor_decide → final_synthesis → rag_package
```

Each round has conditional `when` expressions gating on the composite Confidence Index:

**CI = 0.25×coverage + 0.20×source_quality + 0.20×agreement + 0.20×verification + 0.15×recency**

with a threshold of CI ≥ 0.80 and additional gating on `recent_source_count` and `critical_contradictions > 0`. The supervisor uses a `coalesce()` pattern to select which round's output to forward.

This design implements techniques from three foundational papers: **ReAct** (Yao et al., ICLR 2023) for interleaved reasoning and action in the retrieval loop, **Tree of Thoughts** (Yao et al., NeurIPS 2023) for the `hypothesis_tree_tot` node's branching exploration, and **Chain of Verification** (Dhuliawala et al., ACL 2024) for the `cove_verify` node's independent verification step. The bounded unrolling approach (R1–R4 as explicit YAML steps) trades configuration duplication for deterministic, inspectable execution paths — aligned with bounded model checking's practice of "unrolling the transition relation of a finite state machine for a fixed number of steps k."

### Formal State Transition Model

Applying Harel statechart formalism (Harel, 1987), the supervisor operates as a **hierarchical state machine** with three levels:

```
SUPERSTATE: DeepResearch
├─ INIT → Planning
├─ Planning
│   ├─ intake_scope (entry: parse query, decompose search space)
│   └─ source_policy (entry: define source constraints)
│       → [complete] → Execution
├─ Execution (SUPERSTATE with history H*)
│   ├─ Round[n] for n ∈ {1..4}    [guard: max_rounds >= n]
│   │   ├─ hypothesis_tree_tot    (ToT branching exploration)
│   │   ├─ retrieval_react        (ReAct search-fetch loop)
│   │   ├─ PARALLEL REGION:
│   │   │   ├─ analyst_ai         (domain analysis)
│   │   │   └─ analyst_swe        (technical analysis)
│   │   ├─ cove_verify            (CoVe independent verification)
│   │   └─ coverage_confidence_audit (compute CI, 6 metrics)
│   │       → [CI >= 0.80 AND all floors pass] → Coalesce
│   │       → [CI < 0.80 AND n < max_rounds] → Round[n+1]
│   │       → [n == max_rounds] → Coalesce
│   └─ H* (deep history: remembers best round state)
├─ Coalesce
│   ├─ entry: best_round = argmax(CI(r) for r in completed_rounds)
│   ├─ [best_CI >= 0.80] → Synthesis(full_confidence)
│   └─ [best_CI < 0.80] → Synthesis(degraded)
└─ Synthesis
    ├─ final_synthesis (entry: compose report from best_round output)
    └─ rag_package (entry: package for RAG indexing)
        → FINAL
```

### Risk Analysis

#### (B) Partial CI Pass Handling — Compensability Vulnerability

The current design gates on composite CI only. This creates a **compensability vulnerability**: a research output with `verification_score = 0.35` with other scores at 0.90+ yields CI = 0.81 — a passing score despite severely inadequate verification.

Multi-criteria decision analysis (MCDA) literature identifies this as the **compensability problem** inherent in weighted arithmetic means. Healthcare quality measurement has converged on a hybrid approach where individual measure minimums prevent dangerous metric compensation.

**Recommendation:** Implement **two-tier gating**:

- **Tier 1 — Per-metric floors** (non-compensatory): `source_quality ≥ 0.40`, `verification ≥ 0.40`, `coverage ≥ 0.35`, `agreement ≥ 0.35`, `recency ≥ 0.30`, `recent_source_count ≥ inputs.min_recent_sources`
- **Tier 2 — Composite gate** (compensatory): CI ≥ 0.80

Both tiers must pass. If Tier 1 fails but Tier 2 passes, the supervisor should trigger a **targeted remediation round** that re-executes only the failing dimension's nodes rather than a full round.

#### (C) Round Regression Mitigation

The SELF-REFINE paper (Madaan et al., NeurIPS 2023) explicitly acknowledges that "output quality can vary during iteration with improvement in one aspect but decline in another." Round 3 might discover sources that introduce contradictions absent in Round 2's output, causing `agreement_score` to drop even as `coverage_score` improves.

**Recommendation:** The supervisor should maintain a **running best** across rounds:

```python
if CI(round_n) > CI(best_round_so_far):
    best_round = round_n        # improvement
elif CI(round_n) < CI(round_n-1):
    regression_count += 1       # track regressions
    if regression_count >= 2:
        break  # early-stop: consecutive regressions signal diminishing returns
```

#### (D) Metric Independence vs. Composite Gating

The CI formula's weights (0.25 + 0.20 + 0.20 + 0.20 + 0.15 = 1.0) are a valid weighted arithmetic mean. The current weight assignment prioritizes **coverage** (0.25) as the most important dimension. **Recency** carries the lowest weight (0.15), appropriate since many research topics don't require ultra-recent sources.

**Recommendation:** Conduct **weight sensitivity analysis** by computing CI under ±0.05 perturbations of each weight. Consider using the **geometric mean** as an alternative aggregation — it is less compensatory than the arithmetic mean and more heavily penalizes low scores on any dimension:

```python
# Geometric mean alternative (less compensatory)
CI_geometric = (coverage**0.25 * source_quality**0.20 * agreement**0.20 
                * verification**0.20 * recency**0.15)
```

The geometric mean naturally enforces that no single metric can be near-zero without dragging the composite down significantly. With the arithmetic mean, `verification = 0.10` contributes only -0.16 to CI; with the geometric mean, it contributes a multiplicative factor of `0.10^0.20 ≈ 0.63` — far more punishing.

#### (E) Graceful Degradation When max_rounds Exhausted

When all R1–R4 rounds complete without achieving CI ≥ 0.80, the system must deliver the best available result rather than failing entirely. Google SRE's principle: "Serve lower-quality, cheaper-to-compute results to the user" when under stress. AWS Well-Architected: "Application components should continue to perform their core function even if dependencies become unavailable."

**Recommendation:** Implement **tiered delivery** based on the best CI achieved:

| Best CI Achieved | Delivery Tier | Behavior |
|---|---|---|
| ≥ 0.80 | Full confidence | Deliver without qualification |
| 0.65 – 0.79 | Moderate confidence | Deliver with warning; highlight weak metrics |
| 0.50 – 0.64 | Low confidence | Deliver with prominent disclaimer; mark unverified sections |
| < 0.50 | Insufficient | Flag for human review; deliver only if explicitly requested |

Attach structured **quality metadata** to every output:

```yaml
confidence_level: "moderate"
best_ci_achieved: 0.74
target_ci: 0.80
selected_round: 2       # best-of-4, not necessarily the last
rounds_completed: 4
failing_metrics:
  - verification: 0.55
  - recency: 0.48
passing_metrics:
  - coverage: 0.85
  - source_quality: 0.82
  - agreement: 0.78
```

### Bounded Unrolling — Design Validation

The current approach of explicitly defining R1–R4 as separate YAML steps (static unrolling) rather than using engine-level dynamic looping is the correct architectural decision. Bounded model checking literature confirms: "BMC operates by unrolling the transition relation of a finite state machine for a fixed number of steps k." Static unrolling provides **deterministic execution paths**, **no dynamic graph construction overhead**, **independent checkpointability per round**, and **bounded resource consumption known a priori**.

### Decision

Adopt the **two-tier gating system** (per-metric floors + composite CI), implement **best-of-N selection with consecutive regression early-stopping**, add **targeted remediation rounds** for partial CI failures, and implement **tiered graceful degradation** with structured quality metadata. Retain the bounded unrolled R1–R4 architecture. Evaluate geometric mean aggregation as an alternative to the arithmetic mean through sensitivity analysis.

### Consequences

**Positive:** Two-tier gating eliminates the compensability vulnerability where one critical metric near zero passes due to strong performance on others. Best-of-N selection with regression detection prevents wasted computation when iterative refinement has peaked. Tiered degradation ensures users always receive the best available output with transparent quality signaling. Structured metadata enables downstream systems to make informed decisions about output reliability.

**Negative:** Per-metric floors introduce 6 additional thresholds to tune and maintain. Targeted remediation rounds add conditional branching complexity to the YAML workflow. The regression detection heuristic (2 consecutive regressions → stop) may occasionally stop too early if Round 4 would have recovered.

### Code-Level Recommendations

1. **`deep_research.yaml`**: Add `floor_thresholds` to the workflow inputs: `{coverage: 0.35, source_quality: 0.40, agreement: 0.35, verification: 0.40, recency: 0.30}`. Add `when` conditions to each round that check both floor gates and composite CI.
2. **`coverage_confidence_audit` node**: Return both `ci_score` (composite) and individual metric scores as separate output fields. Add a `floor_violations: list[str]` output field listing any metrics below their floor.
3. **`supervisor_decide` node**: Implement `best_round = argmax(ci_scores)` rather than always selecting the latest round. Add `regression_count` tracking and early-stop logic. Add `confidence_level` classification (full/moderate/low/insufficient).
4. **Create `agentic_v2/workflows/lib/ci_calculator.py`**: Centralize the CI formula, floor checks, and sensitivity analysis utilities. Support both arithmetic and geometric mean aggregation with a config switch.
5. **`final_synthesis` node**: Accept `confidence_level` and `quality_metadata` from the supervisor. Embed quality disclaimers in the output when `confidence_level != "full"`.
6. **Add YAML template macros** for round definitions to reduce duplication across R1–R4. Each round should reference a shared `research_round` template with `round_number` as a parameter.

### Validation Plan

- Two-tier gating unit tests: verify compensability vulnerability is closed (verification=0.10 with other scores=0.90 does not pass).
- Regression early-stop test: confirm execution halts after 2 consecutive CI regressions regardless of `max_rounds`.
- Tiered delivery test: verify correct `confidence_level` label and quality metadata for CI buckets (full/moderate/low/insufficient).
- Geometric vs. arithmetic mean sensitivity analysis: CI outcomes stable under ±0.05 weight perturbations.
- Targeted remediation test: single failing floor metric triggers only the relevant node subset, not full re-execution.

### References

- ReAct (Yao et al., ICLR 2023) — https://arxiv.org/abs/2210.03629
- Tree of Thoughts (Yao et al., NeurIPS 2023) — https://arxiv.org/abs/2305.10601
- Chain of Verification (Dhuliawala et al., ACL 2024) — https://arxiv.org/abs/2309.11495
- SELF-REFINE (Madaan et al., NeurIPS 2023) — https://arxiv.org/abs/2303.17651
- Harel, D. (1987), "Statecharts: A visual formalism for complex systems" — Science of Computer Programming
- Google SRE Book, Chapter 22 — https://sre.google/sre-book/handling-overload/
- AWS Well-Architected Reliability Pillar — https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html
- Bounded Model Checking — Clarke et al., TACAS 1999
- MCDA Compensability Problem — Belton & Stewart (2002), Multiple Criteria Decision Analysis

---

<a id="planned-adr-registry"></a>
## Planned ADR Program Registry — ADR-0004 through ADR-0023

> **Status:** All entries are **Proposed** — titles, owners, and reference mappings are defined. Full authoring of each ADR body is the next workstream. Authored ADRs must follow the template defined in ADR-0005.

| ADR ID | Title | Category | Key References | Status |
|---|---|---|---|---|
| ADR-0004 | ADR lifecycle and state machine policy | Governance | R16, R17, R18 | Proposed |
| ADR-0005 | ADR template standard (MADR-inspired + Nygard core) | Governance | R15, R20, R21, R22 | Proposed |
| ADR-0006 | Immutable accepted ADRs; supersede-only evolution | Governance | R16, R17 | Proposed |
| ADR-0007 | Ownership and review cadence | Governance | R16, R17 | Proposed |
| ADR-0008 | In-repo storage, optional wiki mirror | Governance | R16, R18, R19 | Proposed |
| ADR-0009 | ADR brevity and decision-only scope (not design docs) | Governance | R18 | Proposed |
| ADR-0010 | Deep-research workflow shape (bounded rounds) | Workflow | R9, R10, R11 | Proposed |
| ADR-0011 | Source tiering policy | Source Governance | R1, R2, R3, R4 | Proposed |
| ADR-0012 | Recency minimum gate (183-day window) | Source Governance | R1, R8 | Proposed |
| ADR-0013 | Date extraction precedence (implementation inference + governance consistency) | Source Governance | R16, R18 | Proposed |
| ADR-0014 | Tree of Thoughts planner stage | Workflow | R13 | Proposed |
| ADR-0015 | ReAct retrieval stage | Workflow | R12 | Proposed |
| ADR-0016 | Chain-of-Verification verifier stage | Workflow | R14 | Proposed |
| ADR-0017 | Confidence Index formula and stop policy | Metrics | R7, R10 | Proposed |
| ADR-0018 | Critical-claim dual-source rule | Citation Policy | R14, R16, R18 | Proposed |
| ADR-0019 | Citation completeness gate | Citation Policy | R1, R6, R7 | Proposed |
| ADR-0020 | RAG artifact contract | Output | R3, R10, R11 | Proposed |
| ADR-0021 | Tool allowlists and safety defaults | Safety | R2, R5, R10 | Proposed |
| ADR-0022 | Bounded iteration + partial-output fallback | Resilience | R10, R11 | Proposed |
| ADR-0023 | Unit-test strategy and deterministic fixtures | Testing | R10, R18, R22 | Proposed |

### ADR Template (Enforced by Tests from ADR-0023)

All authored ADRs must conform to the following template. Structural compliance is validated by `test_adr_required_sections`, `test_adr_status_valid`, `test_adr_numbering_monotonic`, `test_adr_supersede_links_reciprocal`, `test_adr_has_validation_plan`, and `test_adr_has_references`.

```markdown
# ADR 00XX — Title

Status: Proposed | Accepted | Rejected | Deprecated | Superseded
Date: YYYY-MM-DD
Deciders: ...
Consulted: ...
Informed: ...
Tags: ...
Supersedes: ...
Superseded-By: ...

## Context and Problem Statement
## Decision Drivers
## Options Considered
## Decision Outcome
## Why This Decision
## Consequences
## Validation Plan
## References
```

### ADR Program Quality Gates

The following test assertions must pass for every authored ADR before it transitions from Proposed → Accepted:

1. Required metadata and section checks (`test_adr_required_sections`)
2. Status is one of the allowed values (`test_adr_status_valid`)
3. ADR numbering is monotonic and unique (`test_adr_numbering_monotonic`)
4. Supersession links are reciprocal (`test_adr_supersede_links_reciprocal`)
5. Validation plan is present and non-empty (`test_adr_has_validation_plan`)
6. References section is present with ≥1 citation (`test_adr_has_references`)

---

<a id="references"></a>
## Master Reference Index

> Reference IDs map to `agentic-v2-eval/docs/deep_research_plan_series/reference-map.md`. Tier A sources required for all architectural claims; ≥2 independent Tier A sources required per critical architectural recommendation.

| ID | Resource | URL | Tier |
|---|---|---|---|
| R1 | OpenAI — Introducing deep research | https://openai.com/index/introducing-deep-research/ | A |
| R2 | OpenAI — Tools guide | https://developers.openai.com/api/docs/guides/tools | A |
| R3 | OpenAI — Web search tool guide | https://developers.openai.com/api/docs/guides/tools-web-search | A |
| R4 | OpenAI — File search tool guide | https://developers.openai.com/api/docs/guides/tools-file-search | A |
| R5 | OpenAI — Agent builder safety | https://developers.openai.com/api/docs/guides/agent-builder-safety | A |
| R6 | Anthropic — Citations docs | https://platform.claude.com/docs/en/build-with-claude/citations | A |
| R7 | OpenAI — Agent evals guide | https://developers.openai.com/api/docs/guides/agent-evals | A |
| R8 | Google Cloud — Research Assistant docs | https://docs.cloud.google.com/gemini/enterprise/docs/research-assistant | A |
| R9 | Google Cloud — Multi-agent architecture | https://docs.cloud.google.com/architecture/multiagent-ai-system | A |
| R10 | AWS Bedrock — Multi-agent collaboration | https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html | A |
| R11 | Microsoft — AI agent design patterns | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns | A |
| R12 | ReAct (Yao et al., 2022) | https://arxiv.org/abs/2210.03629 | A |
| R13 | Tree of Thoughts (Yao et al., 2023) | https://arxiv.org/abs/2305.10601 | A |
| R14 | Chain-of-Verification (Dhuliawala et al., 2023) | https://arxiv.org/abs/2309.11495 | A |
| R15 | Nygard — Documenting architecture decisions | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions | A |
| R16 | AWS — ADR process | https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html | A |
| R17 | AWS — ADR best practices | https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html | A |
| R18 | Microsoft — ADR guidance | https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record | A |
| R19 | Google Cloud — Architecture decision records | https://cloud.google.com/architecture/architecture-decision-records | A |
| R20 | ADR templates index | https://adr.github.io/adr-templates/ | B |
| R21 | ADR GitHub organization | https://github.com/adr | B |
| R22 | MADR project | https://adr.github.io/madr/ | B |
| R23 | OpenAI tools (last-modified 2026-02-14) | https://developers.openai.com/api/docs/guides/tools | A |
| R24 | OpenAI tools-web-search (last-modified 2026-02-14) | https://developers.openai.com/api/docs/guides/tools-web-search | A |
| R25 | OpenAI tools-file-search (last-modified 2026-02-14) | https://developers.openai.com/api/docs/guides/tools-file-search | A |
| R26 | OpenAI agent-builder-safety (last-modified 2026-02-14) | https://developers.openai.com/api/docs/guides/agent-builder-safety | A |
| R27 | OpenAI agent-evals (last-modified 2026-02-14) | https://developers.openai.com/api/docs/guides/agent-evals | A |
| R28 | Google research assistant docs (last-modified 2026-02-13) | https://docs.cloud.google.com/gemini/enterprise/docs/research-assistant | A |
| — | LangGraph Concepts | https://langchain-ai.github.io/langgraph/concepts/ | B |
| — | Google SRE Book, Chapter 22 | https://sre.google/sre-book/handling-overload/ | A |
| — | AWS Well-Architected Reliability Pillar | https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html | A |
| — | SELF-REFINE (Madaan et al., NeurIPS 2023) | https://arxiv.org/abs/2303.17651 | A |
| — | Anthropic Prompt Engineering | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview | A |

---

*End of compiled ADR registry. Target commit path: `reports/deep-research/ADR_COMPILED_agentic-workflows-v2.md`*

