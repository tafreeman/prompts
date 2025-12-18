---
title: Prompt Testing & Evaluation
shortTitle: Testing
intro: Testing framework for prompt validation and evaluation.
type: reference
difficulty: beginner
audience:
- senior-engineer
- junior-engineer
platforms:
- github-copilot
- claude
- chatgpt
author: Prompts Library Team
version: '3.0'
date: '2025-12-04'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: approved
---
# 🧪 Prompt Testing & Evaluation

Focused testing framework for validation and multi-model evaluation.

> **📋 Architecture**: See [ARCHITECTURE_PLAN.md](../docs/ARCHITECTURE_PLAN.md) for the complete testing architecture.

## 📁 Directory Structure

```text
testing/
├── README.md               # This file
├── conftest.py             # Shared pytest fixtures
├── requirements.txt        # Test dependencies
├── run_tests.py            # Test runner script
│
├── unit/                   # Unit tests
│   └── __init__.py
│
├── integration/            # Integration & E2E tests
│   ├── __init__.py
│   ├── test_prompt_integration.py
│   ├── test_prompt_toolkit.py
│   ├── test_evaluation_agent_e2e.py
│   └── test_evaluation_agent_integration.py
│
├── tools/                  # Tool-specific tests
│   ├── __init__.py
│   ├── test_evaluation_agent.py
│   ├── test_generator.py
│   ├── test_llm_connection.py
│   └── test_cli.py
│
├── evals/                  # Evaluation tests & tool
│   ├── dual_eval.py            # Multi-model evaluation (PRIMARY)
│   ├── test_dual_eval.py       # Unit tests (66 tests)
│   ├── README.md               # Eval tool documentation
│   └── results/                # Evaluation outputs
│
├── validators/             # Validation tests
│   ├── test_frontmatter.py     # Frontmatter validation (27 tests)
│   ├── test_frontmatter_auditor.py
│   ├── test_schema.py          # Schema compliance (23 tests)
│   └── README.md               # Validator documentation
│
├── framework/              # Test framework core
│   └── core/
│       └── test_runner.py
│
└── archive/                # Archived legacy tests
```

text

## 🚀 Quick Start

```bash
# Run all tests (116 total)
python -m pytest testing/ -v

# Run evaluation tests only (66 tests)
python -m pytest testing/evals/ -v

# Run validation tests only (50 tests)
python -m pytest testing/validators/ -v

# Run the primary evaluation tool
python testing/evals/dual_eval.py prompts/developers/ --format markdown
```text
## 🔬 Primary Evaluation Tool

The main tool for prompt evaluation is `testing/evals/dual_eval.py`.

See [testing/evals/README.md](evals/README.md) for full documentation.

### Key Features

- **Multi-model evaluation**: Cross-validate with 5+ models
- **Batch processing**: Evaluate entire folders or glob patterns
- **JSON output**: CI/CD integration ready
- **Changed-only mode**: Evaluate only git-modified files
- **File filtering**: Auto-excludes agents, instructions, READMEs
- **8-dimension rubric**: Comprehensive quality assessment

### Example Commands

```bash
# Evaluate a single prompt
python testing/evals/dual_eval.py prompts/developers/code-review.md

# Evaluate folder with JSON output
python testing/evals/dual_eval.py prompts/ --format json --output results.json

# CI/CD: Only changed files
python testing/evals/dual_eval.py prompts/ --changed-only --quiet

# Include all files (override filtering)
python testing/evals/dual_eval.py prompts/ --include-all
```text
## ✅ Test Categories

| Category | Location | Tests | Purpose |
|----------|----------|-------|---------|
| **Evaluation** | `evals/test_dual_eval.py` | 66 | Core eval tool functionality |
| **Frontmatter** | `validators/test_frontmatter.py` | 27 | Required fields, parsing |
| **Schema** | `validators/test_schema.py` | 23 | Field types, constraints |

### Running Specific Tests

```bash
# Run by file
python -m pytest testing/evals/test_dual_eval.py -v

# Run by test class
python -m pytest testing/validators/test_schema.py::TestValidationFunctions -v

# Run by test name pattern
python -m pytest testing/ -k "frontmatter" -v
```text
## 📊 Scoring Rubric

Prompts are evaluated on **8 dimensions** (scored 1-10):

| Criterion | Description | Pass Threshold |
|-----------|-------------|----------------|
| **Clarity** | How clear and unambiguous | ≥7.0 |
| **Specificity** | Enough detail for consistency | ≥7.0 |
| **Actionability** | Clear actions to take | ≥7.0 |
| **Structure** | Well-organized sections | ≥7.0 |
| **Completeness** | All necessary aspects covered | ≥7.0 |
| **Factuality** | Accurate claims/examples | ≥7.0 |
| **Consistency** | Reproducible outputs | ≥7.0 |
| **Safety** | Avoids harmful patterns | ≥7.0 |

**Pass Criteria**:
- Overall score ≥ 7.0/10
- No individual dimension < 5.0/10
- Cross-validation variance ≤ 1.5

## 🔄 CI/CD Integration

The testing framework is integrated with GitHub Actions:

```yaml
# .github/workflows/prompt-validation.yml
- name: Run unit tests
  run: pytest testing/evals/test_dual_eval.py -v

- name: Validate frontmatter
  run: python tools/validators/frontmatter_validator.py --all

- name: Evaluate changed prompts (PR only)
  run: |
    python testing/evals/dual_eval.py prompts/ \
      --changed-only \
      --format json
```json
## 📦 Dependencies

Install test dependencies:

```bash
pip install -r testing/requirements.txt
```json
Required packages:
- `pytest` - Test runner
- `pyyaml` - YAML parsing
- `pytest-asyncio` - Async test support (optional)

## 📖 See Also

- [testing/evals/README.md](evals/README.md) - Detailed evaluation documentation
- [testing/validators/README.md](validators/README.md) - Validation test details
- [ARCHITECTURE_PLAN.md](../docs/ARCHITECTURE_PLAN.md) - Complete architecture
- [CONSOLIDATED_IMPROVEMENT_PLAN.md](../docs/CONSOLIDATED_IMPROVEMENT_PLAN.md) - Roadmap

---

**Built with ❤️ for reliable AI prompt development**
