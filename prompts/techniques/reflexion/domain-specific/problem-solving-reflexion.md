---
name: Problem-Solving Reflexion Pattern
description: A prompt for problem solving reflexion pattern tasks.
type: how_to
---
## Description

## Prompt

```markdown
**Problem**:
{{problem_description}}

**Task**: Propose a step-by-step solution.

**Initial Solution**:
```

A prompt for problem solving reflexion pattern tasks.

## Description

## Prompt

```markdown
**Problem**:
{{problem_description}}

**Task**: Propose a step-by-step solution.

**Initial Solution**:
```

A prompt for problem solving reflexion pattern tasks.


# Problem-Solving Reflexion Pattern

## Purpose

Solve complex logical problems or debug difficult errors by iteratively proposing solutions, testing them (mentally or via code), and refining the approach based on failure analysis.

## Overview

This pattern mimics the scientific method or debugging process:

1. **Hypothesis**: Propose a solution or cause.
2. **Verification (Reflexion)**: "Walk through this solution step-by-step. Does it actually work for input X?"
3. **Correction**: Fix the logic errors found during verification.

## Prompt

### Step 1: Problem Statement & Initial Solution

```markdown
**Problem**:
{{problem_description}}

**Task**: Propose a step-by-step solution.

**Initial Solution**:
```text

### Step 2: Verification (The "Rubber Duck" Phase)

```markdown
Review your solution. Simulate the execution with the following edge case input: {{edge_case_input}}.

**Trace**:

1. Step 1 result: ...
2. Step 2 result: ...

...

**Did the solution produce the correct expected output?**
If NO, explain exactly where the logic failed.
```text

### Step 3: Corrected Solution

```markdown
Based on the failure identified in the trace, provide a corrected solution.

**Corrected Solution**:
```text

## Example

### Scenario: Debugging a Deadlock

**Problem**: "Two threads are stuck. Thread A holds Resource 1 and waits for 2. Thread B holds Resource 2 and waits for 1."

**Initial Solution**: "Just add a timeout to the wait calls."

**Verification**:
"Trace: Thread A waits. Timeout fires. Thread A retries. Thread B is still holding Resource 2. Thread A waits again.
*Result*: This doesn't solve the deadlock, it just turns it into a livelock or slow failure loop."

**Corrected Solution**:
"Implement a global resource ordering. All threads must acquire Resource 1 *before* Resource 2. This makes the circular wait condition impossible."

## Usage

### When to Use

- **Debugging**: When the error cause is ambiguous.
- **Algorithmic Challenges**: "Find the shortest path in a graph with negative weights."
- **Incident Response**: "Server is down, logs show high CPU. What do I do?"

### When to Avoid

- **Simple Fact Retrieval**: "What is the capital of France?" (Reflexion adds no value).
- **Creative Writing**: Logic verification stifles creativity.

## Best Practices

1. **Concrete Inputs**: Always verify with specific data (e.g., `input = [1, 5, -2]`), not abstract reasoning.
2. **Fatal Flaw Check**: Explicitly ask the model to "Find the fatal flaw" in its plan.
3. **Iterate**: For very hard problems, you may need 3-4 cycles of hypothesis/verification.## Variables

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
| `[1, 5, -2]` | AUTO-GENERATED: describe `1, 5, -2` |
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

