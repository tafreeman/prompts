---
title: Tools Suite Overview
shortTitle: Tools Overview
intro: Quick reference and navigation guide for the prompts tools ecosystem.
type: reference
difficulty: intermediate
audience:
- senior-engineer
- junior-engineer
- ai-agent
platforms:
- github-copilot
- claude
- chatgpt
author: Prompts Library Team
version: '2.0'
date: '2026-01-06'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: approved
---

# Tools Suite Overview

Quick reference guide for the prompts tools ecosystem. Each tool has detailed documentation linked below.

---

## 🚀 Quick Start (6 Most Common Commands)

```powershell
# 1. Check what models are available (DO THIS FIRST)
python tools/model_probe.py --discover -v

# 2. Run a prompt with local model (FREE)
python prompt.py run prompts/example.md -p local -m phi4

# 3. Evaluate prompts (FREE, local G-Eval, with parallel)
python -m prompteval prompts/advanced/ --tier 2 --parallel 4

# 4. Validate all prompt frontmatter
python tools/validators/frontmatter_validator.py --all

# 5. Generate an image locally (FREE)
python tools/local_media.py image "A sunset over mountains" -o sunset.png

# 6. Manage LLM response cache
python tools/cache.py --stats    # View cache statistics
python tools/cache.py --clear    # Clear all cached responses
```

---

## 📁 Architecture

```
tools/
├── 🔧 CORE INFRASTRUCTURE
│   ├── llm_client.py              → Unified LLM dispatcher (with caching)
│   ├── local_model.py             → ONNX model runner
│   ├── model_probe.py             → Model discovery/availability
│   ├── cache.py                   → LLM response caching (NEW)
│   ├── errors.py                  → Standardized error codes
│   ├── _encoding.py               → Windows encoding fix
│   └── windows_ai.py              → NPU integration
│
├── 📊 EVALUATION
│   ├── prompteval/                → prompteval/README.md (with --parallel)
│   ├── enterprise_evaluator/      → Enterprise evaluation framework
│   ├── evaluation_agent.py        → Autonomous evaluation agent
│   ├── run_lats_improvement.py    → LATS self-refinement
│   └── cove_runner.py             → Chain-of-Verification
│
├── ✅ VALIDATION
│   └── validators/                → Frontmatter, links, scores
│
├── 🔍 ANALYSIS
│   ├── analyzers/                 → Prompt analysis tools
│   └── improve_prompts.py         → AI-driven improvements
│
├── 🎨 MEDIA
│   └── local_media.py             → Stable Diffusion, Whisper
│
└── 📄 DOCUMENTATION
    ├── TOOLS_OVERVIEW.md          ← You are here
    ├── EXECUTION_GUIDELINES.md    → Mandatory patterns
    └── docs/                      → Detailed tool docs
```

---

## ⚡ Tool Quick Reference

### Core Infrastructure

| Tool | Purpose | Quick Command | Docs |
|------|---------|---------------|------|
| `llm_client.py` | Unified LLM dispatcher | `python prompt.py run <file> -p local -m phi4` | [📄](./docs/llm-client.md) |
| `local_model.py` | Direct ONNX interface | `python tools/local_model.py --model phi4 "Hello"` | [📄](./docs/local-model.md) |
| `model_probe.py` | Model availability | `python tools/model_probe.py --discover` | [📄](./docs/model-probe.md) |
| `windows_ai.py` | Windows AI / NPU | `python prompt.py run <file> -p windows` | [📄](./WINDOWS_AI_README.md) |

### Evaluation

| Tool | Purpose | Quick Command | Docs |
|------|---------|---------------|------|
| `prompteval/` | ⭐ Unified evaluation | `python -m prompteval prompts/` | [📄](./prompteval/README.md) |
| `enterprise-evaluator/` | Batch multi-model | `cd enterprise-evaluator && python main.py` | [📄](./enterprise-evaluator/README.md) |
| `evaluation_agent.py` | Autonomous agent | `python tools/evaluation_agent.py --category advanced` | [📄](./docs/evaluation-agent.md) |
| `run_lats_improvement.py` | LATS Self-Refine | `python tools/run_lats_improvement.py prompts/` | [📄](./docs/lats-improvement.md) |
| `cove_runner.py` | Chain-of-Verification | `python tools/cove_runner.py "Question?"` | [📄](./docs/cove-runner.md) |

### Validation & Analysis

| Tool | Purpose | Quick Command | Docs |
|------|---------|---------------|------|
| `frontmatter_validator.py` | YAML validation | `python tools/validators/frontmatter_validator.py --all` | [📄](./docs/validators.md) |
| `prompt_analyzer.py` | 5-dimension scoring | `python tools/analyzers/prompt_analyzer.py prompts/` | [📄](./docs/analyzers.md) |
| `improve_prompts.py` | AI improvements | `python tools/improve_prompts.py prompts/ --worst 10` | [📄](./docs/analyzers.md) |
| `check_links.py` | Link integrity | `python tools/check_links.py docs/` | [📄](./docs/validators.md) |

### Media

| Tool | Purpose | Quick Command | Docs |
|------|---------|---------------|------|
| `local_media.py` | Image/Audio/Upscale | `python tools/local_media.py image "prompt" -o out.png` | [📄](./docs/local-media.md) |

---

## 🏷️ Model Prefixes

| Prefix | Provider | Cost | Example |
|--------|----------|------|---------|
| `local:*` | Local ONNX | $0 | `local:phi4` |
| `windows-ai:*` | Windows AI (NPU) | $0 | `windows-ai:phi-silica` |
| `gh:*` | GitHub Models | FREE tier | `gh:gpt-4o-mini` |
| `ollama:*` | Ollama | $0 | `ollama:deepseek-r1:14b` |
| `azure-foundry:*` | Azure Foundry | Pay-per-use | `azure-foundry:phi4` |
| `openai:*` | OpenAI | Paid | `openai:gpt-4o` |

---

## 🎯 Evaluation Tiers

| Tier | Name | Models | Cost | Use Case |
|------|------|--------|------|----------|
| 0 | Structural | None | $0 | Quick syntax check |
| 1 | Local Quick | phi4 | $0 | Fast local scoring |
| 2 | Local G-Eval | phi4 + mistral | $0 | CoT reasoning (default) |
| 3 | Cross-Model | gpt-4o-mini + local | $$$ | Production validation |
| 4 | Full Suite | 5+ models | $$$$ | Publication release |

```powershell
# Examples
python -m prompteval prompts/ -t 0    # Structural only
python -m prompteval prompts/ -t 2    # Local G-Eval (FREE)
python -m prompteval prompts/ -t 3    # Cross-model
```

---

## 🔧 Environment Setup

```powershell
# GitHub Models (FREE tier)
$env:GITHUB_TOKEN = "your-token"

# OpenAI (Paid)
$env:OPENAI_API_KEY = "sk-..."

# Azure
$env:AZURE_OPENAI_ENDPOINT = "https://..."
$env:AZURE_OPENAI_API_KEY = "..."

# Fix encoding issues (Windows)
$env:PYTHONIOENCODING = "utf-8"
```

---

## 🔥 Common Issues

| Issue | Quick Fix |
|-------|-----------|
| Model not found | `python tools/model_probe.py --discover` |
| 401 Unauthorized (GitHub) | `gh auth login` |
| Connection refused (Ollama) | `ollama serve` |
| Unicode errors | `$env:PYTHONIOENCODING = "utf-8"` |
| ONNX not installed | `pip install onnxruntime-genai` |
| Windows AI access denied | Apply at <https://aka.ms/phi-silica-unlock> |

**For detailed troubleshooting, see [EXECUTION_GUIDELINES.md](./EXECUTION_GUIDELINES.md)**

---

## 📚 Detailed Documentation

### By Category

| Category | Documentation |
|----------|---------------|
| **Core LLM Integration** | [llm-client.md](./docs/llm-client.md) · [local-model.md](./docs/local-model.md) |
| **Model Discovery** | [model-probe.md](./docs/model-probe.md) |
| **Evaluation** | [prompteval/README.md](./prompteval/README.md) · [evaluation-agent.md](./docs/evaluation-agent.md) · [lats-improvement.md](./docs/lats-improvement.md) |
| **Validation** | [validators.md](./docs/validators.md) |
| **Analysis** | [analyzers.md](./docs/analyzers.md) |
| **Media** | [local-media.md](./docs/local-media.md) |
| **Fact-Checking** | [cove-runner.md](./docs/cove-runner.md) |
| **Windows AI** | [WINDOWS_AI_README.md](./WINDOWS_AI_README.md) |

### Execution & Best Practices

- [EXECUTION_GUIDELINES.md](./EXECUTION_GUIDELINES.md) - **Mandatory patterns for all tool execution**
- [README.md](./README.md) - Quick start guide
- [tests_README.md](./tests_README.md) - Test documentation

### Architecture & Planning

- [../docs/ARCHITECTURE_PLAN.md](../docs/ARCHITECTURE_PLAN.md) - Architecture overview
- [../docs/UNIFIED_TOOLING_GUIDE.md](../docs/UNIFIED_TOOLING_GUIDE.md) - Complete tooling guide

---

## 📂 Cache Locations

| Cache | Location |
|-------|----------|
| AI Gallery (ONNX) | `~/.cache/aigallery/` |
| AI Toolkit | `~/.aitk/models/` |
| Model Probes | `~/.cache/prompts-eval/model-probes/` |
| Ollama | `~/.ollama/models/` |
