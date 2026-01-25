---
name: Reflection Self Critique
description: ## Description
type: how_to
---
## Description

## Prompt

```

## Example

**Input:**

```

## Description

## Description

## Prompt

```

## Example

**Input:**

```

## Description


## Description

The Reflection pattern involves generating an initial answer and then systematically critiquing it to identify weaknesses, gaps, or errors. This two-phase approach improves answer quality by catching mistakes, considering alternatives, and refining reasoning. Essential for high-stakes decisions, complex problems, or when accuracy is paramount.

## Use Cases

- Critical business decisions requiring validation
- Complex technical solutions needing error-checking
- High-stakes communications (executive briefings, client proposals)
- Code review and architecture decisions
- Compliance and legal document review
- Research and analysis requiring accuracy
- Teaching and explanation where correctness matters

**Phase 2: Self-Critique and Reflection**

Now, critically evaluate your initial answer using this framework:

**1. Accuracy Check**:

- Are all facts correct?
- Are there any logical errors?
- Did I make unsupported assumptions?
- Are there edge cases I missed?

**2. Completeness Check**:

- Did I fully answer the question?
- Are there important aspects I overlooked?
- Is additional context needed?
- Are there alternative perspectives to consider?

**3. Quality Check**:

- Is the answer clear and well-structured?
- Is the reasoning sound?
- Are examples appropriate?
- Is the level of detail appropriate for the audience?

**4. Bias Check**:

- Am I overly confident in any claims?
- Did I favor familiar solutions over better alternatives?
- Are there unstated assumptions affecting my answer?
- Did I consider diverse viewpoints?

**5. Risk Assessment**:

- What could go wrong if this answer is followed?
- What am I uncertain about?
- What additional validation is needed?
- What's my confidence level (High/Medium/Low)?

Based on this critique, provide:

**Critique Summary**:

- **Strengths**: What was good about the initial answer
- **Weaknesses**: What needs improvement
- **Gaps**: What's missing
- **Risks**: What could go wrong

**Revised Answer**:
[Improved answer incorporating the critique]

**Confidence Level**: High/Medium/Low
**Confidence Justification**: [Explain your confidence level]

**Recommended Next Steps**: [If applicable]
```

## Example

**Input:**

```text
You will answer a question using a two-phase reflection pattern.

**Question**: Should we migrate our monolithic application to microservices?

**Context**: 

- Current: 300K LOC Java monolith, 8 years old
- Team: 30 developers
- Users: 10M MAU
- Revenue: $50M annually
- Pain points: Slow deployment (2-week cycle), scaling issues during peak
- Budget: $2M for migration
- Timeline: Must decide and plan this quarter

**Phase 1: Initial Answer**
[Generate initial answer]

**Phase 2: Self-Critique and Reflection**
[Apply critical evaluation framework]
```

**Output:**

```text
**Phase 1: Initial Answer**

**Initial Answer**:

Yes, you should migrate to microservices. Your pain points (slow deployment, scaling issues) are classic monolith problems that microservices solve. With $2M budget and 30 developers, you have sufficient resources for a phased migration over 18-24 months.

Recommended approach:

1. Start with strangler fig pattern
2. Extract the most painful services first (likely the scaling bottlenecks)
3. Implement proper service mesh (Istio or Linkerd)
4. Migrate gradually, service by service

Expected benefits:

- Deployment frequency: From 2 weeks to multiple times per day
- Scaling: Individual service scaling instead of scaling entire monolith
- Team autonomy: Teams can work on services independently
- Technology flexibility: Can use different languages/frameworks per service

Timeline: 18-24 months for complete migration.

## Tips

- **Be harsh in critique**: The goal is to find problems, not justify the initial answer
- **Look for unstated assumptions**: What did you assume without explicitly stating?
- **Consider alternatives seriously**: Don't just list them to dismiss them
- **Quantify uncertainty**: Replace "should" with "might" where appropriate
- **Check your confidence calibration**: Are you overconfident? Under-confident?
- **Time investment**: Reflection adds 50-100% to response time; use for high-stakes questions
- **Iterate if needed**: If critique reveals major flaws, revise and critique again

## Output Schema (JSON)

```json
{
  "initial_answer": "...",
  "critique": {
    "accuracy_issues": ["...", "..."],
    "completeness_gaps": ["...", "..."],
    "quality_concerns": ["...", "..."],
    "bias_detected": ["...", "..."],
    "risks": ["...", "..."]
  },
  "critique_summary": {
    "strengths": ["...", "..."],
    "weaknesses": ["...", "..."],
    "gaps": ["...", "..."],
    "risks": ["...", "..."]
  },
  "revised_answer": "...",
  "confidence": {
    "level": "high|medium|low",
    "justification": "...",
    "remaining_uncertainties": ["...", "..."]
  },
  "next_steps": ["...", "..."]
}
```

## Governance Notes

- **PII Safety**: No inherent PII handling; ensure question/context don't contain sensitive data
- **Human Review Required**: For critiques of high-impact decisions (>$100K, legal, compliance)
- **Audit Trail**: Save both initial answer and revised answer for accountability
- **Quality Assurance**: Reflection output should be reviewed by domain expert for critical decisions

## Platform Adaptations

### API Integration

Use this pattern when you need to enforce quality programmatically:

```python
def reflection_pattern(question, context):
    # Phase 1: Initial answer
    initial = llm.generate(f"Answer this question: {question}\nContext: {context}")

    # Phase 2: Self-critique
    critique_prompt = f"""
    Critically evaluate this answer:
    Question: {question}
    Answer: {initial}

    Find errors, gaps, biases, and risks.
    Then provide a revised, improved answer.
    """

    reflection = llm.generate(critique_prompt)

    return {
        "initial_answer": initial,
        "reflection": reflection,
        "final_answer": extract_revised_answer(reflection)
    }
```## Variables

_No bracketed variables detected._

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
| `["...", "..."]` | AUTO-GENERATED: describe `"...", "..."` |
| `[Apply critical evaluation framework]` | AUTO-GENERATED: describe `Apply critical evaluation framework` |
| `[Explain your confidence level]` | AUTO-GENERATED: describe `Explain your confidence level` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Generate initial answer]` | AUTO-GENERATED: describe `Generate initial answer` |
| `[If applicable]` | AUTO-GENERATED: describe `If applicable` |
| `[Improved answer incorporating the critique]` | AUTO-GENERATED: describe `Improved answer incorporating the critique` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

