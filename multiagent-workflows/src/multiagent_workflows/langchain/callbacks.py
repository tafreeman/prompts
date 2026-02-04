"""LangChain Callbacks for Evaluation and Logging Parity.

Provides callback handlers that align LangChain run outputs with the
existing evaluation and logging expectations in the multiagent-workflows
engine.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

try:
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_core.messages import BaseMessage
    from langchain_core.outputs import LLMResult

    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    BaseCallbackHandler = object
    LLMResult = Any

from multiagent_workflows.core.logger import VerboseLogger


@dataclass
class RunMetrics:
    """Metrics collected during a run."""

    start_time: float = 0.0
    end_time: float = 0.0
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    llm_calls: int = 0
    tool_calls: int = 0
    errors: List[str] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        return (self.end_time - self.start_time) * 1000 if self.end_time else 0


class WorkflowCallbackHandler(BaseCallbackHandler if LANGCHAIN_AVAILABLE else object):
    """Callback handler that bridges LangChain events to the workflow logger.

    Ensures that LangChain runs produce logs compatible with the
    existing evaluation and reporting infrastructure.
    """

    def __init__(
        self,
        logger: Optional[VerboseLogger] = None,
        collect_metrics: bool = True,
    ):
        if LANGCHAIN_AVAILABLE:
            super().__init__()
        self.logger = logger
        self.collect_metrics = collect_metrics

        # Run tracking
        self._run_metrics: Dict[str, RunMetrics] = {}
        self._workflow_runs: Dict[str, Dict[str, Any]] = {}
        self._current_workflow_id: Optional[str] = None

    # =========================================================================
    # Workflow-level callbacks (custom, not LangChain)
    # =========================================================================

    def on_workflow_start(
        self,
        workflow_id: str,
        workflow_name: str,
        inputs: Dict[str, Any],
    ) -> None:
        """Called when a workflow starts."""
        self._current_workflow_id = workflow_id
        self._workflow_runs[workflow_id] = {
            "name": workflow_name,
            "start_time": time.time(),
            "inputs": inputs,
            "steps": [],
            "metrics": RunMetrics(start_time=time.time()),
        }

        if self.logger:
            self.logger.log_workflow_start(workflow_name, inputs)

    def on_workflow_complete(
        self,
        workflow_id: str,
        result: Dict[str, Any],
    ) -> None:
        """Called when a workflow completes."""
        if workflow_id in self._workflow_runs:
            run = self._workflow_runs[workflow_id]
            run["metrics"].end_time = time.time()
            run["result"] = result
            run["success"] = result.get("success", True)

        if self.logger:
            self.logger.log_workflow_complete(
                workflow_id,
                result.get("success", True),
                result,
            )

    def on_workflow_error(
        self,
        workflow_id: str,
        error: Exception,
    ) -> None:
        """Called when a workflow fails."""
        if workflow_id in self._workflow_runs:
            run = self._workflow_runs[workflow_id]
            run["metrics"].end_time = time.time()
            run["metrics"].errors.append(str(error))
            run["success"] = False

        if self.logger:
            self.logger.log_workflow_error(workflow_id, error)

    def on_step_start(
        self,
        step_name: str,
        state: Dict[str, Any],
    ) -> None:
        """Called when a workflow step starts."""
        step_data = {
            "name": step_name,
            "start_time": time.time(),
            "state_snapshot": {k: v for k, v in state.items() if k != "artifacts"},
        }

        if self._current_workflow_id in self._workflow_runs:
            self._workflow_runs[self._current_workflow_id]["steps"].append(step_data)

        if self.logger:
            self.logger.log_step_start(
                self._current_workflow_id or "",
                step_name,
            )

    def on_step_complete(
        self,
        step_name: str,
        result: Dict[str, Any],
        duration_ms: float,
    ) -> None:
        """Called when a workflow step completes."""
        if self._current_workflow_id in self._workflow_runs:
            steps = self._workflow_runs[self._current_workflow_id]["steps"]
            for step in reversed(steps):
                if step["name"] == step_name:
                    step["end_time"] = time.time()
                    step["duration_ms"] = duration_ms
                    step["result"] = result
                    step["success"] = True
                    break

        if self.logger:
            self.logger.log_step_complete(step_name, True, result)

    def on_step_error(
        self,
        step_name: str,
        error: Exception,
    ) -> None:
        """Called when a workflow step fails."""
        if self._current_workflow_id in self._workflow_runs:
            steps = self._workflow_runs[self._current_workflow_id]["steps"]
            for step in reversed(steps):
                if step["name"] == step_name:
                    step["end_time"] = time.time()
                    step["error"] = str(error)
                    step["success"] = False
                    break

        if self.logger:
            self.logger.log_step_error(step_name, error)

    # =========================================================================
    # LangChain LLM callbacks
    # =========================================================================

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        **kwargs,
    ) -> None:
        """Called when an LLM call starts."""
        run_key = str(run_id)
        self._run_metrics[run_key] = RunMetrics(start_time=time.time())

        if self._current_workflow_id in self._workflow_runs:
            self._workflow_runs[self._current_workflow_id]["metrics"].llm_calls += 1

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        **kwargs,
    ) -> None:
        """Called when an LLM call completes."""
        run_key = str(run_id)
        if run_key in self._run_metrics:
            metrics = self._run_metrics[run_key]
            metrics.end_time = time.time()

            # Extract token usage if available
            if hasattr(response, "llm_output") and response.llm_output:
                token_usage = response.llm_output.get("token_usage", {})
                metrics.prompt_tokens = token_usage.get("prompt_tokens", 0)
                metrics.completion_tokens = token_usage.get("completion_tokens", 0)
                metrics.total_tokens = token_usage.get("total_tokens", 0)

            # Update workflow metrics
            if self._current_workflow_id in self._workflow_runs:
                wf_metrics = self._workflow_runs[self._current_workflow_id]["metrics"]
                wf_metrics.total_tokens += metrics.total_tokens
                wf_metrics.prompt_tokens += metrics.prompt_tokens
                wf_metrics.completion_tokens += metrics.completion_tokens

    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        **kwargs,
    ) -> None:
        """Called when an LLM call fails."""
        run_key = str(run_id)
        if run_key in self._run_metrics:
            self._run_metrics[run_key].errors.append(str(error))

        if self._current_workflow_id in self._workflow_runs:
            self._workflow_runs[self._current_workflow_id]["metrics"].errors.append(
                f"LLM error: {error}"
            )

    # =========================================================================
    # LangChain Tool callbacks
    # =========================================================================

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        **kwargs,
    ) -> None:
        """Called when a tool call starts."""
        if self._current_workflow_id in self._workflow_runs:
            self._workflow_runs[self._current_workflow_id]["metrics"].tool_calls += 1

        if self.logger:
            tool_name = serialized.get("name", "unknown")
            self.logger.log_tool_invocation(
                self._current_workflow_id or "",
                tool_name,
                {"input": input_str[:500]},
            )

    def on_tool_end(
        self,
        output: str,
        *,
        run_id: UUID,
        **kwargs,
    ) -> None:
        """Called when a tool call completes."""
        pass  # Tool completion is logged as part of step completion

    def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        **kwargs,
    ) -> None:
        """Called when a tool call fails."""
        if self._current_workflow_id in self._workflow_runs:
            self._workflow_runs[self._current_workflow_id]["metrics"].errors.append(
                f"Tool error: {error}"
            )

    # =========================================================================
    # Metrics and reporting
    # =========================================================================

    def get_workflow_metrics(
        self,
        workflow_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Get metrics for a workflow run."""
        if workflow_id not in self._workflow_runs:
            return None

        run = self._workflow_runs[workflow_id]
        metrics = run["metrics"]

        return {
            "workflow_id": workflow_id,
            "workflow_name": run["name"],
            "duration_ms": metrics.duration_ms,
            "total_tokens": metrics.total_tokens,
            "prompt_tokens": metrics.prompt_tokens,
            "completion_tokens": metrics.completion_tokens,
            "llm_calls": metrics.llm_calls,
            "tool_calls": metrics.tool_calls,
            "step_count": len(run["steps"]),
            "success": run.get("success", False),
            "errors": metrics.errors,
        }

    def get_step_metrics(
        self,
        workflow_id: str,
    ) -> List[Dict[str, Any]]:
        """Get metrics for all steps in a workflow run."""
        if workflow_id not in self._workflow_runs:
            return []

        return [
            {
                "name": step["name"],
                "duration_ms": step.get("duration_ms", 0),
                "success": step.get("success", False),
                "error": step.get("error"),
            }
            for step in self._workflow_runs[workflow_id]["steps"]
        ]


# =============================================================================
# UI Scoring Categories (matches UI app)
# =============================================================================

# Default weights and values from UI (index.html lines 1134-1141)
UI_SCORING_CATEGORIES = {
    "correctness": {"weight": 81, "description": "Functional correctness of output"},
    "quality": {
        "weight": 25,
        "description": "Code quality (style, structure, patterns)",
    },
    "documentation": {"weight": 25, "description": "Documentation completeness"},
    "completeness": {"weight": 15, "description": "Task completion coverage"},
    "efficiency": {"weight": 9, "description": "Performance and resource efficiency"},
}


class EvaluationCallbackHandler(WorkflowCallbackHandler):
    """Extended callback handler for evaluation scoring.

    Collects data needed for the WorkflowEvaluator to score runs.
    Integrates the UI scoring categories (Correctness, Quality,
    Documentation, etc.)
    """

    def __init__(
        self,
        logger: Optional[VerboseLogger] = None,
        evaluator: Optional[Any] = None,
        scorer: Optional[Any] = None,
        scoring_weights: Optional[Dict[str, int]] = None,
    ):
        super().__init__(logger, collect_metrics=True)
        self.evaluator = evaluator
        self.scorer = scorer
        # Allow custom weights or use defaults from UI
        self.scoring_weights = scoring_weights or {
            k: v["weight"] for k, v in UI_SCORING_CATEGORIES.items()
        }
        self._evaluation_data: Dict[str, Dict[str, Any]] = {}

    def on_workflow_complete(
        self,
        workflow_id: str,
        result: Dict[str, Any],
    ) -> None:
        """Called when a workflow completes - triggers evaluation."""
        super().on_workflow_complete(workflow_id, result)

        if workflow_id in self._workflow_runs:
            self._run_evaluation(workflow_id, result)

    def _run_evaluation(
        self,
        workflow_id: str,
        result: Dict[str, Any],
    ) -> None:
        """Run evaluation on completed workflow with UI-compatible scoring."""
        try:
            run = self._workflow_runs[workflow_id]

            # Prepare evaluation input
            eval_input = {
                "workflow_id": workflow_id,
                "workflow_name": run["name"],
                "inputs": run["inputs"],
                "outputs": result.get("outputs", {}),
                "metrics": self.get_workflow_metrics(workflow_id),
                "steps": self.get_step_metrics(workflow_id),
            }

            # Compute UI-compatible category scores
            category_scores = self._compute_category_scores(
                result.get("outputs", {}),
                result.get("golden", ""),
            )

            # Calculate weighted total score
            total_weight = sum(self.scoring_weights.values())
            weighted_score = 0.0
            for category, score in category_scores.items():
                weight = self.scoring_weights.get(category, 0)
                weighted_score += score * weight / 100.0

            overall_percentage = (
                (weighted_score / total_weight * 100) if total_weight > 0 else 0
            )

            # Build evaluation result
            eval_result = {
                "workflow_id": workflow_id,
                "timestamp": datetime.utcnow().isoformat(),
                # UI-compatible scoring
                "score": round(overall_percentage, 1),
                "correctness": round(category_scores.get("correctness", 0) * 100, 1),
                "quality": round(category_scores.get("quality", 0) * 100, 1),
                "documentation": round(
                    category_scores.get("documentation", 0) * 100, 1
                ),
                "completeness": round(category_scores.get("completeness", 0) * 100, 1),
                "efficiency": round(category_scores.get("efficiency", 0) * 100, 1),
                "category_scores": {
                    k: round(v * 100, 1) for k, v in category_scores.items()
                },
                "weights": self.scoring_weights,
                "passed": overall_percentage >= 70,  # Default threshold from UI
                # Additional metadata
                "metrics": eval_input["metrics"],
                "step_count": len(eval_input["steps"]),
            }

            # If external evaluator provided, merge its results
            if self.evaluator and hasattr(self.evaluator, "evaluate"):
                external_result = self.evaluator.evaluate(eval_input)
                if isinstance(external_result, dict):
                    eval_result["external_evaluation"] = external_result
                    # Prefer external score if provided
                    if "score" in external_result:
                        eval_result["score"] = external_result["score"]

            self._evaluation_data[workflow_id] = eval_result

            if self.logger:
                self.logger.log_evaluation_result(workflow_id, eval_result)

        except Exception as e:
            if self.logger:
                self.logger.warning(f"Evaluation failed: {e}")

    def _compute_category_scores(
        self,
        outputs: Dict[str, Any],
        golden: str = "",
    ) -> Dict[str, float]:
        """Compute scores for each UI category (0-1 scale).

        Uses the Scorer class if available, otherwise uses heuristics.
        """
        # Convert outputs to string for analysis
        output_str = ""
        if isinstance(outputs, str):
            output_str = outputs
        elif isinstance(outputs, dict):
            # Try to extract code/text content
            output_str = (
                outputs.get("code", "")
                or outputs.get("output", "")
                or outputs.get("result", "")
            )
            if not output_str and outputs:
                output_str = json.dumps(outputs, indent=2)

        scores = {}

        # Use Scorer if available
        if self.scorer and hasattr(self.scorer, "score_correctness"):
            scores["correctness"] = self.scorer.score_correctness(output_str, golden)
            scores["quality"] = self.scorer.score_code_quality(output_str)
            scores["documentation"] = self.scorer.score_documentation(output_str)
            scores["completeness"] = self.scorer.score_completeness(output_str, golden)
            scores["efficiency"] = 0.7  # Default - efficiency requires execution
        else:
            # Fallback heuristic scoring
            scores = self._heuristic_scores(output_str, golden)

        return scores

    def _heuristic_scores(
        self,
        output: str,
        golden: str,
    ) -> Dict[str, float]:
        """Fallback heuristic scoring when Scorer is not available."""
        from difflib import SequenceMatcher

        scores = {}

        # Correctness: similarity to golden (if available)
        if golden:
            scores["correctness"] = SequenceMatcher(None, output, golden).ratio()
        else:
            scores["correctness"] = 0.7 if output else 0.0

        # Quality: check for good patterns
        quality = 0.5
        if "def " in output or "class " in output:
            quality += 0.15
        if '"""' in output or "'''" in output:
            quality += 0.1
        if ": str" in output or "-> " in output:
            quality += 0.1
        if "TODO" in output or "FIXME" in output:
            quality -= 0.1
        scores["quality"] = max(0, min(1, quality))

        # Documentation: presence of docs
        doc_score = 0.0
        doc_indicators = [
            "README",
            "##",
            "Usage",
            "Example",
            '"""',
            "Args:",
            "Returns:",
        ]
        for indicator in doc_indicators:
            if indicator in output:
                doc_score += 0.15
        scores["documentation"] = min(1, doc_score)

        # Completeness: based on output existence and length
        if output:
            completeness = min(1, len(output) / 1000)  # Scale up to 1000 chars
            if len(output) > 100:
                completeness = max(completeness, 0.5)
        else:
            completeness = 0.0
        scores["completeness"] = completeness

        # Efficiency: default placeholder
        scores["efficiency"] = 0.7

        return scores

    def get_evaluation_result(
        self,
        workflow_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Get evaluation result for a workflow run."""
        return self._evaluation_data.get(workflow_id)

    def get_scoring_summary(
        self,
        workflow_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Get a UI-compatible scoring summary.

        Returns format matching UI expectations:
        {
            "score": 75.5,
            "correctness": 80.0,
            "quality": 70.0,
            ...
        }
        """
        eval_result = self._evaluation_data.get(workflow_id)
        if not eval_result:
            return None

        return {
            "score": eval_result.get("score", 0),
            "correctness": eval_result.get("correctness", 0),
            "quality": eval_result.get("quality", 0),
            "documentation": eval_result.get("documentation", 0),
            "completeness": eval_result.get("completeness", 0),
            "efficiency": eval_result.get("efficiency", 0),
            "passed": eval_result.get("passed", False),
        }


def create_callbacks(
    logger: Optional[VerboseLogger] = None,
    evaluator: Optional[Any] = None,
    scorer: Optional[Any] = None,
    scoring_weights: Optional[Dict[str, int]] = None,
) -> List[Any]:
    """Create the appropriate callback handlers.

    Args:
        logger: Optional logger for workflow events
        evaluator: Optional evaluator for custom scoring
        scorer: Optional Scorer instance for category scoring
        scoring_weights: Optional custom weights for scoring categories

    Returns:
        List of callback handlers
    """
    # Try to create a default Scorer if not provided
    if scorer is None:
        try:
            from multiagent_workflows.evaluation.scorer import Scorer

            scorer = Scorer(rubrics={})
        except ImportError:
            scorer = None

    if evaluator or scorer:
        return [EvaluationCallbackHandler(logger, evaluator, scorer, scoring_weights)]
    elif logger:
        return [WorkflowCallbackHandler(logger)]
    else:
        return []
