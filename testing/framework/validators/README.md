# ✅ Validation Framework

Comprehensive validation system for prompt outputs with multiple validators.

## 📋 Overview

This directory contains the validation framework that validates LLM outputs against expected results, format requirements, and quality standards. Each validator implements the `BaseValidator` interface and can be composed into validation pipelines.

## 📁 Files

```
validators/
├── README.md              # This file
├── __init__.py            # Package initialization & exports
├── base_validator.py      # Base validator class
├── code_validator.py      # Code syntax validation
├── content_validator.py   # Content quality validation
├── format_validator.py    # Format/structure validation
└── semantic_validator.py  # Semantic similarity validation
```

## 🚀 Quick Start

### Basic Usage

```python
from framework.validators import CodeValidator, SemanticValidator

# Validate Python code
code_validator = CodeValidator(language='python')
is_valid = await code_validator.validate(
    output="def hello():\n    print('Hello')",
    expected={"syntax": "valid", "has_function": True}
)

# Validate semantic similarity
semantic_validator = SemanticValidator(
    expected_keywords=["greeting", "hello", "welcome"]
)
is_valid = await semantic_validator.validate(
    output="Hello! Welcome to our service.",
    expected={"contains": ["greeting"]}
)
```

### Using with Test Runner

```yaml
# test_suite.yaml
test_cases:

  - id: test_code_generation

    validators:

      - code_python      # Python syntax validation
      - semantic         # Semantic correctness
      - format           # Output format

```

```python
# In test runner
runner = PromptTestRunner()
runner.validators = {
    'code_python': CodeValidator(language='python'),
    'semantic': SemanticValidator(['correct', 'accurate']),
    'format': FormatValidator()
}
```

## 🔧 Available Validators

### 1. BaseValidator

Abstract base class for all validators.

**Purpose:** Provides common validation infrastructure and utilities.

**Features:**

- Error and warning collection
- Deep object comparison
- Pattern matching
- Validation reporting

```python
class BaseValidator(ABC):
    @abstractmethod
    async def validate(self, output: Any, expected: Optional[Any] = None) -> bool:
        """Validate output against expected result."""
        pass

    def add_error(self, message: str)
    def add_warning(self, message: str)
    def get_validation_report(self) -> Dict[str, Any]
    def _deep_compare(self, actual, expected, path="") -> bool
    def _contains_all(self, output: str, required_items: List[str]) -> bool
    def _matches_pattern(self, text: str, pattern: str) -> bool
```

**Usage:**

```python
from framework.validators.base_validator import BaseValidator

class MyValidator(BaseValidator):
    async def validate(self, output, expected=None):
        if output is None:
            self.add_error("Output is None")
            return False

        if expected and not self._contains_all(output, expected.get("keywords", [])):
            return False

        return True
```

### 2. CodeValidator

Validates code syntax and structure.

**Purpose:** Ensure generated code is syntactically correct and follows conventions.

**Supported Languages:**

- Python
- JavaScript
- TypeScript (future)
- SQL (future)

**Configuration:**

```python
validator = CodeValidator(
    language='python',
    strict_mode=True,        # Enforce strict linting
    check_imports=True,      # Validate imports
    check_style=False        # Skip style checks
)
```

**Validation Checks:**

| Check | Description | Example |
| ------- | ------------- | --------- |
| Syntax | Valid language syntax | No `SyntaxError` |
| Imports | Valid import statements | `import os` exists |
| Functions | Function definitions | `def func():` present |
| Classes | Class definitions | `class MyClass:` present |
| Type hints | Type annotations (Python 3.6+) | `def func(x: int) -> str:` |

**Usage:**

```python
# Python validation
python_validator = CodeValidator(language='python')
result = await python_validator.validate(
    output="""
def calculate_sum(a: int, b: int) -> int:
    return a + b
    """,
    expected={
        "has_function": "calculate_sum",
        "has_type_hints": True,
        "syntax": "valid"
    }
)

# JavaScript validation
js_validator = CodeValidator(language='javascript')
result = await js_validator.validate(
    output="function hello() { console.log('hi'); }",
    expected={"has_function": "hello"}
)
```

### 3. ContentValidator

Validates content quality and completeness.

**Purpose:** Check if output meets content quality standards.

**Validation Checks:**

| Check | Description | Configuration |
| ------- | ------------- | --------------- |
| Length | Min/max character count | `min_length`, `max_length` |
| Required sections | Expected sections present | `required_sections` |
| Keywords | Required keywords included | `required_keywords` |
| Tone | Writing tone consistency | `expected_tone` |
| Readability | Reading level | `max_reading_level` |

**Usage:**

```python
validator = ContentValidator(
    min_length=100,
    max_length=5000,
    required_keywords=["security", "authentication"],
    required_sections=["Overview", "Implementation"]
)

result = await validator.validate(
    output="# Overview\nSecurity best practices...",
    expected={
        "has_sections": ["Overview"],
        "contains_keywords": ["security"]
    }
)
```

### 4. FormatValidator

Validates output format and structure.

**Purpose:** Ensure output follows specified format (JSON, XML, Markdown, etc.).

**Supported Formats:**

- JSON
- XML
- YAML
- Markdown
- HTML
- CSV

**Usage:**

```python
# JSON validation
json_validator = FormatValidator(format='json')
result = await json_validator.validate(
    output='{"name": "John", "age": 30}',
    expected={
        "schema": {
            "type": "object",
            "required": ["name", "age"]
        }
    }
)

# Markdown validation
md_validator = FormatValidator(format='markdown')
result = await md_validator.validate(
    output="# Title\n\n## Section\n\nContent here",
    expected={
        "has_title": True,
        "has_sections": True,
        "min_sections": 1
    }
)
```

**JSON Schema Validation:**

```python
validator = FormatValidator(format='json')
result = await validator.validate(
    output='{"user": "john", "email": "john@example.com"}',
    expected={
        "schema": {
            "type": "object",
            "properties": {
                "user": {"type": "string"},
                "email": {"type": "string", "format": "email"}
            },
            "required": ["user", "email"]
        }
    }
)
```

### 5. SemanticValidator

Validates semantic meaning and similarity.

**Purpose:** Check if output conveys the expected meaning, even with different wording.

**Validation Approaches:**

| Approach | Description | Use Case |
| ---------- | ------------- | ---------- |
| Keyword matching | Required terms present | Specific terminology |
| Phrase matching | Expected phrases found | Exact requirements |
| Embedding similarity | Vector similarity (future) | Semantic equivalence |
| Intent matching | Goal achievement | Task completion |

**Usage:**

```python
# Keyword-based validation
validator = SemanticValidator(
    expected_keywords=["authentication", "authorization", "security"],
    similarity_threshold=0.8
)

result = await validator.validate(
    output="The system uses OAuth for auth and implements role-based access control.",
    expected={
        "keywords": ["authentication", "authorization"],
        "min_keyword_match": 2
    }
)

# Intent validation
validator = SemanticValidator()
result = await validator.validate(
    output="I've implemented JWT-based authentication with refresh tokens.",
    expected={
        "intent": "describe_authentication",
        "conveys": ["implementation", "token-based"]
    }
)
```

## 🎯 Validation Pipeline

### Sequential Validation

```python
async def validate_all(output, expected):
    validators = [
        CodeValidator(language='python'),
        SemanticValidator(['correct', 'valid']),
        FormatValidator(format='json')
    ]

    results = {}
    for validator in validators:
        results[validator.__class__.__name__] = await validator.validate(
            output, 
            expected
        )

    return all(results.values()), results
```

### Conditional Validation

```python
async def validate_conditional(output, expected, output_type):
    if output_type == 'code':
        return await CodeValidator('python').validate(output, expected)
    elif output_type == 'json':
        return await FormatValidator('json').validate(output, expected)
    else:
        return await ContentValidator().validate(output, expected)
```

## 📊 Validation Reports

Get detailed validation reports:

```python
validator = CodeValidator(language='python')
result = await validator.validate(code_output, expected)

report = validator.get_validation_report()
print(report)
```

**Report Format:**

```json
{
  "errors": [
    "Syntax error on line 5: expected ':'",
    "Missing required function: calculate_total"
  ],
  "warnings": [
    "Function 'helper' is not type-hinted",
    "Unused import: sys"
  ],
  "error_count": 2,
  "warning_count": 2,
  "is_valid": false
}
```

## 🔧 Custom Validators

Create custom validators by extending `BaseValidator`:

```python
from framework.validators.base_validator import BaseValidator

class SecurityValidator(BaseValidator):
    """Validates code for security issues."""

    def __init__(self, strict=True):
        super().__init__()
        self.strict = strict
        self.dangerous_patterns = [
            r'eval\(',
            r'exec\(',
            r'__import__',
            r'os\.system',
        ]

    async def validate(self, output, expected=None):
        import re

        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, output):
                self.add_error(f"Dangerous pattern found: {pattern}")
                if self.strict:
                    return False
                else:
                    self.add_warning(f"Potentially unsafe: {pattern}")

        # Check for SQL injection vulnerabilities
        if 'SELECT' in output and '%s' in output:
            self.add_warning("Potential SQL injection vulnerability")

        return len(self.validation_errors) == 0

# Register with test runner
runner.validators['security'] = SecurityValidator(strict=True)
```

## 🔄 Validator Composition

Combine multiple validators:

```python
class CompositeValidator(BaseValidator):
    """Combines multiple validators."""

    def __init__(self, validators: List[BaseValidator]):
        super().__init__()
        self.validators = validators

    async def validate(self, output, expected=None):
        all_valid = True

        for validator in self.validators:
            is_valid = await validator.validate(output, expected)
            all_valid = all_valid and is_valid

            # Collect errors from sub-validators
            report = validator.get_validation_report()
            self.validation_errors.extend(report['errors'])
            self.validation_warnings.extend(report['warnings'])

        return all_valid

# Usage
composite = CompositeValidator([
    CodeValidator('python'),
    SecurityValidator(),
    ContentValidator(min_length=50)
])
```

## 📈 Validation Metrics

Track validation performance:

```python
class MetricsCollectingValidator(BaseValidator):
    def __init__(self, wrapped_validator):
        super().__init__()
        self.wrapped = wrapped_validator
        self.validation_count = 0
        self.success_count = 0
        self.avg_time = 0

    async def validate(self, output, expected=None):
        import time
        start = time.time()

        result = await self.wrapped.validate(output, expected)

        self.validation_count += 1
        if result:
            self.success_count += 1

        duration = time.time() - start
        self.avg_time = (
            (self.avg_time * (self.validation_count - 1) + duration) 
            / self.validation_count
        )

        return result

    def get_metrics(self):
        return {
            "total_validations": self.validation_count,
            "success_rate": self.success_count / self.validation_count,
            "avg_validation_time": self.avg_time
        }
```

## 🐛 Troubleshooting

### Validator Not Found

```python
# Check registered validators
print(runner.validators.keys())

# Register missing validator
from framework.validators import CodeValidator
runner.validators['code_python'] = CodeValidator('python')
```

### Validation Always Fails

```python
# Enable debug mode
validator = CodeValidator('python')
result = await validator.validate(output, expected)

# Check detailed report
report = validator.get_validation_report()
print("Errors:", report['errors'])
print("Warnings:", report['warnings'])
```

### Performance Issues

```python
# Use caching for expensive validations
from functools import lru_cache

class CachedValidator(BaseValidator):
    @lru_cache(maxsize=1000)
    def _cached_validate(self, output_hash, expected_hash):
        # Expensive validation logic
        pass

    async def validate(self, output, expected):
        import hashlib
        output_hash = hashlib.md5(str(output).encode()).hexdigest()
        expected_hash = hashlib.md5(str(expected).encode()).hexdigest()
        return self._cached_validate(output_hash, expected_hash)
```

## 📖 See Also

- [../README.md](../README.md) - Framework overview
- [../core/README.md](../core/README.md) - Test runner implementation
- [../../integration/README.md](../../integration/README.md) - Integration tests
- [../../docs/ARCHITECTURE_PLAN.md](../../../docs/ARCHITECTURE_PLAN.md) - Overall architecture

---

**Built with ❤️ for reliable output validation**
