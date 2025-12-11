---
title: Prompt Library Tools
shortTitle: Tools
intro: Prompt auditing and validation tools for the prompt library.
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
version: '2.0'
date: '2025-12-04'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
---
# Prompt Library Tools

Prompt auditing, validation, and evaluation tools.

> **📋 Architecture**: See [ARCHITECTURE_PLAN.md](../docs/ARCHITECTURE_PLAN.md) for the complete tooling architecture.

## Quick Start

```bash
# Run prompt evaluations (PRIMARY TOOL)
python testing/evals/dual_eval.py prompts/developers/ --log-file eval.md

# Audit prompts for migration/validation issues
python tools/audit_prompts.py prompts/ --output audit_report.csv

# Validate frontmatter schema compliance
python tools/validators/frontmatter_validator.py --all
```text
---

## Active Tools

### 1. Prompt Auditor (`audit_prompts.py`)

Scans library and generates CSV migration report. **Only processes actual prompt files** (excludes agents, instructions, docs).

```bash
python tools/audit_prompts.py prompts/ --output audit_report.csv
```text
### 2. Frontmatter Validator (`validators/frontmatter_validator.py`)

Validates YAML frontmatter against the metadata schema.

```bash
python tools/validators/frontmatter_validator.py --all
python tools/validators/frontmatter_validator.py prompts/developers/
```yaml
---

## Scoring Rubrics

Located in `rubrics/`:

| File | Purpose |
|------|---------|
| `quality_standards.json` | Tier-based quality scoring (0-100) |
| `prompt-scoring.yaml` | 5-dimension effectiveness scoring (1.0-5.0) |

---

## Evaluation Tools

The following tools handle prompt library evaluation:

| Tool | Description |
|------|-------------|
| `evaluation_agent.py` | Autonomous multi-phase evaluation agent |
| `evaluate_library.py` | Dual-rubric library evaluator (quality + effectiveness) |
| `generate_eval_files.py` | Generate YAML eval files from prompts |
| `run_gh_eval.py` | Run `gh models eval` and format reports |
| `improve_prompts.py` | Generate improvement recommendations |

---

## Archived Documentation

The following documentation has been archived to `tools/archive/`:

| File | Description |
|------|-------------|
| `EVALUATION_AGENT_GUIDE.md` | User guide for the evaluation agent |

---

## File Structure

```text
tools/
├── README.md                      # This file
├── audit_prompts.py               # CSV migration audit
├── evaluation_agent.py            # Autonomous evaluation agent
├── evaluate_library.py            # Dual-rubric library evaluator
├── generate_eval_files.py         # YAML eval file generator
├── run_gh_eval.py                 # GitHub Models eval runner
├── improve_prompts.py             # Improvement recommendations
├── validators/
│   ├── frontmatter_validator.py   # Schema validation
│   ├── metadata_schema.yaml       # Schema definition
│   └── prompt_validator.py        # Content validation
├── rubrics/
│   ├── quality_standards.json     # Tier scoring
│   └── prompt-scoring.yaml        # Effectiveness scoring
├── analyzers/
│   └── prompt_analyzer.py         # Prompt analysis
└── archive/                       # Deprecated tools
    ├── evaluation_agent.py
    ├── evaluate_library.py
    └── improve_prompts.py
```text
---

## See Also

- [ARCHITECTURE_PLAN.md](../docs/ARCHITECTURE_PLAN.md) - Complete tooling architecture
- [testing/evals/README.md](../testing/evals/README.md) - Primary evaluation tool
- [COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md](../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md) - Scoring methodology
