---
title: Best Practices for Prompt Engineering
shortTitle: Best Practices for Promp...
intro: A prompt for best practices for prompt engineering tasks.
type: how_to
difficulty: intermediate
audience:
- senior-engineer
- junior-engineer
platforms:
- github-copilot
- claude
- chatgpt
author: Prompts Library Team
version: '1.0'
date: '2025-11-30'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
---
# Best Practices for Prompt Engineering

A comprehensive guide to writing effective prompts based on research from Anthropic, OpenAI, Microsoft, and academic papers.

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [The Five Dimensions of Quality](#the-five-dimensions-of-quality)
3. [Platform-Specific Best Practices](#platform-specific-best-practices)
4. [Common Patterns](#common-patterns)
5. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
6. [Quality Checklist](#quality-checklist)
7. [Additional Resources](#additional-resources)

---

## Core Principles

### 1. Be Specific

Vague prompts produce vague outputs. Always include specific details about what you want.

❌ **Don't:**
```
Analyze this data.
```

✅ **Do:**
```
Analyze this Q4 2024 sales data and identify:
1. Top 5 products by revenue
2. Month-over-month growth trends
3. Underperforming categories (below 10% growth)

Format the output as a markdown table with columns: Product, Revenue, MoM Growth, Status.
```

### 2. Provide Context

Give the AI the background information it needs to produce relevant results.

Include:
- **Purpose**: Why you need this output
- **Audience**: Who will read/use the result
- **Domain**: Industry or technical context
- **Constraints**: Time, format, or compliance requirements

### 3. Define Output Format

Specify exactly how you want the response structured.

```
Output as JSON with this schema:
{
  "summary": "string (2-3 sentences)",
  "key_points": ["string"],
  "action_items": [{"task": "string", "owner": "string", "due": "date"}],
  "confidence": "number (0-1)"
}
```

### 4. Use Examples (Few-Shot Learning)

Show the AI what you want with concrete examples.

```
Convert these informal notes to formal bullet points.

Example:
Input: "talked to john about proj timeline - he says 2 weeks maybe 3"
Output: • Project timeline discussion with John: Estimated 2-3 weeks to completion

Now convert:
Input: "meeting with stakeholders went well - they approved budget but want monthly reports"
```

### 5. Iterate and Refine

First attempts rarely perfect. Start simple and add detail based on results.

1. Test with a minimal prompt
2. Review the output
3. Add constraints or examples to improve
4. Repeat until satisfied

---

## The Five Dimensions of Quality

Our scoring methodology evaluates prompts across five dimensions:

### 1. Clarity & Specificity (20 points)

| Score | Criteria |
| :--- |----------|
| 20 | Crystal clear goal, explicit instructions, defined success criteria |
| 15 | Clear goal, good instructions, some criteria defined |
| 10 | Understandable but lacks detail |
| 5 | Vague or ambiguous |
| 0 | Unclear what's being asked |

### 2. Structure & Completeness (20 points)

| Score | Criteria |
| :--- |----------|
| 20 | All necessary sections, examples, full documentation |
| 15 | Most sections present, good examples |
| 10 | Basic structure, some missing elements |
| 5 | Minimal structure |
| 0 | Unstructured, incomplete |

### 3. Usefulness & Reusability (20 points)

| Score | Criteria |
| :--- |----------|
| 20 | Solves common problems, highly adaptable |
| 15 | Useful for specific scenarios, somewhat adaptable |
| 10 | Limited use cases |
| 5 | Very narrow applicability |
| 0 | Not practically useful |

### 4. Technical Quality (20 points)

| Score | Criteria |
| :--- |----------|
| 20 | Proper reasoning style, structured output, follows best practices |
| 15 | Good technique, minor issues |
| 10 | Acceptable quality |
| 5 | Technical problems |
| 0 | Fundamentally flawed |

### 5. Ease of Use (20 points)

| Score | Criteria |
| :--- |----------|
| 20 | Simple to customize, minimal prerequisites, excellent tips |
| 15 | Easy to use with some guidance needed |
| 10 | Moderate learning curve |
| 5 | Difficult to customize |
| 0 | Very hard to use |

**Target Score**: 75+ points for production-quality prompts

---

## Platform-Specific Best Practices

### GitHub Copilot

**The Four S's Framework:**
1. **Single**: One task per prompt
2. **Specific**: Detailed, explicit instructions
3. **Short**: Concise but information-rich
4. **Surround**: Use context from open files

**Tips:**
- Use comments above code for context
- Open related files for better suggestions
- Specify language version and libraries
- Include example inputs/outputs

### Microsoft 365 Copilot

**CARE Framework:**
- **Context**: Background information
- **Action**: What you want done
- **Result**: Expected output
- **Example**: Sample of desired output

**Tips:**
- Use natural, conversational language
- Specify audience and tone
- Reference connected documents
- Ask for specific output formats

### Claude & GPT

**Tips:**
- Longer, detailed prompts work well
- Use XML tags for complex structure
- Request reasoning explicitly
- Specify exact output format
- Assign roles/personas for expertise

### Windows Copilot

**Tips:**
- Be specific about what you want done
- Specify output format preferences
- Use for quick system tasks
- Combine multiple related actions in one prompt

---

## Common Patterns

### Role-Task-Format (RTF)

```
You are a [ROLE].

Your task is to [TASK].

Provide output in the following format:
[FORMAT_SPECIFICATION]
```

**Best for**: Software development, business analysis, reporting

### Context-Action-Result-Example (CARE)

```
**Context**: [BACKGROUND_INFORMATION]
**Action**: [WHAT_YOU_WANT]
**Result**: [EXPECTED_OUTPUT]
**Example**: [SAMPLE_OUTPUT]
```

**Best for**: Business communications, document generation

### Chain-of-Thought

```
Think through this step by step:

Step 1: [First consideration]
Step 2: [Second consideration]
Step 3: [Synthesis and conclusion]

Show your reasoning at each step.
```

**Best for**: Complex problems, debugging, analysis

### Tree-of-Thoughts

```
Evaluate multiple approaches:

**Approach A**: [Description] - Pros/Cons - Score
**Approach B**: [Description] - Pros/Cons - Score
**Approach C**: [Description] - Pros/Cons - Score

**Recommendation**: Based on analysis, select the best approach.
```

**Best for**: Architecture decisions, strategic planning, trade-off analysis

---

## Common Mistakes to Avoid

### ❌ Being Too Vague

**Problem**: "Help me with my code"
**Solution**: Specify what kind of help—debug, optimize, refactor, document

### ❌ Overloading a Single Prompt

**Problem**: Asking for 10 different things at once
**Solution**: Break complex tasks into focused prompts

### ❌ Ignoring Output Format

**Problem**: Getting unstructured text when you need JSON
**Solution**: Always specify the exact format needed

### ❌ Missing Context

**Problem**: Not explaining the domain or constraints
**Solution**: Include relevant background information

### ❌ Hardcoding Values

**Problem**: Writing prompts that only work for one specific case
**Solution**: Use `[PLACEHOLDERS]` for reusability

### ❌ Embedding Secrets

**Problem**: Including API keys, passwords, or PII in prompts
**Solution**: Use placeholder variables like `[API_KEY]`

### ❌ Skipping Examples

**Problem**: Expecting the AI to guess your desired output style
**Solution**: Provide at least one example input/output pair

---

## Quality Checklist

Before using or submitting a prompt, verify:

### Structure
- [ ] Clear, descriptive title
- [ ] Appropriate category and tags
- [ ] Goal is explicitly stated
- [ ] All placeholders are documented

### Content
- [ ] Specific instructions provided
- [ ] Necessary context included
- [ ] Output format defined
- [ ] Constraints specified
- [ ] At least one example included

### Technical
- [ ] Appropriate reasoning style chosen
- [ ] Edge cases addressed
- [ ] No embedded secrets or PII
- [ ] Variables use `[BRACKET]` format

### Usability
- [ ] Easy to customize
- [ ] Tips for better results included
- [ ] Related prompts linked (if applicable)

---

## Additional Resources

### In This Repository

- [Ultimate Prompting Guide](ultimate-prompting-guide.md) - Top 20% most effective prompts
- [Platform-Specific Templates](platform-specific-templates.md) - Ready-to-use templates
- [Prompt Effectiveness Methodology](prompt-effectiveness-scoring-methodology.md) - Full scoring details
- [Advanced Techniques](advanced-techniques.md) - CoT, ReAct, ToT patterns

### External Resources

- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/constructing-a-prompt)
- [OpenAI Best Practices](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
- [Microsoft 365 Copilot Adoption](https://adoption.microsoft.com/en-us/copilot/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)

### Research Papers

- Wei et al. (NeurIPS 2022): "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- Yao et al. (NeurIPS 2023): "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
- "The Prompt Report" (arXiv:2406.06608): Comprehensive taxonomy of prompting techniques

---

*Last Updated: 2025-11-28*
