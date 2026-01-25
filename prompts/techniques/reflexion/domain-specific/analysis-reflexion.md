---
name: Analysis Reflexion Pattern
description: A prompt for analysis reflexion pattern tasks.
type: how_to
---
## Description

## Prompt

```markdown
You are a Principal Software Architect.

**Task**: Analyze the following system design for scalability bottlenecks.

**System Design**:
{{system_design}}

**Output**: Provide an initial analysis of potential scalability issues.
```

A prompt for analysis reflexion pattern tasks.

## Description

## Prompt

```markdown
You are a Principal Software Architect.

**Task**: Analyze the following system design for scalability bottlenecks.

**System Design**:
{{system_design}}

**Output**: Provide an initial analysis of potential scalability issues.
```

A prompt for analysis reflexion pattern tasks.


# Analysis Reflexion Pattern

## Purpose

Ensure deep, comprehensive analysis of complex topics (architecture, security, requirements) by forcing the model to critique its own analysis for gaps, bias, and superficiality before finalizing the output.

## Overview

Standard analysis prompts often yield surface-level observations. This pattern forces a "Deep Dive" cycle:

1. **Initial Analysis**: Broad sweep of the topic.
2. **Gap Analysis (Reflexion)**: "What did I miss? What assumptions did I make?"
3. **Deepened Analysis**: addressing the identified gaps.

## Prompt

### Step 1: Initial Analysis

```markdown
You are a Principal Software Architect.

**Task**: Analyze the following system design for scalability bottlenecks.

**System Design**:
{{system_design}}

**Output**: Provide an initial analysis of potential scalability issues.
```text

### Step 2: Reflexion (Self-Critique)

```markdown
Review your initial analysis above.

**Critique Criteria**:

1.  **Depth**: Did you identify specific components or just general concepts?
2.  **Edge Cases**: Did you consider peak load, failover, or network partitions?
3.  **Assumptions**: What unverified assumptions are you making about the technology stack?
4.  **Missing Perspectives**: Did you consider database locking, connection pooling, or cache invalidation?

**List 3-5 specific gaps or weaknesses in your initial analysis.**
```sql

### Step 3: Refined Analysis

```markdown
Based on the gaps identified, rewrite your analysis.

**Requirements**:

- Address all the gaps you found.
- Be specific about technologies and patterns (e.g., "Use Redis Cluster" instead of "Use caching").
- Provide concrete mitigation strategies for each bottleneck.

**Final Analysis**:
```text

## Example

### Scenario: analyzing a monolithic e-commerce app

**Initial Analysis (Weak)**:
"The system might be slow because it's a monolith. The database could get overloaded. We should use microservices."

**Reflexion**:
"1. **Depth**: 'Database overloaded' is too vague. Which tables? Reads or writes?

2. **Assumptions**: Assumed microservices are the only solution without considering modular monoliths.
3. **Missing**: Didn't mention specific bottlenecks like the checkout transaction lock or inventory decrementing."

**Refined Analysis (Strong)**:
"The primary bottleneck is the **Inventory Table** during flash sales. Row-level locking on high-demand items will cause transaction timeouts.

* **Mitigation**: Implement optimistic concurrency control or use a Redis Lua script for atomic inventory decrementing.
* **Architecture**: Decompose the 'Order Processing' module into a worker service to offload the main API."

## Usage

### Python Implementation

```python
async def run_analysis_reflexion(client, system_design):
    # 1. Initial Analysis
    analysis = await client.generate(f"Analyze this design: {system_design}")

    # 2. Reflexion
    critique = await client.generate(f"Critique this analysis for depth and missing edge cases: {analysis}")

    # 3. Refinement
    final_output = await client.generate(f"Rewrite the analysis based on this critique: {critique}. Original analysis: {analysis}")

    return final_output
```text

## Best Practices

1. **Persona**: Assign a strict persona (e.g., "Security Auditor", "Database Expert") to the critique step.
2. **Specific Criteria**: Don't just ask "Is this good?". Ask "Did I miss OWASP Top 10 vulnerability #3?".
3. **Separation**: Ideally, use a different model instance or temperature (0.7) for the critique to avoid "echo chamber" effects.## Variables

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
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
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

