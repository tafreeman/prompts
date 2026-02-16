"""Expression evaluator for YAML conditions.

Evaluates ``${...}`` expressions from YAML ``when`` / ``loop_until``
fields against the current LangGraph ``WorkflowState``.

This is a *minimal* reimplementation that works directly on the state
dict rather than requiring the old ``ExecutionContext``.
"""

from __future__ import annotations

import ast
import re
from typing import Any


# ${...} extraction pattern
_VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")


def evaluate_condition(expr: str, state: dict[str, Any]) -> bool:
    """Evaluate a YAML condition expression against workflow state.

    Supports:
    - Variable access: ``${inputs.code_file}``
    - Step outputs: ``${steps.parse_code.outputs.ast}``
    - Comparisons: ``${inputs.review_depth} != 'quick'``
    - Boolean: ``${context.is_valid}``
    - ``in`` operator: ``${steps.review.outputs.status} in ['APPROVED']``

    Returns ``True`` if the condition is met, ``False`` otherwise.
    """
    if not expr or not isinstance(expr, str):
        return True

    expr = expr.strip()

    # Replace all ${...} references with resolved values
    resolved = _VAR_PATTERN.sub(
        lambda m: repr(_resolve_path(m.group(1).strip(), state)),
        expr,
    )

    # Safety: only allow a restricted AST
    try:
        tree = ast.parse(resolved, mode="eval")
        _validate_ast(tree.body)
        result = eval(compile(tree, "<expr>", "eval"))  # noqa: S307
        return bool(result)
    except Exception:
        return False


def resolve_expression(expr: str, state: dict[str, Any]) -> Any:
    """Resolve a single ``${...}`` expression to its value."""
    if not isinstance(expr, str):
        return expr
    expr = expr.strip()
    match = _VAR_PATTERN.fullmatch(expr)
    if match:
        return _resolve_path(match.group(1).strip(), state)
    return expr


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _resolve_path(path: str, state: dict[str, Any]) -> Any:
    """Walk a dotted path like ``steps.parse_code.outputs.ast``."""
    parts = path.split(".")
    current: Any = state

    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        elif hasattr(current, part):
            current = getattr(current, part)
        else:
            return None

        if current is None:
            return None

    return current


_ALLOWED_AST_NODES = (
    ast.Expression,
    ast.BoolOp,
    ast.BinOp,
    ast.UnaryOp,
    ast.Compare,
    ast.Constant,
    ast.List,
    ast.Tuple,
    ast.Set,
    ast.Name,
    ast.Load,       # context node for List/Tuple/Set/Name
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
)


def _validate_ast(node: ast.AST) -> None:
    """Raise ValueError if the AST contains disallowed node types."""
    if not isinstance(node, _ALLOWED_AST_NODES):
        raise ValueError(f"Disallowed AST node: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _validate_ast(child)
