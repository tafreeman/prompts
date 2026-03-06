# Architecture Review

**Repository:** `tafreeman/prompts`
**Date:** 2026-03-03
**Reviewer:** Architecture Analyst (automated)

---

## Executive Summary

The `tafreeman/prompts` monorepo is a well-structured, enterprise-grade agentic AI platform comprising three independent Python packages and a React 19 dashboard. The architecture follows a protocol-first design using PEP 544 structural subtyping, enabling clean framework abstraction through a dual-engine execution layer (native DAG via Kahn's algorithm and LangChain/LangGraph state machines). The RAG pipeline is thoroughly modular with proper separation across loading, chunking, embedding, indexing, retrieval, and context assembly. Cross-package coupling is minimal and intentional. The config-driven workflow system (10 YAML definitions) demonstrates high declarative-to-imperative ratio. Primary areas for improvement are: tightening the `Any`-heavy protocol signatures, reducing code duplication in the deep research workflow YAML (4 near-identical rounds), and establishing formal cross-package integration testing.

---

## Repository Structure Overview

### Package Dependency Graph

```
                     +------------------------+
                     |     pyproject.toml      |
                     |   (prompts-tools)       |
                     |   Python >= 3.10        |
                     |   setuptools            |
                     +------------------------+
                              |
                              | (shared utilities,
                              |  LLM client, benchmarks)
                              v
         +--------------------------------------------+
         |        agentic-workflows-v2/                |
         |        pyproject.toml                       |
         |        Python >= 3.11, hatchling            |
         |                                             |
         |  +----------+  +----------+  +-----------+  |
         |  |  core/   |  | engine/  |  | langchain/|  |
         |  | protocols|->| dag_exec |  |  runner   |  |
         |  | errors   |  | pipeline |  |  graph    |  |
         |  | memory   |  | context  |  |  state    |  |
         |  | context  |  | step     |  |  agents   |  |
         |  +----------+  +----------+  +-----------+  |
         |       |              |              |        |
         |       v              v              v        |
         |  +----------+  +-----------+                |
         |  | adapters/|  | contracts/|                |
         |  | registry |  | (Pydantic)|                |
         |  | native   |  +-----------+                |
         |  | langchain|       |                       |
         |  +----------+       v                       |
         |       |        +-----------+  +---------+   |
         |       +------->| agents/   |  |  rag/   |   |
         |                | base      |  | pipeline|   |
         |                | coder     |  | memory  |   |
         |                | reviewer  |  | tools   |   |
         |                | orchestr. |  | tracing |   |
         |                +-----------+  +---------+   |
         |                     |              |        |
         |                     v              v        |
         |  +----------+  +-----------+  +---------+   |
         |  | models/  |  | tools/    |  | server/ |   |
         |  | router   |  | registry  |  | FastAPI |   |
         |  | client   |  | builtin/  |  | routes  |   |
         |  | backends |  |  (12 mods)|  | ws/sse  |   |
         |  +----------+  +-----------+  +---------+   |
         |                                     |       |
         +--------------------------------------------+
                                               |
                                               v
                                    +-------------------+
                                    |  ui/ (React 19)   |
                                    |  Vite 6, TS 5.7   |
                                    |  React Flow 12    |
                                    |  TanStack Query 5 |
                                    |  Tailwind CSS 3   |
                                    +-------------------+

         +--------------------------------------------+
         |        agentic-v2-eval/                     |
         |        pyproject.toml                       |
         |        Python >= 3.10, setuptools           |
         |                                             |
         |  evaluators/ | metrics/ | rubrics/ (YAML)   |
         |  runners/    | reporters/ | sandbox/        |
         +--------------------------------------------+
```

### Cross-Package Import Analysis

| From | To | Nature | Coupling |
|------|----|--------|----------|
| `agentic-workflows-v2` | `tools/` | **None at runtime** | Fully independent |
| `agentic-v2-eval` | `tools/` | **None at runtime** | Fully independent |
| `agentic-v2-eval` | `agentic-workflows-v2` | **None at runtime** | Fully independent |
| `ui/` (React) | `server/` (FastAPI) | HTTP/WebSocket API | Loose (REST contract) |
| `server/` | `langchain/`, `engine/`, `contracts/` | Python imports | Internal package |

**Finding:** All three Python packages are fully independent at the import level. No cross-package `import` statements exist. The only coupling between packages is implicit: they share YAML workflow definitions and evaluation rubric schemas. This is excellent monorepo hygiene.

---

## Modularity Assessment

### Boundary Ratings

| Boundary | Rating | Rationale |
|----------|--------|-----------|
| **Package isolation** (3 packages) | **Excellent** | Zero cross-package imports; each has independent pyproject.toml, venv, test suite |
| **Core protocols layer** | **Good** | Clean PEP 544 protocol hierarchy; `@runtime_checkable` enables duck typing; minor concern: heavy use of `Any` types |
| **Engine/Executor layer** | **Excellent** | DAGExecutor cleanly separated from Pipeline; StepExecutor delegates individual step logic; StepStateManager isolates lifecycle tracking |
| **Adapter pattern** | **Good** | AdapterRegistry singleton is thread-safe with lazy instantiation; LangChain adapter gracefully degrades when deps missing; context forwarding gap in LangChainEngine |
| **RAG pipeline** | **Excellent** | 13 modules with clear single-responsibility: contracts, config, protocols, loaders, chunking, ingestion, embeddings, vectorstore, retrieval, context_assembly, memory, tools, tracing |
| **Agent system** | **Good** | BaseAgent generic over TInput/TOutput; capability mixins enable composition; `agent_to_step` bridges to DAG engine; some methods exceed 50-line guideline |
| **Server layer** | **Good** | FastAPI with route modules, auth middleware, WebSocket streaming; SPA serving with path traversal protection; couples to LangGraph runner for execution |
| **Frontend (React)** | **Good** | Clean page/component/hook/api separation; React Flow for DAG viz; TanStack Query for server state; no direct Python coupling |
| **Workflow definitions** | **Fair** | YAML-driven with strong schema validation; deep_research.yaml has significant duplication across 4 rounds (YAML anchors help but ~600 lines) |

---

## Protocol Design Analysis

### Core Protocols (`core/protocols.py`)

The protocol layer is the architectural keystone. Five protocols define the system's structural contracts:

| Protocol | Methods | `runtime_checkable` | Implementations |
|----------|---------|---------------------|-----------------|
| `ExecutionEngine` | `execute(workflow, ctx, on_update)` | Yes | `DAGExecutor`, `PipelineExecutor`, `NativeEngine`, `LangChainEngine` |
| `SupportsStreaming` | `stream(workflow, ctx)` | Yes | `LangChainEngine` |
| `SupportsCheckpointing` | `get_checkpoint_state()`, `resume()` | Yes | `WorkflowRunner` (via LangGraph) |
| `AgentProtocol` | `name`, `run(input_data, ctx)` | Yes | `BaseAgent` subclasses, Claude SDK agent |
| `ToolProtocol` | `name`, `description`, `execute()` | Yes | 12 built-in tool modules |

### RAG Protocols (`rag/protocols.py`)

| Protocol | Methods | Implementations |
|----------|---------|-----------------|
| `LoaderProtocol` | `load(source)`, `supported_extensions` | `TextLoader`, `MarkdownLoader` |
| `ChunkerProtocol` | `chunk(document, config)` | `RecursiveChunker` |
| `EmbeddingProtocol` | `embed(texts)`, `dimensions` | `InMemoryEmbedder`, `FallbackEmbedder` |
| `VectorStoreProtocol` | `add()`, `search()`, `delete()` | `InMemoryVectorStore` |

### Memory Protocol (`core/memory.py`)

| Protocol | Methods | Implementations |
|----------|---------|-----------------|
| `MemoryStoreProtocol` | `store()`, `retrieve()`, `search()`, `delete()`, `list_keys()` | `InMemoryStore`, `RAGMemoryStore` |

**Strengths:**
- PEP 544 structural subtyping (Protocol over ABC) enables implicit conformance without inheritance
- `@runtime_checkable` allows isinstance() checks for adapter validation
- Clean separation between core engine protocols and domain-specific RAG/memory protocols
- Backward-compatible alias: `MemoryStore = MemoryStoreProtocol`

**Weaknesses:**
- `ExecutionEngine.execute()` uses `Any` for workflow, ctx, and return type. This loses compile-time type safety and pushes type validation to runtime.
- `AgentProtocol.run()` also uses `Any` for both input and output. The `BaseAgent` generic typing (TInput/TOutput) is excellent but the protocol itself doesn't enforce it.
- No protocol for the WorkflowLoader or config validation — these are concrete classes only.

**Cross-reference (Code Quality Auditor):** The ruff linter configuration is **missing** from `agentic-workflows-v2/pyproject.toml` -- no `[tool.ruff]` section exists. The pre-commit hook runs `ruff --fix` with no `--select`, falling back to ruff defaults (E+F only). CLAUDE.md prescribes 13 rule categories (E, F, W, I, N, UP, S, B, A, C4, SIM, TCH, RUF). Only `agentic-v2-eval` has an explicit ruff config. This means documented code quality standards are aspirational rather than tool-enforced for the main package.

---

## Adapter Pattern Analysis

### AdapterRegistry (`adapters/registry.py`)

The adapter pattern cleanly decouples workflow execution from engine implementation:

```
Server/CLI  -->  AdapterRegistry.get_adapter("native")  -->  NativeEngine  -->  DAGExecutor
                                                                              -->  PipelineExecutor

Server/CLI  -->  AdapterRegistry.get_adapter("langchain")  -->  LangChainEngine  -->  WorkflowRunner
```

**Design Quality:**

| Aspect | Assessment |
|--------|-----------|
| **Thread safety** | Excellent: `threading.Lock` on singleton creation and adapter access |
| **Lazy instantiation** | Good: adapters constructed on first `get_adapter()` call |
| **Duplicate registration guard** | Good: raises `AdapterError` on name collision |
| **Error handling** | Good: `AdapterNotFoundError` with list of available adapters |
| **Optional dependency handling** | Good: LangChainEngine guarded by `try/except ImportError` |

**Gap: Context bridging.** The `LangChainEngine` adapter accepts `ctx: Any` but currently does not forward the `ExecutionContext` to the underlying `WorkflowRunner`. This means shared state (variables, services, step tracking) from the native context system is not available in LangGraph executions. The ctx parameter is reserved for "future use" per the docstring.

**Gap: Instance caching.** The registry caches adapter instances, meaning configuration changes after first access require a registry reset. This is fine for production but requires `object.__new__()` workarounds in tests (as noted in MEMORY.md).

---

## RAG Pipeline Architecture

The RAG module is the most architecturally sophisticated component, implemented across 13 focused modules:

```
Document Sources
      |
      v
  LoaderProtocol  -->  [TextLoader, MarkdownLoader]
      |                     (path traversal protection via allowed_base_dir)
      v
  ChunkerProtocol  -->  RecursiveChunker
      |                     (configurable: chunk_size, overlap, separators)
      v
  IngestionPipeline  -->  content-hash deduplication
      |
      v
  EmbeddingProtocol  -->  [InMemoryEmbedder, FallbackEmbedder]
      |
      v
  VectorStoreProtocol  -->  InMemoryVectorStore (cosine similarity)
      |
      v
  BM25Index  -->  Pure Python Okapi BM25 (no deps)
      |
      v
  HybridRetriever  -->  reciprocal_rank_fusion() (RRF, k=60)
      |
      v
  TokenBudgetAssembler  -->  Token-budget-aware context packing
      |
      v
  RAGSearchTool / RAGIngestTool  -->  Agent tool bridge
      |
      v
  RAGMemoryStore  -->  MemoryStoreProtocol bridge
      |
      v
  RAGTracer  -->  OpenTelemetry-style span tracing
```

**Strengths:**
- Every stage is protocol-backed and independently replaceable
- Content-hash deduplication prevents embedding waste
- Hybrid retrieval (dense + BM25 via RRF) is state-of-the-art for recall
- Token budget assembly prevents context window overflow
- Tool bridges (`RAGSearchTool`, `RAGIngestTool`) integrate cleanly with agent tool registry
- `RAGMemoryStore` bridges the RAG vectorstore to the memory protocol, enabling agents to persist memories semantically
- Security: path traversal protection in loaders, top_k bounds validation

**Areas for improvement:**
- All current implementations are in-memory (suitable for dev/testing). Production would require persistent vector store (LanceDB optional dep exists but no adapter yet).
- No chunking strategy selection at the YAML workflow level.
- ~92% test coverage exceeds the 80% gate, which is good.

---

## Config vs Code Analysis

### Ratio by Category

| Category | Config-Driven | Code-Driven | Ratio |
|----------|--------------|-------------|-------|
| **Workflow definitions** | 10 YAML files (~2,500 lines) | WorkflowLoader parser (~570 lines) | **81% config** |
| **Agent personas** | 22+ markdown files | BaseAgent, concrete agents (~860 lines) | **72% config** |
| **Evaluation rubrics** | 8 YAML files | Scorer, evaluators (~1,200 lines) | **40% config** |
| **Model routing** | `models.yaml` defaults | SmartModelRouter, backends (~2,000 lines) | **15% config** |
| **Tool definitions** | Tool registry metadata | 12 builtin modules (~3,000 lines) | **10% config** |
| **Server routes** | CORS env var, API key env | FastAPI routes (~1,500 lines) | **5% config** |

**Overall config-driven ratio: ~45%** for the workflow/agent layer, which is the primary focus. This is appropriate: workflows and personas are highly declarative, while execution engines, model routing, and tools require imperative logic.

### YAML Workflow Schema Features

Each workflow YAML supports:
- `name`, `description`, `version`
- `capabilities` (inputs/outputs for dataset matching)
- `evaluation` block with weighted rubric criteria, critical floors, and formula IDs
- `inputs` with type/enum/default/required validation
- `steps` with `agent`, `depends_on`, `when` conditions, `inputs`/`outputs` mappings, `loop_until`/`loop_max`, `tools` allowlist
- `outputs` with `from` expressions and `optional` flag
- YAML anchors (`_templates`) for step reuse

This is a comprehensive declarative DSL. The `deep_research.yaml` workflow demonstrates the full power (and limits) — at 619 lines, the 4 iterative rounds are well-structured but repetitive.

---

## Extensibility Assessment

### Adding a New Vertical (e.g., Defense Compliance)

| Extension Point | Effort | Impact | Notes |
|----------------|--------|--------|-------|
| New workflow YAML | **S** | 5 | Add `defense_compliance_review.yaml` under `workflows/definitions/` |
| New agent personas | **S** | 4 | Add `compliance_auditor.md`, `security_assessor.md` under `prompts/` |
| New evaluation rubric | **S** | 3 | Add `defense_compliance.yaml` under `rubrics/` |
| New tool (e.g., STIG checker) | **M** | 4 | Implement `BaseTool` subclass in `tools/builtin/`, register in registry |
| New execution engine | **M** | 3 | Implement `ExecutionEngine` protocol, register in `AdapterRegistry` |
| New RAG data loader | **S** | 3 | Implement `LoaderProtocol` for new document format |
| New vector store backend | **M** | 4 | Implement `VectorStoreProtocol` for production store (Pinecone, Weaviate, etc.) |
| New LLM provider | **S** | 3 | Add provider adapter in `models/backends.py`, update tier config |
| Vertical-specific UI page | **M** | 3 | Add page component, route, and API endpoint |

**Overall extensibility: High.** The protocol-driven design means most extensions require implementing a well-defined interface and registering the implementation. No core code changes needed for the common cases (new workflow, persona, rubric, loader, or provider).

**Constraints:**
- The `deep_research.yaml` round-based structure doesn't support dynamic round counts; adding more rounds requires YAML duplication.
- The server routes module (`workflows.py`) at ~1,200 lines is the largest single file and may need splitting as verticals add specialized endpoints.
- No plugin/discovery mechanism for custom adapters or tools — registration is import-time only.

---

## Dual Purpose Evaluation

### As a Working Framework

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **Functional completeness** | **Good** | Full pipeline: YAML load -> DAG schedule -> LLM route -> execute -> trace -> evaluate |
| **Production readiness** | **Fair** | In-memory stores sufficient for dev; needs persistent backends for production |
| **Test coverage** | **Good** | 1305 tests, ~92% RAG coverage, 80% overall target |
| **Observability** | **Good** | OpenTelemetry tracing, WebSocket/SSE streaming, JSON replay logs |
| **Security** | **Good** | API key auth, CORS, path traversal protection, tool allowlisting, prompt injection noted for future |

### As an Educational Portfolio

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **Architectural clarity** | **Excellent** | Protocol hierarchy, adapter pattern, DAG execution — textbook patterns |
| **Code documentation** | **Good** | Comprehensive docstrings in Google style; module-level docstrings explain rationale |
| **Progressive complexity** | **Good** | Phases 0-4 in `__init__.py` show build-up; ADR roadmap documents decisions |
| **Runnable examples** | **Fair** | YAML workflows serve as examples but no standalone quickstart script |
| **Visual learning aids** | **Good** | React Flow DAG visualization, evaluation scoring UI |
| **Concept coverage** | **Excellent** | Covers: protocols, adapters, DAG scheduling, LLM routing, RAG, hybrid retrieval, BM25, RRF, memory abstraction, evaluation rubrics, observability |

---

## Recommendations

| # | Recommendation | Impact (1-5) | Effort (S/M/L) | Priority |
|---|---------------|:------------:|:---------------:|:--------:|
| 1 | **Tighten protocol type signatures** — Replace `Any` in `ExecutionEngine.execute()` and `AgentProtocol.run()` with bounded TypeVars or Union types to recover compile-time safety | 4 | M | High |
| 2 | **Bridge ExecutionContext to LangChainEngine** — Forward ctx variables and services so both engines share state during adapter-routed execution | 4 | M | High |
| 3 | **Extract deep_research round template** — Refactor the 4 repeated rounds into a loader-level loop construct (e.g., `loop_count` at workflow level) to reduce 619 lines to ~200 | 3 | M | Medium |
| 4 | **Add cross-package integration tests** — Create tests that exercise workflow execution end-to-end across the `tools/` LLM client, `agentic-workflows-v2` engine, and `agentic-v2-eval` scoring | 4 | M | High |
| 5 | **Split `server/routes/workflows.py`** — At ~1,200 lines, extract evaluation, dataset, and run-history concerns into separate route modules | 3 | S | Medium |
| 6 | **Add persistent VectorStore adapter** — Implement `VectorStoreProtocol` for LanceDB (already an optional dep) to bridge dev and production | 4 | M | Medium |
| 7 | **Add adapter/tool plugin discovery** — Use entry_points or a plugin directory scan so custom adapters/tools don't need import-time registration in core code | 3 | M | Low |
| 8 | **Create standalone quickstart script** — A `quickstart.py` or CLI command that runs a simple workflow end-to-end for new engineers | 3 | S | Medium |
| 9 | **Document protocol implementation guide** — A "How to implement ExecutionEngine / VectorStoreProtocol" tutorial with test template for the educational portfolio | 3 | S | Medium |
| 10 | **Add RAG prompt injection hardening** — Implement delimiter framing at the system prompt level for retrieved documents (noted as architectural gap in security audit) | 4 | M | High |

---

## Appendix: Key File Reference

| File | Lines | Purpose |
|------|-------|---------|
| `core/protocols.py` | 155 | Core protocol definitions (5 protocols) |
| `core/memory.py` | 240 | MemoryStoreProtocol + InMemoryStore |
| `core/errors.py` | 43 | Error hierarchy (8 exception types) |
| `adapters/registry.py` | 105 | Thread-safe singleton adapter registry |
| `adapters/native/engine.py` | 77 | NativeEngine (DAG + Pipeline delegation) |
| `adapters/langchain/engine.py` | 123 | LangChainEngine (WorkflowRunner wrapper) |
| `engine/dag_executor.py` | 269 | Kahn's algorithm DAG scheduler |
| `engine/context.py` | 451 | Hierarchical execution context + DI |
| `langchain/runner.py` | 717 | LangGraph workflow runner |
| `agents/base.py` | 861 | BaseAgent + ConversationMemory + AgentConfig |
| `rag/protocols.py` | 116 | RAG protocol definitions (4 protocols) |
| `rag/retrieval.py` | 329 | BM25Index + RRF + HybridRetriever |
| `rag/memory.py` | 193 | RAGMemoryStore (vectorstore-backed memory) |
| `rag/contracts.py` | 103 | Document, Chunk, RetrievalResult, RAGResponse |
| `workflows/loader.py` | 572 | YAML workflow parser + DAG builder |
| `server/app.py` | 167 | FastAPI application factory |
| `workflows/definitions/code_review.yaml` | 131 | Example declarative workflow |
| `workflows/definitions/deep_research.yaml` | 619 | Complex multi-round research workflow |
