#!/usr/bin/env python3
"""
Prompt Performance Evaluator
Author: AI Research Team
Version: 3.0.0
Last Updated: 2025-12-13

Automated performance evaluation and benchmarking system for prompt templates.
Supports both simulated and real LLM integration via tools/llm_client.py.
"""

import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from llm_client import LLMClient

    LLM_CLIENT_AVAILABLE = True
except ImportError:
    LLM_CLIENT_AVAILABLE = False


# Configuration for LLM integration
DEFAULT_MODEL = "gpt-4o-mini"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2.0
RATE_LIMIT_DELAY_SECONDS = 1.0


@dataclass
class TestCase:
    """Represents a single test case for evaluation."""

    input_data: str
    expected_output: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMResponse:
    """Represents a response from an LLM call."""

    text: str
    latency_seconds: float
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""
    success: bool = True
    error: Optional[str] = None


@dataclass
class BenchmarkResult:
    """Result from a single benchmark."""

    score: float
    details: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class PerformanceReport:
    """Comprehensive performance evaluation report."""

    prompt_file: str
    timestamp: str
    accuracy_score: float = 0.0
    latency_score: float = 0.0
    cost_score: float = 0.0
    robustness_score: float = 0.0
    effectivenessScore: float = 0.0  # Standardized field name
    benchmark_results: Dict[str, BenchmarkResult] = field(default_factory=dict)
    use_real_llm: bool = False
    model_used: str = ""

    @property
    def overall_score(self) -> float:
        """Alias for effectivenessScore for backwards compatibility."""
        return self.effectivenessScore

    @overall_score.setter
    def overall_score(self, value: float):
        """Setter alias for backwards compatibility."""
        self.effectivenessScore = value

    def add_score(self, benchmark_name: str, result: BenchmarkResult):
        """Add a benchmark result to the report."""
        self.benchmark_results[benchmark_name] = result
        setattr(self, f"{benchmark_name}_score", result.score)

    def calculate_overall_score(self):
        """Calculate weighted overall performance score."""
        weights = {
            "accuracy": 0.40,
            "latency": 0.25,
            "cost_efficiency": 0.20,
            "robustness": 0.15,
        }

        self.effectivenessScore = (
            self.accuracy_score * weights["accuracy"]
            + self.latency_score * weights["latency"]
            + self.cost_score * weights["cost_efficiency"]
            + self.robustness_score * weights["robustness"]
        )

        return self.effectivenessScore

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "prompt_file": self.prompt_file,
            "timestamp": self.timestamp,
            "use_real_llm": self.use_real_llm,
            "model_used": self.model_used,
            "scores": {
                "accuracy": self.accuracy_score,
                "latency": self.latency_score,
                "cost_efficiency": self.cost_score,
                "robustness": self.robustness_score,
                "effectivenessScore": self.effectivenessScore,
                "overall": self.effectivenessScore,  # Alias for compatibility
            },
            "benchmark_results": {
                name: {
                    "score": result.score,
                    "details": result.details,
                    "metrics": result.metrics,
                }
                for name, result in self.benchmark_results.items()
            },
        }


class AccuracyBenchmark:
    """Evaluate prompt accuracy and task completion."""

    def __init__(self, use_real_llm: bool = False, model: str = DEFAULT_MODEL):
        self.use_real_llm = use_real_llm
        self.model = model

    async def _call_llm(self, prompt: str, test_input: str) -> LLMResponse:
        """Make an actual LLM call and return the response with timing."""
        if not LLM_CLIENT_AVAILABLE:
            return LLMResponse(
                text="",
                latency_seconds=0,
                success=False,
                error="LLM client not available",
            )

        start_time = time.time()
        try:
            # Combine prompt with test input
            full_prompt = f"{prompt}\n\nInput: {test_input}"
            response_text = LLMClient.generate_text(self.model, full_prompt)
            latency = time.time() - start_time

            # Estimate tokens (rough approximation)
            input_tokens = len(full_prompt.split()) * 1.3
            output_tokens = len(response_text.split()) * 1.3

            return LLMResponse(
                text=response_text,
                latency_seconds=latency,
                input_tokens=int(input_tokens),
                output_tokens=int(output_tokens),
                model=self.model,
                success=True,
            )
        except Exception as e:
            return LLMResponse(
                text="",
                latency_seconds=time.time() - start_time,
                success=False,
                error=str(e),
            )

    async def _call_llm_with_retry(self, prompt: str, test_input: str) -> LLMResponse:
        """Call LLM with retry logic for rate limiting."""
        for attempt in range(MAX_RETRIES):
            response = await self._call_llm(prompt, test_input)

            if response.success:
                return response

            # Check for rate limiting
            if response.error and (
                "rate" in response.error.lower() or "429" in response.error
            ):
                wait_time = RETRY_DELAY_SECONDS * (attempt + 1)
                await asyncio.sleep(wait_time)
                continue

            # Non-retryable error
            if attempt == MAX_RETRIES - 1:
                return response

            await asyncio.sleep(RETRY_DELAY_SECONDS)

        return response

    def _evaluate_response_quality(
        self, response: str, expected: Optional[str]
    ) -> Tuple[bool, float]:
        """Evaluate the quality of an LLM response."""
        if not response:
            return False, 0.0

        # If expected output provided, compare
        if expected:
            # Simple similarity check (could be enhanced with semantic similarity)
            response_lower = response.lower()
            expected_lower = expected.lower()

            # Check for key phrases
            expected_words = set(expected_lower.split())
            response_words = set(response_lower.split())
            overlap = (
                len(expected_words & response_words) / len(expected_words)
                if expected_words
                else 0
            )

            return overlap >= 0.5, overlap

        # No expected output - check for reasonable response
        has_content = len(response.strip()) > 20
        not_error = not any(
            err in response.lower() for err in ["error", "cannot", "unable", "sorry"]
        )

        return has_content and not_error, 0.85 if (has_content and not_error) else 0.3

    def evaluate(self, prompt: str, test_cases: List[TestCase]) -> BenchmarkResult:
        """Evaluate prompt accuracy (synchronous wrapper)"""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.evaluate_async(prompt, test_cases))

    async def evaluate_async(
        self, prompt: str, test_cases: List[TestCase]
    ) -> BenchmarkResult:
        """Evaluate prompt accuracy with optional real LLM calls."""
        if not test_cases:
            return BenchmarkResult(
                score=0.0, details={"error": "No test cases provided"}
            )

        total_cases = len(test_cases)
        successful_cases = 0
        details = {
            "total_cases": total_cases,
            "test_results": [],
            "use_real_llm": self.use_real_llm,
            "model": self.model if self.use_real_llm else "simulated",
        }

        if self.use_real_llm and LLM_CLIENT_AVAILABLE:
            # Real LLM evaluation
            for i, test_case in enumerate(test_cases):
                # Rate limiting delay between calls
                if i > 0:
                    await asyncio.sleep(RATE_LIMIT_DELAY_SECONDS)

                response = await self._call_llm_with_retry(prompt, test_case.input_data)

                if response.success:
                    is_successful, quality_score = self._evaluate_response_quality(
                        response.text, test_case.expected_output
                    )
                    successful_cases += 1 if is_successful else 0

                    details["test_results"].append(
                        {
                            "case_id": i,
                            "input": test_case.input_data[:100],
                            "success": is_successful,
                            "quality_score": quality_score,
                            "latency_seconds": response.latency_seconds,
                            "response_preview": (
                                response.text[:200] if response.text else None
                            ),
                        }
                    )
                else:
                    details["test_results"].append(
                        {
                            "case_id": i,
                            "input": test_case.input_data[:100],
                            "success": False,
                            "error": response.error,
                        }
                    )
        else:
            # Simulated accuracy evaluation (original behavior)
            for i, test_case in enumerate(test_cases):
                # Placeholder: Assume 85% success rate for demonstration
                is_successful = (i % 100) < 85
                successful_cases += 1 if is_successful else 0

                details["test_results"].append(
                    {
                        "case_id": i,
                        "input": test_case.input_data[:100],
                        "success": is_successful,
                    }
                )

        accuracy = (successful_cases / total_cases) * 100

        return BenchmarkResult(
            score=accuracy,
            details=details,
            metrics={
                "success_rate": accuracy / 100,
                "total_cases": total_cases,
                "successful_cases": successful_cases,
                "failed_cases": total_cases - successful_cases,
            },
        )


class LatencyBenchmark:
    """Evaluate prompt latency and response time."""

    def __init__(self, use_real_llm: bool = False, model: str = DEFAULT_MODEL):
        self.use_real_llm = use_real_llm
        self.model = model

    async def _measure_real_latency(
        self, prompt: str, test_input: str
    ) -> Tuple[float, bool]:
        """Measure actual latency from LLM call."""
        if not LLM_CLIENT_AVAILABLE:
            return 0.0, False

        start_time = time.time()
        try:
            full_prompt = f"{prompt}\n\nInput: {test_input}"
            LLMClient.generate_text(self.model, full_prompt)
            return time.time() - start_time, True
        except Exception:
            return time.time() - start_time, False

    def evaluate(self, prompt: str, test_cases: List[TestCase]) -> BenchmarkResult:
        """Evaluate prompt latency (synchronous wrapper)"""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.evaluate_async(prompt, test_cases))

    async def evaluate_async(
        self, prompt: str, test_cases: List[TestCase]
    ) -> BenchmarkResult:
        """Evaluate prompt latency with optional real measurements."""
        if not test_cases:
            return BenchmarkResult(
                score=100.0, details={"error": "No test cases provided"}
            )

        latencies = []

        if self.use_real_llm and LLM_CLIENT_AVAILABLE:
            # Measure actual latencies (sample first 3 test cases to avoid excessive API calls)
            sample_cases = test_cases[:3]
            for i, test_case in enumerate(sample_cases):
                if i > 0:
                    await asyncio.sleep(RATE_LIMIT_DELAY_SECONDS)

                latency, success = await self._measure_real_latency(
                    prompt, test_case.input_data
                )
                if success:
                    latencies.append(latency)

            if latencies:
                estimated_latency = sum(latencies) / len(latencies)
            else:
                # Fall back to estimation if no successful calls
                estimated_latency = self._estimate_latency(prompt)
        else:
            # Estimate latency based on prompt characteristics
            estimated_latency = self._estimate_latency(prompt)

        # Score: lower latency = higher score
        # 1s = 100, 2s = 75, 3s = 50, 4s+ = 25
        if estimated_latency <= 1.0:
            score = 100.0
        elif estimated_latency <= 2.0:
            score = 100.0 - ((estimated_latency - 1.0) * 25)
        elif estimated_latency <= 3.0:
            score = 75.0 - ((estimated_latency - 2.0) * 25)
        else:
            score = max(25.0, 50.0 - ((estimated_latency - 3.0) * 10))

        prompt_length = len(prompt.split())

        return BenchmarkResult(
            score=score,
            details={
                "prompt_length": prompt_length,
                "use_real_llm": self.use_real_llm,
                "model": self.model if self.use_real_llm else "simulated",
                "measured_latencies": latencies if latencies else None,
                "estimated_latency_seconds": round(estimated_latency, 2),
            },
            metrics={
                "latency_seconds": estimated_latency,
                "tokens_per_second": prompt_length / max(estimated_latency, 0.1),
            },
        )

    def _estimate_latency(self, prompt: str) -> float:
        """Estimate latency based on prompt characteristics."""
        prompt_length = len(prompt.split())
        complexity_indicators = ["reflexion", "multi-agent", "chain", "iteration"]
        complexity_count = sum(
            1 for indicator in complexity_indicators if indicator in prompt.lower()
        )

        base_latency = 1.0  # seconds
        length_penalty = (prompt_length / 1000) * 0.5
        complexity_penalty = complexity_count * 0.3

        return base_latency + length_penalty + complexity_penalty


class CostBenchmark:
    """Evaluate cost efficiency."""

    # Token costs per provider (prices in USD)
    TOKEN_COSTS = {
        "gpt-4o": {"input": 0.0025 / 1000, "output": 0.01 / 1000},
        "gpt-4o-mini": {"input": 0.00015 / 1000, "output": 0.0006 / 1000},
        "gpt-4.1": {"input": 0.002 / 1000, "output": 0.008 / 1000},
        "claude-3-opus": {"input": 0.015 / 1000, "output": 0.075 / 1000},
        "claude-3-sonnet": {"input": 0.003 / 1000, "output": 0.015 / 1000},
        "gemini-1.5-pro": {"input": 0.00125 / 1000, "output": 0.005 / 1000},
        "default": {"input": 0.00001, "output": 0.00003},  # Legacy fallback
    }

    def __init__(self, use_real_llm: bool = False, model: str = DEFAULT_MODEL):
        self.use_real_llm = use_real_llm
        self.model = model
        self._actual_tokens: Dict[str, int] = {}

    def _get_cost_rates(self, model: str) -> Dict[str, float]:
        """Get token costs for a specific model."""
        model_lower = model.lower()
        for model_name, rates in self.TOKEN_COSTS.items():
            if model_name in model_lower:
                return rates
        return self.TOKEN_COSTS["default"]

    def record_actual_usage(self, input_tokens: int, output_tokens: int):
        """Record actual token usage from API responses."""
        self._actual_tokens["input"] = (
            self._actual_tokens.get("input", 0) + input_tokens
        )
        self._actual_tokens["output"] = (
            self._actual_tokens.get("output", 0) + output_tokens
        )

    def evaluate(self, prompt: str, test_cases: List[TestCase]) -> BenchmarkResult:
        """Evaluate cost efficiency."""
        # Get cost rates for the model
        rates = self._get_cost_rates(self.model)

        # Use actual tokens if recorded, otherwise estimate
        if self._actual_tokens:
            prompt_tokens = self._actual_tokens.get("input", 0)
            output_tokens = self._actual_tokens.get("output", 0)
            actual_usage = True
        else:
            # Estimate token usage
            prompt_tokens = int(len(prompt.split()) * 1.3)  # Rough token estimate
            output_tokens = 500  # Assume average 500 token response
            actual_usage = False

        # Calculate costs per test case
        num_test_cases = max(len(test_cases), 1)
        input_cost_per_case = (prompt_tokens / 1000) * rates["input"] * 1000
        output_cost_per_case = (output_tokens / 1000) * rates["output"] * 1000

        total_cost_per_case = input_cost_per_case + output_cost_per_case

        # Score based on cost efficiency
        # Lower cost = higher score
        if total_cost_per_case <= 0.001:
            score = 100.0
        elif total_cost_per_case <= 0.01:
            score = 90.0
        elif total_cost_per_case <= 0.05:
            score = 75.0
        elif total_cost_per_case <= 0.10:
            score = 60.0
        else:
            score = max(40.0, 100.0 - (total_cost_per_case * 100))

        return BenchmarkResult(
            score=score,
            details={
                "model": self.model,
                "actual_usage": actual_usage,
                "estimated_prompt_tokens": int(prompt_tokens),
                "estimated_output_tokens": output_tokens,
                "cost_per_request": round(total_cost_per_case, 6),
                "cost_per_1000_requests": round(total_cost_per_case * 1000, 2),
                "input_rate_per_1k": rates["input"] * 1000,
                "output_rate_per_1k": rates["output"] * 1000,
            },
            metrics={
                "input_tokens": prompt_tokens,
                "output_tokens": output_tokens,
                "cost_usd": total_cost_per_case,
            },
        )


class RobustnessBenchmark:
    """Evaluate prompt robustness and edge case handling."""

    INDICATORS = {
        "error_handling": r"(error|exception|fallback|validation)",
        "edge_cases": r"(edge case|boundary|limit|constraint)",
        "examples": r"(example|instance|sample)",
        "clarity": r"(clear|explicit|specific|precise)",
    }

    def evaluate(self, prompt: str, test_cases: List[TestCase]) -> BenchmarkResult:
        """Evaluate prompt robustness."""
        import re

        prompt_lower = prompt.lower()
        scores = {}

        # Check for robustness indicators
        for indicator, pattern in self.INDICATORS.items():
            matches = len(re.findall(pattern, prompt_lower, re.IGNORECASE))
            scores[indicator] = min(100.0, matches * 20)

        # Calculate overall robustness score
        overall_score = sum(scores.values()) / len(scores)

        # Bonus for having examples
        has_examples = "##" in prompt and "example" in prompt_lower
        if has_examples:
            overall_score = min(100.0, overall_score * 1.2)

        return BenchmarkResult(
            score=overall_score,
            details={
                "indicator_scores": scores,
                "has_examples": has_examples,
                "prompt_length": len(prompt),
            },
            metrics={
                "robustness_indicators": len([s for s in scores.values() if s > 0]),
                "clarity_score": scores.get("clarity", 0),
            },
        )


class PromptPerformanceEvaluator:
    """Automated performance evaluation and benchmarking."""

    def __init__(self, use_real_llm: bool = False, model: str = DEFAULT_MODEL):
        """Initialize evaluator with benchmark suites.

        Args:
            use_real_llm: If True, makes actual LLM API calls; otherwise uses simulated values
            model: The model to use for LLM calls (e.g., 'gpt-4o-mini', 'claude-3-sonnet')
        """
        self.use_real_llm = use_real_llm
        self.model = model

        self.benchmark_suites = {
            "accuracy": AccuracyBenchmark(use_real_llm=use_real_llm, model=model),
            "latency": LatencyBenchmark(use_real_llm=use_real_llm, model=model),
            "cost_efficiency": CostBenchmark(use_real_llm=use_real_llm, model=model),
            "robustness": RobustnessBenchmark(),
        }

    def evaluate_prompt(
        self, prompt: str, test_cases: List[TestCase] = None
    ) -> PerformanceReport:
        """Evaluate prompt across multiple dimensions (synchronous)"""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.evaluate_prompt_async(prompt, test_cases))

    async def evaluate_prompt_async(
        self, prompt: str, test_cases: List[TestCase] = None
    ) -> PerformanceReport:
        """Evaluate prompt across multiple dimensions (async)"""
        if test_cases is None:
            test_cases = []

        report = PerformanceReport(
            prompt_file="prompt_string",
            timestamp=datetime.now().isoformat(),
            use_real_llm=self.use_real_llm,
            model_used=self.model if self.use_real_llm else "simulated",
        )

        # Run all benchmark suites
        for suite_name, suite in self.benchmark_suites.items():
            try:
                # Check if suite has async evaluate method
                if hasattr(suite, "evaluate_async"):
                    result = await suite.evaluate_async(prompt, test_cases)
                else:
                    result = suite.evaluate(prompt, test_cases)
                report.add_score(suite_name, result)
            except Exception as e:
                print(f"Error in {suite_name} benchmark: {e}")
                report.add_score(
                    suite_name, BenchmarkResult(score=0.0, details={"error": str(e)})
                )
            except Exception as e:
                print(f"Error in {suite_name} benchmark: {e}")
                report.add_score(
                    suite_name, BenchmarkResult(score=0.0, details={"error": str(e)})
                )

        # Calculate overall score
        report.calculate_overall_score()

        return report

    def evaluate_prompt_file(
        self, prompt_file: str, test_cases: List[TestCase] = None
    ) -> PerformanceReport:
        """Evaluate a prompt file."""
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                content = f.read()

            report = self.evaluate_prompt(content, test_cases)
            report.prompt_file = prompt_file
            return report

        except Exception as e:
            report = PerformanceReport(
                prompt_file=prompt_file,
                timestamp=datetime.now().isoformat(),
                use_real_llm=self.use_real_llm,
                model_used=self.model if self.use_real_llm else "simulated",
            )
            print(f"Error reading file {prompt_file}: {e}")
            return report

    async def evaluate_prompt_file_async(
        self, prompt_file: str, test_cases: List[TestCase] = None
    ) -> PerformanceReport:
        """Evaluate a prompt file (async version)"""
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                content = f.read()

            report = await self.evaluate_prompt_async(content, test_cases)
            report.prompt_file = prompt_file
            return report

        except Exception as e:
            report = PerformanceReport(
                prompt_file=prompt_file,
                timestamp=datetime.now().isoformat(),
                use_real_llm=self.use_real_llm,
                model_used=self.model if self.use_real_llm else "simulated",
            )
            print(f"Error reading file {prompt_file}: {e}")
            return report

    def generate_recommendations(self, report: PerformanceReport) -> List[str]:
        """Generate performance improvement recommendations."""
        recommendations = []

        if report.accuracy_score < 75:
            recommendations.append(
                "Accuracy: Add more specific examples and constraints to improve task completion"
            )

        if report.latency_score < 70:
            recommendations.append(
                "Latency: Reduce prompt complexity or length to improve response time"
            )

        if report.cost_score < 70:
            recommendations.append(
                "Cost: Optimize prompt length and consider batch processing to reduce costs"
            )

        if report.robustness_score < 75:
            recommendations.append(
                "Robustness: Add error handling examples and edge case documentation"
            )

        return recommendations


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate prompt performance")
    parser.add_argument("file", help="Prompt file to evaluate")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument(
        "--min-score", type=float, default=70.0, help="Minimum passing score"
    )
    parser.add_argument(
        "--use-real-llm",
        action="store_true",
        help="Use real LLM API calls instead of simulated values",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Model to use for LLM calls (default: {DEFAULT_MODEL})",
    )

    args = parser.parse_args()

    # Check for real LLM prerequisites
    if args.use_real_llm and not LLM_CLIENT_AVAILABLE:
        print("⚠️  Warning: LLM client not available. Falling back to simulated mode.")
        print(
            "   Make sure tools/llm_client.py exists and required packages are installed."
        )
        args.use_real_llm = False

    # Evaluate prompt
    evaluator = PromptPerformanceEvaluator(
        use_real_llm=args.use_real_llm, model=args.model
    )
    report = evaluator.evaluate_prompt_file(args.file)

    # Output results
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(f"\n{'='*70}")
        print(f"Performance Evaluation: {report.prompt_file}")
        if report.use_real_llm:
            print(f"Mode: Real LLM ({report.model_used})")
        else:
            print("Mode: Simulated")
        print(f"{'='*70}\n")

        print("Performance Scores:")
        print(f"  Accuracy:       {report.accuracy_score:5.1f}/100")
        print(f"  Latency:        {report.latency_score:5.1f}/100")
        print(f"  Cost Efficiency:{report.cost_score:5.1f}/100")
        print(f"  Robustness:     {report.robustness_score:5.1f}/100")
        print(f"  {'─'*40}")
        print(f"  Overall:        {report.effectivenessScore:5.1f}/100\n")

        # Show detailed metrics
        for suite_name, result in report.benchmark_results.items():
            if result.metrics:
                print(f"{suite_name.title()} Metrics:")
                for metric, value in result.metrics.items():
                    print(f"  {metric}: {value}")
                print()

        # Generate recommendations
        recommendations = evaluator.generate_recommendations(report)
        if recommendations:
            print("Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
            print()

        # Exit with appropriate code
        if report.effectivenessScore < args.min_score:
            print(
                f"❌ Performance below threshold (score {report.effectivenessScore:.1f} < {args.min_score})"
            )
            exit(1)
        else:
            print(f"✅ Performance acceptable (score {report.effectivenessScore:.1f})")
            exit(0)


if __name__ == "__main__":
    main()
