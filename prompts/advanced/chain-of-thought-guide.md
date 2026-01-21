---
name: Chain Of Thought Guide
description: # Chain-of-Thought: Decision Guide
type: reference
---

# Chain-of-Thought: Decision Guide

## Research Foundation

This technique is based on the paper:
**Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D. (2022).** "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *Advances in Neural Information Processing Systems (NeurIPS) 35*. [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)

Wei et al. demonstrated that prompting large language models to generate intermediate reasoning steps (a "chain of thought") significantly improves performance on complex reasoning tasks including arithmetic, commonsense, and symbolic reasoning. The paper showed accuracy improvements from 17.7% to 58.1% on GSM8K math problems when using Chain-of-Thought prompting.

## Text-Based Decision Tree

For reference, here's the same logic in text format:

```text
START: Do you have a task that needs AI reasoning?
│
├─→ Is it a simple lookup or straightforward task?
│   (e.g., "What's the capital of France?", "Format this JSON")
│   └─→ NO COT NEEDED - Use direct prompt
│
├─→ Does it require logical steps or problem-solving?
│   └─→ YES
│       │
│       ├─→ Is it high-stakes or novel?
│       │   (>$10K impact, compliance, untested domain)
│       │   └─→ USE DETAILED COT
│       │
│       ├─→ Do you need transparency but not full justification?
│       │   (audit trail, debugging, team learning)
│       │   └─→ USE CONCISE COT
│       │
│       └─→ Need to explore multiple approaches?
│           └─→ USE TREE-OF-THOUGHTS (see ToT guide)
```

## Comparative Examples

### Example 1: API Error

**Problem:** "Our API returns 401 errors sporadically"

**Direct Prompt** (No CoT):

```text
Fix: Check authentication tokens are being passed correctly.
```

*Token count: ~70*
*Accuracy: Good - covers main scenarios*

**Detailed CoT:**

```text
[10+ steps analyzing authentication flow, token types, edge cases, 
alternative hypotheses, considering rate limiting, caching, etc.]
```

*Token count: ~15*
*Accuracy: Poor - no context consideration*

**Concise CoT:**

```text
Step 1: Team size? Small team (<10) → monolith easier to manage.
Step 2: Expected scale? <100K users → monolith sufficient.
Step 3: Domain complexity? Simple domain → monolith fine.
Step 4: Time to market? Monolith faster for MVP.

Recommendation: Start with modular monolith, extract services later if needed.
```

*Token count: ~500*
*Accuracy: Excellent - considers all factors*

**Best choice:** **Detailed CoT** - Architecture decisions have long-term impact (>$100K), affecting many engineers, and are hard to reverse. Investment justified.

## Best Practices

### 1. Start Simple, Escalate if Needed

```text
Try: Direct prompt
↓ (if answer insufficient)
Try: Concise CoT
↓ (if still uncertain)
Try: Detailed CoT or Tree-of-Thoughts
```

### 2. Match Mode to Stakes

- Low stakes (quick lookup): No CoT
- Medium stakes (daily decisions): Concise CoT
- High stakes (architecture, compliance): Detailed CoT

### 3. Consider Your Audience

- Experts who need quick answers: No CoT or Concise
- Learning/teaching contexts: Detailed CoT
- Audit/compliance: Detailed CoT with explicit reasoning

### 4. Optimize Token Usage

- For batch processing: Use concise CoT only for failures/edge cases
- For interactive use: Let users toggle CoT mode
- For APIs: Cache common CoT reasoning patterns

### 5. Validate CoT Effectiveness

```python
# A/B test CoT vs no CoT
results = {
    "no_cot": measure_accuracy(tasks, mode="direct"),
    "concise_cot": measure_accuracy(tasks, mode="concise"),
    "detailed_cot": measure_accuracy(tasks, mode="detailed")
}

# Choose based on accuracy vs. cost trade-off
optimal_mode = optimize(results, cost_constraint=budget)
```

## Common Anti-Patterns

### ❌ Not Using CoT for Complex Tasks

```text
Bad: "Direct prompt for system architecture decision"
Risk: Missing critical considerations, expensive mistakes
```

### ❌ Using Detailed CoT Under Time Pressure

```text
Bad: "Production is down, need detailed analysis of all possibilities"
Problem: Too slow, need concise CoT for quick fix first
```

### ❌ Overusing CoT for Simple Tasks

```text
Bad: "Use detailed CoT to translate 'hello' to Spanish"
Problem: Wasted tokens, slower response, no accuracy gain
```

## Integration Patterns

### Pattern 1: Adaptive CoT

```python
def choose_cot_mode(task):
    if task.complexity < 3:
        return "none"
    elif task.stakes > 10000 or task.is_novel:
        return "detailed"
    else:
        return "concise"
```

### Pattern 2: Human-in-the-Loop

```python
# Use CoT for reasoning
reasoning = llm.generate(prompt, mode="concise_cot")

# Present steps to human for validation
if user.approves(reasoning.steps):
    execute(reasoning.final_answer)
else:
    # Escalate to detailed or revise
    reasoning = llm.generate(prompt, mode="detailed_cot", 
                            feedback=user.feedback)
```

## Cost-Benefit Analysis

### Token Cost Estimates

| Mode | Input Overhead | Output Overhead | Total Overhead |
| ------ | --------------- | ---------------- | ---------------- |
| No CoT | 0 tokens | 0 tokens | 0 tokens |
| Concise CoT | +20-30 | +40-70 | +60-100 |
| Detailed CoT | +30-50 | +200-400 | +230-450 |

### When CoT Pays Off

**Break-even calculation:**

```text
CoT is worth it when:
(Accuracy Gain) × (Cost of Error) > (Token Cost) × (Price per Token)

Example:
Accuracy gain: +25% (0.25)
Cost of error: $1,000 (wrong decision cost)
Token cost: 100 extra tokens
Price per token: $0.00003 (GPT-4 pricing)

Value = 0.25 × $1,000 = $250
Cost = 100 × $0.00003 = $0.003

ROI = $250 / $0.003 = 83,333x ✓ Definitely worth it!
```

## Governance Notes

- **PII Safety**: No PII handling in this guide
- **Human Review**: Detailed CoT outputs for >$10K decisions should be reviewed by domain experts
- **Audit Requirements**: Save CoT reasoning for compliance-critical decisions (7-year retention recommended)
- **Cost Management**: Monitor CoT usage in production; implement automatic fallback if token budgets exceeded
