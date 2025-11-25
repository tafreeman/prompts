---
title: "Multi-Step Reflexion Pattern"
category: "techniques"
subcategory: "reflexion"
technique_type: "self-correction"
framework_compatibility:
  langchain: ">=0.1.0"
  anthropic: ">=0.8.0"
  openai: ">=1.0.0"
difficulty: "advanced"
use_cases:
  - complex-reasoning
  - code-generation
  - mathematical-proofs
  - creative-writing
performance_metrics:
  accuracy_improvement: "25-40%"
  latency_impact: "high"
  cost_multiplier: "2.0-3.0x"
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - reflexion
  - multi-step
  - iterative
  - self-correction
---

# Multi-Step Reflexion Pattern

## Purpose

The Multi-Step Reflexion Pattern extends the basic reflexion concept by introducing a structured, multi-stage iterative process. Unlike basic reflexion which typically involves a single "critique-revise" loop, this pattern orchestrates a sequence of distinct reflection stages (e.g., planning, drafting, critiquing, refining) to handle complex tasks that require deep reasoning or high precision.

## Overview

This pattern implements a state-machine approach to prompt engineering where the model moves through defined stages:

1. **Initial Reasoning/Planning**: Deconstruct the problem.
2. **Draft Generation**: Create a first attempt.
3. **Structured Critique**: Evaluate against specific criteria.
4. **Refinement**: Improve based on critique.
5. **Final Verification**: Ensure all requirements are met.

## Prompt Template

```markdown
You are an advanced AI assistant capable of complex reasoning and self-correction.
Your goal is to complete the following task with the highest possible quality.

Task: {{task_description}}

You will proceed through the following steps. Do not stop until you have completed all steps.

### Step 1: Analysis & Planning
- Break down the task into components.
- Identify potential challenges and edge cases.
- Outline your approach.

### Step 2: Initial Draft
- Execute your plan to create a first version of the solution.
- Focus on completeness rather than perfection.

### Step 3: Critical Reflection
- Review your Initial Draft.
- Identify at least 3 specific areas for improvement.
- Check against these criteria: {{evaluation_criteria}}
- Be harsh in your critique.

### Step 4: Refined Solution
- Rewrite the solution incorporating your reflections.
- Address every issue identified in Step 3.

### Step 5: Final Verification
- Does the Refined Solution meet all original requirements?
- If yes, present the Final Output.
- If no, list remaining issues and repeat Step 4.

Output Format:
[Step 1: Analysis]
...
[Step 2: Draft]
...
[Step 3: Critique]
...
[Step 4: Refinement]
...
[Final Output]
...
```

## Usage Example: Complex Code Generation

**Input:**
"Write a Python script to recursively traverse a directory, identify duplicate files based on content hash, and delete the duplicates while preserving the oldest version. Handle permission errors gracefully."

**Model Output (Simulated):**

```text
[Step 1: Analysis]
Components:
1. Recursive directory traversal.
2. Hashing file content (MD5 or SHA256) for comparison.
3. Tracking files: Map hash to list of (timestamp, path).
4. Deletion logic: Keep oldest, delete others.
5. Error handling: PermissionError, OSError.

Challenges:
- Large files (memory usage during hashing).
- Race conditions (file deleted during processing).
- System files/Protected directories.

[Step 2: Draft]
(Draft code generated...)
def find_duplicates(dir):
    hashes = {}
    for root, dirs, files in os.walk(dir):
        for f in files:
            path = os.path.join(root, f)
            h = hashlib.md5(open(path, 'rb').read()).hexdigest()
            if h in hashes:
                hashes[h].append(path)
            else:
                hashes[h] = [path]
    # ... (rest of draft)

[Step 3: Critique]
1. Memory Issue: `open(path, 'rb').read()` loads entire file into memory. Will crash on large files.
2. Logic Error: The draft doesn't check timestamps to preserve the oldest. It just groups them.
3. Error Handling: No try/except blocks for PermissionError as requested.
4. Efficiency: MD5 is faster but SHA256 is safer, though for dedup MD5 is usually acceptable. I should use chunked reading.

[Step 4: Refinement]
(Refined code generated...)
import os
import hashlib
import logging

def get_file_hash(filepath, chunk_size=8192):
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, OSError) as e:
        logging.warning(f"Skipping {filepath}: {e}")
        return None

def clean_duplicates(start_dir):
    hashes = {}
    # ... (Implementation with timestamp comparison and error handling)

[Final Output]
(Final polished script provided)
```

## Python Implementation

```python
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ReflexionStep:
    name: str
    prompt: str
    output: Optional[str] = None

class MultiStepReflexionChain:
    def __init__(self, llm_client, model: str = "gpt-4"):
        self.client = llm_client
        self.model = model
        self.steps = [
            ReflexionStep("Plan", "Analyze the request and create a detailed plan."),
            ReflexionStep("Draft", "Generate an initial solution based on the plan."),
            ReflexionStep("Critique", "Critique the draft. List specific flaws."),
            ReflexionStep("Refine", "Fix the flaws and generate a refined solution.")
        ]

    def execute(self, task: str) -> Dict[str, str]:
        context = f"Task: {task}\n\n"
        results = {}

        for step in self.steps:
            prompt = f"{context}Step: {step.name}\nInstruction: {step.prompt}"
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content
            step.output = content
            results[step.name] = content
            
            # Append to context for next step
            context += f"\n[{step.name} Output]\n{content}\n\n"
        
        return results
```

## Best Practices

1. **Explicit Separation**: Force the model to use headers (e.g., `[Step 1]`) to clearly demarcate phases.
2. **Targeted Critique**: In the critique step, ask for a specific *number* of issues (e.g., "Find 3 flaws") to prevent lazy evaluation.
3. **Stop Sequences**: If using an API, you can use stop sequences to halt generation after each step to process or validate intermediate outputs programmatically.
4. **Context Management**: For very long chains, summarize the "Analysis" and "Draft" steps before feeding them into the "Refinement" step to save tokens.

## Related Patterns

- [Basic Reflexion](../basic-reflexion/basic-reflexion.md)
- [Chain of Thought](https://arxiv.org/abs/2201.11903)
- [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
