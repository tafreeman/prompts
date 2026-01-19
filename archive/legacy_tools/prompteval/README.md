# PromptEval - Easy, Robust Prompt Evaluation

A unified CLI tool for evaluating prompts across multiple models and methods.

**NEW in Phase 4:** Full support for `.prompt.yml` evaluation files! See [YAML Evaluation Guide](../../docs/YAML_EVALUATION.md).

## What It Does

PromptEval assesses prompt quality across six dimensions:

- **Clarity** - Clear, unambiguous instructions
- **Specificity** - Sufficient detail for consistent outputs
- **Actionability** - AI can determine what actions to take
- **Structure** - Well-organized with logical flow
- **Completeness** - Covers all necessary aspects
- **Safety** - Avoids harmful patterns or biases

**Scoring:** 0-100 scale with letter grades (A-F). Default pass threshold: 70%.

## Setup

```bash
# Clone and setup virtual environment
cd tools
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m prompteval --list-models
```

**Prerequisites:**
- Python 3.10+
- For cloud models: `GITHUB_TOKEN` environment variable
- For local models: ~2GB disk space (auto-downloads ONNX models)

## Quick Start

```bash
# Navigate to tools directory
cd tools

# Evaluate a directory (Tier 2 - Local G-Eval)
python -m prompteval ../prompts/advanced/

# Evaluate YAML evaluation files
python -m prompteval ../testing/evals/

# Evaluate a single file (Markdown or YAML)
python -m prompteval ../prompts/advanced/chain-of-thought-concise.md
python -m prompteval ../testing/evals/test-simple.prompt.yml

# Structural analysis only (instant, no LLM)
python -m prompteval ../prompts/ --tier 0

# Cross-model validation
python -m prompteval ../prompts/ --tier 3

# Specific models
python -m prompteval ../prompts/ --models phi4,mistral,gpt-4o-mini
```

## Supported Input Formats

- **Markdown** (`.md`): Traditional prompt library files with frontmatter
- **YAML** (`.prompt.yml`): GitHub Models-compatible evaluation files with multi-case testing

Both formats produce identical output schemas. See [YAML Evaluation Guide](../../docs/YAML_EVALUATION.md) for details.

## When to Use Which Tier

```
Quick validation?          → Tier 0 (structural, instant)
Iterating on prompt?       → Tier 1 (local quick, 30s)
Standard quality check?    → Tier 2 (G-Eval, recommended)
Pre-commit validation?     → Tier 3 (cross-validate, 5min)
Release candidate?         → Tier 4-5 (cloud validation)
Production/critical?       → Tier 6-7 (premium + enterprise)
```

## Tiers

| Tier | Name | Models | Cost | Time |
|------|------|--------|------|------|
| 0 | Structural | None (static analysis) | $0 | <1s |
| 1 | Local Quick | phi4 x1 | $0 | ~30s |
| 2 | Local G-Eval | phi4 x1 | $0 | ~60s |
| 3 | Local Cross | phi4, mistral, phi3.5 x2 | $0 | ~5min |
| 4 | Cloud Quick | gpt-4o-mini x1 | ~$0.01 | ~5s |
| 5 | Cloud Cross | 3 cloud models x2 | ~$0.10 | ~30s |
| 6 | Premium | 5 models x3 | ~$0.30 | ~2min |
| 7 | Enterprise | 5 models x4 | ~$0.50 | ~5min |

## 

### Example Output

```json
{
  "title": "Chain of Thought Reasoning",
  "tier": 2,
  "overall_score": 85.3,
  "grade": "B",
  "passed": true,
  "criteria": {
    "clarity": 90,
    "specificity": 85,
    "actionability": 88,
    "structure": 82,
    "completeness": 80,
    "safety": 87
  },
  "recommendations": [
    "Add example outputs for clarity",
    "Specify format requirements"
  ]
}
```Output Options

```bash
# JSON output
python -m prompteval ../prompts/ -o results.json

# Markdown report
python -m prompteval ../prompts/ -o report.md

# CI/CD mode (exit code 1 if failures)
python -m prompteval ../prompts/ --ci
```

## Options

```
python -m prompteval --help

Arguments:
  path                 Prompt file or directory

Options:
  -t, --tier {0-7}     Evaluation tier (default: 2)
  -m, --models         Comma-separated models (phi4,mistral,gpt-4o-mini)
  -r, --runs           Runs per model (overrides tier default)
  --threshold          Pass threshold in % (default: 70)
  -o, --output         Output file (.json or .md)
  -v, --verbose        Verbose output
  --ci                 CI mode: exit 1 if any failed
  --all-local          Use all local ONNX models
  -Common Workflows

### Development Workflow
```bash
# Quick check while editing
python -m prompteval prompt.md --tier 0 -v

# Test with local model
python -m prompteval prompt.md --tier 2

# Validate before commit
python -m prompteval prompts/new-feature/ --tier 3
```

### CI/CD Integration
```bash
# In your CI pipeline (GitHub Actions, etc.)
python -m prompteval prompts/ --tier 2 --ci --output results.json

# Pre-commit hook
python -m prompteval $(git diff --name-only --cached | grep '\.md$') --tier 1 --ci
```

### Batch Processing
```bash
# ETroubleshooting

### Model Not Found
```bash
# List available models
python -m prompteval --list-models

# Probe model availability
python -m prompteval prompts/ --verbose
```

### Local Models Slow/Failing
- **First run**: Models download automatically (~2GB), takes 5-10min
- **Performance**: Local models use CPU/ONNX. Tier 0 for instant feedback.
- **Memory**: Close other applications if running out of RAM

### Cloud Models Not Working
```bash
# Set GitHub token
export GITHUB_TOKEN=ghp_your_token_here  # Linux/Mac
$env:GITHUB_TOKEN="ghp_your_token_here"  # Windows PowerShell

# Verify token works
python -m prompteval --list-models
```

### Scores Seem Off
- **Too low**: Check threshold (default 70%). Try `--threshold 60`
- **Inconsistent**: Use higher tier (3+) for cross-validation
- **Need details**: Add `--verbose` flag to see per-criterion scores

### CI Mode Failing
```bash
# See what failed
python -m prompteval prompts/ --ci --verbose -o failures.json

# Lower threshold for initial adoption
python -m prompteval prompts/ --ci --threshold 60
```

## What This Replaces

PromptEval consolidates these tools:

| Old Tool | New Command |
|----------|-------------|
| `tiered_eval.py --tier N` | `prompteval --tier N` |
| `evaluate_library.py` | `prompteval DIR` |
| `run_eval_geval.py` | `prompteval --tier 2` |
| `batch_evaluate.py` | `prompteval DIR` |

## Further Reading

- [YAML Evaluation Guide](../../docs/YAML_EVALUATION.md) - GitHub Models-compatible eval files
- [Prompt Standards](../../docs/PROMPT_STANDARDS.md) - Quality guidelines
- [Scoring Methodology](../../docs/prompt-effectiveness-scoring-methodology.md) - How scores are calculated
- [Tools Reference](../../docs/tools-reference.md) - Complete tooling overview
from prompteval import evaluate, evaluate_directory

# Single file
result = evaluate("prompts/example.md", tier=2)
print(f"Score: {result.overall_score}% ({result.grade})")

# Directory
results = evaluate_directory("prompts/advanced/", tier=3)
for r in results:
    print(f"{r.title}: {r.avg_score}%")

# Custom configuration
from prompteval import PromptEval, EvalConfig

config = EvalConfig(tier=3, threshold=80.0, verbose=True)
evaluator = PromptEval(config=config)
result = evaluator.evaluate("prompt.md
| mistral | local:mistral |

### Cloud Models (require GITHUB_TOKEN)

| Shortname | Full Name |
|-----------|-----------|
| gpt-4o-mini | gh:gpt-4o-mini |
| gpt-4.1 | gh:gpt-4.1 |
| gpt-4o | gh:gpt-4o |
| llama-70b | gh:llama-3.3-70b-instruct |

## Python API

```python
from prompteval import evaluate, evaluate_directory

# Single file
result = evaluate("prompts/example.md", tier=2)
print(f"Score: {result.overall_score}% ({result.grade})")

# Directory
results = evaluate_directory("prompts/advanced/", tier=3)
for r in results:
    print(f"{r.title}: {r.avg_score}%")
```

## Architecture

PromptEval reuses existing infrastructure:

- `llm_client.py` - Multi-provider LLM dispatch
- `local_model.py` - Local ONNX model evaluation (G-Eval)
- `rubrics/prompt-scoring.yaml` - Scoring dimensions

This keeps the tool lean (~400 lines) while providing full functionality.

## What This Replaces

PromptEval consolidates these tools:

| Old Tool | New Command |
|----------|-------------|
| `tiered_eval.py --tier N` | `prompteval --tier N` |
| `evaluate_library.py` | `prompteval DIR` |
| `run_eval_geval.py` | `prompteval --tier 2` |
| `batch_evaluate.py` | `prompteval DIR` |
