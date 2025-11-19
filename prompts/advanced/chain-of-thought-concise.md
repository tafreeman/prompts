---
title: "Chain-of-Thought: Concise Mode"
category: "advanced-techniques"
tags: ["chain-of-thought", "cot", "reasoning", "concise", "step-by-step", "problem-solving"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-17"
difficulty: "intermediate"
governance_tags: ["PII-safe", "general-use"]
platform: "Claude Sonnet 4.5, GPT-5.1, Code 5"
---

# Chain-of-Thought: Concise Mode

## Description
A streamlined Chain-of-Thought prompt template that encourages step-by-step reasoning while maintaining brevity. This mode is ideal for situations where you need logical progression without extensive elaboration. Perfect for time-sensitive decisions, quick problem-solving, or when working with token constraints.

## Use Cases
- Quick debugging sessions where you need logical steps but not extensive explanation
- Real-time code review with step-by-step analysis
- Rapid technical decision-making with clear reasoning trail
- Problem-solving in resource-constrained environments
- Situations requiring audit trail but not detailed justification

## Prompt

```
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

## Variables
- `[DESCRIBE_YOUR_TASK]`: The specific problem, question, or task you need to solve
- `[PROVIDE_RELEVANT_CONTEXT]`: Essential background information, constraints, or data
- `[LIST_ANY_CONSTRAINTS]`: Time limits, resource limits, requirements, or boundaries

## Example Usage

**Input:**
```
You are an expert problem solver using concise chain-of-thought reasoning.

**Task**: Debug why our API is returning 500 errors intermittently

**Context**: Users report errors during peak hours (9-11 AM). Error logs show "Database connection timeout". We're using PostgreSQL with connection pooling (max 20 connections). API receives ~50 requests/minute during peak.

**Constraints**: Need quick diagnosis - team is waiting for fix decision

**Instructions**:
Think through this step-by-step, but keep each step brief (1-2 sentences max).

Format your response as:

**Step 1**: [First logical step]
**Step 2**: [Second logical step]
**Step 3**: [Continue as needed]
...
**Final Answer**: [Concise conclusion]

Keep reasoning tight and focused. Skip obvious steps. Focus on key insights that drive the solution.
```

**Output:**
```
**Step 1**: Calculate peak load: 50 req/min = 0.83 req/sec. If each request holds connection for 2-3 sec, we need 2-3 simultaneous connections typically.

**Step 2**: Connection pool of 20 should handle this easily. Timeouts suggest connections aren't being released or pool is exhausted by long-running queries.

**Step 3**: Intermittent nature + peak hour timing indicates cumulative connection leak or slow query accumulation during high-load periods.

**Step 4**: Check for missing connection.close() in error handlers or transactions left open. Also profile queries running during 9-11 AM for slow performers.

**Final Answer**: Root cause is likely connection leak (unreleased connections in error paths) or slow queries accumulating during peak. Immediate actions: (1) audit connection handling in all error paths, (2) add connection timeout monitoring, (3) profile queries during peak hours. Quick win: reduce connection timeout from default to 5 seconds.
```

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
```
Think through this in bullet steps:
• [Key insight 1]
• [Key insight 2]
• [Key insight 3]
→ Conclusion: [Final answer]
```

### Numbered Steps with Confidence
```
1. [Step] (Confidence: High/Medium/Low)
2. [Step] (Confidence: High/Medium/Low)
Final Answer: [Conclusion] (Overall Confidence: X%)
```

## Related Prompts
- [Chain-of-Thought: Detailed Mode](chain-of-thought-detailed.md) - For complex problems requiring elaboration
- [Chain-of-Thought Guide](chain-of-thought-guide.md) - Decision framework for choosing CoT modes
- [ReAct Tool-Augmented](react-tool-augmented.md) - For tasks requiring external tool interaction
- [Tree-of-Thoughts Template](tree-of-thoughts-template.md) - When you need to explore multiple solution paths

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
```
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

## Changelog

### Version 1.0 (2025-11-17)
- Initial release
- Concise CoT template with 3-6 step guidance
- JSON schema for automation
- Platform adaptation examples
- Governance metadata included
