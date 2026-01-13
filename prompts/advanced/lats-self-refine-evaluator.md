---
title: "LATS Self-Refine: Iterative Multi-Branch Prompt Evaluator"
shortTitle: LATS Self-Refine Evaluator
intro: >
  Combines LATS (Language Agent Tree Search), Self-Refine, ToT, ReAct, and CoVe patterns
  for iterative prompt evaluation with parallel branches that loop until quality threshold.
description: >
  Combines LATS (Language Agent Tree Search), Self-Refine, ToT, ReAct, and CoVe patterns 
  for iterative prompt evaluation with parallel branches that loop until quality threshold.
category: evaluation
tags:
  - lats
  - self-refine
  - tree-of-thoughts
  - react
  - cove
  - iterative-refinement
  - prompt-evaluation
author: Prompts Library Team
version: 1.0.0
model_compatibility:
  - gpt-4
  - gpt-4o
  - claude-3
  - o1
  - deepseek-r1
variables:
  - name: PROMPT_CONTENT
    description: The full text of the prompt to evaluate
    required: true
  - name: QUALITY_THRESHOLD
    description: Minimum acceptable score (0-100) to stop iteration
    required: false
    default: "80"
  - name: MAX_ITERATIONS
    description: Maximum refinement loops before stopping
    required: false
    default: "5"
  - name: GRADING_CRITERIA
    description: JSON object with criteria names and weights
    required: false
    default: '{"clarity": 25, "effectiveness": 30, "specificity": 20, "completeness": 25}'
use_cases:
  - Automated prompt quality improvement
  - Rubric validation against research
  - Self-improving prompt libraries
  - CI/CD quality gates for prompts
complexity: expert
estimated_tokens: 2000-4000
type: how_to
difficulty: advanced
audience:
  - senior-engineer
  - solution-architect
platforms:
  - github-copilot
  - claude
  - chatgpt
topics:
  - evaluation
  - quality-assurance
  - automation
date: "2026-01-05"
reviewStatus: draft
governance_tags:
  - PII-safe
dataClassification: internal
effectivenessScore: 0.0
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
|---------|-------|------------------|
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
|----------|----------|---------|-------------|
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

---

## EXECUTION PROTOCOL

For each iteration, execute THREE PARALLEL BRANCHES, then synthesize and decide whether to loop.

### ═══════════════════════════════════════════════════════════════
### ITERATION [N]
### ═══════════════════════════════════════════════════════════════

---

## BRANCH A: CRITERIA VALIDATION (CoVe Pattern)

**Goal**: Verify that grading criteria are valid and research-backed.

### A1. Draft Assessment
For each criterion in `{{GRADING_CRITERIA}}`, assess:
- Is this criterion supported by GenAI prompt engineering research (2023-2025)?
- Does the weight reflect its importance in practice?

### A2. Verification Questions
Generate one verification question per criterion:
| Criterion | Verification Question |
|-----------|----------------------|
| [name] | "Is [criterion] supported by [specific research]?" |

### A3. Independent Verification
Answer EACH question independently (do not reference A1):
| Criterion | Research Support | Citation/Source |
|-----------|-----------------|-----------------|
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

---

## BRANCH B: SCORING & FEEDBACK (G-Eval + Self-Refine Pattern)

**Goal**: Score the prompt and generate actionable improvement feedback.

### B1. Score Each Criterion
Using the **effective_criteria** from Branch A, score the prompt:

| Criterion | Score (0-100) | Weight | Evidence | Issue (if <80) |
|-----------|---------------|--------|----------|----------------|
| [name] | [score] | [weight]% | "[quote from prompt]" | "[specific problem]" |

### B2. Calculate Weighted Score
```
Total Score = Σ(criterion_score × weight) / Σ(weights)
```

**Current Score**: [X]%
**Threshold**: {{QUALITY_THRESHOLD}}%
**Status**: PASS/FAIL

### B3. Generate Improvement Suggestions
For each criterion scoring below 80%:
```json
{
  "criterion": "[name]",
  "current_score": [X],
  "target_score": 85,
  "suggestion": "[Specific, actionable improvement]",
  "example_fix": "[Show exactly what to add/change]",
  "priority": [1-5]
}
```

### B4. Prioritized Action List
Rank by: (100 - score) × weight × priority
1. [Highest impact fix]
2. [Second highest]
3. [Third highest]

---

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

---

## SYNTHESIS & TERMINATION CHECK

### Current State
| Metric | Value |
|--------|-------|
| Iteration | [N] |
| Previous Score | [X]% |
| Current Score | [Y]% |
| Improvement | +[Z]% |
| Threshold | {{QUALITY_THRESHOLD}}% |

### Termination Decision
```json
{
  "score_meets_threshold": true/false,
  "max_iterations_reached": true/false,
  "continue_iteration": true/false,
  "reason": "[Why continuing or stopping]"
}
```

---

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

---

## FINAL OUTPUT (When Terminated)

### Summary
| Metric | Value |
|--------|-------|
| Starting Score | [X]% |
| Final Score | [Y]% |
| Total Improvement | +[Z]% |
| Iterations Used | [N] |
| Criteria Adjustments Made | [count] |

### Final Grading Criteria (Validated)
```json
{
  "criteria": { ... },
  "research_validation": { ... }
}
```

### Final Prompt
<final_prompt>
[The improved prompt]
</final_prompt>

### Improvement History
| Iteration | Score | Change Made | Impact |
|-----------|-------|-------------|--------|
| 0 | [X]% | (baseline) | - |
| 1 | [Y]% | [fix] | +[Z]% |
| ... | ... | ... | ... |

### Confidence Assessment
- **Score Confidence**: High/Medium/Low
- **Criteria Validity**: High/Medium/Low  
- **Remaining Risks**: [Any issues not addressed]
```

## Example

### Input
```
PROMPT_CONTENT: "You are a helpful assistant. Answer questions."
QUALITY_THRESHOLD: 80
MAX_ITERATIONS: 3
GRADING_CRITERIA: {"clarity": 25, "effectiveness": 30, "specificity": 20, "completeness": 25}
```

### Expected Output (Iteration 1)
```
═══════════════════════════════════════════════════════════════
ITERATION 1
═══════════════════════════════════════════════════════════════

BRANCH A: CRITERIA VALIDATION
✓ All criteria validated against DAIR.AI 2024, Madaan et al. 2023
No adjustments needed.

BRANCH B: SCORING & FEEDBACK
| Criterion | Score | Evidence |
|-----------|-------|----------|
| clarity | 70% | "Generic role, no specifics" |
| effectiveness | 45% | "No goal, constraints, or process" |
| specificity | 30% | "No variables, examples, or structure" |
| completeness | 40% | "Missing output format, edge cases" |

**Current Score**: 46.25%
**Status**: FAIL (below 80% threshold)

Top Fix: Add explicit goal, constraints, and output format (effectiveness +25%)

BRANCH C: IMPLEMENTATION
**Action**: Add structured sections

<!-- AFTER -->
You are a [ROLE] assistant specializing in [DOMAIN].

## Goal
[SPECIFIC_OBJECTIVE]

## Constraints
- [CONSTRAINT_1]
- [CONSTRAINT_2]

## Output Format
[EXPECTED_FORMAT]

**Observation**: Fix addresses effectiveness gap. Score estimate: ~65%

SYNTHESIS: Score 46% < 80% threshold → CONTINUE

REFLEXION: Prioritize specificity next (largest remaining gap)

→ LOOP TO ITERATION 2
```

## Comparison: This Design vs. Existing Implementations

| Aspect | Self-Refine (Madaan) | Reflexion (Shinn) | LATS (Zhou) | **This Prompt** |
|--------|---------------------|-------------------|-------------|-----------------|
| **Parallel Branches** | No (sequential) | No | Yes (tree search) | **Yes (3 branches)** |
| **Criteria Validation** | No | No | No | **Yes (CoVe in Branch A)** |
| **Research Grounding** | No | No | No | **Yes (verifies against papers)** |
| **Backtracking** | No | No | Yes | **Yes (via Reflexion)** |
| **Termination** | max_attempts or "none" feedback | max_trials or correct | goal reached | **Score threshold** |
| **Learning Across Iterations** | History appended | Reflections stored | State tracking | **Explicit Reflexion phase** |
| **Domain** | General text tasks | QA/Code | General reasoning | **Prompt evaluation** |

### Why These Design Choices

1. **Three Parallel Branches** (vs. Self-Refine's single feedback loop)
   - Self-Refine: `Generate → Feedback → Refine` (linear)
   - **This prompt**: `Validate Criteria ‖ Score ‖ Implement` (parallel)
   - **Rationale**: Criteria validation and scoring are independent operations that can inform each other; parallelism catches criteria drift before it affects scoring.

2. **CoVe for Criteria Validation** (vs. fixed rubrics)
   - Most evaluators use static rubrics that may be outdated
   - **This prompt**: Verifies each criterion against research before scoring
   - **Rationale**: Prevents "evaluating with invalid metrics" - a meta-error that wastes iterations.

3. **ReAct for Implementation** (vs. batch replacement)
   - Self-Refine: Model generates entire refined output
   - **This prompt**: Explicit Thought → Action → Observe with targeted edits
   - **Rationale**: Controlled changes prevent regression; observation validates before committing.

4. **Score Threshold Termination** (vs. heuristic stopping)
   - Self-Refine: Stops when feedback says "none" or "it is correct"
   - **This prompt**: Stops when weighted score ≥ threshold
   - **Rationale**: Quantitative threshold is reproducible and configurable per use case.

5. **Reflexion Phase Between Iterations** (from Shinn et al.)
   - Captures "what worked, what didn't" explicitly
   - **Rationale**: Prevents repeating ineffective strategies; accelerates convergence.

---

## References

- Zhou, S., Xu, F. F., Zhu, H., et al. (2023). "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models." arXiv:2310.04406
- Madaan, A., Tandon, N., et al. (2023). "Self-Refine: Iterative Refinement with Self-Feedback." arXiv:2303.17651
- Yao, S., Yu, D., et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." arXiv:2305.10601
- Yao, S., Zhao, J., et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." arXiv:2210.03629
- Dhuliawala, S., Komeili, M., et al. (2023). "Chain-of-Verification Reduces Hallucination in Large Language Models." arXiv:2309.11495
- Shinn, N., Cassano, F., et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." arXiv:2303.11366
