# Repository Documentation Orchestrator - Usage Guide

> **All GitHub Models are FREE** with rate limits. GPT-4o is the base model with unlimited requests (rate-limited). Other models consume "premium requests" at varying multipliers.

## Quick Start

```bash
# Full repository analysis with GPT-4o (recommended - unlimited free)
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m openai/gpt-4o \
    --temperature 0.3 --max-tokens 16000

# Single directory analysis
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m openai/gpt-4o \
    --temperature 0.3 --max-tokens 16000 \
    -s "Focus only on: tools/"
```

---

## GitHub Models - Tested Availability (Dec 2025)

> Rate limits are **per-model**, not a global pool. Most models work; reasoning models have tight limits.

### ✅ TESTED WORKING (Recommended)

| Model | Command | Notes |
|-------|---------|-------|
| **GPT-4o** | `-p gh -m openai/gpt-4o` | Best overall - reliable |
| **GPT-4.1** | `-p gh -m openai/gpt-4.1` | Latest OpenAI |
| **GPT-4o-mini** | `-p gh -m openai/gpt-4o-mini` | Fast, good quality |
| **GPT-5-mini** | `-p gh -m openai/gpt-5-mini` | Newest small |
| **Phi-4-mini** | `-p gh -m microsoft/phi-4-mini-instruct` | Fast Microsoft |
| **Ministral 3B** | `-p gh -m mistral-ai/ministral-3b` | Very fast |
| **Llama 3.1 8B** | `-p gh -m meta/meta-llama-3.1-8b-instruct` | Good open-source |
| **Llama 3.3 70B** | `-p gh -m meta/llama-3.3-70b-instruct` | Strong open-source |
| **DeepSeek-R1** | `-p gh -m deepseek/deepseek-r1` | Reasoning capable |
| **Grok 3** | `-p gh -m xai/grok-3` | xAI model |

### ⚠️ TIGHT RATE LIMITS (Use Sparingly)

| Model | Command | Notes |
|-------|---------|-------|
| o3 | `-p gh -m openai/o3` | Reasoning - 1-2 calls then limited |
| o1 | `-p gh -m openai/o1` | Reasoning - limited |
| o4-mini | `-p gh -m openai/o4-mini` | Reasoning - limited |

### 🧠 Reasoning Models (Complex Analysis)

| Model | Command | Notes |
|-------|---------|-------|
| **o3** | `-p gh -m openai/o3` | Best reasoning |
| o3-mini | `-p gh -m openai/o3-mini` | Fast reasoning |
| o4-mini | `-p gh -m openai/o4-mini` | Latest reasoning |
| o1 | `-p gh -m openai/o1` | Original reasoning |
| Phi-4-reasoning | `-p gh -m microsoft/phi-4-reasoning` | MS reasoning |
| DeepSeek-R1 | `-p gh -m deepseek/deepseek-r1` | Open reasoning |

### 🖼️ Vision Models (For Screenshots/Diagrams)

| Model | Command |
|-------|---------|
| Llama 3.2 11B Vision | `-p gh -m meta/llama-3.2-11b-vision-instruct` |
| Llama 3.2 90B Vision | `-p gh -m meta/llama-3.2-90b-vision-instruct` |
| Phi-4-multimodal | `-p gh -m microsoft/phi-4-multimodal-instruct` |

### 💻 Code-Focused

| Model | Command |
|-------|---------|
| **Codestral 25.01** | `-p gh -m mistral-ai/codestral-2501` |
| GPT-5 | `-p gh -m openai/gpt-5` |
| GPT-5-mini | `-p gh -m openai/gpt-5-mini` |

### 🆕 Cutting-Edge (May Be Preview)

| Model | Command |
|-------|---------|
| GPT-5-chat | `-p gh -m openai/gpt-5-chat` |
| Llama 4 Maverick | `-p gh -m meta/llama-4-maverick-17b-128e-instruct-fp8` |
| Llama 4 Scout | `-p gh -m meta/llama-4-scout-17b-16e-instruct` |
| Grok 3 | `-p gh -m xai/grok-3` |
| Grok 3 Mini | `-p gh -m xai/grok-3-mini` |

---

## All Provider Options

| Provider | Command | Cost | Context |
|----------|---------|------|---------|
| **GitHub Models (Free)** | `-p gh -m <model>` | $0 | 128K |
| Local ONNX | `-p local -m phi4-cpu` | $0 | 4K |
| Azure Foundry | `-p azure-foundry:<deployment>` | $$ | Varies |
| OpenAI Direct | `-p openai -m gpt-4o` | $$ | 128K |
| Claude | `-p claude -m claude-3-5-sonnet` | $$ | 200K |

---

## Parameter Options

| Flag | Purpose | Example |
|------|---------|---------|
| `--temperature` | Creativity (0.1-1.0, lower = focused) | `--temperature 0.3` |
| `--max-tokens` | Output length limit | `--max-tokens 16000` |
| `-s` | System prompt override | `-s "Analyze only: tools/"` |
| `-o` | Output file | `-o docs/tools-reference.md` |

---

## Directory-by-Directory Execution

### Using GPT-4o (Recommended)

```bash
# 1. Tools (23 files)
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m openai/gpt-4o \
    --temperature 0.3 --max-tokens 16000 \
    -s "Analyze only: tools/" \
    -o docs/tools-reference.md

# 2. Agents (13 files)
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m openai/gpt-4o \
    --temperature 0.3 --max-tokens 16000 \
    -s "Analyze only: agents/" \
    -o docs/agents-reference.md

# 3. Toolkit
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m openai/gpt-4o \
    --temperature 0.3 --max-tokens 16000 \
    -s "Analyze only: toolkit/" \
    -o docs/toolkit-reference.md

# 4. Testing
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m openai/gpt-4o \
    --temperature 0.3 --max-tokens 16000 \
    -s "Analyze only: testing/" \
    -o docs/testing-reference.md

# 5. Frameworks
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m openai/gpt-4o \
    --temperature 0.3 --max-tokens 16000 \
    -s "Analyze only: frameworks/" \
    -o docs/frameworks-reference.md

# 6. Archive
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m openai/gpt-4o \
    --temperature 0.3 --max-tokens 16000 \
    -s "Analyze only: _archive/" \
    -o docs/archive-reference.md
```

### Using Alternative Models

```bash
# With o3 reasoning model (best for complex analysis)
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m openai/o3 \
    --temperature 0.3 --max-tokens 16000 \
    -s "Analyze only: tools/"

# With Llama 3.3 (strong open-source)
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m meta/llama-3.3-70b-instruct \
    --temperature 0.3 --max-tokens 16000 \
    -s "Analyze only: tools/"

# With Mistral Medium (fast + capable)
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m mistral-ai/mistral-medium-2505 \
    --temperature 0.3 --max-tokens 16000 \
    -s "Analyze only: tools/"

# With Codestral (code-focused)
python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md \
    -p gh -m mistral-ai/codestral-2501 \
    --temperature 0.3 --max-tokens 16000 \
    -s "Analyze only: tools/"
```

---

## Batch Execution Script

```powershell
# run-doc-orchestrator.ps1
param(
    [string]$Model = "openai/gpt-4o",
    [string]$Temperature = "0.3",
    [string]$MaxTokens = "16000"
)

$dirs = @("tools", "agents", "toolkit", "testing", "frameworks", "_archive")

foreach ($dir in $dirs) {
    Write-Host "Analyzing $dir with $Model..."
    python prompt.py run toolkit/prompts/orchestrator/repo-doc-orchestrator.md `
        -p gh -m $Model `
        --temperature $Temperature `
        --max-tokens $MaxTokens `
        -s "Analyze only: $dir/" `
        -o "docs/$dir-reference.md"
    
    Start-Sleep -Seconds 5  # Rate limit buffer
}

Write-Host "Done! Check docs/ for output files."
```

**Usage:**

```powershell
# Default (GPT-4o)
.\run-doc-orchestrator.ps1

# With o3 reasoning
.\run-doc-orchestrator.ps1 -Model "openai/o3"

# With Llama
.\run-doc-orchestrator.ps1 -Model "meta/llama-3.3-70b-instruct"
```

---

## Expected Outputs

| File | Content |
|------|---------|
| `docs/tools-reference.md` | 23 Python tools documented |
| `docs/agents-reference.md` | 13 agent definitions |
| `docs/toolkit-reference.md` | Meta-prompts & rubrics |
| `docs/testing-reference.md` | Test framework overview |
| `docs/frameworks-reference.md` | External integrations |
| `docs/archive-reference.md` | Archived content review |

---

## Model Selection Guide

| Use Case | Recommended Model |
|----------|-------------------|
| **Best overall quality** | `openai/gpt-4o` or `openai/gpt-4.1` |
| **Complex reasoning/analysis** | `openai/o3` |
| **Code documentation** | `mistral-ai/codestral-2501` |
| **Fast iteration** | `openai/gpt-4o-mini` |
| **Open-source preference** | `meta/llama-3.3-70b-instruct` |
| **Budget/rate limits** | `mistral-ai/ministral-3b` |
