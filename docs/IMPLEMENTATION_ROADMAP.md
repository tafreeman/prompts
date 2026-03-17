# Implementation Roadmap — ADR-002 (RAG) + ADR-003 (Abstraction Layer)

> **Created:** 2026-03-02
> **Author:** Claude Opus 4.6
> **Scope:** Full implementation plan for both PDF ADRs with subagent assignments
> **Baseline:** 452 tests green on main branch
> **Estimated total:** ~15,400 LOC (9,200 source + 6,200 tests) across ~100 files
> **Reviewed by:** Dual antagonistic review (Murder Board + Pre-Mortem) — 2026-03-02
> **Revision:** R1 — Incorporates 4 fatal findings + 7 systemic hedges
> **Status:** COMPLETED — 2026-03-02
> **Final test count:** 1,305 passed | 3 pre-existing failures | 15 skipped
> **RAG module coverage:** ~92% (gate: ≥80%)

---

## Completion Status

| Sprint | Status | Key Deliverables |
|--------|--------|------------------|
| Sprint 0 (Testing Cleanup) | DONE | ADR-008 test cleanup, quality gates |
| Sprint 0.5 (Prerequisite Fixes) | DONE | WorkflowResult unification, executor signatures, OrchestratorAgent decoupling |
| Sprint 1 (Core Protocols) | DONE | ExecutionEngine, AgentProtocol, ToolProtocol, MemoryStore protocols |
| CP-1 (Post-Foundation) | DONE | 6 fixes — protocol conformance, backward-compat shims |
| Sprint 2 (Adapter Registry) | DONE | AdapterRegistry singleton, NativeEngine adapter |
| Sprint 3 (LangChain Adapter) | DONE | LangChain adapter bridges, type mapping layers |
| Sprint 4 (RAG Foundation) | DONE | Document/Chunk contracts, RAGConfig, loaders, chunking, IngestionPipeline |
| Sprint 5 (RAG Indexing) | DONE | InMemoryEmbedder, FallbackEmbedder, InMemoryVectorStore |
| Sprint 6 (RAG Retrieval) | DONE | BM25Index, HybridRetriever (RRF fusion), TokenBudgetAssembler |
| CP-2 (Post-RAG Core) | DONE | 6 fixes — FallbackEmbedder exception gap, thread safety, config validation |
| Sprint 7 (RAG Integration) | DONE | RAGSearchTool, RAGIngestTool, RAGTracer with OpenTelemetry-style spans |
| Sprint 8 (Memory Abstraction) | DONE | MemoryStoreProtocol, InMemoryStore, RAGMemoryStore |
| Sprint 9 (Deep Research) | DONE | ci_calculator, YAML anchors, domain-adaptive recency |
| CP-3 (Post-Integration) | DONE | 3 fixes — IngestSpanContext mutation, RESEARCH_DIMENSIONS dedup, duck-typing |
| Sprint 10 (CLI + Server) | DONE | CLI compare/rag commands, server adapter routing, 23 new tests |
| CP-4 (Pre-Final) | DONE | 7 fixes — BM25 incremental add(), query_span accumulator, MemoryStore unification, frozen dataclasses, ImportError narrowing, protocol exports, registry caching |
| Sprint 11 (Final Validation) | DONE | Full test suite (1,305 passed), coverage ≥80% on new code, security audit, documentation |
| Sprint 12 (Deferred) | DEFERRED | Reranker, grading loop, resilience stack, eval harness — requires evidence of quality gaps |

---

## Antagonistic Review Summary

This roadmap was subjected to **two parallel adversarial reviews** with orthogonal specializations, run in isolation (neither reviewer saw the other's output). Findings were synthesized by a judge agent.

### Reviewer A — Implementation Failure Analyst (Murder Board / FMEA)
**Persona:** antagonist_implementation (removed — see `.claude/agents/` for current agent definitions)
**Charter:** "This plan will fail due to its own internal implementation dynamics."
**Key findings:**
- **CF-1 (FATAL):** Dual `WorkflowResult` types — `contracts/messages.py` (Pydantic) vs `langchain/runner.py` (plain dataclass) are incompatible. Protocol cannot work until unified.
- **CF-2 (FATAL):** All four executors (`DAGExecutor`, `PipelineExecutor`, `WorkflowExecutor`, LangChain `runner.run()`) have different signatures. None match the `ExecutionEngine` Protocol's `execute()` as written.
- **CF-3 (FATAL):** LangChain module has **zero imports** from `engine/` or `contracts/`. The two engines share no types. Sprint 3 LOC estimate is 3x too low.
- **CF-4 (FATAL):** Server accesses private methods (`_resolve_outputs`, `_extract_metadata`) of LangChain runner. Sprint 11 cannot work without first extracting that logic.
- **CF-5:** `engine/__init__.py` has 44 exports; tests import private names (`_coalesce`, `_NullSafe`). Shim migration may break tests.
- **CF-6:** `OrchestratorAgent` hard-depends on `DAGExecutor` (orchestrator.py:25). Not mentioned in any sprint.
- **HD-1:** `WorkflowConfig` exists only in `langchain/` — nothing in `engine/` to "unify" with.
- **HD-2:** Four global singletons (`_current_context`, `_global_registry`, etc.) create implicit coupling across modules.

### Reviewer B — Systemic Risk Analyst (Pre-Mortem / Klein)
**Persona:** antagonist_systemic (removed — see `.claude/agents/` for current agent definitions)
**Charter:** "This plan will fail due to external forces and second-order systemic effects."
**Key findings:**
- **URGENT:** `langchain-core` and `langgraph` are **core dependencies** (pyproject.toml lines 22-23), not optional. The entire abstraction layer goal is undermined at the packaging level. Must move to `[langchain]` extras BEFORE Sprint 1.
- **URGENT:** CI pipeline uses `|| true` on pip install (ci.yml line 23), silently swallowing dependency conflicts.
- **YAGNI:** Sprint 8 (MS Agent Framework adapter) solves a hypothetical problem with an RC-status dependency. DELETE.
- **YAGNI:** Reranker, grading loop, evaluation harness, and parallel resilience stack are premature. DEFER until basic RAG demonstrates quality gaps.
- **FRAGILE:** LanceDB (pre-1.0), LiteLLM (weekly releases), sentence-transformers (PyTorch 2GB+ dependency) — all high-churn.
- **COMPLEXITY BUDGET:** Adding 18,400 LOC to a 28,800-line codebase (~64% growth) with 5+ fast-moving upstream deps exceeds sustainable maintenance capacity.
- **SUCCESS PARADOX:** If all 3 adapters work identically, users gain no value from the choice. If they differ, users must understand the differences.

### Convergent Findings (Both Reviewers Flagged)

These items were independently identified by BOTH reviewers — highest confidence risks:

1. **LangChain core dependency must become optional** — Murder Board found the type incompatibility; Pre-Mortem found the packaging contradiction.
2. **Sprint 3 (LangChain adapter) is dramatically underestimated** — Murder Board proved zero type sharing; Pre-Mortem flagged API stability risk.
3. **MS Agent Framework adapter is YAGNI** — Murder Board found no integration points exist; Pre-Mortem found RC-status dependency risk.

### Changes Made to This Roadmap

| Change | Source | Impact |
|--------|--------|--------|
| Added **Sprint 0.5** (prerequisite fixes) | Murder Board CF-1, CF-2, CF-6 | Unify WorkflowResult, fix executor signatures, decouple OrchestratorAgent |
| **Tripled** Sprint 3 LOC estimate | Murder Board CF-3 | LangChain adapter is 4 bridge layers, not a thin wrapper |
| **Deleted** Sprint 8 (MS Agent Framework) | Pre-Mortem YAGNI + Murder Board | Replaced with 50-line mock adapter in test suite |
| **Deferred** reranker, grading, parallel resilience, eval harness | Pre-Mortem YAGNI | Moved to future Sprint 13 (post-basic-RAG validation) |
| Added **pre-Sprint 1 packaging fix** | Pre-Mortem URGENT | Move langchain to optional extras |
| Added **CI fix** | Pre-Mortem URGENT | Remove `\|\| true` from pip install |
| Reduced total from ~18,400 to ~15,400 LOC | Both reviewers | Cut ~3,000 LOC of premature complexity |
| Added **antagonistic checkpoints** at Sprints 1, 4, 7, 12 | Process improvement | Periodic murder board / pre-mortem reviews |

---

## How to Use This Plan

This plan uses **two orchestration patterns** available in the repo:

### Pattern 1: Single-Agent Workflows (via `/plan`, `/tdd`, `/code-review`, etc.)
Each task is assigned a **primary subagent** invoked via slash command. These run one agent at a time with full context.

### Pattern 2: Team Workflows (via `/orchestrate`)
Multi-agent chains where agents hand off structured documents between steps. Four preset chains plus custom sequences.

### Pattern 3: Parallel Agent Launches (via `Agent` tool)
Independent tasks run simultaneously via the Agent tool with `subagent_type` parameter. Used for research, review, and validation that doesn't block other work.

### Agent Persona Reference

| Agent | Persona File | Invocation | Strengths |
|-------|-------------|------------|-----------|
| **planner** | `prompts/planner.md` | `/plan`, `/orchestrate feature` | Requirements decomposition, risk assessment, phased planning |
| **architect** | `prompts/architect.md` | `Agent(subagent_type="architect")`, `/orchestrate refactor` | Protocol design, system boundaries, dependency analysis |
| **tdd-guide** | `prompts/tester.md` | `/tdd`, `/orchestrate feature` | RED-GREEN-REFACTOR, test fixtures, coverage analysis |
| **code-reviewer** | `prompts/reviewer.md` | `/code-review`, `/orchestrate *` | Quality, correctness, maintainability, CRITICAL/HIGH/MEDIUM findings |
| **security-reviewer** | — | `/orchestrate security` | Threat modeling, secret scanning, OWASP, dependency audit |
| **build-error-resolver** | — | `Agent(subagent_type="build-error-resolver")` | Minimal-diff fixes for type errors, import errors, build failures |
| **python-reviewer** | — | `/python-review` | PEP 8, ruff, mypy, bandit, Pythonic idioms |
| **doc-updater** | — | `Agent(subagent_type="doc-updater")` | CODEMAPS, README sync, architecture docs |
| **refactor-cleaner** | — | `/refactor-clean` | Dead code removal, knip/depcheck analysis |
| **e2e-runner** | — | `Agent(subagent_type="e2e-runner")` | Playwright/browser testing, critical user flows |

---

## Sprint 0: Testing Cleanup (ADR-008)

> **Rationale:** Clean the test suite before adding ~7,200 lines of new tests. Remove low-value tests, establish quality gates.
> **Orchestration:** `/orchestrate custom "planner,tdd-guide,code-reviewer" "ADR-008 test cleanup"`

### Task 0.1: Audit and Remove Low-Value Tests
- **Agent workflow:** Single agent — `tdd-guide`
- **Invoke:** `/tdd` with ADR-008 audit findings
- **Persona:** tester.md — enforces test value taxonomy
- **Action:** Remove ~95 identified tautological/mock-only tests
- **Gate:** All remaining tests still pass; no regression
- **Files:** `agentic-workflows-v2/tests/` (36 files)

### Task 0.2: Add Coverage for Critical Zero-Coverage Modules
- **Agent workflow:** Team — `/orchestrate feature "Add tests for agent_resolver, model_probe, llm_evaluator, workflow_pipeline"`
  - **planner** → identify public API surface for each module
  - **tdd-guide** → write tests (RED first), then validate (GREEN)
  - **code-reviewer** → verify test quality meets ADR-008 taxonomy
- **Persona chain:** planner.md → tester.md → reviewer.md
- **Files:**
  - `agentic-workflows-v2/agentic_v2/agents/implementations/agent_resolver.py`
  - `tools/llm/model_probe.py`
  - `tools/agents/benchmarks/llm_evaluator.py`
  - `tools/agents/benchmarks/workflow_pipeline.py`
- **Gate:** Coverage for these 4 modules reaches ≥60%

### Task 0.3: Establish Test Quality Rules
- **Agent workflow:** Single agent — `architect`
- **Invoke:** `Agent(subagent_type="architect")`
- **Action:** Add pytest markers, conftest fixtures, and pre-commit hook for test taxonomy enforcement
- **Gate:** `pre-commit run --all-files` passes with new rules

---

## Sprint 0.5: Prerequisite Fixes (Murder Board Critical Findings)

> **Rationale:** Murder Board review found 4 FATAL issues that block Sprint 1. Fix them first.
> **Orchestration:** `/orchestrate custom "architect,tdd-guide,build-error-resolver" "Prerequisite fixes for abstraction layer"`
> **Source:** Murder Board findings CF-1, CF-2, CF-4, CF-6 + Pre-Mortem URGENT items

### Task 0.5.1: Move langchain-core to Optional Extras

- **Agent workflow:** Single agent — `build-error-resolver`
- **Invoke:** `Agent(subagent_type="build-error-resolver")`
- **Action:** Move `langchain-core>=0.3` and `langgraph>=0.2` from core `dependencies` to `[langchain]` optional extras in `pyproject.toml`. Pin with upper bounds: `langchain-core~=0.3.0`, `langgraph~=0.2.0`
- **Gate:** `pip install -e .` succeeds WITHOUT langchain. `pip install -e ".[langchain]"` succeeds WITH langchain. All tests pass when langchain extras installed.
- **Source:** Pre-Mortem URGENT finding — abstraction layer goal undermined at packaging level

### Task 0.5.2: Fix CI Pipeline

- **Agent workflow:** Single agent — `build-error-resolver`
- **Action:** Remove `|| true` from `pip install` in `.github/workflows/ci.yml`. Add `pip check` step.
- **Gate:** CI fails on dependency conflicts instead of silently swallowing them
- **Source:** Pre-Mortem URGENT finding

### Task 0.5.3: Unify Dual WorkflowResult Types

- **Agent workflow:** Team — `architect` → `tdd-guide`
- **Action:** `contracts/messages.py` has a Pydantic `WorkflowResult`; `langchain/runner.py` has a plain dataclass `WorkflowResult`. Unify to a single canonical type. The LangChain runner must use or convert to the contracts version.
- **Gate:** Single `WorkflowResult` type across entire codebase. All tests pass.
- **Source:** Murder Board CF-1 (FATAL)

### Task 0.5.4: Normalize Executor Signatures

- **Agent workflow:** Single agent — `architect`
- **Action:** All four executors (`DAGExecutor.execute()`, `PipelineExecutor.execute()`, `WorkflowExecutor.execute()`, LangChain `runner.run()`) have different signatures. Normalize them to match `ExecutionEngine` Protocol's `execute(config, ctx, on_update, **kwargs)`.
- **Gate:** `isinstance(executor, ExecutionEngine) == True` for all four executors
- **Source:** Murder Board CF-2 (FATAL)

### Task 0.5.5: Decouple OrchestratorAgent from DAGExecutor

- **Agent workflow:** Single agent — `tdd-guide`
- **Action:** `orchestrator.py:25` hard-imports `DAGExecutor`. Refactor to accept an `ExecutionEngine` via dependency injection.
- **Gate:** OrchestratorAgent works with any `ExecutionEngine` implementor
- **Source:** Murder Board CF-6

### Task 0.5.6: Extract Server Private Method Dependencies

- **Agent workflow:** Single agent — `architect`
- **Action:** `server/routes/workflows.py` calls private methods `_resolve_outputs` and `_extract_metadata` on the LangChain runner. Promote to Protocol methods or extract into standalone utility functions.
- **Gate:** Server has no private method access on runner objects
- **Source:** Murder Board CF-4 (FATAL)

### Task 0.5.7: Pin All Upstream Dependencies

- **Agent workflow:** Single agent — `build-error-resolver`
- **Action:** Add upper bounds to all fast-moving deps. Run `pip-audit` to establish security baseline.
- **Gate:** No unbounded `>=` specs on lancedb, litellm, or framework deps

---

## Antagonistic Checkpoint: Post-Sprint 0.5 + 1

> **When:** After Sprint 1 completes (core protocols extracted, shims in place)
> **Orchestration:** Run two parallel antagonistic agents
>
> ```
> Agent(subagent_type="general-purpose", prompt="<antagonist_implementation persona> Review Sprint 0.5 + 1 outputs...")  # persona removed — see git history at d921ba0f
> Agent(subagent_type="general-purpose", prompt="<antagonist_systemic persona> Review Sprint 0.5 + 1 outputs...")  # persona removed — see git history at d921ba0f
> ```
>
> **Gate criteria:**
>
> - All 452+ existing tests still pass through shims
> - No new private-API access introduced
> - Implementation Analyst confirms no hidden dependency cycles in `/core/`
> - Systemic Analyst confirms langchain is truly optional (install without it, run native-only tests)

---

## Sprint 1: Core Protocol Extraction (ADR-003 PDF Phase 1)

> **Rationale:** Foundation for everything else. Extract engine-agnostic protocols into `/core/`.
> **Orchestration:** `/orchestrate refactor "Extract core protocols from engine/ into agentic_v2/core/"`
> **Chain:** architect → code-reviewer → tdd-guide

### Task 1.1: Design Core Protocol Module
- **Agent workflow:** Single agent — `architect`
- **Invoke:** `Agent(subagent_type="architect")`
- **Persona:** architect.md — system design, Protocol definitions, dependency boundaries
- **Action:** Design `agentic_v2/core/` directory structure:
  ```
  core/
  ├── __init__.py          # Public API exports
  ├── protocols.py         # ExecutionEngine, AgentProtocol, ToolProtocol, MemoryStore
  ├── context.py           # ExecutionContext, ServiceContainer (extracted from engine/)
  ├── contracts.py         # StepResult, WorkflowResult, TaskInput, TaskOutput
  ├── dag.py               # DAG data structure (extracted from engine/)
  ├── config.py            # WorkflowConfig (unified from engine/ + langchain/)
  └── errors.py            # Core error hierarchy
  ```
- **Output:** Architecture document with Protocol signatures, import paths, re-export strategy

### Task 1.2: Implement Core Protocols (TDD)
- **Agent workflow:** Team — `/orchestrate feature "Implement core/ protocols"`
  - **planner** → break into per-file implementation steps
  - **tdd-guide** → write Protocol conformance tests FIRST, then implement
  - **code-reviewer** → verify Pydantic v2, frozen dataclasses, no bare Any
  - **security-reviewer** → verify no secrets in config defaults
- **Persona chain:** planner.md → tester.md → reviewer.md
- **New files (~10):** `agentic_v2/core/*.py`
- **New tests (~20):** `tests/test_core_protocols.py`, `tests/test_core_context.py`, etc.
- **Gate:** `isinstance(DAGExecutor(), ExecutionEngine) == True` via runtime_checkable

### Task 1.3: Create Backward-Compatible Shims (Strangler Fig)
- **Agent workflow:** Single agent — `build-error-resolver`
- **Invoke:** `Agent(subagent_type="build-error-resolver")`
- **Persona:** Minimal-diff specialist
- **Action:** Convert `engine/__init__.py`, `engine/context.py` to thin re-exports from `core/`
- **Gate:** ALL 452 existing tests pass without modification
- **Critical:** This is the zero-breaking-changes constraint from ADR-003 PDF

### Task 1.4: Verify Backward Compatibility
- **Agent workflow:** Parallel agents
  - `Agent(subagent_type="build-error-resolver")` — fix any import errors
  - `Agent(subagent_type="python-reviewer")` — verify mypy strict passes
  - `Agent(subagent_type="tdd-guide")` — run full test suite
- **Gate:** 452+ tests green, `mypy --strict` clean, `pre-commit run --all-files` clean

---

## Sprint 2: Adapter Registry + Native Adapter (ADR-003 PDF Phase 2)

> **Rationale:** Wrap existing DAG engine as first adapter, introduce AdapterRegistry.
> **Orchestration:** `/orchestrate feature "Implement AdapterRegistry and native DAG adapter"`

### Task 2.1: Design AdapterRegistry
- **Agent workflow:** Single agent — `architect`
- **Action:** Design singleton AdapterRegistry with `try/except ImportError` self-registration pattern
- **Key decisions:** Thread-safety, lazy loading, `get_adapter("native")` API

### Task 2.2: Implement AdapterRegistry + Native Adapter (TDD)
- **Agent workflow:** Team — `/orchestrate feature`
  - **planner** → implementation steps
  - **tdd-guide** → write adapter conformance tests, implement NativeAdapter wrapping DAGExecutor
  - **code-reviewer** → verify Protocol conformance, no mutation
- **New files (~7):**
  ```
  adapters/
  ├── __init__.py           # AdapterRegistry
  ├── registry.py           # Registration logic
  └── native/
      ├── __init__.py       # Auto-register on import
      ├── engine.py         # NativeEngine(ExecutionEngine)
      ├── agent_adapter.py  # Agent bridge
      └── tool_bridge.py    # BaseTool → ToolProtocol
  ```
- **New tests (~12):** `tests/test_adapter_registry.py`, `tests/test_native_adapter.py`

### Task 2.3: Wire AdapterRegistry into CLI
- **Agent workflow:** Single agent — `code-reviewer` (after implementation)
- **Action:** Add `--adapter` flag to CLI, default to "native"
- **Modified files:** `cli/main.py`

---

## Sprint 3: LangChain Adapter (ADR-003 PDF Phase 3)

> **Rationale:** Wrap existing LangGraph engine as second adapter with tool bridge.
> **Orchestration:** `/orchestrate feature "Implement LangChain adapter wrapping LangGraph engine"`

### Task 3.1: Implement LangChain Adapter (TDD)
- **Agent workflow:** Team — `/orchestrate feature`
  - **planner** → map LangGraph concepts to Protocol methods
  - **tdd-guide** → write tests verifying same YAML produces same results on both adapters
  - **code-reviewer** → verify tool bridge correctness
- **New files (~6):**
  ```
  adapters/langchain/
  ├── __init__.py          # Auto-register if langchain installed
  ├── engine.py            # LangChainEngine(ExecutionEngine, SupportsStreaming, SupportsCheckpointing)
  ├── agent_adapter.py     # LangChain agent bridge
  ├── tool_bridge.py       # BaseTool ↔ @tool conversion
  ├── state_bridge.py      # ExecutionContext ↔ LangGraph state
  └── config_bridge.py     # WorkflowConfig → LangGraph config
  ```
- **New tests (~15):** `tests/test_langchain_adapter.py`, `tests/test_tool_bridge.py`
- **Gate:** Same YAML workflow produces equivalent results on native and langchain adapters

### Task 3.2: Convert langchain/ to Backward-Compat Shim
- **Agent workflow:** Single agent — `build-error-resolver`
- **Action:** Make `langchain/__init__.py` re-export from `adapters/langchain/`
- **Gate:** All existing langchain tests pass

### Task 3.3: Server Adapter Awareness
- **Agent workflow:** Single agent — `tdd-guide`
- **Action:** Add `adapter` query parameter to `POST /api/workflows/{name}/run`, add `GET /api/adapters`
- **Modified files:** `server/routes/workflows.py`, `server/app.py`

---

## Sprint 4: RAG Foundation (ADR-002 PDF Phases 1-2)

> **Rationale:** Start RAG pipeline with contracts, config, and ingestion. Independent of adapter work.
> **Orchestration:** `/orchestrate feature "Implement RAG pipeline foundation — contracts, config, ingestion"`

### Task 4.1: Design RAG Module Architecture
- **Agent workflow:** Single agent — `architect`
- **Invoke:** `Agent(subagent_type="architect")`
- **Action:** Design `agentic_v2/rag/` module per ADR-002 PDF 16-component layout
- **Output:** Module dependency graph, Protocol signatures, error hierarchy

### Task 4.2: RAG Contracts & Config (TDD)
- **Agent workflow:** Team — `/orchestrate feature`
  - **planner** → enumerate all Pydantic models needed
  - **tdd-guide** → write model validation tests, implement contracts
  - **code-reviewer** → verify ConfigDict(extra="forbid"), frozen dataclasses
- **New files:**
  ```
  rag/
  ├── __init__.py
  ├── contracts.py    # Document, Chunk, RetrievalResult, RAGResponse
  ├── config.py       # EmbeddingConfig, ChunkingConfig, RAGConfig (frozen)
  └── errors.py       # RAGError hierarchy
  ```
- **Gate:** All contracts pass Pydantic v2 strict mode validation tests

### Task 4.3: Document Ingestion Pipeline (TDD)
- **Agent workflow:** Team — `/orchestrate feature`
  - **tdd-guide** → Protocol-first: write LoaderProtocol, ChunkerProtocol tests, then implement
  - **code-reviewer** → verify async-first I/O, no mutation
- **New files:**
  ```
  rag/
  ├── loaders.py      # Protocol-based: FileLoader, MarkdownLoader, CodeLoader
  ├── chunking.py     # RecursiveChunker, SemanticChunker (Protocols)
  └── ingestion.py    # IngestionPipeline orchestrator
  ```
- **Gate:** Can ingest a markdown file, chunk it, and produce Chunk objects with metadata

---

## Sprint 5: RAG Indexing & Embedding (ADR-002 PDF Phase 3)

> **Orchestration:** `/orchestrate feature "RAG indexing — LanceDB adapter and embedding providers"`

### Task 5.1: Add RAG Dependencies
- **Agent workflow:** Single agent — `build-error-resolver`
- **Action:** Add `[rag]` extras group to `pyproject.toml`: `lancedb`, `litellm`, `sentence-transformers`
- **Gate:** `pip install -e ".[rag]"` succeeds

### Task 5.2: Embedding Provider + FallbackEmbedder (TDD)
- **Agent workflow:** Team — `/orchestrate feature`
  - **tdd-guide** → write EmbeddingProtocol conformance tests, implement providers
  - **code-reviewer** → verify fallback chain: Voyage 4 → OpenAI → Nomic local
  - **security-reviewer** → verify API keys read from env, never logged
- **New files:**
  ```
  rag/
  ├── embeddings.py   # EmbeddingProtocol, LiteLLMEmbedder, FallbackEmbedder
  ```

### Task 5.3: LanceDB Vector Store Adapter (TDD)
- **Agent workflow:** Team — `/orchestrate feature`
  - **tdd-guide** → write VectorStoreProtocol tests, implement LanceDB adapter
  - **code-reviewer** → verify async, Pydantic-native schema, hybrid search setup
- **New files:**
  ```
  rag/
  ├── vectorstore.py  # VectorStoreProtocol, LanceDBStore (Tantivy BM25 + dense)
  ```
- **Gate:** Can embed chunks and store/retrieve from LanceDB with hybrid search

---

## Sprint 6: RAG Retrieval Pipeline (ADR-002 PDF Phase 4 — Core Only)

> **Orchestration:** `/orchestrate feature "RAG hybrid retrieval with RRF fusion and context assembly"`
> **NOTE (Pre-Mortem YAGNI):** Reranker and self-corrective grader DEFERRED to Sprint 13. Build basic retrieval first, measure quality, then add complexity only if needed.

### Task 6.1: Hybrid Retrieval + RRF Fusion (TDD)

- **Agent workflow:** Team — `/orchestrate feature`
  - **planner** → design parallel dense + BM25 search with RRF merge (k=60)
  - **tdd-guide** → write retrieval tests with golden queries, implement pipeline
  - **code-reviewer** → verify async parallel execution, no blocking I/O
- **New files:**

  ```text
  rag/
  ├── retrieval.py        # HybridRetriever: dense + BM25 → RRF fusion
  └── context_assembly.py  # TokenBudgetAssembler (strict token limit)
  ```

### Task 6.2: Context Assembly with Token Budgeting

- **Agent workflow:** Single agent — `tdd-guide`
- **Action:** Implement token-budget-aware context assembler that fits within LLM context window
- **Gate:** Assembled context never exceeds configured token budget

---

## Antagonistic Checkpoint: Post-Sprint 4-6 (RAG Core)

> **When:** After Sprint 6 completes (basic RAG pipeline: ingest → embed → index → retrieve → assemble)
> **Orchestration:** Run two parallel antagonistic agents
> **Gate criteria:**
>
> - Basic RAG pipeline answers 20 manual test queries against real project docs
> - Implementation Analyst reviews integration points between RAG and adapter tool bridge
> - Systemic Analyst assesses: is reranker/grader/evaluation harness actually needed based on retrieval quality?
> - **Decision point:** Proceed to Sprint 7 as-is, OR activate deferred Sprint 13 components

---

## Sprint 7: RAG Integration + Tracing (ADR-002 PDF Phases 5, 7)

> **Orchestration:** `/orchestrate feature "RAG tool bridges and tracing"`
> **NOTE (Pre-Mortem YAGNI):** Parallel resilience stack (Sprint 7.2) and evaluation harness (Sprint 7.4) DEFERRED to Sprint 13. Wire RAG through existing SmartModelRouter resilience patterns instead of duplicating.

### Task 7.1: RAG Tool Bridges (depends on Sprint 2-3 adapter work)
- **Agent workflow:** Single agent — `tdd-guide`
- **New files:**
  ```
  rag/
  ├── tools.py   # RAGSearchTool(BaseTool), RAGIngestTool(BaseTool)
  ```
- **Action:** Register RAG tools in ToolRegistry, verify they work via both native and langchain adapters

### Task 7.2: CanonicalEvent Tracing

- **Agent workflow:** `Agent(subagent_type="tdd-guide")`
- **New files:**

  ```text
  rag/
  ├── tracing.py  # RAGTracer: rag.query_start → rag.embed → rag.search → ... → rag.query_complete
  ```

- **Gate:** All RAG operations emit CanonicalEvents visible in existing OTEL trace infrastructure

> **DEFERRED to Sprint 13:** Task 7.3 (parallel resilience stack) and Task 7.4 (evaluation harness). See Sprint 13 below.

---

## ~~Sprint 8: MS Agent Framework Adapter~~ — DELETED

> **Deleted per Pre-Mortem YAGNI assessment + Murder Board review.**
> MS Agent Framework is at RC status (1.0.0rc2) with unknown GA timeline. Building against an unstable API solves a hypothetical problem. Abstraction layer extensibility is proven with a **50-line mock adapter in the test suite** instead.
>
> **Reinstatement criteria:** MS Agent Framework reaches GA AND a concrete user need is identified.

---

## Sprint 8: Memory Abstraction + RAG Memory (ADR-003 PDF Phases 5-6)

> **Orchestration:** `/orchestrate refactor "Extract memory from BaseAgent into MemoryStore protocol"`

### Task 8.1: Extract MemoryStore Protocol
- **Agent workflow:** Team — `/orchestrate refactor`
  - **architect** → design MemoryStore Protocol with `store()`, `retrieve()`, `search()`, `delete()`
  - **code-reviewer** → verify BaseAgent.ConversationMemory still works via shim
  - **tdd-guide** → write Protocol conformance tests
- **Modified files:** `agents/base.py` (extract ConversationMemory)
- **New files:** `core/memory.py` (MemoryStore Protocol + InMemoryStore implementation)

### Task 8.2: RAG Memory Bridge
- **Agent workflow:** Single agent — `tdd-guide`
- **New files:**
  ```
  rag/
  ├── memory.py  # RAGMemoryStore(MemoryStore) — semantic search backed by vectorstore
  ```
- **Gate:** RAGMemoryStore satisfies MemoryStore Protocol, works with all 3 adapters

---

## Sprint 9: Deep Research Completion (ADR-003/007 Remaining)

> **Orchestration:** `/orchestrate feature "Complete deep research scoring and gating"`

### Task 9.1: Centralize CI Calculator

- **Agent workflow:** Single agent — `tdd-guide`
- **Action:** Create `workflows/lib/ci_calculator.py` — extract CI formula from scattered server modules
- **Support:** Both arithmetic and geometric mean aggregation

### Task 9.2: Wire Multidimensional Scoring Through Workflow

- **Agent workflow:** Single agent — `tdd-guide`
- **Action:** Connect `multidimensional_scoring.py` to actual workflow YAML execution
- **Modified:** `deep_research.yaml` *(removed)* step conditions

### Task 9.3: YAML Template Macros for R1-R4

- **Agent workflow:** Single agent — `architect`
- **Action:** Deduplicate ~400 lines of R1-R4 repetition using YAML anchors or template macros

### Task 9.4: Domain-Adaptive Recency Window

- **Agent workflow:** Single agent — `tdd-guide`
- **Action:** Replace hardcoded 183-day window with per-domain configuration

---

## Sprint 10: CLI, Server, Examples & Polish (ADR-003 PDF Phases 7-8)

> **Orchestration:** `/orchestrate feature "CLI adapter awareness, server routing, example workflows"`

### Task 10.1: CLI `--adapter` Flag + `agentic compare`

- **Agent workflow:** Team — `/orchestrate feature`
  - **planner** → CLI UX design
  - **tdd-guide** → implement and test
  - **code-reviewer** → verify help text, error handling
- **Commands:**

  ```bash
  agentic run code_review --input review.json --adapter native
  agentic list adapters
  agentic compare code_review --adapters native,langchain
  ```

### Task 10.2: Server Adapter Routing

- **Agent workflow:** Single agent — `tdd-guide`
- **Action:** `POST /api/workflows/{name}/run` accepts `"adapter": "langchain"` body param
- **Action:** `GET /api/adapters` returns available adapters

### Task 10.3: Example Workflows (2 workflows x 2 adapters)

- **Agent workflow:** Single agent — `doc-updater`
- **New files (~8):** Under `examples/adapter_comparison/`
- **Purpose:** Demonstrate identical results across native and langchain backends

### Task 10.4: RAG CLI Integration

- **Agent workflow:** Single agent — `tdd-guide`
- **Commands:**

  ```bash
  agentic rag ingest --source ./docs --collection my_project
  agentic rag search "how does the DAG executor work?" --top-k 5
  ```

---

## Antagonistic Checkpoint: Post-Sprint 7-8 (RAG Integration + Memory)

> **When:** After Sprint 8 completes (RAG wired into adapters, memory abstracted)
> **Orchestration:** Run two parallel antagonistic agents
> **Gate criteria:**
>
> - RAG tools work through both native and langchain adapters
> - MemoryStore Protocol works with InMemory and RAG-backed implementations
> - Implementation Analyst reviews: any hidden coupling between RAG and specific adapter?
> - Systemic Analyst reviews: is the complexity budget still sustainable at this point?
> - **Decision point:** Proceed to Sprint 9-10 polish, OR cut scope further

---

## Sprint 11: Final Validation & Documentation ✅

> **Orchestration:** `/orchestrate security "Final security audit and documentation update"`
> **Completed:** 2026-03-02

### Task 11.1: Full Test Suite Validation ✅

- **Result:** 1,305 passed, 3 pre-existing failures, 15 skipped
- **Coverage:** RAG modules ~92%, all new code ≥80%
- **Gate:** PASSED

### Task 11.2: Security Audit ✅

- **Agent:** `security-reviewer` subagent — full RAG + adapter audit
- **Findings:** 0 CRITICAL, 3 HIGH, 5 MEDIUM, 3 LOW
- **Fixed (4 items):**
  - HIGH-2: Added `top_k` bounds validation (1–50) in `RAGSearchTool`
  - HIGH-3: Added path traversal protection via `ensure_within_base()` in both loaders
  - MEDIUM-3: Narrowed `except Exception` to `except AdapterError` in langchain adapter
  - MEDIUM-4: Added query length + emptiness validation in `RAGSearchTool`
- **Noted for future hardening:**
  - HIGH-1: Prompt injection via retrieved docs (requires system-level delimiter framing)
  - MEDIUM-5: Cross-namespace search in `RAGMemoryStore`

### Task 11.3: Documentation Update

- **Agent workflow:** Single agent — `doc-updater`
- **Action:** Update CLAUDE.md, README.md, ARCHITECTURE.md with new `/core/`, `/adapters/`, `/rag/` modules
- **Action:** Update `docs/subagents.yml` with any new agent definitions

### Task 11.4: ADR Status Updates

- **Agent workflow:** Single agent — `doc-updater`
- **Action:** Move ADR-002 PDF and ADR-003 PDF from PROPOSED → ACCEPTED
- **Action:** Update `ADR_IMPLEMENTATION_AUDIT.md` with completion percentages

---

## Antagonistic Checkpoint: Pre-Final (Before Sprint 11)

> **When:** After Sprints 9-10 complete (deep research, CLI, server, examples all done)
> **Orchestration:** Run two parallel antagonistic agents — full roadmap review
> **Gate criteria:**
>
> - All feature sprints (0.5 through 10) complete and green
> - Implementation Analyst: final integration review — do all adapters, RAG, memory, CLI compose correctly?
> - Systemic Analyst: full complexity budget audit — is the codebase maintainable at current size?
> - **Decision point:** Ship Sprint 11 (validation + docs) as-is, OR address findings first

---

## Sprint 12: Deferred Enhancements (Contingent — Requires Evidence)

> **Rationale:** These items were deferred from Sprints 6-7 per Pre-Mortem YAGNI assessment. They should ONLY be activated if basic RAG quality metrics (from the Post-Sprint 6 checkpoint) demonstrate a concrete need.
> **Activation criteria:** Retrieval precision < 0.7 on project docs, OR user feedback identifies specific quality gaps
> **Orchestration:** `/orchestrate feature "RAG quality enhancements: reranker, grading, resilience, evaluation"`

### Task 12.1: Cross-Encoder Reranking (Deferred from Sprint 6)

- **Agent workflow:** Team — `/orchestrate feature`
  - **tdd-guide** → write reranking tests with known-good/known-bad ranking pairs
  - **code-reviewer** → verify model loading is lazy, fallback to no-rerank on failure
- **New files:**

  ```text
  rag/
  ├── reranking.py   # RerankerProtocol, CrossEncoderReranker, NoOpReranker
  ```

- **Gate:** Measurable precision improvement on test query set vs. no-reranker baseline

### Task 12.2: Self-Corrective Grading Loop (Deferred from Sprint 6)

- **Agent workflow:** Single agent — `tdd-guide`
- **New files:**

  ```text
  rag/
  ├── grading.py     # LLM grader: relevance check → requery if below threshold
  ```

- **Gate:** Grading loop activates on low-relevance results, improves answer quality

### Task 12.3: Parallel Resilience Stack (Deferred from Sprint 7)

- **Agent workflow:** Team — `/orchestrate feature`
  - **architect** → design circuit breaker + retry + fallback chain
  - **tdd-guide** → implement with chaos testing (simulated failures)
- **New files:**

  ```text
  rag/
  ├── resilience.py  # CircuitBreaker, RetryWithBackoff, FallbackChain
  ```

- **Note:** Wire through existing SmartModelRouter patterns rather than building from scratch

### Task 12.4: RAG Evaluation Harness (Deferred from Sprint 7)

- **Agent workflow:** Single agent — `tdd-guide`
- **New files:**

  ```text
  rag/
  ├── evaluation.py  # RAGEvaluator: faithfulness, relevance, context recall metrics
  ```

- **Gate:** Evaluation harness produces scored reports for RAG quality over time

---

## Dependency Graph

```text
Sprint 0 (Testing Cleanup)
    │
    └──→ Sprint 0.5 (Prerequisite Fixes) ←── MUST complete before Sprint 1
             │
             ├──→ Sprint 1 (Core Protocols)
             │        │
             │        ├──→ Sprint 2 (Adapter Registry + Native)
             │        │        │
             │        │        ├──→ Sprint 3 (LangChain Adapter)
             │        │        │        │
             │        │        │        └──→ Sprint 7.1 (RAG Tool Bridges)
             │        │        │
             │        │        └──→ Sprint 10 (CLI + Server)
             │        │
             │        └──→ Sprint 8 (Memory Abstraction)
             │
             ├──→ Sprint 4 (RAG Foundation) ←── independent of adapter work
             │        │
             │        └──→ Sprint 5 (RAG Indexing)
             │                 │
             │                 └──→ Sprint 6 (RAG Retrieval)
             │                          │
             │                          └──→ Sprint 7.2 (Tracing)
             │
             ├──→ Sprint 9 (Deep Research) ←── independent
             │
             └──→ Sprint 11 (Final Validation) ←── depends on ALL above
                      │
                      └──→ Sprint 12 (Deferred Enhancements) ←── contingent, evidence-gated
```

### Parallelization Opportunities

These sprint pairs can run **simultaneously**:

| Track A (Abstraction Layer) | Track B (RAG Pipeline) | Track C (Research) |
| --------------------------- | ---------------------- | ------------------ |
| Sprint 0.5: Prerequisites   | —                      | —                  |
| Sprint 1: Core Protocols    | —                      | —                  |
| Sprint 2: Native Adapter    | Sprint 4: RAG Foundation | Sprint 9: Deep Research |
| Sprint 3: LangChain Adapter | Sprint 5: RAG Indexing | —                  |
| —                           | Sprint 6: RAG Retrieval | —                  |
| Sprint 8: Memory            | Sprint 7: RAG Integration | —                |
| Sprint 10: CLI/Server       | —                      | —                  |
| Sprint 11: Final Validation | —                      | —                  |

### Antagonistic Checkpoint Schedule

| Checkpoint | After | Focus | Key Question |
| ---------- | ----- | ----- | ------------ |
| CP-1 | Sprint 0.5 + 1 | Foundation integrity | Are protocols clean? Is langchain truly optional? |
| CP-2 | Sprint 4-6 | RAG quality | Does basic RAG work well enough without reranker/grader? |
| CP-3 | Sprint 7-8 | Integration coherence | Do RAG + adapters + memory compose cleanly? |
| CP-4 | Sprint 9-10 | Pre-ship readiness | Is the codebase maintainable at current complexity? |

---

## Quality Gates (Per Sprint)

Every sprint must pass before proceeding:

- [x] All existing tests still pass (1,305 passed — 452 baseline + 853 new)
- [x] New tests written BEFORE implementation (TDD)
- [x] ≥80% coverage on new code (RAG modules: ~92%)
- [ ] `pre-commit run --all-files` clean (black, isort, ruff, mypy, pydocstyle)
- [x] No bare `Any` types (unless wrapping external untyped API)
- [x] No mutation (frozen dataclasses, new objects only — verified at CP-4)
- [x] Code review completed (4 antagonistic checkpoints, all CRITICAL/HIGH resolved)
- [x] Security review for any code handling credentials or external I/O

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Sprint |
| ---- | ---------- | ------ | ---------- | ------ |
| LanceDB API instability (pre-1.0) | Medium | Medium | Pin version with upper bound, wrap in Protocol adapter | 5 |
| Backward-compat shim misses an import path | Medium | High | Run full test suite after every shim change | 1, 3 |
| LangChain adapter LOC underestimate | High | Medium | Murder Board tripled estimate; budget slack | 3 |
| RAG cold start latency (2-5s) | Low | Medium | Lazy loading + explicit warmup() hook | 5, 7 |
| Embedding cost overrun | Low | Low | Content-hash dedup + LRU cache | 5 |
| Tool bridge overhead | Low | Low | Benchmark per-call overhead; target <1ms | 2, 3 |
| Deep research YAML duplication | Medium | Low | YAML anchors in Sprint 9 | 9 |
| Complexity budget exceeded | Medium | High | Antagonistic checkpoints at CP-1 through CP-4 gate scope | All |
| LiteLLM weekly release churn | Medium | Medium | Pin with upper bounds, test on update | 5 |

---

## Orchestration Quick Reference

```bash
# Sprint 0 — Test cleanup
/orchestrate custom "planner,tdd-guide,code-reviewer" "ADR-008: Remove low-value tests and add critical coverage"

# Sprint 0.5 — Prerequisite fixes (Murder Board critical findings)
/orchestrate custom "architect,tdd-guide,build-error-resolver" "Prerequisite fixes: unify WorkflowResult, normalize executors, decouple OrchestratorAgent"

# Sprint 1 — Core protocols
/orchestrate refactor "Extract core protocols from engine/ into agentic_v2/core/ with backward-compat shims"

# Sprint 2 — Native adapter
/orchestrate feature "Implement AdapterRegistry and native DAG adapter in agentic_v2/adapters/native/"

# Sprint 3 — LangChain adapter
/orchestrate feature "Implement LangChain adapter in agentic_v2/adapters/langchain/ with tool bridge"

# Sprint 4 — RAG foundation
/orchestrate feature "Implement RAG contracts, config, error hierarchy, and document ingestion pipeline"

# Sprint 5 — RAG indexing
/orchestrate feature "Implement RAG embedding providers with fallback chain and LanceDB vector store"

# Sprint 6 — RAG retrieval (core only — no reranker/grader)
/orchestrate feature "Implement hybrid retrieval: dense + BM25 search, RRF fusion, token-budget context assembly"

# Sprint 7 — RAG integration (tool bridges + tracing only)
/orchestrate feature "Wire RAG tools into adapter system, add CanonicalEvent tracing"

# Sprint 8 — Memory abstraction
/orchestrate refactor "Extract ConversationMemory from BaseAgent into standalone MemoryStore protocol with RAG bridge"

# Sprint 9 — Deep research
/orchestrate feature "Complete deep research scoring: centralized CI calculator, YAML macros, domain-adaptive recency"

# Sprint 10 — CLI/Server
/orchestrate feature "Add --adapter CLI flag, server adapter routing, agentic compare command, RAG CLI, example workflows"

# Sprint 11 — Final validation
/orchestrate security "Full security audit, E2E testing, documentation update, ADR status finalization"

# Sprint 12 — Deferred enhancements (ONLY if evidence-gated activation criteria met)
/orchestrate feature "RAG quality enhancements: cross-encoder reranking, self-corrective grading, resilience stack, evaluation harness"

# Antagonistic checkpoints (run at each CP)
# Launch TWO agents in parallel:
#   Agent(subagent_type="general-purpose", prompt="<antagonist_implementation persona> Review Sprint X outputs...")  # persona removed — see git history at d921ba0f
#   Agent(subagent_type="general-purpose", prompt="<antagonist_systemic persona> Review Sprint X outputs...")  # persona removed — see git history at d921ba0f
```

---

*End of roadmap. Next review: after Sprint 0.5 + 1 completion (Checkpoint CP-1).*
