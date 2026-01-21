---
name: Chain Of Thought Concise
description: # Chain-of-Thought: Concise Mode
type: how_to
---

# Chain-of-Thought: Concise Mode

## Research Foundation

Based on Chain-of-Thought prompting (Wei et al., NeurIPS 2022). [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)

This concise variant maintains the core reasoning benefits while optimizing for token efficiency and speed.

## Prompt

```text
You are an expert problem solver using concise chain-of-thought reasoning.

**Task**: [DESCRIBE_YOUR_TASK]

**Context**: [PROVIDE_RELEVANT_CONTEXT]

**Constraints**: [LIST_ANY_CONSTRAINTS]

**Instructions**:
Think through this step-by-step, but keep each step brief (1-2 sentences max).

Format your response as:

**Step 1**: [First logical step - what needs to be understood or done first]
**Step 2**: [Second logical step - what follows from step 1]
**Step 3**: [Continue as needed]
...
**Final Answer**: [Concise conclusion based on the steps above]

Keep reasoning tight and focused. Skip obvious steps. Focus on key insights that drive the solution.
```

## Usage

To use this prompt:

1. Copy the prompt template from the "## Prompt" section above
2. Replace the bracketed placeholders with your specific information
3. Submit to your preferred AI platform (Claude, ChatGPT, or GitHub Copilot)
4. Review the step-by-step reasoning and final answer

## Tips

- **When to use Concise CoT**: Use when you need reasoning transparency but not extensive justification. Ideal for experienced audiences who can fill in obvious steps.
- **Step granularity**: Each step should represent a meaningful logical leap. Skip trivial steps like "read the problem" or "understand the context".
- **Balance**: Aim for 3-6 steps for most problems. More than 8 suggests you might need detailed mode instead.
- **Combine with tools**: Concise CoT works well with code execution, API calls, or database queries as validation steps.
- **Token efficiency**: This mode can reduce token usage by 40-60% compared to detailed CoT while maintaining reasoning quality.
- **Switch when needed**: If a step reveals unexpected complexity, acknowledge it and switch to detailed mode for that sub-problem.

## When NOT to Use

- High-stakes decisions requiring full justification
- Teaching contexts where elaboration aids learning
- Novel or unfamiliar problems where more exploration is needed
- Compliance situations requiring extensive documentation

## Variations

### Ultra-Concise (Bullet Mode)

```text
Think through this in bullet steps:
• [Key insight 1]
• [Key insight 2]
• [Key insight 3]
→ Conclusion: [Final answer]
```

### Numbered Steps with Confidence

```text

1. [Step] (Confidence: High/Medium/Low)
2. [Step] (Confidence: High/Medium/Low)

Final Answer: [Conclusion] (Overall Confidence: X%)
```

## Output Schema (JSON)

For automation pipelines, request output in this format:

```json
{
  "reasoning_steps": [
    {"step": 1, "description": "...", "confidence": "high|medium|low"},
    {"step": 2, "description": "...", "confidence": "high|medium|low"}
  ],
  "final_answer": "...",
  "overall_confidence": 0.85,
  "assumptions": ["...", "..."],
  "next_steps": ["...", "..."]
}
```

## Governance Notes

- **PII Safety**: This template doesn't inherently process PII. Ensure your task description and context don't include sensitive data.
- **Human Review**: Not required for general use, but recommended for:
  - Decisions with >$10K impact
  - Security-related conclusions
  - Compliance-affecting choices
- **Audit Trail**: The step-by-step format provides natural audit trail. Consider logging reasoning for critical decisions.

## Platform Adaptations

### GitHub Copilot Chat

```text
@workspace /explain [your-code-or-issue] using concise chain-of-thought reasoning
```

### API Integration

```python
response = client.chat.completions.create(
    model="gpt-5.1",
    messages=[
        {"role": "system", "content": "You use concise chain-of-thought reasoning."},
        {"role": "user", "content": f"Task: {task}\nThink step-by-step (concise mode)"}
    ]
)
```
