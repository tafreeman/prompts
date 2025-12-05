---
title: "Comprehensive Prompt Development Guide"
shortTitle: "Prompt Development Guide"
intro: "The definitive guide to developing effective AI prompts, synthesizing repository standards, industry best practices from OpenAI, Anthropic, Google, and academic research."
type: reference
difficulty: intermediate
audience:
  - junior-engineer
  - senior-engineer
  - solution-architect
  - business-analyst
  - prompt-engineer
platforms:
  - github-copilot
  - claude
  - chatgpt
  - azure-openai
  - m365-copilot
  - gemini
topics:
  - prompt-engineering
  - best-practices
  - evaluation
  - structure
  - advanced-techniques
author: Prompts Library Team
version: "1.0"
date: "2025-12-01"
governance_tags:
  - PII-safe
dataClassification: public
reviewStatus: approved
---

# Comprehensive Prompt Development Guide

**The Definitive Resource for Creating High-Quality AI Prompts**

This guide synthesizes best practices from:
- **Repository Standards**: Our prompt templates, evaluation criteria, and quality frameworks
- **Industry Leaders**: OpenAI, Anthropic, Google (Gemini), Microsoft, GitHub Copilot
- **Academic Research**: Wei et al. (Chain-of-Thought), Yao et al. (Tree-of-Thoughts), The Prompt Report
- **Evaluation Insights**: Analysis of 24+ prompts with 8-criteria evaluation framework

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [The Seven Components of Effective Prompts](#the-seven-components-of-effective-prompts)
3. [Prompt Structure Patterns](#prompt-structure-patterns)
4. [Platform-Specific Guidelines](#platform-specific-guidelines)
5. [Advanced Techniques](#advanced-techniques)
6. [Quality Evaluation Criteria](#quality-evaluation-criteria)
7. [Common Mistakes and Fixes](#common-mistakes-and-fixes)
8. [Templates and Checklists](#templates-and-checklists)
9. [Industry Best Practices Summary](#industry-best-practices-summary)

---

## Quick Reference

### Universal Prompt Structure

```text
[ROLE]      Who/what expertise to assume
[CONTEXT]   Background information and setup  
[TASK]      What needs to be accomplished
[FORMAT]    How output should be structured
[CONSTRAINTS] Boundaries and requirements
```text
### Quality Score Targets

| Level | Score | Use Case |
|-------|-------|----------|
| **Production** | 85+ | Enterprise, customer-facing |
| **Standard** | 70-84 | Internal tools, team use |
| **Draft** | 55-69 | Prototyping, iteration |
| **Needs Work** | <55 | Major improvements required |

### The 8 Evaluation Criteria

1. **Clarity** - Is the goal unambiguous?
2. **Specificity** - Are instructions detailed?
3. **Actionability** - Can the AI act on it?
4. **Structure** - Is it well-organized?
5. **Completeness** - All necessary info included?
6. **Factuality** - Does it guide accurate outputs?
7. **Consistency** - Will it produce reliable results?
8. **Safety** - Does it prevent harmful outputs?

---

## The Seven Components of Effective Prompts

Based on repository standards and industry research, effective prompts contain up to seven key components. Not every prompt needs all seven—the skill is knowing which to include.

### 1. Context

**Purpose**: Provides background information the AI needs to understand your situation.

**What to Include**:
- Relevant background information
- Current situation or problem state
- Domain-specific details
- Stakeholder information

**Example**:
```text
❌ Without context:
"How should I handle this error?"

✅ With context:
"I'm building a REST API in Python using FastAPI. When a user 
submits a form with an invalid email format, I get a 422 
Validation Error. The form is used by customers on our 
public website.

How should I handle this error?"
```text
**Industry Guidance**:
- **Google Gemini**: "Add contextual information to help the model understand constraints and details"
- **OpenAI**: "Provide relevant context that affects how the response should be generated"
- **Anthropic**: "Be clear about what you want Claude to know before responding"

---

### 2. Role (Persona)

**Purpose**: Tells the AI what expertise and perspective to bring to the response.

**Common Role Patterns**:

| Pattern | Example | Best For |
|---------|---------|----------|
| **Expert** | "You are a senior security engineer..." | Technical depth |
| **Reviewer** | "You are a code reviewer focusing on..." | Critical analysis |
| **Teacher** | "You are explaining to a junior developer..." | Clarity |
| **Consultant** | "You are a business consultant..." | Strategic advice |

**Example**:
```text
You are a senior DevOps engineer with 10 years of experience 
in cloud infrastructure and container orchestration.

Review this Kubernetes deployment configuration and identify 
potential issues for a production environment.
```text
**Industry Guidance**:
- **Anthropic**: "Assigning Claude a role can help establish the right perspective and expertise level"
- **OpenAI**: "System messages can set the behavior and persona"
- **Google Gemini**: "Define role definitions in System Instructions or at the beginning of prompts"

---

### 3. Task

**Purpose**: The core of your prompt—what you actually need accomplished.

**Characteristics of Good Tasks**:
- ☑️ **Specific** — Name exactly what you need
- ☑️ **Actionable** — Use clear action verbs
- ☑️ **Scoped** — Define boundaries
- ☑️ **Measurable** — Include success criteria when relevant

**Example**:
```text
❌ Weak task:
"Tell me about databases."

✅ Strong task:
"Compare PostgreSQL and MongoDB for a new e-commerce 
application that needs to handle 10,000 concurrent users, 
focusing on:
1. Query performance for product searches
2. Transaction handling for orders
3. Operational complexity for a team of 3 developers"
```sql
**Industry Guidance**:
- **OpenAI**: "Be specific, descriptive, and as detailed as possible about the desired context, outcome, length, format, style"
- **Google Gemini**: "State your goal clearly and concisely. Avoid unnecessary or overly persuasive language."
- **Anthropic**: "Break complex tasks into clear, sequential steps"

---

### 4. Format

**Purpose**: Tells the AI how to structure its output.

**Common Format Specifications**:

```markdown
# List format
"Provide as a numbered list of 5 items"

# Table format
"Present in a table with columns: Feature, Pros, Cons, Use Case"

# Code format
"Return as a Python function with docstrings and type hints"

# Structured document
"Write as a technical specification with sections for:
1. Overview
2. Requirements
3. Implementation
4. Testing"

# JSON/Data format
"Return as valid JSON matching this schema: {name: string, items: array}"
```json
**Example**:
```json
Format your response as a markdown table with the following columns:
| Tool | Pros | Cons | Best For | Cost |
```json
**Industry Guidance**:
- **OpenAI**: "Articulate the desired output format through examples. Show, and tell."
- **Google Gemini**: "Give instructions that specify the format of the response—table, bulleted list, JSON, paragraph"
- **Anthropic**: "Use XML tags to clearly delineate different parts of your prompt and expected output"

---

### 5. Constraints

**Purpose**: Sets boundaries on what to include, exclude, or limit.

**Types of Constraints**:

| Type | Example |
|------|---------|
| **Length** | "Maximum 200 words" |
| **Scope** | "Focus only on frontend concerns" |
| **Exclusions** | "Do not include deprecated methods" |
| **Requirements** | "Must work with Python 3.8+" |
| **Quality** | "Production-ready with error handling" |

**Example**:
```yaml
Constraints:
- Maximum 500 words
- Use only standard library (no external dependencies)
- Must handle edge cases: empty input, None values, invalid types
- Include type hints
- No print statements in production code
```text
**Industry Guidance**:
- **OpenAI**: "Reduce 'fluffy' and imprecise descriptions. Use '3 to 5 sentence paragraph' not 'fairly short'"
- **Google Gemini**: "Specify any constraints on reading the prompt or generating a response"
- **Anthropic**: "Set clear boundaries and be explicit about what you don't want"

---

### 6. Examples (Few-Shot Learning)

**Purpose**: Demonstrates the pattern you want the AI to follow.

**When to Use Examples**:
- ✅ Custom output formats
- ✅ Classification or categorization tasks
- ✅ Tone/style matching
- ✅ Domain-specific terminology
- ✅ When instructions alone are ambiguous

**Example**:
```yaml
Classify these support tickets by category and priority.

Examples:
Input: "The server is responding slowly during peak hours"
Output: Category: Performance, Priority: Medium, Team: Infrastructure

Input: "Cannot log in, getting 403 error"
Output: Category: Authentication, Priority: High, Team: Security

Now classify:
Input: "Dashboard graphs not loading on mobile devices"
```text
**Industry Guidance**:
- **Google Gemini**: "We recommend to always include few-shot examples in your prompts. Prompts without few-shot examples are likely to be less effective."
- **OpenAI**: "Start with zero-shot, then few-shot, then fine-tune if needed"
- **Anthropic**: "Provide multishot examples to establish patterns"

**Best Practices for Examples**:
1. Use **consistent formatting** across all examples
2. Show **positive patterns** (what to do) rather than anti-patterns (what not to do)
3. Include **3-5 examples** for complex tasks (more isn't always better)
4. Ensure examples are **realistic and representative**

---

### 7. Tone

**Purpose**: Shapes the voice and style of the response.

**Tone Dimensions**:

| Dimension | Range |
|-----------|-------|
| **Formality** | Casual ↔ Formal |
| **Technical level** | Beginner ↔ Expert |
| **Emotion** | Neutral ↔ Enthusiastic ↔ Empathetic |
| **Brevity** | Concise ↔ Detailed |

**Example**:
```yaml
Tone: Professional but approachable. Assume the reader is a 
business analyst with limited technical background. Avoid 
jargon—when technical terms are necessary, provide brief 
explanations in parentheses.
```text
**Industry Guidance**:
- **Google Gemini**: "Control output verbosity—by default Gemini 3 provides direct answers. Explicitly request conversational or detailed responses if needed."
- **Microsoft 365**: "Specify audience and tone in the CARE framework"

---

## Prompt Structure Patterns

### Pattern 1: RTF (Role-Task-Format)

**Usage**: 68% of top-rated prompts use this pattern

```text
You are a [ROLE].

Your task is to [TASK].

Provide output in the following format:
[FORMAT_SPECIFICATION]
```text
**Best For**: Software development, business analysis, reporting

---

### Pattern 2: RACE Framework

```text
[ROLE]    - Who you want the AI to be
[ACTION]  - What you want done
[CONTEXT] - Background information
[EXPECTATION] - Desired outcome/format
```text
**Best For**: Business communications, document generation

---

### Pattern 3: CARE Framework (Microsoft 365)

```yaml
Context: [BACKGROUND_INFORMATION]
Action: [WHAT_YOU_WANT]
Result: [EXPECTED_OUTPUT]
Example: [SAMPLE_OUTPUT]
```sql
**Best For**: Microsoft 365 Copilot, business communications

---

### Pattern 4: The Four S's (GitHub Copilot)

1. **Single**: One task per prompt
2. **Specific**: Detailed, explicit instructions
3. **Short**: Concise but information-rich
4. **Surround**: Use context from open files

**Best For**: Code generation, inline suggestions

---

### Pattern 5: Context-Task-Constraints (Technical)

```yaml
Context: [SITUATION_AND_BACKGROUND]
Task: [WHAT_NEEDS_TO_BE_DONE]
Constraints: [LIMITATIONS_AND_REQUIREMENTS]
```text
**Best For**: Technical tasks, code review, debugging

---

### Pattern 6: XML-Structured (Anthropic/Gemini)

```xml
<role>
You are a [specific expert].
</role>

<constraints>
1. [Constraint 1]
2. [Constraint 2]
</constraints>

<context>
[Insert relevant background information]
</context>

<task>
[Insert specific request]
</task>
```text
**Best For**: Complex multi-part prompts, Claude/Gemini

---

## Platform-Specific Guidelines

### GitHub Copilot

**Key Principles**:
- Use comments above code for context
- Open related files for better suggestions
- Keep prompts short (< 200 words)
- Specify language version and libraries
- Include example inputs/outputs

**Template**:
```python
# Write a Python function that validates email addresses
# Input: string (email address)
# Output: boolean (True if valid, False if invalid)
# Requirements:
# - Use regex for validation
# - Handle common edge cases (empty, None, no @ symbol)
# - Include type hints
def validate_email(email: str) -> bool:
    # Implementation here
```text
---

### Claude (Anthropic)

**Key Principles**:
- Use XML tags for complex structure
- Longer, detailed prompts work well
- Request reasoning explicitly
- Assign roles/personas for expertise
- Use `<thinking>` tags for chain-of-thought

**Template**:
```xml
<role>You are a senior software architect.</role>

<context>
We're evaluating whether to migrate from a monolithic 
architecture to microservices.
</context>

<task>
Analyze the trade-offs and provide a recommendation.
</task>

<format>
Structure your response with:
1. Executive Summary
2. Trade-off Analysis
3. Recommendation with Rationale
</format>
```text
---

### OpenAI (GPT-4/o1)

**Key Principles**:
- Put instructions at the beginning
- Use delimiters (""", ###) to separate sections
- Be specific about format and length
- Use leading words to nudge output direction
- Articulate output format through examples

**Template**:
```text
Summarize the text below as a bullet point list of the most 
important points.

Text: """
{text input here}
"""

Format: 5-7 bullet points, each point should be one sentence.
```text
---

### Microsoft 365 Copilot

**Key Principles**:
- Use natural, conversational language
- Specify audience and tone
- Reference connected documents
- Use the CARE pattern
- Ask for specific output formats

**Template**:
```yaml
Context: I'm preparing for a quarterly business review with 
the executive team.

Action: Summarize the attached sales report and create 
talking points.

Result: Executive summary with 5 key insights and 3 
recommendations.

Example: "Sales increased 15% YoY, driven by enterprise 
accounts" - this level of specificity.
```text
---

### Google Gemini

**Key Principles**:
- Be precise and direct
- Use consistent structure (XML or Markdown)
- Define parameters explicitly
- Place critical instructions at the beginning
- Use anchoring after large context blocks

**Template (Gemini 3)**:
```markdown
# Identity
You are a senior solution architect.

# Constraints
- No external libraries allowed
- Python 3.11+ syntax only

# Context
[Insert relevant background]

# Task
[Insert specific request]

# Output format
Return a single code block with comments.
```text
---

## Advanced Techniques

### Chain-of-Thought (CoT) Prompting

**Purpose**: Encourages step-by-step reasoning for complex problems.

**Research Foundation**: Wei et al. (NeurIPS 2022) - improves reasoning by 20-40%

**Template**:
```text
Think through this step by step:

Step 1: Understanding
- Restate the problem
- Identify key challenges

Step 2: Analysis
- Break down the problem
- Consider alternatives

Step 3: Solution
- Propose approach
- Justify reasoning

Step 4: Implementation
- Outline concrete steps
- Note potential risks

Show your reasoning at each step.
```text
**Best For**: Debugging, complex analysis, math/logic problems

---

### Tree-of-Thoughts (ToT) Prompting

**Purpose**: Explores multiple solution paths before selecting the best.

**Research Foundation**: Yao et al. (NeurIPS 2023)

**Template**:
```sql
Evaluate multiple approaches for [PROBLEM].

**Approach A: Conservative**
- Description: [APPROACH_1]
- Pros: [BENEFITS]
- Cons: [DRAWBACKS]
- Score: [1-10]

**Approach B: Balanced**
- Description: [APPROACH_2]
- Pros: [BENEFITS]
- Cons: [DRAWBACKS]
- Score: [1-10]

**Approach C: Innovative**
- Description: [APPROACH_3]
- Pros: [BENEFITS]
- Cons: [DRAWBACKS]
- Score: [1-10]

**Recommendation**: Based on scores and trade-offs, select 
the best approach and explain why.
```text
**Best For**: Architecture decisions, strategic planning, trade-off analysis

---

### ReAct (Reasoning + Acting)

**Purpose**: Combines reasoning with action-taking for tool-augmented tasks.

**Template**:
```text
Use the ReAct pattern to solve [TASK].

**Think**: What information do I need? What tools can help?
**Act**: [USE_TOOL] with [PARAMETERS]
**Observe**: [RESULT_FROM_TOOL]
**Reflect**: Did this get me closer to the goal? What's next?

Repeat until task is complete.

**Available Tools**:
- [TOOL_1]: [DESCRIPTION]
- [TOOL_2]: [DESCRIPTION]

Output format: Show each Think-Act-Observe-Reflect cycle clearly.
```text
**Best For**: Research, data analysis, multi-step workflows, RAG patterns

---

### Self-Critique / Reflection

**Purpose**: Model reviews and improves its own output.

**Template**:
```text
Before returning your final response, review your generated 
output against the user's original constraints:

1. Did I answer the user's *intent*, not just their literal words?
2. Is the output complete and accurate?
3. Are there any errors or inconsistencies?
4. Is the tone appropriate for the audience?

If you find issues, correct them before presenting the final answer.
```text
**Best For**: Quality improvement, iterative refinement, high-stakes outputs

---

## Quality Evaluation Criteria

Based on our GitHub Models evaluation framework and industry standards:

### The 8 Criteria

| Criterion | Weight | Description | What to Check |
|-----------|--------|-------------|---------------|
| **Clarity** | 15% | Goal is unambiguous | Single clear objective, no confusion |
| **Specificity** | 15% | Instructions are detailed | Concrete details, not vague |
| **Actionability** | 15% | AI can act on instructions | Clear verbs, defined scope |
| **Structure** | 12.5% | Well-organized format | Logical flow, consistent format |
| **Completeness** | 12.5% | All necessary info included | Context, constraints, examples |
| **Factuality** | 10% | Guides accurate outputs | No misleading info, verifiable |
| **Consistency** | 10% | Produces reliable results | Reproducible, predictable |
| **Safety** | 10% | Prevents harmful outputs | No PII exposure, ethical |

### Pass/Fail Thresholds

- **Overall Score**: ≥ 7.0/10 to pass
- **Individual Criterion**: No score below 5.0/10
- **Critical Flags**: Any safety or factuality score < 5.0 is automatic fail

### Score Interpretation

| Score Range | Tier | Quality Level | Action |
|-------------|------|---------------|--------|
| 9.0-10.0 | A | Exceptional | Reference example |
| 8.0-8.9 | B+ | Strong | Production ready |
| 7.0-7.9 | B | Good | Minor improvements |
| 5.0-6.9 | C | Needs Work | Significant revision |
| <5.0 | F | Poor | Major rewrite needed |

---

## Common Mistakes and Fixes

### ❌ Being Too Vague

**Problem**: "Help me with my code"

**Fix**: Specify what kind of help—debug, optimize, refactor, document

```text
Review this Python function for:
1. Security vulnerabilities
2. Performance bottlenecks
3. Code style and best practices
```text
---

### ❌ Overloading a Single Prompt

**Problem**: Asking for 10 different things at once

**Fix**: Break complex tasks into focused prompts or use numbered steps

```text
Step 1: Analyze the current state
Step 2: Identify issues
Step 3: Propose solutions
Step 4: Create implementation plan
```text
---

### ❌ Ignoring Output Format

**Problem**: Getting unstructured text when you need JSON

**Fix**: Always specify the exact format needed

```json
Return as valid JSON:
{
  "summary": "string",
  "findings": ["string"],
  "recommendations": ["string"]
}
```json
---

### ❌ Saying What NOT to Do

**Problem**: "Don't be too technical"

**Fix**: Say what to do instead

```text
✅ "Explain in terms a business analyst would understand. 
When technical terms are necessary, provide brief 
explanations in parentheses."
```text
**Industry Evidence**: Google Gemini documentation explicitly states "Using examples to show patterns is more effective than showing anti-patterns to avoid"

---

### ❌ Hardcoding Values

**Problem**: Writing prompts that only work for one specific case

**Fix**: Use `[PLACEHOLDERS]` for reusability

```sql
Analyze [DATA_TYPE] from [TIME_PERIOD] focusing on [METRIC].
```text
---

### ❌ Missing Examples

**Problem**: Expecting AI to guess desired output style

**Fix**: Provide at least one example input/output pair

```text
Example:
Input: "Server CPU at 95% for 10 minutes"
Output: {"severity": "high", "category": "performance", 
         "action": "scale-up"}

Now classify: [YOUR_INPUT]
```text
---

### ❌ Embedding Secrets

**Problem**: Including API keys, passwords, or PII

**Fix**: Use placeholder variables

```text
✅ Use [API_KEY] instead of actual values
✅ Use [USER_EMAIL] instead of real emails
```text
---

## Templates and Checklists

### Prompt Quality Checklist

Before using or submitting a prompt, verify:

**Structure**
- [ ] Clear, descriptive title
- [ ] Appropriate category and tags
- [ ] Goal is explicitly stated
- [ ] All placeholders are documented

**Content**
- [ ] Specific instructions provided
- [ ] Necessary context included
- [ ] Output format defined
- [ ] Constraints specified
- [ ] At least one example included

**Technical**
- [ ] Appropriate reasoning style chosen
- [ ] Edge cases addressed
- [ ] No embedded secrets or PII
- [ ] Variables use `[BRACKET]` format

**Usability**
- [ ] Easy to customize
- [ ] Tips for better results included
- [ ] Related prompts linked (if applicable)

---

### Standard Prompt Template

```yaml
---
title: "[Descriptive Title]"
category: "[developers|business|analysis|creative|advanced|governance]"
tags: ["tag1", "tag2", "tag3"]
author: "Your Name"
version: "1.0"
date: "YYYY-MM-DD"
difficulty: "beginner|intermediate|advanced"
platform: "Claude|GPT-4|Copilot|Universal"
governance_tags: ["PII-safe"]
---

# [Title]

## Description

[2-3 sentences describing what this prompt does and when to use it]

## Use Cases

- [Specific use case 1]
- [Specific use case 2]
- [Specific use case 3]

## Prompt

```text
[Your prompt here with [PLACEHOLDERS] for variables]
```text
## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[VAR_1]` | What this variable represents | "example value" |
| `[VAR_2]` | What this variable represents | "example value" |

## Example Usage

**Input:**
```text
[Show the prompt with placeholders filled in]
```text
**Output:**
```text
[Show expected AI response]
```text
## Tips

- Tip 1 for getting better results
- Tip 2 for customization
- Tip 3 for edge cases
- Tip 4 for iteration
- Tip 5 for advanced use

## Related Prompts

- [Related Prompt 1](link)
- [Related Prompt 2](link)
```text
---

### Quick Pattern Selection Guide

| If You Need... | Use This Pattern | Components |
|----------------|------------------|------------|
| Simple task | Task only | Task |
| Code generation | RTF + Four S's | Role, Task, Format |
| Business document | CARE | Context, Action, Result, Example |
| Complex analysis | RTF + CoT | Role, Task, Format, Chain-of-Thought |
| Architecture decision | ToT | Multiple approaches, scoring, recommendation |
| Research task | ReAct | Think-Act-Observe-Reflect cycles |
| Multi-part prompt | XML Structure | Tags for each section |

---

## Industry Best Practices Summary

### OpenAI Key Rules

1. **Use the latest model** for best results
2. **Put instructions at the beginning** and use delimiters
3. **Be specific** about context, outcome, length, format, style
4. **Articulate output format through examples** (show, don't just tell)
5. **Start zero-shot, then few-shot**, then fine-tune if needed
6. **Reduce fluffy descriptions** ("3-5 sentences" not "fairly short")
7. **Say what to do**, not what NOT to do
8. **Use leading words** to nudge toward patterns (e.g., "import" for Python)

### Anthropic Key Rules

1. **Be clear and direct** about what you want
2. **Use XML tags** for complex prompts
3. **Provide multishot examples** for consistent outputs
4. **Break complex tasks** into steps
5. **Request thinking/reasoning** explicitly when needed
6. **Set clear constraints** and boundaries
7. **Assign personas** for specific expertise

### Google Gemini Key Rules

1. **Be precise and direct** - avoid unnecessary language
2. **Use consistent structure** - XML or Markdown throughout
3. **Define parameters explicitly** - explain ambiguous terms
4. **Prioritize critical instructions** at the beginning
5. **Always include few-shot examples** - they're more effective than instructions alone
6. **Use positive patterns** - show what to do, not what to avoid
7. **For complex tasks**: Plan → Execute → Validate → Format

### Microsoft/GitHub Copilot Key Rules

1. **Single task per prompt** - break complex requests apart
2. **Specific and detailed** - explicit instructions
3. **Short but information-rich** - concise context
4. **Use surrounding context** - open related files
5. **Comments drive suggestions** - natural language above code
6. **Specify versions** - language, framework, library versions

---

## Summary

Creating effective prompts is a skill that improves with practice and systematic application of proven patterns. Remember:

1. **Start with the basics**: Task + Context + Format covers most needs
2. **Add components as needed**: Role, Constraints, Examples, Tone
3. **Match patterns to platforms**: Each AI has preferences
4. **Use advanced techniques** for complex tasks: CoT, ToT, ReAct
5. **Evaluate against criteria**: 8 dimensions, ≥7.0 overall to pass
6. **Iterate based on results**: Prompting is rarely perfect on the first try

**Target Quality**:
- Production prompts: 85+ score, Tier A-B
- General use: 70-84 score, Tier B
- No individual criterion below 5.0

---

## Resources

### Repository Documentation

- [Prompt Template](../templates/prompt-template.md)
- [Prompt Improvement Template](../templates/prompt-improvement-template.md)
- [Reference Cheat Sheet](../reference/cheat-sheet.md)
- [Prompt Anatomy](../concepts/prompt-anatomy.md)
- [Best Practices](best-practices.md)
- [Ultimate Prompting Guide](ultimate-prompting-guide.md)

### Evaluation Tools

- [Prompt Quality Evaluator](../prompts/system/prompt-quality-evaluator.md)
- [GitHub Models Evaluation System](../testing/evals/README.md)

### External Resources

- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/constructing-a-prompt)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [Google Gemini Prompting Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Microsoft 365 Copilot Adoption](https://adoption.microsoft.com/en-us/copilot/)

### Research Papers

- Wei et al. (NeurIPS 2022): "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- Yao et al. (NeurIPS 2023): "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
- "The Prompt Report" (arXiv:2406.06608): Comprehensive taxonomy of prompting techniques

---

*Version 1.0 | Last Updated: 2025-12-01 | Prompts Library Team*
