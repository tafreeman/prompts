# Sprint 1 — Ticket 01

## Header

| Field | Value |
|---|---|
| Sprint | 1 |
| Ticket ID | S1-01 |
| Title | Sanitization middleware fail-closed + exploding-detector test |
| Points | 2 |
| Value | 9 |
| T-shirt | S |
| V/E | 4.50 |
| Phase ref | Sec C2, Test C1 |
| Source finding | `05-final-report.md` Critical #2 |
| Status | Open |

---

## Sprint 1 Backlog (sorted by V/E)

| # | Ticket | Points | Value | V/E |
|---|---|---|---|---|
| **01** | **Sanitization fail-closed + exploding-detector test** | **2** | **9** | **4.50** |
| 02 | `file_ops` fail-closed when `AGENTIC_FILE_BASE_DIR` unset | 2 | 8 | 4.00 |
| 03 | `run_id` traversal test corpus | 2 | 6 | 3.00 |
| 04 | Audit `expressions.py:_validate_ast`; add injection negative corpus | 3 | 8 | 2.67 |
| 07 | Subprocess env sparse-scope across all tools (stretch) | 3 | 6 | 2.00 |
| 05 | Replace `ShellTool` blocklist with env-driven argv-allowlist | 5 | 10 | 2.00 |
| 06 | Harden `code_execution.py`: builtins, sparse env, `setrlimit` | 8 | 10 | 1.25 |

---

## Agent Persona

**Agent:** `security-reviewer` (`.claude/agents/security-reviewer.md`)

**Role:** Security-focused Python Engineer hardening ASGI middleware against detector failures.

**Expertise areas:**
- ASGI/Starlette middleware lifecycle and exception propagation
- Fail-safe vs. fail-open design patterns
- FastAPI request body handling and streaming
- pytest-asyncio test design for ASGI apps (asyncio_mode=auto)

**Boundaries:**
- Do not refactor the `SanitizationMiddleware` detector logic itself
- Do not change the 422-block path or the redact/rewrite path
- Do not add auth or CORS logic — out of scope for local-only platform

**Critical rules:**
- Pydantic v2 only (`model_dump`/`model_validate`)
- No `@pytest.mark.asyncio` — asyncio_mode=auto is configured
- All edits trigger ruff fix + format via post-commit hook; let it run
- Never modify `.env` files

**Output format:** Two files changed: `middleware/__init__.py` (2-line fix) + one new test file. Pre-commit green. pytest green.

---

## Problem Statement

**Why this matters:** `SanitizationASGIMiddleware` is the first line of defense against prompt injection in API request bodies. If any registered detector raises an unexpected exception, the current handler logs the error and silently passes the request through to the application unchanged. An attacker who knows a detector panics on specific input can bypass sanitization entirely by crafting a payload that crashes the detector.

**Blast radius:** Every `POST /api/run` and any other JSON endpoint protected by this middleware. On the local dev platform, a prompt-injected workflow step could execute shell commands, write files, or exfiltrate environment variables (including LLM API keys) from the developer's own workstation.

**Finding closed:** `05-final-report.md` Critical #2 (Sec C2) — "Blanket `except Exception` lets any detector error silently pass the request through. Fix: narrow to body-decode errors; return 500 on detector failure."

**Current code:**

```python
# agentic-workflows-v2/agentic_v2/server/middleware/__init__.py  lines 59-62
        except Exception:
            logger.exception("Sanitization middleware error — passing request through")

        return await call_next(request)
```

The `except Exception` block logs and falls through to `call_next`. The request reaches the application unsanitized.

---

## Scope

**In scope:**
- Change the `except Exception` handler to return HTTP 500 instead of passing through
- Add a test that injects an exploding detector and verifies the 500 response
- Update the docstring to reflect fail-closed behavior

**Explicitly out of scope:**
- Changing any detector implementation
- Changing the 422 (blocked) or redact paths
- Adding retry logic or circuit-breaker patterns
- Any auth or rate-limiting work

---

## Acceptance Criteria

- [ ] `except Exception` in `dispatch()` returns `JSONResponse(status_code=500, ...)` instead of falling through to `call_next`
- [ ] The error response body is `{"detail": "Internal sanitization error"}` (no stack trace in response body)
- [ ] `logger.exception(...)` call is preserved (still logs server-side)
- [ ] New test `tests/server/test_sanitization_middleware.py::test_exploding_detector_returns_500` passes: inject a detector that raises `RuntimeError`, POST JSON, assert response status == 500
- [ ] Existing tests for clean / redacted / blocked paths still pass
- [ ] `pre-commit run --all-files` exits 0
- [ ] `python -m pytest tests/server/ -v` exits 0

---

## Implementation Plan

1. **Open** `agentic-workflows-v2/agentic_v2/server/middleware/__init__.py`.

2. **Change** the exception handler (currently lines 59-62). Replace:
   ```python
   except Exception:
       logger.exception("Sanitization middleware error — passing request through")

   return await call_next(request)
   ```
   With:
   ```python
   except Exception:
       logger.exception("Sanitization middleware error — request rejected")
       return JSONResponse(
           status_code=500,
           content={"detail": "Internal sanitization error"},
       )

   return await call_next(request)
   ```

3. **Update the class docstring** to add: "On detector exception: returns HTTP 500 (fail-closed)."

4. **Create** `agentic-workflows-v2/tests/server/test_sanitization_middleware.py` (or add to an existing file if one exists):
   ```python
   import pytest
   from httpx import AsyncClient, ASGITransport
   from starlette.applications import Starlette
   from starlette.requests import Request
   from starlette.responses import JSONResponse
   from starlette.routing import Route

   from agentic_v2.server.middleware import SanitizationASGIMiddleware


   class _ExplodingDetector:
       async def process(self, text: str, metadata: dict) -> None:
           raise RuntimeError("detector exploded")


   async def _echo(request: Request) -> JSONResponse:
       return JSONResponse({"ok": True})


   def _make_app(detector) -> Starlette:
       app = Starlette(routes=[Route("/run", _echo, methods=["POST"])])
       app.state.sanitization = detector
       app.add_middleware(SanitizationASGIMiddleware)
       return app


   async def test_exploding_detector_returns_500():
       app = _make_app(_ExplodingDetector())
       async with AsyncClient(
           transport=ASGITransport(app=app), base_url="http://test"
       ) as client:
           response = await client.post(
               "/run",
               json={"workflow": "test"},
               headers={"content-type": "application/json"},
           )
       assert response.status_code == 500
       assert response.json()["detail"] == "Internal sanitization error"


   async def test_no_sanitizer_passes_through():
       """When sanitizer is not mounted, requests pass through normally."""
       app = _make_app(None)
       async with AsyncClient(
           transport=ASGITransport(app=app), base_url="http://test"
       ) as client:
           response = await client.post(
               "/run",
               json={"workflow": "test"},
               headers={"content-type": "application/json"},
           )
       assert response.status_code == 200
   ```

5. **Run** `pre-commit run --all-files` from repo root. Let ruff auto-fix any formatting.

6. **Run** `python -m pytest tests/server/ -v` from `agentic-workflows-v2/`.

---

## Test Plan

| Test | Type | Pass condition |
|---|---|---|
| `test_exploding_detector_returns_500` | Security / adversarial | Response 500, body `{"detail": "Internal sanitization error"}` |
| `test_no_sanitizer_passes_through` | Regression | Response 200 when `app.state.sanitization` is None |
| Existing clean / redact / block tests | Regression | All still pass |

The exploding-detector test is the **adversarial negative test** required by the security charter.

---

## Risks / Pitfalls

| Risk | Mitigation |
|---|---|
| The `except Exception` also catches `UnicodeDecodeError` from `body_bytes.decode(...)` | The decode is inside the `try` block, so 500 is still correct here — a malformed body should also be rejected, not passed through. No change needed. |
| `JSONResponse` import not in scope | `JSONResponse` is already imported at the top of the file (used for the 422 block path). No new import needed. |
| Test uses `AsyncClient(transport=ASGITransport(...))` which requires `httpx` | `httpx` is already a dev dependency. Verify with `uv run python -c "import httpx"`. |
| `_ExplodingDetector` doesn't match the real `SanitizationMiddleware` interface | The middleware only calls `await sanitizer.process(body_text, metadata)` — the test stub matches this interface exactly. |

---

## Not in Scope

- Changing the 422 blocked-request path
- Changing the redacted-body rewrite path
- Adding tests for the redact / block flows (they may already exist; don't delete them)
- Any changes outside `middleware/__init__.py` and the test file

---

## Verification

Run these commands from `agentic-workflows-v2/` before declaring done:

```bash
# 1. Lint + format
pre-commit run --all-files

# 2. Type check
python -m mypy agentic_v2/server/middleware/__init__.py --ignore-missing-imports

# 3. Run affected tests
python -m pytest tests/server/ -v

# 4. Manual smoke — verify the 500 path exists in the diff
git diff --stat HEAD
```

Expected: all pass, diff shows exactly 2 files changed.

---

## Dependencies

None. This ticket has no upstream dependencies and can land on day 1 of the sprint.
