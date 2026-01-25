# Full Repository Analysis

**Generated**: 2026-01-25  
**Repository**: Enterprise AI Prompt Library  
**Analysis Status**: Complete

---

## Executive Summary

This document provides a comprehensive analysis of the entire repository, covering all folders, their contents, purpose, and current state. It also identifies outdated files recommended for removal.

### Repository Statistics

| Category | Count |
|----------|-------|
| Total Prompt Files | 165+ |
| Python Tools/Scripts | 80+ |
| Documentation Files | 50+ |
| Test Files | 40+ |
| Configuration Files | 15+ |
| Archived/Deprecated Items | 30+ |

---

## Table of Contents

1. [Root Directory](#root-directory)
2. [Prompts Directory](#prompts-directory)
3. [Tools Directory](#tools-directory)
4. [Testing Directory](#testing-directory)
5. [Documentation Directory](#documentation-directory)
6. [Archive Directory](#archive-directory)
7. [Scripts Directory](#scripts-directory)
8. [Data Directory](#data-directory)
9. [Workflows Directory](#workflows-directory)
10. [Reasoning Directory](#reasoning-directory)
11. [Multiagent Systems](#multiagent-systems)
12. [GitHub Configuration](#github-configuration)
13. [VS Code Configuration](#vscode-configuration)
14. [Outdated Files to Remove](#outdated-files-to-remove)
15. [Validation Issues Summary](#validation-issues-summary)
16. [Recommendations](#recommendations)

---

## Root Directory

### Core Files

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | Main repository documentation | ✅ Active |
| `LICENSE` | MIT License | ✅ Active |
| `CONTRIBUTING.md` | Contribution guidelines | ✅ Active |
| `SECURITY.md` | Security policy | ✅ Active |
| `pyproject.toml` | Python package configuration | ✅ Active |
| `pytest.ini` | Pytest configuration | ✅ Active |
| `requirements.txt` | Python dependencies | ✅ Active |
| `.env.example` | Environment variable template | ✅ Active |
| `.flake8` | Linting configuration | ✅ Active |
| `.gitignore` | Git ignore rules | ✅ Active |
| `prompt.py` | Unified CLI entry point | ✅ Active - Main tool |
| `prompts.sln` | Visual Studio solution | ✅ Active |

### Root Scripts (Potential Cleanup Candidates)

| File | Purpose | Status | Recommendation |
|------|---------|--------|----------------|
| `analyze_missing.py` | One-time registry analysis | ⚠️ Utility | Move to `scripts/` or archive |
| `update_progress_report.py` | One-time progress tracking | ⚠️ Utility | Move to `scripts/` or archive |
| `prompteval-tier0.json` | Evaluation results cache | ⚠️ Generated | Move to `archive/outputs/` |
| `promptevlas.json` | Evaluation results (typo in name) | ⚠️ Generated | Delete or archive |
| `validation_issues_full.txt` | Validation report | ⚠️ Generated | Move to `archive/` |
| `.cleanup_manifest.json` | Cleanup tracking | ⚠️ Internal | Can be deleted (empty ops) |

---

## Prompts Directory

The main content library with **165+ prompts** organized by category.

### Structure

```
prompts/
├── advanced/          # 28 files - CoT, ReAct, RAG, ToT patterns
├── agents/            # 12 files - GitHub Copilot custom agents
├── analysis/          # 24 files - Data/business analysis prompts
├── business/          # 16 files - Business operations prompts
├── creative/          # 2 files - Content creation prompts
├── developers/        # 29 files - Code generation/review prompts
├── frameworks/        # 5 subdirs - Provider-specific patterns
├── m365/              # 3 files - Microsoft 365 Copilot prompts
├── socmint/           # 7 files - OSINT investigation prompts
├── system/            # 24 files - System architecture prompts
├── techniques/        # 4 subdirs - Advanced prompting techniques
├── templates/         # 8 files - Reusable templates
├── index.md           # Category index
├── README.md          # Prompts overview
├── registry.yaml      # Prompt registry
└── self-consistency-reasoning.md # Standalone technique
```

### Category Details

#### `prompts/advanced/` (28 files)
**Purpose**: Advanced prompting patterns (Chain-of-Thought, ReAct, RAG, Tree-of-Thoughts)

| Notable Files | Description |
|--------------|-------------|
| `chain-of-thought-*.md` | 6 CoT variants |
| `react-*.md` | 4 ReAct patterns |
| `tree-of-thoughts-*.md` | 3 ToT evaluators |
| `lats-*.prompt.txt` | LATS (Language Agent Tree Search) prompts |
| `CoVe.md` | Chain of Verification |
| `reflection-self-critique.md` | Self-reflection pattern |

#### `prompts/agents/` (12 files)
**Purpose**: GitHub Copilot custom agents

| File | Agent Purpose |
|------|---------------|
| `architecture-agent.agent.md` | System design |
| `code-review-agent.agent.md` | PR reviews |
| `docs-agent.agent.md` | Documentation |
| `refactor-agent.agent.md` | Code improvement |
| `security-agent.agent.md` | Security analysis |
| `test-agent.agent.md` | Test generation |
| `prompt-agent.agent.md` | Prompt creation |
| `cloud-agent.agent.md` | Cloud architecture |
| `devsecops-tooling-agent.agent.md` | DevSecOps |
| `AGENTS_GUIDE.md` | Agent usage guide |
| `agent-template.md` | Template for new agents |

#### `prompts/analysis/` (24 files)
**Purpose**: Business and data analysis prompts

Key files: `data-analysis-insights.md`, `competitive-analysis-researcher.md`, `market-research-analyst.md`, `workflow-designer.md`, `tools-ecosystem-evaluator.md`

**Issues**: Contains a misnamed file `%% Mermaid radar chart illustrating samp.mmd` (Mermaid fragment)

#### `prompts/business/` (16 files)
**Purpose**: Business operations and management

Key files: `agile-sprint-planner.md`, `competitive-analysis.md`, `performance-review.md`, `pitch-deck-generator.md`

#### `prompts/creative/` (2 files)
**Purpose**: Content creation - **SPARSE CATEGORY**

Files: `ad-copy-generator.md`, `brand-voice-developer.md`

#### `prompts/developers/` (29 files)
**Purpose**: Software development assistance

Key files: `code-review-expert.md`, `api-design-consultant.md`, `devops-pipeline-architect.md`, `security-code-auditor.md`, `test-automation-engineer.md`

#### `prompts/frameworks/` (5 subdirectories)
**Purpose**: Provider-specific prompt patterns

| Subdirectory | Contents |
|--------------|----------|
| `anthropic/` | Claude patterns, tool-use |
| `langchain/` | Agent patterns, LCEL patterns |
| `microsoft/` | Copilot patterns, Semantic Kernel, .NET |
| `openai/` | Assistants API, function calling |
| `enterprise-prompt-evaluation-framework.md` | Evaluation framework |

#### `prompts/m365/` (3 files)
**Purpose**: Microsoft 365 Copilot integration

Files: `m365-daily-standup-assistant.md`, `m365-data-insights-assistant.md`, `README.md`

#### `prompts/socmint/` (7 files)
**Purpose**: OSINT/Social Media Intelligence

Files: `email-investigation.md`, `username-investigation.md`, `social-media-profile-analysis.md`, `socmint-investigator.md`

#### `prompts/system/` (24 files)
**Purpose**: System architecture and design

Key files: `ai-assistant-system-prompt.md`, `frontier-agent-deep-research.md`, various architecture specialist prompts

#### `prompts/techniques/` (4 subdirectories)
**Purpose**: Advanced prompting technique implementations

| Subdirectory | Contents |
|--------------|----------|
| `agentic/` | Multi-agent, single-agent patterns |
| `context-optimization/` | Compression, many-shot, RAG |
| `reflexion/` | Basic, domain-specific, multi-step reflexion |
| `README.md` | Techniques overview |

#### `prompts/templates/` (8 files)
**Purpose**: Canonical templates for prompt creation

Key files: `prompt-template.md` (canonical), `prompt-template-minimal.md`, `quick-start-template.md`

---

## Tools Directory

**The canonical tooling location** - All evaluation, validation, and LLM utilities.

### Structure

```
tools/
├── prompteval/        # ✅ PRIMARY - Unified evaluation tool
├── llm/               # LLM client and model management
├── core/              # Core utilities (caching, config, errors)
├── cli/               # Command-line interface
├── validation/        # Auto-fix and debug tools
├── validators/        # Schema validation
├── runners/           # Execution runners (CoVe, eval)
├── agents/            # Multi-agent orchestration
├── models/            # Model generators/refiners
├── analysis/          # Ecosystem analysis tools
├── scripts/           # Utility scripts
├── utils/             # Shared utilities
├── rubrics/           # Evaluation rubrics (YAML)
├── benchmarks/        # Performance evaluation
├── tests/             # Tool-specific tests
├── documentation/     # Tool documentation
├── docs/              # Additional docs
├── archive/           # Deprecated evaluation tools
├── README.md          # Tools overview
├── validate_prompts.py # Main validation entry point
└── __init__.py        # Package init
```

### Key Components

#### `tools/prompteval/` (16 files) - **PRIMARY EVALUATION TOOL**
**Purpose**: Unified prompt evaluation (replaces deprecated tools)

| File | Purpose |
|------|---------|
| `main.py` | Entry point |
| `core.py` | Core evaluation logic |
| `parser.py` | Prompt parsing |
| `unified_scorer.py` | Multi-criteria scoring |
| `pattern_evaluator.py` | Pattern-specific evaluation |
| `builtin_evaluators.py` | Standard evaluators |
| `config.py` | Configuration |
| `loader.py` | File loading |

#### `tools/llm/` (9 files)
**Purpose**: LLM client abstraction layer

| File | Purpose |
|------|---------|
| `llm_client.py` | Unified dispatcher for all providers |
| `local_model.py` | ONNX model runner |
| `windows_ai.py` | Windows Copilot Runtime (NPU) |
| `model_probe.py` | Model discovery |
| `model_inventory.py` | Model catalog |
| `model_locks.py` | Concurrency management |
| `windows_ai_bridge/` | C# bridge for Phi Silica |

#### `tools/core/` (10 files)
**Purpose**: Shared infrastructure

Files: `cache.py`, `config.py`, `errors.py`, `tool_init.py`, `response_cache.py`, `prompt_db.py`

#### `tools/archive/` (12+ files) - **DEPRECATED**
**Purpose**: Archived evaluation tools (replaced by `prompteval`)

| Item | Status | Recommendation |
|------|--------|----------------|
| `batch_evaluate.py` | Deprecated | Use `prompteval` |
| `tiered_eval.py` | Deprecated | Use `prompteval` |
| `evaluate_library.py` | Deprecated | Use `prompteval` |
| `run_eval_*.py` | Deprecated | Use `prompteval` |
| `enterprise_evaluator/` | Deprecated | Archive fully |

#### `tools/rubrics/` (7 files)
**Purpose**: Evaluation scoring criteria

| File | Purpose |
|------|---------|
| `prompt-scoring.yaml` | Main prompt rubric |
| `pattern-scoring.yaml` | Pattern-specific rubric |
| `unified-scoring.yaml` | Combined rubric |
| `quality_standards.json` | Quality thresholds |
| `judges/` | LLM judge prompts |
| `patterns/` | Pattern-specific criteria |

---

## Testing Directory

### Structure

```
testing/
├── unit/              # Unit tests
├── integration/       # Integration tests
├── evals/             # Evaluation test fixtures
├── tool_tests/        # Tool-specific tests
├── validators/        # Validator tests
├── framework/         # Test framework core
├── archive/           # Archived tests
├── conftest.py        # Pytest configuration
├── run_tests.py       # Test runner
├── README.md          # Testing documentation
├── requirements.txt   # Test dependencies
├── CONSOLIDATION_REPORT.md # Consolidation status
└── various test_*.py files
```

### Test Categories

| Directory | Purpose | Files |
|-----------|---------|-------|
| `unit/` | Unit tests | 4 files |
| `integration/` | Integration tests | 6 files |
| `tool_tests/` | Tool-specific tests | 7 files |
| `validators/` | Validation tests | 5 files |
| `evals/` | Evaluation fixtures | Multiple subdirs |
| `framework/` | Test framework | Core + validators |

### Issues Found

| File | Issue |
|------|-------|
| `import unittest.py` | **INCORRECT FILENAME** - Should be `test_dynamic_eval_manager.py` |
| `archive/` | Contains old test structures |

---

## Documentation Directory

### Structure

```
docs/
├── analysis/          # Research analysis outputs
├── concepts/          # Conceptual documentation
├── instructions/      # Copilot instructions files
├── planning/          # Planning documents
├── reference/         # Quick reference guides
├── research/          # Research outputs
├── tutorials/         # Learning tutorials
├── README.md          # Docs overview
├── REPO_ANALYSIS.md   # Previous analysis
├── PROMPT_TEMPLATE_STANDARD.md # Template standard
└── .gitignore         # Docs-specific ignores
```

### Subdirectory Details

#### `docs/reference/` (8 files)
Key files: `frontmatter-schema.md` (canonical), `cheat-sheet.md`, `TASKS_QUICK_REFERENCE.md`, `glossary.md`

#### `docs/planning/` (9 files)
Planning documents: `REPOSITORY_CLEANUP_ANALYSIS.md`, `VALIDATION_REMEDIATION_PLAN.md`, `REPO_UPDATE_TRACKING.md`

#### `docs/tutorials/` (6 files)
Learning resources: `first-prompt.md`, `building-effective-prompts.md`, `running-pattern-evaluation-locally.md`

#### `docs/concepts/` (6 files)
Theory: `about-prompt-engineering.md`, `prompt-anatomy.md`, `model-capabilities.md`

#### `docs/instructions/` (12 files)
Copilot instruction files for different roles/contexts

#### `docs/research/` (15 files)
Research outputs including CoVe analysis, library analysis, ReAct patterns

---

## Archive Directory

**Purpose**: Stores deprecated code and historical artifacts

### Structure

```
archive/
├── prompttools-deprecated/  # Old prompttools package
├── toolkit-backup/          # Backup of old toolkit
├── audit-files/             # Historical audit outputs
└── README.md                # Archive documentation
```

### Contents

#### `prompttools-deprecated/` (11 files)
The deprecated `prompttools` package (now use `tools/` instead):
- `cli.py`, `evaluate.py`, `llm.py`, `parse.py`, `validate.py`, `cache.py`, `config.py`
- `rubrics/` subdirectory

#### `toolkit-backup/` (3 files)
Old toolkit files: `QUICK_START.md`, `README.md`, `rubrics/`

#### `audit-files/` (3 files)
Historical audit outputs: `CoVE-Prompt-Library-Audit.md`, `reflection-data-pipeline-risk-review.md`

---

## Scripts Directory

**Purpose**: Utility scripts for evaluation and maintenance

### Contents

```
scripts/
├── prompteval/              # PromptEval scripts
├── FREE_TIER_EVALS.md       # Free evaluation guide
├── run-free-tier-evals.ps1  # PowerShell runner
└── run_free_tier_evals.py   # Python runner
```

---

## Data Directory

**Purpose**: Metadata schemas and learning tracks

### Structure

```
data/
├── db/                      # Database files (JSON)
│   ├── evaluations.json
│   ├── prompts.json
│   └── rubrics.json
├── learning-tracks/         # Learning path definitions
│   ├── architect-depth.yml
│   ├── engineer-quickstart.yml
│   └── functional-productivity.yml
├── audiences.yml            # Audience definitions
├── platforms.yml            # Platform definitions
├── topics.yml               # Topic taxonomy
└── README.md                # Data schema docs
```

---

## Workflows Directory

**Purpose**: Workflow templates and documentation

### Contents

```
workflows/
├── business-planning-blueprint.md
├── business-planning.md
├── data-pipeline.md
├── incident-response-playbook.md
├── incident-response.md
├── sdlc.md
└── README.md
```

---

## Reasoning Directory

**Purpose**: Reasoning pattern documentation

### Contents

```
reasoning/
├── chain-of-verification.md
└── README.md
```

---

## Multiagent Systems

### `multiagent-dev-system/`
**Purpose**: Multi-agent development system prototype

```
multiagent-dev-system/
└── src/
    └── multiagent_dev_system/
```

### `multiagent-workflows/`
**Purpose**: Complete multi-agent workflow system

```
multiagent-workflows/
├── config/          # Agent/model/workflow configs (YAML)
├── docs/            # Architecture documentation
├── evaluation/      # Evaluation datasets
├── examples/        # Example implementations
├── scripts/         # Utility scripts
├── src/             # Source code
├── tests/           # Test suite (8 files)
├── ui/              # Web UI
├── workflows/       # Workflow definitions (4 files)
├── pyproject.toml   # Package config
├── requirements.txt # Dependencies
└── README.md        # Overview
```

---

## GitHub Configuration

### `.github/` Structure

```
.github/
├── agents/           # GitHub Copilot agent definitions
├── instructions/     # Copilot instructions
├── workflows/        # CI/CD workflows
├── copilot-instructions.md
└── registry-schema.json
```

### Workflows (6 files)

| Workflow | Purpose |
|----------|---------|
| `dependency-review.yml` | Dependency security |
| `deploy.yml` | Deployment |
| `performance-benchmark.yml` | Performance testing |
| `prompt-quality-gate.yml` | Quality gates |
| `prompt-validation.yml` | Prompt validation |
| `validate-prompts.yml` | Additional validation |

### Agents (13 files)
Duplicates of `prompts/agents/` plus:

| File | Issue |
|------|-------|
| `prompt-agent.agent copy.md` | **DUPLICATE** - Needs removal |
| `my-agent.agent.md` | Test/placeholder agent |
| `docs-ux-agent.agent.md` | Additional agent variant |

---

## VS Code Configuration

### `.vscode/` Contents

| File | Purpose |
|------|---------|
| `extensions.json` | Recommended extensions |
| `launch.json` | Debug configurations |
| `mcp.json` | MCP configuration |
| `settings.json` | Workspace settings |
| `tasks.json` | VS Code tasks |

---

## Outdated Files to Remove

### **Priority 1: Immediate Cleanup (Broken/Duplicate)**

| Path | Issue | Action |
|------|-------|--------|
| `.github/agents/prompt-agent.agent copy.md` | Duplicate file with "copy" suffix | **DELETE** |
| `testing/import unittest.py` | Invalid filename (space in name) | **RENAME** to `test_dynamic_eval_manager.py` |
| `prompts/analysis/%% Mermaid radar chart illustrating samp.mmd` | Mermaid fragment, invalid filename | **DELETE** or move to assets |
| `promptevlas.json` | Typo in filename, generated output | **DELETE** |
| `.cleanup_manifest.json` | Empty cleanup manifest | **DELETE** |

### **Priority 2: Move to Archive (Generated/Temporary)**

| Path | Issue | Action |
|------|-------|--------|
| `prompteval-tier0.json` | Generated evaluation results | Move to `archive/outputs/` |
| `validation_issues_full.txt` | Generated validation report | Move to `archive/outputs/` |
| `analyze_missing.py` | One-time utility script | Move to `scripts/` or `archive/` |
| `update_progress_report.py` | One-time tracking script | Move to `scripts/` or `archive/` |

### **Priority 3: Deprecated Packages (Already Marked)**

| Path | Status | Notes |
|------|--------|-------|
| `archive/prompttools-deprecated/` | ✅ Already archived | Keep for reference |
| `archive/toolkit-backup/` | ✅ Already archived | Can delete after 90 days |
| `tools/archive/` | Contains deprecated eval tools | Review and consolidate |

### **Priority 4: Stale Archive Content**

| Path | Content | Action |
|------|---------|--------|
| `tools/archive/enterprise_evaluator/eval_log_*.jsonl` | Old eval logs (Dec 2025) | **DELETE** |
| `testing/archive/2025-12-04/` | Old test archive | Review and clean |

### **Priority 5: Duplicate/Redundant Documentation**

| Path | Issue |
|------|-------|
| Duplicate agents in `.github/agents/` vs `prompts/agents/` | Consider symlinks or single source |

---

## Validation Issues Summary

Based on `validation_issues_full.txt`, **137 prompt files** have validation issues:

### Issues by Category

| Category | Files with Issues | Common Problems |
|----------|-------------------|-----------------|
| Advanced | 14 | Missing Description, Prompt, Variables, Example sections |
| Agents | 11 | Missing all standard sections (agent format is different) |
| Analysis | 21 | Missing Description, Prompt sections |
| Business | 37 | Missing Description, Prompt, Example sections |
| Creative | 8 | Missing frontmatter fields |
| Developers | 12 | Missing Description, Variables sections |
| System | 16 | Missing Prompt section |
| Frameworks | 6 | Missing Description, Variables sections |
| Techniques | 12 | Missing standard sections |

### Most Common Issues

1. **Missing Description section** - 100+ files
2. **Missing Prompt section** - 80+ files
3. **Missing Variables section** - 90+ files
4. **Missing Example section** - 85+ files
5. **Missing frontmatter fields** (`name`, `description`, `type`) - 20+ files

---

## Recommendations

### Immediate Actions

1. **Delete broken files**:
   - `.github/agents/prompt-agent.agent copy.md`
   - `prompts/analysis/%% Mermaid radar chart illustrating samp.mmd`
   - `promptevlas.json`
   - `.cleanup_manifest.json`

2. **Rename invalid file**:
   - `testing/import unittest.py` → `testing/test_dynamic_eval_manager.py`

3. **Move root-level generated files**:
   - `prompteval-tier0.json` → `archive/outputs/`
   - `validation_issues_full.txt` → `archive/outputs/`

### Short-term Actions

1. **Consolidate agents**: Decide on single source for agents (`.github/agents/` or `prompts/agents/`)

2. **Clean archive logs**: Remove `tools/archive/enterprise_evaluator/eval_log_*.jsonl`

3. **Move utility scripts**: 
   - `analyze_missing.py` → `scripts/`
   - `update_progress_report.py` → `scripts/`

### Medium-term Actions

1. **Address validation issues**: Systematically fix the 137 prompt files with validation issues

2. **Documentation cleanup**: Ensure docs point to correct paths (many reference `tools/archive/` instead of canonical locations)

3. **Test coverage**: Add tests for newly consolidated tools

### Long-term Actions

1. **Remove deprecated packages**: After validation period, fully remove `archive/prompttools-deprecated/`

2. **Consolidate multiagent systems**: Merge `multiagent-dev-system/` and `multiagent-workflows/` if redundant

3. **Sparse category expansion**: Add more prompts to `creative/` category (only 2 files)

---

## Appendix: File Counts by Directory

| Directory | Files | Subdirectories |
|-----------|-------|----------------|
| `prompts/` | 30+ | 12 |
| `prompts/advanced/` | 28 | 0 |
| `prompts/agents/` | 12 | 0 |
| `prompts/analysis/` | 24 | 0 |
| `prompts/business/` | 16 | 0 |
| `prompts/creative/` | 2 | 0 |
| `prompts/developers/` | 29 | 0 |
| `prompts/frameworks/` | 2 | 4 |
| `prompts/m365/` | 3 | 0 |
| `prompts/socmint/` | 7 | 0 |
| `prompts/system/` | 24 | 0 |
| `prompts/techniques/` | 1 | 3 |
| `prompts/templates/` | 8 | 0 |
| `tools/` | 10 | 17 |
| `tools/prompteval/` | 16 | 0 |
| `tools/llm/` | 8 | 1 |
| `tools/archive/` | 12 | 1 |
| `testing/` | 15 | 8 |
| `docs/` | 5 | 7 |
| `archive/` | 1 | 3 |
| `multiagent-workflows/` | 5 | 9 |

---

*Analysis completed by automated repository scan. Manual review recommended for cleanup actions.*
