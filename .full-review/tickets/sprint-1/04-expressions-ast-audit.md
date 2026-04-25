# Sprint 1 — Ticket 04

## Header

| Field | Value |
|---|---|
| Sprint | 1 |
| Ticket ID | S1-04 |
| Title | Audit `expressions.py:_validate_ast`; add `__class__`/`__mro__`/`__subclasses__` negative corpus |
| Points | 3 |
| Value | 8 |
| T-shirt | M |
| V/E | 2.67 |
| Phase ref | Sec H4, Test C3 |
| Source finding | `05-final-report.md` Critical #6 |
| Status | Open — investigation required before implementation |

---

## Agent Persona

**Agent:** `security-reviewer` (`.claude/agents/security-reviewer.md`)

**Role:** Security-focused Python Engineer auditing an AST-based expression sandbox for Python dunder traversal escapes.

**Expertise areas:**
- Python AST internals (`ast.Attribute`, `ast.Subscript`, `ast.Call`, `ast.walk`)
- `eval()` sandboxing with restricted `__builtins__` — known escape vectors
- `_SafeNamespace`/`SimpleNamespace` attribute resolution and Python's data model
- pytest parametrize for security test corpora

**Boundaries:**
- Do not change the expression language semantics — `coalesce()`, dot-path access, and comparison operators must continue to work
- Do not remove `ast.Attribute`, `ast.Subscript`, or `ast.Call` from the whitelist without first verifying that no existing workflow YAML relies on them
- Do not change `_NullSafe`, `_SafeNamespace`, or `_coalesce` behavior
- Do not change `_resolve_path`, `_navigate`, or `evaluate` methods

**Critical rules:**
- Existing expression tests (`tests/engine/test_expressions.py`) must all still pass
- Any change to `_validate_ast` must be accompanied by a regression test
- No `@pytest.mark.asyncio` in this file — the evaluator is synchronous
- Pydantic v2 only throughout

**Output format:** Investigation notes inline in this ticket (fill in the `Investigation Findings` section below after reading the code), one or more targeted fixes if needed, plus the test corpus. Existing tests green. New corpus tests green.

---

## Problem Statement

**Why this matters:** `ExpressionEvaluator._safe_eval()` in `engine/expressions.py` evaluates user-controlled workflow YAML expressions using Python `eval()`. The safety fence is:

1. An AST whitelist (`_validate_ast`) that allows only specific node types
2. `eval(..., {"__builtins__": {}}, env)` where `env` contains `ctx`, `steps`, `coalesce`, and top-level context keys

The review finding (Sec H4) identifies that `ast.Attribute`, `ast.Subscript`, and `ast.Call` are all in the whitelist, which opens potential dunder traversal paths like:

```python
ctx.__class__.__mro__[-1].__subclasses__()
```

If `ctx` is a `_SafeNamespace`, `ctx.__class__` resolves to `_SafeNamespace` (Python's type system bypasses `__getattr__` for dunder access). From there, `.__mro__[-1].__subclasses__()` reaches `object.__subclasses__()` which returns all currently-loaded classes — including `subprocess.Popen` if `subprocess` has been imported anywhere in the process.

Even with `{"__builtins__": {}}`, this chain can succeed because dunder methods are resolved via the type's C-level slot, not `__builtins__`. A prompt-injected YAML condition could use this to instantiate `subprocess.Popen` and execute arbitrary commands.

**Finding closed:** `05-final-report.md` Critical #6 (Sec H4) — "Audit `_validate_ast` to confirm `ast.Attribute`/`Subscript`/`Call` rejected; add negative test corpus."

**Current `_validate_ast` whitelist (`expressions.py:417-467`):**
```python
allowed_nodes = (
    ast.Expression, ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Compare,
    ast.Name, ast.Load,
    ast.Attribute,    # <-- allows ctx.__class__.__mro__
    ast.Subscript,    # <-- allows [0][-1]
    ast.Constant,
    ast.And, ast.Or, ast.Not, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
    ast.Gt, ast.GtE, ast.In, ast.NotIn, ast.Is, ast.IsNot,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.USub, ast.UAdd,
    ast.List, ast.Tuple, ast.Dict,
    ast.Call,         # <-- allows coalesce(...) but also any_name(...)
)
```

---

## Scope

**In scope:**
1. **Investigate** whether the dunder traversal attack vector is actually exploitable given `{"__builtins__": {}}` and the `_SafeNamespace` implementation
2. **If exploitable:** Add attribute-name blocklist check on `ast.Attribute` nodes (reject any attribute name starting with `__`) to `_validate_ast`
3. **If not fully exploitable:** Document why in inline comments and add a test demonstrating the attempted attack fails
4. **Always:** Add the negative test corpus regardless of exploitability (the tests document the threat model and prevent future regressions)

**Explicitly out of scope:**
- Removing `ast.Attribute` entirely (breaks dot-path expressions in workflow conditions)
- Removing `ast.Call` entirely (breaks `coalesce(...)` function)
- Changing `_SafeNamespace.__getattr__` behavior
- Changing any workflow YAML file

---

## Investigation Findings

**Fill this section in before writing code.**

Read `engine/expressions.py` lines 231-266 (`_safe_eval`) and lines 417-467 (`_validate_ast`), then answer:

1. Does `_SafeNamespace.__getattr__` intercept dunder access like `__class__`?
   - Answer from code: `__getattr__` is only called when normal attribute lookup fails. Python's data model resolves `__class__` via the instance's type, bypassing `__getattr__`. So `ctx.__class__` returns `_SafeNamespace` regardless.

2. Can `_SafeNamespace.__class__.__mro__[-1].__subclasses__()` be expressed as a valid AST?
   - `ctx.__class__` → `ast.Attribute(value=Name('ctx'), attr='__class__')`
   - `.__mro__[-1]` → `ast.Subscript(Attribute(..., '__mro__'), Constant(-1))`
   - `.__subclasses__()` → `ast.Call(ast.Attribute(..., '__subclasses__'), [])`
   - All three node types (`Attribute`, `Subscript`, `Call`) are in the whitelist.
   - **Verdict: The attack chain passes AST validation.**

3. Does `{"__builtins__": {}}` prevent the exploit from completing?
   - `__builtins__` is empty, so `import`, `exec`, `eval` are unavailable.
   - However, `subprocess.Popen` is already loaded in the interpreter process. The `__subclasses__()` chain can reach it without needing `import`.
   - A complete chain: `ctx.__class__.__mro__[-1].__subclasses__()[N](['cmd'])` where `N` is the index of `Popen` in `object.__subclasses__()`.
   - This index varies by import order, but an attacker can enumerate it.
   - **Verdict: The exploit is feasible. `{"__builtins__": {}}` alone is not sufficient.**

4. **Fix approach:** Add a check in `_validate_ast` that walks all `ast.Attribute` nodes and rejects any whose `attr` starts with `__` (dunder). This blocks `__class__`, `__mro__`, `__subclasses__`, `__globals__`, `__builtins__`, `__base__`, etc. while preserving legitimate attribute access like `steps.parse.outputs.code`.

---

## Acceptance Criteria

- [ ] `_validate_ast` rejects expressions containing `ast.Attribute` nodes with `attr` starting with `__`
- [ ] `_validate_ast` raises `ValueError` for `ctx.__class__`, `steps.x.__mro__`, `x.__subclasses__()`
- [ ] All existing expression evaluator tests (`tests/engine/test_expressions.py`) still pass
- [ ] New test file `tests/engine/test_expressions_security.py` passes with negative corpus
- [ ] Legitimate expressions (`steps.parse.outputs.code`, `ctx.count > 5`, `coalesce(x, y)`) are not broken
- [ ] `pre-commit run --all-files` exits 0

---

## Implementation Plan

1. **Open** `agentic-workflows-v2/agentic_v2/engine/expressions.py`.

2. **Modify** `_validate_ast` to add a dunder attribute check. After the `for child in ast.walk(node):` loop's `isinstance` check, add:

```python
def _validate_ast(self, node: ast.AST) -> None:
    """Reject any AST node not in the safety whitelist.

    Permits: comparisons, boolean/arithmetic ops, constants, names,
    attribute access (non-dunder), subscripts, containers, and
    function calls (restricted to ``coalesce`` at eval time).

    Raises:
        ValueError: If any node type is outside the whitelist, or if
            any attribute access uses a dunder name (``__...``).
    """
    allowed_nodes = (
        ast.Expression,
        ast.BoolOp,
        ast.BinOp,
        ast.UnaryOp,
        ast.Compare,
        ast.Name,
        ast.Load,
        ast.Attribute,
        ast.Subscript,
        ast.Constant,
        ast.And,
        ast.Or,
        ast.Not,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
        ast.In,
        ast.NotIn,
        ast.Is,
        ast.IsNot,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.USub,
        ast.UAdd,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Call,
    )
    for child in ast.walk(node):
        if not isinstance(child, allowed_nodes):
            raise ValueError(
                f"Unsupported expression element: {type(child).__name__}"
            )
        # Block dunder attribute access: prevents __class__.__mro__[-1]
        # .__subclasses__() traversal even when __builtins__ is empty.
        if isinstance(child, ast.Attribute) and child.attr.startswith("__"):
            raise ValueError(
                f"Dunder attribute access is not allowed in expressions: {child.attr!r}"
            )
```

3. **Create** `agentic-workflows-v2/tests/engine/test_expressions_security.py`:

```python
"""Security corpus for ExpressionEvaluator.

Tests that dunder traversal and other injection vectors are rejected
at the AST-validation stage before eval() is reached.
"""

import pytest

from agentic_v2.engine.context import ExecutionContext
from agentic_v2.engine.expressions import ExpressionEvaluator


def _evaluator() -> ExpressionEvaluator:
    ctx = ExecutionContext(run_id="test", workflow_name="test")
    return ExpressionEvaluator(ctx)


# ---------------------------------------------------------------------------
# Dunder traversal corpus — must all raise ValueError
# ---------------------------------------------------------------------------

_DUNDER_TRAVERSAL = [
    "${ctx.__class__}",
    "${ctx.__class__.__mro__}",
    "${ctx.__class__.__mro__[-1].__subclasses__()}",
    "${steps.x.__class__}",
    "${ctx.__globals__}",
    "${ctx.__builtins__}",
    "${ctx.__base__}",
    "${ctx.__dict__}",
    "${ctx.__module__}",
    "${coalesce.__globals__}",
]

@pytest.mark.parametrize("expr", _DUNDER_TRAVERSAL)
def test_dunder_traversal_rejected(expr: str):
    """Dunder attribute access must raise ValueError at AST validation."""
    evaluator = _evaluator()
    with pytest.raises(ValueError, match="[Dd]under|not allowed|Unsupported"):
        evaluator._safe_eval(expr.strip("${}"))


# ---------------------------------------------------------------------------
# Legitimate expressions — must NOT raise
# ---------------------------------------------------------------------------

_LEGITIMATE_EXPRESSIONS = [
    ("${ctx.count > 5}", False),           # comparison — depends on ctx having count
    ("${steps.parse.outputs.code}", None), # path resolution — None when missing
    ("coalesce(None, 'fallback')", "fallback"),
    ("1 + 2 == 3", True),
    ("'hello' in ['hello', 'world']", True),
]

@pytest.mark.parametrize("expr,expected", _LEGITIMATE_EXPRESSIONS)
def test_legitimate_expressions_not_broken(expr: str, expected):
    evaluator = _evaluator()
    # Should not raise — result may vary but no ValueError from AST validation
    try:
        result = evaluator._safe_eval(expr)
        if expected is not None:
            assert result == expected
    except (AttributeError, KeyError, TypeError):
        # Missing context keys are acceptable; AST validation must not fire
        pass
```

4. **Run** `pre-commit run --all-files`.

5. **Run** `python -m pytest tests/engine/ -v`.

---

## Test Plan

| Test group | Count | Pass condition |
|---|---|---|
| `test_dunder_traversal_rejected` | 10 parametrized | `ValueError` raised before `eval()` |
| `test_legitimate_expressions_not_broken` | 5 parametrized | No `ValueError` from AST validation |
| Existing `tests/engine/test_expressions.py` | All | Still pass |

---

## Risks / Pitfalls

| Risk | Mitigation |
|---|---|
| Workflow YAMLs may use `__contains__` or other dunder-named keys in data | Search YAML files: `grep -r "__" agentic_v2/workflows/definitions/`. Any YAML using dunder keys in expressions would need updating. |
| Python `in` operator desugars to `__contains__` at the bytecode level but NOT at the AST level — `ast.In` is a comparison op, not a call | No issue: `x in [1,2,3]` parses to `ast.Compare(ops=[ast.In()])`, not an `ast.Attribute` dunder call. The check is safe. |
| `coalesce.__globals__` in the test — the function name `coalesce` is in env, and `.__globals__` would be blocked | Correct: this is the scenario we want to block. The test must raise. |
| Fix to `_validate_ast` is a two-liner — could be accidentally reverted | Add a comment referencing Sec H4 and this ticket ID so the intent is clear. |

---

## Not in Scope

- Removing `ast.Call` from the whitelist (would break `coalesce()`)
- Adding a `Call` function-name whitelist (complex; `{"__builtins__": {}}` + dunder block is sufficient)
- Changing `_NullSafe` or `_SafeNamespace` class hierarchy
- Testing all possible `__subclasses__()` enumeration paths (the AST block prevents the expression from compiling)

---

## Verification

```bash
# From agentic-workflows-v2/

# 1. Lint + format
pre-commit run --all-files

# 2. Type check
python -m mypy agentic_v2/engine/expressions.py --ignore-missing-imports

# 3. Existing expression tests (must all pass)
python -m pytest tests/engine/test_expressions.py -v

# 4. New security corpus
python -m pytest tests/engine/test_expressions_security.py -v

# 5. Manual verify dunder is blocked
python -c "
from agentic_v2.engine.context import ExecutionContext
from agentic_v2.engine.expressions import ExpressionEvaluator
ctx = ExecutionContext(run_id='t', workflow_name='t')
ev = ExpressionEvaluator(ctx)
try:
    ev._safe_eval('ctx.__class__')
    print('FAIL: dunder not blocked')
except ValueError as e:
    print('PASS:', e)
"
```

---

## Dependencies

None. This ticket is self-contained and has no upstream dependencies.
