# ADR Implementation Audit — agentic-workflows-v2

> **Audit date:** 2026-02-28
> **Auditor:** Claude Opus 4.6
> **Scope:** 7 ADR documents + RAG Blueprint vs. codebase implementation
> **Last validated against:** commit 94818282 (main)

---

## Executive Summary

Analyzed **7 ADR documents** (ADR-001 through ADR-003, ADR-007, ADR-0001 through ADR-0003, plus the RAG Pipeline Blueprint) against actual codebase implementation. Package-level decisions (0001-0003) are fully implemented. Core system-level ADRs (001-003, 007) are largely unimplemented, with ADR-003/007 being the notable partial exception.

---

## Scorecard

| ADR | Title | Status | Implementation % |
|-----|-------|--------|-----------------|
| **ADR-0001** | Package Structure (co-location) | FULLY IMPLEMENTED | ~100% |
| **ADR-0002** | Evaluation as Separate Package | FULLY IMPLEMENTED | ~100% |
| **ADR-0003** | Server as Optional Install | FULLY IMPLEMENTED | ~100% |
| **ADR-001** | Dual Execution Engine Protocol | PARTIALLY IMPLEMENTED | ~40% |
| **ADR-002** | SmartModelRouter Circuit-Breaker Hardening | FULLY IMPLEMENTED | ~100% |
| **ADR-003** | Deep Research Supervisor / CI Gating | PARTIALLY IMPLEMENTED | ~55% |
| **ADR-007** | Classification Matrix Stop Policy | PARTIALLY IMPLEMENTED | ~50% |
| **Blueprint** | RAG Pipeline | NOT IMPLEMENTED | ~0% |

---

## 1. ADR-0001, 0002, 0003 — Package Structure Decisions

### Verdict: ALL PASS

| ADR | Decision | Evidence |
|-----|----------|----------|
| **0001** | Agents + Workflows co-located in `agentic_v2/` | Both at `agentic_v2/agents/` and `agentic_v2/workflows/`. Zero circular imports. Clean shared-infra dependency through `engine/` and `contracts/` |
| **0002** | Eval as separate package | `agentic-v2-eval/` is fully independent. Protocol-based interface in `interfaces.py`. Zero dependency on core runtime |
| **0003** | Server as optional extra | `pip install .[server]` pattern in `pyproject.toml` (lines 35-39). Core has zero FastAPI imports. CLI fails gracefully with helpful error when server extras missing |

**Dependency graph:**
```
agentic-v2-eval (independent)
       ↑ (optional protocol import)
agentic-workflows-v2 (core: agents, workflows, engine, contracts)
       ↑ (optional [server] extra)
agentic_v2.server (FastAPI layer)
```

---

## 2. ADR-001 — Dual Execution Engine Protocol

### Verdict: PARTIALLY IMPLEMENTED (~40%, updated 2026-02-28)

ADR decided on **Option D: Common `ExecutionEngine` interface** as transitional architecture converging toward LangGraph.

| Recommended Component | Status | Finding |
|-----------------------|--------|---------|
| `engine/protocol.py` with `ExecutionEngine(Protocol)` | DONE | PEP 544 structural subtyping with `runtime_checkable` |
| `SupportsStreaming` capability protocol | DONE | Optional protocol for engines with `stream()` method |
| `SupportsCheckpointing` capability protocol | DONE | Optional protocol for engines with checkpoint/resume |
| `DAGExecutor` conforms to protocol | DONE | Verified at runtime: `isinstance(DAGExecutor(), ExecutionEngine) == True` |
| `PipelineExecutor` conforms to protocol | DONE | Verified at runtime: `isinstance(PipelineExecutor(), ExecutionEngine) == True` |
| `LangGraphEngine` wrapper | NOT DONE | Logic embedded directly in `langchain/runner.py` |
| `engine_selector.py` (capability-based routing) | NOT DONE | No routing layer |
| `orchestrator.py` dispatches via protocol | NOT DONE | Still uses `isinstance()` type-checks |
| Shadow execution / conformance tests | NOT DONE | Tests exist independently; no comparative tests |
| Server-level dual-engine support | NOT DONE | Hard-coded `lc_runner = LangChainRunner(...)` in `server/routes/workflows.py:46` |

### Remaining Gaps

1. **LangGraphEngine wrapper** — need thin adapter around `langchain/runner.py` that satisfies `ExecutionEngine` + `SupportsStreaming` + `SupportsCheckpointing`.
2. **Orchestrator migration** — replace `isinstance()` dispatch with protocol-based routing.
3. **Shadow execution** — comparative tests running both engines on same input.

---

## 3. ADR-002 — SmartModelRouter Circuit-Breaker Hardening

### Verdict: 5/5 HARDENING MEASURES IMPLEMENTED (updated 2026-02-28)

**Foundational infrastructure works:** Circuit breaker state machine (CLOSED/OPEN/HALF_OPEN), atomic JSON persistence, per-model stats tracking.

| Priority | Measure | Status | Risk | Key Location |
|----------|---------|--------|------|-------------|
| **C** | `time.monotonic()` for cooldowns | DONE | ~~CRITICAL~~ Resolved | `model_stats.py` — `_cooldown_until_mono`, `_last_failure_mono` fields |
| **E** | Rate-limit header parsing (Retry-After) | DONE | ~~HIGHEST~~ Resolved | `rate_limit_tracker.py` — provider-aware dual token buckets |
| **D** | Half-open probe serialization | DONE | ~~MEDIUM~~ Resolved | `smart_router.py` — `_probe_locks` per provider |
| **A** | Bulkhead semaphores (cascade prevention) | DONE | ~~HIGH~~ Resolved | `smart_router.py` — `_provider_semaphores` per provider |
| **B** | Cross-tier degradation | DONE | ~~MEDIUM~~ Resolved | `smart_router.py` — `_cross_tier_search()` degrades down then up |

### Implementation Details (Sprint — 2026-02-28)

**ADR-002C (Monotonic clock):** All cooldown and circuit-breaker timing now uses `time.monotonic()`. Wall-clock `datetime` fields retained for serialization/logging only. `from_dict()` recomputes monotonic deadlines from persisted wall-clock deltas.

**ADR-002E (Rate-limit headers):** New `rate_limit_tracker.py` module with:

- `TokenBucket` — capacity + refill_rate, monotonic timing
- `ProviderRateLimits` — dual RPM + TPM buckets per provider
- `RateLimitTracker` — parses OpenAI/Anthropic/Azure `Retry-After` and `x-ratelimit-*` headers
- Provider-specific header formats: OpenAI reset durations ("6s", "1m30s"), Anthropic remaining counts

**ADR-002D (Probe locks):** `asyncio.Lock` per provider prevents thundering herd during HALF_OPEN recovery probes.

**ADR-002A (Bulkheads):** `asyncio.Semaphore` per provider (OpenAI:50, Ollama:10, etc.) caps concurrent requests. `call_with_fallback()` checks semaphore capacity before attempting a model.

**Test coverage:** 67 new tests in `test_rate_limit_tracker.py` covering token buckets, header parsing, duration parsing, bulkheads, probe locks, error classification, and monotonic clock integration.

---

## 4. ADR-003 + ADR-007 — Deep Research Supervisor & Classification Matrix

### Verdict: PARTIALLY IMPLEMENTED (~50-55%)

**Implemented:**

| Component | Location |
|-----------|----------|
| `deep_research.yaml` with R1-R4 bounded rounds | `workflows/definitions/deep_research.yaml` (588 lines) |
| DORA-style multidimensional classification matrix | `server/multidimensional_scoring.py` (528 lines) |
| Non-compensatory conjunction gate | All 5 dims >= High required |
| `coalesce()` for best-of-N selection | `engine/expressions.py:74-79` |
| Tiered graceful degradation | Full/moderate/low/insufficient tiers |
| Per-dimension score outputs | Each round returns 5 scores + gate_passed |
| Feature flag (legacy vs multidimensional) | `scoring_engine: legacy | multidimensional` |

**NOT Implemented:**

| Component | Impact |
|-----------|--------|
| `ci_calculator.py` centralized module | Logic split across server modules |
| Consecutive regression tracking across rounds | Field exists; not wired in workflow |
| YAML template macros for R1-R4 dedup | ~400 lines of duplication |
| Domain-adaptive recency window | Hardcoded 183 days (from tax law, not IR) |
| Geometric mean CI alternative | Only arithmetic mean |
| Weight sensitivity analysis | Weights uncalibrated |
| Targeted remediation rounds | Full re-execution only |

### Architecture Tension: ADR-003 vs ADR-007

- ADR-003: Two-tier gating (floors + composite CI >= 0.80)
- ADR-007: Abandons CI as primary gate; DORA-style conjunction only; CI demoted to tiebreaker
- Implementation follows ADR-007 (correct), but ADR-003 never formally superseded

---

## 5. RAG Pipeline Blueprint

### Verdict: NOT IMPLEMENTED (0%)

The blueprint document is a detailed specification. **None of it exists in code:**

- No `rag/` module, no vector store adapters, no embedding providers
- No hybrid search, no reranking, no document ingestion
- No RAG evaluation metrics
- No dependencies installed (`pyproject.toml` has zero RAG packages)

**Ready infrastructure:** OTEL tracing, tool system, Pydantic v2 patterns, LLM client abstraction.

---

## 6. ADR Governance

### Issues

1. **ADR numbering inconsistent:** `0001-0003` vs `001-003` vs `007` vs planned `0004-0023`
2. **Duplicate content:** `ADR-001-002-003-architecture-decisions.md` and `ADR_COMPILED.md` overlap
3. **No supersession chain:** ADR-007 evolves ADR-003 but no formal `Superseded-By` link
4. **ADRs 0004-0023 all still Proposed:** No governance process authored

---

## 7. Risk Heatmap

```
                    LIKELIHOOD
                Low    Medium    High
           ┌─────────┬─────────┬─────────┐
  Critical │ Clock   │ Cascade │         │
           │ skew    │ failure │         │
  SEVERITY ├─────────┼─────────┼─────────┤
  High     │ Engine  │ Half-   │ Rate    │
           │ diverg. │ open    │ limit   │
           ├─────────┤ race    │ waste   │
  Medium   │ Compen- │         │ 183-day │
           │ sability│         │ window  │
           └─────────┴─────────┴─────────┘
```

---

## 8. Prioritized Roadmap

### Phase 1: Quick Wins (1-2 days each)

| # | Action | ADR | Effort |
|---|--------|-----|--------|
| 1 | ~~Replace `datetime.now()` with `time.monotonic()` in cooldown tracking~~ | ADR-002C | DONE |
| 2 | ~~Create `engine/protocol.py` with `ExecutionEngine(Protocol)`~~ | ADR-001 | DONE |
| 3 | ~~Add `Superseded-By: ADR-007` to ADR-003~~ | Governance | DONE |

### Phase 2: High-Impact Hardening (3-5 days each)

| # | Action | ADR | Effort |
|---|--------|-----|--------|
| 4 | ~~Implement `rate_limit_tracker.py` with `Retry-After` parsing~~ | ADR-002E | DONE |
| 5 | ~~Add bulkhead semaphores per provider~~ | ADR-002A | DONE |
| 6 | ~~Add `asyncio.Lock` for half-open probe serialization~~ | ADR-002D | DONE |
| 7 | Wire multidimensional scoring through workflow YAML | ADR-007 | 1-2 days |

### Phase 3: Architecture Completion (1-2 weeks)

| # | Action | ADR | Effort |
|---|--------|-----|--------|
| 8 | Wrap LangGraph runner as `LangGraphEngine` adapter | ADR-001 | 2-3 days |
| 9 | Replace `isinstance()` dispatch in orchestrator with protocol | ADR-001 | 1-2 days |
| 10 | Implement domain-adaptive recency windows | ADR-007 | 2-3 days |
| 11 | Add YAML template macros for R1-R4 deduplication | ADR-003 | 1-2 days |
| 12 | ~~Implement cross-tier degradation in SmartModelRouter~~ | ADR-002B | DONE |

### Phase 4: New Capabilities (Multi-week)

| # | Action | ADR | Effort |
|---|--------|-----|--------|
| 12 | Implement RAG pipeline module | Blueprint | 2-4 weeks |
| 13 | Author ADRs 0004-0023 | Governance | Ongoing |
| 14 | Shadow execution CI for dual-engine conformance | ADR-001 | 1 week |

---

*End of audit. Next review recommended: 2026-03-28*
