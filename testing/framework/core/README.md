# 🎯 Core Testing Utilities

Universal test runner implementation and core testing infrastructure.

## 📋 Overview

This directory contains the core test execution engine (`test_runner.py`) that powers all testing in the framework. It provides a flexible, provider-agnostic interface for executing prompts and collecting results.

## 📁 Files

```
core/
├── README.md          # This file
├── __init__.py        # Package initialization
└── test_runner.py     # Main test runner implementation
```

## 🚀 Quick Start

### Basic Usage

```python
import asyncio
from framework.core.test_runner import (
    PromptTestRunner,
    TestCase,
    TestType,
    TestStatus
)

async def main():
    # Initialize runner
    runner = PromptTestRunner()
    
    # Create test case
    test = TestCase(
        id="test_001",
        name="Simple Test",
        description="Test basic functionality",
        test_type=TestType.UNIT,
        prompt_id="my_prompt",
        inputs={"query": "Hello"},
        validators=["semantic"],
        timeout=10
    )
    
    # Execute test
    result = await runner.run_single_test(test)
    
    # Check result
    print(f"Status: {result.status}")
    print(f"Output: {result.actual_output}")
    print(f"Tokens: {result.token_usage}")
    print(f"Time: {result.execution_time:.2f}s")

asyncio.run(main())
```

### Load and Run Test Suites

```python
runner = PromptTestRunner()

# Load YAML suite
runner.load_test_suite("my_suite.yaml")

# Run suite
results = await runner.run_test_suite(
    "my_suite",
    parallel=True,
    max_workers=5
)

# Access results
print(f"Pass rate: {results['pass_rate']:.2f}%")
```

## 🏗️ Core Components

### 1. PromptTestRunner

Main test execution engine.

**Responsibilities:**
- Load test suites from YAML/JSON
- Execute tests with retry logic
- Manage LLM provider connections
- Collect metrics and validation results
- Cache results for performance
- Generate comprehensive reports

**Key Methods:**

```python
class PromptTestRunner:
    def __init__(self, config_path: Optional[str] = None)
    
    def load_test_suite(self, suite_path: str)
    
    async def run_test_suite(
        self,
        suite_name: str,
        parallel: bool = True,
        max_workers: int = 10,
        filter_tags: Optional[List[str]] = None
    ) -> Dict[str, Any]
    
    async def run_single_test(self, test_case: TestCase) -> TestResult
```

### 2. TestCase

Defines an individual test case.

```python
@dataclass
class TestCase:
    id: str                                    # Unique identifier
    name: str                                  # Display name
    description: str                           # Test description
    test_type: TestType                        # Test category
    prompt_id: str                             # Target prompt
    inputs: Dict[str, Any]                     # Input variables
    expected_outputs: Optional[Dict] = None    # Expected results
    validators: List[str] = []                 # Validators to run
    metrics: List[str] = []                    # Metrics to collect
    timeout: int = 30                          # Timeout (seconds)
    retries: int = 3                           # Retry attempts
    tags: List[str] = []                       # Categorization tags
    priority: int = 0                          # Execution priority
    dependencies: List[str] = []               # Dependency test IDs
```

### 3. TestResult

Captures test execution results.

```python
@dataclass
class TestResult:
    test_case: TestCase                        # Original test case
    status: TestStatus                         # PASSED/FAILED/ERROR/etc
    actual_output: Any                         # LLM response
    execution_time: float                      # Duration (seconds)
    token_usage: Dict[str, int]                # Token counts
    metrics: Dict[str, float]                  # Collected metrics
    validation_results: Dict[str, bool]        # Validator outcomes
    error_message: Optional[str] = None        # Error description
    stack_trace: Optional[str] = None          # Full error trace
    timestamp: datetime                        # Execution timestamp
    retry_count: int = 0                       # Number of retries
```

### 4. Test Types

```python
class TestType(Enum):
    UNIT = "unit"                    # Single prompt tests
    INTEGRATION = "integration"      # Multi-component tests
    REGRESSION = "regression"        # Prevent regressions
    PERFORMANCE = "performance"      # Speed/cost analysis
    SAFETY = "safety"               # Security testing
    QUALITY = "quality"             # Output quality
    BENCHMARK = "benchmark"         # Comparative testing
```

### 5. Test Status

```python
class TestStatus(Enum):
    PASSED = "passed"       # All validations passed
    FAILED = "failed"       # Validation failure
    SKIPPED = "skipped"     # Test skipped
    ERROR = "error"         # Execution error
    WARNING = "warning"     # Passed with warnings
    TIMEOUT = "timeout"     # Execution timeout
```

## 🔌 LLM Provider Support

The test runner auto-detects and connects to available LLM providers.

### Provider Priority

1. **Azure Foundry** - Production API (requires `AZURE_FOUNDRY_API_KEY`)
2. **Local ONNX** - Local models (requires `tools/local_model.py`)
3. **GitHub Models** - `gh` CLI (requires `gh models` extension)
4. **Ollama** - Local inference (requires Ollama server)

### Provider Detection

```python
def _detect_provider(self) -> str:
    """Auto-detect best available LLM provider."""
    # Check for Azure Foundry
    if "AZURE_FOUNDRY_API_KEY" in os.environ:
        return "azure"
    
    # Check for local ONNX model
    if Path("tools/local_model.py").exists():
        return "local"
    
    # Check for GitHub CLI
    if shutil.which("gh"):
        return "gh"
    
    # Check for Ollama
    if shutil.which("ollama"):
        return "ollama"
    
    return "local"  # Fallback
```

### Provider Configuration

**Azure Foundry:**
```bash
export AZURE_FOUNDRY_API_KEY="your-key"
export AZURE_FOUNDRY_ENDPOINT_1="https://..."
export AZURE_FOUNDRY_ENDPOINT_2="https://..."
```

**GitHub Models:**
```bash
gh auth login
gh extension install github/gh-models
```

**Ollama:**
```bash
ollama serve  # Start server on localhost:11434
```

## ⚙️ Execution Pipeline

### Test Execution Flow

```
1. Load Test Suite
   ├─> Parse YAML/JSON
   ├─> Create TestCase objects
   └─> Apply filters (tags, type)

2. Execute Tests
   ├─> Parallel or sequential mode
   ├─> For each test:
   │   ├─> Load prompt
   │   ├─> Format with inputs
   │   ├─> Execute via provider
   │   ├─> Validate output
   │   ├─> Collect metrics
   │   └─> Cache result
   └─> Aggregate results

3. Generate Report
   ├─> Calculate statistics
   ├─> Analyze failures
   ├─> Format output (JSON/console)
   └─> Save to file
```

### Retry Logic

Tests automatically retry on failure with exponential backoff:

```python
for attempt in range(test_case.retries):
    try:
        result = await self._execute_test(test_case)
        if result.is_success:
            return result
    except Exception:
        if attempt == test_case.retries - 1:
            # Final attempt failed
            raise
        # Wait before retry
        await asyncio.sleep(2 ** attempt)
```

### Timeout Handling

```python
async def run_single_test(self, test_case: TestCase):
    try:
        result = await asyncio.wait_for(
            self._execute_test(test_case),
            timeout=test_case.timeout
        )
    except asyncio.TimeoutError:
        return TestResult(
            status=TestStatus.TIMEOUT,
            error_message=f"Timed out after {test_case.timeout}s"
        )
```

## 📊 Metrics Collection

Automatically collected metrics:

```python
async def _collect_metrics(self, test_case, output, token_usage, execution_time):
    metrics = {
        "execution_time": execution_time,
        "total_tokens": sum(token_usage.values()),
        "prompt_tokens": token_usage.get("prompt_tokens", 0),
        "completion_tokens": token_usage.get("completion_tokens", 0),
        "estimated_cost": calculate_cost(token_usage),
        "output_length": len(str(output)),
        "output_lines": str(output).count('\n') + 1
    }
    
    # Custom metrics from metrics collector
    for metric_name in test_case.metrics:
        metric_value = await self.metrics_collector.calculate_metric(
            metric_name, output, test_case
        )
        metrics[metric_name] = metric_value
    
    return metrics
```

## 🎯 Validation Pipeline

```python
async def _validate_output(self, output, expected, validators):
    results = {}
    
    for validator_name in validators:
        validator = self.validators.get(validator_name)
        if validator:
            results[validator_name] = await validator.validate(
                output, 
                expected
            )
    
    return results
```

See [../validators/README.md](../validators/README.md) for validator details.

## 💾 Result Caching

Results are cached to avoid redundant executions:

```python
def _get_cache_key(self, test_case: TestCase) -> str:
    """Generate cache key from test case."""
    data = f"{test_case.prompt_id}:{json.dumps(test_case.inputs, sort_keys=True)}"
    return hashlib.md5(data.encode()).hexdigest()

async def _execute_test(self, test_case: TestCase):
    # Check cache
    cache_key = self._get_cache_key(test_case)
    if cache_key in self.cache:
        return self.cache[cache_key]
    
    # Execute and cache
    result = await self._execute_prompt(...)
    self.cache[cache_key] = result
    return result
```

**Note:** Performance tests bypass cache to ensure accurate measurements.

## 📈 Report Generation

### Summary Statistics

```python
def _process_suite_results(self, results, suite_name):
    return {
        "suite_name": suite_name,
        "total_tests": len(results),
        "passed": count_by_status(results, TestStatus.PASSED),
        "failed": count_by_status(results, TestStatus.FAILED),
        "errors": count_by_status(results, TestStatus.ERROR),
        "pass_rate": (passed / total * 100),
        "total_tokens": sum(r.token_usage for r in results),
        "total_cost": sum(r.metrics.get("estimated_cost")),
        "avg_execution_time": mean(r.execution_time for r in results)
    }
```

### Failure Analysis

```python
def _analyze_failures(self, failures):
    failure_reasons = {}
    for failure in failures:
        reason = failure.get("error_message", "Unknown")
        failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
    
    return {
        "total_failures": len(failures),
        "failure_reasons": failure_reasons,
        "most_common_failure": max(failure_reasons, key=failure_reasons.get)
    }
```

## 🔧 Configuration

### Config File Format (Optional)

```yaml
# test_config.yaml
default_timeout: 30
default_retries: 3
max_parallel_workers: 10
enable_caching: true

providers:
  azure:
    timeout: 120
  local:
    model_path: "models/phi4mini"
  gh:
    model: "gpt-4o-mini"
```

Load with:
```python
runner = PromptTestRunner(config_path="test_config.yaml")
```

## 🐛 Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

runner = PromptTestRunner()
# Detailed logs will be printed
```

Access detailed test information:

```python
result = await runner.run_single_test(test_case)

print(f"Status: {result.status}")
print(f"Error: {result.error_message}")
print(f"Stack trace: {result.stack_trace}")
print(f"Validation: {result.validation_results}")
print(f"Metrics: {result.metrics}")
```

## 📖 See Also

- [../README.md](../README.md) - Framework overview
- [../validators/README.md](../validators/README.md) - Validation framework
- [../../integration/README.md](../../integration/README.md) - Integration tests
- [../../unit/README.md](../../unit/README.md) - Unit tests

---

**Built with ❤️ for universal prompt testing**
