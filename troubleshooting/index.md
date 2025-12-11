---
title: Troubleshooting
shortTitle: Troubleshooting
intro: Solutions to common issues when working with AI prompts and models.
type: troubleshooting
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
author: Prompt Library Team
version: '1.0'
date: '2025-11-29'
governance_tags:
  - PII-safe
dataClassification: public
reviewStatus: approved
layout: category-landing
children:
  - /troubleshooting/common-issues
  - /troubleshooting/model-specific
  - /troubleshooting/prompt-debugging
featuredLinks:
  gettingStarted:
    - /get-started/quickstart-copilot
  popular:
    - /troubleshooting/common-issues
---

# Troubleshooting

Find solutions to common problems encountered when working with AI prompts and models.

## Quick Diagnosis

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Response too long/verbose | Missing length constraints | Add "maximum X words" or "be concise" |
| Response too short | Insufficient detail request | Ask to "elaborate" or "provide details" |
| Wrong format | No format specification | Explicitly specify output format |
| Off-topic response | Ambiguous prompt | Add more context or constraints |
| Hallucinated information | Model uncertainty | Ask for sources or verification |
| Inconsistent outputs | No examples provided | Add few-shot examples |
| Wrong expertise level | Missing role/audience | Specify persona or target audience |

## In This Section

| Guide | Description |
|-------|-------------|
| [Common Issues](/troubleshooting/common-issues) | Solutions to frequently encountered problems |
| [Model-Specific Issues](/troubleshooting/model-specific) | Troubleshooting per AI platform |
| [Prompt Debugging](/troubleshooting/prompt-debugging) | Systematic approach to fixing prompts |

---

## General Troubleshooting Steps

When a prompt isn't working as expected, follow this systematic approach:

### 1. Verify the Basics

- Is your prompt clear and unambiguous?
- Does it include necessary context?
- Are there conflicting instructions?

### 2. Check the Output Gap

- What did you expect vs. what did you get?
- Is it a format issue, content issue, or quality issue?
- Is the problem consistent or intermittent?

### 3. Apply Targeted Fixes

- **Wrong format** → Add explicit format instructions
- **Missing information** → Add context or examples
- **Wrong tone** → Specify the desired tone/audience
- **Too long/short** → Add length constraints
- **Off-topic** → Narrow the scope with constraints

### 4. Test Incrementally

- Change one thing at a time
- Test each change before adding more
- Document what works and what doesn't

---

## Common Quick Fixes

### Response Is Too Generic

**Problem:** AI gives surface-level, generic answers

**Fixes:**
1. Add specific context about your situation
2. Ask for "specific examples" or "concrete recommendations"
3. Provide constraints that force depth ("considering X, Y, Z factors")

### Response Keeps Repeating Itself

**Problem:** AI restates the same points multiple ways

**Fixes:**
1. Add "be concise and avoid repetition"
2. Specify exact number of points ("provide exactly 3 distinct reasons")
3. Request bullet points instead of paragraphs

### AI Won't Follow Instructions

**Problem:** Model ignores parts of your prompt

**Fixes:**
1. Put critical instructions at the beginning AND end of prompt
2. Use numbered steps for complex instructions
3. Break complex prompts into simpler sequential requests
4. Use emphasis (bold, caps) for crucial requirements

### Inconsistent Results

**Problem:** Same prompt gives different results each time

**Fixes:**
1. Add few-shot examples showing desired output
2. Lower temperature setting (if available)
3. Make instructions more explicit
4. Use structured output formats (JSON, tables)

---

## Related Resources

- [About Prompt Engineering](/concepts/about-prompt-engineering) — Fundamentals
- [Best Practices](/guides/best-practices) — Prevention is better than cure
- [Advanced Patterns](/concepts/about-advanced-patterns) — Techniques for complex tasks

---

## Still Stuck?

If you've tried the guides in this section and still have issues:

1. **Check platform documentation** — Model-specific limitations may apply
2. **Simplify your prompt** — Start with a minimal working prompt and add complexity
3. **Try a different approach** — Sometimes rephrasing achieves better results
4. **Consider the task** — Some tasks may be beyond current AI capabilities
