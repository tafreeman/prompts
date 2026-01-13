---
title: "LATS-Lite: Compact Prompt Evaluator"
shortTitle: LATS-Lite
intro: >
  Streamlined LATS evaluator optimized for local models. Reduces 16KB prompt to ~2KB
  while preserving core evaluation logic including scoring, threshold checks, and iteration.
description: Streamlined LATS evaluator optimized for local models (~2KB vs 16KB)
type: how_to
difficulty: intermediate
audience:
  - senior-engineer
  - solution-architect
platforms:
  - chatgpt
  - claude
  - github-copilot
topics:
  - evaluation
  - quality-assurance
category: evaluation
tags: [lats, evaluation, local-models]
version: 1.0.0
model_compatibility: [phi4, qwen2.5, deepseek, llama]
variables:
  - name: PROMPT_CONTENT
    required: true
  - name: QUALITY_THRESHOLD
    default: "80"
  - name: MAX_ITERATIONS
    default: "3"
complexity: intermediate
estimated_tokens: 500-800
date: "2026-01-12"
reviewStatus: draft
governance_tags:
  - PII-safe
dataClassification: internal
effectivenessScore: 0.0
---

# LATS-Lite: Compact Prompt Evaluator

Streamlined version of LATS Self-Refine, optimized for local models. Reduces 16KB prompt to ~2KB while preserving core evaluation logic.

## Description

Use this prompt to score and iteratively improve another prompt using a compact, structured rubric that works well with smaller local-model context windows.

## Prompt

```text
You are a Prompt Quality Evaluator. Score and improve the prompt below.

THRESHOLD: {{QUALITY_THRESHOLD}}%
MAX_ITERATIONS: {{MAX_ITERATIONS}}

<prompt>
{{PROMPT_CONTENT}}
</prompt>

## Evaluate using these criteria (weights in parentheses):
- Clarity (25%): Is the goal and role clear?
- Effectiveness (30%): Does it produce good results?
- Specificity (20%): Are instructions precise with examples?
- Completeness (25%): Are edge cases and output format covered?

## For each iteration, output EXACTLY this format:

### SCORES
| Criterion | Score | Issue |
|-----------|-------|-------|
| clarity | [0-100] | [problem if <80] |
| effectiveness | [0-100] | [problem if <80] |
| specificity | [0-100] | [problem if <80] |
| completeness | [0-100] | [problem if <80] |

**Weighted Score**: [calculated]%
**Threshold Met**: [YES/NO]

### TOP FIX (if score < threshold)
**Problem**: [biggest issue]
**Fix**: [specific change]
**Before**: [original text]
**After**: [improved text]

### DECISION
```json
{"score": [X], "threshold_met": [true/false], "continue": [true/false]}
```

If threshold met or max iterations reached, output final improved prompt:

### FINAL PROMPT
<final>
[improved prompt text]
</final>

### SUMMARY
| Metric | Value |
|--------|-------|
| Initial Score | [X]% |
| Final Score | [Y]% |
| Improvement | +[Z]% |
| Iterations | [N] |
```

## Usage

```python
from tools.llm_client import LLMClient

prompt = open("my-prompt.md").read()
evaluator = open("prompts/advanced/lats-lite-evaluator.md").read()

# Extract just the prompt section (skip frontmatter/docs)
import re
match = re.search(r'```text\n(.*?)\n```', evaluator, re.DOTALL)
template = match.group(1) if match else evaluator

filled = template.replace("{{PROMPT_CONTENT}}", prompt[:3000])
filled = filled.replace("{{QUALITY_THRESHOLD}}", "80")
filled = filled.replace("{{MAX_ITERATIONS}}", "3")

result = LLMClient.generate_text("ollama:qwen2.5-coder:14b", filled)
print(result)
```

## Variables

| Variable | Description |
|---|---|
| `{{PROMPT_CONTENT}}` | The prompt text to evaluate and improve. |
| `{{QUALITY_THRESHOLD}}` | Minimum weighted score required to stop iterating (default: 80). |
| `{{MAX_ITERATIONS}}` | Max improvement iterations to attempt (default: 3). |

## Size Comparison

| Version | Size | Tokens | Local Model? |
|---------|------|--------|--------------|
| LATS Full | 16KB | ~4000 | ❌ Timeouts |
| **LATS-Lite** | **2KB** | **~500** | ✅ Fast |

## What Was Removed

- Documentation sections (humans only)
- ASCII architecture diagram
- Research citations table
- Detailed sub-steps (A1-A4, B1-B4, C1-C3)
- 2KB example (reduced to format spec)
- Comparison tables
- Design rationale

## What Was Preserved

✅ 4 scoring criteria with weights  
✅ Weighted score calculation  
✅ Threshold-based termination  
✅ Iteration loop logic  
✅ Before/After fix format  
✅ JSON decision output  
✅ Final prompt output  
