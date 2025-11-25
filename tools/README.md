# Validation & Automation Tools

Comprehensive tooling for prompt development, validation, and optimization.

## 📁 Directory Structure

```
tools/
├── validators/      # Validation frameworks and schema
├── benchmarks/      # Performance evaluation tools
├── generators/      # Prompt generation utilities
├── optimizers/      # Optimization engines
└── integrations/    # IDE and platform integrations
```

## 🛠️ Core Tools

### Prompt Validator

**Path:** `validators/prompt_validator.py`

Comprehensive validation framework with 5 validators:

- Structure validation
- Metadata compliance
- Performance assessment
- Security scanning
- Accessibility checks

**Usage:**

```bash
python tools/validators/prompt_validator.py path/to/prompt.md

# JSON output
python tools/validators/prompt_validator.py path/to/prompt.md --json

# Custom minimum score
python tools/validators/prompt_validator.py path/to/prompt.md --min-score 80
```

### Performance Evaluator

**Path:** `benchmarks/performance_evaluator.py`

Automated performance benchmarking with 4 benchmark suites:

- Accuracy benchmarking
- Latency measurement
- Cost efficiency analysis
- Robustness testing

**Usage:**

```bash
python tools/benchmarks/performance_evaluator.py path/to/prompt.md

# With test cases
python tools/benchmarks/performance_evaluator.py path/to/prompt.md --test-cases tests.json
```

### Metadata Schema

**Path:** `validators/metadata_schema.yaml`

Enhanced metadata schema defining:

- Required and optional fields
- Framework compatibility specifications
- Performance metrics structure
- Governance and testing fields

## 🚀 Quick Start

### Validate a Prompt

```bash
cd d:/source/tafreeman/prompts

# Install dependencies
pip install -r requirements.txt

# Validate prompt
python tools/validators/prompt_validator.py techniques/reflexion/basic-reflexion/basic-reflexion.md
```

### Benchmark Performance

```bash
python tools/benchmarks/performance_evaluator.py techniques/reflexion/basic-reflexion/basic-reflexion.md
```

## 📊 Validation Report Example

```
======================================================================
Validation Report: techniques/reflexion/basic-reflexion.md
======================================================================

Scores:
  Structure:      95.0/100
  Metadata:       98.0/100
  Performance:    85.0/100
  Security:       92.0/100
  Accessibility:  88.0/100
  ────────────────────────────────────────
  Overall:        92.1/100

✅ Validation passed (score 92.1)
```

## 🔧 Python API

### Validation Framework

```python
from tools.validators.prompt_validator import PromptValidationFramework

# Initialize framework
validator = PromptValidationFramework()

# Validate prompt
report = validator.validate_prompt("path/to/prompt.md")

# Get suggestions
suggestions = validator.generate_improvement_suggestions(report)

print(f"Overall Score: {report.overall_score}/100")
for suggestion in suggestions:
    print(f"- {suggestion}")
```

### Performance Evaluator

```python
from tools.benchmarks.performance_evaluator import PromptPerformanceEvaluator

# Initialize evaluator
evaluator = PromptPerformanceEvaluator()

# Evaluate prompt
report = evaluator.evaluate_prompt_file("path/to/prompt.md")

# Get recommendations
recommendations = evaluator.generate_recommendations(report)

print(f"Performance Score: {report.overall_score}/100")
```

## 📝 Metadata Schema Usage

All prompts must include YAML frontmatter following the schema:

```yaml
---
title: "Your Prompt Title"
category: "techniques"
subcategory: "reflexion"
difficulty: "advanced"
framework_compatibility:
  langchain: ">=0.1.0"
  anthropic: ">=0.8.0"
performance_metrics:
  accuracy_improvement: "20-30%"
  latency_impact: "medium"
version: "1.0.0"
author: "Your Name"
last_updated: "2025-11-23"
---
```

See [`validators/metadata_schema.yaml`](./validators/metadata_schema.yaml) for complete specification.

## 🧪 Testing

Run validator tests:

```bash
pytest tools/validators/test_prompt_validator.py -v
```

Run evaluator tests:

```bash
pytest tools/benchmarks/test_performance_evaluator.py -v
```

## 🎯 Quality Standards

Our automated tools enforce:

- **Metadata Compliance:** >95% required fields present
- **Structure Quality:** >80% well-formed sections
- **Performance Documentation:** Metrics documented
- **Security:** No high-risk patterns detected
- **Overall Score:** >75 for acceptance

## 🤝 Contributing

When adding new tools:

1. Follow existing code structure
2. Include comprehensive docstrings
3. Add unit tests (pytest)
4. Update this README
5. Document CLI interface

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for details.

## 📚 Tool Dependencies

- Python 3.8+
- pyyaml>=6.0.1
- pytest>=7.4.0 (for testing)

Optional for specific features:

- langchain (for framework integrations)
- anthropic (for Claude-specific tools)
- openai (for GPT-specific tools)
