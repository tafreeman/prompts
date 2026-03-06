# CLAUDE.md

## Shell Environment

- Primary development is on **Windows using PowerShell**.
- Bash helpers exist (e.g., `agentic-workflows-v2/dev.sh`) for Unix-like shells.
- When writing Windows automation, prefer PowerShell (`Stop-Process`, `Get-NetTCPConnection`) over Bash-specific commands.

## Behavioral Rules

- After making fixes, always verify by running relevant code or tests immediately.
- When asked for a file path or simple answer, give the direct answer first.
- Treat all AI-generated code as untrusted input — review for correctness, security, and standards.

---

## Project Overview

**Repo:** `tafreeman/prompts` | **Branch:** `main` | **Python:** 3.11+ (main), 3.10+ (eval, tools)

A monorepo for multi-agent workflow runtime, evaluation framework, and shared LLM utilities. Serves dual purpose as (1) working agentic AI platform and (2) educational portfolio for team onboarding at Deloitte. Targets enterprise-grade practices for cleared federal environments.

| Package | Description | Build |
|---------|-------------|-------|
| `agentic-workflows-v2/` | Multi-agent workflow runtime (Python 3.11+) | hatchling |
| `agentic-v2-eval/` | Evaluation framework (Python 3.10+) | setuptools |
| `tools/` (prompts-tools) | Shared LLM client, benchmarks, utilities (Python 3.10+) | setuptools |
| `agentic-workflows-v2/ui/` | React 19 dashboard | Vite 6 |

---

## Architecture

### High-Level Structure

```
./
├── agentic-workflows-v2/        # Main runtime
│   ├── agentic_v2/              # Source (~20,900 lines)
│   │   ├── agents/              # BaseAgent, Coder, Architect, Reviewer, Orchestrator + implementations/
│   │   ├── adapters/            # Pluggable engine backends (native, langchain)
│   │   ├── core/                # Protocols, memory, context, contracts, errors
│   │   ├── engine/              # Native DAG executor (Kahn's algorithm)
│   │   ├── langchain/           # LangGraph execution engine
│   │   ├── models/              # LLM tier routing (8+ providers)
│   │   ├── rag/                 # Full RAG pipeline (chunking, embedding, retrieval, assembly)
│   │   ├── contracts/           # Pydantic I/O models (additive-only)
│   │   ├── prompts/             # 24 agent persona definitions (.md)
│   │   ├── server/              # FastAPI + WebSocket/SSE streaming
│   │   ├── tools/builtin/       # 11 built-in tool modules
│   │   └── workflows/definitions/ # 10 YAML workflow definitions
│   ├── tests/                   # 66 files, ~1456 tests (pytest-asyncio)
│   └── ui/                      # React 19 + React Flow 12 + TanStack Query + Tailwind
├── agentic-v2-eval/             # Evaluation: rubrics, evaluators, runners, reporters
├── tools/                       # Shared: LLM client, benchmarks, caching, errors
├── research/                    # ADRs, research library
├── docs/                        # ARCHITECTURE.md, CODING_STANDARDS.md
└── .claude/                     # Commands (11), contexts (3), rules (12), skills (9)
```

### Key Architectural Points

- **Dual execution engine:** `langchain/` wraps LangGraph state machines; `engine/` is a native DAG executor (Kahn's algorithm). Both active.
- **Adapter registry:** `AdapterRegistry` singleton maps names to `ExecutionEngine` protocol backends. Built-in: `native`, `langchain`.
- **Core protocols:** `core/protocols.py` — `ExecutionEngine`, `AgentProtocol`, `ToolProtocol`, `MemoryStore`, `SupportsStreaming`, `SupportsCheckpointing`. All `@runtime_checkable`.
- **RAG pipeline:** Full pipeline in `rag/` — loading, recursive chunking, embedding (content-hash dedup), cosine similarity vectorstore, BM25 keyword index, hybrid retrieval (RRF fusion), token-budget assembly, OTEL tracing.
- **Memory:** `MemoryStoreProtocol` (async key-value + search). Implementations: `InMemoryStore`, `RAGMemoryStore`.
- **LLM routing:** `smart_router.py` dispatches by tier/capability. 8+ providers: OpenAI, Anthropic, Gemini, Azure OpenAI, Azure Foundry, GitHub Models, Ollama, local ONNX.
- **Contracts:** Pydantic models in `contracts/`. **Additive-only** — never break existing schemas.

---

## Commands

### Backend (from `agentic-workflows-v2/`)

```bash
pip install -e ".[dev,server,langchain]"       # Install
python -m pytest tests/ -v                      # Test
python -m pytest tests/ -q --cov=agentic_v2 --cov-report=term-missing  # Coverage
pre-commit run --all-files                      # Lint (from repo root)
```

### Dev Server (two terminals)

```bash
# Terminal 1 — Backend (from agentic-workflows-v2/):
python -m uvicorn agentic_v2.server.app:app --host 127.0.0.1 --port 8010 --app-dir src

# Terminal 2 — Frontend (from agentic-workflows-v2/ui/):
npm run dev
```

### CLI

```bash
agentic list workflows|agents|tools
agentic run <workflow> --input <file.json>
agentic validate <workflow>
agentic serve
```

### Frontend (from `agentic-workflows-v2/ui/`)

```bash
npm install && npm run dev       # Dev
npm run build                    # TypeScript check + Vite build
npm run test                     # Vitest
```

### Evaluation (from `agentic-v2-eval/`)

```bash
pip install -e ".[dev]"
python -m agentic_v2_eval evaluate results.json
python -m agentic_v2_eval report results.json --format html
```

### Shared Tools (from repo root)

```bash
pip install -e ".[dev]"
# from tools.llm import LLMClient
# from tools.core.errors import ErrorCode
```

---

## Environment Variables

See `.env.example` for the full template. At least one LLM provider key is required.

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API |
| `ANTHROPIC_API_KEY` | Anthropic Claude API |
| `GEMINI_API_KEY` | Google Gemini API |
| `AZURE_OPENAI_API_KEY_0` | Azure OpenAI (supports `_0` through `_n` for failover) |
| `AZURE_OPENAI_ENDPOINT_0` | Azure OpenAI endpoint |
| `GITHUB_TOKEN` | GitHub Models API |
| `LOCAL_MODEL_PATH` | Local ONNX models (auto-detected from `~/.cache/aigallery`) |

---

## Testing

| Location | Count | Framework |
|----------|-------|-----------|
| `agentic-workflows-v2/tests/` | 66 files, ~1456 tests | pytest-asyncio (auto mode) |
| `agentic-v2-eval/tests/` | 12 files | pytest + pytest-asyncio |
| `tests/e2e/` | 1 file | pytest |
| `agentic-workflows-v2/ui/` | — | Vitest + React Testing Library |

---

## Pre-commit Hooks

Tools: **black** (v26.1.0), **isort** (v7.0.0), **ruff** (v0.15.0), **docformatter** (v1.7.7), **mypy** (v1.19.1), **pydocstyle** (v6.3.0).

Run: `pre-commit run --all-files`

---

## Gotchas & Common Issues

- **Windows paths:** Use forward slashes in Python code. `pathlib.Path` handles cross-platform automatically.
- **pytest-asyncio mode:** Tests use `asyncio_mode = "auto"` — all async test functions run without `@pytest.mark.asyncio`.
- **Adapter imports:** LangChain adapter is optional. Guard imports with `try/except ImportError` — don't make it a hard dependency.
- **Port conflicts:** Backend uses 8010, frontend uses 5173. Check for conflicts before starting dev servers.
- **Contract changes:** `contracts/` models are additive-only. Never remove or rename fields — downstream consumers depend on the schema.
- **Tool safety:** Built-in tools default to DENY for high-risk operations (shell, git, file_delete). Explicitly allowlist per workflow step.
- **Pydantic v2:** The codebase uses Pydantic v2. Use `model_dump()` not `.dict()`, `model_validate()` not `.parse_obj()`.
- **Import style:** Never use `sys.path` hacks. Use proper package imports: `from tools.llm import LLMClient`.

---

## Workflow & Agent Authoring

- **YAML steps** must have: `name`, `agent`, `description`, `depends_on`, `inputs`, `outputs`.
- **Personas** in `agentic_v2/prompts/*.md` must define: Expertise, Boundaries, Critical rules, Output format.
- **Tools** are allowlisted per step. Default DENY for high-risk tools.

---

## Evaluation Framework

- **Rubrics:** 8 YAML definitions (default, agent, code, coding_standards, pattern, prompt_pattern, prompt_standard, quality).
- **Evaluators:** base, LLM, pattern, quality, standard.
- **Runners:** BatchRunner, StreamingRunner, AsyncStreamingRunner.
- **LLM Judge:** `tools/agents/benchmarks/llm_evaluator.py` — 0.0–10.0 rubric scoring.
- **Research gating:** `coverage_score >= 0.80`, `source_quality_score >= 0.80`.

---

## Research Standards

- **Tier A (always):** Official docs, peer-reviewed papers, arXiv (known groups).
- **Tier B (conditional):** High-quality engineering blogs, Stack Overflow (high votes).
- **Tier C (blocked):** Unverified blogs, marketing materials.
- **Citations required:** `[Claim] (Source: Title, Publisher, Date — URL)`.
- **Critical claims:** >= 2 independent Tier A sources for architectural decisions.
