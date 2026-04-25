# Sprint 1 — Ticket 02

## Header

| Field | Value |
|---|---|
| Sprint | 1 |
| Ticket ID | S1-02 |
| Title | `file_ops` fail-closed when `AGENTIC_FILE_BASE_DIR` unset |
| Points | 2 |
| Value | 8 |
| T-shirt | S |
| V/E | 4.00 |
| Phase ref | Sec H3 (promoted Critical), Test H2 |
| Source finding | `05-final-report.md` Critical #5 |
| Status | Open |

---

## Agent Persona

**Agent:** `security-reviewer` (`.claude/agents/security-reviewer.md`)

**Role:** Security-focused Python Engineer enforcing path containment in file operation tools.

**Expertise areas:**
- Path traversal attack prevention and `pathlib.Path.resolve()` semantics
- Environment variable-driven configuration with fail-closed defaults
- pytest parametrize for exhaustive path traversal corpora
- Pydantic v2 Settings classes and `get_settings()` patterns

**Boundaries:**
- Do not change `ensure_within_base()` in `utils/path_safety.py` — it is correct
- Do not touch the `file_read`/`file_write`/`file_copy`/`file_move`/`file_delete`/`directory_create` execute methods
- Do not add new tool classes
- Do not change Docker or CI configuration

**Critical rules:**
- The change must be backward-compatible via env var: setting `AGENTIC_FILE_BASE_DIR` to a valid directory must restore current behavior
- `pathlib.Path` for all path handling — no raw string concatenation
- No `@pytest.mark.asyncio` — asyncio_mode=auto is configured
- All edits trigger ruff fix + format via post-commit hook

**Output format:** One file changed (`file_ops.py`, ~5 lines), one test file added. Pre-commit green. pytest green.

---

## Problem Statement

**Why this matters:** When the `AGENTIC_FILE_BASE_DIR` environment variable is not set, `_validate_path()` in `file_ops.py` is a no-op — it simply resolves the path and returns it. This means any file tool (file_read, file_write, file_delete, etc.) accepts absolute paths including `/etc/passwd`, `/root/.ssh/id_rsa`, or any path on the developer's filesystem.

An LLM agent with prompt injection can silently exfiltrate API keys stored in `~/.env`, write to system files, or delete arbitrary paths. The `.env.example` ships with `AGENTIC_FILE_BASE_DIR` empty, so every default installation is fail-open.

**Blast radius:** All 7 file tools (`FileCopyTool`, `FileMoveTool`, `FileDeleteTool`, `DirectoryCreateTool`, `FileReadTool`, `FileWriteTool`, `FileAppendTool` if present) in any workflow that includes file operations.

**Finding closed:** `05-final-report.md` Critical #5 (Sec H3 promoted) — "`file_ops.py:15-32` + `.env.example:98` ships `AGENTIC_FILE_BASE_DIR` empty. Agent can `file_read('/etc/passwd')`. Fix: fail-closed when unset."

**Current code (`file_ops.py` lines 15-32):**
```python
_FILE_BASE_DIR: str | None = _get_settings().agentic_file_base_dir

def _validate_path(path: str) -> Path:
    if _FILE_BASE_DIR:
        return ensure_within_base(path, _FILE_BASE_DIR)
    return Path(path).resolve()  # NO-OP when unset — fail-open
```

---

## Scope

**In scope:**
- Modify `_validate_path()` to raise `ValueError` when `AGENTIC_FILE_BASE_DIR` is unset or empty
- Add a test that verifies file_read (and at least file_write) returns an error result when the env var is unset
- Add a parametrized path-traversal test corpus

**Explicitly out of scope:**
- Changing `ensure_within_base()` in `utils/path_safety.py`
- Changing the execute() methods on any tool class
- Modifying `.env.example` (that is a docs/DevEx item in Sprint 5)
- Adding a UI warning about the unset variable

---

## Acceptance Criteria

- [ ] When `AGENTIC_FILE_BASE_DIR` is unset or empty, `_validate_path()` raises `ValueError` with a clear message: `"AGENTIC_FILE_BASE_DIR must be set to use file tools"`
- [ ] All file tools return `ToolResult(success=False, error="AGENTIC_FILE_BASE_DIR must be set...")` when the env var is unset (they already catch `ValueError` from `_validate_path`)
- [ ] When `AGENTIC_FILE_BASE_DIR` is set to a valid directory, existing behavior is preserved (path contained within base dir, traversal still rejected by `ensure_within_base`)
- [ ] New test `tests/tools/test_file_ops_containment.py::test_fail_closed_when_base_dir_unset` passes
- [ ] New test `tests/tools/test_file_ops_containment.py::test_path_traversal_corpus` passes with traversal attempts returning error results
- [ ] `pre-commit run --all-files` exits 0
- [ ] `python -m pytest tests/tools/ -v` exits 0

---

## Implementation Plan

1. **Open** `agentic-workflows-v2/agentic_v2/tools/builtin/file_ops.py`.

2. **Change** `_validate_path()` (lines 21-32). Replace:
   ```python
   def _validate_path(path: str) -> Path:
       if _FILE_BASE_DIR:
           return ensure_within_base(path, _FILE_BASE_DIR)
       return Path(path).resolve()
   ```
   With:
   ```python
   def _validate_path(path: str) -> Path:
       if not _FILE_BASE_DIR:
           raise ValueError(
               "AGENTIC_FILE_BASE_DIR must be set to use file tools. "
               "Set it to the directory agents are allowed to read and write."
           )
       return ensure_within_base(path, _FILE_BASE_DIR)
   ```

3. **Create** `agentic-workflows-v2/tests/tools/test_file_ops_containment.py`:
   ```python
   import os
   import pytest
   from unittest.mock import patch


   # ---------------------------------------------------------------------------
   # Helpers
   # ---------------------------------------------------------------------------

   def _import_tools():
       """Re-import file_ops with a fresh module state so _FILE_BASE_DIR picks
       up the patched environment."""
       import importlib
       import agentic_v2.tools.builtin.file_ops as mod
       importlib.reload(mod)
       return mod


   # ---------------------------------------------------------------------------
   # Fail-closed tests
   # ---------------------------------------------------------------------------

   async def test_file_read_fail_closed_when_base_dir_unset(tmp_path):
       """file_read must return error when AGENTIC_FILE_BASE_DIR is not set."""
       (tmp_path / "secret.txt").write_text("secret content")
       with patch.dict(os.environ, {}, clear=False):
           os.environ.pop("AGENTIC_FILE_BASE_DIR", None)
           mod = _import_tools()
           tool = mod.FileReadTool()
           result = await tool.execute(str(tmp_path / "secret.txt"))
       assert result.success is False
       assert "AGENTIC_FILE_BASE_DIR" in result.error


   async def test_file_write_fail_closed_when_base_dir_unset(tmp_path):
       with patch.dict(os.environ, {}, clear=False):
           os.environ.pop("AGENTIC_FILE_BASE_DIR", None)
           mod = _import_tools()
           tool = mod.FileWriteTool()
           result = await tool.execute(str(tmp_path / "out.txt"), "hello")
       assert result.success is False
       assert "AGENTIC_FILE_BASE_DIR" in result.error


   async def test_file_ops_work_when_base_dir_set(tmp_path):
       """Sanity: tools still work when the env var is set."""
       with patch.dict(os.environ, {"AGENTIC_FILE_BASE_DIR": str(tmp_path)}):
           mod = _import_tools()
           tool = mod.FileWriteTool()
           result = await tool.execute(str(tmp_path / "out.txt"), "hello")
       assert result.success is True


   # ---------------------------------------------------------------------------
   # Path traversal corpus
   # ---------------------------------------------------------------------------

   _TRAVERSAL_ATTEMPTS = [
       "/etc/passwd",
       "/root/.ssh/id_rsa",
       "../../etc/shadow",
       "../../../windows/system32/cmd.exe",
       "/proc/self/environ",
       "~/.aws/credentials",
   ]


   @pytest.mark.parametrize("bad_path", _TRAVERSAL_ATTEMPTS)
   async def test_path_traversal_rejected(tmp_path, bad_path):
       """Every traversal attempt must return success=False."""
       with patch.dict(os.environ, {"AGENTIC_FILE_BASE_DIR": str(tmp_path)}):
           mod = _import_tools()
           tool = mod.FileReadTool()
           result = await tool.execute(bad_path)
       assert result.success is False
   ```

4. **Run** `pre-commit run --all-files` from repo root.

5. **Run** `python -m pytest tests/tools/test_file_ops_containment.py -v`.

---

## Test Plan

| Test | Type | Pass condition |
|---|---|---|
| `test_file_read_fail_closed_when_base_dir_unset` | Security / adversarial | `success=False`, error mentions `AGENTIC_FILE_BASE_DIR` |
| `test_file_write_fail_closed_when_base_dir_unset` | Security / adversarial | Same |
| `test_file_ops_work_when_base_dir_set` | Regression | `success=True` |
| `test_path_traversal_rejected[...]` (6 parametrized) | Security corpus | All `success=False` |

---

## Risks / Pitfalls

| Risk | Mitigation |
|---|---|
| `_FILE_BASE_DIR` is resolved at module import time via `_get_settings()`, so monkeypatching `os.environ` after import won't affect the already-resolved module-level constant | The test reloads the module via `importlib.reload()` after patching the env. Note: reload semantics can be fragile if the module has side effects at load time — verify it doesn't. |
| Reloading the module in tests may conflict with other tests that import it normally | Use `importlib.reload()` only within these specific tests; restore with a fixture `autouse=False`. |
| Existing integration tests that call file tools without setting `AGENTIC_FILE_BASE_DIR` will now fail | Search for all test files that invoke file tools: `grep -r "FileReadTool\|FileWriteTool\|file_read\|file_write" tests/`. Update those tests to set `AGENTIC_FILE_BASE_DIR=tmp_path` via a pytest fixture. |

**Before landing this ticket**, run the full test suite to discover any callers that need `AGENTIC_FILE_BASE_DIR` added:
```bash
python -m pytest tests/ -v -k "file" 2>&1 | grep FAILED
```

---

## Not in Scope

- Changing `ensure_within_base()` in `utils/path_safety.py`
- Modifying `.env.example` or documentation (Sprint 5 DevEx ticket)
- Adding `AGENTIC_FILE_BASE_DIR` to CI environment (Sprint 5 ticket)
- Any changes to the execute() methods in file tool classes

---

## Verification

```bash
# From agentic-workflows-v2/

# 1. Lint + format
pre-commit run --all-files

# 2. Type check the changed file
python -m mypy agentic_v2/tools/builtin/file_ops.py --ignore-missing-imports

# 3. Run new containment tests
python -m pytest tests/tools/test_file_ops_containment.py -v

# 4. Run full test suite to catch regressions in callers
python -m pytest tests/ -v --tb=short 2>&1 | tail -20

# 5. Confirm the no-op path is gone
grep -n "return Path(path).resolve()" agentic_v2/tools/builtin/file_ops.py
# Expected: no output (line deleted)
```

---

## Dependencies

None. This ticket has no upstream dependencies and can land on day 1 of the sprint.
