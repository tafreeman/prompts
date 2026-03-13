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
| C16a | `b3bf74e9` | feat: add RerankerProtocol and RerankerConfig | 3 |
| C16b | `7513de79` | feat: add reranking implementations (NoOp, CrossEncoder, LLM) | 2 |
| C16c | `002971bc` | feat: wire optional reranker into HybridRetriever | 2 |
| C17 | `a9d2cd52` | test: add protocol conformance tests for RAG, Agent, Tool, and Memory | 1 |
| C19a | `0a645ddd` | refactor: split tools/llm oversized files into focused modules | 9 |
| C19b | `b244d301` | refactor: split tools/agents/benchmarks oversized files | 7 |
| C19c | `f2136619` | refactor: split tools/research/build_library.py into focused modules | 2 |
| C19-cleanup | `46147dda` | refactor: remove duplicate constants and convert print to logging in tools/llm | 2 |
| C18 | `6ac26971` | feat: add conditional branching and iterative review YAML workflow examples | 3 |
| C20 | `1711be25` | ci: fix ruff violations and add integration-test CI job | 16 |

**Total: 25 commits, ~152 files changed** | PR #95 (C1–C15), PR #97 (CI fix), PR #98 (C16–C19), PR #99 (C18, C20)

---

## All Backlog Items Complete

All planned improvement items (C1–C20) have been implemented and committed.

---

## Plan Reference

Full original plan: `~/.claude/plans/agile-shimmying-beacon.md`
