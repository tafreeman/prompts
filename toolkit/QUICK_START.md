# 🚀 Quick Start Guide

Get productive with the Prompt Library Toolkit in 5 minutes.

---

## 1️⃣ Run Your First Prompt (30 seconds)

```bash
python prompt.py run prompts/tools/validate_prompts.py -p local -m phi4-cpu
```

This executes a prompt using your local Phi-4 model (no API keys needed).

---

## 2️⃣ Evaluate a Prompt (1 minute)

```bash
python prompt.py eval prompts/advanced/ -t 3
```

This evaluates all prompts in the `advanced/` folder using Tier 3 (cross-model validation).

---

## 3️⃣ Improve a Prompt (2 minutes)

```bash
python prompt.py improve prompts/basic/greeting.md
```

This provides AI-powered improvement recommendations.

---

## 4️⃣ Use a Workflow (in GitHub Copilot)

Type `/generate-prompt` in Copilot Chat to create a new prompt with AI assistance.

---

## 5️⃣ Validate Your Library

```bash
# Check all frontmatter schemas
python tools/validators/frontmatter_validator.py --all

# Audit prompts for issues
python tools/audit_prompts.py prompts/
```

---

## 📦 What's Included

| Category | Location | Count |
|----------|----------|-------|
| Python Tools | `tools/` | 20+ scripts |
| Meta-Prompts | `archive/clutter/toolkit_prompts/` | 8 key prompts |
| Rubrics | `toolkit/rubrics/` | 2 scoring files |
| Agents | `agents/` | 9 Copilot agents |
| Workflows | `.agent/workflows/` | 2 slash commands |

---

## 🔑 API Keys (Optional)

For cloud models, set these environment variables:

```bash
# GitHub Models (free tier)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# OpenAI
export OPENAI_API_KEY=sk-xxxxxxxxxxxx

# Azure Foundry
export AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
export AZURE_OPENAI_KEY=xxxxxxxxxxxx
```

---

## 📚 Next Steps

1. **Browse the full toolkit**: [toolkit/README.md](README.md)
2. **Explore meta-prompts**: [archive/clutter/toolkit_prompts/](archive/clutter/toolkit_prompts/)
3. **Review rubrics**: [toolkit/rubrics/](rubrics/)
4. **Learn about agents**: [agents/AGENTS_GUIDE.md](../agents/AGENTS_GUIDE.md)
