# 🧪 Testing Framework Core

Core testing infrastructure for prompt validation and evaluation across the entire library.

## 📋 Overview

This directory contains the universal testing framework that powers all prompt validation, integration testing, and evaluation workflows. It provides a unified interface for running tests against prompts, agents, and multimodal content.

## 📁 Structure

```
framework/
├── README.md           # This file
├── core/               # Core test runner and orchestration
└── validators/         # Validation framework components
```

## 🎯 Purpose

The testing framework provides:

- **Universal test runner** - Execute any test suite with parallel/sequential execution
- **Multi-provider support** - Azure, GitHub Models, Ollama, local ONNX
- **Test orchestration** - Manage test suites, retries, timeouts, and caching
- **Result aggregation** - Collect metrics, validation results, and performance data
- **Provider auto-detection** - Automatically select available LLM provider
- **Validation pipeline** - Structured output validation with multiple validators

## 🚀 Quick Start

### Run Test Suites

```bash
# Run a single test suite
python testing/run_tests.py test_suites/example_test_suite.yaml

# Run multiple suites
python testing/run_tests.py suite1.yaml suite2.yaml

# Run with specific settings
python testing/run_tests.py test_suite.yaml \
  --parallel \
  --max-workers 5 \
  --filter-tags unit integration \
  --output results.json
```

### Create a Test Suite

```yaml
# test_suite.yaml
name: My Test Suite
description: Tests for my prompts
test_cases:
  - id: test_001
    name: Test basic prompt
    description: Verify basic prompt execution
    test_type: unit
    prompt_id: my_prompt
    inputs:
      user_input: "Hello world"
    expected_outputs:
      contains: "greeting"
    validators:
      - semantic
      - format
    metrics:
      - response_relevance
    timeout: 30
    retries: 3
    tags:
      - quick
      - smoke
```

### Programmatic Usage

```python
import asyncio
from framework.core.test_runner import PromptTestRunner, TestCase, TestType

async def run_tests():
    runner = PromptTestRunner()
    
    # Create test case
    test_case = TestCase(
        id="test_001",
        name="Test Prompt",
        description="Test a simple prompt",
        test_type=TestType.UNIT,
        prompt_id="basic_prompt",
        inputs={"input": "Hello, world!"},
        validators=["semantic"],
        timeout=10
    )
    
    # Run test
    result = await runner.run_single_test(test_case)
    print(f"Status: {result.status.value}")
    print(f"Output: {result.actual_output}")
    print(f"Metrics: {result.metrics}")

asyncio.run(run_tests())
```

## 🔧 Features

### Test Types

| Type | Purpose | Use Cases |
|------|---------|-----------|
| `unit` | Single prompt validation | Individual prompt testing |
| `integration` | Multi-component tests | End-to-end workflows |
| `regression` | Prevent regressions | CI/CD validation |
| `performance` | Speed/cost analysis | Optimization testing |
| `safety` | Security testing | Harmful content detection |
| `quality` | Output quality | Score validation |
| `benchmark` | Comparative testing | Model comparison |

### LLM Provider Support

The framework auto-detects available providers in priority order:

1. **Azure Foundry** - If `AZURE_FOUNDRY_API_KEY` and endpoints configured
2. **Local ONNX** - If `tools/local_model.py` available
3. **GitHub Models** - If `gh` CLI with models extension installed
4. **Ollama** - If Ollama server running on localhost:11434

### Execution Modes

```bash
# Parallel execution (default)
python testing/run_tests.py suite.yaml --parallel --max-workers 10

# Sequential execution
python testing/run_tests.py suite.yaml --max-workers 1

# Filter by tags
python testing/run_tests.py suite.yaml --filter-tags smoke quick

# Filter by type
python testing/run_tests.py suite.yaml --filter-type unit

# Dry run (validate without executing)
python testing/run_tests.py suite.yaml --dry-run
```

### Retry Logic

Tests automatically retry on failure with exponential backoff:

```yaml
test_cases:
  - id: test_flaky
    retries: 3  # Will retry up to 3 times
    timeout: 30  # 30 second timeout per attempt
```

### Caching

Results are automatically cached based on prompt ID and inputs. Cache is bypassed for performance tests.

## 📊 Test Results

### Console Output

```
🧪 Running Test Suite: example_suite
==================================================
✅ Test basic prompt: passed (1.23s)
✅ Test complex workflow: passed (3.45s)
❌ Test edge case: failed (0.89s)
   Error: Output validation failed

==================================================
TEST EXECUTION SUMMARY
==================================================
📊 Suite: example_suite
   Total Tests: 3
   ✅ Passed: 2
   ❌ Failed: 1
   💥 Errors: 0
   Pass Rate: 66.67%
   Execution Time: 5.57s
   Total Cost: $0.0023
```

### JSON Output

```json
{
  "timestamp": "2025-12-04T10:30:00",
  "summary": {
    "suite_name": "example_suite",
    "total_tests": 3,
    "passed": 2,
    "failed": 1,
    "pass_rate": "66.67%",
    "execution_time": "5.57s",
    "total_cost": "$0.0023"
  },
  "metrics": {
    "total_tokens": 1234,
    "avg_execution_time": "1.86s"
  },
  "details": [...]
}
```

## 🔍 Validation

The framework integrates with validators in `framework/validators/`:

```python
# Available validators
validators:
  - json          # JSON structure validation
  - code_python   # Python code validation
  - code_javascript  # JavaScript code validation
  - semantic      # Semantic similarity
  - safety        # Safety checks
  - performance   # Performance metrics
```

See [validators/README.md](validators/README.md) for details.

## 📈 Metrics Collection

Automatically collected metrics:

| Metric | Description |
|--------|-------------|
| `execution_time` | Test execution duration (seconds) |
| `total_tokens` | Combined prompt + completion tokens |
| `prompt_tokens` | Input tokens |
| `completion_tokens` | Output tokens |
| `estimated_cost` | Estimated API cost ($) |
| `output_length` | Response character count |
| `output_lines` | Response line count |

Custom metrics can be added via the metrics collector.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         TestOrchestrator                    │
│  (run_tests.py)                             │
└──────────────┬──────────────────────────────┘
               │
               ├──> Load Test Suites (YAML/JSON)
               │
               ├──> PromptTestRunner
               │    ├─> Provider Auto-detection
               │    ├─> Test Execution (parallel/sequential)
               │    ├─> Retry Logic & Timeouts
               │    ├─> Result Caching
               │    └─> Validation Pipeline
               │
               ├──> Validators (framework/validators/)
               │    ├─> JSON Validator
               │    ├─> Code Validator
               │    ├─> Semantic Validator
               │    └─> Safety Validator
               │
               └──> Results
                    ├─> Console Summary
                    ├─> JSON Report
                    └─> Log Files
```

## 🔗 Integration Points

### With Validators

```python
# Register custom validator
from framework.validators.base_validator import BaseValidator

class MyValidator(BaseValidator):
    async def validate(self, output, expected):
        # Custom validation logic
        return True

runner.validators['my_validator'] = MyValidator()
```

### With CI/CD

```yaml
# .github/workflows/test.yml
- name: Run test suite
  run: |
    python testing/run_tests.py test_suite.yaml \
      --output results.json
  
- name: Check results
  run: |
    python -c "
    import json
    with open('results.json') as f:
        results = json.load(f)
    exit(0 if results['summary']['failed'] == 0 else 1)
    "
```

## 📦 Dependencies

```bash
# Required
pip install pyyaml pytest

# Optional (for specific providers)
pip install onnxruntime-genai  # Local ONNX models
gh extension install github/gh-models  # GitHub Models
```

## 🐛 Troubleshooting

### No Provider Available

```bash
# Check available providers
python -c "
from framework.core.test_runner import PromptTestRunner
runner = PromptTestRunner()
print(f'Provider: {runner._detect_provider()}')
"
```

### Timeout Issues

Increase timeout values in test suite:

```yaml
test_cases:
  - timeout: 60  # Increase to 60 seconds
```

### Rate Limiting

Use sequential execution to avoid rate limits:

```bash
python testing/run_tests.py suite.yaml --max-workers 1
```

## 📖 See Also

- [core/README.md](core/README.md) - Test runner implementation details
- [validators/README.md](validators/README.md) - Validation framework
- [../integration/README.md](../integration/README.md) - Integration tests
- [../unit/README.md](../unit/README.md) - Unit tests
- [../../docs/ARCHITECTURE_PLAN.md](../../docs/ARCHITECTURE_PLAN.md) - Overall architecture

---

**Built with ❤️ for reliable prompt testing**
