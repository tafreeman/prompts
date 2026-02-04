"""Universal test runner for all prompt types and agents."""

import asyncio
import hashlib
import json
import logging
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestType(Enum):
    """Types of tests that can be run"""
    __test__ = False  # Not a pytest test class
    UNIT = "unit"
    INTEGRATION = "integration"
    REGRESSION = "regression"
    PERFORMANCE = "performance"
    SAFETY = "safety"
    QUALITY = "quality"
    BENCHMARK = "benchmark"


class TestStatus(Enum):
    """Possible test execution statuses"""
    __test__ = False  # Not a pytest test class
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    WARNING = "warning"
    TIMEOUT = "timeout"


@dataclass
class TestCase:
    """Individual test case definition"""
    __test__ = False  # Not a pytest test class
    id: str
    name: str
    description: str
    test_type: TestType
    prompt_id: str
    inputs: Dict[str, Any]
    expected_outputs: Optional[Dict[str, Any]] = None
    validators: List[str] = field(default_factory=list)
    metrics: List[str] = field(default_factory=list)
    timeout: int = 30
    retries: int = 3
    tags: List[str] = field(default_factory=list)
    priority: int = 0
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data["test_type"] = self.test_type.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestCase":
        """Create from dictionary."""
        data["test_type"] = TestType(data["test_type"])
        return cls(**data)


@dataclass
class TestResult:
    """Test execution result"""
    __test__ = False  # Not a pytest test class
    test_case: TestCase
    status: TestStatus
    actual_output: Any
    execution_time: float
    token_usage: Dict[str, int]
    metrics: Dict[str, float]
    validation_results: Dict[str, bool]
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    retry_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "test_case_id": self.test_case.id,
            "test_case_name": self.test_case.name,
            "status": self.status.value,
            "execution_time": self.execution_time,
            "token_usage": self.token_usage,
            "metrics": self.metrics,
            "validation_results": self.validation_results,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat(),
            "retry_count": self.retry_count,
        }

    @property
    def is_success(self) -> bool:
        """Check if test passed."""
        return self.status == TestStatus.PASSED


class PromptTestRunner:
    """Main test execution engine."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize test runner with configuration."""
        self.config = self._load_config(config_path) if config_path else {}
        self.test_suites: Dict[str, List[TestCase]] = {}
        self.results: List[TestResult] = []
        self.validators = {}
        self.evaluators = {}
        self.metrics_collector = None
        self.cache = {}
        self.executor = ThreadPoolExecutor(max_workers=10)

        # Initialize components
        self._initialize_components()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        path = Path(config_path)
        if path.exists():
            with open(path, "r") as f:
                return yaml.safe_load(f)
        return {}

    def _initialize_components(self):
        """Initialize validators, evaluators, and metrics."""
        # Import here to avoid circular dependencies
        # Use proper relative import from parent module
        from ..validators import (
            CodeValidator,
            JSONValidator,
            PerformanceValidator,
            SafetyValidator,
            SemanticValidator,
        )

        # Initialize validators
        self.validators = {
            "json": JSONValidator() if JSONValidator else None,
            "code_python": CodeValidator(language="python"),
            "code_javascript": CodeValidator(language="javascript"),
            "semantic": SemanticValidator([]),
            "safety": SafetyValidator() if SafetyValidator else None,
            "performance": PerformanceValidator() if PerformanceValidator else None,
        }

        # Initialize evaluators and metrics (Placeholder for future implementation)
        self.evaluators = {}
        self.metrics_collector = None

    def _detect_provider(self) -> str:
        """Auto-detect best available LLM provider.

        Priority: Local ONNX > gh CLI > Ollama
        """
        import os
        import shutil

        # Check for Azure Foundry
        if (
            "AZURE_FOUNDRY_API_KEY" in os.environ
            and "AZURE_FOUNDRY_ENDPOINT_1" in os.environ
        ):
            return "azure"

        # Check for local ONNX model
        local_model_path = Path("tools/local_model.py")
        if local_model_path.exists():
            return "local"

        # Check for GitHub CLI with models extension
        if shutil.which("gh"):
            # Check if gh models is available
            try:
                import subprocess

                result = subprocess.run(
                    ["gh", "models", "--help"], capture_output=True, timeout=5
                )
                if result.returncode == 0:
                    return "gh"
            except Exception:
                pass

        # Check for Ollama
        if shutil.which("ollama") or os.path.exists("/usr/local/bin/ollama"):
            return "ollama"

        # Default fallback
        return "local"

    async def _execute_local_model(
        self, prompt: Dict, inputs: Dict
    ) -> Tuple[Any, Dict[str, int]]:
        """Execute using local ONNX model."""
        # Format prompt
        formatted = self._format_prompt(prompt.get("template", ""), inputs)

        # Mock implementation - in production would use tools/local_model.py
        await asyncio.sleep(0.1)
        return f"Local model response for: {formatted[:50]}...", {
            "prompt_tokens": len(formatted) // 4,
            "completion_tokens": 50,
            "total_tokens": len(formatted) // 4 + 50,
        }

    async def _execute_gh_models(
        self, prompt: Dict, inputs: Dict
    ) -> Tuple[Any, Dict[str, int]]:
        """Execute using GitHub Models CLI (gh models eval)."""
        import subprocess

        formatted = self._format_prompt(prompt.get("template", ""), inputs)
        model = prompt.get("model", "gpt-4o-mini")

        try:
            result = await asyncio.to_thread(
                subprocess.run,
                ["gh", "models", "run", model, "-p", formatted],
                capture_output=True,
                text=True,
                timeout=60,
            )
            output = (
                result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
            )
        except Exception as e:
            output = f"gh models execution failed: {e}"

        return output, {
            "prompt_tokens": len(formatted) // 4,
            "completion_tokens": len(output) // 4,
            "total_tokens": (len(formatted) + len(output)) // 4,
        }

    async def _execute_ollama(
        self, prompt: Dict, inputs: Dict
    ) -> Tuple[Any, Dict[str, int]]:
        """Execute using local Ollama server."""
        import urllib.error
        import urllib.request

        formatted = self._format_prompt(prompt.get("template", ""), inputs)
        model = prompt.get("model", "llama3")

        try:
            payload = json.dumps(
                {"model": model, "prompt": formatted, "stream": False}
            ).encode()

            request = urllib.request.Request(
                "http://localhost:11434/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"},
            )

            response = await asyncio.to_thread(
                urllib.request.urlopen, request, timeout=60
            )
            result = json.loads(response.read().decode())
            output = result.get("response", "")

        except Exception as e:
            output = f"Ollama execution failed: {e}"

        return output, {
            "prompt_tokens": len(formatted) // 4,
            "completion_tokens": len(output) // 4,
            "total_tokens": (len(formatted) + len(output)) // 4,
        }

    async def _execute_azure_foundry(
        self, prompt: Dict, inputs: Dict
    ) -> Tuple[Any, Dict[str, int]]:
        """Execute using Azure Foundry API (Azure OpenAI-compatible endpoints).

        Environment variables required:
          - AZURE_FOUNDRY_API_KEY: API key for authentication
          - AZURE_FOUNDRY_ENDPOINT_1: Endpoint URL for phi4mini
          - AZURE_FOUNDRY_ENDPOINT_2: Endpoint URL for mistral
        """
        import os
        import urllib.error
        import urllib.request

        formatted = self._format_prompt(prompt.get("template", ""), inputs)
        model = prompt.get("model", "phi4mini")

        # Get API key
        api_key = os.environ.get("AZURE_FOUNDRY_API_KEY")
        if not api_key:
            return "Error: AZURE_FOUNDRY_API_KEY not set", {"total_tokens": 0}

        # Determine endpoint based on model
        if model in ("phi4mini", "phi4", "phi", "1"):
            endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT_1")
        elif model in ("mistral", "2"):
            endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT_2")
        else:
            endpoint = os.environ.get(f"AZURE_FOUNDRY_ENDPOINT_{model}")
            if not endpoint:
                endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT_1")

        if not endpoint:
            return "Error: Azure Foundry endpoint not configured", {"total_tokens": 0}

        # Ensure endpoint ends with /chat/completions
        if not endpoint.endswith("/chat/completions"):
            endpoint = endpoint.rstrip("/") + "/chat/completions"

        # Add API version if not present
        if "api-version" not in endpoint:
            endpoint += "?api-version=2024-02-15-preview"

        try:
            messages = [{"role": "user", "content": formatted}]
            if prompt.get("system"):
                messages.insert(0, {"role": "system", "content": prompt["system"]})

            payload = json.dumps(
                {
                    "messages": messages,
                    "temperature": prompt.get("temperature", 0.7),
                    "max_tokens": prompt.get("max_tokens", 2000),
                }
            ).encode()

            request = urllib.request.Request(
                endpoint,
                data=payload,
                headers={"Content-Type": "application/json", "api-key": api_key},
            )

            response = await asyncio.to_thread(
                urllib.request.urlopen, request, timeout=120
            )
            result = json.loads(response.read().decode())
            output = result["choices"][0]["message"]["content"]

            # Extract token usage if available
            usage = result.get("usage", {})
            token_usage = {
                "prompt_tokens": usage.get("prompt_tokens", len(formatted) // 4),
                "completion_tokens": usage.get("completion_tokens", len(output) // 4),
                "total_tokens": usage.get(
                    "total_tokens", (len(formatted) + len(output)) // 4
                ),
            }

        except Exception as e:
            output = f"Azure Foundry execution failed: {e}"
            token_usage = {"total_tokens": 0}

        return output, token_usage

    def load_test_suite(self, suite_path: str):
        """Load test suite from file."""
        path = Path(suite_path)

        if path.suffix == ".yaml":
            with open(path, "r") as f:
                suite_data = yaml.safe_load(f)
        elif path.suffix == ".json":
            with open(path, "r") as f:
                suite_data = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

        # Parse test cases
        suite_name = suite_data.get("name", path.stem)
        test_cases = []

        for case_data in suite_data.get("test_cases", []):
            test_case = TestCase.from_dict(case_data)
            test_cases.append(test_case)

        self.test_suites[suite_name] = test_cases
        logger.info(
            f"Loaded test suite '{suite_name}' with {len(test_cases)} test cases"
        )

    async def run_test_suite(
        self,
        suite_name: str,
        parallel: bool = True,
        max_workers: int = 10,
        filter_tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Execute a complete test suite."""

        logger.info(f"🧪 Running Test Suite: {suite_name}")
        logger.info("=" * 50)

        test_cases = self.test_suites.get(suite_name, [])
        if not test_cases:
            raise ValueError(f"Test suite '{suite_name}' not found")

        # Filter by tags if specified
        if filter_tags:
            test_cases = [
                tc for tc in test_cases if any(tag in tc.tags for tag in filter_tags)
            ]

        # Sort by priority
        test_cases.sort(key=lambda x: x.priority, reverse=True)

        start_time = time.time()

        if parallel:
            # Run tests in parallel with semaphore for rate limiting
            semaphore = asyncio.Semaphore(max_workers)
            tasks = [
                self._run_test_with_semaphore(test_case, semaphore)
                for test_case in test_cases
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        else:
            # Run tests sequentially
            results = []
            for test_case in test_cases:
                result = await self.run_single_test(test_case)
                results.append(result)
                self._print_test_result(result)

        # Process results
        suite_results = self._process_suite_results(results, suite_name)
        suite_results["execution_time"] = time.time() - start_time

        # Generate report
        report = self._generate_report(suite_results)

        # Save results
        self._save_results(report)

        return report

    async def _run_test_with_semaphore(
        self, test_case: TestCase, semaphore: asyncio.Semaphore
    ) -> TestResult:
        """Run test with semaphore for rate limiting."""
        async with semaphore:
            return await self.run_single_test(test_case)

    async def run_single_test(self, test_case: TestCase) -> TestResult:
        """Execute a single test case with retry logic."""

        logger.info(f"Running test: {test_case.name}")

        for attempt in range(test_case.retries):
            try:
                result = await self._execute_test(test_case)

                if result.is_success or attempt == test_case.retries - 1:
                    result.retry_count = attempt
                    return result

                logger.warning(
                    f"Test {test_case.id} failed, retrying... (attempt {attempt + 1}/{test_case.retries})"
                )
                await asyncio.sleep(2**attempt)  # Exponential backoff

            except Exception as e:
                if attempt == test_case.retries - 1:
                    return TestResult(
                        test_case=test_case,
                        status=TestStatus.ERROR,
                        actual_output=None,
                        execution_time=0,
                        token_usage={},
                        metrics={},
                        validation_results={},
                        error_message=str(e),
                        stack_trace=traceback.format_exc(),
                        retry_count=attempt,
                    )

    async def _execute_test(self, test_case: TestCase) -> TestResult:
        """Execute a single test case."""

        start_time = time.time()

        try:
            # Check cache
            cache_key = self._get_cache_key(test_case)
            if cache_key in self.cache and test_case.test_type != TestType.PERFORMANCE:
                logger.info(f"Using cached result for {test_case.id}")
                return self.cache[cache_key]

            # Execute the prompt/agent
            actual_output, token_usage = await asyncio.wait_for(
                self._execute_prompt(test_case.prompt_id, test_case.inputs),
                timeout=test_case.timeout,
            )

            # Validate output
            validation_results = await self._validate_output(
                actual_output, test_case.expected_outputs, test_case.validators
            )

            # Collect metrics
            metrics = await self._collect_metrics(
                test_case, actual_output, token_usage, time.time() - start_time
            )

            # Determine status
            if all(validation_results.values()):
                status = TestStatus.PASSED
            elif any(v == False for v in validation_results.values()):
                status = TestStatus.FAILED
            else:
                status = TestStatus.WARNING

            result = TestResult(
                test_case=test_case,
                status=status,
                actual_output=actual_output,
                execution_time=time.time() - start_time,
                token_usage=token_usage,
                metrics=metrics,
                validation_results=validation_results,
            )

            # Cache result
            self.cache[cache_key] = result

            return result

        except asyncio.TimeoutError:
            return TestResult(
                test_case=test_case,
                status=TestStatus.TIMEOUT,
                actual_output=None,
                execution_time=test_case.timeout,
                token_usage={},
                metrics={},
                validation_results={},
                error_message=f"Test timed out after {test_case.timeout} seconds",
            )

        except Exception as e:
            return TestResult(
                test_case=test_case,
                status=TestStatus.ERROR,
                actual_output=None,
                execution_time=time.time() - start_time,
                token_usage={},
                metrics={},
                validation_results={},
                error_message=str(e),
                stack_trace=traceback.format_exc(),
            )

    def _get_cache_key(self, test_case: TestCase) -> str:
        """Generate cache key for test case."""
        data = f"{test_case.prompt_id}:{json.dumps(test_case.inputs, sort_keys=True)}"
        return hashlib.md5(data.encode()).hexdigest()

    async def _execute_prompt(
        self, prompt_id: str, inputs: Dict[str, Any]
    ) -> Tuple[Any, Dict[str, int]]:
        """Execute a prompt or agent with given inputs."""

        # Load prompt/agent
        prompt = await self._load_prompt(prompt_id)

        # Determine execution type
        if prompt.get("type") == "agent":
            return await self._execute_agent(prompt, inputs)
        elif prompt.get("modalities"):
            return await self._execute_multimodal(prompt, inputs)
        else:
            return await self._execute_text_prompt(prompt, inputs)

    async def _load_prompt(self, prompt_id: str) -> Dict[str, Any]:
        """Load prompt from file system."""
        # This would load from the actual prompt files
        # For now, return a mock prompt
        return {
            "id": prompt_id,
            "template": "You are a helpful assistant. {input}",
            "model": "gpt-4o-mini",
            "temperature": 0.7,
        }

    async def _execute_text_prompt(
        self, prompt: Dict, inputs: Dict
    ) -> Tuple[Any, Dict[str, int]]:
        """Execute standard text prompt using detected provider."""

        provider = self._detect_provider()

        if provider == "azure":
            return await self._execute_azure_foundry(prompt, inputs)
        elif provider == "gh":
            return await self._execute_gh_models(prompt, inputs)
        elif provider == "ollama":
            return await self._execute_ollama(prompt, inputs)
        else:
            return await self._execute_local_model(prompt, inputs)

    async def _execute_multimodal(
        self, prompt: Dict, inputs: Dict
    ) -> Tuple[Any, Dict[str, int]]:
        """Execute multi-modal prompt."""
        # Mock implementation
        await asyncio.sleep(0.2)
        return "Mock multimodal response", {"total_tokens": 500}

    async def _execute_agent(
        self, prompt: Dict, inputs: Dict
    ) -> Tuple[Any, Dict[str, int]]:
        """Execute agent prompt."""
        # Mock implementation
        await asyncio.sleep(0.3)
        return {"agent_output": "Task completed"}, {"total_tokens": 1000}

    def _format_prompt(self, template: str, inputs: Dict[str, Any]) -> str:
        """Format prompt template with inputs."""
        try:
            return template.format(**inputs)
        except KeyError as e:
            logger.error(f"Missing input key: {e}")
            return template

    async def _validate_output(
        self, output: Any, expected: Optional[Dict[str, Any]], validators: List[str]
    ) -> Dict[str, bool]:
        """Run validators on output."""

        results = {}

        for validator_name in validators:
            validator = self.validators.get(validator_name)
            if validator:
                try:
                    results[validator_name] = await validator.validate(output, expected)
                except Exception as e:
                    logger.error(f"Validator {validator_name} failed: {e}")
                    results[validator_name] = False
            else:
                logger.warning(f"Validator {validator_name} not found")
                results[validator_name] = None

        return results

    async def _collect_metrics(
        self,
        test_case: TestCase,
        output: Any,
        token_usage: Dict[str, int],
        execution_time: float,
    ) -> Dict[str, float]:
        """Collect performance and quality metrics."""

        metrics = {
            "execution_time": execution_time,
            "total_tokens": sum(token_usage.values()),
            "prompt_tokens": token_usage.get("prompt_tokens", 0),
            "completion_tokens": token_usage.get("completion_tokens", 0),
        }

        # Cost estimation (example rates)
        metrics["estimated_cost"] = (
            metrics["prompt_tokens"] * 0.00001  # $0.01 per 1K tokens
            + metrics["completion_tokens"] * 0.00003  # $0.03 per 1K tokens
        )

        # Quality metrics
        if output and isinstance(output, str):
            metrics["output_length"] = len(output)
            metrics["output_lines"] = output.count("\n") + 1

        # Custom metrics
        if self.metrics_collector:
            for metric_name in test_case.metrics:
                try:
                    metric_value = await self.metrics_collector.calculate_metric(
                        metric_name, output, test_case
                    )
                    metrics[metric_name] = metric_value
                except Exception as e:
                    logger.error(f"Metric {metric_name} failed: {e}")
                    metrics[metric_name] = -1

        return metrics

    def _process_suite_results(
        self, results: List[TestResult], suite_name: str
    ) -> Dict[str, Any]:
        """Process and aggregate test suite results."""

        total = len(results)
        passed = sum(1 for r in results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in results if r.status == TestStatus.FAILED)
        errors = sum(1 for r in results if r.status == TestStatus.ERROR)
        skipped = sum(1 for r in results if r.status == TestStatus.SKIPPED)
        timeouts = sum(1 for r in results if r.status == TestStatus.TIMEOUT)

        total_tokens = sum(sum(r.token_usage.values()) for r in results)
        total_cost = sum(r.metrics.get("estimated_cost", 0) for r in results)
        avg_execution_time = (
            sum(r.execution_time for r in results) / total if total > 0 else 0
        )

        return {
            "suite_name": suite_name,
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
            "timeouts": timeouts,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "avg_execution_time": avg_execution_time,
            "results": [r.to_dict() for r in results],
        }

    def _generate_report(self, suite_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive test report."""

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "suite_name": suite_results["suite_name"],
                "total_tests": suite_results["total_tests"],
                "passed": suite_results["passed"],
                "failed": suite_results["failed"],
                "errors": suite_results["errors"],
                "skipped": suite_results["skipped"],
                "timeouts": suite_results["timeouts"],
                "pass_rate": f"{suite_results['pass_rate']:.2f}%",
                "execution_time": f"{suite_results.get('execution_time', 0):.2f}s",
                "total_cost": f"${suite_results['total_cost']:.4f}",
            },
            "metrics": {
                "total_tokens": suite_results["total_tokens"],
                "avg_execution_time": f"{suite_results['avg_execution_time']:.2f}s",
            },
            "details": suite_results["results"],
        }

        # Add failure analysis
        failures = [r for r in suite_results["results"] if r["status"] == "failed"]
        if failures:
            report["failure_analysis"] = self._analyze_failures(failures)

        return report

    def _analyze_failures(self, failures: List[Dict]) -> Dict[str, Any]:
        """Analyze failure patterns."""

        failure_reasons = {}
        for failure in failures:
            reason = failure.get("error_message", "Unknown")
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1

        return {
            "total_failures": len(failures),
            "failure_reasons": failure_reasons,
            "most_common_failure": (
                max(failure_reasons, key=failure_reasons.get)
                if failure_reasons
                else None
            ),
        }

    def _print_test_result(self, result: TestResult):
        """Print test result to console."""

        status_symbols = {
            TestStatus.PASSED: "✅",
            TestStatus.FAILED: "❌",
            TestStatus.ERROR: "💥",
            TestStatus.SKIPPED: "⏭️",
            TestStatus.TIMEOUT: "⏱️",
            TestStatus.WARNING: "⚠️",
        }

        symbol = status_symbols.get(result.status, "❓")
        print(
            f"{symbol} {result.test_case.name}: {result.status.value} ({result.execution_time:.2f}s)"
        )

        if result.error_message:
            print(f"   Error: {result.error_message}")

    def _save_results(self, report: Dict[str, Any]):
        """Save test results to file."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("testing/results")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"test_results_{timestamp}.json"

        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Results saved to {output_file}")


# Example usage
if __name__ == "__main__":

    async def main():
        runner = PromptTestRunner()

        # Create sample test case
        test_case = TestCase(
            id="test_001",
            name="Test Basic Prompt",
            description="Test a simple text prompt",
            test_type=TestType.UNIT,
            prompt_id="basic_prompt",
            inputs={"input": "Hello, world!"},
            expected_outputs={"contains": "response"},
            validators=["semantic"],
            metrics=["response_relevance"],
            timeout=10,
        )

        # Run single test
        result = await runner.run_single_test(test_case)
        print(f"Test result: {result.status.value}")

    asyncio.run(main())
