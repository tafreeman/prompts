# 🧪 Prompt Testing & Evaluation Framework

A comprehensive testing framework for validating, evaluating, and benchmarking AI prompts across all modalities (text, multi-modal, agents).

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Test Types](#test-types)
- [Validators](#validators)
- [Writing Tests](#writing-tests)
- [Running Tests](#running-tests)
- [CI/CD Integration](#cicd-integration)
- [Metrics & Reporting](#metrics--reporting)
- [Best Practices](#best-practices)

## ✨ Features

### Core Capabilities
- **Universal Test Runner**: Supports all prompt types (text, multi-modal, agents)
- **Multiple Test Types**: Unit, integration, regression, performance, safety, quality
- **Comprehensive Validators**: Code, JSON, safety, semantic, performance
- **Parallel Execution**: Run tests concurrently with configurable workers
- **Retry Logic**: Automatic retry with exponential backoff
- **Result Caching**: Cache results to speed up repeated tests
- **Detailed Reporting**: JSON, HTML, and console output formats

### Safety & Compliance
- **PII Detection**: Automatic detection of personal information
- **Security Scanning**: Identify API keys, passwords, secrets
- **Harmful Content Detection**: Block dangerous commands and content
- **Bias Detection**: Check for potential bias in outputs
- **Content Moderation**: Validate against content policies

### Performance & Quality
- **Token Usage Tracking**: Monitor token consumption and costs
- **Latency Metrics**: Track P50, P95, P99 response times
- **Quality Scoring**: Automated quality assessment
- **Regression Detection**: Compare against baseline performance
- **Benchmark Suites**: Standard benchmarks for comparison

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r testing/requirements.txt

# Run example test suite
python testing/run_tests.py testing/test_suites/example_test_suite.yaml
```

### Basic Usage

```python
from testing.framework.core import PromptTestRunner, TestCase, TestType

# Create test runner
runner = PromptTestRunner()

# Define a test case
test_case = TestCase(
    id="test_001",
    name="Test Code Generation",
    description="Test Python code generation",
    test_type=TestType.UNIT,
    prompt_id="code-generator",
    inputs={"task": "Create fibonacci function"},
    validators=["code_python", "safety"],
    timeout=30
)

# Run test
result = await runner.run_single_test(test_case)
print(f"Test passed: {result.is_success}")
```

## 🏗️ Architecture

```
testing/
├── framework/
│   ├── core/
│   │   ├── test_runner.py      # Main test execution engine
│   │   ├── evaluators.py       # Output evaluation logic
│   │   └── metrics.py          # Metrics collection
│   ├── validators/
│   │   ├── base_validator.py   # Base validator class
│   │   ├── code_validator.py   # Code syntax/execution validation
│   │   ├── safety_validator.py # Safety and compliance checks
│   │   ├── json_validator.py   # JSON structure validation
│   │   └── semantic_validator.py # Semantic correctness
│   └── reporters/
│       ├── console_reporter.py # Console output formatting
│       ├── html_reporter.py    # HTML report generation
│       └── json_reporter.py    # JSON result export
├── test_suites/
│   ├── unit/                   # Unit test suites
│   ├── integration/            # Integration test suites
│   ├── regression/             # Regression test suites
│   └── benchmarks/             # Performance benchmarks
├── results/                    # Test execution results
└── run_tests.py               # Main test execution script
```

## 🧪 Test Types

### Unit Tests
Test individual prompts in isolation:
```yaml
test_type: "unit"
prompt_id: "code-generator"
inputs:
  language: "python"
  task: "fibonacci function"
validators:
  - "code_python"
  - "safety"
```

### Integration Tests
Test prompt chains and workflows:
```yaml
test_type: "integration"
prompts:
  - "requirement-analyzer"
  - "code-generator"
  - "test-generator"
workflow: "sequential"
```

### Safety Tests
Validate output safety and compliance:
```yaml
test_type: "safety"
validators:
  - "safety"
  - "content_moderation"
checks:
  - no_pii
  - no_secrets
  - no_harmful_commands
```

### Performance Tests
Measure latency and resource usage:
```yaml
test_type: "performance"
metrics:
  - latency_p50
  - latency_p95
  - token_usage
  - cost_per_request
benchmarks:
  p95_target: 5.0  # seconds
  max_tokens: 4000
```

## 🔍 Validators

### Code Validator
Validates code syntax and execution:

```python
from testing.framework.validators import CodeValidator

validator = CodeValidator(language="python")
is_valid = await validator.validate(code_output)
```

**Supported Languages:**
- Python (AST validation)
- JavaScript/TypeScript
- Java, Go, Rust
- SQL
- More coming soon...

### Safety Validator
Checks for security and compliance issues:

```python
from testing.framework.validators import SafetyValidator

validator = SafetyValidator()
is_safe = await validator.validate(output)
report = validator.get_safety_report()
```

**Safety Checks:**
- PII Detection (SSN, credit cards, emails)
- Secret Detection (API keys, passwords)
- Harmful Commands (rm -rf, DROP TABLE)
- SQL Injection Patterns
- XSS/Script Injection

### Semantic Validator
Validates content and meaning:

```python
validator = SemanticValidator(
    criteria=["contains_solution", "explains_reasoning"]
)
is_valid = await validator.validate(output)
```

## 📝 Writing Tests

### YAML Test Suite Format

```yaml
name: "My Test Suite"
description: "Test suite description"
version: "1.0.0"

config:
  parallel: true
  max_workers: 5
  timeout_default: 30

test_cases:
  - id: "test_001"
    name: "Test Name"
    description: "Test description"
    test_type: "unit"
    prompt_id: "prompt-to-test"
    inputs:
      param1: "value1"
      param2: "value2"
    expected_outputs:
      contains:
        - "expected text"
      patterns:
        - "regex.*pattern"
    validators:
      - "safety"
      - "semantic"
    metrics:
      - "quality_score"
      - "response_time"
    timeout: 30
    retries: 3
    tags:
      - "core"
      - "safety"
```

### Python Test Format

```python
import pytest
from testing.framework.core import PromptTestRunner, TestCase

class TestPrompts:
    @pytest.fixture
    def runner(self):
        return PromptTestRunner()
    
    @pytest.mark.asyncio
    async def test_code_generation(self, runner):
        test_case = TestCase(
            id="test_code_gen",
            name="Code Generation Test",
            test_type=TestType.UNIT,
            prompt_id="code-generator",
            inputs={"language": "python", "task": "sort array"},
            validators=["code_python"],
            timeout=30
        )
        
        result = await runner.run_single_test(test_case)
        assert result.is_success
        assert "def" in result.actual_output
```

## 🏃 Running Tests

### Command Line Interface

```bash
# Run single test suite
python testing/run_tests.py test_suites/my_suite.yaml

# Run multiple suites
python testing/run_tests.py test_suites/*.yaml

# Filter by tags
python testing/run_tests.py --filter-tags safety security

# Filter by test type
python testing/run_tests.py --filter-type unit

# Run in sequential mode
python testing/run_tests.py --no-parallel

# Dry run (don't execute)
python testing/run_tests.py --dry-run

# Verbose output
python testing/run_tests.py --verbose

# Custom output file
python testing/run_tests.py --output results.json
```

### Python API

```python
import asyncio
from testing.framework.core import PromptTestRunner

async def run_tests():
    runner = PromptTestRunner()
    runner.load_test_suite("test_suites/my_suite.yaml")
    
    results = await runner.run_test_suite(
        suite_name="my_suite",
        parallel=True,
        max_workers=5,
        filter_tags=["safety"]
    )
    
    print(f"Pass rate: {results['pass_rate']}%")
    print(f"Total cost: ${results['total_cost']}")

asyncio.run(run_tests())
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: Prompt Testing

on:
  push:
    branches: [main]
  pull_request:
    paths:
      - 'prompts/**'
      - 'testing/**'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r testing/requirements.txt
      
      - name: Run tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python testing/run_tests.py \
            testing/test_suites/*.yaml \
            --output test-results.json
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-results.json
      
      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('test-results.json'));
            const passRate = results.summary.pass_rate;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Test Results\n\nPass Rate: ${passRate}%`
            });
```

## 📊 Metrics & Reporting

### Available Metrics

- **Performance Metrics**
  - `execution_time`: Total test execution time
  - `latency_p50`, `latency_p95`, `latency_p99`: Response time percentiles
  - `throughput`: Requests per second

- **Resource Metrics**
  - `total_tokens`: Total tokens used
  - `prompt_tokens`: Input token count
  - `completion_tokens`: Output token count
  - `estimated_cost`: Cost estimation based on token usage

- **Quality Metrics**
  - `code_quality`: Code quality score (0-1)
  - `safety_score`: Safety validation score (0-1)
  - `relevance_score`: Output relevance to input (0-1)
  - `completeness`: Task completion score (0-1)

### Report Formats

#### Console Output
```
📊 Suite: example_suite
   Total Tests: 10
   ✅ Passed: 8
   ❌ Failed: 1
   💥 Errors: 1
   Pass Rate: 80.00%
   Execution Time: 45.23s
   Total Cost: $0.1234
```

#### JSON Report
```json
{
  "timestamp": "2025-11-25T10:00:00Z",
  "summary": {
    "total_tests": 10,
    "passed": 8,
    "failed": 1,
    "errors": 1,
    "pass_rate": "80.00%"
  },
  "metrics": {
    "total_tokens": 15000,
    "avg_execution_time": "4.52s"
  },
  "details": [...]
}
```

## 📚 Best Practices

### 1. Test Organization
- Group related tests in suites
- Use descriptive test IDs and names
- Tag tests for easy filtering
- Set appropriate timeouts

### 2. Validation Strategy
- Use multiple validators for comprehensive checking
- Always include safety validation
- Validate both structure and content
- Check for edge cases

### 3. Performance Optimization
- Use parallel execution for independent tests
- Cache results for expensive operations
- Set reasonable retry limits
- Monitor token usage and costs

### 4. Safety First
- Always validate for PII and secrets
- Check for harmful commands
- Implement content moderation
- Log all safety violations

### 5. Continuous Improvement
- Track metrics over time
- Set performance baselines
- Run regression tests regularly
- Update test cases as prompts evolve

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Adding new validators
- Creating test suites
- Improving the framework
- Reporting issues

## 📄 License

This testing framework is part of the Prompts Library and is licensed under the MIT License.

---

**Built with ❤️ for reliable AI prompt development**