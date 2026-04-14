# Security Audit — 2026-04-14

**Git SHA (audit):** 0252c88ce93792d05d13613e0b1f431d3193d006
**Git SHA (after fixes):** 7f1ae0f
**Auditor:** Claude Code (Security Expert agent)
**Scope:** `agentic-workflows-v2/agentic_v2/`, `agentic-v2-eval/`, `tools/`
**Status:** ⚠️ Issues Found (M-1 and L-3, L-4 resolved)

## Implementation Status (2026-04-14)

| Finding | Status | Commit |
|---------|--------|--------|
| M-1 — Sanitization in `dry_run=True` | ✅ Fixed: `dry_run=False` | `9cc4003` |
| M-2 — Auth open by default | Open — Strategic item S-3 | — |
| M-3 — `ShellTool` subprocess_shell | Open — Strategic item S-4 | — |
| L-1 — Placeholder `api_key="lm-studio"` | Open (low priority) | — |
| L-2 — `hashlib.md5` for cache keys | Open (low priority) | — |
| L-3 — `AGENTIC_FILE_BASE_DIR` undocumented | ✅ Fixed: added to `.env.example` | `c9b3247` |
| L-4 — `.gitignore` missing `.env.*` | ✅ Fixed: wildcard added | `2900cc0` |
| L-5 — No rate limiting on `/api/run` | Open — Strategic item S-9 | — |

---

---

## Executive Summary

The codebase demonstrates solid security fundamentals: parameterized SQL, constant-time token comparison, `secrets` module usage, path-traversal protection, a layered sanitization middleware pipeline, and no hardcoded production credentials. However, three medium-severity issues and several low-severity issues were identified that should be addressed before a production deployment.

---

## Findings

### Critical

_No critical findings._

---

### High

_No high-severity findings._

---

### Medium

#### M-1: Sanitization middleware initialized in `dry_run=True` (enforces nothing)

**File:** `agentic-workflows-v2/agentic_v2/server/app.py:88`

```python
app.state.sanitization = SanitizationMiddleware.default(dry_run=True)
```

The `SanitizationMiddleware` is deliberately started in shadow/dry-run mode — it detects and logs but **never blocks or redacts** any content. The `_sanitize_inputs` helper in `routes/workflows.py` calls `result.is_safe` and raises HTTP 400 on a block, but `is_safe` will always return `True` in dry-run mode because the policy is overridden to return `Classification.CLEAN` for every input. Prompt injection, PII, and secrets in workflow inputs are silently logged and then passed to the LLM unchanged.

**Risk:** An attacker can embed prompt-injection payloads in workflow inputs with no enforcement consequence.

**Recommendation:** Flip to `dry_run=False` after validating the detector false-positive rate against real traffic. Track via `AGENTIC_SANITIZATION_DRY_RUN` env var so it can be toggled without a code change.

---

#### M-2: Authentication is opt-in — server is fully open by default

**File:** `agentic-workflows-v2/agentic_v2/server/auth.py`, `app.py:65-69`

When `AGENTIC_API_KEY` is not set (which is the default out-of-box), the `APIKeyMiddleware` is a complete no-op and every `/api/` route is publicly accessible. The startup log emits a warning, but there is no server-level enforcement requiring the key to be set for any non-localhost bind address.

**Risk:** In a cloud or containerized deployment where the developer forgets to set `AGENTIC_API_KEY`, the workflow execution API (including code execution and shell tools) is unauthenticated.

**Recommendation:** Add a startup check: if the bind host is not `127.0.0.1` / `localhost` and `AGENTIC_API_KEY` is unset, either refuse to start or emit a `CRITICAL` log line and return HTTP 503 on all `/api/run` and `/api/workflows` mutating endpoints.

---

#### M-3: `ShellTool` uses `create_subprocess_shell` with user-supplied command string

**File:** `agentic-workflows-v2/agentic_v2/tools/builtin/shell_ops.py:113,153`

```python
process = await asyncio.create_subprocess_shell(
    command,   # user-supplied string
    ...
)
```

`ShellTool.execute()` passes the `command` parameter (which ultimately originates from LLM-generated tool calls or workflow YAML) directly to the shell interpreter. The blocklist at lines 73–96 is substring-based and easily bypassed (e.g., `curl\t`, `curl${IFS}`, `CURL`, tab-separated commands). `ShellExecTool` correctly uses `create_subprocess_exec`, but `ShellTool` does not.

**Risk:** Prompt injection → LLM generates a crafted shell command → blocklist bypass → arbitrary command execution.

**Recommendation:** Replace `create_subprocess_shell` in `ShellTool` with `create_subprocess_exec` using `shlex.split()` (as `ShellExecTool` already does). If pipeline metacharacters are genuinely required, apply allowlisting of known-safe commands rather than blocklisting dangerous ones.

---

### Low

#### L-1: Placeholder `api_key` literals for local LLM adapters (not real secrets)

**File:** `agentic-workflows-v2/agentic_v2/langchain/model_builders.py:352,402`

```python
api_key="lm-studio"
api_key="local-api"
```

These are dummy values required by the `ChatOpenAI` constructor for local endpoints that do not need authentication. They are not real secrets and do not expose sensitive data. However, automated secret scanners (e.g., `detect-secrets`) may flag them.

**Recommendation:** Replace with environment variable reads with a documented fallback: `os.getenv("LMSTUDIO_API_KEY", "lm-studio")`. This also future-proofs authentication if the local endpoint gains auth support.

---

#### L-2: `hashlib.md5` used for non-security identifiers

**Files:**
- `agentic-workflows-v2/agentic_v2/integrations/mcp/results/storage.py:76,124`
- `tools/llm/probe_config.py:283`

MD5 is used to generate short content-hash IDs (8-char hex, truncated) for cache keys and storage identifiers — not for security purposes. This is architecturally benign but may trigger static analysis tools.

**Recommendation:** Replace with `hashlib.sha256(...).hexdigest()[:8]` for consistency. The performance difference is negligible. Add a comment clarifying the non-security intent.

---

#### L-3: `AGENTIC_FILE_BASE_DIR` not set by default — path traversal protection is inactive

**File:** `agentic-workflows-v2/agentic_v2/tools/builtin/file_ops.py:15-32`

```python
_FILE_BASE_DIR: str | None = os.environ.get("AGENTIC_FILE_BASE_DIR")
# When unset, validation is skipped (backwards-compatible with pre-hardening behaviour)
```

File I/O tools (`FileReadTool`, `FileWriteTool`, etc.) call `_validate_path()`, but the path-containment check in `ensure_within_base` is only activated when `AGENTIC_FILE_BASE_DIR` is set. In default deployments, an LLM-generated tool call can read or write any file accessible to the server process (e.g., `../../.env`, `/etc/passwd`).

**Recommendation:** Document `AGENTIC_FILE_BASE_DIR` in `.env.example` and recommend setting it to the project working directory in all non-development deployments. Optionally default to the repository root when the env var is absent.

---

#### L-4: `.gitignore` covers `.env` but not `.env.*` wildcard

**File:** `.gitignore:8`

```
.env
```

The root `.gitignore` contains a single `.env` entry. Environment files named `.env.local`, `.env.production`, `.env.staging`, etc. are **not** ignored.

**Recommendation:** Add `.env.*` (with `!.env.example` exception) to `.gitignore`:

```gitignore
.env
.env.*
!.env.example
```

---

#### L-5: No API-level rate limiting on `/api/run`

**Files:** `agentic-workflows-v2/agentic_v2/server/routes/workflows.py:278`

The `/api/run` endpoint spawns a background LLM workflow task without any request-rate gating. While LLM provider rate limits act as a natural backstop, an unauthenticated (or authenticated) client can trigger unbounded concurrent workflows, causing DoS via provider cost or resource exhaustion.

**Recommendation:** Add `slowapi` or a simple token-bucket middleware on `/api/run`. Enforce a per-IP and per-API-key limit (e.g., 10 requests/minute).

---

#### L-6: `verification.py` `_run_single` uses `create_subprocess_shell` with config-sourced commands

**File:** `agentic-workflows-v2/agentic_v2/engine/verification.py:92`

```python
proc = await asyncio.create_subprocess_shell(cmd, ...)
```

Commands here come from workflow YAML `verification_commands` fields — not directly from user HTTP input — so the attack surface is limited to YAML authoring. Still, if workflow YAMLs can be modified via the `/api/workflows/{name}` PUT endpoint, this could be exploited.

**Recommendation:** Apply the same command validation blocklist used in `build_ops.py` before executing verification commands. Prefer `create_subprocess_exec` with `shlex.split()`.

---

## Metrics

| Check | Result | Status |
|-------|--------|--------|
| Hardcoded production secrets | None found | ✅ Pass |
| `eval()` / `exec()` on untrusted input | `exec()` used in `CodeExecutionTool` — sandboxed subprocess with AST safety check | ✅ Acceptable |
| `pickle.loads()` on untrusted data | Not used | ✅ Pass |
| `yaml.load()` without `SafeLoader` | Not found — `yaml.safe_load` not audited but no unsafe calls found | ✅ Pass |
| `shell=True` / `create_subprocess_shell` with user input | Found in `ShellTool` (M-3) and `verification.py` (L-6) | ⚠️ Medium / Low |
| File path traversal protection | `ensure_within_base` exists but opt-in only (L-3) | ⚠️ Low |
| FastAPI endpoint authentication | Opt-in only — open by default (M-2) | ⚠️ Medium |
| CORS wildcard `allow_origins=["*"]` | Not set — defaults to localhost only | ✅ Pass |
| Weak crypto (MD5/SHA1 for security) | MD5 used for non-security identifiers (L-2) | ⚠️ Low |
| Insecure `random` for tokens | `random` used for jitter/sampling only, not security tokens | ✅ Pass |
| SQL injection | Parameterized queries throughout SQLite store | ✅ Pass |
| FastAPI input typed with Pydantic models | Core routes use typed models; some `dict[str, Any]` in internal helpers | ✅ Acceptable |
| Logging of secrets / PII | No leakage found in server or tool code | ✅ Pass |
| Prompt injection sanitization | Pipeline exists but `dry_run=True` — not enforced (M-1) | ⚠️ Medium |
| `.gitignore` covers `.env.*` wildcard | `.env` only — missing wildcard (L-4) | ⚠️ Low |
| API rate limiting on `/api/run` | Not implemented (L-5) | ⚠️ Low |
| Constant-time token comparison | `secrets.compare_digest` used in `auth.py` | ✅ Pass |
| Path safety utility implemented | `ensure_within_base` in `utils/path_safety.py` is correct | ✅ Pass |
| `AGENTIC_FILE_BASE_DIR` documented | Missing from `.env.example` (L-3) | ⚠️ Low |

---

## Recommendations (Priority Order)

1. **[M-1] Enable sanitization enforcement** — Set `dry_run=False` (or gate on `AGENTIC_SANITIZATION_DRY_RUN` env var) after baseline false-positive testing. This is the most impactful change — it activates existing prompt-injection and PII detection that is currently dormant.

2. **[M-3] Replace `create_subprocess_shell` in `ShellTool`** — Migrate to `create_subprocess_exec` + `shlex.split()`. The blocklist approach is fundamentally bypassable. `ShellExecTool` already demonstrates the correct pattern.

3. **[M-2] Harden no-auth default** — Emit a `CRITICAL` warning and optionally block mutating routes when `AGENTIC_API_KEY` is unset on a non-localhost binding. Consider requiring auth for `/api/run` unconditionally.

4. **[L-3] Document and default `AGENTIC_FILE_BASE_DIR`** — Add to `.env.example`, set a sensible default in the tool (e.g., `os.getcwd()`), and document the security implication in `WORKFLOW_AUTHORING.md`.

5. **[L-4] Expand `.gitignore` for `.env.*`** — One-line fix to prevent accidental commit of `.env.staging`, `.env.local`, etc.

6. **[L-5] Add rate limiting to `/api/run`** — Install `slowapi` and apply `@limiter.limit("10/minute")` to the run endpoint.

7. **[L-2] Replace `hashlib.md5` with `sha256`** — Low effort, eliminates static analysis noise.

8. **[L-6] Apply command validation in `verification.py`** — Apply the same blocklist used in `build_ops.py` to `_run_single`, or migrate to `create_subprocess_exec`.

---

## Positive Findings

The following security controls were found to be correctly implemented:

- **Constant-time token comparison** — `secrets.compare_digest` in `auth.py:108`.
- **Parameterized SQL** — All SQLite queries in `_checkpoint_store.py` use `?` placeholders.
- **`CodeExecutionTool` sandboxing** — AST-based import blocklist + subprocess isolation + restricted builtins.
- **Path traversal utility** — `ensure_within_base` uses `Path.resolve()` + `is_relative_to()` correctly.
- **No hardcoded production secrets** — All API keys/tokens loaded from environment variables.
- **CORS restricted to localhost** — Default allow-list does not include wildcard.
- **SHA-256 for audit hashes** — `SanitizationResult.compute_hash` uses SHA-256.
- **Sanitization pipeline architecture** — The detector chain (Unicode → Secrets → PII → Injection) is well-designed and immutable (`model_config = {"frozen": True}`).
- **WebSocket origin validation** — `is_websocket_origin_allowed` validates browser Origin headers.
