---
name: Lats Lite Evaluator
description: Streamlined version of LATS Self-Refine, optimized for local models. Reduces 16KB prompt to ~2KB while preserving core evaluation logic.
type: how_to
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
| ----------- | ------- | ------- |
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
| -------- | ------- |
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
| --- | --- |
| `{{PROMPT_CONTENT}}` | The prompt text to evaluate and improve. |
| `{{QUALITY_THRESHOLD}}` | Minimum weighted score required to stop iterating (default: 80). |
| `{{MAX_ITERATIONS}}` | Max improvement iterations to attempt (default: 3). |

## Example

**Input:**

```text
THRESHOLD: 80%
MAX_ITERATIONS: 3

<prompt>
Write a poem about cats.
</prompt>
```

**Output:**

```markdown
### SCORES
| Criterion | Score | Issue |
| ----------- | ------- | ------- |
| clarity | 40 | No specified style, length, or tone |
| effectiveness | 50 | Too vague to produce consistent results |
| specificity | 20 | No examples or constraints provided |
| completeness | 30 | Missing output format, edge cases |

**Weighted Score**: 35%
**Threshold Met**: NO

### TOP FIX
**Problem**: Lacks specificity on poem style, length, and desired outcome
**Fix**: Add concrete parameters for style, tone, length, and output format
**Before**: Write a poem about cats.
**After**: Write a 4-stanza poem about cats in the style of Emily Dickinson. Each stanza should have 4 lines with an ABAB rhyme scheme. Focus on themes of independence and mystery. Output only the poem, no explanations.

### DECISION
{"score": 35, "threshold_met": false, "continue": true}
```

## Size Comparison

| Version | Size | Tokens | Local Model? |
| --------- | ------ | -------- | -------------- |
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
