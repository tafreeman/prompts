# CLAUDE.md

This file provides guidance for AI assistants working with the **Enterprise AI Prompt Library** repository.

## Project Overview

This is a Python-based enterprise prompt engineering and multi-agent AI orchestration system. It contains:

- **196+ curated prompts** across 12 categories (developers, business, creative, analysis, advanced, system, governance, etc.)
- **Multi-agent orchestration engine** built on LangChain/LangGraph (`multiagent-workflows/`)
- **Next-gen agentic workflows** (`agentic-workflows-v2/`)
- **Unified tooling suite** for CLI, evaluation, validation, and LLM interaction (`tools/`)
- **Comprehensive test suite** with 103+ tests (`testing/`)

## Repository Structure

```
prompts/                        # Root of the repository
├── prompt.py                   # Main unified CLI entry point
├── conftest.py                 # Pytest configuration (async shim, .env loading)
├── pyproject.toml              # Project metadata, dependencies, entry points
├── requirements.txt            # Pinned dependencies
├── .pre-commit-config.yaml     # Formatting/linting hooks
├── .flake8                     # Flake8 configuration
├── pytest.ini                  # Pytest markers and test discovery
├── .env.example                # API key template (copy to .env)
│
├── prompts/                    # Prompt library (196+ markdown files)
│   ├── developers/             # Code-related prompts
│   ├── business/               # Business analysis prompts
│   ├── creative/               # Content creation prompts
│   ├── analysis/               # Data analysis prompts
│   ├── advanced/               # CoT, ReAct, RAG patterns
│   ├── system/                 # System-level agent prompts
│   ├── agents/                 # Copilot agent definitions
│   └── registry.yaml           # Central prompt registry
│
├── tools/                      # Unified tooling suite
│   ├── cli/                    # CLI commands (main.py = entry point)
│   ├── core/                   # Core utilities, errors, prompt_db
│   ├── llm/                    # LLM client (multi-provider)
│   ├── prompteval/             # Evaluation framework
│   ├── agents/                 # Agent implementations
│   ├── validators/             # Validation tools
│   ├── rubrics/                # Scoring rubrics (YAML/JSON)
│   ├── runners/                # Execution runners
│   └── scripts/                # Utility scripts
│
├── multiagent-workflows/       # Multi-agent orchestration (LangChain)
│   ├── src/multiagent_workflows/
│   │   ├── core/               # Workflow engine, model manager, agent base
│   │   ├── agents/             # 14+ specialized agents
│   │   ├── langchain/          # LangChain integration
│   │   ├── mcp/                # Model Context Protocol support
│   │   └── evaluation/         # Output evaluation
│   ├── config/                 # YAML configs (workflows, agents)
│   └── tests/                  # Workflow tests
│
├── agentic-workflows-v2/       # Next-gen orchestration engine
│   ├── src/agentic_v2/         # Source code (cli.py entry point)
│   └── pyproject.toml          # V2-specific config
│
├── testing/                    # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   ├── evals/                  # Evaluation tests
│   ├── framework/              # Test framework utilities
│   └── conftest.py             # Shared fixtures
│
├── docs/                       # Documentation
│   ├── concepts/               # Theory and understanding
│   ├── tutorials/              # Step-by-step guides
│   ├── reference/              # Quick lookup, glossary
│   ├── research/               # Research documentation
│   └── planning/               # Project planning docs
│
├── scripts/                    # Utility scripts
├── workflows/                  # Workflow definitions
│
└── .github/
    ├── workflows/              # CI/CD (9 workflow files)
    ├── agents/                 # Copilot custom agents
    └── instructions/           # Copilot instructions
```

## Build & Install

**Python version:** 3.9+ (CI uses 3.11)

```bash
# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Install with AI provider dependencies
pip install -e ".[ai]"

# Install everything
pip install -e ".[all]"
```

## Running Tests

```bash
# Run tests (skips slow tests by default)
pytest -q

# Run full test suite including slow tests (ONNX model loading)
pytest -m ""

# Run only slow tests
pytest -m slow

# Run specific test file
pytest testing/unit/test_pattern_evaluation.py

# Run with verbose output
pytest -v
```

**Key testing details:**
- Tests live in `testing/` (configured in both `pytest.ini` and `pyproject.toml`)
- Slow tests (ONNX model tests) are skipped by default via `addopts = -m "not slow"`
- `conftest.py` at root provides async test support without requiring pytest-asyncio
- `.env` file is auto-loaded by conftest for API keys

## Linting & Formatting

Pre-commit hooks enforce code quality. All are run in CI.

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Individual tools
black --line-length 88 .          # Code formatting
isort --profile black .           # Import sorting
ruff --fix .                      # Fast linting with auto-fix
mypy --ignore-missing-imports .   # Type checking
pydocstyle --convention=google .  # Docstring validation
```

**Code style rules:**
- **Black** formatting with 88-char line length
- **isort** with `black` profile for import ordering
- **Ruff** for linting with auto-fix enabled
- **mypy** for type checking (missing imports ignored)
- **pydocstyle** enforcing Google-style docstrings
- **docformatter** wrapping summaries at 79 chars
- **Flake8** max line length: 120 (separate from Black's 88)

## CI/CD

GitHub Actions workflows in `.github/workflows/`:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | push/PR to main, agenticv2 | Pre-commit hooks + pytest + docs build |
| `prompt-quality-gate.yml` | push/PR on prompts/ | Validate prompt score >= 75 |
| `prompt-validation.yml` | push/PR on prompts/ | YAML frontmatter validation |
| `validate-prompts.yml` | Manual | Full prompt validation |
| `dependency-review.yml` | PR | Vulnerable dependency check |
| `deploy.yml` | Release | Documentation deployment |

The main CI job runs: `pre-commit run --all-files` then `python -m pytest -q`.

## Prompt File Format

All prompts are Markdown files with YAML frontmatter:

```markdown
---
title: "Prompt Title"
description: "One-line summary"
category: "developers|business|creative|analysis|system|governance|advanced"
difficulty: "beginner|intermediate|advanced"
author: "Author Name"
version: "1.0"
date: "YYYY-MM-DD"
---

# Prompt Title

## Description
## Use Cases
## Prompt
## Variables
## Example Usage
## Tips
```

**Required frontmatter fields:** `title`, `description`, `category`, `difficulty`

**File naming:** lowercase-with-hyphens (e.g., `code-review-assistant.md`)

**Validation:** `python tools/validate_prompts.py` checks frontmatter and structure.

## Environment Variables

Copy `.env.example` to `.env` and fill in keys as needed:

- `GITHUB_TOKEN` - GitHub Models API access
- `OPENAI_API_KEY` - OpenAI API
- `ANTHROPIC_API_KEY` - Anthropic Claude API
- `AZURE_OPENAI_API_KEY` / `AZURE_OPENAI_ENDPOINT` - Azure OpenAI
- `LOCAL_MODEL_PATH` - Path to local ONNX models (optional, auto-detected)

The `.env` file is gitignored. Never commit API keys.

## Key Code Conventions

- **Async/await** used extensively with `asyncio` and `aiohttp`
- **Pydantic v2** for data validation and models
- **Google-style docstrings** enforced by pydocstyle
- **Type hints** throughout the codebase
- **YAML-driven configuration** for workflows and agents
- **Provider pattern** with unified interface for 8+ LLM providers and automatic fallbacks
- **Custom exception classes** in `tools/core/errors.py`
- **Structured logging** with verbose logger

## CLI Entry Points

```bash
prompt-tools    # General tools CLI (tools/cli/main.py)
prompteval      # Prompt evaluation CLI (tools/prompteval/__main__.py)
agentic         # Agentic workflows V2 CLI (agentic_v2.cli:main)
python prompt.py # Unified CLI entry point
```

## Architecture Notes

**Agent hierarchy:** `BaseAgent` (abstract) is extended by 14+ specialized agents (VisionAgent, AnalystAgent, ArchitectAgent, CoderAgent, ReviewerAgent, TestAgent, etc.)

**Model routing:** Smart router selects models with automatic fallback (Premium -> Mid-tier -> Local). Supports Anthropic Claude, OpenAI, GitHub Models, Google Gemini, Azure OpenAI, and local ONNX models (Phi-4, Phi-3.5, Mistral 7B).

**Workflow engine:** DAG-based orchestrator defined via YAML configs in `multiagent-workflows/config/`. Supports parallel step execution via `asyncio.gather()`.

## Common Tasks

```bash
# Validate all prompts
python tools/validate_prompts.py

# Check for broken links
python tools/check_links.py

# Run evaluation on prompts
prompteval

# Run the full CI checks locally
pre-commit run --all-files && pytest -q
```
