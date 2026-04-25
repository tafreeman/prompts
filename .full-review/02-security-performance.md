# Phase 2: Security & Performance Review

## Scope Calibration (Local-Only Learning Platform)

This project runs on developer workstations, not production. Priorities below are **re-ranked** accordingly:

**Still Critical locally** (agent-driven prompt injection → local tool execution):
- Sec C1 Shell blocklist bypass — agent can damage dev's machine/files
- Sec C2 Sanitization fail-open — same path, local blast radius
- Sec H3 `file_ops` path traversal — agent can read any file the dev can
- Sec H4 Eval expression injection — sandbox escape
- Sec H5 Code execution sandbox escape — same
- Sec H6 Subprocess env leaks API keys to untrusted code — agent exfil to its own LLM or file

**Downgraded to Low / Informational** (production concerns, not applicable to localhost-only use):
- Sec H1 CORS `allow_credentials` defaults → Informational
- Sec H2 API key default-open → Informational (localhost is the trust boundary)
- Sec M1 SSE auth strategy → Informational
- Sec M2 WebSocket null-Origin → Informational
- Sec M3 GitHub Actions SHA-pinning → Low (supply-chain still matters but not critical here)
- Sec M4 JWT/rotation → Drop (no multi-user surface)
- Sec L1 Dockerfile `--reload` → Drop (dev target is fine for dev use)
- Sec L5 CSP/HSTS headers → Drop

**All Performance findings remain relevant** — they affect how the platform behaves when a team of 5–10 devs each runs workflows locally (concurrency, memory, vector-store latency). Only Perf C3 (horizontal scaling) is downgraded to Informational since `--workers 1` is appropriate for local use anyway.

## Summary

- **Security (2A):** 2 Critical, 6 High, 8 Medium, 5 Low
- **Performance (2B):** 3 Critical, 9 High, 11 Medium, 6 Low

---

## Security Findings (Phase 2A)

### Critical

**C1 — Shell tool bypasses block-list** — CWE-77/78, CVSS 9.1
`agentic-workflows-v2/agentic_v2/tools/builtin/shell_ops.py:63-171`. `ShellTool` uses `asyncio.create_subprocess_shell` with `shell=True` + substring blocklist. Trivial bypasses: `rm  -rf  /` (double space), `/usr/bin/curl http://attacker/`, `$(echo cu)$(echo rl) ...`, unicode fullwidth `ｃｕｒｌ`. **Fix:** Require env-driven allowlist via `shlex.split(cmd)[0] ∈ AGENTIC_SHELL_ALLOWED_COMMANDS` or delete `ShellTool` in favor of the argv variant `ShellExecTool`.

**C2 — Sanitization middleware fails open** — CWE-703/754, CVSS 8.2
`agentic_v2/server/middleware/__init__.py:60-63`. `except Exception: logger.exception(...); return await call_next(request)`. Any detector error (ReDoS, malformed unicode, oversized body) silently bypasses the entire sanitization chain. **Fix:** Return HTTP 500 on detector exception; narrow exception scope to body-decode only.

### High

- **H1 — CORS with `allow_credentials=True` and dev defaults** (CWE-942, CVSS 7.4). `server/app.py:120-127`, `server/auth.py:43-50, 130`. `is_websocket_origin_allowed` honors `*` even with credentials, bypassing browser-enforced CORS for WS path. **Fix:** Reject `*`; require explicit `AGENTIC_CORS_ORIGINS` in prod; log warning on defaults.
- **H2 — API key auth is opt-in; default deploy is public** (CWE-306, CVSS 8.6). `server/auth.py:66-72, 156-159`, `app.py:66-70`. When `AGENTIC_API_KEY` unset, middleware short-circuits — every endpoint public. `docker-compose.yml` doesn't set it. **Fix:** Require `AGENTIC_ALLOW_UNAUTHENTICATED=1` explicit override; otherwise refuse to start.
- **H3 — Path containment disabled without `AGENTIC_FILE_BASE_DIR`** (CWE-22, CVSS 8.6). `agentic_v2/tools/builtin/file_ops.py:15-32`; `.env.example:98` ships empty. With defaults, agent can `file_read("/etc/passwd")`, `file_write("/root/.ssh/authorized_keys")`. **Fix:** Fail-closed when var unset.
- **H4 — `eval()` for workflow `when` conditions** (CWE-95, CVSS 7.2). `engine/expressions.py:231-266`, `langchain/expressions.py:50-52`. Audit `_validate_ast` in `engine/expressions.py` — ensure `ast.Attribute`/`ast.Subscript`/`ast.Call` excluded. Add injection test. Consider `simpleeval` replacement.
- **H5 — Code execution sandbox bypass** (CWE-913/94, CVSS 7.5). `agentic_v2/tools/builtin/code_execution.py:106-207`. `_DANGEROUS_BUILTINS` defined but unused; `__import__` kept; `getattr(0, "__class__").__mro__[-1].__subclasses__()` reaches `subprocess.Popen`; string concat bypasses AST scan. **Fix:** Use external sandbox (Firejail/gVisor/Docker seccomp/Pyodide); remove `__import__`/`getattr`; `resource.setrlimit` caps.
- **H6 — Subprocess inherits full parent env (secret leak)** (CWE-532, CVSS 5.3). `code_execution.py:207, 223` uses `env={**os.environ, ...}` — untrusted code has access to `OPENAI_API_KEY`/`ANTHROPIC_API_KEY`/`GITHUB_TOKEN`. **Fix:** `env={"PATH": os.environ["PATH"], "PYTHONDONTWRITEBYTECODE": "1"}` for all child processes.

### Medium

- **M1** SSE stream `/api/runs/{run_id}/stream` — EventSource can't send custom headers; no signed-URL fallback wired. Document SSE auth strategy (first-party cookie or short-lived signed URLs).
- **M2** `auth.py:122-123` — `if origin is None: return True` trusts any non-browser client (curl, websockets). **Fix:** Require Origin or bearer token when `AGENTIC_API_KEY` is set.
- **M3** `.github/workflows/*.yml` use mutable tags (`@v6`, `@v7`); `actions/checkout@v6`/`download-artifact@v8` may not exist (current: v4/v5). **Fix:** Pin by full SHA.
- **M4** Single shared `AGENTIC_API_KEY`, no rotation/expiration/per-caller identity. **Fix:** Multi-key support `AGENTIC_API_KEY`/`AGENTIC_API_KEY_OLD`; long-term JWT.
- **M5** `server/routes/workflows.py:306` — caller-controlled `run_id` flows to `RunLogger` filesystem paths. **Fix:** Pydantic validator `^[a-zA-Z0-9_-]{1,64}$`.
- **M6** Silent exception swallow on LLM-output parse paths loses prompt-injection canaries. **Fix:** Typed `MalformedModelOutputError`.
- **M7** `integrations/mcp/results/storage.py:76, 124` — MD5 w/ `usedforsecurity=False` OK for dedup; migrate to SHA-256 for FIPS.
- **M8** Sanitization only runs on API requests — tool outputs (HTTP, file, MCP) re-enter context unsanitized. **Fix:** Process tool results through `response_sanitizer.py`.

### Low

- **L1** Dockerfile `--reload` in backend-dev target — separate `backend-prod` target.
- **L2** Auth failure logs lack structured fields — adopt `structlog`.
- **L3** Sensitive env inherited by `shell_ops`, `git_ops`, `code_execution` children — explicit `env=` everywhere.
- **L4** `ui/src/hooks/useTheme.ts` uses localStorage — clean; noted for completeness.
- **L5** No CSP/HSTS/X-Content-Type-Options/Referrer-Policy emitted. **Fix:** Small middleware.

### Security Strengths

1. `secrets.compare_digest` for API key (`auth.py:108`).
2. SSRF blocks: schemes, cloud metadata, RFC 1918 (`http_ops.py:21-61`).
3. Path-traversal helper `utils/path_safety.py:9-29` used consistently.
4. SPA fallback anti-traversal (`app.py:155-166`).
5. Query-string WS tokens explicitly rejected (`websocket.py:233-243`).
6. Sanitization pipeline architecture (classification taxonomy, detectors, NFKC, hashed audit).
7. AST-restricted expression evaluator excludes `ast.Attribute`/`Call`/`Subscript`.
8. `yaml.safe_load` everywhere; no `yaml.load`/`unsafe_load`.
9. Secret provider abstraction (`models/secrets.py`).
10. `detect-secrets` in pre-commit.
11. Ruff `S` (bandit) rules enabled.
12. `git_ops.py:61-71` uses allowlist (opposite of shell tool).
13. Evaluation JSON schema-based TS↔Py drift guard in CI.
14. Origin-vs-Host port/scheme normalization (`auth.py:209-225`).

---

## Performance Findings (Phase 2B)

### Critical

**C1 — Thread-pool-in-event-loop in `NativeEngine.get_checkpoint_state`** — concurrency/IO
`adapters/native/engine.py:144-164`. `ThreadPoolExecutor(max_workers=1) + asyncio.run()` per call. 100-1000× overhead; deadlock risk if store holds any caller-loop asyncio lock. **Fix:** Make `SupportsCheckpointing.get_checkpoint_state` async.

**C2 — Mutating `step_def.timeout_seconds` on shared dataclass** — concurrency
`engine/executor.py:371-373`. `StepDefinition` instances shared across concurrent runs; one request's `timeout=300` silently overwritten by another's default. **Fix:** Compute `effective_timeout` locally; pass as override.

**C3 — Stateful global singletons block horizontal scaling** — scalability
Eight module-globals (`_smart_router`, `_lc_runner`, `_global_cache`, `AdapterRegistry`, etc.) hold per-process mutable state. `uvicorn --workers N` gives N divergent copies; file-lock on `_save_stats` is only cross-worker sync. **Fix:** Redis-backed stats/bulkheads; until then document `--workers 1`.

### High

- **H1** `LLMClientWrapper.complete()` reimplements router fallback loop (125 lines); ignores rate-limit headers, skips bulkhead, skips half-open probe lock — 3× retry amplification on 429. `models/client.py:270-394`. **Fix:** Delegate to `router.call_with_fallback`.
- **H2** `InMemoryVectorStore.search` O(N·d) pure-Python cosine; 15M float mults per query at 10k × 1536. `rag/vectorstore.py:83-135, 163-179`. **Fix:** Numpy pre-normalized matrix + `matmul` + `argpartition` — 50-200× speedup.
- **H3** `BM25Index.search` scans every doc per query, even docs with no query-token match. `rag/retrieval.py:97-156`. **Fix:** Inverted posting lists or `rank_bm25`.
- **H4** Shared `self._engine_kwargs = kwargs` race in `WorkflowExecutor`. `engine/executor.py:214-215, 317`. **Fix:** Pass kwargs through call stack.
- **H5** `LangChainEngine.runner` lazy-init race — double construction possible; each is expensive graph compilation. `adapters/langchain/engine.py:62-70`. **Fix:** `asyncio.Lock` on first construct.
- **H6** `_save_stats` fires on every success/failure/timeout/rate-limit via cross-process `FileLock` + temp-rename. `models/smart_router.py:400-418`, called from 141/159/174/185. **Fix:** Debounce 5-10s; JSONL append-only; Redis backend for multi-worker.
- **H7** `StepExecutor` clones entire `steps` state dict per step. `engine/step.py:354-359`. Quadratic memory churn; lost-update race if `set_sync` non-transactional. **Fix:** Per-step keys `steps.<name>`; lazy expression resolution.
- **H8** `RunConfigForm.tsx` preview fetch has no `AbortController`; stacked in-flight requests race; last-resolver wins. `ui/src/components/runs/RunConfigForm.tsx:81-109`. **Fix:** `AbortController` + TanStack Query `useQuery`.
- **H9** `useRuns` polls every 5s unconditionally — background tabs, WebSocket already streaming. `ui/src/hooks/useRuns.ts:9-15`. **Fix:** `refetchIntervalInBackground: false`; invalidate on WS events.

### Medium

- **M1** SQLite checkpoint store opens fresh connection per call; no WAL, no `busy_timeout`, no pool. `adapters/native/_checkpoint_store.py:82-101`. **Fix:** WAL + `synchronous=NORMAL` + `busy_timeout=5000`.
- **M2** No secondary index on `workflow_name` in checkpoints table — future full-table scans.
- **M3** `_load_eval_config` re-reads YAML from disk per call; 3 calls per `/datasets` page load, blocking async loop. `server/datasets.py:104-118`. **Fix:** `lru_cache` by path+mtime.
- **M4** `list_local_datasets()` rglobs + JSON-parses every file on every request. `server/datasets.py:227-251`. **Fix:** Cache by (root, max_mtime).
- **M5** `InMemoryVectorStore.add` no content_hash dedup (LanceDB has it); re-ingest leaks memory. `rag/vectorstore.py:51-81`.
- **M6** `_merge_stream_state` rebuilds full dict per stream tick; no error dedup. `server/execution.py:100-143`. **Fix:** Merge only changed fields.
- **M7** `WebSocket.broadcast` serial per-connection; slow client blocks fast ones. `server/websocket.py:148-159`. **Fix:** `asyncio.gather(..., return_exceptions=True)`.
- **M8** `event_buffers[run_id]` never evicted; ~1 GB after 1000 runs. `server/websocket.py:198-204`. **Fix:** Clear in `finally:` of `_run_and_evaluate`; TTL reaper.
- **M9** `CachedResponse.age_seconds` recomputes per access; 1000 `datetime.now()` calls per over-capacity prune. `models/client.py:260-268`. **Fix:** `OrderedDict` + `popitem(last=False)`.
- **M10** `InMemoryStore.search` O(N) substring scan; unbounded growth; no TTL. `core/memory.py:174-212`. **Fix:** Mark test-only; or cap+LRU.
- **M11** `ResponseCache` hit_count updates never persisted without explicit save. `tools/core/response_cache.py:215-278`. **Fix:** Periodic flush.

### Low

- **L1** Sanitization middleware instantiation cost even when disabled; ensure `sanitization=None` default.
- **L2** Gemini `x-goog-api-key` passed per-call header; move to `AsyncClient.headers`. `backends_cloud.py:408-409`.
- **L3** `dense_only` single-query embed: 10 searches = 10 provider round-trips. `rag/retrieval.py:299-312`.
- **L4** `_cosine_similarity` per-entry (duplicate of H2).
- **L5** `@xyflow/react` (200+ KB gzip) not code-split; downloaded on first page load. `ui/vite.config.ts`. **Fix:** `React.lazy` + `manualChunks`.
- **L6** `ConnectionManager` uses list with O(n) remove; use dict/set. `server/websocket.py:100-104, 193-196`.

### Performance Strengths

1. `CheckpointStore` and LanceDB store offload sync I/O via `asyncio.to_thread` — event loop never blocked.
2. `deque(maxlen=500)` for event replay buffers — O(1) eviction.
3. Pagination in dataset APIs avoids O(N²) re-read.
4. DAG executor uses `asyncio.wait(FIRST_COMPLETED)` — max parallelism.
5. Per-provider bulkhead semaphores (`smart_router.py:120-126`) with sane defaults.
6. Atomic stats write with `filelock` + temp-rename (correct semantics, wrong frequency).
7. RRF fusion O(k·L), shared chunk_id dict (`retrieval.py:185-214`).
8. `InMemoryVectorStore._entries` snapshot-before-iterate — safe under concurrent add.
9. LanceDB vector store dedupes by `content_hash`.
10. TanStack Query cache in UI, well-suited to SSE-driven invalidation.
11. `useMemo` on `stepStates`/`edgeCounts` in `RunDetailPage`.
12. WebSocket event buffer for late-joiner replay.
13. Sanitization middleware opt-in (zero cost when disabled).
14. Reranker `batch_size=32` exposed as config.

---

## Critical Issues for Phase 3 Context

These findings shape what Phase 3 (Testing & Documentation) should look for:

### Test coverage must-haves
- **Shell blocklist bypasses (Sec C1):** unit tests with double-space, abs-path, command substitution, fullwidth unicode, `$(echo ...)` vectors.
- **Sanitization fail-open (Sec C2):** inject a detector that raises; assert request is rejected with 500, not forwarded.
- **Path containment (Sec H3):** test that file ops refuse absolute paths when `AGENTIC_FILE_BASE_DIR` unset.
- **Auth default-open (Sec H2):** test that server refuses startup without `AGENTIC_ALLOW_UNAUTHENTICATED` override.
- **Code execution sandbox (Sec H5):** `getattr(0, "__class__").__mro__[-1].__subclasses__()` escape, `__import__` bypass, env-leak check.
- **Run ID path traversal (Sec M5):** `run_id="../../etc/passwd"` must be rejected.
- **Concurrent workflow execution (Perf C2, H4, H5, H7):** launch 20 concurrent runs with differing `timeout_seconds`, `max_concurrency`, `runner` first-hit; assert no state crosstalk.
- **Multi-worker scaling (Perf C3):** at minimum a documented note + integration test showing router stats diverge when `--workers > 1`.
- **Vector store perf regression tests (Perf H2, H3):** assert query latency doesn't degrade past threshold when N grows.
- **Stream backpressure (Perf M7, M8):** slow WS consumer should not block others; buffer must be reaped.

### Documentation must-haves
- **Deployment security docs:** clear "production-ready checklist" — mandatory `AGENTIC_API_KEY`, `AGENTIC_FILE_BASE_DIR`, `AGENTIC_CORS_ORIGINS`, forbidden `--workers > 1` until Perf C3 resolved.
- **Tool safety model:** which tools are high-risk, allowlist mechanism, how to disable.
- **CORS + WebSocket origin model** — documented behaviors and gotchas.
- **SSE auth strategy** — resolve M1.
- **Subprocess env scoping** — document that LLM API keys must not leak to `code_execution`/`shell_ops`/`git_ops` children.
- **Multi-worker scaling limitations** — `CLAUDE.md`, `README.md`, `ARCHITECTURE.md` should document the single-worker constraint and Redis migration path.
