---
title: Code Generation Tools
shortTitle: Tools
intro: AI-powered code and prompt generation tools with multi-model quality review workflow.
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
version: '1.0'
date: '2025-11-30'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
---
# Prompt Library Tools

AI-powered code/prompt generation, evaluation, and validation tools.

## Quick Start: Evaluate the Library

```bash
# Run unified evaluation (uses BOTH rubrics)
python tools/evaluate_library.py --all --summary

# Audit prompts for migration/validation issues
python tools/audit_prompts.py prompts/ --output audit_report.csv

# Validate frontmatter schema compliance
python tools/validators/frontmatter_validator.py --all
```

---

## Evaluation Tools

### 1. Unified Library Evaluator (`evaluate_library.py`) ⭐ NEW

**Combines both rubrics** for comprehensive prompt scoring:

| Rubric | Scale | Source |
|--------|-------|--------|
| Quality Standards | 0-100 (Tiers 1-4) | `rubrics/quality_standards.json` |
| Effectiveness Score | 1.0-5.0 (Stars) | `rubrics/prompt-scoring.yaml` |

```bash
# Evaluate all prompts
python tools/evaluate_library.py --all --output docs/EVALUATION_REPORT.md

# Evaluate specific folder
python tools/evaluate_library.py --folder prompts/developers/

# Evaluate single file with verbose output
python tools/evaluate_library.py prompts/business/budget-tracker.md --verbose
```

**Combined Grades:**
- **A (Excellent)**: Quality ≥90, Effectiveness ≥4.5
- **B (Good)**: Quality ≥75, Effectiveness ≥4.0
- **C (Acceptable)**: Quality ≥60, Effectiveness ≥3.0
- **D (Below Average)**: Quality ≥45 or Effectiveness ≥2.5
- **F (Poor)**: Below thresholds

### 2. Prompt Auditor (`audit_prompts.py`)

Scans library and generates CSV migration report. **Only processes actual prompt files** (excludes agents, instructions, docs).

```bash
python tools/audit_prompts.py prompts/ --output audit_report.csv
```

---

## Scoring Rubrics

### Quality Standards (`rubrics/quality_standards.json`)

| Criterion | Weight | What it measures |
|-----------|--------|------------------|
| **Completeness** | 25% | All required sections present |
| **Example Quality** | 30% | Realistic, detailed, no placeholders |
| **Specificity** | 20% | Domain-specific, actionable content |
| **Format Adherence** | 15% | Valid YAML, correct markdown |
| **Enterprise Quality** | 10% | Professional, references frameworks |

**Tier Scoring:**
- **Tier 1 (90-100)**: Excellent - Production ready
- **Tier 2 (75-89)**: Good - Minor improvements
- **Tier 3 (60-74)**: Acceptable - Needs work
- **Tier 4 (0-59)**: Poor - Major rewrite

### Effectiveness Rubric (`rubrics/prompt-scoring.yaml`)

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| **Clarity** | 25% | Unambiguous, easy to understand |
| **Effectiveness** | 30% | Produces quality output consistently |
| **Reusability** | 20% | Works across different contexts |
| **Simplicity** | 15% | Minimal without losing value |
| **Examples** | 10% | Helpful and realistic |

**Star Ratings:**
- ⭐⭐⭐⭐⭐ **(4.5-5.0)**: Excellent
- ⭐⭐⭐⭐ **(4.0-4.4)**: Good
- ⭐⭐⭐ **(3.0-3.9)**: Acceptable
- ⭐⭐ **(2.0-2.9)**: Below Average
- ⭐ **(1.0-1.9)**: Poor

---

## Code Generator

# Universal Code Generator

AI-powered code/prompt generation with multi-model quality review.

### Overview

The Universal Code Generator applies a three-step workflow to create Tier 1 quality content:

1. **Generate** (Gemini 1.5 Pro) - Create initial draft
2. **Review** (Claude Sonnet 4) - Score against quality rubric (0-100)
3. **Refine** (Gemini 1.5 Pro) - Improve based on feedback

## Installation

```bash
# Install dependencies
pip install click

# Optional: Set model preferences via environment variables
│   ├── ModelConfig (default models, temperatures)
│   └── PathConfig (templates, rubrics)
├── LLMClient (tools/llm_client.py)
│   └── Provider dispatch (Gemini/Claude/GPT)
├── Generator (tools/models/generator.py)
├── Reviewer (tools/models/reviewer.py)
│   └── Quality rubric (tools/rubrics/quality_standards.json)
└── Refiner (tools/models/refiner.py)
```

## Configuration

### Via Environment Variables

```bash
export GEN_MODEL="gemini-1.5-pro"        # Generation model
export REV_MODEL="claude-sonnet-4"       # Review model
export REF_MODEL="gemini-1.5-pro"        # Refinement model
```

### Via Code

```python
from tools.config import Config, ModelConfig
from tools.code_generator import UniversalCodeGenerator

custom_config = Config()
custom_config.models = ModelConfig(
    generator_model="gemini-2.0-flash-thinking",
    reviewer_model="claude-sonnet-4",
    refiner_model="gemini-1.5-pro"
)

generator = UniversalCodeGenerator(config=custom_config)
```

## Quality Rubric

The reviewer scores content against 5 criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Completeness** | 25% | All required sections present |
| **Example Quality** | 30% | Realistic, detailed scenarios |
| **Specificity** | 20% | Actionable, concrete content |
| **Format Adherence** | 15% | Valid YAML, markdown structure |
| **Enterprise Quality** | 10% | References frameworks, metrics |

**Scoring**:

- **90-100**: Tier 1 (Excellent)
- **75-89**: Tier 2 (Good)
- **60-74**: Tier 3 (Acceptable)
- **<60**: Tier 4 (Poor)

## Current Status

✅ **Phases A-D Complete**

- Core generator class
- Quality review with rubric
- Refinement loop
- CLI interface (interactive + non-interactive)

⏳ **Phase E: In Progress**

- Real API integration (currently mocked)
- Regression testing
- Documentation

## Examples

### Example 1: Generate Business Prompt

```bash
python -m tools.cli.main create \
  --category business \
  --use-case "Project Risk Register for IT Transformations" \
  --variables '{"project_name": "ERP Modernization", "risk_categories": "Technical, Financial, Organizational"}' \
  --output risk-register.md
```

### Example 2: Interactive Wizard

```bash
$ python -m tools.cli.main interactive

🎯 Universal Code Generator - Interactive Mode
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Category: business
📝 Use Case (be specific): Create executive budget tracker
📝 Enter variables (leave empty to finish):
Variable name: project_name
Value for 'project_name': Cloud Platform Migration

🚀 Generating content...
✅ Generation Complete!
Review Score: 88
```

## Testing

```bash
# Run core workflow test
python -m tools.test_generator

# Run CLI test
python -m tools.cli.test_cli
```

## File Structure

```
tools/
├── README.md                  # This file
├── config.py                  # Configuration management
├── llm_client.py              # LLM provider abstraction
├── code_generator.py          # Main UniversalCodeGenerator class
├── test_generator.py          # Core verification tests
├── models/
│   ├── generator.py           # Generation step
│   ├── reviewer.py            # Quality review step
│   └── refiner.py             # Refinement step
├── rubrics/
│   └── quality_standards.json # Tier 1 quality criteria
└── cli/
    ├── main.py                # CLI entry point
    ├── interactive.py         # Interactive wizard
    └── test_cli.py            # CLI tests
```

## Next Steps

1. **Connect Real APIs**: Replace mocked LLMClient with actual API calls
2. **Template System**: Build template selection logic
3. **Batch Processing**: Add `upgrade-stubs` command for bulk prompt upgrades
4. **Performance Tracking**: Log generation times and costs

## Support

For issues or questions, refer to:

- `walkthrough.md` - Detailed implementation walkthrough
- `implementation_plan.md` - Full architecture plan
- `quality_standards.json` - Complete rubric criteria
