---
title: "Prompts Library"
shortTitle: "Prompts"
intro: "Comprehensive collection of AI prompts organized by use case, technique, and framework."
type: "reference"
difficulty: "beginner"
audience:

  - "junior-engineer"
  - "senior-engineer"
  - "business-analyst"
  - "investigator"

platforms:

  - "github-copilot"
  - "claude"
  - "chatgpt"

author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:

  - "PII-safe"

dataClassification: "public"
reviewStatus: "approved"
---

# Prompts Library

A comprehensive, well-organized collection of AI prompts covering everything from basic templates to advanced prompting techniques, framework-specific implementations, and specialized use cases.

## 📁 Directory Structure

```text
prompts/
├── advanced/               # 🎯 Advanced prompting patterns (CoT, ReAct, ToT)
├── agents/                 # 🤖 GitHub Copilot custom agents
├── analysis/               # 📊 Data analysis and research prompts
├── business/               # 💼 Business strategy and operations
├── creative/               # 🎨 Content creation and marketing
├── developers/             # 💻 Code generation and technical tasks
├── frameworks/             # 🏗️ Framework-specific implementations
├── governance/             # 📋 Legal, security, and compliance
├── m365/                   # 🏢 Microsoft 365 Copilot prompts
├── socmint/                # 🔍 Social media intelligence (OSINT)
├── system/                 # ⚙️ System-level prompts and configurations
├── techniques/             # 🎓 Advanced prompting techniques
└── templates/              # 📄 Reusable prompt templates
```

## 🎯 Quick Navigation

### By Role

| Role | Recommended Starting Point | Key Directories |
| ------ | --------------------------- | ----------------- |
| **Developers** | [developers/](./developers/) | `developers/`, `techniques/`, `frameworks/` |
| **Business Analysts** | [business/](./business/) | `business/`, `analysis/`, `templates/` |
| **Creative Professionals** | [creative/](./creative/) | `creative/`, `templates/` |
| **Security/OSINT** | [socmint/](./socmint/) | `socmint/`, `governance/` |
| **Enterprise Teams** | [governance/](./governance/) | `governance/`, `m365/` |
| **AI Researchers** | [techniques/](./techniques/) | `techniques/`, `advanced/`, `frameworks/` |

### By Use Case

| Use Case | Directory | Description |
| ---------- | ----------- | ------------- |
| **Code Generation** | [developers/](./developers/) | Write, debug, and optimize code |
| **Strategy & Planning** | [business/](./business/) | Business analysis and decision support |
| **Data Analysis** | [analysis/](./analysis/) | Extract insights from data |
| **Content Creation** | [creative/](./creative/) | Marketing, copywriting, storytelling |
| **Investigation** | [socmint/](./socmint/) | OSINT and social media analysis |
| **Advanced AI** | [techniques/](./techniques/) | ReAct, reflexion, agentic patterns |

## 🚀 Getting Started

### For First-Time Users

1. **Browse by Role**: Use the table above to find your relevant directory
2. **Check Templates**: Start with [templates/](./templates/) for basic prompt structures
3. **Review Examples**: Each prompt includes usage examples and expected outputs
4. **Customize**: Replace variables (marked with `[brackets]`) with your specific needs

### For Developers

```bash
# Clone the repository
git clone https://github.com/tafreeman/prompts.git
cd prompts/prompts

# View a specific prompt
cat developers/code-generation.md

# Use with Python
python tools/prompt.py run --file developers/code-generation.md
```

### For Advanced Users

Explore sophisticated patterns in:

- [techniques/reflexion/](./techniques/reflexion/) - Self-correction and improvement
- [techniques/agentic/](./techniques/agentic/) - Multi-agent workflows
- [techniques/context-optimization/](./techniques/context-optimization/) - Long-context handling
- [frameworks/](./frameworks/) - Framework-specific implementations

## 📚 Directory Guides

### Core Content

- **[advanced/](./advanced/)** - Chain-of-Thought, ReAct, RAG, Tree-of-Thoughts
- **[agents/](./agents/)** - GitHub Copilot custom agents ([@docs_agent](./agents/docs-agent.agent.md), [@test_agent](./agents/test-agent.agent.md), etc.)
- **[analysis/](./analysis/)** - Data analysis, research synthesis, insights
- **[business/](./business/)** - Strategy, market research, financial analysis
- **[creative/](./creative/)** - Copywriting, marketing, content creation
- **[developers/](./developers/)** - Code generation, debugging, testing, architecture

### Specialized Content

- **[frameworks/](./frameworks/)** - [LangChain](./frameworks/langchain/), [Anthropic](./frameworks/anthropic/), [OpenAI](./frameworks/openai/), [Microsoft](./frameworks/microsoft/)
- **[governance/](./governance/)** - Legal, security, compliance, risk management
- **[m365/](./m365/)** - Microsoft 365 Copilot specific prompts
- **[socmint/](./socmint/)** - Social media intelligence and OSINT investigations
- **[system/](./system/)** - System prompts, role definitions, behavior guidelines

### Learning & Templates

- **[techniques/](./techniques/)** - [Reflexion](./techniques/reflexion/), [Agentic](./techniques/agentic/), [Context Optimization](./techniques/context-optimization/)
- **[templates/](./templates/)** - Reusable templates for creating new prompts

## 🎓 Prompt Format

All prompts follow a consistent structure with YAML frontmatter:

```markdown
---
title: "Prompt Title"
difficulty: "beginner|intermediate|advanced"
platforms: ["github-copilot", "claude", "chatgpt"]
tags: ["tag1", "tag2"]
version: "1.0"
---

# Prompt Title

## Description
Brief description of what this prompt does.

## Prompt
\`\`\`text
[Actual prompt text with [VARIABLES]]
\`\`\`

## Variables
| Variable | Description |
| ---------- | ------------- |
| `[VAR]`  | What to replace |

## Example
Input/output examples...
```

## 🔍 Finding the Right Prompt

### By Search

Use GitHub's search or grep:

```bash
# Search by keyword
grep -r "code review" prompts/

# Search by tag
grep -r "tags: .*debugging" prompts/

# Search by difficulty
grep -r "difficulty: beginner" prompts/
```

### By Metadata

All prompts include structured metadata:

- **difficulty**: beginner, intermediate, advanced
- **platforms**: github-copilot, claude, chatgpt, etc.
- **audience**: junior-engineer, senior-engineer, business-analyst, etc.
- **type**: how_to, reference, tutorial, etc.

## 🏆 Top Prompts

Based on effectiveness scoring (75+/100):

| Prompt | Category | Score | Use Case |
| -------- | ---------- | ------- | ---------- |
| [Chain-of-Thought Analysis](./techniques/chain-of-thought-analysis.md) | Advanced | 90 | Complex reasoning |
| [ReAct Knowledge Base](./techniques/react-knowledge-base.md) | Advanced | 88 | Tool-augmented tasks |
| [Basic Reflexion](./techniques/reflexion/basic-reflexion/) | Techniques | 87 | Self-correction |
| [Multi-Agent Workflow](./techniques/agentic/multi-agent/) | Techniques | 85 | Complex orchestration |

## 🤝 Contributing

Want to add a prompt? See our [contribution guidelines](../CONTRIBUTING.md).

Each new prompt should:

1. Follow the standard format (use [templates/prompt-template.md](./templates/prompt-template.md))
2. Include complete metadata
3. Provide working examples
4. Be tested and validated

## 📖 Additional Resources

- **[Ultimate Prompting Guide](../docs/ultimate-prompting-guide.md)** - Comprehensive best practices
- **[Platform-Specific Templates](../docs/platform-specific-templates.md)** - Optimized for each AI platform
- **[Scoring Methodology](../docs/prompt-effectiveness-scoring-methodology.md)** - How we evaluate prompts

## 🔧 Tools & Utilities

Execute and evaluate prompts:

```bash
# Run a prompt
python tools/prompt.py run --file prompts/developers/code-generation.md

# Evaluate effectiveness
python tools/prompt.py eval --file prompts/developers/code-generation.md

# Chain-of-Verification
python tools/prompt.py cove --file prompts/analysis/data-analysis.md
```

See [tools/README.md](../tools/README.md) for full documentation.

## 📊 Statistics

- **Total Prompts**: 165+
- **Categories**: 12
- **Frameworks**: 4 (LangChain, Anthropic, OpenAI, Microsoft)
- **Techniques**: 10+
- **Custom Agents**: 7+

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**Need help?** Check our [documentation](../docs/) or [open an issue](https://github.com/tafreeman/prompts/issues).
