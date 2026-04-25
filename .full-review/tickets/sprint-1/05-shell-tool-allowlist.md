# Sprint 1 — Ticket 05

## Header

| Field | Value |
|---|---|
| Sprint | 1 |
| Ticket ID | S1-05 |
| Title | Replace `ShellTool` blocklist with env-driven argv-allowlist + bypass corpus test |
| Points | 5 |
| Value | 10 |
| T-shirt | L |
| V/E | 2.00 |
| Phase ref | Sec C1, Test C2 |
| Source finding | `05-final-report.md` Critical #1 |
| Status | Open |

---

## Agent Persona

**Agent:** `security-reviewer` (`.claude/agents/security-reviewer.md`)

**Role:** Security-focused Python Engineer replacing a substring blocklist with an env-driven argv-allowlist in `ShellTool`.

**Expertise areas:**
- Shell injection attack vectors: metachar bypass, double-space, unicode fullwidth, absolute path, command substitution, chaining
- `shlex.split()` behavior on Windows vs. POSIX and the `posix=` flag
- Environment variable-driven configuration with fail-closed defaults
- `asyncio.create_subprocess_exec` vs. `shell=True` distinction
- pytest parametrize security corpora

**Boundaries:**
- Do not change `ShellExecTool` — it takes explicit `program`/`args` and is already safe
- Do not add a new shell execution engine; modify `ShellTool.execute()` only
- Do not change CI/CD pipeline files
- Do not change any YAML workflow definitions

**Critical rules:**
- The allowlist must be opt-in via `AGENTIC_SHELL_ALLOWED_COMMANDS` env var; when unset, `ShellTool.execute()` must reject all commands (fail-closed)
- `shlex.split(cmd)[0]` extracts the executable name for allowlist checking after metachar rejection
- The existing `_SHELL_METACHARS` frozenset and `_split_command()` must be preserved (they provide a second safety layer)
- No `@pytest.mark.asyncio` — asyncio_mode=auto is configured

**Output format:** `shell_ops.py` changed (~40 lines net change), one test file. Pre-commit green. pytest green.

---

## Problem Statement

**Why this matters:** `ShellTool.execute()` currently uses a `dangerous_patterns` string-blocklist approach (lines 84-113 of `shell_ops.py`). Blocklists fail against:

- **Double-space bypass:** `"curl  http://evil.com"` — pattern checks for `"curl "` (one space)
- **Unicode fullwidth:** `"\uff43\uff55\uff52\uff4c "` looks like `"curl "` to humans but not to the blocklist
- **Absolute path:** `"/usr/bin/curl http://evil.com"` — blocklist checks for `"curl "` not the full path
- **Command substitution:** `"ls $(curl http://evil.com)"` — the `$(` metachar is caught by `_SHELL_METACHARS`, but only if the check runs before the blocklist
- **Case variation:** `"CURL http://evil.com"` — `cmd_lower` handles this, but the pattern must still be exact

An allowlist is strictly stronger: if `curl` is not in the allowed list, it cannot run regardless of how the command is spelled or obfuscated. The fail-closed default (no env var = no shell commands allowed) ensures new installations are safe out of the box.

**Finding closed:** `05-final-report.md` Critical #1 (Sec C1) — "ShellTool substring blocklist bypassed by double-space, absolute path, `$(echo ...)`, unicode fullwidth, chained commands. Fix: env-driven allowlist via `shlex.split(cmd)[0]`."

**Current vulnerable code (`shell_ops.py:84-113`):**
```python
dangerous_patterns = [
    "rm -rf /", "curl ", "wget ", "python -c", ...
]
cmd_lower = command.lower()
if any(pattern in cmd_lower for pattern in dangerous_patterns):
    return ToolResult(success=False, error="Command contains potentially dangerous operations...")
```

---

## Scope

**In scope:**
- Replace the `dangerous_patterns` blocklist in `ShellTool.execute()` with an allowlist loaded from `AGENTIC_SHELL_ALLOWED_COMMANDS`
- When `AGENTIC_SHELL_ALLOWED_COMMANDS` is unset or empty, reject all commands with a clear error message
- When set, parse as comma-separated command names (e.g., `"ls,cat,python"`) and check `shlex.split(cmd)[0]` against the list
- Add bypass corpus test covering the documented attack vectors

**Explicitly out of scope:**
- Changing `ShellExecTool` (already safe — uses explicit argv)
- Changing `_SHELL_METACHARS` or `_split_command()` helper (keep as second layer)
- Adding sub-path allowlisting (e.g., allowing `/usr/bin/ls` but not `/tmp/ls`)
- Changing CI environment variables or workflow YAML files

---

## Acceptance Criteria

- [ ] When `AGENTIC_SHELL_ALLOWED_COMMANDS` is unset, `ShellTool.execute()` returns `ToolResult(success=False, error="Shell commands are disabled...")` for any input
- [ ] When set to `"ls,cat,python"`, only `ls`, `cat`, and `python` invocations are allowed; all others return `ToolResult(success=False, ...)`
- [ ] The `dangerous_patterns` list is removed from `execute()`
- [ ] `_SHELL_METACHARS` check still runs before the allowlist check (preserved as defense-in-depth)
- [ ] New test `tests/tools/test_shell_tool_security.py` passes with bypass corpus
- [ ] `pre-commit run --all-files` exits 0
- [ ] `python -m pytest tests/tools/test_shell_tool_security.py -v` exits 0

---

## Implementation Plan

1. **Open** `agentic-workflows-v2/agentic_v2/tools/builtin/shell_ops.py`.

2. **Add** a module-level helper to load and parse the allowlist:

```python
import os

def _load_shell_allowlist() -> frozenset[str] | None:
    """Return the set of allowed command names, or None if env var is unset."""
    raw = os.environ.get("AGENTIC_SHELL_ALLOWED_COMMANDS", "").strip()
    if not raw:
        return None
    return frozenset(name.strip().lower() for name in raw.split(",") if name.strip())
```

3. **Replace** the `dangerous_patterns` blocklist in `ShellTool.execute()`. The method currently starts with:

```python
async def execute(self, command: str, cwd: str = ".", timeout: float = 60.0, capture_output: bool = True) -> ToolResult:
    try:
        dangerous_patterns = [...]
        cmd_lower = command.lower()
        if any(pattern in cmd_lower for pattern in dangerous_patterns):
            return ToolResult(success=False, error="Command contains potentially dangerous operations...")
        ...
```

Replace the blocklist section with:

```python
async def execute(self, command: str, cwd: str = ".", timeout: float = 60.0, capture_output: bool = True) -> ToolResult:
    try:
        # Load allowlist — fail-closed when env var is unset
        allowed = _load_shell_allowlist()
        if allowed is None:
            return ToolResult(
                success=False,
                error=(
                    "Shell commands are disabled. "
                    "Set AGENTIC_SHELL_ALLOWED_COMMANDS to a comma-separated list "
                    "of permitted command names (e.g. 'ls,cat,python')."
                ),
            )

        # Verify working directory
        cwd_path = Path(cwd)
        if not cwd_path.exists():
            return ToolResult(success=False, error=f"Working directory does not exist: {cwd}")

        # Parse command — rejects shell metacharacters
        try:
            cmd_list = _split_command(command)
        except ValueError as exc:
            return ToolResult(success=False, error=str(exc))

        if not cmd_list:
            return ToolResult(success=False, error="Command must not be empty")

        # Allowlist check: compare the resolved executable name
        exe = Path(cmd_list[0]).name.lower()
        if exe not in allowed:
            return ToolResult(
                success=False,
                error=f"Command '{exe}' is not in the shell allowlist. "
                      f"Add it to AGENTIC_SHELL_ALLOWED_COMMANDS to permit it.",
            )

        # Execute command without a shell ...
        # (rest of execution logic unchanged)
```

4. **Remove** the `dangerous_patterns` list and `cmd_lower` variable entirely from `execute()`.

5. **Create** `agentic-workflows-v2/tests/tools/test_shell_tool_security.py`:

```python
"""Security corpus for ShellTool.

Verifies that the env-driven allowlist correctly rejects bypass attempts
that would defeat a substring blocklist.
"""

import os
import pytest
from unittest.mock import patch

from agentic_v2.tools.builtin.shell_ops import ShellTool


def _tool_with_allowlist(allowed: str) -> ShellTool:
    return ShellTool()


# ---------------------------------------------------------------------------
# Fail-closed: no env var
# ---------------------------------------------------------------------------

async def test_fail_closed_when_allowlist_unset():
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("AGENTIC_SHELL_ALLOWED_COMMANDS", None)
        tool = ShellTool()
        result = await tool.execute("ls")
    assert result.success is False
    assert "AGENTIC_SHELL_ALLOWED_COMMANDS" in result.error


# ---------------------------------------------------------------------------
# Allowlist enforcement
# ---------------------------------------------------------------------------

async def test_allowed_command_executes(tmp_path):
    with patch.dict(os.environ, {"AGENTIC_SHELL_ALLOWED_COMMANDS": "echo"}):
        tool = ShellTool()
        result = await tool.execute("echo hello", cwd=str(tmp_path))
    assert result.success is True


async def test_disallowed_command_rejected(tmp_path):
    with patch.dict(os.environ, {"AGENTIC_SHELL_ALLOWED_COMMANDS": "ls"}):
        tool = ShellTool()
        result = await tool.execute("curl http://example.com", cwd=str(tmp_path))
    assert result.success is False


# ---------------------------------------------------------------------------
# Bypass corpus — all must be rejected even with allowlist containing 'curl'
# ---------------------------------------------------------------------------
# These inputs try to run curl via paths that defeated the old blocklist.

_CURL_BYPASS_ATTEMPTS = [
    "curl  http://evil.com",          # double-space
    "/usr/bin/curl http://evil.com",  # absolute path (exe name extraction handles this)
    "CURL http://evil.com",           # uppercase (allowlist is lowercase-normalised)
    "\uff43\uff55\uff52\uff4c http://evil.com",  # fullwidth chars (not in allowlist)
]

@pytest.mark.parametrize("cmd", _CURL_BYPASS_ATTEMPTS)
async def test_blocklist_bypass_corpus_rejected(cmd: str, tmp_path):
    """Without 'curl' in the allowlist, all bypass attempts must be rejected."""
    with patch.dict(os.environ, {"AGENTIC_SHELL_ALLOWED_COMMANDS": "ls,echo"}):
        tool = ShellTool()
        result = await tool.execute(cmd, cwd=str(tmp_path))
    assert result.success is False


# ---------------------------------------------------------------------------
# Metachar corpus — must be rejected by _split_command before allowlist check
# ---------------------------------------------------------------------------

_METACHAR_CORPUS = [
    "ls; cat /etc/passwd",
    "ls && curl http://evil.com",
    "ls | nc -l 4444",
    "ls `id`",
    "ls $(id)",
    "ls > /tmp/out",
    "ls < /dev/null",
]

@pytest.mark.parametrize("cmd", _METACHAR_CORPUS)
async def test_metachar_corpus_rejected(cmd: str, tmp_path):
    """Shell metacharacters must be rejected regardless of allowlist."""
    with patch.dict(os.environ, {"AGENTIC_SHELL_ALLOWED_COMMANDS": "ls,cat,curl"}):
        tool = ShellTool()
        result = await tool.execute(cmd, cwd=str(tmp_path))
    assert result.success is False
```

6. **Run** `pre-commit run --all-files`.

7. **Run** `python -m pytest tests/tools/test_shell_tool_security.py -v`.

---

## Test Plan

| Test | Type | Pass condition |
|---|---|---|
| `test_fail_closed_when_allowlist_unset` | Security | `success=False`, error mentions env var |
| `test_allowed_command_executes` | Regression | `success=True` for `echo hello` |
| `test_disallowed_command_rejected` | Security | `success=False` for `curl` when only `ls` allowed |
| `test_blocklist_bypass_corpus_rejected` (4) | Security corpus | All `success=False` |
| `test_metachar_corpus_rejected` (7) | Security corpus | All `success=False` |

---

## Risks / Pitfalls

| Risk | Mitigation |
|---|---|
| Existing workflow YAMLs that use `ShellTool` will break if `AGENTIC_SHELL_ALLOWED_COMMANDS` is not set | Search: `grep -r '"shell"\|shell_tool\|ShellTool' agentic_v2/workflows/definitions/`. Update workflow docs to set the env var for demos. The sprint plan flags this as a known risk — land behind feature flag first. |
| `Path(cmd_list[0]).name.lower()` on Windows returns `ls.exe` not `ls` | Strip `.exe` suffix on Windows: `exe = Path(cmd_list[0]).stem.lower()` |
| Allowlist loaded once per call from `os.environ` — OK for tests with `patch.dict` | The `_load_shell_allowlist()` function reads `os.environ` at call time, so patching in tests works correctly. |
| `/usr/bin/curl` → `Path("/usr/bin/curl").name` → `"curl"` — correct | This is the intended behavior: full-path commands are checked by their basename. |
| Test for fullwidth `\uff43\uff55\uff52\uff4c` — `shlex.split()` may fail on non-ASCII | If `shlex.split()` raises `ValueError`, `_split_command()` returns the error and the call is rejected before the allowlist check. Still `success=False`. |

---

## Not in Scope

- Changing `ShellExecTool`
- Adding logging of rejected commands (deferred — don't log user-controlled command strings to prevent log injection)
- Making the allowlist persistent across restarts (env var is sufficient)
- Adding a per-workflow allowlist override

---

## Verification

```bash
# From agentic-workflows-v2/

# 1. Lint + format
pre-commit run --all-files

# 2. Type check
python -m mypy agentic_v2/tools/builtin/shell_ops.py --ignore-missing-imports

# 3. Security corpus
python -m pytest tests/tools/test_shell_tool_security.py -v

# 4. Full tools test suite
python -m pytest tests/tools/ -v --tb=short

# 5. Verify dangerous_patterns list is gone
grep -n "dangerous_patterns" agentic_v2/tools/builtin/shell_ops.py
# Expected: no output

# 6. Search for shell tool usage in workflows
grep -r '"shell"\|ShellTool' agentic_v2/workflows/definitions/
# Review any hits — those workflows need AGENTIC_SHELL_ALLOWED_COMMANDS in their docs
```

---

## Dependencies

None. This ticket is self-contained and has no upstream dependencies.
