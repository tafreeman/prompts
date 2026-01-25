---
name: Chain Of Thought Detailed
description: # Chain-of-Thought: Detailed Mode
type: how_to
---
## Description

## Prompt

```text
You are an expert problem solver using detailed chain-of-thought reasoning.

**Task**: [DESCRIBE_YOUR_TASK]

**Context**: [PROVIDE_COMPREHENSIVE_CONTEXT]

**Success Criteria**: [DEFINE_WHAT_SUCCESS_LOOKS_LIKE]

**Constraints**: [LIST_CONSTRAINTS_AND_REQUIREMENTS]

**Instructions**:
Think through this problem systematically and thoroughly. For each step:

1. Explain your reasoning in detail
2. Consider alternatives and explain why you chose this approach
3. Acknowledge assumptions explicitly
4. Note any uncertainties or risks

Format your response as:

**Understanding the Problem**

- Restate the problem in your own words
- Identify key challenges and unknowns
- List critical assumptions

**Step 1: [Title of Step]**

- **What**: [What you're doing in this step]
- **Why**: [Reasoning and justification]
- **Alternatives Considered**: [What else you thought about]
- **Risks/Assumptions**: [What could go wrong or what you're assuming]
- **Outcome**: [Result of this step]

**Step 2: [Title of Step]**
[Continue the same detailed format]

...

**Synthesis and Validation**

- How the steps fit together
- Validation that this addresses the original problem
- Edge cases or scenarios not fully addressed

**Final Answer**

- Clear, actionable conclusion
- Confidence level (High/Medium/Low) with justification
- Recommended next steps
- Potential refinements or follow-up questions

```

# Chain-of-Thought: Detailed Mode

## Description

## Prompt

```text
You are an expert problem solver using detailed chain-of-thought reasoning.

**Task**: [DESCRIBE_YOUR_TASK]

**Context**: [PROVIDE_COMPREHENSIVE_CONTEXT]

**Success Criteria**: [DEFINE_WHAT_SUCCESS_LOOKS_LIKE]

**Constraints**: [LIST_CONSTRAINTS_AND_REQUIREMENTS]

**Instructions**:
Think through this problem systematically and thoroughly. For each step:

1. Explain your reasoning in detail
2. Consider alternatives and explain why you chose this approach
3. Acknowledge assumptions explicitly
4. Note any uncertainties or risks

Format your response as:

**Understanding the Problem**

- Restate the problem in your own words
- Identify key challenges and unknowns
- List critical assumptions

**Step 1: [Title of Step]**

- **What**: [What you're doing in this step]
- **Why**: [Reasoning and justification]
- **Alternatives Considered**: [What else you thought about]
- **Risks/Assumptions**: [What could go wrong or what you're assuming]
- **Outcome**: [Result of this step]

**Step 2: [Title of Step]**
[Continue the same detailed format]

...

**Synthesis and Validation**

- How the steps fit together
- Validation that this addresses the original problem
- Edge cases or scenarios not fully addressed

**Final Answer**

- Clear, actionable conclusion
- Confidence level (High/Medium/Low) with justification
- Recommended next steps
- Potential refinements or follow-up questions

```

# Chain-of-Thought: Detailed Mode


# Chain-of-Thought: Detailed Mode

## Research Foundation

This technique is based on the foundational paper:
**Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D. (2022).** "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *Advances in Neural Information Processing Systems (NeurIPS) 35*. [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)

Wei et al. demonstrated that generating a chain of thought—a series of intermediate reasoning steps—significantly improves the ability of large language models to perform complex reasoning. With just eight chain-of-thought exemplars, a 540B-parameter model achieved state-of-the-art accuracy on the GSM8K math benchmark, surpassing even finetuned GPT-3 with a verifier.

## Prompt

```text
You are an expert problem solver using detailed chain-of-thought reasoning.

**Task**: [DESCRIBE_YOUR_TASK]

**Context**: [PROVIDE_COMPREHENSIVE_CONTEXT]

**Success Criteria**: [DEFINE_WHAT_SUCCESS_LOOKS_LIKE]

**Constraints**: [LIST_CONSTRAINTS_AND_REQUIREMENTS]

**Instructions**:
Think through this problem systematically and thoroughly. For each step:

1. Explain your reasoning in detail
2. Consider alternatives and explain why you chose this approach
3. Acknowledge assumptions explicitly
4. Note any uncertainties or risks

Format your response as:

**Understanding the Problem**

- Restate the problem in your own words
- Identify key challenges and unknowns
- List critical assumptions

**Step 1: [Title of Step]**

- **What**: [What you're doing in this step]
- **Why**: [Reasoning and justification]
- **Alternatives Considered**: [What else you thought about]
- **Risks/Assumptions**: [What could go wrong or what you're assuming]
- **Outcome**: [Result of this step]

**Step 2: [Title of Step]**
[Continue the same detailed format]

...

**Synthesis and Validation**

- How the steps fit together
- Validation that this addresses the original problem
- Edge cases or scenarios not fully addressed

**Final Answer**

- Clear, actionable conclusion
- Confidence level (High/Medium/Low) with justification
- Recommended next steps
- Potential refinements or follow-up questions

```

## Usage

To use this prompt:

1. Copy the prompt template from the "## Prompt" section above
2. Replace all bracketed placeholders with your comprehensive information
3. Submit to your preferred AI platform (Claude, ChatGPT, or GitHub Copilot)
4. Allow adequate time for the detailed analysis
5. Review each step carefully, including alternatives considered and assumptions made

## Related Prompts

- [Chain-of-Thought: Concise Mode](chain-of-thought-concise.md) - For quicker reasoning
- [Chain-of-Thought Guide](chain-of-thought-guide.md) - Decision framework for choosing CoT modes
- [Tree-of-Thoughts Template](tree-of-thoughts-template.md) - When you need to explore multiple solution paths

## Governance Notes

- **PII Safety**: This template doesn't inherently process PII. Ensure your task description and context don't include sensitive data.
- **Human Review Required For**:
  - Decisions with >$100K impact
  - Architecture decisions affecting >10 engineers
  - Security or compliance-critical choices
  - Novel problem domains without precedent
- **Audit Trail**: The detailed format provides comprehensive audit trail. Archive reasoning for critical decisions (minimum 7 years for compliance).
- **Quality Assurance**: Consider having 2-3 experts review detailed CoT for critical decisions (similar to code review).

## Platform Adaptations

### GitHub Copilot Chat

```text
@workspace /explain [complex-issue] using detailed chain-of-thought reasoning. Include alternatives considered and risks for each step.
```

### API Integration

```python
response = client.chat.completions.create(
    model="gpt-5.1",
    messages=[
        {"role": "system", "content": "You use detailed chain-of-thought reasoning with alternatives and justifications."},
        {"role": "user", "content": detailed_cot_prompt}
    ],
    temperature=0.7,  # Slightly higher for exploration
    max_tokens=4000   # Detailed mode needs more tokens
)
```## Variables

| Variable | Description |
|---|---|
| `[DEFINE_WHAT_SUCCESS_LOOKS_LIKE]` | AUTO-GENERATED: describe `DEFINE_WHAT_SUCCESS_LOOKS_LIKE` |
| `[DESCRIBE_YOUR_TASK]` | AUTO-GENERATED: describe `DESCRIBE_YOUR_TASK` |
| `[LIST_CONSTRAINTS_AND_REQUIREMENTS]` | AUTO-GENERATED: describe `LIST_CONSTRAINTS_AND_REQUIREMENTS` |
| `[PROVIDE_COMPREHENSIVE_CONTEXT]` | AUTO-GENERATED: describe `PROVIDE_COMPREHENSIVE_CONTEXT` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[Chain-of-Thought Guide]` | AUTO-GENERATED: describe `Chain-of-Thought Guide` |
| `[Chain-of-Thought: Concise Mode]` | AUTO-GENERATED: describe `Chain-of-Thought: Concise Mode` |
| `[Continue the same detailed format]` | AUTO-GENERATED: describe `Continue the same detailed format` |
| `[DEFINE_WHAT_SUCCESS_LOOKS_LIKE]` | AUTO-GENERATED: describe `DEFINE_WHAT_SUCCESS_LOOKS_LIKE` |
| `[DESCRIBE_YOUR_TASK]` | AUTO-GENERATED: describe `DESCRIBE_YOUR_TASK` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[LIST_CONSTRAINTS_AND_REQUIREMENTS]` | AUTO-GENERATED: describe `LIST_CONSTRAINTS_AND_REQUIREMENTS` |
| `[PROVIDE_COMPREHENSIVE_CONTEXT]` | AUTO-GENERATED: describe `PROVIDE_COMPREHENSIVE_CONTEXT` |
| `[Reasoning and justification]` | AUTO-GENERATED: describe `Reasoning and justification` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[Result of this step]` | AUTO-GENERATED: describe `Result of this step` |
| `[Title of Step]` | AUTO-GENERATED: describe `Title of Step` |
| `[Tree-of-Thoughts Template]` | AUTO-GENERATED: describe `Tree-of-Thoughts Template` |
| `[What could go wrong or what you're assuming]` | AUTO-GENERATED: describe `What could go wrong or what you're assuming` |
| `[What else you thought about]` | AUTO-GENERATED: describe `What else you thought about` |
| `[What you're doing in this step]` | AUTO-GENERATED: describe `What you're doing in this step` |
| `[arXiv:2201.11903]` | AUTO-GENERATED: describe `arXiv:2201.11903` |
| `[complex-issue]` | AUTO-GENERATED: describe `complex-issue` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

