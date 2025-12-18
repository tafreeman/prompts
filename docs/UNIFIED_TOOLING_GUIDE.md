# Unified Prompt Tooling Guide

> **One command to run, evaluate, and verify prompts across 8 providers**

---

## Quick Start

```bash
# Interactive mode - guided menu for all features
python prompt.py

# Or use direct commands:
python prompt.py run prompts/basic/greeting.md -p local     # Execute
python prompt.py eval prompts/advanced/ -t 2                 # Evaluate
python prompt.py cove "When was Python created?" -p github   # Verify
python prompt.py batch prompts/socmint/ -p local             # Batch
python prompt.py improve prompts/business/                   # Improve
python prompt.py models                                       # List models
python prompt.py tiers                                        # Show tiers
```

---

## Commands

### `run` - Execute a Prompt

```bash
python prompt.py run <file> [options]

Options:
  -p, --provider     Provider (default: local)
  -m, --model        Model name (default: provider-specific)
  -i, --input        Input text to pass to prompt
  -o, --output       Save response to file
  -s, --system       System prompt/instruction
  -v, --verbose      Show detailed output
  --temperature      Sampling temperature (default: 0.7)
  --max-tokens       Maximum tokens to generate (default: 2000)
```

**Parameter Reference:**

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `--temperature` | 0.7 | 0.0 - 2.0 | **0.0** = Deterministic (same output each time). **0.3-0.7** = Balanced (recommended for factual). **1.0+** = Creative/varied (stories, brainstorming). |
| `--max-tokens` | 2000 | 100 - 128000 | Maximum response length. Short tasks: 500. Long reports: 4000+. Note: local models may have lower limits. |
| `--system` | None | - | Prepends system instruction. Use for persona, constraints, or formatting rules. |

**Examples:**

```bash
# Basic execution (balanced temperature, 2000 tokens)
python prompt.py run prompts/analysis/gap-analysis.md -p local

# Factual/deterministic (temperature 0)
python prompt.py run prompts/code/review.md --temperature 0

# Creative/varied (high temperature)
python prompt.py run prompts/creative/story.md --temperature 1.2

# With persona via system prompt
python prompt.py run prompts/code/review.md -s "You are a senior security engineer"

# Long output
python prompt.py run prompts/report/analysis.md --max-tokens 8000
```

### `eval` - Evaluate Prompts

```bash
python prompt.py eval <path> [options]

Options:
  -t, --tier       0-6 (default: 2)
  -o, --output     Save results to file
  -f, --format     json or markdown
  -v, --verbose    Show detailed output
```

**Tiers:**

| Tier | Name | Cost | Time | Best For |
|------|------|------|------|----------|
| 0 | Local | Free | 30-60s | Development |
| 1 | Structural | Free | <1s | Quick filter |
| 2 | Single Model | Free | 15-45s | Validation |
| 3 | Cross-Validation | Free | 2-4m | Confidence |
| 4 | Full Pipeline | Free | 5-10m | Release |
| 5 | Premium | Free | 10-20m | Critical |
| 6 | Azure Foundry | $ | 15-30s | Production |
| 7 | Windows AI (NPU) | Free | 5-15s | Local + Fast |

**Examples:**

```bash
python prompt.py eval prompts/business/ -t 1           # Quick structure check
python prompt.py eval prompts/advanced/react.md -t 3   # Cross-validate
python prompt.py eval prompts/ -t 4 -o report.json     # Full eval with output
```

### `cove` - Chain-of-Verification

Reduces hallucinations by 50-60% through independent fact verification.

```bash
python prompt.py cove <question> [options]

Options:
  -p, --provider   local, github, azure, openai, claude, gemini
  -n, --questions  Number of verification questions (default: 5)
  -o, --output     Save result to file
```

**Examples:**

```bash
python prompt.py cove "When was Python created and by whom?"
python prompt.py cove "Explain microservices benefits" -p github
python prompt.py cove "What is RAG?" -p azure -n 10
```

### `batch` - Batch Processing

```bash
python prompt.py batch <folder> [options]

Options:
  -p, --provider   local, gh, azure
  -o, --output     Output directory
```

**Example:**

```bash
python prompt.py batch prompts/socmint/ -p local -o results/
```

### `improve` - Get Improvement Suggestions

```bash
python prompt.py improve <path> [options]

Options:
  -o, --output     Save recommendations to file
```

**Example:**

```bash
python prompt.py improve prompts/business/
```

### `models` - List Available Models

```bash
python prompt.py models
```

Shows all available models by provider:

- **Local ONNX (Free):** phi4mini, phi3.5, phi3, phi3-medium, mistral-7b
- **GitHub (Free):** gpt-4o-mini, gpt-4.1, gpt-4o, llama-3.3-70b
- **Azure Foundry ($):** Your deployed models
- **API (Paid):** OpenAI, Claude, Gemini

### `tiers` - Show Evaluation Tiers

```bash
python prompt.py tiers
```

---

## Providers

| Provider | Key | Cost | Setup |
|----------|-----|------|-------|
| **Local ONNX** | `local` | Free | Auto (from AI Gallery) |
| **GitHub Models** | `gh` | Free | `gh auth login` |
| **Azure Foundry** | `azure` | $ | Set `.env` endpoints |
| **OpenAI** | `openai` | $ | Set `OPENAI_API_KEY` |
| **Ollama** | `ollama` | Free | Install Ollama |
| **Claude** | `claude` | $ | Set `ANTHROPIC_API_KEY` |
| **Gemini** | `gemini` | $ | Set `GOOGLE_API_KEY` |
| **Windows AI** | `windows` | Free | Windows 11 only |

---

## Environment Setup

### Quick Setup (Recommended)

```bash
# 1. Local ONNX models (auto-detected from Windows AI Gallery)
# No setup needed if you have models in ~/.cache/aigallery/

# 2. GitHub Models (free tier)
gh auth login
gh extension install github/gh-models

# 3. Core dependencies
pip install pyyaml
```

### Full Setup (.env file)

```bash
# Required for GitHub Models
GITHUB_TOKEN=your_github_pat_token

# Optional - Azure Foundry
AZURE_FOUNDRY_API_KEY=your_key
AZURE_FOUNDRY_ENDPOINT_1=https://your-endpoint/openai/deployments/phi4mini
AZURE_FOUNDRY_ENDPOINT_2=https://your-endpoint/openai/deployments/mistral

# Optional - Paid APIs
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

---

## Workflows

### Development (Free, Fast)

```bash
# 1. Write prompt
code prompts/my-prompt.md

# 2. Quick structure check
python prompt.py eval prompts/my-prompt.md -t 1

# 3. Local model test
python prompt.py run prompts/my-prompt.md -p local
```

### Before Commit

```bash
# Single model validation
python prompt.py eval prompts/my-prompt.md -t 2
```

### PR/Release

```bash
# Cross-validation with multiple models
python prompt.py eval prompts/changed-prompt.md -t 4 -o pr-report.md
```

### Full Library Audit

```bash
# 1. Batch analyze
python prompt.py batch prompts/ -p local

# 2. Get improvement suggestions
python prompt.py improve prompts/

# 3. Generate report
python prompt.py eval prompts/ -t 2 -o audit.json
```

### Production (Azure Foundry)

```bash
# 1. Set endpoints in .env
# 2. Execute or evaluate
python prompt.py run prompts/production/critical.md -p azure
python prompt.py eval prompts/production/ -t 6
```

---

## Advanced: Direct Tool Access

For power users, individual tools can be called directly:

| Tool | Command |
|------|---------|
| Local model | `python tools/local_model.py --prompt "..."` |
| Tiered eval | `python tools/tiered_eval.py --tier 3 path/` |
| CoVe | `python tools/cove_runner.py "question" --provider github` |
| Batch CoVe | `python tools/cove_batch_analyzer.py --provider local` |
| Dual eval | `python testing/evals/dual_eval.py file.md` |
| Improve | `python tools/improve_prompts.py --all` |
| Audit | `python tools/audit_prompts.py prompts/ --output audit.csv` |

---

## Related Documentation

- [CoVE Reflexion Methodology](../CoVE%20Reflexion%20Prompt%20Library%20Evaluation.md)
- [Research Reports](research/)
- [Testing Framework](../testing/README.md)

---

*Last updated: 2025-12-16*
