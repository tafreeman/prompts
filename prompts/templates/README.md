---
name: Prompt Templates
description: Reusable templates for creating high-quality prompts following best practices and established patterns.
---

# Prompt Templates

Comprehensive collection of reusable templates for creating effective, well-structured prompts. These templates follow best practices and have been validated across multiple AI platforms.

## 📋 Contents

```text
templates/
├── README.md                        # This file
├── prompt-template.md               # Standard prompt template
├── prompt-template-minimal.md       # Minimal quick-start template
├── prompt-improvement-template.md   # Template for improving existing prompts
├── advanced_research_prompt.md      # Complex research prompt template
├── quick-start-template.md          # Rapid prototyping template
├── index-template.md                # Directory index template
└── roi-calculator.md                # ROI calculation template
```

## 🎯 When to Use Templates

| Template | Best For | Time to Complete |
| ---------- | ---------- | ------------------ |
| **[prompt-template-minimal.md](./prompt-template-minimal.md)** | Quick prompts, simple tasks | 5 min |
| **[prompt-template.md](./prompt-template.md)** | Standard prompts, most use cases | 15 min |
| **[advanced_research_prompt.md](./advanced_research_prompt.md)** | Complex analysis, research | 30 min |
| **[prompt-improvement-template.md](./prompt-improvement-template.md)** | Refining existing prompts | 10 min |
| **[quick-start-template.md](./quick-start-template.md)** | Prototyping, testing ideas | 5 min |

## ✨ Template Features

All templates include:

- ✅ YAML frontmatter with metadata
- ✅ Structured sections (Description, Prompt, Variables, Examples)
- ✅ Clear formatting guidelines
- ✅ Example usage patterns
- ✅ Tips and best practices
- ✅ Version control friendly

## 🚀 Quick Start

### 1. Choose Your Template

**For Simple Prompts:**

```bash
# Copy minimal template
cp templates/prompt-template-minimal.md prompts/your-category/your-prompt.md
```

**For Standard Prompts:**

```bash
# Copy standard template
cp templates/prompt-template.md prompts/your-category/your-prompt.md
```

**For Complex Analysis:**

```bash
# Copy advanced template
cp templates/advanced_research_prompt.md prompts/your-category/your-prompt.md
```

### 2. Fill in Metadata

```yaml
```

### 3. Write Your Content

Follow the template structure and fill in each section.

## 📚 Template Descriptions

### Standard Template

**File:** [prompt-template.md](./prompt-template.md)

The most commonly used template. Includes:

- Complete metadata schema
- Description section
- Prompt text area
- Variables table
- Example usage
- Tips section

**Use When:**

- Creating most prompts
- Need structured format
- Want comprehensive documentation

**Example Structure:**

```markdown
# Prompt Title

## Description
What this prompt does and when to use it.

## Prompt
\`\`\`text
Your actual prompt text with [VARIABLES]
\`\`\`

## Variables
| Variable | Description |
| ---------- | ------------- |
| [VAR]    | What to replace |

## Example
Input and output examples

## Tips
Best practices and suggestions
```

### Minimal Template

**File:** [prompt-template-minimal.md](./prompt-template-minimal.md)

Stripped-down version for quick prompts.

**Use When:**

- Need a prompt fast
- Simple, straightforward use case
- Prototyping or testing

**Example Structure:**

```markdown
# Quick Prompt Title

Brief description.

## Prompt
\`\`\`text
[Your prompt here]
\`\`\`

## Example
Quick example
```

### Advanced Research Template

**File:** [advanced_research_prompt.md](./advanced_research_prompt.md)

Comprehensive template for complex analytical tasks.

**Includes:**

- Multi-stage analysis sections
- Research methodology
- Source evaluation
- Synthesis and conclusions
- Confidence scoring

**Use When:**

- Complex research tasks
- Multi-step analysis required
- Need thorough documentation
- Academic or professional research

### Prompt Improvement Template

**File:** [prompt-improvement-template.md](./prompt-improvement-template.md)

Structured approach to refining existing prompts.

**Sections:**

- Original prompt analysis
- Issues identified
- Improvement strategy
- Revised prompt
- A/B testing results

**Use When:**

- Prompt not performing well
- Need systematic improvement
- Optimizing for specific platform
- Comparing variations

### Quick Start Template

**File:** [quick-start-template.md](./quick-start-template.md)

Get users productive immediately.

**Includes:**

- 5-minute quickstart
- Minimal setup
- Copy-paste ready examples
- Common variations

**Use When:**

- Creating getting-started guides
- Need rapid adoption
- Simplicity is key

## 🎓 Best Practices

### Writing Effective Prompts

#### 1. Be Specific

✅ **Do:**

```text
Write a Python function that validates email addresses using regex.
Include:

- Type hints
- Docstring with examples
- Error handling for invalid formats
- Unit tests using pytest

```

❌ **Don't:**

```text
Write code to check emails
```

#### 2. Provide Context

✅ **Do:**

```text
You are a senior Python developer following PEP 8 style guide.
Write production-ready code with:

- Comprehensive error handling
- Logging for debugging
- Type hints for clarity

```

❌ **Don't:**

```text
Write good code
```

#### 3. Use Examples

✅ **Do:**

```text
Convert natural language to SQL. Examples:

Input: "Show all users"
Output: SELECT * FROM users;

Input: "Count active users"
Output: SELECT COUNT(*) FROM users WHERE active = true;

Now convert: "Show users who joined in 2024"
```

❌ **Don't:**

```text
Convert this to SQL: "Show users who joined in 2024"
```

#### 4. Define Output Format

✅ **Do:**

```text
Respond in JSON format:
{
  "analysis": "string",
  "recommendations": ["array of strings"],
  "confidence": 0.0-1.0
}
```

❌ **Don't:**

```text
Give me JSON output
```

### Metadata Best Practices

#### Difficulty Levels

| Level | Description | User Expertise |
| ------- | ------------- | ---------------- |
| **beginner** | Simple, single-step tasks | No prior experience needed |
| **intermediate** | Multi-step, requires some knowledge | Some AI/domain experience |
| **advanced** | Complex, specialized knowledge | Expert in domain/technique |

#### Type Categories

| Type | Description | Example |
| ------ | ------------- | --------- |
| **how_to** | Step-by-step guide | "How to debug code" |
| **reference** | Quick lookup | "API reference" |
| **tutorial** | Learning path | "Introduction to prompting" |
| **conceptual** | Theory/understanding | "What is RAG?" |

#### Audience Tags

Common audiences:

- `junior-engineer` - Early career developers
- `senior-engineer` - Experienced developers
- `business-analyst` - Non-technical analysts
- `investigator` - OSINT/security professionals
- `data-scientist` - ML/data specialists

#### Platform Tags

Common platforms:

- `github-copilot` - GitHub Copilot
- `claude` - Anthropic Claude
- `chatgpt` - OpenAI ChatGPT
- `semantic-kernel` - Microsoft Semantic Kernel
- `langchain` - LangChain framework

## 🔧 Template Customization

### Adding Custom Sections

You can extend templates with additional sections:

```markdown
## Prerequisites

- Required tools
- Knowledge needed
- Setup steps

## Troubleshooting
Common issues and solutions

## Related Prompts

- [Similar Prompt 1](../link1.md)
- [Similar Prompt 2](../link2.md)

## Performance Notes

- Expected token usage: ~500 tokens
- Average response time: 3-5 seconds
- Cost estimate: $0.01 per request

```

### Creating Domain-Specific Templates

For specialized domains, create derived templates:

**Example: Code Review Template**

```markdown
# Code Review: [Component Name]

## Code to Review
\`\`\`language
[Code here]
\`\`\`

## Review Focus

- [ ] Security vulnerabilities
- [ ] Performance issues
- [ ] Code maintainability
- [ ] Test coverage

## Findings
[AI will fill this section]

## Recommendations
[AI will fill this section]
```

## 📊 Template Comparison

| Template | Sections | Complexity | Setup Time | Best For |
| ---------- | ---------- | ------------ | ------------ | ---------- |
| Minimal | 3 | Low | 5 min | Quick tasks |
| Standard | 7 | Medium | 15 min | Most prompts |
| Advanced | 12+ | High | 30 min | Research/analysis |
| Improvement | 8 | Medium | 10 min | Optimization |
| Quick Start | 4 | Low | 5 min | User onboarding |

## 🛠️ Tools & Utilities

### Template Validation

Check if your prompt follows the template:

```bash
# Validate prompt structure
python tools/validators/prompt_validator.py prompts/your-prompt.md

# Check metadata completeness
python tools/validators/metadata_checker.py prompts/your-prompt.md
```

### Template Generator

Create prompts from templates interactively:

```bash
# Interactive prompt creation
python tools/generators/prompt_creator.py

# From command line
python tools/generators/prompt_creator.py \
  --template standard \
  --title "My New Prompt" \
  --category developers \
  --output prompts/developers/my-prompt.md
```

## 📖 Additional Resources

### Prompt Engineering Guides

- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Ultimate Prompting Guide](../../docs/ultimate-prompting-guide.md)

### Examples
Browse existing prompts for inspiration:

- [Developer Prompts](../developers/)
- [Business Prompts](../business/)
- [Advanced Techniques](../techniques/)

### Community

- [GitHub Discussions](https://github.com/tafreeman/prompts/discussions)
- Share your templates
- Get feedback on prompts

## 🤝 Contributing

### Adding New Templates

When creating a new template:

1. **Identify the need**: What's missing from existing templates?
2. **Design the structure**: What sections are essential?
3. **Create example**: Fill template with realistic example
4. **Document usage**: When to use this template
5. **Test thoroughly**: Use with multiple AI platforms
6. **Add to README**: Update this file with new template info

### Template Submission Checklist

- [ ] YAML frontmatter included
- [ ] All required sections present
- [ ] Clear, concise descriptions
- [ ] Example usage provided
- [ ] Tested with at least 2 AI platforms
- [ ] Follows repository conventions
- [ ] Documentation updated

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for full guidelines.

## 💡 Tips for Template Usage

### 1. Start Simple

Begin with minimal template, expand as needed:

```text
Minimal → Standard → Advanced
```

### 2. Iterate Quickly

Don't aim for perfection on first draft:

1. Create basic version
2. Test with AI
3. Refine based on results
4. Add examples and tips

### 3. Version Control

Track improvements:

```yaml
version: "1.0"  # Initial
version: "1.1"  # Minor improvements
version: "2.0"  # Major rewrite
```

### 4. Document Learnings

Add tips based on actual usage:

```markdown
## Tips

- Works best with GPT-4 (tested 2025-11-30)
- For Claude, add XML tags around code blocks
- Set temperature to 0.7 for creative tasks

```

## 📝 Version History

- **1.0** (2025-11-30): Initial release with 7 core templates

---

**Need Help?** Check our [documentation](../../docs/) or [open an issue](https://github.com/tafreeman/prompts/issues).
