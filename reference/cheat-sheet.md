---
title: Prompt Engineering Cheat Sheet
shortTitle: Cheat Sheet
intro: Quick-reference patterns and templates for common prompting scenarios.
type: reference
difficulty: beginner
audience:
  - junior-engineer
  - senior-engineer
  - solution-architect
  - business-analyst
  - project-manager
platforms:
  - github-copilot
  - claude
  - chatgpt
  - azure-openai
  - m365-copilot
topics:
  - fundamentals
  - patterns
author: Prompt Library Team
version: '1.0'
date: '2025-12-02'
governance_tags:
  - PII-safe
dataClassification: public
reviewStatus: approved
---

# Prompt Engineering Cheat Sheet

Quick-reference patterns and templates for common prompting tasks. Print this page or keep it open while crafting prompts.

---

## Universal Prompt Structure

```text
[ROLE] You are a [persona with expertise].

[CONTEXT] I'm working on [situation] and need help with [specific challenge].

[TASK] Please [specific action verb] that [desired outcome].

[FORMAT] Provide your response as [format specification].

[CONSTRAINTS] Important: [limitations, requirements, things to avoid].
```text
---

## Quick Patterns

### Give the AI a Role

```text
You are an experienced [role] who specializes in [specialty].
```text
**Examples:**
- `You are an experienced software architect who specializes in microservices.`
- `You are a technical writer who excels at making complex topics accessible.`
- `You are a security engineer focused on web application vulnerabilities.`

### Specify Output Format

```text
Format your response as:
- [format type]
- [length constraint]
- [structure requirements]
```text
**Examples:**
- `Format as a numbered list with no more than 5 items.`
- `Return valid JSON with keys: summary, recommendations, priority.`
- `Write in bullet points, maximum 100 words total.`

### Add Constraints

```text
Important constraints:
- [must include]
- [must avoid]
- [scope limitation]
```text
**Examples:**
- `Use only Python standard library, no external packages.`
- `Do not include any deprecated APIs.`
- `Focus only on the authentication flow, not the full system.`

---

## Task-Specific Templates

### Code Review

```text
Review this code for:
1. Security vulnerabilities
2. Performance issues
3. Maintainability concerns

Code:
```[language]
[code here]
```text
For each issue found, provide:
- Location (line/section)
- Severity (high/medium/low)
- Explanation
- Suggested fix
```text
### Explain Code

```text
Explain this code as if teaching a [junior/senior] developer:

```[language]
[code here]
```yaml
Include:
- What it does (high-level purpose)
- How it works (step by step)
- Why key decisions were made
- Potential gotchas or edge cases
```text
### Debug Assistance

```text
I'm experiencing this error:
```text
[error message]
```yaml
Context:
- Language/Framework: [tech stack]
- What I was trying to do: [action]
- What I expected: [expected behavior]
- What happened: [actual behavior]

Help me:
1. Understand why this error occurs
2. Identify the root cause in my code
3. Provide a fix with explanation
```text
### Generate Tests

```text
Generate [unit/integration] tests for this code:

```[language]
[code here]
```yaml
Requirements:
- Use [testing framework]
- Cover happy path and edge cases
- Include descriptive test names
- Add comments explaining each test's purpose
```text
### Write Documentation

```text
Write documentation for this [function/class/API]:

```[language]
[code here]
```yaml
Include:
- Brief description
- Parameters with types and descriptions
- Return value
- Example usage
- Edge cases or limitations
```text
### Summarize Content

```text
Summarize this [document/article/meeting notes] for [audience]:

[content here]

Format:
- Executive summary (2-3 sentences)
- Key points (bullet list, max 5)
- Action items (if any)
- Questions or concerns raised
```text
### Draft Communication

```text
Draft a [email/message/announcement] for [audience]:

Purpose: [what you want to communicate]
Tone: [formal/casual/urgent]
Key points to include:
- [point 1]
- [point 2]

Constraints:
- Maximum [X] sentences
- [any specific requirements]
```text
---

## Advanced Patterns

### Chain-of-Thought

```text
Think through this step by step:

[problem or question]

For each step:
1. State what you're considering
2. Explain your reasoning
3. Note any assumptions

Then provide your final answer.
```text
### Few-Shot Learning

```text
Here are examples of the format I need:

Input: [example 1 input]
Output: [example 1 output]

Input: [example 2 input]
Output: [example 2 output]

Now process this:
Input: [actual input]
Output:
```text
### Self-Critique

```text
After providing your response:
1. List potential weaknesses or gaps
2. Rate your confidence (high/medium/low)
3. Suggest what additional information would improve the answer
```text
### Structured Analysis

```text
Analyze [topic/situation] using this framework:

1. **Current State**: What exists now?
2. **Desired State**: What should exist?
3. **Gap Analysis**: What's the difference?
4. **Options**: What are possible approaches?
5. **Recommendation**: What do you suggest and why?
```text
---

## Format Specifiers

| Want This | Say This |
|-----------|----------|
| Bullet list | "Format as a bullet list" |
| Numbered steps | "Provide as numbered steps" |
| Table | "Format as a markdown table with columns: X, Y, Z" |
| JSON | "Return as valid JSON with this structure: {...}" |
| Code only | "Return only the code, no explanation" |
| Short answer | "Answer in one sentence" |
| Detailed | "Provide a comprehensive explanation" |
| Comparison | "Compare in a table with pros/cons" |

---

## Length Controls

| Want | Say |
|------|-----|
| Very short | "Maximum 1-2 sentences" |
| Concise | "Keep it under 100 words" |
| Moderate | "Approximately 200-300 words" |
| Detailed | "Provide a thorough explanation (500+ words)" |
| Exact | "Exactly 5 bullet points" |

---

## Tone Adjustments

| Tone | Phrase |
|------|--------|
| Formal | "Use formal, professional language suitable for executive audience" |
| Casual | "Keep it conversational and friendly" |
| Technical | "Use technical terminology appropriate for senior engineers" |
| Simple | "Explain in plain language a non-technical person could understand" |
| Urgent | "Communicate with appropriate urgency" |

---

## Common Fixes

| Problem | Solution |
|---------|----------|
| Too long | Add "Maximum X words/sentences/points" |
| Too short | Add "Elaborate with examples and details" |
| Too generic | Add specific context about your situation |
| Wrong format | Add explicit format instructions with examples |
| Off-topic | Add "Focus specifically on X. Do not discuss Y." |
| Inconsistent | Add few-shot examples showing exact format |
| Too technical | Add "Explain for someone with [level] experience" |
| Not actionable | Add "Provide specific, actionable recommendations" |

---

## Quick Debugging

When a prompt isn't working:

1. **Check the basics**: Is your request clear and unambiguous?
2. **Add context**: Does the AI know your situation?
3. **Specify format**: Did you tell it exactly how to respond?
4. **Add constraints**: Are there things it should avoid?
5. **Give examples**: Would showing the desired output help?

---

## Platform Quick Tips

### GitHub Copilot
- Write detailed comments before code
- Include function signatures first
- Use descriptive variable names

### ChatGPT/Claude
- Use system prompts for consistent behavior
- Summarize long conversations
- Break complex tasks into steps

### M365 Copilot
- Reference specific files by name
- Be explicit about data sources
- Use natural language queries

---

## See Also

- [Platform Comparison](/reference/platform-comparison) — Detailed platform differences
- [Glossary](/reference/glossary) — Term definitions
- [Troubleshooting](/troubleshooting/) — Fix common issues
- [Advanced Patterns](/concepts/about-advanced-patterns) — Deep dive on techniques
