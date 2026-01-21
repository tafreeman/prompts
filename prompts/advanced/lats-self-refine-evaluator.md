---
name: Lats Self Refine Evaluator
description: # LATS Self-Refine: Iterative Multi-Branch Prompt Evaluator
type: how_to
---

# LATS Self-Refine: Iterative Multi-Branch Prompt Evaluator

## Description

This prompt implements a hybrid pattern combining:

- **LATS** (Language Agent Tree Search) - Tree exploration with backtracking
- **Self-Refine** - Iterative improvement loop until threshold met
- **ToT** (Tree-of-Thoughts) - Parallel branch exploration
- **ReAct** - Thought → Action → Observe cycles
- **CoVe** (Chain-of-Verification) - Verify claims against research

The evaluator runs three parallel branches per iteration:

1. **Branch A: Criteria Validation** - Verifies grading rubric against research
2. **Branch B: Scoring & Feedback** - Scores the prompt and generates improvements
3. **Branch C: Implementation** - Applies changes based on feedback

The outer loop continues until the score exceeds the threshold or max iterations reached.

## Research Foundation

| Pattern | Paper | Key Contribution |
| --------- | ------- | ------------------ |
| **LATS** | Zhou et al., 2023 | Tree search + iteration + backtracking for agents |
| **Self-Refine** | Madaan et al., 2023 | Generate → Feedback → Refine loop until termination |
| **ToT** | Yao et al., 2023 | Multi-branch deliberate problem solving |
| **ReAct** | Yao et al., 2022 | Thought-Action-Observation reasoning traces |
| **CoVe** | Dhuliawala et al., 2023 | Verify claims independently to reduce hallucination |
| **Reflexion** | Shinn et al., 2023 | Verbal self-reflection for agent learning |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│              LATS OUTER LOOP (iterate until threshold)              │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  ITERATION N                                                   │  │
│  │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐  │  │
│  │  │ Branch A: CoVe  │ │ Branch B: Score │ │ Branch C: ReAct │  │  │
│  │  │ Criteria Valid. │ │ G-Eval Scoring  │ │ Implement Fixes │  │  │
│  │  │                 │ │                 │ │                 │  │  │
│  │  │ • Verify rubric │ │ • Score prompt  │ │ • Apply changes │  │  │
│  │  │ • Check research│ │ • Gen feedback  │ │ • Validate edit │  │  │
│  │  │ • Adjust if bad │ │ • Prioritize    │ │ • Test result   │  │  │
│  │  └────────┬────────┘ └────────┬────────┘ └────────┬────────┘  │  │
│  │           │                   │                   │           │  │
│  │           └───────────────────┼───────────────────┘           │  │
│  │                               ▼                               │  │
│  │                    ┌─────────────────────┐                    │  │
│  │                    │ SYNTHESIS & CHECK   │                    │  │
│  │                    │ Score >= Threshold? │                    │  │
│  │                    └──────────┬──────────┘                    │  │
│  └───────────────────────────────┼───────────────────────────────┘  │
│                                  │                                  │
│              ┌───────────────────┴───────────────────┐              │
│              │                                       │              │
│              ▼ NO                                YES ▼              │
│     ┌────────────────┐                    ┌────────────────┐        │
│     │ REFLEXION      │                    │ RETURN RESULT  │        │
│     │ Learn from     │                    │ Score, Prompt, │        │
│     │ iteration,     │                    │ Criteria Used  │        │
│     │ loop back      │                    └────────────────┘        │
│     └────────────────┘                                              │
└─────────────────────────────────────────────────────────────────────┘
```

## Variables

| Variable | Required | Default | Description |
| ---------- | ---------- | --------- | ------------- |
| `PROMPT_CONTENT` | Yes | - | The full prompt text to evaluate |
| `QUALITY_THRESHOLD` | No | 80 | Minimum score (0-100) to terminate |
| `MAX_ITERATIONS` | No | 5 | Maximum refinement loops |
| `GRADING_CRITERIA` | No | See default | JSON with criteria and weights |

## Prompt

```text
You are an expert Prompt Quality Engineer using a hybrid LATS + Self-Refine + ToT + ReAct + CoVe evaluation system.

## Configuration

- **Quality Threshold**: {{QUALITY_THRESHOLD}}%
- **Max Iterations**: {{MAX_ITERATIONS}}
- **Grading Criteria**: {{GRADING_CRITERIA}}

## Prompt to Evaluate
<prompt_under_test>
{{PROMPT_CONTENT}}
</prompt_under_test>

## BRANCH A: CRITERIA VALIDATION (CoVe Pattern)

**Goal**: Verify that grading criteria are valid and research-backed.

### A1. Draft Assessment
For each criterion in `{{GRADING_CRITERIA}}`, assess:

- Is this criterion supported by GenAI prompt engineering research (2023-2025)?
- Does the weight reflect its importance in practice?

### A2. Verification Questions
Generate one verification question per criterion:
| Criterion | Verification Question |
| ----------- | ---------------------- |
| [name] | "Is [criterion] supported by [specific research]?" |

### A3. Independent Verification
Answer EACH question independently (do not reference A1):
| Criterion | Research Support | Citation/Source |
| ----------- | ----------------- | ----------------- |
| [name] | Y/N | [e.g., "Dhuliawala et al. 2023", "DAIR.AI Guide 2024"] |

### A4. Criteria Adjustment Decision
```json

{
  "criteria_valid": true/false,
  "adjustments_needed": [
    {"criterion": "name", "action": "keep|modify|remove|add", "reason": "..."}
  ],
  "effective_criteria": { ... } // The criteria to use for this iteration
}

```

## BRANCH C: IMPLEMENTATION (ReAct Pattern)

**Goal**: Apply the top improvement and validate the change.

### C1. Select Top Fix

From Branch B's prioritized list, select the #1 action.

**Selected Action**: [description]

### C2. Thought → Action → Observe Cycle

**Thought**: What specific change will address this issue?

```

[Reasoning about how to implement the fix]

```

**Action**: Apply the change

```markdown

<!-- BEFORE -->
[Original section of prompt]

<!-- AFTER -->
[Modified section with fix applied]

```

**Observation**: Validate the change

- Does the fix address the identified issue? [Y/N]
- Does it introduce new problems? [Y/N]
- Estimated score improvement: +[X]%

### C3. Updated Prompt

<updated_prompt>
[Full prompt with the fix applied]
</updated_prompt>

## IF CONTINUING: REFLEXION (Learning from Iteration)

### What Worked

- [Effective strategy from this iteration]

### What Didn't Work

- [Ineffective approach to avoid]

### Adjusted Strategy for Next Iteration

- [New approach based on learning]

### ═══════════════════════════════════════════════════════════════

### → LOOP BACK TO ITERATION [N+1]

### ═══════════════════════════════════════════════════════════════

## References

- Zhou, S., Xu, F. F., Zhu, H., et al. (2023). "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models." arXiv:2310.04406
- Madaan, A., Tandon, N., et al. (2023). "Self-Refine: Iterative Refinement with Self-Feedback." arXiv:2303.17651
- Yao, S., Yu, D., et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." arXiv:2305.10601
- Yao, S., Zhao, J., et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." arXiv:2210.03629
- Dhuliawala, S., Komeili, M., et al. (2023). "Chain-of-Verification Reduces Hallucination in Large Language Models." arXiv:2309.11495
- Shinn, N., Cassano, F., et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." arXiv:2303.11366

## Example

**Input:**

```yaml
QUALITY_THRESHOLD: 85
MAX_ITERATIONS: 3
PROMPT_CONTENT: |
  Summarize the following text in 3 bullet points.
  [TEXT]
GRADING_CRITERIA:
  clarity: 25
  effectiveness: 30
  specificity: 20
  completeness: 25
```

**Output (Iteration 1):**

```markdown
## BRANCH A: CRITERIA VALIDATION

### A3. Independent Verification
| Criterion | Research Support | Citation/Source |
| ----------- | ----------------- | ----------------- |
| clarity | Y | Wei et al. 2022 - Clear prompts improve accuracy |
| effectiveness | Y | DAIR.AI Guide 2024 - Outcome-driven prompts |
| specificity | Y | OpenAI Best Practices 2024 |
| completeness | Y | Anthropic Prompt Engineering Guide |

### A4. Criteria Adjustment Decision
{"criteria_valid": true, "adjustments_needed": [], "effective_criteria": {...}}

## BRANCH B: SCORING (G-Eval)

| Criterion | Score | Feedback |
| ----------- | ------- | ---------- |
| clarity | 60 | Goal is clear but lacks role definition |
| effectiveness | 55 | No example output provided |
| specificity | 45 | "3 bullet points" is specific but no format shown |
| completeness | 40 | Missing: input length limits, edge cases |

**Weighted Score**: 50%
**Threshold Met**: NO

## BRANCH C: IMPLEMENTATION (ReAct)

**Thought**: The prompt needs role definition and output format example.

**Action**: Apply the change
<!-- BEFORE -->
Summarize the following text in 3 bullet points.

<!-- AFTER -->
You are a concise summarization assistant.

Summarize the following text into exactly 3 bullet points:
- Each bullet should be 10-20 words
- Focus on key facts, not opinions
- Use present tense

[TEXT]

**Observation**: Fix addresses clarity and specificity. Estimated improvement: +25%
```
