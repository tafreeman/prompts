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
```

---

## Active Tools

### 1. Prompt Auditor (`audit_prompts.py`)

Scans library and generates CSV migration report. **Only processes actual prompt files** (excludes agents, instructions, docs).

```bash
python tools/audit_prompts.py prompts/ --output audit_report.csv
```

### 2. Frontmatter Validator (`validators/frontmatter_validator.py`)

Validates YAML frontmatter against the metadata schema.

```bash
python tools/validators/frontmatter_validator.py --all
python tools/validators/frontmatter_validator.py prompts/developers/
```

---

## Scoring Rubrics

Located in `rubrics/`:

| File | Purpose |
|------|---------|
| `quality_standards.json` | Tier-based quality scoring (0-100) |
| `prompt-scoring.yaml` | 5-dimension effectiveness scoring (1.0-5.0) |

---

## Archived Tools

The following tools have been archived to `tools/archive/` (December 4, 2025):

| Tool | Reason |
|------|--------|
| `evaluation_agent.py` | Superseded by `testing/evals/dual_eval.py` |
| `evaluate_library.py` | Different approach, not API-based |
| `improve_prompts.py` | Redundant with evaluation outputs |
| `generate_eval_files.py` | Logic merged into dual_eval.py |
| `run_gh_eval.py` | Superseded by dual_eval.py batch mode |
| `EVALUATION_AGENT_GUIDE.md` | Documentation for archived agent |

---

## File Structure

```
tools/
├── README.md                      # This file
├── audit_prompts.py               # CSV migration audit
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
```

---

## See Also

- [ARCHITECTURE_PLAN.md](../docs/ARCHITECTURE_PLAN.md) - Complete tooling architecture
- [testing/evals/README.md](../testing/evals/README.md) - Primary evaluation tool
- [COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md](../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md) - Scoring methodology
