# Sprint 1 — Ticket 03

## Header

| Field | Value |
|---|---|
| Sprint | 1 |
| Ticket ID | S1-03 |
| Title | `run_id` path-traversal test corpus |
| Points | 2 |
| Value | 6 |
| T-shirt | S |
| V/E | 3.00 |
| Phase ref | Sec M5, Test H5 |
| Source finding | `05-final-report.md` High Test H5 |
| Status | Partially resolved — validator exists; test corpus missing |

---

## Agent Persona

**Agent:** `tdd-guide` (`.claude/agents/tdd-guide.md`)

**Role:** Test-first Python Engineer adding security regression coverage for `run_id` path traversal.

**Expertise areas:**
- pytest parametrize and negative-test corpora
- Pydantic v2 `field_validator` and `ValidationError` semantics
- Security test design: path traversal, null-byte injection, unicode normalization
- FastAPI `TestClient` / `httpx.AsyncClient` for endpoint-level tests

**Boundaries:**
- Do not change the `_validate_run_id` validator logic — it already exists and is correct
- Do not change any model fields other than adding test coverage
- Do not add new validators or constraints beyond what the ticket specifies
- Do not modify production route code

**Critical rules:**
- No `@pytest.mark.asyncio` — asyncio_mode=auto is configured
- All test assertions must be verifiable by running pytest, not by visual inspection
- Pydantic v2 raises `ValidationError` on field_validator failures — import from `pydantic`

**Output format:** One new test file. No production code changes. Pre-commit green. pytest green.

---

## Problem Statement

**Why this matters:** The `run_id` field in `WorkflowRunRequest` is used to name run directories and appears in log messages. Path traversal via `run_id` (e.g., `../../etc/passwd`, `../../../windows/system32`) could escape the intended run storage directory if any code later uses `run_id` to construct file paths.

**Current state:** A `field_validator("run_id")` exists at `server/models.py:81-90`:
```python
@field_validator("run_id")
@classmethod
def _validate_run_id(cls, v: str | None) -> str | None:
    if v is None:
        return v
    if not re.match(r"^[a-zA-Z0-9_-]{1,128}$", v):
        raise ValueError(
            "run_id must be 1-128 characters using only letters, digits, hyphens, and underscores"
        )
    return v
```

The validator is correct and was present at the review cut (commit `10c84cc`). The finding (Test H5) is that **no test coverage** exists for path-traversal inputs. This ticket adds that coverage.

**Finding closed:** `05-final-report.md` High Test H5 — "`run_id` path traversal untested."

---

## Scope

**In scope:**
- Add `tests/server/test_run_id_validation.py` with:
  - A parametrized path traversal corpus (at least 12 adversarial inputs)
  - Tests for valid `run_id` values (regression)
  - Tests for `None` (allowed) and empty string (rejected)
  - A null-byte injection test
  - A unicode/fullwidth injection test

**Explicitly out of scope:**
- Changing the validator length limit (128 vs. 64 — the 128 limit is already deployed; the sprint plan suggested 64 but the live code uses 128; do not regress existing behavior)
- Changing any route or handler code
- Adding endpoint-level integration tests (the validator fires at model instantiation, so unit tests are sufficient)

---

## Acceptance Criteria

- [ ] `tests/server/test_run_id_validation.py` exists and passes
- [ ] Corpus includes at minimum: `../etc/passwd`, `../../windows/system32`, `.`, `..`, `../`, null-byte injection, unicode fullwidth, shell metachar injection (`; rm -rf /`), slash-only path
- [ ] All adversarial inputs result in `ValidationError` being raised
- [ ] Valid `run_id` values (`my-run_01`, `abc`, `A1-B2_C3`) do not raise
- [ ] `None` does not raise (allowed per validator)
- [ ] `pre-commit run --all-files` exits 0
- [ ] `python -m pytest tests/server/test_run_id_validation.py -v` exits 0

---

## Implementation Plan

1. **Create** `agentic-workflows-v2/tests/server/test_run_id_validation.py`:

```python
"""Regression tests for WorkflowRunRequest.run_id path-traversal protection.

The field_validator at server/models.py:81-90 uses ^[a-zA-Z0-9_-]{1,128}$
which rejects anything outside alphanumeric + hyphen + underscore.
These tests form the canonical negative corpus.
"""

import pytest
from pydantic import ValidationError

from agentic_v2.server.models import WorkflowRunRequest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_request(run_id: str | None) -> WorkflowRunRequest:
    return WorkflowRunRequest(workflow="test_wf", run_id=run_id)


# ---------------------------------------------------------------------------
# Positive cases (must NOT raise)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("valid_id", [
    "my-run_01",
    "abc",
    "A1-B2_C3",
    "a" * 128,           # max length
    "RUN-2026-04-27",
    "sprint1_ticket03",
])
def test_valid_run_id_accepted(valid_id: str):
    req = _make_request(valid_id)
    assert req.run_id == valid_id


def test_none_run_id_accepted():
    req = _make_request(None)
    assert req.run_id is None


# ---------------------------------------------------------------------------
# Path traversal corpus (must ALL raise ValidationError)
# ---------------------------------------------------------------------------

_PATH_TRAVERSAL_CORPUS = [
    "../etc/passwd",
    "../../windows/system32",
    "../../.env",
    "../../../root/.ssh/id_rsa",
    ".",
    "..",
    "../",
    "./",
    "/etc/passwd",
    "/root",
    "\\..\\..\\windows",
    "run/../../../etc",
]

@pytest.mark.parametrize("bad_id", _PATH_TRAVERSAL_CORPUS)
def test_path_traversal_rejected(bad_id: str):
    with pytest.raises(ValidationError):
        _make_request(bad_id)


# ---------------------------------------------------------------------------
# Injection corpus
# ---------------------------------------------------------------------------

_INJECTION_CORPUS = [
    "run; rm -rf /",          # shell metachar
    "run && cat /etc/passwd",  # chained command
    "run`id`",                  # backtick substitution
    "run$(id)",                 # dollar substitution
    "run\x00etc",              # null byte
    "run\necho injected",      # newline injection
    "\uff52\uff55\uff4e",      # unicode fullwidth (r-u-n)
    "run<script>",             # HTML injection
    "a" * 129,                 # exceeds max length
    "",                        # empty string
    " ",                       # whitespace only
    "run id",                  # space in id
]

@pytest.mark.parametrize("bad_id", _INJECTION_CORPUS)
def test_injection_corpus_rejected(bad_id: str):
    with pytest.raises(ValidationError):
        _make_request(bad_id)
```

2. **Run** `pre-commit run --all-files`.

3. **Run** `python -m pytest tests/server/test_run_id_validation.py -v`.

---

## Test Plan

| Test group | Count | Pass condition |
|---|---|---|
| `test_valid_run_id_accepted` | 6 parametrized | No exception raised |
| `test_none_run_id_accepted` | 1 | `req.run_id is None` |
| `test_path_traversal_rejected` | 12 parametrized | `ValidationError` raised |
| `test_injection_corpus_rejected` | 12 parametrized | `ValidationError` raised |

**Total:** 31 test cases, all self-contained unit tests with zero I/O.

---

## Risks / Pitfalls

| Risk | Mitigation |
|---|---|
| Pydantic v2 `ValidationError` import path changed | Import from `pydantic`, not `pydantic.error_wrappers`. |
| `WorkflowRunRequest` requires other mandatory fields | Pass `workflow="test_wf"` as the only required field — all others have defaults. |
| Empty string `""` currently passes if validator only checks `None` | The regex `^[a-zA-Z0-9_-]{1,128}$` requires at least 1 character, so `""` correctly raises. Verified by reading the validator. |
| Unicode fullwidth characters `\uff52` look like ASCII `r` but are outside `[a-zA-Z0-9_-]` | The regex is byte/codepoint-level, so fullwidth chars are correctly rejected without normalization. Test still valuable as a demonstration. |

---

## Not in Scope

- Changing the `_validate_run_id` validator
- Changing the length limit from 128 to 64 (would be a breaking change for existing runs; defer to a separate decision)
- Adding endpoint-level POST tests (the validator fires on model instantiation, so unit tests cover the full behavior)
- Adding `run_id` sanitization to the run storage path (if `run_id` is used to construct paths elsewhere, that is a separate finding)

---

## Verification

```bash
# From agentic-workflows-v2/

# 1. Lint + format
pre-commit run --all-files

# 2. Run the new tests
python -m pytest tests/server/test_run_id_validation.py -v

# 3. Confirm no production files changed
git diff --name-only HEAD | grep -v "tests/"
# Expected: no output (only test file added)
```

---

## Dependencies

None. This ticket adds tests only and has no upstream dependencies.
