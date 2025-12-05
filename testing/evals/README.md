# 🔬 Prompt Evaluation with GitHub Models

This directory contains the **primary evaluation tool** for the prompt library using GitHub Models (`gh models eval`).

> **📋 Architecture**: See [ARCHITECTURE_PLAN.md](../../docs/ARCHITECTURE_PLAN.md) for the complete evaluation architecture.

## Prerequisites

1. **GitHub CLI** - Install from [cli.github.com](https://cli.github.com/)
2. **gh-models extension** - Install with:
   ```bash
   gh extension install github/gh-models
   ```
3. **Authentication** - Login with `gh auth login`
4. **Python 3.10+** with `pyyaml` installed

## Quick Start

### Evaluate prompts with `dual_eval.py`

```bash
# Evaluate a single prompt
python testing/evals/dual_eval.py prompts/developers/code-review.md

# Evaluate all prompts in a folder (recursive)
python testing/evals/dual_eval.py prompts/developers/

# Evaluate with JSON output for CI/CD
python testing/evals/dual_eval.py prompts/ --format json --output report.json

# Evaluate only changed files (for PR validation)
python testing/evals/dual_eval.py prompts/ --changed-only

# Use specific models with fewer runs
python testing/evals/dual_eval.py prompts/advanced/ --models openai/gpt-4o --runs 2

# Glob pattern support
python testing/evals/dual_eval.py "prompts/**/*.md" --format json

# Real-time logging to markdown
python testing/evals/dual_eval.py prompts/ --log-file eval.md

# Fast evaluation (skip model validation)
python testing/evals/dual_eval.py prompts/developers/ --skip-validation
```

## Primary Tool: `dual_eval.py`

Multi-model prompt evaluation with cross-validation and batch support.

### Features

- **Batch evaluation**: Evaluate entire folders or glob patterns
- **Smart filtering**: Automatically excludes non-prompt files (agents, instructions, README, index)
- **Multi-model evaluation**: Run same prompt against multiple models
- **Cross-validation**: Detects score variance between models
- **JSON output**: Machine-readable format for CI/CD pipelines
- **Changed-only mode**: Evaluate only git-modified files (for PRs)
- **Real-time logging**: Markdown file updated after each evaluation
- **8-dimension rubric**: Comprehensive quality assessment
- **Pass/fail grading**: Clear thresholds with exit codes

### File Filtering

By default, the tool automatically excludes non-prompt files:

| Excluded | Examples |
|----------|----------|
| README/index files | `README.md`, `index.md`, `CHANGELOG.md` |
| Agent files | `*.agent.md` |
| Instruction files | `*.instructions.md` |
| Archive directories | Files in `archive/`, `.git/`, etc. |

Use `--include-all` to override this filtering and evaluate all `.md` files.

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `paths` | File(s), folder(s), or glob patterns | Required |
| `--format`, `-f` | Output format: `markdown` or `json` | `markdown` |
| `--output`, `-o` | Output file path | Auto-generated |
| `--models`, `-m` | Space-separated model list | 5 default models |
| `--runs`, `-r` | Number of runs per model | 4 |
| `--changed-only` | Only evaluate git-changed files | False |
| `--base-ref` | Git ref for `--changed-only` | `origin/main` |
| `--skip-validation` | Skip model availability check | False |
| `--include-all` | Include all .md files (no filtering) | False |
| `--log-file` | Real-time markdown log file | None |
| `--max-workers` | Parallel execution (1=sequential) | 1 |
| `--no-recursive` | Don't search directories recursively | False |
| `--quiet`, `-q` | Suppress per-file output | False |

### Default Models

- `openai/gpt-4.1`
- `openai/gpt-4o`
- `openai/gpt-4o-mini`
- `mistral-ai/mistral-small-2503`
- `meta/llama-3.3-70b-instruct`

## Evaluation Criteria

Prompts are evaluated on **8 criteria** (scored 1-10):

| Criterion | Description |
|-----------|-------------|
| **Clarity** | How clear and unambiguous are the instructions? |
| **Specificity** | Does it provide enough detail for consistent outputs? |
| **Actionability** | Can the AI clearly determine what actions to take? |
| **Structure** | Is it well-organized with clear sections? |
| **Completeness** | Does it cover all necessary aspects? |
| **Factuality** | Are any claims/examples accurate? |
| **Consistency** | Will it produce reproducible outputs? |
| **Safety** | Does it avoid harmful patterns? |

## Pass/Fail Thresholds

```
✅ PASS: Overall score >= 7.0 AND no individual criterion < 5.0
         AND cross-validation variance <= 1.5
❌ FAIL: Overall score < 7.0 OR any criterion < 5.0
         OR cross-validation variance > 1.5
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All evaluated prompts passed |
| 1 | One or more prompts failed |
| 2 | Usage error (invalid arguments, no files found) |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| A | 8.5-10 | Excellent - production ready |
| B | 7.0-8.4 | Good - minor improvements possible |
| C | 5.5-6.9 | Average - several areas need work |
| D | 4.0-5.4 | Below Average - significant rework needed |
| F | <4.0 | Fails - major issues, not usable |

## Example Output

```
📊 EVALUATION RESULTS: code-review.md
======================================================================

Model: openai/gpt-4.1 (Run 1 of 1)
   Score: 8.7/10 (Grade: A) ✅ PASS
   clarity: 9 | specificity: 8 | actionability: 9 | structure: 9
   completeness: 8 | factuality: 9 | consistency: 9 | safety: 9

Model: meta/llama-3.3-70b-instruct (Run 1 of 1)
   Score: 8.5/10 (Grade: A) ✅ PASS
   clarity: 8 | specificity: 9 | actionability: 8 | structure: 9
   completeness: 8 | factuality: 9 | consistency: 8 | safety: 9

----------------------------------------------------------------------
📈 CROSS-VALIDATION
----------------------------------------------------------------------
   Score Range: 8.5 - 8.7 (variance: 0.2) ✅
   Consensus: PASS
```

## Unit Tests

54 unit tests validate the evaluation framework:

```bash
# Run all tests
pytest testing/evals/test_dual_eval.py -v

# Run specific test class
pytest testing/evals/test_dual_eval.py::TestCrossValidate -v

# Run new feature tests
pytest testing/evals/test_dual_eval.py::TestDiscoverPromptFiles -v
pytest testing/evals/test_dual_eval.py::TestJsonReport -v
```

## Files

| File | Description |
|------|-------------|
| `dual_eval.py` | **Primary evaluation tool** |
| `test_dual_eval.py` | Unit tests (54 tests) |
| `results/` | Evaluation output storage |
| `analysis/` | Analysis eval files |

## CI/CD Integration

### Basic PR Evaluation

```yaml
name: Evaluate Prompts

on:
  pull_request:
    paths:
      - 'prompts/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for --changed-only
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: pip install pyyaml pytest
      
      - name: Install gh-models
        run: gh extension install github/gh-models
        env:
          GH_TOKEN: ${{ github.token }}
      
      - name: Evaluate changed prompts
        run: |
          python testing/evals/dual_eval.py prompts/ \
            --changed-only \
            --format json \
            --output eval-results.json \
            --runs 1
        env:
          GH_TOKEN: ${{ github.token }}
      
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: evaluation-results
          path: eval-results.json
```

### Full Library Evaluation

```yaml
name: Full Library Evaluation

on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday

jobs:
  evaluate-all:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: pip install pyyaml
      
      - name: Install gh-models
        run: gh extension install github/gh-models
        env:
          GH_TOKEN: ${{ github.token }}
      
      - name: Evaluate all prompts
        run: |
          python testing/evals/dual_eval.py prompts/ \
            --format json \
            --output full-eval.json \
            --quiet
        env:
          GH_TOKEN: ${{ github.token }}
      
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: full-evaluation
          path: full-eval.json
```

## Available Models

List available models:
```bash
gh models list
```

Common options:
- `openai/gpt-4.1` - Latest GPT-4 (recommended)
- `openai/gpt-4o` - Fast GPT-4
- `openai/gpt-4o-mini` - Fastest/cheapest
- `meta/llama-3.3-70b-instruct` - Open source
- `mistral-ai/mistral-small-2503` - Mistral alternative

## Troubleshooting

### Rate Limiting
If you hit rate limits, use sequential mode (default):
```bash
python testing/evals/dual_eval.py prompts/ --max-workers 1
```

### Authentication Issues
```bash
gh auth login
gh auth status
```

### Model Not Available
Check model availability:
```bash
gh models view openai/gpt-4.1
```

## See Also

- [ARCHITECTURE_PLAN.md](../../docs/ARCHITECTURE_PLAN.md) - Complete architecture
- [tools/README.md](../../tools/README.md) - Auxiliary tools
- [COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md) - Scoring methodology
