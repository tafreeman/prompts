# PromptEval - Easy, Robust Prompt Evaluation

A unified CLI tool for evaluating prompts across multiple models and methods.

**NEW in Phase 4:** Full support for `.prompt.yml` evaluation files! See [YAML Evaluation Guide](../../docs/YAML_EVALUATION.md).

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

## Output Options

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
  --all-cloud          Use all GitHub Models
  --list-models        Show available models
  --list-tiers         Show tier configurations
```

## Models Available

### Local Models (FREE - no API key needed)

| Shortname | Full Name |
|-----------|-----------|
| phi4, phi4mini | local:phi4mini |
| phi3, phi3.5 | local:phi3.5 |
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
