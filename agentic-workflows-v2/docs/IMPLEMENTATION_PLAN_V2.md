# Implementation Plan v2 - Migration & Module Expansion

**Status:** ✅ PHASE 2D COMPLETE  
**Created:** February 3, 2026  
**Updated:** February 4, 2026  
**Based On:** Industry Architecture Research (AutoGen, LangGraph, CrewAI, OpenAI Agents SDK, MS Agent Framework)

### Progress Summary

- **Tests:** 370+ passing (as of Feb 4, 2026)
- **Agents:** ArchitectAgent, TestAgent migrated
- **Prompts:** 13 templates migrated with loader utility
- **Configs:** agents.yaml, models.yaml, evaluation.yaml migrated
- **Workflows:** 3 definitions in place
- **Tools:** 5 new tool categories added (Git, HTTP, Shell, CodeAnalysis, Search)
- **Memory/Context:** Token-aware `ConversationMemory` + persistent memory/context builtin tools

---

## 📋 Overview

This plan covers migrating missing components from the original `multiagent-workflows/` source and establishing the final module architecture based on industry best practices.

### Architecture Decision Summary

| Decision | Rationale |
|----------|-----------|
| **Agents + Workflows = Same Package** | Industry consensus - tightly coupled |
| **Evaluation = Separate Package** | Optional, different dependencies |
| **Server = Optional Install** | `pip install agentic-v2[server]` |
| **Tools = Same Package** | Core functionality needed |
| **Tests = Same Repo** | Standard Python convention |

---

## 🎯 Phase 2A: Component Migration (From Original Source)

### Priority 1: Missing Agents

| Agent | Source | Target | Status |
|-------|--------|--------|--------|
| `ArchitectAgent` | `multiagent-workflows/src/.../agents/architect_agent.py` | `agentic_v2/agents/architect.py` | ✅ Done |
| `TestAgent` | `multiagent-workflows/src/.../agents/test_agent.py` | `agentic_v2/agents/test_agent.py` | ✅ Done |

> **Tests:** 36 new tests added in `tests/test_new_agents.py` - All passing (341 total)

### Priority 2: Prompt Templates (13 files)

> **Status: ✅ COMPLETE** - 13 prompts migrated with loader utility

| Prompt | Source | Target | Status |
|--------|--------|--------|--------|
| `analyst.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `architect.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `coder.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `debugger.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `judge.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `planner.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `reasoner.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `researcher.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `reviewer.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `tester.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `validator.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `vision.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |
| `writer.md` | `multiagent-workflows/config/prompts/` | `agentic_v2/prompts/` | ✅ Done |

**Utilities Added:**

- `prompts/__init__.py` with `load_prompt()`, `list_prompts()`, `get_prompt_path()`
- Prompt name constants for autocompletion

### Priority 3: Workflow Definitions (5 files)

> **Status: ✅ PARTIAL** - 3 workflows in place, configs migrated

| Workflow | Description | Status |
|----------|-------------|--------|
| `code_review.yaml` | Code review workflow | ✅ Already exists |
| `fullstack_generation.yaml` | Full development cycle | ✅ Already exists |
| `plan_implementation.yaml` | Iterative implementation workflow | ✅ Migrated |

### Priority 4: Configuration Files

> **Status: ✅ COMPLETE**

| Config | Description | Status |
|--------|-------------|--------|
| `agents.yaml` | Agent definitions | ✅ Migrated to `config/defaults/` |
| `models.yaml` | Model configurations | ✅ Migrated to `config/defaults/` |
| `evaluation.yaml` | Evaluation settings | ✅ Migrated to `config/defaults/` |

---

## 🎯 Phase 2B: Evaluation Module (Separate Package)

Based on industry patterns, evaluation should be a **separate optional package**.

### Structure: `agentic-v2-eval/`

```
agentic-v2-eval/
├── pyproject.toml
├── README.md
├── src/agentic_v2_eval/
│   ├── __init__.py
│   ├── scorer.py           # Scoring framework
│   ├── metrics/
│   │   ├── accuracy.py     # Accuracy metrics
│   │   ├── quality.py      # Code quality metrics
│   │   └── performance.py  # Execution metrics
│   ├── rubrics/
│   │   └── default.yaml    # Evaluation rubrics
│   ├── runners/
│   │   ├── batch.py        # Batch evaluation runner
│   │   └── streaming.py    # Streaming evaluation
│   └── reporters/
│       ├── json.py         # JSON output
│       ├── markdown.py     # Markdown reports
│       └── html.py         # HTML dashboards
└── tests/
    └── test_eval.py
```

| Component | Description | Status |
|-----------|-------------|--------|
| Scorer Framework | Port from original `evaluation/scorer.py` | ⬜ Todo |
| Rubric System | YAML-based evaluation rubrics | ⬜ Todo |
| Batch Runner | Run evals across test datasets | ⬜ Todo |
| Reporters | JSON, Markdown, HTML output | ⬜ Todo |

---

## 🎯 Phase 2C: Server Module (Optional Install)

### Option 1: Install Extra (Recommended)

Add to `pyproject.toml`:

```toml
[project.optional-dependencies]
server = [
    "fastapi>=0.100.0",
    "uvicorn>=0.23.0",
    "websockets>=11.0",
]
```

### Structure: `agentic_v2/server/`

```
src/agentic_v2/server/
├── __init__.py
├── app.py              # FastAPI application
├── routes/
│   ├── workflows.py    # Workflow endpoints
│   ├── agents.py       # Agent endpoints
│   └── health.py       # Health checks
├── models.py           # API request/response models
└── websocket.py        # Real-time streaming
```

| Component | Description | Status |
|-----------|-------------|--------|
| FastAPI App | REST API for workflows | ✅ Done |
| Workflow Routes | Execute/list/validate workflows | ✅ Done |
| Agent Routes | Run agents, get capabilities | ✅ Done |
| WebSocket | Real-time execution streaming | ✅ Done |

---

## 🎯 Phase 2D: Enhanced Tools

### Additional Builtin Tools

| Tool | Description | Tier | Status |
|------|-------------|------|--------|
| `GitTool` | Git operations (status, diff, commit) | 0 | ✅ Done |
| `HttpTool` | HTTP requests (GET, POST, etc.) | 0 | ✅ Done |
| `ShellTool` | Execute shell commands | 0 | ✅ Done |
| `CodeAnalysisTool` | AST parsing, complexity | 1 | ✅ Done |
| `SearchTool` | Semantic search in files | 2 | ✅ Done |

**Implementation Details:**

- **Git Operations** (`git_ops.py`):
  - `GitTool`: Main tool with support for status, diff, log, add, commit, branch commands
  - `GitStatusTool`: Convenience wrapper for git status
  - `GitDiffTool`: Convenience wrapper for git diff
  
- **HTTP Operations** (`http_ops.py`):
  - `HttpTool`: Full HTTP client with GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
  - `HttpGetTool`: Convenience wrapper for GET requests
  - `HttpPostTool`: Convenience wrapper for POST requests with JSON body
  
- **Shell Execution** (`shell_ops.py`):
  - `ShellTool`: Execute shell commands with security controls (blocks dangerous operations)
  - `ShellExecTool`: Execute commands with automatic argument escaping
  
- **Code Analysis** (`code_analysis.py`):
  - `CodeAnalysisTool`: Analyze Python code for metrics (lines, functions, classes, imports, complexity)
  - `AstDumpTool`: Generate AST dumps for detailed structure analysis
  
- **Search Operations** (`search_ops.py`):
  - `SearchTool`: Multi-mode search (regex, fuzzy, semantic) with recursive directory support
  - `GrepTool`: Quick grep-like pattern matching

**Test Coverage:** 28 new tests covering all tools and edge cases (100% pass rate)

---

## 🧠 Post-2D: Memory & Context Utilities

While working through Phase 2D, we also hardened the agent memory and added deterministic context helpers.

- **Token-aware conversation memory:** `ConversationMemory` now trims to a *message budget* and an *approximate token budget* (`AgentConfig.max_memory_messages`, `AgentConfig.max_memory_tokens`).
- **Persistent memory tools:** Built-in CRUD tools backed by a JSON file.
  - Configure the storage location with `AGENTIC_MEMORY_PATH`.
- **Context utilities:** `token_estimate` + `context_trim` helpers for predictable context shaping.

---

## 🎯 Phase 2E: Documentation & Polish

| Task | Description | Status |
|------|-------------|--------|
| API Reference | Auto-generated from docstrings | ✅ Done |
| Tutorials | Step-by-step guides (kept in sync with public API) | 🚧 In progress |
| README | Quick start + current CLI/Python examples | 🚧 In progress |
| Examples | Real-world usage examples | ✅ Done |
| Architecture Docs | ADRs, design decisions | ✅ Done |

---

## 📊 Progress Tracker

### Phase 2A: Migration

- [ ] Architect Agent
- [ ] Test Agent  
- [ ] 13 Prompt Templates
- [ ] 5 Workflow Definitions
- [ ] 3 Config Files

### Phase 2B: Evaluation Package

- [ ] Project structure
- [ ] Scorer framework
- [ ] Rubric system
- [ ] Reporters

### Phase 2C: Server Module

- [x] FastAPI integration
- [x] Workflow routes
- [x] WebSocket streaming

### Phase 2D: Tools

- [x] Git operations
- [x] HTTP requests
- [x] Shell execution

### Phase 2E: Documentation

- [x] API reference
- [x] Tutorials
- [x] Examples

---

## 🔍 Refinement: Issues & Ideas Assessment (Feb 4, 2026)

Critical review of the evaluation migration plan identified duplications and coupling risks.

### Identified Issues

1. **Three overlapping Scorers**: `tools/prompteval/unified_scorer`, `multiagent-workflows/.../scorer`, and `agentic-v2-eval/scorer` have conflicting interfaces.
2. **LLMClientProtocol mismatch**: `llm.py` defines a protocol, but `agentic-workflows-v2` uses a different client structure.
3. **Sandbox is Docker-only**: Blocks local development; need `LocalSubprocessSandbox`.
4. **Benchmark code stranded**: Code remains in `tools/agents/benchmarks`, creating import risks.
5. **No tests for loader**: Benchmark loader lacks unit tests.
6. **Pattern scorer coupled**: Tightly coupled to `tools.llm.llm_client`.
7. **Rubrics external**: Depends on files in `rubrics/` outside the package.
8. **No CI**: Evaluation tests not in CI.

### Refined Prioritization

| Priority | Task | Rationale |
|----------|------|-----------|
| **P0** | **Sandbox (Local)** | Unblocks dev execution. |
| **P0** | **Benchmark Tests** | Ensures data reliability. |
| **P1** | **LLM Protocol** | Unifies model access. |
| **P1** | **Move Benchmarks** | Fixes architecture/imports. |
| **P2** | **Merge Scorers** | Unified Scoring API. |
| **P2** | **Decouple Pattern Scorer** | Clean dependencies. |
| **P3** | **Rubrics/CI** | Polish/Integration. |

> **Current Focus:** Implementing **P2** (Merge Scorers & Decouple Pattern Scorer) as requested.

---

## 🏗️ Target Architecture (Post-Phase 2)

```
agentic-workflows-v2/
├── src/agentic_v2/           # Main package
│   ├── agents/               # All agents (7+)
│   ├── cli/                  # CLI commands
│   ├── config/               # YAML configs
│   ├── contracts/            # Pydantic schemas
│   ├── engine/               # DAG execution
│   ├── models/               # LLM routing
│   ├── prompts/              # Agent prompts (13+)
│   ├── server/               # Optional REST API
│   ├── tools/                # Builtin tools (18+)
│   └── workflows/            # Definitions (7+)
├── tests/                    # ~350+ tests
├── pyproject.toml            # With [server], [dev] extras
└── README.md

# Separate Package (Optional)
agentic-v2-eval/              # Evaluation framework
├── src/agentic_v2_eval/
└── tests/
```

---

## 📈 Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Tests | 369 | 400+ |
| Agents | 4 | 7+ |
| Workflows | 2 | 7+ |
| Tools | 18 | 18+ ✅ |
| Prompts | 0 | 13+ |
| Documentation | Basic | Full API docs |

---

## 🔗 References

- [AutoGen Architecture](https://github.com/microsoft/autogen) - Layered packages
- [LangGraph](https://github.com/langchain-ai/langgraph) - Graph-based workflows
- [CrewAI](https://github.com/crewAIInc/crewAI) - Crews + Flows pattern
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) - Minimal core
- [MS Agent Framework](https://github.com/microsoft/agent-framework) - Multi-package mono-repo

---

**Next Action:** Start with Phase 2A Priority 1 (Missing Agents)
