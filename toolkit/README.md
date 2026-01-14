---
title: "Prompt Library Toolkit"
shortTitle: "Toolkit"
intro: "Unified command center for all library improvement, validation, and testing capabilities."
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
version: '1.0'
date: '2025-12-18'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: approved
---

# 🛠️ Prompt Library Toolkit

> **Your single entry point** for all library improvement, validation, evaluation, and execution capabilities.

---

## ⚡ One-Click Execution Matrix

Copy-paste these commands. Replace `<file>` with a prompt path (e.g., `prompts/basic/greeting.md`) and `<dir>` with a directory.

### **Text Generation**

| Use Case | Command | Best Model |
|----------|---------|------------|
| Fastest Local | `python prompt.py run <file> -p local -m phi4-cpu` | `phi4-cpu` |
| NPU (Copilot+ PC) | `python prompt.py run <file> -p windows` | `phi-silica` |
| GPU Accelerated | `python prompt.py run <file> -p local -m phi3-dml` | `phi3-dml` |
| Cloud (GitHub) | `python prompt.py run <file> -p gh -m gpt-4o-mini` | `gpt-4o-mini` |

### **Evaluation & Validation**

| Use Case | Command | Tier/Cost |
|----------|---------|-----------|
| Local Triage | `python prompt.py eval <dir> -t 0` | Tier 0 / $0 |
| NPU Eval | `python prompt.py eval <dir> -t 7` | Tier 7 / $0 |
| Cross-Model | `python prompt.py eval <dir> -t 3` | Tier 3 / ~$0.05 |
| Fact-Check (CoVe) | `python prompt.py cove "<question>"` | Local or Cloud |
| Batch CoVe | `python tools/cove_batch_analyzer.py <dir>` | Varies |
| Schema Validation | `python tools/validators/frontmatter_validator.py --all` | N/A |
| Audit Prompts | `python tools/audit_prompts.py <dir>` | N/A |

### **Improvement & Generation**

| Use Case | Command | Notes |
|----------|---------|-------|
| Improve Prompt | `python prompt.py improve <file>` | AI-powered recommendations |
| Generate Prompt | Use `/generate-prompt` workflow | Slash command in Copilot |
| Refactor Library | Use `prompt-library-refactor-react.md` | ReAct pattern |

### **Multi-Modal (Local)**

| Use Case | Command | Model |
|----------|---------|-------|
| Generate Image | `python tools/local_media.py image "<prompt>" -o out.png` | `stable-diffusion` |
| Speech-to-Text | `python tools/local_media.py transcribe <audio.wav>` | `whisper-small` |
| Upscale Image | `python tools/local_media.py upscale <image.png>` | `esrgan` |

---

## 🤖 Agents & Workflows

### **Slash Commands (Workflows)**

| Command | Purpose | Path |
|---------|---------|------|
| `/generate-prompt` | AI-assisted prompt generation with review loop | `.agent/workflows/generate-prompt.md` |
| `/improve-prompt` | Quality evaluation & automated improvement | `.agent/workflows/improve-prompt.md` |

### **GitHub Copilot Agents**

| Agent | Purpose | Path |
|-------|---------|------|
| `@prompt_agent` | Prompt engineering expert | `agents/prompt-agent.agent.md` |
| `@docs_agent` | Documentation specialist | `agents/docs-agent.agent.md` |
| `@test_agent` | Test generation | `agents/test-agent.agent.md` |
| `@refactor_agent` | Code improvement | `agents/refactor-agent.agent.md` |
| `@code_review_agent` | PR reviews | `agents/code-review-agent.agent.md` |

---

## 📊 Meta-Prompts for Library Operations

### **Quality Evaluation**

| Prompt | Path | Purpose |
|--------|------|---------|
| Prompt Quality Evaluator | `toolkit/prompts/evaluation/quality-evaluator.md` | Score prompts on 5 dimensions |
| CoVe Library Audit | `toolkit/prompts/evaluation/cove-library-audit.md` | Chain-of-Verification audit |
| Tree-of-Thoughts Evaluator | `toolkit/prompts/evaluation/tree-of-thoughts-evaluator.md` | Multi-branch reasoning |

### **Library Analysis**

| Prompt | Path | Purpose |
|--------|------|---------|
| Library Treemap | `toolkit/prompts/analysis/library-treemap.md` | Visualize structure |
| Library Radar | `toolkit/prompts/analysis/library-radar.md` | Capability radar chart |
| Library Network | `toolkit/prompts/analysis/library-network.md` | Relationship graph |

### **Improvement**

| Prompt | Path | Purpose |
|--------|------|---------|
| Refactor (ReAct) | `toolkit/prompts/improvement/refactor-react.md` | ReAct-based refactoring |
| Self-Critique | `toolkit/prompts/improvement/self-critique.md` | Iterative self-improvement |

---

## 📦 Python Tools Reference

### **Core Execution**

| Tool | Path | Purpose |
|------|------|---------|
| `llm_client.py` | `tools/llm_client.py` | Unified LLM dispatcher (28 models) |
| `local_model.py` | `tools/local_model.py` | ONNX model runner |
| `windows_ai.py` | `tools/windows_ai.py` | NPU integration |
| `local_media.py` | `tools/local_media.py` | Image/audio tools |

### **Evaluation**

| Tool | Path | Purpose |
|------|------|---------|
| `prompteval` | `tools/prompteval/` | Unified evaluation CLI (replaces `tiered_eval.py`) |
| `cove_runner.py` | `tools/cove_runner.py` | Chain-of-Verification |
| `batch_evaluate.py` | `tools/batch_evaluate.py` | Batch evaluation (legacy — prefer `prompteval`) |
| `evaluation_agent.py` | `tools/evaluation_agent.py` | Autonomous eval agent |

### **Validation**

| Tool | Path | Purpose |
|------|------|---------|
| `frontmatter_validator.py` | `tools/validators/frontmatter_validator.py` | Schema validation |
| `audit_prompts.py` | `tools/audit_prompts.py` | Migration audit |
| `check_links.py` | `tools/check_links.py` | Link checker |

### **Improvement**

| Tool | Path | Purpose |
|------|------|---------|
| `improve_prompts.py` | `tools/improve_prompts.py` | AI recommendations |
| `normalize_frontmatter.py` | `tools/normalize_frontmatter.py` | Frontmatter cleanup |

---

## 🖥️ Local Models (28 Available)

| Model Key | Size | Hardware | Use Case |
|-----------|------|----------|----------|
| `phi4-cpu` | 3.8B | CPU | Fast, general purpose |
| `phi4-gpu` | 3.8B | GPU | Faster with GPU |
| `phi3.5-cpu` | 3.8B | CPU | Good balance |
| `phi3-dml` | 3.8B | GPU/DirectML | GPU-accelerated |
| `phi3-medium` | 14B | CPU | Higher quality |
| `phi3-medium-dml` | 14B | GPU | Best local quality |
| `mistral-cpu` | 7B | CPU | Alternative architecture |
| `mistral-dml` | 7B | GPU | Fast Mistral |
| `phi3-vision` | 4.2B | CPU | Image understanding |
| `phi3.5-vision` | 4.2B | CPU | Image understanding |

**Full model list**: See `tools/llm_client.py` → `LOCAL_MODELS`

---

## � Grading Rubrics

Prompts are scored using a **100-point rubric** with 5 weighted criteria.

### **Scoring Criteria** (`toolkit/rubrics/quality_standards.json`)

| Criterion | Weight | What It Measures |
|-----------|--------|------------------|
| **Completeness** | 25% | All required sections present (frontmatter, description, examples, tips) |
| **Example Quality** | 30% | Realistic, detailed examples with actual data (no placeholders) |
| **Specificity** | 20% | Actionable, domain-specific content |
| **Format Adherence** | 15% | Correct markdown, YAML, and variable syntax |
| **Enterprise Quality** | 10% | Professional tone, industry framework references |

### **Quality Tiers**

| Tier | Score Range | Label |
|------|-------------|-------|
| Tier 1 | 90-100 | Excellent (Production-ready) |
| Tier 2 | 75-89 | Good (Minor improvements needed) |
| Tier 3 | 60-74 | Acceptable (Needs work) |
| Tier 4 | 0-59 | Poor (Major revision required) |

### **Rubric Files**

| File | Path | Purpose |
|------|------|---------|
| `quality_standards.json` | `toolkit/rubrics/quality_standards.json` | Structural scoring criteria |
| `prompt-scoring.yaml` | `toolkit/rubrics/prompt-scoring.yaml` | 5-dimension effectiveness scoring |

---

## �📈 Evaluation Tiers

| Tier | Name | Models | Cost | Use Case |
|------|------|--------|------|----------|
| 0 | Local ONNX | Phi4, Mistral | $0 | Quick local triage |
| 1 | Quick Triage | Structure only | $0 | Syntax check |
| 2 | Single Model | 1 cloud model | ~$0.01 | Basic eval |
| 3 | Cross-Validate | 3 models × 2 | ~$0.05 | Standard eval |
| 4 | Full Pipeline | 5 models × 3 | ~$0.15 | Thorough eval |
| 5 | Premium | 5 models × 4 | ~$0.25 | Production eval |
| 6 | Azure Foundry | Your deployment | Varies | Enterprise |
| 7 | Windows AI | NPU (Phi Silica) | $0 | NPU-accelerated |

---

## 🔧 Setup & Configuration

### **Environment Variables**

| Variable | Purpose | Required For |
|----------|---------|--------------|
| `GITHUB_TOKEN` | GitHub Models API | `gh:*` models |
| `AZURE_OPENAI_ENDPOINT` | Azure Foundry | `azure-foundry:*` |
| `AZURE_OPENAI_KEY` | Azure Foundry | `azure-foundry:*` |
| `OPENAI_API_KEY` | OpenAI | `gpt-*` models |

### **Local Model Cache**

Models are cached in: `~/.cache/aigallery/`

### **Windows AI (NPU)**

Requires Copilot+ PC and unlock token from Microsoft:

- [Apply for access](https://aka.ms/phi-silica-unlock)
- Run: `scripts/setup_windows_ai.ps1`

---

## 📚 Additional Resources

| Resource | Path |
|----------|------|
| Tools README | `tools/README.md` |
| Windows AI Guide | `WINDOWS_AI_INSTALL.md` |
| Unified Tooling Guide | `docs/UNIFIED_TOOLING_GUIDE.md` |
| CLI Reference | `docs/CLI_TOOLS.md` |
| Agents Guide | `agents/AGENTS_GUIDE.md` |

---

## 🚀 Quick Start

1. **Run a prompt locally**:

   ```bash
   python prompt.py run prompts/basic/greeting.md -p local -m phi4-cpu
   ```

2. **Evaluate a directory**:

   ```bash
   python prompt.py eval prompts/advanced/ -t 3
   ```

3. **Improve a prompt**:

   ```bash
   python prompt.py improve prompts/basic/greeting.md
   ```

4. **Use a workflow** (in GitHub Copilot):

   ```
   /generate-prompt
   ```
