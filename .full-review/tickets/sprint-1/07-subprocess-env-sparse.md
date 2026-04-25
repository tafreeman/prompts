# Sprint 1 — Ticket 07 (Stretch)

## Header

| Field | Value |
|---|---|
| Sprint | 1 |
| Ticket ID | S1-07 |
| Title | Subprocess env sparse-scope across all tools incl. MCP runtime |
| Points | 3 |
| Value | 6 |
| T-shirt | M |
| V/E | 2.00 |
| Phase ref | Sec L3 |
| Source finding | `05-final-report.md` High Sec H6 (subprocess env, extended scope) |
| Status | Stretch — land only if Sprint 1 committed items (S1-01 through S1-06) are done with buffer remaining |

---

## Agent Persona

**Agent:** `security-reviewer` (`.claude/agents/security-reviewer.md`)

**Role:** Security-focused Python Engineer auditing and hardening subprocess environment in tool modules outside `code_execution.py`.

**Expertise areas:**
- `asyncio.create_subprocess_exec` `env=` parameter semantics
- Sparse environment construction for security-sensitive child processes
- grep/audit patterns across a Python codebase
- pytest parametrize for regression coverage

**Boundaries:**
- Do not change `code_execution.py` — it already has correct sparse env (S1-06 scope)
- Do not change `shell_ops.py`'s `execute()` method — the allowlist (S1-05) is the primary defense there; sparse env is defense-in-depth and can be added in the same PR
- Do not add resource limits to non-subprocess tools
- Do not change MCP client library internals

**Critical rules:**
- On Windows, `PATH` and `PATHEXT` must be included in the sparse env or subprocess calls fail (executable not found)
- `SYSTEMROOT` and `WINDIR` are also required on Windows for some system DLL loading
- Sparse env should be extracted as a shared helper `_minimal_subprocess_env()` in a new `agentic_v2/tools/subprocess_utils.py` module to avoid duplication
- No `@pytest.mark.asyncio`

**Output format:** New `subprocess_utils.py` helper, updated `git_ops.py` and `shell_ops.py` (env= added), updated MCP runtime calls if found. One test file. Pre-commit green.

---

## Problem Statement

**Why this matters:** `CodeExecutionTool` (S1-06) already constructs a sparse subprocess environment that excludes API keys. However, other tools that spawn subprocesses do not. Any subprocess that inherits the full `os.environ` receives all environment variables of the parent process — including `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`, and any other secrets loaded into the dev environment.

For a local dev platform, this is a realistic risk: a prompt-injected agent step that uses `GitOpsTool` to run `git` commands could be crafted to exfiltrate API keys via git remote URLs or git hooks.

**Finding closed:** `05-final-report.md` Sec H6 — "uses `env={**os.environ, ...}` — untrusted code has `OPENAI_API_KEY`/`ANTHROPIC_API_KEY`/`GITHUB_TOKEN`." (Extended scope: beyond `code_execution.py`.)

**Tools to audit:**
1. `agentic_v2/tools/builtin/git_ops.py` — `asyncio.create_subprocess_exec` with no `env=` (inherits full environment)
2. `agentic_v2/tools/builtin/shell_ops.py` — `ShellTool.execute()` with no `env=` (inherits full environment)
3. `agentic_v2/integrations/mcp/` — any subprocess spawns in MCP transport

---

## Scope

**In scope:**
- Create `agentic_v2/tools/subprocess_utils.py` with a `minimal_subprocess_env()` function that returns the safe sparse env
- Update `git_ops.py` subprocess calls to pass `env=minimal_subprocess_env()`
- Update `shell_ops.py` `ShellTool.execute()` subprocess calls (two locations: capture_output and fire-and-forget) to pass `env=minimal_subprocess_env()`
- Audit `agentic_v2/integrations/mcp/` for subprocess spawns and apply the same treatment
- Add a test that verifies the sparse env does not include API key variable names

**Explicitly out of scope:**
- Changing `code_execution.py` (already has correct sparse env, different implementation)
- Adding resource limits to `git_ops` or `shell_ops` (S1-06 scope)
- Auditing tools outside `agentic_v2/tools/builtin/` and `agentic_v2/integrations/mcp/`

---

## Acceptance Criteria

- [ ] `agentic_v2/tools/subprocess_utils.py` exists with `minimal_subprocess_env()` that returns a `dict[str, str]` containing only safe env keys
- [ ] `git_ops.py` subprocess calls pass `env=minimal_subprocess_env()`
- [ ] `shell_ops.py` `ShellTool.execute()` subprocess calls pass `env=minimal_subprocess_env()`
- [ ] `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`, `ANTHROPIC_API_KEY` are not present in `minimal_subprocess_env()` output even when set in `os.environ`
- [ ] `PATH` and `PATHEXT` (Windows) are present in the output
- [ ] New test `tests/tools/test_subprocess_utils.py` passes
- [ ] `pre-commit run --all-files` exits 0
- [ ] `python -m pytest tests/tools/test_subprocess_utils.py -v` exits 0

---

## Implementation Plan

1. **Create** `agentic-workflows-v2/agentic_v2/tools/subprocess_utils.py`:

```python
"""Shared subprocess environment utilities for tool modules.

All subprocesses spawned by tools should use ``minimal_subprocess_env()``
rather than inheriting the full parent environment, to prevent API keys
and secrets from leaking to untrusted child processes.
"""

from __future__ import annotations

import os

# Keys that subprocesses legitimately need to function.
# API keys, tokens, and secrets are intentionally excluded.
_SAFE_ENV_KEYS: frozenset[str] = frozenset(
    {
        "PATH",
        "PATHEXT",        # Windows: executable extension list
        "SYSTEMROOT",     # Windows: required for some DLL loading
        "WINDIR",         # Windows: same
        "TEMP",
        "TMP",
        "TMPDIR",
        "HOME",
        "USERPROFILE",    # Windows: home directory
        "LANG",           # Locale for output encoding
        "LC_ALL",
        "LC_CTYPE",
        "PYTHONDONTWRITEBYTECODE",
    }
)


def minimal_subprocess_env() -> dict[str, str]:
    """Return a minimal environment for subprocess execution.

    Includes only keys required for the subprocess to locate executables
    and write temporary files. Excludes all API keys, tokens, and secrets.

    Returns:
        dict[str, str]: Sparse environment suitable for ``env=`` kwarg.
    """
    env = {
        key: value
        for key, value in os.environ.items()
        if key.upper() in {k.upper() for k in _SAFE_ENV_KEYS}
    }
    env.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    return env
```

2. **Update** `git_ops.py` — find all `asyncio.create_subprocess_exec` calls and add `env=minimal_subprocess_env()`:

```python
from ..subprocess_utils import minimal_subprocess_env

# In execute():
process = await asyncio.create_subprocess_exec(
    *cmd_list,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    cwd=str(cwd_path),
    env=minimal_subprocess_env(),   # <-- add this
)
```

3. **Update** `shell_ops.py` `ShellTool.execute()` — both subprocess calls (capture_output=True and capture_output=False):

```python
from .subprocess_utils import minimal_subprocess_env

# Both asyncio.create_subprocess_exec calls get env=minimal_subprocess_env()
```

4. **Audit MCP transports** — run:
```bash
grep -rn "create_subprocess_exec\|create_subprocess_shell\|Popen\|subprocess.run" \
    agentic_v2/integrations/mcp/ agentic_v2/integrations/
```
For each hit, add `env=minimal_subprocess_env()` if the call does not already pass a sparse env.

5. **Create** `agentic-workflows-v2/tests/tools/test_subprocess_utils.py`:

```python
"""Tests that minimal_subprocess_env() excludes secrets."""

import os
from unittest.mock import patch

from agentic_v2.tools.subprocess_utils import minimal_subprocess_env


_SECRET_KEYS = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GITHUB_TOKEN",
    "AZURE_OPENAI_API_KEY_0",
    "GEMINI_API_KEY",
    "DATABASE_URL",
    "SECRET_KEY",
]


def test_api_keys_excluded_from_sparse_env():
    """API keys must never appear in the subprocess environment."""
    fake_secrets = {k: "sk-fake-value-1234" for k in _SECRET_KEYS}
    with patch.dict(os.environ, fake_secrets):
        env = minimal_subprocess_env()
    for key in _SECRET_KEYS:
        assert key not in env, f"Secret key {key!r} leaked into subprocess env"


def test_path_present_in_sparse_env():
    """PATH must be present so executables can be found."""
    env = minimal_subprocess_env()
    assert "PATH" in env or "path" in {k.lower() for k in env}


def test_pythondontwritebytecode_set():
    env = minimal_subprocess_env()
    assert env.get("PYTHONDONTWRITEBYTECODE") == "1"


def test_sparse_env_is_subset_of_full_env():
    """Every key in the sparse env must also exist in the full env (or be our addition)."""
    full_env = os.environ
    env = minimal_subprocess_env()
    for key in env:
        if key == "PYTHONDONTWRITEBYTECODE":
            continue  # We inject this
        assert key in full_env or key.upper() in {k.upper() for k in full_env}, \
            f"Unexpected key {key!r} in sparse env"
```

6. **Run** `pre-commit run --all-files`.

7. **Run** `python -m pytest tests/tools/test_subprocess_utils.py -v`.

---

## Test Plan

| Test | Type | Pass condition |
|---|---|---|
| `test_api_keys_excluded_from_sparse_env` | Security corpus | All secret keys absent from output |
| `test_path_present_in_sparse_env` | Regression | `PATH` in env |
| `test_pythondontwritebytecode_set` | Regression | Value is `"1"` |
| `test_sparse_env_is_subset_of_full_env` | Sanity | No phantom keys injected |

---

## Risks / Pitfalls

| Risk | Mitigation |
|---|---|
| `git` on some systems requires `GIT_*` env vars (e.g., `GIT_SSH_COMMAND`, `GIT_ASKPASS`) | Add `GIT_*` keys explicitly to `_SAFE_ENV_KEYS` only if tests fail because of missing git config. Check git output in test mode first. |
| Windows: missing `SYSTEMROOT`/`WINDIR` causes some executables to fail silently | Both are already in `_SAFE_ENV_KEYS`. Verify on Windows CI (story 3.2 already has Windows CI). |
| MCP transports may use `subprocess.Popen` instead of `asyncio.create_subprocess_exec` | Audit covers both — `grep` command checks `Popen` as well. |
| `_SAFE_ENV_KEYS` case-insensitive matching is needed on Windows (env vars are case-insensitive) | The comparison `key.upper() in {k.upper() for k in _SAFE_ENV_KEYS}` handles this. |

---

## Not in Scope

- Changing `code_execution.py` (already has correct sparse env)
- Adding resource limits to git/shell tools (S1-06 scope)
- Auditing tools outside the specified paths

---

## Verification

```bash
# From agentic-workflows-v2/

# 1. Lint + format
pre-commit run --all-files

# 2. Type check
python -m mypy agentic_v2/tools/subprocess_utils.py agentic_v2/tools/builtin/git_ops.py --ignore-missing-imports

# 3. New tests
python -m pytest tests/tools/test_subprocess_utils.py -v

# 4. Confirm no subprocess calls inherit full env in tools
grep -n "create_subprocess_exec\|Popen" \
    agentic_v2/tools/builtin/git_ops.py \
    agentic_v2/tools/builtin/shell_ops.py \
    | grep -v "env="
# Expected: no output (all subprocess calls now pass env=)

# 5. Full tools tests
python -m pytest tests/tools/ -v --tb=short
```

---

## Dependencies

**S1-05 (ShellTool allowlist)** should land first if modifying `shell_ops.py` in the same sprint. If S1-05 is not done, this ticket can still land independently — it only adds `env=minimal_subprocess_env()` to the existing subprocess calls in `ShellTool`, which is additive and does not conflict.
