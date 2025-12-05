---
title: Common Prompt Issues and Solutions
shortTitle: Common Issues
intro: Solutions to the most frequently encountered problems when working with AI prompts.
type: troubleshooting
difficulty: beginner
audience:
  - junior-engineer
  - senior-engineer
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
---

# Common Prompt Issues and Solutions

This guide covers the most frequently encountered issues when working with AI prompts and provides tested solutions.

## Output Quality Issues

### Issue: Response Is Too Long

**Symptoms:**
- AI provides walls of text when you need concise answers
- Output includes unnecessary explanations or caveats
- Response takes too long to read and process

**Solutions:**

1. **Add explicit length constraints:**
   ```
   Limit your response to 3 sentences maximum.
   ```

2. **Request specific format:**
   ```
   Provide your answer as a single paragraph of no more than 100 words.
   ```

3. **Ask for summary first:**
   ```
   Start with a one-sentence summary, then provide details only if essential.
   ```

### Issue: Response Is Too Short

**Symptoms:**
- AI gives one-line answers when you need detailed explanations
- Missing important nuances or considerations
- Feels like the response was cut off

**Solutions:**

1. **Request elaboration explicitly:**
   ```
   Provide a detailed explanation with at least 3 supporting points.
   ```

2. **Ask for specific sections:**
   ```
   Include sections for: Background, Analysis, Recommendations, and Next Steps.
   ```

3. **Use depth cues:**
   ```
   Explain thoroughly as if teaching someone unfamiliar with the topic.
   ```

### Issue: Response Is Generic/Superficial

**Symptoms:**
- Answers could apply to any situation
- Missing specific, actionable recommendations
- Feels like boilerplate content

**Solutions:**

1. **Add specific context:**
   ```
   Context: I'm a frontend developer at a fintech startup with 5 engineers, using React and TypeScript. Our main challenge is...
   ```

2. **Request concrete examples:**
   ```
   Include specific code examples that I can adapt for my situation.
   ```

3. **Add constraints that force specificity:**
   ```
   Considering our budget of $5,000/month and team size of 3, what would you recommend?
   ```

## Format Issues

### Issue: Wrong Output Format

**Symptoms:**
- Asked for JSON, got prose
- Asked for bullet points, got paragraphs
- Output doesn't match your system requirements

**Solutions:**

1. **Be explicit about format:**
   ```
   Return your response as valid JSON with the following structure:
   {
     "summary": "string",
     "recommendations": ["string"],
     "priority": "high|medium|low"
   }
   ```

2. **Provide format examples:**
   ```
   Format each item like this:
   - **Term**: Definition (use case)
   
   Example:
   - **API Gateway**: A server that acts as an intermediary (microservices architectures)
   ```

3. **Specify what NOT to include:**
   ```
   Return only the JSON object. Do not include any explanation, markdown code fences, or additional text.
   ```

### Issue: Inconsistent Formatting Across Responses

**Symptoms:**
- Same prompt produces differently formatted outputs
- Hard to parse or process outputs programmatically
- Quality varies between interactions

**Solutions:**

1. **Use few-shot examples:**
   ```
   Here are examples of the exact format I need:
   
   Input: "Server timeout error"
   Output: [ERROR] Server | Timeout | Retry in 5s
   
   Input: "Authentication failed"  
   Output: [ERROR] Auth | Invalid credentials | Check API key
   
   Now process: "Database connection lost"
   ```

2. **Use structured templates:**
   ```
   Fill in this exact template:
   
   ## Summary
   [1-2 sentences]
   
   ## Key Points
   - Point 1
   - Point 2
   - Point 3
   
   ## Recommendation
   [Single actionable sentence]
   ```

## Content Issues

### Issue: Hallucinated or Incorrect Information

**Symptoms:**
- AI confidently states incorrect facts
- Made-up citations or references
- Technical details that don't exist

**Solutions:**

1. **Ask for verification:**
   ```
   For each fact you mention, indicate your confidence level (high/medium/low).
   ```

2. **Request sources:**
   ```
   Only include information you're highly confident about. If you're uncertain, say so explicitly.
   ```

3. **Cross-reference important information:**
   ```
   After your response, list any claims that should be verified against official documentation.
   ```

### Issue: Response Misses the Point

**Symptoms:**
- AI answers a different question than asked
- Important aspects of the request ignored
- Focus on wrong part of the prompt

**Solutions:**

1. **Front-load critical requirements:**
   ```
   IMPORTANT: Focus specifically on security implications. Do not discuss performance or cost.
   
   [rest of prompt]
   ```

2. **Use structured prompts:**
   ```
   Question: [your specific question]
   
   Required in response:
   1. [must-have element]
   2. [must-have element]
   
   Not needed:
   - [element to exclude]
   ```

3. **Rephrase as explicit task:**
   ```
   Your task is to [specific action]. You will be evaluated on [criteria].
   ```

## Behavioral Issues

### Issue: AI Won't Complete the Task

**Symptoms:**
- Model refuses to help
- Gets stuck in excessive caveats
- Keeps asking for clarification instead of proceeding

**Solutions:**

1. **Provide missing context:**
   ```
   This is for a fictional scenario / educational example / internal documentation.
   ```

2. **Break into smaller steps:**
   ```
   Let's work through this step by step. First, just outline the approach without implementing it.
   ```

3. **Reframe the request:**
   ```
   I'm learning about [topic]. Can you explain how [thing] works in general terms?
   ```

### Issue: Response Contradicts Itself

**Symptoms:**
- Early parts of response conflict with later parts
- Recommendations don't align with stated reasoning
- Confusing or circular logic

**Solutions:**

1. **Request structured reasoning:**
   ```
   Think through this step by step:
   1. First, state your assumptions
   2. Then, analyze the key factors
   3. Finally, provide your recommendation based on the analysis above
   ```

2. **Ask for consistency check:**
   ```
   After providing your analysis, verify that your conclusion logically follows from your reasoning.
   ```

## Platform-Specific Issues

### GitHub Copilot

| Issue | Solution |
|-------|----------|
| Suggestions don't match project style | Add a comment with style guidance above your cursor |
| Wrong language/framework | Specify in comment: `// Using TypeScript with React` |
| Incomplete functions | Write signature and docstring first, let Copilot fill in |

### ChatGPT/Claude

| Issue | Solution |
|-------|----------|
| Forgets earlier context | Summarize key points when conversation gets long |
| Personality bleed-through | Use system prompt to reset persona |
| Token limit reached | Break large tasks into smaller chunks |

### M365 Copilot

| Issue | Solution |
|-------|----------|
| Can't find relevant documents | Reference files by exact name |
| Wrong data source | Specify which file or email to use |
| Generic business advice | Add company-specific context |

---

## Quick Reference

```text
┌─────────────────────────────────────────────────────────────┐
│                    TROUBLESHOOTING FLOWCHART                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Output not right? ─────────────────────────────────────►   │
│       │                                                     │
│       ├── Too long? ──► Add length constraints             │
│       │                                                     │
│       ├── Too short? ──► Request elaboration               │
│       │                                                     │
│       ├── Wrong format? ──► Add explicit format specs      │
│       │                                                     │
│       ├── Off-topic? ──► Add context + constraints         │
│       │                                                     │
│       ├── Inconsistent? ──► Add few-shot examples          │
│       │                                                     │
│       └── Incorrect info? ──► Request verification         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```text
---

## Next Steps

- [Model-Specific Troubleshooting](/troubleshooting/model-specific) — Platform-specific guides
- [Prompt Debugging](/troubleshooting/prompt-debugging) — Systematic debugging approach
- [Best Practices](/guides/best-practices) — Prevent issues before they occur
