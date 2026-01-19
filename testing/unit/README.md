# 🧩 Unit Tests

Fast, focused unit tests for core functionality and utility functions.

## 📋 Overview

This directory contains unit tests that validate individual functions, classes, and modules in isolation. These tests are designed to be fast, deterministic, and independent.

## 📁 Test Files

```
unit/
├── README.md                                    # This file
├── __init__.py                                  # Package initialization
├── test_prompteval_score_normalization.py       # Score normalization tests
└── test_local_model_geval_parsing.py           # G-Eval parsing tests
```

## 🎯 Purpose

Unit tests verify:

- **Function correctness** - Individual function behavior
- **Edge cases** - Boundary conditions and corner cases
- **Error handling** - Exception handling and validation
- **Data transformations** - Parsing, formatting, conversion
- **Algorithm correctness** - Mathematical and logical operations
- **Utility functions** - Helper and support functions

## 🚀 Quick Start

### Run All Unit Tests

```bash
# Run all unit tests
pytest testing/unit/ -v

# Run with coverage
pytest testing/unit/ --cov=tools.prompteval --cov-report=html

# Run specific test file
pytest testing/unit/test_prompteval_score_normalization.py -v

# Run specific test function
pytest testing/unit/test_prompteval_score_normalization.py::test_normalize_score_to_pct_never_negative -v
```

### Run Fast Tests Only

Unit tests are typically fast, but you can filter further:

```bash
# Run tests under 1 second
pytest testing/unit/ --durations=0 -v

# Skip slow tests if any are marked
pytest testing/unit/ -m "not slow" -v
```

## 📄 Test Files

### 1. test_prompteval_score_normalization.py

**Purpose:** Test score normalization and conversion functions in PromptEval.

**Coverage:**

- Score normalization (0-10 scale to 0-100%)
- Boundary value handling
- Negative score handling
- Percentage conversion
- Rubric scale mapping

**Key Tests:**

| Test | Description | Validates |
| ------ | ------------- | ----------- |
| `test_normalize_score_to_pct_never_negative` | Negative scores converted to 0% | Error handling |
| `test_normalize_score_to_pct_rubric_bounds` | Rubric 1-10 maps to 0-100% | Boundary values |
| `test_normalize_score_to_pct_accepts_fraction_and_percent` | Handle fractions and percents | Input flexibility |

**Usage:**

```bash
# Run all normalization tests
pytest testing/unit/test_prompteval_score_normalization.py -v

# Run specific test
pytest testing/unit/test_prompteval_score_normalization.py::test_normalize_score_to_pct_rubric_bounds -v
```

**Implementation Details:**

The tests validate the `_normalize_score_to_pct()` function which converts various score formats to a consistent 0-100 percentage:

```python
def _normalize_score_to_pct(score: float) -> float:
    """
    Normalize score to percentage (0-100).

    Input ranges:

    - Rubric (1-10) → 0-100%
    - Fraction (0.0-1.0) → 0-100%
    - Percentage (0-100) → 0-100%
    - Negative → 0%
    - >100 → 100%

    """
    if score < 0:
        return 0.0
    elif score <= 1.0:  # Fraction
        return score * 100.0
    elif score <= 10.0:  # Rubric scale
        return (score - 1) / 9 * 100.0
    elif score <= 100:  # Already percentage
        return score
    else:  # Over 100
        return 100.0
```

**Test Cases:**

```python
def test_normalize_score_to_pct_never_negative():
    """Negative scores should become 0%, not negative percent."""
    assert _normalize_score_to_pct(0) == 0.0
    assert _normalize_score_to_pct(-5) == 0.0
    assert _normalize_score_to_pct(-100) == 0.0

def test_normalize_score_to_pct_rubric_bounds():
    """Rubric 1-10 maps to 0-100%."""
    assert _normalize_score_to_pct(1) == 0.0    # Min rubric
    assert _normalize_score_to_pct(5.5) == 50.0  # Mid rubric
    assert _normalize_score_to_pct(10) == 100.0  # Max rubric

def test_normalize_score_to_pct_accepts_fraction_and_percent():
    """Handle fractions (0-1) and percentages (0-100)."""
    assert _normalize_score_to_pct(0.5) == 50.0   # Fraction
    assert _normalize_score_to_pct(75) == 75.0    # Percentage
    assert _normalize_score_to_pct(150) == 100.0  # Over 100
```

### 2. test_local_model_geval_parsing.py

**Purpose:** Test G-Eval response parsing from local models.

**Coverage:**

- JSON extraction from model responses
- Score parsing from various formats
- Error handling for malformed responses
- Fallback parsing strategies
- Dimension score extraction

**Key Tests:**

| Test | Description | Validates |
| ------ | ------------- | ----------- |
| `test_parse_json_from_response` | Extract JSON from text | JSON extraction |
| `test_parse_score_from_json` | Parse score field | Score extraction |
| `test_parse_malformed_json` | Handle invalid JSON | Error recovery |
| `test_parse_embedded_json` | JSON within markdown | Robust parsing |
| `test_parse_score_variations` | Different score formats | Format flexibility |

**Usage:**

```bash
# Run all parsing tests
pytest testing/unit/test_local_model_geval_parsing.py -v
```

**Implementation Details:**

Tests validate parsing of G-Eval responses from local ONNX models which may return JSON in various formats:

```python
def parse_geval_response(response: str) -> dict:
    """
    Parse G-Eval response from local model.

    Handles:

    - Pure JSON response
    - JSON in markdown code block
    - JSON with surrounding text
    - Malformed JSON with fallback

    """
    # Try direct JSON parse
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass

    # Extract from markdown code block
    import re
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', 
                          response, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))

    # Extract first JSON object
    json_match = re.search(r'\{[^{}]*"score"[^{}]*\}', 
                          response, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(0))

    # Fallback: parse scores from text
    return parse_scores_from_text(response)
```

## 🎯 Writing Good Unit Tests

### 1. Test One Thing

Each test should focus on a single behavior:

```python
# Good: Tests one specific case
def test_normalize_negative_score():
    """Negative scores should be normalized to 0."""
    assert normalize_score(-5) == 0

# Bad: Tests multiple unrelated things
def test_normalization():
    """Test score normalization."""
    assert normalize_score(-5) == 0
    assert normalize_score(10) == 100
    assert format_score(5) == "5.0"  # Different function!
```

### 2. Use Descriptive Names

Test names should clearly describe what they test:

```python
# Good: Clear what's being tested
def test_normalize_score_handles_negative_values():
    pass

def test_normalize_score_converts_rubric_to_percentage():
    pass

# Bad: Vague names
def test_normalize():
    pass

def test_scores():
    pass
```

### 3. Follow AAA Pattern

**Arrange, Act, Assert:**

```python
def test_parse_json_from_markdown():
    # Arrange: Set up test data
    response = """
    Here's the evaluation:
    ```json

    {"score": 8.5, "reasoning": "Good"}

    ```
    """

    # Act: Execute the function
    result = parse_json(response)

    # Assert: Verify the result
    assert result["score"] == 8.5
    assert "reasoning" in result
```

### 4. Test Edge Cases

Don't just test the happy path:

```python
def test_normalize_score_edge_cases():
    """Test boundary conditions and edge cases."""
    # Minimum value
    assert normalize_score(0) == 0

    # Maximum value
    assert normalize_score(10) == 100

    # Below minimum
    assert normalize_score(-1) == 0

    # Above maximum
    assert normalize_score(11) == 100

    # Null/None
    with pytest.raises(TypeError):
        normalize_score(None)

    # Non-numeric
    with pytest.raises(ValueError):
        normalize_score("invalid")
```

### 5. Use Parametrization

Test multiple inputs efficiently:

```python
@pytest.mark.parametrize("input_score,expected", [
    (0, 0.0),        # Zero
    (1, 0.0),        # Min rubric
    (5.5, 50.0),     # Mid rubric
    (10, 100.0),     # Max rubric
    (-5, 0.0),       # Negative
    (0.5, 50.0),     # Fraction
    (75, 75.0),      # Percentage
    (150, 100.0),    # Over 100
])
def test_normalize_score_cases(input_score, expected):
    """Test score normalization with various inputs."""
    assert normalize_score(input_score) == expected
```

## 📊 Test Metrics

### Current Status

| File | Tests | Coverage | Speed |
| ------ | ------- | ---------- | ------- |
| test_prompteval_score_normalization.py | 3 | 100% | 0.02s |
| test_local_model_geval_parsing.py | 8 | 95% | 0.05s |
| **Total** | **11** | **97%** | **0.07s** |

### Performance Targets

- ✅ Unit tests should run in < 0.1s each
- ✅ Total suite should complete in < 1s
- ✅ Coverage should be > 90%
- ✅ Zero external dependencies

## 🔧 Test Utilities

### Common Fixtures

```python
# conftest.py
import pytest

@pytest.fixture
def sample_score():
    """Provide sample score for testing."""
    return 8.5

@pytest.fixture
def sample_response():
    """Provide sample LLM response."""
    return {
        "score": 8.5,
        "reasoning": "Good prompt",
        "dimensions": {
            "clarity": 9,
            "specificity": 8
        }
    }

@pytest.fixture
def mock_parser():
    """Provide mocked parser."""
    from unittest.mock import Mock
    parser = Mock()
    parser.parse.return_value = {"score": 8.5}
    return parser
```

### Helper Functions

```python
# test_helpers.py
def assert_score_in_range(score, min_val=0, max_val=100):
    """Assert score is within valid range."""
    assert min_val <= score <= max_val, \
        f"Score {score} not in range [{min_val}, {max_val}]"

def assert_valid_json(response):
    """Assert response is valid JSON."""
    import json
    try:
        json.loads(response)
    except json.JSONDecodeError as e:
        pytest.fail(f"Invalid JSON: {e}")

def create_test_response(score=8.5, **kwargs):
    """Create test response with defaults."""
    return {
        "score": score,
        "reasoning": kwargs.get("reasoning", "Test"),
        **kwargs
    }
```

## 🐛 Debugging Unit Tests

### Isolate Failing Test

```bash
# Run only failing test
pytest testing/unit/test_prompteval_score_normalization.py::test_normalize_score_to_pct_rubric_bounds -v

# Run with detailed output
pytest testing/unit/ -vv --tb=long

# Run with pdb debugger
pytest testing/unit/ --pdb
```

### Add Debug Output

```python
def test_with_debug():
    """Test with debug output."""
    score = normalize_score(5.5)
    print(f"DEBUG: score = {score}")  # Will show with -s flag
    assert score == 50.0

# Run with output shown
# pytest testing/unit/test_file.py::test_with_debug -v -s
```

### Use Hypothesis for Property Testing

```python
from hypothesis import given, strategies as st

@given(st.floats(min_value=-100, max_value=200))
def test_normalize_score_always_returns_valid_range(score):
    """Property test: normalized score always in 0-100 range."""
    result = normalize_score(score)
    assert 0 <= result <= 100
```

## 📈 CI/CD Integration

### GitHub Actions Example

```yaml
name: Unit Tests

on:
  pull_request:
    paths:

      - 'testing/unit/**'
      - 'tools/prompteval/**'

jobs:
  unit-tests:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.11', '3.12', '3.13']

    steps:

      - uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python-version }}

        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies

        run: |
          pip install pytest pytest-cov

      - name: Run unit tests

        run: |
          pytest testing/unit/ \
            -v \
            --cov=tools.prompteval \
            --cov-report=xml \
            --cov-report=term \
            --durations=10

      - name: Check coverage threshold

        run: |
          coverage report --fail-under=90

      - name: Upload coverage

        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## 🔗 Dependencies

```bash
# Minimal dependencies for unit tests
pip install pytest

# Optional: for better assertions
pip install pytest-clarity

# Optional: for property testing
pip install hypothesis

# Optional: for parametrize helpers
pip install pytest-parametrize-cases
```

## 📖 See Also

- [../tool_tests/README.md](../tool_tests/README.md) - Tool-specific tests
- [../integration/README.md](../integration/README.md) - Integration tests
- [../framework/README.md](../framework/README.md) - Testing framework
- [../../tools/prompteval/README.md](../../tools/prompteval/README.md) - PromptEval documentation

---

**Built with ❤️ for fast, focused unit testing**
