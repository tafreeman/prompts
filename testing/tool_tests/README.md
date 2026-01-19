# 🔧 Tool-Specific Tests

Unit tests for individual tools and utilities in the prompts library.

## 📋 Overview

This directory contains focused unit tests for specific tools including the evaluation agent, prompt generator, CLI utilities, and LLM connection handlers. These tests validate individual components in isolation.

## 📁 Test Files

```
tool_tests/
├── README.md                           # This file
├── __init__.py                         # Package initialization
├── test_evaluation_agent.py            # Evaluation agent unit tests
├── test_generator.py                   # Prompt generator tests
├── test_cli.py                         # CLI utility tests
├── test_llm_connection.py              # LLM provider connection tests
└── test_tools_ecosystem_evaluator.py   # Ecosystem evaluator tests
```

## 🎯 Purpose

Tool tests verify:

- **Component functionality** - Individual tool behavior
- **Configuration handling** - Config parsing and validation
- **Error conditions** - Edge cases and error handling
- **API contracts** - Input/output interfaces
- **State management** - Checkpoints, cache, persistence
- **CLI argument parsing** - Command-line interface validation

## 🚀 Quick Start

### Run All Tool Tests

```bash
# Run all tool tests
pytest testing/tool_tests/ -v

# Run with coverage report
pytest testing/tool_tests/ --cov=tools --cov-report=html

# Run specific test file
pytest testing/tool_tests/test_evaluation_agent.py -v

# Run specific test class
pytest testing/tool_tests/test_evaluation_agent.py::TestAgentConfiguration -v

# Run specific test
pytest testing/tool_tests/test_evaluation_agent.py::TestAgentConfiguration::test_agent_config_paths_exist -v
```

### Run Tests by Category

```bash
# Run only configuration tests
pytest testing/tool_tests/ -k "config" -v

# Run only CLI tests
pytest testing/tool_tests/ -k "cli" -v

# Run only validation tests
pytest testing/tool_tests/ -k "validation" -v
```

## 📄 Test Files

### 1. test_evaluation_agent.py

**Purpose:** Unit tests for the evaluation agent tool.

**Coverage:**
- Agent configuration and initialization
- Checkpoint save/load functionality
- Task result tracking
- State management
- Dry-run mode
- Category result aggregation
- Prerequisite checking

**Test Classes:**

```python
class TestAgentConfiguration:
    """Test agent configuration and setup."""
    
class TestCheckpointManagement:
    """Test checkpoint save/load functionality."""
    
class TestTaskResultTracking:
    """Test task result accumulation."""
    
class TestAgentState:
    """Test agent state transitions."""
    
class TestCategoryResults:
    """Test category result aggregation."""
```

**Key Tests:**

| Test | Description |
|------|-------------|
| `test_agent_config_paths_exist` | Verify config paths are set |
| `test_save_checkpoint` | Checkpoint saving works |
| `test_load_checkpoint` | Checkpoint loading works |
| `test_checkpoint_persistence` | Data persists across save/load |
| `test_task_result_creation` | TaskResult objects created correctly |
| `test_task_status_enum` | Status enum values valid |
| `test_category_result_aggregation` | Results aggregated by category |
| `test_dry_run_mode` | Dry run doesn't execute |
| `test_prerequisites_check` | Check required tools |

**Usage:**

```bash
# Run all evaluation agent tests
pytest testing/tool_tests/test_evaluation_agent.py -v

# Test checkpoint functionality only
pytest testing/tool_tests/test_evaluation_agent.py::TestCheckpointManagement -v
```

**Example:**

```python
def test_checkpoint_save_load():
    """Test checkpoint can be saved and loaded."""
    with tempfile.TemporaryDirectory() as tmpdir:
        checkpoint_path = Path(tmpdir) / "checkpoint.json"
        
        # Create state
        state = AgentState(
            current_category="developers",
            total_prompts=10,
            processed_prompts=5
        )
        
        # Save checkpoint
        save_checkpoint(state, checkpoint_path)
        assert checkpoint_path.exists()
        
        # Load checkpoint
        loaded_state = load_checkpoint(checkpoint_path)
        assert loaded_state.current_category == "developers"
        assert loaded_state.processed_prompts == 5
```

### 2. test_generator.py

**Purpose:** Unit tests for prompt generation utilities.

**Coverage:**
- Template parsing and rendering
- Variable substitution
- Format detection and conversion
- Frontmatter generation
- Batch generation
- Validation integration

**Key Tests:**

| Test | Description |
|------|-------------|
| `test_parse_template` | Parse Jinja2/mustache templates |
| `test_substitute_variables` | Variable replacement |
| `test_detect_format` | Detect .md, .yml, .json formats |
| `test_generate_frontmatter` | YAML frontmatter generation |
| `test_generate_from_template` | Full prompt generation |
| `test_batch_generation` | Generate multiple prompts |
| `test_validation_after_generation` | Generated prompts are valid |

**Usage:**

```bash
pytest testing/tool_tests/test_generator.py -v
```

### 3. test_cli.py

**Purpose:** Unit tests for command-line interface utilities.

**Coverage:**
- Argument parsing
- Command dispatch
- Option validation
- Help text generation
- Error handling
- Exit codes

**Key Tests:**

| Test | Description |
|------|-------------|
| `test_parse_args_basic` | Basic argument parsing |
| `test_parse_args_with_options` | Options and flags |
| `test_invalid_arguments` | Error handling for bad args |
| `test_help_text` | Help message generation |
| `test_subcommand_dispatch` | Subcommand routing |
| `test_exit_codes` | Correct exit codes |

**Usage:**

```bash
pytest testing/tool_tests/test_cli.py -v
```

**Example:**

```python
def test_parse_args_basic():
    """Test basic argument parsing."""
    from tools.cli import parse_args
    
    args = parse_args(['evaluate', 'prompts/', '--tier', '2'])
    
    assert args.command == 'evaluate'
    assert args.path == 'prompts/'
    assert args.tier == 2
```

### 4. test_llm_connection.py

**Purpose:** Unit tests for LLM provider connection handlers.

**Coverage:**
- Provider detection
- Authentication handling
- Request formatting
- Response parsing
- Rate limiting
- Error recovery
- Timeout handling

**Supported Providers:**
- Azure Foundry
- GitHub Models
- Ollama
- Local ONNX

**Key Tests:**

| Test | Description |
|------|-------------|
| `test_detect_provider` | Auto-detect available provider |
| `test_azure_connection` | Azure Foundry authentication |
| `test_github_models_connection` | GitHub Models setup |
| `test_ollama_connection` | Ollama server connection |
| `test_local_model_connection` | Local ONNX model loading |
| `test_format_request` | Request payload formatting |
| `test_parse_response` | Response parsing |
| `test_handle_rate_limit` | Rate limit handling |
| `test_handle_timeout` | Timeout handling |
| `test_handle_errors` | Error recovery |

**Usage:**

```bash
pytest testing/tool_tests/test_llm_connection.py -v

# Test specific provider
pytest testing/tool_tests/test_llm_connection.py -k "azure" -v
```

**Example:**

```python
def test_detect_provider():
    """Test provider auto-detection."""
    from tools.llm_connection import detect_provider
    
    # With Azure env vars
    with mock.patch.dict(os.environ, {
        'AZURE_FOUNDRY_API_KEY': 'test-key',
        'AZURE_FOUNDRY_ENDPOINT_1': 'https://test'
    }):
        provider = detect_provider()
        assert provider == 'azure'
    
    # With gh CLI available
    with mock.patch('shutil.which', return_value='/usr/bin/gh'):
        provider = detect_provider()
        assert provider == 'gh'
```

### 5. test_tools_ecosystem_evaluator.py

**Purpose:** Unit tests for the tools ecosystem evaluator.

**Coverage:**
- Tool discovery
- Compatibility checking
- Version validation
- Integration testing
- Report generation

**Key Tests:**

| Test | Description |
|------|-------------|
| `test_discover_tools` | Find all available tools |
| `test_check_tool_availability` | Verify tool is installed |
| `test_check_tool_version` | Validate tool versions |
| `test_check_compatibility` | Tool compatibility matrix |
| `test_generate_report` | Evaluation report generation |

**Usage:**

```bash
pytest testing/tool_tests/test_tools_ecosystem_evaluator.py -v
```

## 🎯 Testing Best Practices

### 1. Test Isolation

Each test should be completely independent:

```python
import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def temp_dir():
    """Provide a temporary directory for each test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

def test_with_temp_dir(temp_dir):
    """Test using temporary directory."""
    test_file = temp_dir / "test.txt"
    test_file.write_text("test data")
    assert test_file.exists()
    # Cleanup happens automatically
```

### 2. Mock External Dependencies

```python
from unittest.mock import Mock, patch, MagicMock

@patch('tools.evaluation_agent.call_llm')
def test_with_mocked_llm(mock_llm):
    """Test with mocked LLM calls."""
    mock_llm.return_value = {
        "score": 8.5,
        "reasoning": "Good prompt"
    }
    
    agent = EvaluationAgent()
    result = agent.evaluate("test.md")
    
    assert result['score'] == 8.5
    mock_llm.assert_called_once()
```

### 3. Test Edge Cases

```python
import pytest

def test_empty_input():
    """Test handling of empty input."""
    from tools.generator import generate_prompt
    
    with pytest.raises(ValueError, match="Input cannot be empty"):
        generate_prompt("")

def test_invalid_format():
    """Test handling of invalid format."""
    from tools.generator import parse_prompt
    
    result = parse_prompt("invalid data")
    assert result is None

def test_boundary_values():
    """Test boundary conditions."""
    from tools.validator import validate_score
    
    assert validate_score(0) is True   # Min value
    assert validate_score(10) is True  # Max value
    assert validate_score(-1) is False # Below min
    assert validate_score(11) is False # Above max
```

### 4. Parametrize Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("WORLD", "WORLD"),
    ("MiXeD", "MIXED"),
    ("", ""),
])
def test_uppercase_conversion(input, expected):
    """Test string uppercase conversion."""
    from tools.utils import to_uppercase
    assert to_uppercase(input) == expected
```

### 5. Test Error Messages

```python
def test_error_message_clarity():
    """Test that error messages are helpful."""
    from tools.validator import validate_config
    
    with pytest.raises(ValueError) as exc_info:
        validate_config({"invalid": "config"})
    
    error_message = str(exc_info.value)
    assert "required field" in error_message.lower()
    assert "missing" in error_message.lower()
```

## 📊 Test Metrics

### Current Coverage

| Tool | Tests | Coverage | Status |
|------|-------|----------|--------|
| evaluation_agent | 35 | 92% | ✅ |
| generator | 18 | 85% | ✅ |
| cli | 22 | 88% | ✅ |
| llm_connection | 28 | 90% | ✅ |
| ecosystem_evaluator | 12 | 78% | 🟡 |
| **Total** | **115** | **87%** | ✅ |

### Test Execution Time

| Test File | Count | Avg Time | Total |
|-----------|-------|----------|-------|
| test_evaluation_agent.py | 35 | 0.05s | 1.75s |
| test_generator.py | 18 | 0.08s | 1.44s |
| test_cli.py | 22 | 0.03s | 0.66s |
| test_llm_connection.py | 28 | 0.12s | 3.36s |
| test_tools_ecosystem_evaluator.py | 12 | 0.15s | 1.80s |
| **Total** | **115** | **0.08s** | **9.01s** |

## 🔧 Configuration

### pytest.ini

```ini
[pytest]
testpaths = testing/tool_tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    requires_network: requires network access
    requires_auth: requires authentication

# Coverage
addopts = --strict-markers --tb=short

# Timeout
timeout = 10
```

### Test Environment

```bash
# Set test mode
export TEST_MODE=true

# Use test config
export CONFIG_PATH=testing/test_config.yaml

# Mock external services
export MOCK_LLM=true
export MOCK_GITHUB_API=true
```

## 🐛 Debugging

### Run with Verbose Output

```bash
# Show print statements
pytest testing/tool_tests/ -v -s

# Show local variables on failure
pytest testing/tool_tests/ --showlocals

# Drop into debugger on failure
pytest testing/tool_tests/ --pdb
```

### Run Specific Tests

```bash
# Run single test
pytest testing/tool_tests/test_evaluation_agent.py::test_checkpoint_save -v

# Run tests matching pattern
pytest testing/tool_tests/ -k "checkpoint" -v

# Run failed tests only
pytest testing/tool_tests/ --lf
```

### Debug Test Failures

```python
def test_with_debug():
    """Test with debug output."""
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    result = some_function()
    
    # Add breakpoint for debugging
    import pdb; pdb.set_trace()
    
    assert result is not None
```

## 📈 CI/CD Integration

### GitHub Actions Example

```yaml
name: Tool Tests

on:
  pull_request:
    paths:
      - 'tools/**'
      - 'testing/tool_tests/**'

jobs:
  test-tools:
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
          pip install pytest pytest-cov
      
      - name: Run tool tests
        run: |
          pytest testing/tool_tests/ \
            -v \
            --cov=tools \
            --cov-report=xml \
            --cov-report=term
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## 🔗 Dependencies

```bash
# Core testing dependencies
pip install pytest pytest-cov pytest-mock

# For async tests
pip install pytest-asyncio

# For parametrize helpers
pip install pytest-parametrize-cases

# Optional: for better diffs
pip install pytest-clarity
```

## 📖 See Also

- [../unit/README.md](../unit/README.md) - Unit tests for other components
- [../integration/README.md](../integration/README.md) - Integration tests
- [../framework/README.md](../framework/README.md) - Testing framework
- [../../tools/README.md](../../tools/README.md) - Tools documentation

---

**Built with ❤️ for reliable tool testing**
