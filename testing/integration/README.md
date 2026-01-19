# 🔗 Integration Tests

End-to-end integration tests for prompt execution, evaluation workflows, and multi-component systems.

## 📋 Overview

This directory contains integration tests that validate complete workflows and interactions between multiple components. These tests verify that prompts, agents, and tools work correctly together in realistic scenarios.

## 📁 Test Files

```
integration/
├── README.md                              # This file
├── __init__.py                            # Package initialization
├── test_prompt_integration.py             # Prompt execution integration tests
├── test_prompt_toolkit.py                 # Toolkit integration tests
├── test_evaluation_agent_e2e.py           # End-to-end evaluation agent tests
└── test_evaluation_agent_integration.py   # Evaluation agent integration tests
```

## 🎯 Purpose

Integration tests verify:

- **Full execution pipeline** - Prompt loading → LLM execution → result validation
- **Multi-component workflows** - Agent orchestration, tool chaining
- **Cross-platform compatibility** - Azure, GitHub Models, Ollama, local ONNX
- **Real LLM integration** - Actual model responses (vs. mocked)
- **Performance under load** - Concurrent execution, rate limiting
- **Error handling** - Graceful degradation, retry logic

## 🚀 Quick Start

### Run All Integration Tests

```bash
# Run all integration tests
pytest testing/integration/ -v

# Run with coverage
pytest testing/integration/ --cov=testing --cov-report=html

# Run specific test file
pytest testing/integration/test_prompt_integration.py -v

# Run specific test class
pytest testing/integration/test_evaluation_agent_e2e.py::TestEvaluationAgentE2E -v
```

### Run Slow Tests (Local ONNX Models)

Integration tests that require local ONNX models are marked with `@pytest.mark.slow` and skipped by default.

```bash
# Skip slow tests (default)
pytest testing/integration/ -v

# Include slow tests
pytest testing/integration/ -m slow -v

# Run only slow tests
pytest testing/integration/ -m "slow" -v

# Run all tests including slow
pytest testing/integration/ -v -m ""
```

### Run Specific Test Types

```bash
# Run only E2E tests
pytest testing/integration/ -k "e2e" -v

# Run only evaluation tests
pytest testing/integration/ -k "evaluation" -v

# Run toolkit tests only
pytest testing/integration/ -k "toolkit" -v
```

## 📄 Test Files

### 1. test_prompt_integration.py

**Purpose:** Integration tests for prompt execution pipeline with local models.

**Coverage:**
- Prompt loading and parsing
- Variable substitution and formatting
- Local ONNX model execution
- Response validation
- Error handling

**Requirements:**
- Local ONNX model (`phi4mini` or `mistral` in AI Gallery cache)
- `onnxruntime-genai` library installed

**Key Tests:**

| Test | Description | Speed |
|------|-------------|-------|
| `test_prompt_execution_basic` | Execute simple prompt with local model | Slow |
| `test_prompt_variable_substitution` | Verify variable replacement | Slow |
| `test_prompt_error_handling` | Test error scenarios | Slow |
| `test_multimodal_prompt` | Test image + text prompts | Slow |

**Usage:**

```bash
# Skip by default (requires local model)
pytest testing/integration/test_prompt_integration.py -v

# Run with local model available
pytest testing/integration/test_prompt_integration.py -m slow -v
```

### 2. test_prompt_toolkit.py

**Purpose:** Integration tests for the unified prompt toolkit.

**Coverage:**
- Prompt discovery and loading
- Format detection (Markdown, YAML, JSON)
- Batch processing
- Provider abstraction
- Caching mechanisms

**Key Tests:**

| Test | Description | Speed |
|------|-------------|-------|
| `test_toolkit_initialization` | Initialize toolkit components | Fast |
| `test_discover_prompts` | Find prompts in directory | Fast |
| `test_load_markdown_prompt` | Load .md prompt file | Fast |
| `test_load_yaml_prompt` | Load .prompt.yml file | Fast |
| `test_batch_execution` | Execute multiple prompts | Slow |
| `test_provider_switching` | Switch between LLM providers | Slow |

**Usage:**

```bash
# Run fast tests only
pytest testing/integration/test_prompt_toolkit.py -m "not slow" -v

# Run all toolkit tests
pytest testing/integration/test_prompt_toolkit.py -v
```

### 3. test_evaluation_agent_integration.py

**Purpose:** Integration tests for the evaluation agent's workflow coordination.

**Coverage:**
- Agent initialization and configuration
- Task queue management
- Checkpoint save/load
- Batch prompt evaluation
- Result aggregation
- Error recovery

**Key Tests:**

| Test | Description |
|------|-------------|
| `test_agent_initialization` | Agent starts with valid config |
| `test_checkpoint_save_load` | State persistence works |
| `test_evaluate_single_category` | Evaluate one category |
| `test_evaluate_multiple_categories` | Batch category evaluation |
| `test_error_recovery` | Recovery from failures |
| `test_result_aggregation` | Combine results correctly |

**Usage:**

```bash
pytest testing/integration/test_evaluation_agent_integration.py -v
```

### 4. test_evaluation_agent_e2e.py

**Purpose:** End-to-end tests for complete evaluation agent workflows.

**Coverage:**
- Full evaluation pipeline
- Multi-category processing
- Report generation
- CI/CD integration
- Performance under load

**Key Tests:**

| Test | Description | Duration |
|------|-------------|----------|
| `test_full_library_evaluation` | Evaluate entire library | Long |
| `test_category_evaluation` | Evaluate single category | Medium |
| `test_incremental_evaluation` | Resume from checkpoint | Medium |
| `test_parallel_evaluation` | Concurrent processing | Long |
| `test_report_generation` | Generate HTML/JSON reports | Fast |

**Usage:**

```bash
# Run E2E tests (may take several minutes)
pytest testing/integration/test_evaluation_agent_e2e.py -v

# Run specific E2E test
pytest testing/integration/test_evaluation_agent_e2e.py::test_category_evaluation -v
```

## 🔧 Test Configuration

### Environment Variables

```bash
# Azure Foundry (for Azure provider tests)
export AZURE_FOUNDRY_API_KEY="your-key"
export AZURE_FOUNDRY_ENDPOINT_1="https://..."
export AZURE_FOUNDRY_ENDPOINT_2="https://..."

# GitHub Models (for GitHub provider tests)
export GH_TOKEN="your-github-token"

# Test configuration
export TEST_TIMEOUT=60          # Default test timeout
export TEST_SLOW_THRESHOLD=5    # Mark tests > 5s as slow
```

### Pytest Configuration

```ini
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    e2e: marks tests as end-to-end
    integration: marks integration tests
    requires_model: requires local ONNX model
    requires_network: requires network access

# Default to skip slow tests
addopts = -m "not slow"

# Timeout for all tests
timeout = 60
```

## 📊 Test Metrics

### Test Execution Time

| Test Suite | Count | Avg Time | Total Time |
|------------|-------|----------|------------|
| Prompt Integration | 8 | 2.5s | 20s |
| Prompt Toolkit | 12 | 0.8s | 10s |
| Evaluation Agent Integration | 15 | 1.2s | 18s |
| Evaluation Agent E2E | 6 | 45s | 270s |
| **Total** | **41** | **7.8s** | **318s** |

### Coverage Targets

| Component | Target Coverage | Current |
|-----------|----------------|---------|
| Prompt execution | 90% | 85% |
| Agent workflows | 85% | 80% |
| Error handling | 95% | 90% |
| Provider integration | 80% | 75% |

## 🎯 Best Practices

### 1. Test Isolation

Each test should be independent and not rely on other tests:

```python
@pytest.fixture(autouse=True)
def cleanup():
    """Clean up between tests."""
    yield
    # Clean up test artifacts
    Path("test_results").rmdir(missing_ok=True)
```

### 2. Use Fixtures

Share common setup across tests:

```python
@pytest.fixture
def test_prompt():
    """Sample prompt for testing."""
    return {
        "id": "test_prompt",
        "template": "Hello, {name}!",
        "model": "gpt-4o-mini"
    }

@pytest.fixture
def evaluation_agent(tmp_path):
    """Configured evaluation agent."""
    config = AgentConfig(
        checkpoint_dir=tmp_path / "checkpoints"
    )
    return EvaluationAgent(config)

def test_with_fixtures(test_prompt, evaluation_agent):
    result = evaluation_agent.evaluate(test_prompt)
    assert result is not None
```

### 3. Mock External Services

Use mocks for flaky external dependencies:

```python
from unittest.mock import Mock, patch

@patch('tools.evaluation_agent.call_llm')
def test_evaluation_with_mock(mock_llm):
    mock_llm.return_value = {"score": 8.5, "reasoning": "Good"}
    
    agent = EvaluationAgent()
    result = agent.evaluate_prompt("test.md")
    
    assert result['score'] == 8.5
    mock_llm.assert_called_once()
```

### 4. Parametrize Tests

Test multiple scenarios efficiently:

```python
@pytest.mark.parametrize("provider,model", [
    ("azure", "phi4mini"),
    ("gh", "gpt-4o-mini"),
    ("ollama", "llama3"),
])
def test_multiple_providers(provider, model):
    runner = PromptTestRunner()
    result = runner._execute_with_provider(provider, model)
    assert result is not None
```

### 5. Mark Expensive Tests

Use markers for test categorization:

```python
@pytest.mark.slow
@pytest.mark.requires_model
def test_local_model_execution():
    # This test loads ONNX model (slow)
    pass

@pytest.mark.e2e
@pytest.mark.requires_network
def test_full_pipeline():
    # End-to-end test requiring network
    pass
```

## 🐛 Debugging Integration Tests

### Enable Verbose Logging

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Run test with debug output
pytest testing/integration/test_prompt_integration.py::test_name -v -s
```

### Inspect Test Failures

```bash
# Show local variables on failure
pytest testing/integration/ --showlocals

# Drop into debugger on failure
pytest testing/integration/ --pdb

# Run last failed tests only
pytest testing/integration/ --lf
```

### Check Test Prerequisites

```python
# Check if local model available
pytest testing/integration/ -v --collect-only

# This will show which tests will be skipped
```

## 📈 CI/CD Integration

### GitHub Actions Example

```yaml
name: Integration Tests

on:
  pull_request:
    paths:
      - 'testing/integration/**'
      - 'tools/**'
      - 'prompts/**'

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: |
          pip install -r testing/requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Setup GitHub Models
        run: gh extension install github/gh-models
        env:
          GH_TOKEN: ${{ github.token }}
      
      - name: Run integration tests (fast only)
        run: |
          pytest testing/integration/ \
            -v \
            -m "not slow" \
            --cov=testing \
            --cov-report=xml
        env:
          GH_TOKEN: ${{ github.token }}
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## 🔗 Dependencies

```bash
# Core dependencies
pip install pytest pytest-asyncio pytest-cov

# For local model tests
pip install onnxruntime-genai

# For GitHub Models
gh extension install github/gh-models

# Optional: for specific validators
pip install pyyaml jsonschema
```

## 📖 See Also

- [../unit/README.md](../unit/README.md) - Unit tests
- [../framework/README.md](../framework/README.md) - Testing framework
- [../tool_tests/README.md](../tool_tests/README.md) - Tool-specific tests
- [../../docs/ARCHITECTURE_PLAN.md](../../docs/ARCHITECTURE_PLAN.md) - Overall architecture

---

**Built with ❤️ for comprehensive integration testing**
