# Improvement Plan Tracker

Branch: `claude/laughing-einstein` | Started: 2026-03-11

## Completed Commits

| # | Commit | Message | Files |
|---|--------|---------|-------|
| C1 | `80730dc5` | ci: raise coverage gate to 80%, add mypy and bandit CI jobs | 1 |
| C2+C3 | `9edaf7da` | refactor: extract execution engine, evaluation routes, and result normalization from workflows.py | 6 |
| C4 | `ee949ea6` | refactor: decompose agent_resolver into output parsing, prompt assembly, and tool execution | 5 |
| C5 | `626391aa` | refactor: extract agent memory and config types from base.py | 4 |
| C6 | `75b2db3f` | refactor: split LLM backends into cloud and local provider modules | 4 |
| C7 | `a2cc03a6` | refactor: extract model builder functions and provider utilities from langchain models | 4 |
| C8 | `f20b37d7` | refactor: extract CLI display helpers and RAG commands from main.py | 4 |
| C9a | `5351cf6e` | refactor: extract run history routes and result builder into separate modules | 4 |
| C9b | `3ce1b9d0` | refactor: extract graph wiring from langchain graph module | 3 |
| C10 | — | Trim 600-line files (achieved via C2–C9 splits; all targets under 550L) | 0 |
| C11 | `64e961f9` | refactor: migrate 279 Optional/Union annotations to PEP 604 syntax | 51 |
| C12 | `ce031782` | refactor: replace print statement with structured logging in tool registry | 1 |
| C13 | `82eea53b` | refactor: replace print statements with structured logging in tools/core and tools/llm | 13 |
| C14a | `23ce09d0` | docs: fix stale test file count in CLAUDE.md (66 to 72) | 1 |
| C14b | `37a08cbb` | docs: add .claude directory guide with commands, contexts, rules, and skills reference | 1 |
| C15 | `5592bebd` | feat: add YAML workflow execution and custom tool implementation examples | 3 |

**Total: 15 commits, ~105 files changed**

---

## Remaining Work

### C16 — RAG reranking module (new feature)
**Priority:** Medium | **Effort:** Large | **Model:** opus

Add `RerankerProtocol` to `core/protocols.py` and create `rag/reranking.py` with three implementations:
- `CrossEncoderReranker` — uses cross-encoder models (sentence-transformers), guard import with try/except
- `LLMReranker` — uses an LLM to score relevance
- `NoOpReranker` — passthrough for testing/baseline

Wire optional reranking into `HybridRetriever` in `rag/retrieval.py`. Add config fields to `rag/config.py`.

**Tests:** Unit tests for each implementation + integration test with HybridRetriever. Target >= 80% coverage on new code.

**Files to create/modify:**
- `agentic_v2/core/protocols.py` — add `RerankerProtocol`
- `agentic_v2/rag/reranking.py` — NEW (3 implementations)
- `agentic_v2/rag/config.py` — add reranker config fields
- `agentic_v2/rag/retrieval.py` — wire optional reranking into `HybridRetriever`
- `tests/test_reranking.py` — NEW

---

### C17 — Protocol conformance test suite
**Priority:** Medium | **Effort:** Medium | **Model:** sonnet

Create `tests/test_protocol_conformance.py` asserting `isinstance(impl, Protocol)` for all known implementations of the 6 protocols in `core/protocols.py`:
- `ExecutionEngine`
- `AgentProtocol`
- `ToolProtocol`
- `MemoryStore`
- `SupportsStreaming`
- `SupportsCheckpointing`

Fix protocol declarations on `ClaudeSDKAgent` and `LangChainEngine` if needed.

**Files to create/modify:**
- `tests/test_protocol_conformance.py` — NEW
- Possibly `agents/implementations/claude_sdk_agent.py`, `langchain/engine.py` — protocol fixes

---

### C18 — Conditional branching and iterative workflow YAML examples
**Priority:** Low | **Effort:** Small | **Model:** haiku

Create two example YAML workflow definitions:
- `examples/conditional_branching.yaml` — demonstrates `when:` conditional gates
- `examples/iterative_review.yaml` — demonstrates `loop_until:` iterative patterns

Update `examples/README.md` to list these.

**Files to create:**
- `agentic_v2/workflows/definitions/conditional_branching.yaml` — NEW
- `agentic_v2/workflows/definitions/iterative_review.yaml` — NEW
- `examples/README.md` — update

---

### C19 — Split oversized tools/ files (stretch)
**Priority:** Low | **Effort:** Medium | **Model:** sonnet

Split two oversized files:
- `tools/llm/local_model.py` (851L) → core class + discovery module
- `tools/agents/benchmarks/llm_evaluator.py` (780L) → rubric logic + orchestration

---

### C20 — Remaining ruff violations + integration CI (stretch)
**Priority:** Low | **Effort:** Small | **Model:** haiku

Run `ruff check --fix` for remaining deferred rules. Add an integration-test job to `.github/workflows/ci.yml`.

---

## Plan Reference

Full original plan: `~/.claude/plans/agile-shimmying-beacon.md`
