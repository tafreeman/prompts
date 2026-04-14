# Performance Audit — 2026-04-14

**Git SHA (audit):** 0252c88ce93792d05d13613e0b1f431d3193d006
**Git SHA (after fixes):** 7f1ae0f
**Status:** ⚠️ Issues Found (M-3 resolved)

## Implementation Status (2026-04-14)

| Finding | Status | Commit |
|---------|--------|--------|
| H-1 — Sync `open()` in async FastAPI handlers | Open — Strategic item S-1 | — |
| H-2 — `time.sleep()` in sync callees of async callers | Open — Strategic item S-1 | — |
| H-3 — `subprocess.run()` in LangChain `@tool` | Open — Strategic item S-1 | — |
| M-1 — `RunLogger.summary()` O(N) disk scan | Open | — |
| M-2 — `InMemoryVectorStore.search()` O(N) full scan | Open — Strategic item S-11 | — |
| M-3 — `load_workflow_config()` re-parses YAML on every call | ✅ Fixed: `@lru_cache(maxsize=128)` + cache invalidation on workflow save + test isolation fixture | `9cc4003` + `34294c5` |
| M-4 — 81 eager f-string log calls in MCP subsystem | Open — Strategic item S-12 | — |
| M-5 — `FileTraceAdapter` opens file per event | Open | — |

---

## Findings

### Critical

_No critical (production-blocking) issues found._

---

### High

#### H-1 — Sync `open()` in async FastAPI route handlers (blocks event loop)

Two server-side routes call synchronous `open()` / `Path.open()` directly inside (or in callees of) async route handlers, blocking the uvicorn event loop for the duration of the disk I/O:

| File | Caller context | Pattern |
|------|---------------|---------|
| `server/routes/agents.py:46` | `async def list_agents()` calls `_discover_agents()` which does `open(_AGENTS_CONFIG_PATH)` | sync YAML read on every request (no caching) |
| `server/datasets.py:114` | Called from `async def list_evaluation_datasets()` via `_load_eval_config()` which does `_EVAL_CONFIG_PATH.open("r")` | sync YAML read on every request (no caching) |

**Fix:** Use `asyncio.to_thread(pathlib.Path.read_text, ...)` or `aiofiles` to avoid blocking the event loop. Additionally, both files re-read static YAML on every request — apply `@lru_cache` or `functools.cache` to the load function since these files change only at deploy time.

---

#### H-2 — `time.sleep()` inside blocking sync functions called from async callers (`tools/`)

Three sync functions in `tools/llm/` use `time.sleep()` for retry back-off and are called from the `LLMClient.generate_text()` dispatcher, which itself can be invoked from async contexts via `asyncio.to_thread` or directly:

| File | Lines | Context |
|------|-------|---------|
| `tools/llm/probe_config.py:340` | `time.sleep(delay)` in retry loop | Called synchronously |
| `tools/llm/provider_adapters.py:338,354` | `time.sleep(wait_time)` / `time.sleep(base_delay)` in `call_github_models()` | Called from `LLMClient.generate_text()` |
| `tools/core/tool_init.py:454` | `time.sleep(current_delay)` in retry loop | Called synchronously |

If any of these callees are ever invoked inside an async function without `asyncio.to_thread`, they will stall the event loop for the full sleep interval. The GitHub Models adapter (`call_github_models`) uses `subprocess.run` internally (inherently blocking) and is not run via `asyncio.create_subprocess_exec` or `to_thread`.

**Fix:** Either keep these purely sync and ensure callers always use `asyncio.to_thread()`, or convert the retry loops to use `asyncio.sleep()` and make them `async def`.

---

#### H-3 — `subprocess.run()` inside a `@tool`-decorated sync function (`langchain/tools.py:225`)

`shell_run()` in `agentic_v2/langchain/tools.py` calls `subprocess.run(...)` (blocking). LangChain tools invoked inside an async agent loop will block the event loop for the full subprocess duration. There is no `asyncio.create_subprocess_exec` alternative.

**Fix:** Wrap with `asyncio.to_thread(subprocess.run, ...)` or replace with `asyncio.create_subprocess_exec` and `await proc.communicate()`.

---

#### H-4 — `_discover_agents()` / `_load_eval_config()` read disk on every request — no caching

These functions re-parse YAML from disk on every API call to `/api/agents` and `/api/eval/datasets`. With high request rates this translates directly to unbounded disk I/O and YAML parsing CPU cost.

**Fix:** Cache parsed results with `@functools.lru_cache(maxsize=1)` and add a `Cache-Control` header on the response. Invalidate cache on process restart (acceptable given static config files).

---

### Medium

#### M-1 — `summary()` in `RunLogger` loads every run file from disk on each call (unbounded N+1)

`run_logger.summary()` calls `list_runs()` which enumerates all JSON files in the `runs/` directory, then reads and parses every one sequentially:

```python
# run_logger.py:195-199
for path in runs:
    record = self.load_run(path)   # read_text + json.loads per file
```

The `/api/runs/summary` endpoint calls this on every request with no limit or caching. As the `runs/` directory grows (long-lived deployments), this becomes an O(N) disk scan on every request.

**Fix:** Maintain an in-memory aggregate summary that is updated incrementally when new runs are logged (`log_run()` already has a write path). Cache the result with a short TTL (e.g., 5 s) or invalidate on write.

---

#### M-2 — `InMemoryVectorStore.search()` is O(N) — full linear scan on every query

`agentic_v2/rag/vectorstore.py:108-119` iterates over every stored embedding on each search call:

```python
for entry in entries_snapshot:
    similarity = _cosine_similarity(query_embedding, entry.embedding)
```

For small corpora this is acceptable, but the code is also used in production flows where corpus size may grow. Additionally, `_cosine_similarity` re-computes the L2 norm of each stored vector on every search rather than pre-computing and caching norms at `add()` time.

**Fix (short-term):** Pre-compute and store the norm of each embedding at `add()` time to avoid redundant `math.sqrt(sum(...))` calls. **Fix (long-term):** Upgrade to `LanceDBVectorStore` for non-trivial workloads, which is already implemented and uses native ANN indexing.

---

#### M-3 — `load_workflow_config()` re-reads and re-parses YAML on every call — no caching

`langchain/config.py:135-150` calls `_parse_file(path)` (YAML load + Pydantic validation) with no memoization. Every route that calls `load_workflow_config()` — including `GET /workflows/{name}/dag`, `GET /workflows/{name}/capabilities`, and `POST /run` — parses the file from scratch. These are static files that rarely change.

**Fix:** Add `@functools.lru_cache(maxsize=64)` keyed on the resolved path string, with invalidation on `PUT /workflows/{name}` (the editor save route).

---

#### M-4 — Excessive f-string interpolation in `logger.debug/info` calls (81 occurrences)

The MCP integration subsystem (`integrations/mcp/`) contains 81 `logger.debug(f"...")` / `logger.info(f"...")` calls that eagerly evaluate string interpolation at call time regardless of whether the log level is active. In hot paths (tight retry loops, per-tool invocations), this creates unnecessary allocations.

**Fix:** Replace with `logger.debug("msg %s", val)` lazy format strings. Ruff rule `G004` (`logging-f-string`) detects these automatically — enable it in `pyproject.toml`.

---

#### M-5 — `FileTraceAdapter._flush()` opens the file on every event (no buffering by default)

`integrations/tracing.py:73` opens and closes the trace file on every flush. The default `buffer_size=1` means every single trace event results in a file `open()` + `write()` + `close()` syscall sequence:

```python
with open(self.file_path, "a", encoding="utf-8") as f:
    for line in self._buffer:
        f.write(line + "\n")
```

In a workflow with many steps emitting many events, this can add significant latency.

**Fix:** Increase `buffer_size` default to at least 10–20 events, or keep the file handle open for the lifetime of the adapter.

---

### Low

#### L-1 — `asyncio.run()` used in `adapters/native/engine.py:159` from a potentially mixed context

`NativeExecutionEngine.resume_from_checkpoint()` (line 159) calls `asyncio.run(self._checkpoint_store.read(...))` in the non-running-loop code path. If this method is ever called from within an async context (even indirectly), it will raise `RuntimeError: This event loop is already running`. The same function guards against this with `concurrent.futures` when a loop is detected (lines 155-157), but the code path for the non-loop case uses `asyncio.run()` which could conflict on platforms with custom event loop policies.

**Severity:** Low — only triggered outside the server context. Document the expected call context.

---

#### L-2 — `loop.run_until_complete()` in `integrations/langchain.py` spawns a new event loop per call

Three sync wrappers in `integrations/langchain.py` (lines 107, 185, 234) each create a new `asyncio.new_event_loop()`, run it, and close it. Under concurrent load, this means N threads each creating their own event loop. While functionally correct, it prevents sharing connection pools or other async resources across calls.

**Severity:** Low — only affects the LangChain sync compatibility path. Acceptable if the sync bridge is rarely used.

---

#### L-3 — `requests.get()` in `tools/llm/check_provider_limits.py` (6 calls) is purely synchronous

Six `requests.get()` calls exist in `tools/llm/check_provider_limits.py`. This module is a CLI utility and does not appear to be called from async routes — confirmed by inspection. No remediation required for async correctness, but noted as a future migration target if the health-check endpoint becomes part of the async server.

---

#### L-4 — `BM25Index.search()` iterates all documents on every query (no inverted-index lookup)

`rag/retrieval.py:112-115` scores every document for every query:

```python
for doc_idx in range(self._n_docs):
    score = self._score_document(query_tokens, doc_idx)
```

A standard BM25 implementation uses the inverted index to skip documents that contain none of the query terms. For large corpora this is a significant efficiency gap.

**Fix (medium effort):** Build a term→doc_idx posting list at index time, iterate only docs that contain at least one query token.

---

## Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Total Python files audited | 249 | 185 in `agentic_v2/`, 64 in `tools/` |
| `async def` functions in `agentic_v2/` | 31 across 14 files | Async surface is appropriate |
| `time.sleep()` in sync callees | 4 occurrences | `tools/` only; no occurrences in `agentic_v2/` |
| `requests.get/post` calls | 6 occurrences | `tools/llm/check_provider_limits.py` only (CLI util) |
| `subprocess.run` calls | 1 occurrence | `langchain/tools.py` — sync tool called from async agent |
| `asyncio.run()` inside application code | 8 occurrences | CLI helpers (acceptable) + 1 in `adapters/native/engine.py` |
| `loop.run_until_complete()` | 3 occurrences | `integrations/langchain.py` sync bridge |
| f-string logger calls | 81 | MCP subsystem (14 files) |
| Files using `@lru_cache` / `@cache` | 1 | `prompts/__init__.py` only |
| `open()` in async route callee | 2 | `routes/agents.py`, `server/datasets.py` |
| RAG vectorstore type | `InMemoryVectorStore` (default) | O(N) scan; `LanceDBVectorStore` available but not default |
| Embedding cache present | No | No deduplication layer in the embedding call path |

---

## Recommendations

1. **Enable `ruff` rule `G004`** (`logging-f-string`) in `pyproject.toml` to automatically detect and auto-fix the 81 f-string logger calls across the MCP subsystem. This is a zero-risk, zero-effort win via `ruff check --fix`.

2. **Cache `load_workflow_config()`, `_discover_agents()`, and `_load_eval_config()`** with `@functools.lru_cache(maxsize=...)`. These parse static YAML on every API request. A one-line decorator per function eliminates redundant I/O and parsing under load.

3. **Wrap `_discover_agents()` YAML read with `asyncio.to_thread()`** so it does not block the uvicorn event loop. Apply the same pattern to `_load_eval_config()`.

4. **Pre-compute L2 norms in `InMemoryVectorStore.add()`** to avoid re-computing them on every `search()` call. This is a 1-2 line change that eliminates O(D) redundant work per search where D is embedding dimension (default 384).

5. **Add an inverted-index lookup to `BM25Index.search()`** — build a `term → list[doc_idx]` posting map at `add()` time. Candidate document set becomes the union of postings for each query token, reducing per-query work from O(N·|query|) to O(postings·|query|).

6. **Add incremental `RunLogger.summary()` caching** — update an in-memory aggregate whenever `log_run()` is called so `GET /api/runs/summary` does not scan the entire `runs/` directory on each request.

7. **Increase `FileTraceAdapter` default `buffer_size`** from 1 to at least 16 events, or keep the file handle open for the adapter's lifetime to avoid per-event `open()`/`close()` overhead.

8. **Convert `call_github_models()` and its retry loops** to either: (a) always call via `asyncio.to_thread()` from async contexts, or (b) rewrite as `async def` using `asyncio.create_subprocess_exec` and `asyncio.sleep()`. Document the contract clearly if option (a) is chosen.
