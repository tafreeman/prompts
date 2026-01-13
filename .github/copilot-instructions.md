# GitHub Copilot instructions for `prompts`

This repo is a **prompt-library + tooling** codebase (mostly Markdown + Python). Treat it like a docs/content repo: avoid introducing app/service scaffolding unless a task explicitly targets `app.prompts.library/`.

## Key areas (start here)

- `prompts/` — the actual prompt files (Markdown + YAML frontmatter)
- `templates/` — canonical templates (e.g., `templates/prompt-template.md`)
- `reference/frontmatter-schema.md` — **frontmatter contract** (required fields/allowed values)
- `docs/` — guidance and architecture (e.g., `docs/ARCHITECTURE_PLAN.md`, `docs/prompt-authorship-guide.md`)
- `tools/` — Python tooling (e.g., `tools/llm_client.py`, `tools/model_probe.py`, `tools/prompteval/`)
- `testing/` — pytest suite + evaluation fixtures

## Developer workflows that matter

- Prefer **VS Code Tasks** (see `TASKS_QUICK_REFERENCE.md`):
  - Validate: “🔍 Validate All Prompts”
  - Tests: “🧪 Run Python Tests”
  - Eval: “📊/📂 Eval …” (Tiered PromptEval runs)
- CLI equivalents used in this repo:
  - `python -m pytest testing/ -v`
  - `python tools/validators/frontmatter_validator.py --all`
  - From `tools/` cwd: `python -m prompteval ../prompts/<folder>/ --tier 2 --verbose --ci`

## Model + provider conventions (tooling)

- Models are addressed by prefixes in `tools/llm_client.py` / `tools/README.md`: `local:*`, `windows-ai:*`, `gh:*`, `azure-foundry:*`.
- Before any **batch** LLM run, probe availability and write `discovery_results.json`:
  - `python tools/model_probe.py --discover --force -o discovery_results.json`
- Cloud providers require env vars; use `.env.example` as the template (not hardcoded secrets). Typical: `GITHUB_TOKEN` for `gh:*`.

## Repo-specific authoring conventions

- Prompt files are Markdown with YAML frontmatter; keep filenames **lowercase-hyphenated** under the correct `prompts/<category>/`.
- Use placeholders as `[BRACKETED_VALUES]` and document every placeholder under the prompt’s “Variables” section (see `docs/prompt-authorship-guide.md`).

## When adding/updating Python tools

- Prefer `tools/tool_init.py` to enforce: fail-fast prereqs, UTF-8 console safety on Windows, progress + JSONL logging, and standardized error codes (see `tools/EXECUTION_GUIDELINES.md`).
- Keep imports as `from tools...` (the repo packages `tools` via `pyproject.toml`); avoid `sys.path` hacks.# GitHub Copilot / AI Agent Instructions for the `prompts` Repository

This file is the repository-specific guide for AI coding assistants (Copilot-style agents) that will author, refactor, and validate prompt templates and supporting documentation in this repo.

**High-level intent**: This repository is a curated prompt library and companion tooling. Agents should treat it as a docs/content repo (not a web app or service): focus on prompt content quality, adherence to frontmatter and template rules, discoverable patterns, and tooling for validating/exporting prompts.

---

## Quick Orientation

### Primary Content Locations

- `prompts/` — The actual prompt templates (organized by persona or domain)
- `docs/` — Standards, rationale, and guidance (especially `docs/PROMPT_STANDARDS.md`)
- `instructions/` — Per-role and per-style guidance
- `templates/` — Reusable prompt templates
- `tools/` — Python utilities for validation, evaluation, and model integration

### Key Tools

- `tools/llm_client.py` — Unified LLM dispatcher (all providers)
- `tools/model_probe.py` — Model discovery and availability checking
- `tools/local_model.py` — Local ONNX model runner
- `tools/prompteval/` — Unified prompt evaluation CLI

---

## MANDATORY: Model Checking Before LLM Operations

**ALWAYS check model availability before running any LLM operation:**

```python
# REQUIRED: Check model availability first
from tools.model_probe import is_model_usable, discover_all_models

# Quick check for single model
if not is_model_usable("gh:gpt-4o-mini"):
    print("ERROR: Model not available")
    # Fall back to local model or exit

# Full discovery (recommended before batch operations)
discovered = discover_all_models()
print(f"Available: {discovered['summary']['total_available']} models")
```

**CLI discovery command:**

```powershell
python tools/model_probe.py --discover --force -o discovery_results.json
```

---

## MANDATORY: Fail-Fast Pattern

All scripts MUST fail immediately on critical errors:

```python
import sys
import os
from pathlib import Path

def check_prerequisites():
    """Check all prerequisites before proceeding."""
    errors = []

    # Check environment variables
    if not os.getenv("GITHUB_TOKEN") and needs_github:
        errors.append("Missing GITHUB_TOKEN")

    # Check model availability
    from tools.model_probe import is_model_usable
    if not is_model_usable("local:phi4"):
        errors.append("Model 'local:phi4' not available")

    if errors:
        for e in errors:
            print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)
```

---

## MANDATORY: Iterative Logging

All batch operations MUST log progress immediately:

```python
import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("eval_log.jsonl")

def log_result(file: str, model: str, result: dict):
    """Append result immediately to log file."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "file": file,
        "model": model,
        **result
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        f.flush()  # Force write
```

---

## MANDATORY: Unicode/Encoding Handling

All scripts MUST handle Unicode safely (especially on Windows):

```python
import sys
import io
import os

# Add at top of every script that does console output
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, IOError):
        pass
```

---

## Common Issues & Solutions

### 1. Model Not Found

```powershell
# First, discover what's available
python tools/model_probe.py --discover -v

# Check local model cache
dir $HOME\.cache\aigallery
```

### 2. Unicode Errors

```powershell
# Set encoding
$env:PYTHONIOENCODING = "utf-8"
python -X utf8 your_script.py
```

### 3. GitHub Models 401/403

```powershell
# Check auth
gh auth status

# Re-authenticate
gh auth login
```

### 4. Ollama Connection Refused

```powershell
# Start Ollama
ollama serve

# Check models
ollama list
```

### 5. Rate Limiting (429)

```python
from tools.model_probe import classify_error

error_code, should_retry = classify_error(error_message)
if should_retry:
    time.sleep(60)  # Wait and retry
```

---

## Error Classification

Use standardized error codes:

| Code                | Meaning           | Retry? |
| ------------------- | ----------------- | ------ |
| `success`           | Completed         | N/A    |
| `unavailable_model` | Model not found   | NO     |
| `permission_denied` | Auth error        | NO     |
| `rate_limited`      | Too many requests | YES    |
| `timeout`           | Timed out         | YES    |
| `network_error`     | Connection failed | YES    |

---

## Tool Usage Examples

### Evaluate Prompts

```powershell
# Single file (FREE, local)
python -m prompteval prompts/example.md

# Folder with specific tier
python -m prompteval prompts/advanced/ --tier 2

# CI mode
python -m prompteval prompts/ --ci --threshold 70
```

### Validate Frontmatter

```powershell
python tools/validators/frontmatter_validator.py --all
```

### Generate Text

```python
from tools.llm_client import LLMClient

# Local (FREE)
response = LLMClient.generate_text("local:phi4", "Hello world")

# GitHub Models (FREE tier)
response = LLMClient.generate_text("gh:gpt-4o-mini", "Explain recursion")
```

### Chain-of-Verification

```powershell
python tools/cove_runner.py "What year was Python created?"
```

---

## Key Documentation

- `tools/TOOLS_OVERVIEW.md` — Complete tools suite documentation
- `tools/EXECUTION_GUIDELINES.md` — Mandatory execution patterns
- `tools/README.md` — Quick start guide
- `docs/PROMPT_STANDARDS.md` — Prompt authoring standards
- `docs/ARCHITECTURE_PLAN.md` — Architecture overview

---

## Key Rules

1. **Always check model availability** before LLM operations
2. **Fail fast** on missing prerequisites
3. **Log immediately** - don't buffer results
4. **Handle Unicode** with explicit UTF-8 encoding
5. **Use standardized error codes** for classification
6. **Show progress** for batch operations
7. **Support checkpoints** for long-running operations

---

## Repository Structure

```
prompts/
├── prompts/         # Prompt templates (main content)
├── docs/            # Documentation
├── tools/           # Python utilities
│   ├── llm_client.py      # Unified LLM dispatcher
│   ├── model_probe.py     # Model discovery
│   ├── local_model.py     # Local ONNX runner
│   ├── prompteval/        # Evaluation CLI
│   └── validators/        # Validation tools
├── templates/       # Prompt templates
└── testing/         # Test harness
```

Do not introduce code that converts this into a service or library; keep changes focused on content, tooling (Python scripts), docs, and CI/testing for the content pipeline.
