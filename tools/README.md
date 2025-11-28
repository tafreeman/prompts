# Universal Code Generator

AI-powered code/prompt generation with multi-model quality review.

## Overview

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
