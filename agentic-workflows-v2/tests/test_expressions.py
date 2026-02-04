"""Tests for ExpressionEvaluator.

Covers:
- Variable resolution with ${...} syntax
- Boolean expression evaluation
- Comparison operators
- Step result access
- Safe eval restrictions
"""

import pytest
from agentic_v2.contracts import StepResult, StepStatus
from agentic_v2.engine.context import ExecutionContext
from agentic_v2.engine.expressions import ExpressionEvaluator, StepResultView


class TestExpressionEvaluatorBasic:
    """Basic expression evaluation tests."""

    def test_evaluate_boolean_true(self):
        """Direct boolean True evaluates to True."""
        ctx = ExecutionContext()
        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate(True) is True

    def test_evaluate_boolean_false(self):
        """Direct boolean False evaluates to False."""
        ctx = ExecutionContext()
        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate(False) is False

    def test_evaluate_none_is_false(self):
        """None evaluates to False."""
        ctx = ExecutionContext()
        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate(None) is False

    def test_evaluate_string_true(self):
        """String 'true' (case insensitive) evaluates to True."""
        ctx = ExecutionContext()
        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("true") is True
        assert evaluator.evaluate("True") is True
        assert evaluator.evaluate("TRUE") is True

    def test_evaluate_string_false(self):
        """String 'false' (case insensitive) evaluates to False."""
        ctx = ExecutionContext()
        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("false") is False
        assert evaluator.evaluate("False") is False
        assert evaluator.evaluate("FALSE") is False

    def test_evaluate_truthy_values(self):
        """Non-zero/non-empty values are truthy."""
        ctx = ExecutionContext()
        ctx.set_sync("num", 42)
        ctx.set_sync("text", "hello")
        ctx.set_sync("items", [1, 2, 3])

        evaluator = ExpressionEvaluator(ctx)
        # Test via context variables which get properly evaluated
        assert evaluator.evaluate("${ctx.num}") is True
        assert evaluator.evaluate("${ctx.text}") is True
        assert evaluator.evaluate("${ctx.items}") is True
        # Direct Python values
        assert evaluator.evaluate(1) is True
        assert evaluator.evaluate([1]) is True


class TestExpressionEvaluatorVariables:
    """Tests for variable resolution."""

    def test_resolve_ctx_variable(self):
        """${ctx.var_name} resolves to context variable."""
        ctx = ExecutionContext()
        ctx.set_sync("my_var", "my_value")

        evaluator = ExpressionEvaluator(ctx)
        result = evaluator.resolve_variable("ctx.my_var")
        assert result == "my_value"

    def test_resolve_nested_ctx_variable(self):
        """${ctx.obj.nested} resolves nested values."""
        ctx = ExecutionContext()
        ctx.set_sync("config", {"database": {"host": "localhost"}})

        evaluator = ExpressionEvaluator(ctx)
        result = evaluator.resolve_variable("ctx.config.database.host")
        assert result == "localhost"

    def test_resolve_missing_variable_returns_none(self):
        """Missing variables return None."""
        ctx = ExecutionContext()
        evaluator = ExpressionEvaluator(ctx)
        result = evaluator.resolve_variable("ctx.missing")
        assert result is None

    def test_evaluate_variable_expression(self):
        """${ctx.enabled} evaluates variable as boolean."""
        ctx = ExecutionContext()
        ctx.set_sync("enabled", True)

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.enabled}") is True

    def test_evaluate_variable_expression_false(self):
        """${ctx.disabled} evaluates falsy variable."""
        ctx = ExecutionContext()
        ctx.set_sync("disabled", False)

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.disabled}") is False


class TestExpressionEvaluatorComparisons:
    """Tests for comparison operators."""

    def test_compare_greater_than(self):
        """ctx.count > 5 comparison."""
        ctx = ExecutionContext()
        ctx.set_sync("count", 10)

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.count > 5}") is True

        ctx.set_sync("count", 3)
        evaluator = ExpressionEvaluator(ctx)  # Refresh evaluator
        assert evaluator.evaluate("${ctx.count > 5}") is False

    def test_compare_less_than(self):
        """ctx.value < 100 comparison."""
        ctx = ExecutionContext()
        ctx.set_sync("value", 50)

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.value < 100}") is True

    def test_compare_equal(self):
        """ctx.status == 'active' comparison."""
        ctx = ExecutionContext()
        ctx.set_sync("status", "active")

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.status == 'active'}") is True
        assert evaluator.evaluate("${ctx.status == 'inactive'}") is False

    def test_compare_not_equal(self):
        """ctx.mode != 'debug' comparison."""
        ctx = ExecutionContext()
        ctx.set_sync("mode", "production")

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.mode != 'debug'}") is True

    def test_compare_greater_or_equal(self):
        """ctx.retries >= 3 comparison."""
        ctx = ExecutionContext()
        ctx.set_sync("retries", 3)

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.retries >= 3}") is True
        assert evaluator.evaluate("${ctx.retries >= 4}") is False

    def test_compare_less_or_equal(self):
        """ctx.errors <= 0 comparison."""
        ctx = ExecutionContext()
        ctx.set_sync("errors", 0)

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.errors <= 0}") is True


class TestExpressionEvaluatorBooleanOps:
    """Tests for boolean operators (and, or, not)."""

    def test_boolean_and(self):
        """ctx.a and ctx.b evaluates both."""
        ctx = ExecutionContext()
        ctx.set_sync("a", True)
        ctx.set_sync("b", True)

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.a and ctx.b}") is True

        ctx.set_sync("b", False)
        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.a and ctx.b}") is False

    def test_boolean_or(self):
        """ctx.a or ctx.b evaluates either."""
        ctx = ExecutionContext()
        ctx.set_sync("a", False)
        ctx.set_sync("b", True)

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.a or ctx.b}") is True

        ctx.set_sync("a", False)
        ctx.set_sync("b", False)
        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.a or ctx.b}") is False

    def test_boolean_not(self):
        """Not ctx.disabled inverts value."""
        ctx = ExecutionContext()
        ctx.set_sync("disabled", False)

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${not ctx.disabled}") is True

    def test_complex_boolean_expression(self):
        """Complex expression: (a > 5) and (b or c)."""
        ctx = ExecutionContext()
        ctx.set_sync("a", 10)
        ctx.set_sync("b", False)
        ctx.set_sync("c", True)

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${(ctx.a > 5) and (ctx.b or ctx.c)}") is True


class TestExpressionEvaluatorStepResults:
    """Tests for accessing step results."""

    def test_access_step_status(self):
        """steps.step1.status returns step status."""
        ctx = ExecutionContext()
        step_result = StepResult(step_name="step1", status=StepStatus.SUCCESS)

        evaluator = ExpressionEvaluator(ctx, step_results={"step1": step_result})
        assert evaluator.evaluate("${steps.step1.status == 'success'}") is True

    def test_access_step_output(self):
        """steps.step1.output.field returns output data."""
        ctx = ExecutionContext()
        step_result = StepResult(
            step_name="step1", status=StepStatus.SUCCESS, output_data={"count": 42}
        )

        evaluator = ExpressionEvaluator(ctx, step_results={"step1": step_result})
        # Access via output attribute - returns namespace with attributes
        result = evaluator.resolve_variable("steps.step1.output")
        assert result is not None
        # The output is converted to namespace, access via attribute
        assert hasattr(result, "count") or (
            isinstance(result, dict) and result.get("count") == 42
        )

    def test_access_step_error(self):
        """steps.step1.error is accessible for failed steps."""
        ctx = ExecutionContext()
        step_result = StepResult(
            step_name="step1", status=StepStatus.FAILED, error="Something went wrong"
        )

        evaluator = ExpressionEvaluator(ctx, step_results={"step1": step_result})
        # Check that error is not None
        assert evaluator.evaluate("${steps.step1.error}") is True

    def test_check_step_succeeded(self):
        """Common pattern: steps.step1.status == 'success'."""
        ctx = ExecutionContext()
        success_result = StepResult(step_name="good", status=StepStatus.SUCCESS)
        failed_result = StepResult(step_name="bad", status=StepStatus.FAILED)

        evaluator = ExpressionEvaluator(
            ctx, step_results={"good": success_result, "bad": failed_result}
        )

        assert evaluator.evaluate("${steps.good.status == 'success'}") is True
        assert evaluator.evaluate("${steps.bad.status == 'success'}") is False


class TestExpressionEvaluatorSafety:
    """Tests for safe eval restrictions."""

    def test_rejects_function_calls(self):
        """Function calls are not allowed."""
        ctx = ExecutionContext()
        evaluator = ExpressionEvaluator(ctx)

        with pytest.raises(ValueError, match="Unsupported"):
            evaluator.evaluate("${print('hello')}")

    def test_rejects_import(self):
        """Import statements are not allowed."""
        ctx = ExecutionContext()
        evaluator = ExpressionEvaluator(ctx)

        with pytest.raises((ValueError, SyntaxError)):
            evaluator.evaluate("${__import__('os')}")

    def test_rejects_lambda(self):
        """Lambda expressions are not allowed."""
        ctx = ExecutionContext()
        evaluator = ExpressionEvaluator(ctx)

        with pytest.raises(ValueError, match="Unsupported"):
            evaluator.evaluate("${(lambda x: x)(1)}")

    def test_allows_basic_arithmetic(self):
        """Basic arithmetic in comparisons is allowed."""
        ctx = ExecutionContext()
        ctx.set_sync("a", 5)
        ctx.set_sync("b", 3)

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${ctx.a + ctx.b == 8}") is True
        assert evaluator.evaluate("${ctx.a - ctx.b == 2}") is True
        assert evaluator.evaluate("${ctx.a * ctx.b == 15}") is True

    def test_allows_in_operator(self):
        """'in' operator for membership is allowed."""
        ctx = ExecutionContext()
        ctx.set_sync("items", ["a", "b", "c"])

        evaluator = ExpressionEvaluator(ctx)
        assert evaluator.evaluate("${'a' in ctx.items}") is True
        assert evaluator.evaluate("${'z' in ctx.items}") is False


class TestStepResultView:
    """Tests for StepResultView dataclass."""

    def test_step_result_view_fields(self):
        """StepResultView holds expected fields."""
        view = StepResultView(
            status="success",
            output={"key": "value"},
            outputs={"key": "value"},
            error=None,
            error_type=None,
            completed_at="2026-02-03T12:00:00Z",
        )

        assert view.status == "success"
        assert view.output == {"key": "value"}
        assert view.error is None
        assert view.completed_at == "2026-02-03T12:00:00Z"
