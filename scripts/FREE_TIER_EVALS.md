# Free Tier Evaluation Scripts

Scripts for running prompt evaluations using **only free models** - local ONNX, Ollama, AI Toolkit, and GitHub Models (free tier).

## Quick Start

```powershell
# Quick evaluation with minimal models (fastest)
python scripts/run_free_tier_evals.py --quick --path prompts/analysis

# Full evaluation with all default free models
python scripts/run_free_tier_evals.py --path prompts/

# Use all discovered free models
python scripts/run_free_tier_evals.py --discovery --path prompts/

# Local only (no cloud/GitHub)
python scripts/run_free_tier_evals.py --local-only --path prompts/analysis
```

## Scripts

### `run_free_tier_evals.py` (Python)

Main evaluation script supporting multiple modes:

```
Usage: python scripts/run_free_tier_evals.py [OPTIONS]

Options:
  --path, -p PATH          Path to evaluate (default: prompts/)
  --tiers, -t TIERS        Tiers to run (default: 1 2)
  --models, -m MODELS      Specific models to use
  --discovery              Use all free models from discovery_results.json
  --max-per-provider N     Max models per provider with --discovery (default: 3)
  --quick                  Quick mode: minimal fast models
  --local-only             Only local models (no cloud)
  --no-gh                  Exclude GitHub Models
  --parallel N             Parallel evaluations (default: 1)
  --verbose, -v            Verbose output
  --output-dir, -o DIR     Output directory
  --dry-run                Show plan without executing
```

### `run-free-tier-evals.ps1` (PowerShell)

Windows-friendly wrapper with the same options:

```powershell
./scripts/run-free-tier-evals.ps1 -Path prompts/analysis -Quick
./scripts/run-free-tier-evals.ps1 -Discovery -MaxPerProvider 5
./scripts/run-free-tier-evals.ps1 -LocalOnly -Tiers 1,2
```

## Free Model Providers

| Provider | Prefix | Cost | Notes |
|----------|--------|------|-------|
| Local ONNX | `local:*` | Free | Requires AI Toolkit models downloaded |
| Ollama | `ollama:*` | Free | Requires Ollama server running |
| AI Toolkit | `aitk:*` | Free | VS Code AI Toolkit models |
| GitHub Models | `gh:*` | Free | Rate limited, requires `GITHUB_TOKEN` |

## Default Models

### Quick Mode (`--quick`)
- `local:phi4-cpu`
- `ollama:qwen3:8b`
- `gh:openai/gpt-4o-mini`

### Full Mode (default)
- **Local**: phi4-cpu, phi4-gpu, phi3.5-cpu
- **Ollama**: phi4-reasoning, qwen3:8b, deepseek-r1:8b
- **AI Toolkit**: phi-4-mini-reasoning, phi-4-mini-instruct
- **GitHub**: phi-4-mini-reasoning, gpt-4o-mini, llama-3.1-8b-instruct

## Prerequisites

1. **Local Models**: Download via AI Toolkit in VS Code
2. **Ollama**: Start server with `ollama serve`
3. **GitHub Models**: Set `GITHUB_TOKEN` environment variable

Check available models:
```bash
python -m tools.llm.model_probe --discover --force -o discovery_results.json
python -m tools.prompteval --list-models
```

## VS Code Tasks

New tasks available in the command palette (Ctrl+Shift+P → "Tasks: Run Task"):

- 🆓 **Free Tier Eval: Quick** - Fast evaluation with minimal models
- 🆓 **Free Tier Eval: Full Matrix** - All default free models
- 🆓 **Free Tier Eval: Discovery Mode** - All discovered free models
- 🆓 **Free Tier Eval: Local Only** - No cloud models
- 🆓 **Free Tier Eval: Parallel** - 2 concurrent workers

## Output

Results are saved to `results/free-tier-evals/<timestamp>/`:

```
results/free-tier-evals/20260121-143052/
├── summary.json                          # Session summary
├── analysis__tier1__local-phi4-cpu.json  # Individual run results
├── analysis__tier1__ollama-qwen3-8b.json
└── ...
```

## Examples

```powershell
# Evaluate a specific folder quickly
python scripts/run_free_tier_evals.py --quick --path prompts/developers

# Full evaluation with verbose output
python scripts/run_free_tier_evals.py --path prompts/ --verbose

# Parallel execution for faster results
python scripts/run_free_tier_evals.py --discovery --parallel 2

# Dry run to see what would execute
python scripts/run_free_tier_evals.py --discovery --dry-run

# Specific tiers and models
python scripts/run_free_tier_evals.py --tiers 1 2 3 --models local:phi4-cpu ollama:qwen3:8b
```
