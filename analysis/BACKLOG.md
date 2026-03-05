# Product Backlog — tafreeman/prompts

**Repository:** `tafreeman/prompts`
**Last Updated:** 2026-03-04
**Health Score:** 7.9 / 10 *(post-remediation, 2026-03-03)*
**Analysis Team:** Architecture Analyst · ML/AI Patterns Reviewer · Code Quality Auditor · Documentation & DX Reviewer

**Source documents:**
| File | Summary |
|------|---------|
| [`analysis/architecture-review.md`](architecture-review.md) | A- — Protocol-first adapter registry, dual engine, DAG superiority over Microsoft candidates; ctx forwarding bug in LangChainEngine, no checkpointing implementation |
| [`analysis/ml-ai-patterns-review.md`](ml-ai-patterns-review.md) | A- — 24 personas fully structured post-remediation; CoT, Boundaries, Output Format, domain-specific Reasoning Protocols; gap is zero-shot only (no few-shot, no reflection loops) |
| [`analysis/code-quality-report.md`](code-quality-report.md) | B+ — Strong agentic_v2 quality; ruff.lint not configured (E+F only), CI coverage gate 60% vs 80% target, tools/ package needs modernization |
| [`analysis/documentation-review.md`](documentation-review.md) | B+ — Excellent CLAUDE.md and README; 11 broken cross-references, no onboarding tutorial, minimal examples |
| [`analysis/ANALYSIS-SUMMARY.md`](ANALYSIS-SUMMARY.md) | Synthesized findings — 25 prioritized recommendations, 4-sprint roadmap, 7.9/10 health score |

---

## Health Score Dashboard

| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| **Modularity & separation** | 9/10 | Zero cross-package imports; clean adapter pattern; excellent RAG module boundaries |
| **Protocol design** | 8/10 | PEP 544 protocols with `@runtime_checkable`; deducted for `Any` in core signatures |
| **Config-driven design** | 9/10 | 81% config for workflows; all 24 personas fully structured (Expertise, Reasoning Protocol, Output Format, Boundaries, Critical Rules); comprehensive YAML DSL |
| **ML/AI pattern sophistication** | 9/10 | ToT, ReAct, CoVe, RRF hybrid retrieval, circuit breakers, CoT scaffolding in all personas, RAG prompt injection framing; deducted for no few-shot/reflection |
| **Code quality discipline** | 7/10 | Strong in agentic_v2 (no bare except, good typing, logging); tools/ package drags the score |
| **Test coverage & strategy** | 7/10 | 1305+ tests, ~92% RAG coverage; CI threshold mismatch and missing markers hurt |
| **Documentation completeness** | 7/10 | Excellent CLAUDE.md and README; broken cross-refs, no onboarding tutorial, minimal examples |
| **Production readiness** | 7/10 | Good observability, auth, security; in-memory stores limit production scalability |
| **Extensibility** | 9/10 | New workflow/persona/loader/adapter via protocol implementation only; entry_points gap |
| **Educational clarity** | 7/10 | Self-documenting architecture; lacks explicit learning path and pattern catalog |

**Overall: 79/100 → 7.9/10**

---

## Key Strengths

| # | Strength | Evidence |
|---|----------|----------|
| 1 | **Protocol-first architecture** | 9 `@runtime_checkable` Protocol classes in `core/protocols.py` + `rag/protocols.py` enable structural subtyping and clean engine swapping |
| 2 | **Production-grade LLM routing** | `SmartModelRouter` implements circuit breakers, adaptive cooldowns, per-provider bulkheads, rate-limit header parsing, and cross-tier degradation |
| 3 | **Comprehensive RAG pipeline** | 13 protocol-backed modules: load → chunk → embed → index → hybrid retrieve (BM25 + dense + RRF) → token-budget assemble → trace |
| 4 | **Advanced deep-research workflow** | `deep_research.yaml` demonstrates ToT, ReAct, CoVe, and confidence-gated iteration in declarative YAML — rare in the field |
| 5 | **Antagonist review personas** | Two orthogonal antagonist personas (FMEA murder-board + systemic pre-mortem) embody adversarial review methodology at the prompt level |

---

## Full Backlog (All 25 Items + 1 New)

| # | ID | Status | Sprint | Recommendation | Impact | Effort | Owner | Source |
|---|----|--------|--------|----------------|:------:|:------:|-------|--------|
| 1 | CQ-1 | **IN PROGRESS** | Sprint A | Add `[tool.ruff.lint]` to `agentic-workflows-v2/pyproject.toml` with full rule set: `E, F, W, I, N, UP, S, B, A, C4, SIM, TCH, RUF` | 5 | S | Code Quality | CQ-1 |
| 2 | CQ-2 | **IN PROGRESS** | Sprint A | Align CI coverage threshold to 70% intermediate (80% final) with documented roadmap | 4 | S | Code Quality | CQ-2 |
| 3 | ML-1 | **IN PROGRESS** | Sprint B | Add few-shot examples to top 5 agent personas (coder, reviewer, orchestrator, researcher, architect) | 5 | M | ML/AI | ML-1 |
| 4 | DX-1 | BACKLOG | Sprint B | Create `docs/ONBOARDING.md` — progressive tutorial: minimum setup → first workflow → first agent → first evaluation | 5 | M | Docs | DX-1 |
| 5 | DX-3 | BACKLOG | Sprint B | Create a Pattern Catalog mapping agentic AI patterns (ReAct, CoVe, ToT, RRF, confidence gating) to their codebase implementations | 5 | M | Docs | DX-3 |
| 6 | ML-2 | BACKLOG | Sprint D | Implement reflection/self-correction loop in `BaseAgent` — add `_self_critique()` + `_revise()` phase after initial response | 5 | L | ML/AI | ML-2 |
| 7 | ARCH-4 | BACKLOG | Sprint C | Add cross-package integration tests — E2E tests exercising tools/ LLM client → agentic_v2 engine → agentic-v2-eval scoring | 4 | M | Architecture | ARCH-4 |
| 8 | ARCH-1 | BACKLOG | Sprint C | Tighten protocol type signatures — replace `Any` in `ExecutionEngine.execute()` and `AgentProtocol.run()` with bounded TypeVars | 4 | M | Architecture | ARCH-1 |
| 9 | ARCH-2 | **IN PROGRESS** | Sprint A | Bridge ExecutionContext to LangChainEngine — forward ctx state to WorkflowRunner so both engines share execution context | 4 | M | Architecture | ARCH-2 |
| 10 | DX-2 | BACKLOG | Sprint A | Fix all 11 broken cross-references — create stubs or remove references for missing files | 4 | S | Docs | DX-2 |
| 11 | DX-4 | BACKLOG | Sprint B | Add 5-8 examples — cover RAG pipeline, custom agent with tools, new YAML workflow creation, model router, adapter switching | 5 | M | Docs | DX-4 |
| 12 | CQ-3 | **IN PROGRESS** | Sprint A | Add `[tool.mypy]` to `agentic-workflows-v2/pyproject.toml` — `disallow_untyped_defs = true` and `warn_return_any = true` | 4 | M | Code Quality | CQ-3 |
| 13 | CQ-7 | BACKLOG | Sprint A | Add CI jobs for eval and tools test suites — neither `agentic-v2-eval/tests/` nor `tools/tests/` runs in CI | 4 | S | Code Quality | CQ-7 |
| 14 | ARCH-6 | **IN PROGRESS** | Sprint C | Add persistent VectorStore adapter — implement `VectorStoreProtocol` for LanceDB (already optional dep) | 4 | M | Architecture | ARCH-6 |
| 15 | ML-5 | BACKLOG | Sprint D | Integrate online evaluation feedback — evaluation scores feed back into agent execution loop for self-correction | 4 | L | ML/AI | ML-5 |
| 16 | CQ-4/5 | BACKLOG | Sprint C | Modernize `tools/` package — `from __future__ import annotations`, replace legacy typing, convert 365 `print()` to logging | 3 | M | Code Quality | CQ-4/5 |
| 17 | ML-3 | **DONE** ✅ | — | ~~Add chain-of-thought scaffolding to agent prompts~~ — `## Reasoning Protocol` added to all 24 personas (2026-03-03) | 4 | S | ML/AI | ML-3 |
| 18 | DX-5 | BACKLOG | Sprint B | Add YAML workflow authoring guide — document expression syntax, `when` conditions, loops, agent naming, evaluation blocks | 4 | M | Docs | DX-5 |
| 19 | ML-4 | BACKLOG | Sprint C | Add re-ranking stage to RAG pipeline — cross-encoder or LLM re-ranker after RRF fusion | 4 | M | ML/AI | ML-4 |
| 20 | ARCH-3 | BACKLOG | Sprint D | Add workflow `iterate:` construct — YAML looping directive to eliminate `deep_research.yaml` 4x duplication | 3 | M | Architecture | ARCH-3 |
| 21 | ML-6 | **DONE** ✅ | — | ~~Enrich lower-tier personas (B-rated)~~ — all 24 now have Boundaries, Output Format, and Reasoning Protocol (2026-03-03) | 4 | M | ML/AI | ML-6 |
| 22 | DX-6 | BACKLOG | Sprint A | Create GitHub issue/PR templates — `.github/PULL_REQUEST_TEMPLATE.md` referenced but missing | 3 | S | Docs | DX-6 |
| 23 | DX-9 | BACKLOG | Sprint A | Add concept glossary — define DAG, ReAct, CoVe, tier, persona, rubric, circuit breaker, expression, adapter | 4 | S | Docs | DX-9 |
| 24 | CQ-6 | BACKLOG | Sprint D | Split oversized files — `model_probe.py` (2,360 lines), `server/routes/workflows.py` (1,330), `evaluation_scoring.py` (1,160) | 3 | L | Code Quality | CQ-6 |
| 25 | DX-13 | BACKLOG | Sprint D | Add annotated code walkthroughs — guided walkthroughs of workflow execution, model routing, RAG retrieval | 4 | L | Docs | DX-13 |
| 26 | ARCH-5 | **IN PROGRESS** | Sprint A | Implement `SupportsCheckpointing` in `NativeEngine` using SQLite — enables workflow resume without restart | 4 | M | Architecture | ARCH-5 (new) |

---

## Microsoft Agent Framework Decision (ADR-012 Summary)

**Decision: DEFERRED** — Not high value relative to existing capabilities as of 2026-03-04.

### Candidates Evaluated

| Candidate | Status | DAG Alignment | Decision |
|-----------|--------|:-------------:|----------|
| Microsoft AutoGen v0.4 | Maintenance mode (Oct 2025) | 60% | **REJECTED** — maintenance mode |
| Semantic Kernel | Maintenance mode (Oct 2025) | 40% | **REJECTED** — maintenance mode + poor alignment |
| Azure AI Agent Service | Active (cloud-only) | N/A | **REJECTED** — not an adapter candidate; cloud service, not a library |
| Microsoft Agent Framework (MAF) | Public preview | 70% | **DEFERRED** — viable when GA, but inferior parallelism vs local DAG |

### Why the Local DAG Wins

The repo's native DAG executor uses Kahn's algorithm with `asyncio.wait(FIRST_COMPLETED)` — steps unblock immediately when their dependencies resolve. MAF uses superstep barriers (all dependencies must finish before any successor starts), which is fundamentally inferior parallelism. Implementing a MAF adapter would add a vendor dependency while delivering worse execution characteristics.

### Trigger Conditions for Revisit

Revisit ADR-012 when **all three** conditions are met:

1. **MAF reaches GA** (currently public preview — API stability not guaranteed)
2. **Engagement-specific Purview requirement** — client requires Microsoft Purview audit trail for agentic workflow provenance
3. **`SupportsCheckpointing` implemented** in `NativeEngine` (ARCH-5, Item #26) — MAF's only genuine capability advantage is eliminated once SQLite checkpointing is in place

**Full research document:** To be created as `analysis/microsoft-agent-framework-research.md`

---

## Completed Items

| ID | Item | Completion Date | Notes |
|----|------|-----------------|-------|
| ML-3 | Chain-of-thought scaffolding added to all 24 agent personas (`## Reasoning Protocol`) | 2026-03-03 | Domain-specific 5-step reasoning workflows replacing generic boilerplate |
| ML-6 | Lower-tier personas enriched — all 24 now have Boundaries, Output Format, Reasoning Protocol | 2026-03-03 | Post-remediation: all personas rated A- or higher (3 A+, 3 A, 17 A-, 1 B+) |

---

## Sprint Roadmap

### Sprint A — Quick Wins (~1-2 days)

Items currently IN PROGRESS or immediately actionable:

| # | ID | Item | Status |
|---|----|------|--------|
| 1 | CQ-1 | Add `[tool.ruff.lint]` to pyproject.toml | **IN PROGRESS** |
| 2 | CQ-2 | Align CI coverage threshold (70% intermediate, 80% target) | **IN PROGRESS** |
| 3 | CQ-3 | Add `[tool.mypy]` to pyproject.toml | **IN PROGRESS** |
| 4 | ARCH-2 | Fix ctx forwarding bug in LangChainEngine | **IN PROGRESS** |
| 5 | ARCH-5 | Implement SupportsCheckpointing in NativeEngine (SQLite) | **IN PROGRESS** |
| 6 | ARCH-6 | Implement LanceDBVectorStore adapter | **IN PROGRESS** |
| 7 | ML-1 | Add few-shot examples to top 5 personas | **IN PROGRESS** |
| 8 | DX-2 | Fix 11 broken cross-references | BACKLOG |
| 9 | CQ-7 | Add CI jobs for eval + tools test suites | BACKLOG |
| 10 | DX-6 | Create GitHub PR/issue templates | BACKLOG |
| 11 | DX-9 | Add concept glossary | BACKLOG |

### Sprint B — Educational Materials (~1-2 weeks)

| # | ID | Item |
|---|----|------|
| 12 | DX-1 | Create `docs/ONBOARDING.md` progressive tutorial |
| 13 | DX-3 | Create Pattern Catalog |
| 14 | DX-4 | Add 5-8 code examples |
| 15 | DX-5 | Add YAML workflow authoring guide |

### Sprint C — Architecture Hardening (~2-3 weeks)

| # | ID | Item |
|---|----|------|
| 16 | ARCH-1 | Tighten protocol type signatures (bounded TypeVars) |
| 17 | ARCH-4 | Add cross-package integration tests |
| 18 | ML-4 | Add re-ranking stage to RAG pipeline |
| 19 | CQ-4/5 | Modernize tools/ package |

### Sprint D — Advanced Patterns (~4+ weeks)

| # | ID | Item |
|---|----|------|
| 20 | ML-2 | Implement BaseAgent reflection/self-correction loop |
| 21 | ML-5 | Integrate online evaluation feedback loop |
| 22 | ARCH-3 | Add workflow `iterate:` construct |
| 23 | CQ-6 | Split oversized files |
| 24 | DX-13 | Add annotated code walkthroughs |

---

## Current Implementation Plan

**Implementation plan file:** `C:\Users\tandf\.claude\plans\fancy-popping-quail.md`

**Phase 1 (parallel):** ARCH-2 ctx fix + CQ-1/3 ruff/mypy config
**Phase 2 (parallel):** ML-1 few-shot examples + ARCH-5 checkpointing + ARCH-6 LanceDB
**Phase 3 (sequential):** Integration verification — full test suite + protocol assertions

**Orchestration:** 5 specialized subagents with defined personas, tool grants, knowledge areas, and prompt templates. Agent F runs final verification across all changes.
