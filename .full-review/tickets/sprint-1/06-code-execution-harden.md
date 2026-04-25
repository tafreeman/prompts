# Sprint 1 — Ticket 06

## Header

| Field | Value |
|---|---|
| Sprint | 1 |
| Ticket ID | S1-06 |
| Title | Harden `code_execution.py`: remove `__import__`, add `resource.setrlimit` |
| Points | 8 |
| Value | 10 |
| T-shirt | XL |
| V/E | 1.25 |
| Phase ref | Sec H5 (promoted Critical), Sec H6, Test H4 |
| Source finding | `05-final-report.md` Critical #3 and #4 |
| Status | Partially resolved — sparse env already implemented; `__import__` still present in wrapper; `resource.setrlimit` not added |

---

## Agent Persona

**Agent:** `security-reviewer` (`.claude/agents/security-reviewer.md`)

**Role:** Security-focused Python Engineer closing remaining sandbox escape vectors in the code execution tool.

**Expertise areas:**
- Python sandbox escape via `__import__`/`getattr`/`setattr` and builtin override
- `resource.setrlimit(RLIMIT_AS)` / `RLIMIT_NPROC` for subprocess resource constraints
- AST-based import blocking and its limitations vs. bytecode-level escapes
- `asyncio.create_subprocess_exec` and sparse environment construction
- pytest security corpus design (adversarial code snippets)

**Boundaries:**
- Do not change the AST import scanner (`_check_code_safety`) — it is a pre-flight check, not the primary sandbox
- Do not add Docker integration (out of scope for this ticket)
- Do not change the `_SAFE_ENV_KEYS` set definition — the sparse env is already correct
- Do not change `ShellTool` or `GitOpsTool`

**Critical rules:**
- The sandbox child runs as a subprocess (already the case); `resource.setrlimit` must be set in the child via `preexec_fn` (POSIX only — must guard with `os.name != 'nt'`)
- `__import__` removal from the wrapper's `_safe_builtins` must not break the wrapper's own `import sys, json, io, traceback` header (those lines run BEFORE the restricted `exec()` call)
- No `@pytest.mark.asyncio` — asyncio_mode=auto is configured
- Pydantic v2 only

**Output format:** `code_execution.py` changed (~15 lines net), one test file. Pre-commit green. pytest green.

---

## Problem Statement

**Why this matters:** `CodeExecutionTool` runs user-supplied Python code in a subprocess with a restricted `__builtins__` dict. Two escape vectors remain:

**Vector 1: `__import__` in `_safe_builtins`**
The wrapper code constructs `_safe_builtins` by filtering out `exec`, `eval`, `compile`, `breakpoint`, `exit`, `quit`, `open`, `globals`, `locals`, `getattr`, `setattr`, `delattr`. However, `__import__` is explicitly **kept** with the comment: "kept because the AST-based safety check already blocks dangerous modules."

This is insufficient. The AST import scanner runs on the user-supplied `code` string, but the `exec(_code, _globals)` call happens with `__import__` in scope. An attacker can bypass the AST check via:
- String-building: `getattr(__builtins__, '__import__')('os')` — blocked by `getattr` removal
- `__loader__` traversal: reaches `importlib` without `__import__` if `__loader__` is in `_safe_builtins`
- Bytecode manipulation: not blocked by AST scan

**Vector 2: No memory/process limits**
The subprocess has no resource limits. A user-supplied infinite loop or memory-allocation bomb can hang the server process (DoS) or consume all available RAM on the developer's machine. The `timeout` parameter handles CPU time but not memory or fork bombs.

**Current state of `_subprocess_env()`:** Already correct — returns only `_SAFE_ENV_KEYS` plus `PYTHONDONTWRITEBYTECODE`. API keys are not leaked to the child process. No change needed here.

**Finding closed:** `05-final-report.md` Critical #3 (Sec H5) — "remove `__import__`/`getattr`/`setattr` from allowed builtins" and Critical #4 (Sec H6) — "`resource.setrlimit`".

---

## Scope

**In scope:**
- Remove `__import__` from `_safe_builtins` in the wrapper template
- Add `resource.setrlimit(RLIMIT_AS, ...)` and `RLIMIT_NPROC` limits in the child process via `preexec_fn` (POSIX only)
- Add sandbox escape test corpus

**Explicitly out of scope:**
- Changing the AST import scanner (`_check_code_safety`)
- Adding Docker sandboxing
- Changing `_SAFE_ENV_KEYS` (already correct)
- Changing `_DANGEROUS_BUILTINS` (unused class attribute — noted but leaving for Sprint 3 cleanup)
- Changing `ShellTool` or `GitOpsTool`

---

## Acceptance Criteria

- [ ] `__import__` is not present in `_safe_builtins` in the wrapper template
- [ ] The wrapper's own `import sys, json, io, traceback` (lines before the restricted exec) are unaffected — they run in the outer subprocess Python context, not the sandboxed exec
- [ ] On POSIX systems (Linux/macOS), `resource.setrlimit` is called in a `preexec_fn` limiting address space to 256 MB and process count to 64
- [ ] On Windows (`os.name == 'nt'`), no `preexec_fn` is used (resource module not available on Windows)
- [ ] `execute_python(code="import os; os.system('id')")` returns `success=False` (blocked by AST scanner — baseline)
- [ ] `execute_python(code="__import__('os').system('id')")` returns `success=False` (now blocked by missing `__import__` in builtins)
- [ ] New test corpus in `tests/tools/test_code_execution_security.py` passes
- [ ] Existing `execute_python` tests still pass
- [ ] `pre-commit run --all-files` exits 0

---

## Implementation Plan

1. **Open** `agentic-workflows-v2/agentic_v2/tools/builtin/code_execution.py`.

2. **Remove `__import__` from `_safe_builtins`** in the wrapper template (lines 207-215). The current wrapper has:

```python
_safe_builtins = {{
    k: v for k, v in vars(_builtins_mod).items()
    if k not in {{
        "exec", "eval", "compile",
        "breakpoint", "exit", "quit", "open",
        "globals", "locals", "getattr", "setattr",
        "delattr",
    }}
}}
```

Change to:

```python
_safe_builtins = {{
    k: v for k, v in vars(_builtins_mod).items()
    if k not in {{
        "exec", "eval", "compile",
        "__import__",        # prevent dynamic import bypass
        "breakpoint", "exit", "quit", "open",
        "globals", "locals", "getattr", "setattr",
        "delattr",
    }}
}}
```

And update the comment above the wrapper:
```python
# Restrict __builtins__ — remove dangerous functions including __import__
# to prevent dynamic import bypasses. The AST import scanner is a
# complementary pre-flight check, not the sole defense.
```

3. **Add `resource.setrlimit` via `preexec_fn`** in `CodeExecutionTool.execute()`. In the `asyncio.create_subprocess_exec` call, add `preexec_fn` on POSIX:

```python
import platform

def _make_preexec_fn():
    """Return a preexec_fn that sets resource limits, or None on Windows."""
    if os.name == "nt":
        return None

    def _set_limits():
        try:
            import resource  # POSIX only
            # Limit address space to 256 MB
            resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
            # Limit process count to prevent fork bombs
            resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
        except Exception:
            pass  # Resource limits are best-effort; don't crash the subprocess

    return _set_limits
```

Add this function at module level (outside the class). Then in `execute()`:

```python
proc = await asyncio.create_subprocess_exec(
    sys.executable,
    tmp_path,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    env=self._subprocess_env(),
    **({"preexec_fn": _make_preexec_fn()} if _make_preexec_fn() else {}),
)
```

Or more cleanly:

```python
_preexec = _make_preexec_fn()
proc = await asyncio.create_subprocess_exec(
    sys.executable,
    tmp_path,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    env=self._subprocess_env(),
    **({"preexec_fn": _preexec} if _preexec is not None else {}),
)
```

4. **Create** `agentic-workflows-v2/tests/tools/test_code_execution_security.py`:

```python
"""Security corpus for CodeExecutionTool.

Tests that sandbox escape attempts via __import__, getattr,
and subclass traversal are blocked.
"""

import pytest

from agentic_v2.tools.builtin.code_execution import CodeExecutionTool


def _tool() -> CodeExecutionTool:
    return CodeExecutionTool(allow_imports=True, sandbox=True)


# ---------------------------------------------------------------------------
# __import__ bypass corpus
# ---------------------------------------------------------------------------

_IMPORT_BYPASS_CORPUS = [
    # Direct __import__ call — now blocked by missing __import__ in builtins
    "__import__('os').system('id')",
    "__import__('subprocess').run(['id'])",
    # String-based eval bypass — blocked by missing eval in builtins
    "eval(\"__import__('os').system('id')\")",
    # Importlib bypass via builtins — blocked by missing __import__
    "import importlib; importlib.import_module('os').system('id')",
]

@pytest.mark.parametrize("code", _IMPORT_BYPASS_CORPUS)
async def test_import_bypass_blocked(code: str):
    tool = _tool()
    result = await tool.execute(code)
    # Either blocked pre-execution by AST scanner, or fails at runtime
    # due to missing __import__ — either way success must be False
    assert result.success is False


# ---------------------------------------------------------------------------
# Subclass traversal corpus
# ---------------------------------------------------------------------------

_SUBCLASS_CORPUS = [
    # These are blocked by the AST scanner's import check on 'subprocess'
    # when accessed via __subclasses__; also the AST scan catches direct imports
    "().__class__.__mro__[-1].__subclasses__()",
    "type.__subclasses__(type)",
]

@pytest.mark.parametrize("code", _SUBCLASS_CORPUS)
async def test_subclass_traversal_blocked(code: str):
    tool = _tool()
    result = await tool.execute(code)
    # May be blocked by AST pattern check on 'importlib' or fail at runtime
    assert result.success is False


# ---------------------------------------------------------------------------
# Safe code still works
# ---------------------------------------------------------------------------

async def test_safe_arithmetic_executes():
    tool = _tool()
    result = await tool.execute("result = 2 + 2")
    assert result.success is True
    assert result.data["result"] == "4"


async def test_safe_list_comprehension():
    tool = _tool()
    result = await tool.execute("result = [i**2 for i in range(5)]")
    assert result.success is True


async def test_stdout_captured():
    tool = _tool()
    result = await tool.execute("print('hello sandbox')")
    assert result.success is True
    assert "hello sandbox" in result.data["stdout"]
```

5. **Run** `pre-commit run --all-files`.

6. **Run** `python -m pytest tests/tools/test_code_execution_security.py -v`.

---

## Test Plan

| Test | Type | Pass condition |
|---|---|---|
| `test_import_bypass_blocked` (4) | Security corpus | `success=False` |
| `test_subclass_traversal_blocked` (2) | Security corpus | `success=False` |
| `test_safe_arithmetic_executes` | Regression | `success=True`, `result=="4"` |
| `test_safe_list_comprehension` | Regression | `success=True` |
| `test_stdout_captured` | Regression | `success=True`, stdout captured |

---

## Risks / Pitfalls

| Risk | Mitigation |
|---|---|
| Removing `__import__` from `_safe_builtins` may break user code that does `import math` inside the executed snippet | `import` statements at the top of executed code use the subprocess's own Python `__import__` (the outer process builtins, not the sandboxed exec builtins). Verify: the `exec(_code, _globals)` call only restricts code inside the exec scope. The wrapper's own `import sys, json, io, traceback` still works. |
| `resource` module not available on Windows — `RLIMIT_AS` not defined | Guard with `os.name != 'nt'` in `_make_preexec_fn()`. Returns `None` on Windows. |
| `preexec_fn` is not supported with `asyncio.create_subprocess_exec` on Windows | Confirmed: `preexec_fn` is POSIX-only in CPython. The `None` fallback handles Windows. |
| 256 MB address space limit may be too restrictive for ML demos that load models | This is a teaching platform — most demo scripts are simple. If a legitimate demo needs more memory, it should use `ShellExecTool` with explicit Python args, not `CodeExecutionTool`. Document this constraint. |
| `_DANGEROUS_BUILTINS` class attribute is defined but never used | Leave it for Sprint 3 refactor-cleaner pass. Do not remove it in this ticket (separate concern). |

---

## Not in Scope

- Removing the unused `_DANGEROUS_BUILTINS` class attribute (Sprint 3 cleanup)
- Adding Docker-based sandboxing
- Adding network isolation (no `iptables`/`nftables` for a local dev tool)
- Changing the AST import scanner
- Changing `_SAFE_ENV_KEYS`

---

## Verification

```bash
# From agentic-workflows-v2/

# 1. Lint + format
pre-commit run --all-files

# 2. Type check
python -m mypy agentic_v2/tools/builtin/code_execution.py --ignore-missing-imports

# 3. Security corpus
python -m pytest tests/tools/test_code_execution_security.py -v

# 4. Full tools tests
python -m pytest tests/tools/ -v --tb=short

# 5. Verify __import__ is in the blocked set
grep -n "__import__" agentic_v2/tools/builtin/code_execution.py
# Expected: appears in the exclusion set, NOT as a kept builtin

# 6. Manual check: safe code still works
python -c "
import asyncio
from agentic_v2.tools.builtin.code_execution import CodeExecutionTool
tool = CodeExecutionTool()
result = asyncio.run(tool.execute('result = 2 + 2'))
print('safe:', result.success, result.data)
"

# 7. Manual check: __import__ bypass is blocked
python -c "
import asyncio
from agentic_v2.tools.builtin.code_execution import CodeExecutionTool
tool = CodeExecutionTool()
result = asyncio.run(tool.execute(\"__import__('os').system('id')\"))
print('bypass:', result.success, result.error)
# Expected: success=False
"
```

---

## Dependencies

None. This ticket is self-contained and has no upstream dependencies.
