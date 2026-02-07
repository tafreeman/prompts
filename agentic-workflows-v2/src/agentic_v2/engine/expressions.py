"""Expression evaluation helpers for conditional execution.

Supports:
- Variable access: ${ctx.var_name}
- Comparisons: ${ctx.count > 5}
- Boolean ops: ${ctx.enabled and ctx.ready}
- Step results: ${steps.step1.status == 'success'}
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from datetime import timezone
from types import SimpleNamespace
from typing import Any, Optional

from ..contracts import StepResult
from .context import ExecutionContext


@dataclass
class StepResultView:
    """Lightweight view of a StepResult for expression evaluation."""

    status: str
    output: dict[str, Any]
    outputs: dict[str, Any]
    error: Optional[str]
    error_type: Optional[str]
    completed_at: Optional[str]


class ExpressionEvaluator:
    """Safely evaluate simple boolean expressions against context."""

    VARIABLE_PATTERN = re.compile(r"\$\{([^}]+)\}")

    def __init__(
        self,
        ctx: ExecutionContext,
        step_results: Optional[dict[str, StepResult]] = None,
    ):
        self.ctx = ctx
        self.step_results = step_results or {}

    def evaluate(self, expr: Any) -> bool:
        """Evaluate expression to boolean."""
        if isinstance(expr, bool):
            return expr
        if expr is None:
            return False
        if not isinstance(expr, str):
            return bool(expr)

        expression = expr.strip()
        match = self.VARIABLE_PATTERN.fullmatch(expression)
        if match:
            expression = match.group(1).strip()

        if expression.lower() in {"true", "false"}:
            return expression.lower() == "true"

        try:
            return bool(self._safe_eval(expression))
        except AttributeError:
            # Missing attribute in a when-condition means the condition
            # isn't satisfiable (e.g. upstream step didn't produce expected
            # output key).  Treat as False rather than crashing.
            return False

    def resolve_variable(self, path: str) -> Any:
        """Resolve a single ${...} variable reference."""
        return self._resolve_path(path)

    def _safe_eval(self, expression: str) -> Any:
        """Safely evaluate a boolean expression with limited syntax."""
        tree = ast.parse(expression, mode="eval")
        self._validate_ast(tree)

        all_vars = self.ctx.all_variables()

        # Build steps namespace: merge StepResult objects with context-stored
        # step data (stored by StepExecutor as ctx["steps"]).  This allows
        # when-conditions like ${steps.review_code.outputs.review_report.approved}
        # to resolve even when the evaluator has no step_results param.
        step_views = self._build_step_views()
        ctx_steps = all_vars.get("steps")
        if isinstance(ctx_steps, dict):
            for name, data in ctx_steps.items():
                if name not in step_views and isinstance(data, dict):
                    step_views[name] = data  # raw dict, _to_namespace handles it

        env = {
            "ctx": self._to_namespace(all_vars),
            "steps": self._to_namespace(step_views),
        }
        # Expose top-level context keys (e.g. "inputs") as direct names
        # so that ${inputs.foo} resolves without a "ctx." prefix.
        for key, value in all_vars.items():
            if key not in env:
                env[key] = self._to_namespace(value) if isinstance(value, (dict, list)) else value

        return eval(compile(tree, "<expr>", "eval"), {"__builtins__": {}}, env)

    def _build_step_views(self) -> dict[str, StepResultView]:
        views: dict[str, StepResultView] = {}
        for name, result in self.step_results.items():
            completed_at = None
            if result.end_time:
                completed_at = result.end_time.astimezone(timezone.utc).isoformat()
            views[name] = StepResultView(
                status=result.status.value,
                output=result.output_data,
                outputs=result.output_data,
                error=result.error,
                error_type=result.error_type,
                completed_at=completed_at,
            )
        return views

    def _resolve_path(self, path: str) -> Any:
        parts = path.split(".")
        source = parts[0]

        if source == "steps" and len(parts) > 1:
            step_name = parts[1]
            step = self._build_step_views().get(step_name)
            return self._navigate(step, parts[2:])

        if source == "ctx":
            return self._navigate(self.ctx.all_variables(), parts[1:])

        return self._navigate(self.ctx.all_variables(), parts)

    def _navigate(self, obj: Any, path: list[str]) -> Any:
        for key in path:
            if obj is None:
                return None
            if isinstance(obj, dict):
                obj = obj.get(key)
            elif hasattr(obj, key):
                obj = getattr(obj, key)
            else:
                return None
        return obj

    def _validate_ast(self, node: ast.AST) -> None:
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
        )
        for child in ast.walk(node):
            if not isinstance(child, allowed_nodes):
                raise ValueError(
                    f"Unsupported expression element: {type(child).__name__}"
                )

    def _to_namespace(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return SimpleNamespace(**{k: self._to_namespace(v) for k, v in obj.items()})
        if isinstance(obj, list):
            return [self._to_namespace(v) for v in obj]
        return obj
