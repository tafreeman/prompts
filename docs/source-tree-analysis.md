# Source Tree Analysis — `tafreeman/prompts`

Annotated directory tree for the `tafreeman/prompts` monorepo. Annotations describe the purpose of every critical directory, key entry points, and the integration boundaries between the four packages.

---

## Annotated Directory Tree

```
prompts/                                   # Monorepo root — uv workspace, hatchling builds
│
├── pyproject.toml                         # Workspace root: uv workspace members, shared ruff/pytest config,
│                                          #   prompts-tools package definition
├── uv.lock                                # Pinned dependency lockfile for reproducible installs
├── docker-compose.yml                     # Compose stack: backend + otel-collector services
├── Dockerfile                             # Backend container image
├── Dockerfile.ui                          # Frontend container image
├── justfile                               # Task runner shortcuts (build, test, lint, serve)
│
├── agentic-workflows-v2/                  # Package 1 — Multi-agent workflow runtime (Python 3.11+)
│   ├── pyproject.toml                     # Package config: hatchling, extras (dev/server/langchain/rag/tracing)
│   │
│   ├── agentic_v2/                        # Source package (~36,300 lines)
│   │   ├── __init__.py                    # Public API: DAGExecutor, ExecutionContext, WorkflowLoader
│   │   │
│   │   ├── agents/                        # Agent definitions and implementations
│   │   │   ├── base.py                    # BaseAgent abstract class and agent lifecycle
│   │   │   ├── coder.py                   # CoderAgent — code generation specialist
│   │   │   ├── reviewer.py                # ReviewerAgent — code review and quality analysis
│   │   │   ├── orchestrator.py            # OrchestratorAgent — multi-agent coordination
│   │   │   ├── architect.py               # ArchitectAgent — system design decisions
│   │   │   ├── capabilities.py            # Agent capability declarations
│   │   │   ├── config.py                  # Agent-level configuration loading
│   │   │   ├── memory.py                  # Per-agent memory access helpers
│   │   │   ├── json_extraction.py         # LLM output JSON parser utilities
│   │   │   └── implementations/          # Concrete agent implementations (domain-specific)
│   │   │
│   │   ├── adapters/                      # Pluggable execution engine backends
│   │   │   ├── registry.py               # AdapterRegistry singleton — maps name → ExecutionEngine
│   │   │   ├── native/                   # Native DAG engine adapter wrapper
│   │   │   └── langchain/               # LangGraph engine adapter (optional import guard)
│   │   │
│   │   ├── cli/                           # Typer CLI application
│   │   │   ├── main.py                   # Entry point: `agentic` command group
│   │   │   ├── helpers.py                # Shared CLI utilities (output formatting)
│   │   │   ├── display.py                # Rich terminal display helpers
│   │   │   └── rag_commands.py           # `agentic rag ingest/search` subcommands
│   │   │
│   │   ├── config/                        # Runtime configuration
│   │   │   └── defaults/                 # YAML defaults loaded at startup
│   │   │       ├── models.yaml           # LLM tier → model name mappings per provider
│   │   │       ├── agents.yaml           # Agent capability → tier assignments
│   │   │       └── evaluation.yaml       # Scoring profile defaults
│   │   │
│   │   ├── contracts/                     # Pydantic v2 I/O models (additive-only schema policy)
│   │   │   ├── messages.py               # Canonical message types: UserMessage, AssistantMessage, ToolCall
│   │   │   ├── schemas.py                # Workflow and step I/O schemas
│   │   │   ├── sanitization.py           # Sanitization result contracts
│   │   │   └── verification.py           # Step verification result contracts
│   │   │
│   │   ├── core/                          # Foundational abstractions
│   │   │   ├── protocols.py              # Runtime-checkable protocols: ExecutionEngine, AgentProtocol,
│   │   │   │                             #   ToolProtocol, MemoryStore, SupportsStreaming,
│   │   │   │                             #   SupportsCheckpointing
│   │   │   ├── memory.py                 # InMemoryStore + RAGMemoryStore implementations
│   │   │   └── errors.py                 # Base exception hierarchy for the runtime
│   │   │
│   │   ├── engine/                        # Native DAG executor (no LangChain dependency)
│   │   │   ├── dag.py                    # DAG graph construction and topological validation
│   │   │   ├── dag_executor.py           # Kahn's algorithm parallel step scheduler
│   │   │   ├── executor.py               # High-level DAGExecutor facade (public API)
│   │   │   ├── runtime.py                # Execution runtime context and step lifecycle
│   │   │   ├── step.py                   # Step data model and dependency resolution
│   │   │   ├── step_state.py             # Step state machine (PENDING → RUNNING → DONE/FAILED)
│   │   │   ├── pipeline.py               # Pipeline orchestration across steps
│   │   │   ├── agent_resolver.py         # Resolves agent names to agent instances
│   │   │   ├── context.py                # Execution context propagation
│   │   │   ├── expressions.py            # Step input template expression evaluator
│   │   │   ├── prompt_assembly.py        # Prompt construction from templates and context
│   │   │   ├── tool_execution.py         # Built-in tool dispatch and sandboxing
│   │   │   ├── llm_output_parsing.py     # Structured output extraction from LLM responses
│   │   │   ├── verification.py           # Post-step output verification logic
│   │   │   ├── protocol.py               # Engine-layer protocol definitions
│   │   │   └── patterns/                 # Reusable execution patterns (retry, fan-out, etc.)
│   │   │
│   │   ├── evaluation/                    # Inline evaluation primitives (runtime-internal)
│   │   │
│   │   ├── integrations/                  # External system adapters
│   │   │   ├── otel.py                   # OpenTelemetry SDK setup and span helpers
│   │   │   ├── tracing.py                # Trace context propagation utilities
│   │   │   ├── langchain.py              # LangChain callback integration
│   │   │   ├── base.py                   # Integration base class
│   │   │   └── mcp/                      # Model Context Protocol integration
│   │   │
│   │   ├── langchain/                     # LangGraph execution engine (optional [langchain] extra)
│   │   │   ├── graph.py                  # LangGraph state machine construction
│   │   │   ├── graph_wiring.py           # Node and edge wiring from YAML workflow definitions
│   │   │   ├── runner.py                 # LangGraph workflow runner entry point
│   │   │   ├── state.py                  # LangGraph state schema definitions
│   │   │   ├── models.py                 # LLM model instantiation for LangGraph nodes
│   │   │   ├── model_builders.py         # Provider-specific model builder factories
│   │   │   ├── model_utils.py            # Model configuration utilities
│   │   │   ├── config.py                 # Workflow config loading for LangGraph
│   │   │   ├── agents.py                 # Agent node implementations for LangGraph
│   │   │   ├── tools.py                  # Tool node implementations for LangGraph
│   │   │   ├── expressions.py            # Expression evaluation in LangGraph context
│   │   │   ├── dependencies.py           # Dependency injection for LangGraph runners
│   │   │   └── result_builder.py         # Structured result assembly from graph output
│   │   │
│   │   ├── middleware/                    # Request/response sanitization pipeline
│   │   │   ├── sanitization.py           # Main pipeline (clean / redact / block / requires_approval)
│   │   │   ├── base.py                   # Detector base class and result types
│   │   │   ├── policy.py                 # Policy engine: maps detection results to actions
│   │   │   ├── response_sanitizer.py     # Outbound response sanitizer
│   │   │   └── detectors/               # Individual detector modules
│   │   │       ├── secrets.py            # API key, token, and credential pattern detection
│   │   │       ├── pii.py                # PII detection (email, phone, SSN, etc.)
│   │   │       ├── injection.py          # Prompt injection pattern detection
│   │   │       └── unicode.py            # Malicious Unicode normalization and stripping
│   │   │
│   │   ├── models/                        # LLM provider management and routing
│   │   │   ├── router.py                 # ModelRouter: tier-based model selection
│   │   │   ├── smart_router.py           # SmartRouter: adaptive routing with circuit breaker,
│   │   │   │                             #   bulkhead concurrency limits, latency-weighted selection
│   │   │   ├── client.py                 # Unified LLM client facade
│   │   │   ├── llm.py                    # LLM model class (wraps tools.llm aliased as LegacyClient)
│   │   │   ├── backends.py               # Provider backend registry and dispatch
│   │   │   ├── backends_base.py          # Abstract backend interface
│   │   │   ├── backends_cloud.py         # Cloud provider backends (OpenAI, Anthropic, Gemini, Azure)
│   │   │   ├── backends_local.py         # Local model backends (Ollama, ONNX, Windows AI/Phi Silica)
│   │   │   ├── model_stats.py            # Per-model stats: latency, error rate, CircuitState
│   │   │   ├── rate_limit_tracker.py     # Provider-level rate limit tracking and backoff
│   │   │   └── secrets.py                # SecretProvider abstraction for API key retrieval
│   │   │
│   │   ├── prompts/                       # Agent persona definitions (7 Markdown files)
│   │   │   ├── coder.md                  # CoderAgent: expertise, boundaries, output format
│   │   │   ├── reviewer.md               # ReviewerAgent persona
│   │   │   ├── orchestrator.md           # OrchestratorAgent persona
│   │   │   ├── architect.md              # ArchitectAgent persona
│   │   │   ├── planner.md                # PlannerAgent persona
│   │   │   ├── tester.md                 # TesterAgent persona
│   │   │   └── validator.md              # ValidatorAgent persona
│   │   │
│   │   ├── rag/                           # Full Retrieval-Augmented Generation pipeline
│   │   │   ├── ingestion.py              # Document loading and pipeline orchestration
│   │   │   ├── loaders.py                # File format loaders (PDF, DOCX, MD, TXT, code)
│   │   │   ├── chunking.py               # Recursive character splitter with overlap
│   │   │   ├── embeddings.py             # Embedding model abstraction + content-hash dedup
│   │   │   ├── vectorstore.py            # Cosine similarity in-memory vector store
│   │   │   ├── retrieval.py              # BM25 keyword index + hybrid RRF fusion retrieval
│   │   │   ├── reranking.py              # NoOpReranker / CrossEncoderReranker / LLMReranker
│   │   │   ├── context_assembly.py       # Token-budget context assembly from retrieved chunks
│   │   │   ├── memory.py                 # RAGMemoryStore: persistent memory backed by RAG index
│   │   │   ├── tools.py                  # RAG tool wrappers for agent use
│   │   │   ├── config.py                 # RAGConfig and RerankerConfig Pydantic models
│   │   │   ├── contracts.py              # RAG-specific Pydantic contracts
│   │   │   ├── protocols.py              # RerankerProtocol and VectorStore protocol definitions
│   │   │   ├── errors.py                 # RAG-specific exception types
│   │   │   └── tracing.py                # OTEL span instrumentation for every pipeline stage
│   │   │
│   │   ├── server/                        # FastAPI web server
│   │   │   ├── app.py                    # Application factory: CORS, auth middleware, routing,
│   │   │   │                             #   SPA static serving, lifespan (LLM probe + OTEL flush)
│   │   │   ├── auth.py                   # APIKeyMiddleware (Bearer / X-API-Key, timing-safe compare)
│   │   │   ├── websocket.py              # WebSocket endpoint: /ws/execution/{run_id}
│   │   │   ├── execution.py              # Background workflow execution orchestration
│   │   │   ├── models.py                 # Server-layer Pydantic request/response models
│   │   │   ├── evaluation.py             # In-server scoring logic
│   │   │   ├── evaluation_scoring.py     # Score computation helpers
│   │   │   ├── scoring_criteria.py       # Configurable scoring criteria definitions
│   │   │   ├── scoring_profiles.py       # Named scoring profile registry
│   │   │   ├── multidimensional_scoring.py # Multi-axis scoring aggregation
│   │   │   ├── judge.py                  # LLM-as-judge integration for server-side scoring
│   │   │   ├── datasets.py               # Evaluation dataset management (imports tools.agents.benchmarks)
│   │   │   ├── dataset_matching.py       # Workflow ↔ dataset matching heuristics
│   │   │   ├── normalization.py          # Result normalization utilities
│   │   │   ├── result_normalization.py   # Pure result assembly helpers
│   │   │   ├── middleware/               # Server-level middleware (request logging, etc.)
│   │   │   └── routes/                   # FastAPI APIRouter modules (all mounted under /api/)
│   │   │       ├── workflows.py          # GET /workflows, /workflows/{name}/dag,
│   │   │       │                         #   /workflows/{name}/capabilities,
│   │   │       │                         #   /workflows/{name}/editor, /adapters
│   │   │       │                         #   PUT /workflows/{name}
│   │   │       │                         #   POST /run, POST /workflows/{name}/validate
│   │   │       ├── runs.py               # GET /runs, /runs/summary, /runs/{filename},
│   │   │       │                         #   /runs/{run_id}/stream (SSE)
│   │   │       ├── evaluation_routes.py  # GET /eval/datasets,
│   │   │       │                         #   /workflows/{name}/preview-dataset-inputs
│   │   │       ├── agents.py             # GET /agents
│   │   │       └── health.py             # GET /health
│   │   │
│   │   ├── tools/                         # Tool framework
│   │   │   └── builtin/                  # 11 built-in tool modules (default DENY for high-risk ops)
│   │   │       ├── file_ops.py           # File read/write/list (AGENTIC_FILE_BASE_DIR path guard)
│   │   │       ├── shell_ops.py          # Shell command execution (explicit allowlist required)
│   │   │       ├── code_execution.py     # Sandboxed Python code execution
│   │   │       ├── code_analysis.py      # AST-based code analysis tools
│   │   │       ├── search_ops.py         # Web and local search
│   │   │       ├── http_ops.py           # HTTP fetch tools
│   │   │       ├── git_ops.py            # Git operations (explicit allowlist required)
│   │   │       ├── build_ops.py          # Build and test execution tools
│   │   │       ├── memory_ops.py         # Agent memory read/write tools
│   │   │       ├── context_ops.py        # Execution context manipulation tools
│   │   │       └── transform.py          # Data transformation utilities
│   │   │
│   │   ├── utils/                         # General runtime utilities
│   │   │
│   │   └── workflows/                     # Workflow loading and definitions
│   │       └── definitions/              # 6 YAML workflow definitions
│   │           ├── code_review.yaml      # Multi-step code review workflow
│   │           ├── bug_resolution.yaml   # Bug triage and fix workflow
│   │           ├── fullstack_generation.yaml # Full-stack feature generation
│   │           ├── iterative_review.yaml # Review-revise-approve loop
│   │           ├── conditional_branching.yaml # Conditional step branching example
│   │           └── test_deterministic.yaml   # Deterministic workflow (runs without API keys)
│   │
│   ├── tests/                             # 87 test files — pytest-asyncio auto mode
│   │   └── (mirrors agentic_v2/ structure: agents/, engine/, rag/, server/, ...)
│   │
│   ├── examples/                          # Runnable usage examples (some work without API keys)
│   │
│   └── ui/                                # React 19 dashboard (Vite 6)
│       ├── package.json                   # Node deps: React 19, @xyflow/react 12, TanStack Query,
│       │                                  #   Tailwind CSS, Vitest, React Testing Library
│       ├── vite.config.ts                 # Vite config: /api proxy → :8010, /ws proxy (ws) → :8010,
│       │                                  #   VITE_AGENTIC_ENABLE_WORKFLOW_BUILDER feature flag
│       ├── tsconfig.json                  # TypeScript strict mode configuration
│       │
│       ├── src/
│       │   ├── main.tsx                   # React app entry point — QueryClient, Router setup
│       │   ├── App.tsx                    # Root component with client-side route definitions
│       │   ├── api/                       # Network layer
│       │   │   ├── (fetch client)        # Type-safe fetch wrappers for all REST endpoints
│       │   │   └── (websocket client)    # WebSocket connection manager for execution streaming
│       │   ├── components/               # 17 UI components organized by domain
│       │   │   ├── layout/              # AppShell, Sidebar, Header
│       │   │   ├── common/              # Shared: buttons, badges, status indicators
│       │   │   ├── dag/                 # @xyflow/react DAG visualization components
│       │   │   ├── runs/                # Run history list and detail components
│       │   │   └── live/                # Live execution streaming components
│       │   ├── config/                  # Feature flag definitions
│       │   │   └── (feature flags)      # VITE_AGENTIC_ENABLE_WORKFLOW_BUILDER runtime check
│       │   ├── hooks/                   # Data-fetching and WebSocket state hooks
│       │   │   ├── useWorkflows.ts      # TanStack Query: workflow list and DAG data
│       │   │   ├── useRuns.ts           # TanStack Query: run history
│       │   │   ├── useWorkflowStream.ts # WebSocket state machine for live execution
│       │   │   └── useNodeConfigUpdate.ts # Workflow editor node config mutations
│       │   ├── pages/                   # 8 page-level components
│       │   │   ├── WorkflowsPage.tsx    # Workflow list and launch
│       │   │   ├── WorkflowDetailPage.tsx # DAG visualization + run form
│       │   │   ├── WorkflowEditorPage.tsx # Visual workflow editor (feature-flagged)
│       │   │   ├── DashboardPage.tsx    # Overview: stats and recent runs
│       │   │   ├── RunDetailPage.tsx    # Individual run result detail
│       │   │   ├── LivePage.tsx         # Real-time execution monitor
│       │   │   ├── EvaluationsPage.tsx  # Evaluation results browser
│       │   │   └── DatasetsPage.tsx     # Evaluation dataset browser
│       │   ├── styles/                  # globals.css: Tailwind base + dark theme CSS variables
│       │   └── types/                   # Shared TypeScript type definitions
│       │
│       └── __tests__/                    # 23 Vitest test files (React Testing Library)
│
├── agentic-v2-eval/                       # Package 2 — Standalone evaluation framework
│   ├── pyproject.toml                     # Hatchling build config, extras: [dev, llm]
│   │
│   └── src/agentic_v2_eval/              # Source package
│       ├── __main__.py                   # CLI: `python -m agentic_v2_eval evaluate/report`
│       ├── interfaces.py                 # Public interfaces and abstract base types
│       ├── scorer.py                     # Top-level Scorer orchestration class
│       ├── datasets.py                   # Dataset loading (lazy imports tools.agents.benchmarks)
│       ├── evaluators/                   # 4 evaluator implementations
│       │   ├── base.py                   # BaseEvaluator with rubric loading
│       │   ├── llm.py                    # LLM-as-judge: 0.0–10.0 rubric scoring
│       │   ├── pattern.py                # Regex/AST pattern-based evaluator
│       │   ├── quality.py                # AST-based code quality evaluator
│       │   └── standard.py              # Standards compliance evaluator
│       ├── metrics/                      # Metric computation modules
│       │   ├── accuracy.py               # Correctness metrics
│       │   ├── performance.py            # Latency and throughput metrics
│       │   └── quality.py                # AST-based code quality metrics
│       ├── reporters/                    # Output format reporters
│       │   └── (json / markdown / html) # Machine-readable JSON, human Markdown, web HTML
│       ├── runners/                      # Evaluation execution modes
│       │   ├── batch.py                  # BatchRunner: synchronous bulk evaluation
│       │   └── streaming.py              # StreamingRunner + AsyncStreamingRunner
│       ├── rubrics/                      # 8 YAML rubric definitions
│       │   ├── default.yaml             # General-purpose rubric
│       │   ├── agent.yaml               # Agent behavior evaluation rubric
│       │   ├── code.yaml                # Code correctness rubric
│       │   ├── coding_standards.yaml    # Standards compliance rubric
│       │   ├── pattern.yaml             # Pattern matching rubric
│       │   ├── prompt_pattern.yaml      # Prompt engineering rubric
│       │   ├── prompt_standard.yaml     # Prompt standards rubric
│       │   └── quality.yaml             # Code quality rubric
│       ├── sandbox/                      # Local subprocess sandbox for code evaluation
│       └── adapters/                     # Bridge adapters to shared tools
│           └── llm_client.py            # Lazy import of tools.llm.LLMClient for eval LLM calls
│
├── tools/                                 # Package 3 — Shared utilities (prompts-tools)
│   │                                      #   Built from workspace root pyproject.toml
│   ├── llm/                              # Multi-provider LLM client
│   │   ├── llm_client.py                 # LLMClient: 10-provider unified async client
│   │   ├── langchain_adapter.py          # LangChain-compatible adapter wrapping LLMClient
│   │   ├── local_model.py                # ONNX/local model client
│   │   ├── local_model_discovery.py      # Auto-detect models from ~/.cache/aigallery
│   │   ├── provider_adapters.py          # Per-provider request/response normalization
│   │   └── windows_ai.py                 # Windows AI (Phi Silica) integration bridge
│   │
│   ├── core/                             # Shared runtime utilities
│   │   └── (config, errors, cache,      # Configuration loading, exception taxonomy,
│   │        encoding, tool_init)         #   response caching, text encoding utilities
│   │
│   ├── agents/                           # Agent tooling and benchmarks
│   │   └── benchmarks/                  # 8 benchmark definitions + evaluation pipeline
│   │       ├── llm_evaluator.py         # LLM judge: 0.0–10.0 rubric scoring entry point
│   │       ├── evaluation_pipeline.py   # End-to-end benchmark evaluation runner
│   │       ├── datasets.py              # Benchmark dataset definitions (8 named datasets)
│   │       ├── registry.py              # Benchmark registry
│   │       └── runner.py                # Benchmark execution engine
│   │
│   ├── research/                         # Research library builder utilities
│   │
│   └── tests/                            # 10 test modules (70% coverage gate in CI)
│
├── docs/                                  # Project documentation (this directory)
│   ├── source-tree-analysis.md           # This file — annotated directory tree
│   ├── project-overview.md               # Executive summary and tech stack
│   ├── integration-architecture.md       # Cross-package communication contracts
│   ├── development-guide.md              # Developer setup and workflow guide
│   └── deployment-guide.md              # CI/CD, environment variables, production config
│
├── .claude/                               # Claude Code configuration
│   ├── agents/                           # 13 agent definitions
│   ├── commands/                         # 11 custom slash commands
│   ├── rules/                            # 12 rule files (coding-style, security, testing, etc.)
│   └── skills/                           # 14 skill definitions
│
├── .github/                               # GitHub configuration
│   └── workflows/                        # CI/CD — 11 GitHub Actions workflow files
│       ├── ci.yml                        # Primary: 8 jobs (lint-and-test, frontend, eval-tests,
│       │                                 #   tools-tests, type-check, integration,
│       │                                 #   cross-package-e2e, security)
│       ├── deploy.yml                    # Production deployment workflow
│       ├── dependency-review.yml         # Dependency vulnerability review on PRs
│       ├── docs-verify.yml               # Documentation reference validation
│       ├── eval-package-ci.yml           # Eval package isolated CI
│       ├── tools-ci.yml                  # Tools package isolated CI
│       ├── performance-benchmark.yml     # LLM benchmark runs
│       ├── prompt-quality-gate.yml       # Prompt quality gate checks
│       ├── prompt-validation.yml         # Workflow YAML validation
│       ├── eval-poc.yml                  # Eval proof-of-concept runs
│       └── manifest-temperature-check.yml # Model configuration drift detection
│
├── research/                              # Research materials and subagent reports
├── otel/                                  # OpenTelemetry collector configuration
├── tests/                                 # Cross-package E2E tests
│   └── e2e/test_cross_package.py         # Cross-package integration smoke tests (marker: e2e)
├── examples/                              # Runnable usage examples
└── scripts/                               # Maintenance and helper scripts
```

---

## Critical Directories — Detailed Descriptions

### `agentic-workflows-v2/agentic_v2/core/`

The protocol layer. Defines `ExecutionEngine`, `AgentProtocol`, `ToolProtocol`, `MemoryStore`, `SupportsStreaming`, and `SupportsCheckpointing` as `@runtime_checkable` Python protocols. All engine backends and agent implementations depend on these abstractions rather than concrete classes. Changes to protocols here propagate across all four packages.

### `agentic-workflows-v2/agentic_v2/engine/`

The native DAG executor. Implements parallel workflow step scheduling using Kahn's topological sort algorithm. This engine runs without any LangChain dependency, making it suitable for environments where the optional `langchain` extra is not installed. The `DAGExecutor` class (exported from `agentic_v2/__init__.py`) is the primary entry point for programmatic workflow execution.

### `agentic-workflows-v2/agentic_v2/langchain/`

The LangGraph execution engine. Wraps LangGraph state machines for workflows that benefit from LangChain-compatible tool calling, memory, and checkpointing. Protected by optional import guards — the package functions normally if this directory's dependencies are absent. Both engines share the same workflow YAML definitions and produce structurally equivalent output.

### `agentic-workflows-v2/agentic_v2/server/`

The FastAPI HTTP server. Exposes 17 REST endpoints, one WebSocket endpoint for execution streaming, and optional SPA static file serving. The `app.py` application factory handles CORS configuration (configurable via `AGENTIC_CORS_ORIGINS`), optional API key authentication, and the startup lifespan hook that probes available LLM providers and flushes OTEL spans on shutdown. All API routes are mounted under `/api/`; WebSocket is at `/ws/execution/{run_id}`.

### `agentic-workflows-v2/agentic_v2/rag/`

A complete Retrieval-Augmented Generation pipeline. Covers document loading (PDF, DOCX, Markdown, code files), recursive chunking, content-hash-deduplicated embedding, cosine similarity vector store, BM25 keyword indexing, hybrid retrieval with Reciprocal Rank Fusion, optional cross-encoder and LLM reranking, and token-budget context assembly. Every pipeline stage is instrumented with OpenTelemetry spans via `tracing.py`.

### `agentic-workflows-v2/agentic_v2/middleware/`

A sanitization pipeline that runs on all inbound prompt content. Four detector modules (secrets, PII, injection, unicode) classify content and return one of four dispositions: `clean`, `redacted`, `blocked`, or `requires_approval`. The policy engine maps dispositions to actions. No sensitive matched text is stored in audit records — only pattern names and SHA-256 hashes of original input.

### `agentic-workflows-v2/agentic_v2/models/`

LLM provider management. `ModelRouter` provides tier-based model selection (tier-1 = fast/cheap, tier-2 = capable, tier-3 = most powerful). `SmartRouter` adds adaptive learning: circuit breaker per model (CircuitState: CLOSED/HALF_OPEN/OPEN), per-provider bulkhead concurrency limits, latency-weighted selection, and automatic fallback to adjacent tiers on degradation. Supports 8+ providers: OpenAI, Anthropic, Gemini, Azure OpenAI, Azure AI Foundry, GitHub Models, Ollama, and local ONNX/Windows AI.

### `agentic-v2-eval/src/agentic_v2_eval/`

A standalone evaluation framework. Intentionally decoupled from the runtime — the only shared dependency is `tools.llm.LLMClient`, accessed via lazy import in `adapters/llm_client.py`. Provides batch and streaming evaluation runners, four evaluator types (LLM judge, pattern, quality, standards), eight YAML rubrics, and three reporter formats (JSON, Markdown, HTML). Designed for offline scoring of workflow outputs; it does not call into `agentic-workflows-v2` at runtime.

### `tools/llm/`

The shared multi-provider LLM client. `LLMClient` is the single async client used by both the runtime (aliased as `LegacyClient` in `models/llm.py`) and the eval framework. Supports 10 providers, implements provider-specific request/response normalization, and exposes a LangChain-compatible adapter. This is the only LLM dependency that `agentic-v2-eval` takes; it does not import from `agentic-workflows-v2`.

### `agentic-workflows-v2/ui/src/`

The React 19 dashboard frontend. Communicates with the backend exclusively via the proxied `/api/` and `/ws/` paths — it has no hard-coded knowledge of the backend host at runtime. TanStack Query manages all server state. `@xyflow/react` renders interactive DAG visualizations. The `useWorkflowStream` hook manages the WebSocket state machine for real-time execution monitoring.

---

## Entry Points

| Entry Point | Command / Path | Description |
|---|---|---|
| CLI | `agentic` | Main Typer CLI (`agentic_v2/cli/main.py`) |
| Backend server | `python -m uvicorn agentic_v2.server.app:app --host 127.0.0.1 --port 8010` | FastAPI server |
| Frontend dev server | `npm run dev` (from `agentic-workflows-v2/ui/`) | Vite dev server on port 5173 |
| Frontend production build | `npm run build` (from `agentic-workflows-v2/ui/`) | TypeScript check + Vite build |
| Eval CLI | `python -m agentic_v2_eval evaluate results.json` | Evaluation framework CLI |
| Python package API | `from agentic_v2 import DAGExecutor` | Programmatic runtime API |
| Backend test suite | `python -m pytest tests/ -v` (from `agentic-workflows-v2/`) | 87 test files |
| Frontend test suite | `npm run test` (from `agentic-workflows-v2/ui/`) | 23 Vitest files |
| Cross-package E2E | `python -m pytest tests/e2e/ -m e2e` (from repo root) | Cross-package smoke tests |

### CLI Subcommands

```
agentic list workflows|agents|tools      # Enumerate available items
agentic run <workflow> --input <file>    # Execute a named workflow
agentic validate <workflow>              # Validate workflow YAML definition
agentic serve                            # Start the FastAPI server
agentic compare <workflow> --input <f>  # Compare native vs LangGraph engine output
agentic rag ingest --source <path>       # Ingest documents into the RAG index
agentic rag search <query>               # Query the RAG index
```

---

## Multi-Package Integration Points

| Integration | Mechanism | Direction |
|---|---|---|
| `runtime` imports `tools` LLM client | `tools.llm.llm_client.LLMClient` aliased as `LegacyClient` in `models/llm.py` | tools → runtime |
| `runtime` imports `tools` LangChain adapter | `tools.llm.langchain_adapter` in `langchain/model_builders.py` | tools → runtime |
| `runtime` imports `tools` benchmarks | `tools.agents.benchmarks.*` in `server/datasets.py` | tools → runtime |
| `eval` imports `tools` LLM client | Lazy import of `tools.llm.llm_client.LLMClient` in `adapters/llm_client.py` | tools → eval |
| `eval` imports `tools` benchmarks | Lazy import of `tools.agents.benchmarks` in `datasets.py` | tools → eval |
| `ui` calls `runtime` REST API | HTTP over `/api/*` proxied by Vite dev server to `:8010` | ui → runtime |
| `ui` streams from `runtime` | WebSocket `/ws/execution/{run_id}` for live step events | bidirectional |
| `eval` operates on `runtime` outputs | File-based: eval reads saved run JSON results; no direct import | independent |
| All Python packages | `PyYAML`, `Pydantic v2` as shared transitive dependencies | shared |
