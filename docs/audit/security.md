# Security Audit

**Date:** 2026-03-17
**Auditor:** Claude Code (automated)
**Scope:** Secret exposure, injection vectors, access controls, security headers

---

## Findings Summary

| # | Severity | Finding | Status |
|---|----------|---------|--------|
| SEC-0 | FALSE POSITIVE | `.env` has real API keys | Gitignored, local-only |
| SEC-1 | HIGH | Shell injection in `langchain/tools.py` | Open |
| SEC-2 | HIGH | CORS hardcoded to localhost | Open (dev-only) |
| SEC-3 | HIGH | Missing security headers | Open |
| SEC-4 | MEDIUM | File tools accept arbitrary paths | Open |
| SEC-5 | MEDIUM | `.claude/settings.json` tracked | Needs review |
| SEC-6 | LOW | `detect-secrets` hook effectiveness | Needs verification |

---

## Detailed Findings

### SEC-0: `.env` Contains Real API Keys -- FALSE POSITIVE

**Status:** FALSE POSITIVE -- verified safe.

The `.env` file on disk contains real API keys for OpenAI, Anthropic, Gemini, and Azure. However:
- `.env` is listed in `.gitignore` (line 8)
- `git ls-files .env` confirms the file is NOT tracked
- No `.env` file appears in any commit history
- `.env.example` (tracked) contains only placeholder values

This is the correct pattern. The risk is local-only: if the developer's machine is compromised, the keys are exposed. This is inherent to any local development setup.

**Action:** None required. Consider documenting secret rotation procedures for team environments.

### SEC-1: Shell Injection in LangChain Tools (HIGH)

**File:** `agentic-workflows-v2/agentic_v2/langchain/tools.py`, lines 125-155

The `shell_run()` function uses `subprocess.run(shell=True)` with a `# nosec B602` annotation suppressing the Bandit warning:

```python
result = subprocess.run(command, shell=True, capture_output=True, ...)  # nosec B602
```

If `command` originates from LLM output (which it does in agentic workflows), this creates a command injection vector. An adversarial prompt or hallucinated command could execute arbitrary shell commands.

**Risk:** An attacker who can influence the LLM's tool-calling output could achieve remote code execution on the host machine.

**Mitigations already in place:**
- Tool allowlisting per workflow step (default DENY for shell tools)
- The `# nosec` annotation indicates awareness of the risk

**Recommended additional mitigations:**
1. Replace `shell=True` with `shell=False` and pass command as a list
2. Add an explicit command allowlist or blocklist
3. Add input sanitization to reject shell metacharacters (`;`, `|`, `&&`, backticks)
4. Log all shell commands for audit trail

### SEC-2: CORS Hardcoded to Localhost Origins (HIGH)

**File:** `agentic-workflows-v2/agentic_v2/server/app.py`, lines 48-61

CORS middleware is configured with hardcoded localhost origins as a fallback:

```python
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:8010").split(",")
```

This is appropriate for local development but creates a risk if the server is deployed to a production environment without setting `CORS_ORIGINS`:
- Any page on localhost can make authenticated requests to the API
- The fallback masks the absence of proper CORS configuration

**Recommended fixes:**
1. In production mode, require `CORS_ORIGINS` to be explicitly set (fail-closed)
2. Never include `*` as an allowed origin
3. Document the dev-only default in the server README

### SEC-3: Missing Security Headers (HIGH)

**File:** `agentic-workflows-v2/agentic_v2/server/app.py`

The FastAPI server does not set standard security headers:

| Header | Status | Risk |
|--------|--------|------|
| `X-Content-Type-Options: nosniff` | Missing | MIME-type sniffing attacks |
| `X-Frame-Options: DENY` | Missing | Clickjacking |
| `Content-Security-Policy` | Missing | XSS, data injection |
| `Strict-Transport-Security` | Missing | Downgrade attacks |
| `X-XSS-Protection` | Missing | Reflected XSS (legacy browsers) |

For a local development server, this is low risk. For any production or shared deployment, these headers are required by most security baselines (OWASP, FedRAMP).

**Recommended fix:** Add a security headers middleware that is enabled by default and configurable via environment variables:

```python
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    # ... etc
    return response
```

### SEC-4: File Tools Lack Path Traversal Protection (MEDIUM)

**File:** `agentic-workflows-v2/agentic_v2/langchain/tools.py`, lines 23-50

The `file_read()` and `file_write()` LangChain tool implementations accept arbitrary file paths with no `allowed_base_dir` restriction or path traversal validation.

The native engine tools (in `tools/builtin/`) already have path traversal protection via `ensure_within_base()` (added in Sprint 11 security audit). The LangChain tools were not updated to match.

**Risk:** An LLM-generated tool call like `file_read("/etc/passwd")` or `file_write("/root/.ssh/authorized_keys", ...)` would succeed if the process has permissions.

**Recommended fix:** Port the `ensure_within_base()` pattern from native tools to LangChain tools. Require an `allowed_base_dir` constructor argument.

### SEC-5: `.claude/settings.json` Tracked in Git (MEDIUM)

**File:** `.claude/settings.json`

This file is tracked in version control. `.claude/settings.local.json` is properly gitignored for local overrides.

**Risk:** If someone adds sensitive configuration (API endpoints, internal URLs, team-specific settings) to `settings.json` instead of `settings.local.json`, it will be committed and pushed.

**Recommended action:** Review the current contents of `.claude/settings.json` to confirm no sensitive data is present. Add a comment in the file indicating that sensitive values belong in `settings.local.json`.

### SEC-6: `detect-secrets` Pre-Commit Hook Effectiveness (LOW)

**File:** `.pre-commit-config.yaml`

The `detect-secrets` hook is configured in the pre-commit pipeline, which is good. However:
- The baseline file (`.secrets.baseline`) may not be current
- New secret patterns added since the baseline was last regenerated will not be caught
- Pre-commit hooks can be bypassed with `--no-verify`

**Recommended actions:**
1. Run `detect-secrets scan --baseline .secrets.baseline` to refresh the baseline
2. Add a CI check that runs `detect-secrets` independently (not just pre-commit)
3. Periodically audit the baseline for false-positive suppressions that may mask real secrets

---

## Action Items by Priority

| Priority | Action | Effort |
|----------|--------|--------|
| 1 | Add path traversal protection to LangChain file tools | 1 hour |
| 2 | Add security headers middleware (with env gating) | 1 hour |
| 3 | Harden `shell_run()` -- switch to `shell=False` + allowlist | 2 hours |
| 4 | Document CORS as dev-only, fail-closed in prod | 30 min |
| 5 | Review `.claude/settings.json` for sensitive data | 10 min |
| 6 | Refresh `detect-secrets` baseline | 15 min |
