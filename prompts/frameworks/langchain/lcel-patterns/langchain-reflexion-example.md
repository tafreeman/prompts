---
name: LangChain LCEL Pattern with Reflexion
description: A prompt for langchain lcel pattern with reflexion tasks.
type: how_to
---

# LangChain LCEL Pattern with Reflexion

## Description

This pattern demonstrates how to implement Reflexion self-correction workflows using LangChain Expression Language (LCEL). Combines LCEL's composability with iterative improvement through initial analysis, self-evaluation, and refined output generation.

## Prompt

```text
### Initial Analysis Prompt
Analyze the following code for potential issues:
Code: {code}
Provide your initial analysis:

### Reflection Prompt
You provided this initial analysis: {initial_analysis}
Now critically evaluate your analysis:
- What did you miss?
- Were there assumptions you made?
- What edge cases did you not consider?

### Improvement Prompt
Original code: {code}
Your initial analysis: {initial_analysis}
Your self-evaluation: {reflection}
Now provide an improved, comprehensive analysis addressing the gaps you identified:
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{code}` | The code to analyze | `def calc(x): return x*2` |
| `{initial_analysis}` | Output from initial analysis step | "The function lacks docstrings..." |
| `{reflection}` | Self-evaluation of initial analysis | "I missed edge cases for None..." |

## Example

**Input:**

```python
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
```

**Output:**

- **Initial Analysis**: "Function calculates average but has no error handling."
- **Reflection**: "I missed: empty list handling, non-numeric input validation."
- **Final Analysis**: "Function needs try/except for empty lists, type checking for inputs, and docstring documentation."

## Purpose

## Overview

This pattern combines:

- LangChain's LCEL composability
- Reflexion's self-correction approach
- Structured output parsing

## Implementation

```python
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from typing import Dict

# Define prompt templates

initial_prompt = ChatPromptTemplate.from_template("""
Analyze the following code for potential issues:

Code:
{code}

Provide your initial analysis:
""")

reflection_prompt = ChatPromptTemplate.from_template("""
You provided this initial analysis:
{initial_analysis}

Now critically evaluate your analysis:

- What did you miss?
- Were there assumptions you made?
- What edge cases did you not consider?

Provide your self-evaluation:
""")

improved_prompt = ChatPromptTemplate.from_template("""
Original code:
{code}

Your initial analysis:
{initial_analysis}

Your self-evaluation:
{reflection}

Now provide an improved, comprehensive analysis addressing the gaps you identified:
""")

# Create LLM

llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.3)

# Build reflexion chain using LCEL

reflexion_chain = (
    {
        "code": RunnablePassthrough(),
        "initial_analysis": initial_prompt | llm | StrOutputParser()
    }
    | RunnablePassthrough.assign(
        reflection=lambda x: (
            reflection_prompt.format(initial_analysis=x["initial_analysis"])
            | llm | StrOutputParser()
        ).invoke({})
    )
    | RunnablePassthrough.assign(
        final_analysis=lambda x: (
            improved_prompt.format(
                code=x["code"],
                initial_analysis=x["initial_analysis"],
                reflection=x["reflection"]
            )
            | llm | StrOutputParser()
        ).invoke({})
    )
)

# Usage

result = reflexion_chain.invoke("""
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
""")

print("Initial Analysis:", result["initial_analysis"])
print("\nReflection:", result["reflection"])
print("\nFinal Analysis:", result["final_analysis"])

```

## Advanced Pattern: Multi-Iteration LCEL

```python
from langchain_core.runnables import RunnableBranch

def create_multi_iteration_reflexion(max_iterations: int = 3):
    """Create a reflexion chain with multiple iterations"""

    def should_continue(state: Dict) -> bool:
        """Decide if we need another iteration"""
        iteration = state.get("iteration", 0)
        confidence = state.get("confidence", 0)
        return iteration < max_iterations and confidence < 8.0

    def extract_confidence(text: str) -> float:
        """Extract confidence score from analysis"""
        # Simplified - in production, use structured output
        import re
        match = re.search(r'confidence[:\s]+(\d+(?:\.\d+)?)', text.lower())
        return float(match.group(1)) if match else 5.0

    # Iteration chain
    iteration_chain = (
        RunnablePassthrough.assign(
            analysis=lambda x: (
                initial_prompt.format(code=x["code"])
                | llm | StrOutputParser()
            ).invoke({})
        )
        | RunnablePassthrough.assign(
            confidence=lambda x: extract_confidence(x["analysis"])
        )
        | RunnablePassthrough.assign(
            iteration=lambda x: x.get("iteration", 0) + 1
        )
        | RunnableBranch(
            (should_continue, lambda x: iteration_chain.invoke(x)),
            lambda x: x  # Base case: return final result
        )
    )

    return iteration_chain
```

## Structured Output with Pydantic

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class CodeAnalysis(BaseModel):
    """Structured code analysis output"""
    issues: list[str] = Field(description="List of identified issues")
    severity: str = Field(description="Overall severity: low, medium, high")
    confidence: float = Field(description="Confidence score 0-10")
    recommendations: list[str] = Field(description="Improvement recommendations")

# Create parser
parser = PydanticOutputParser(pydantic_object=CodeAnalysis)

# Update prompt with format instructions
structured_prompt = ChatPromptTemplate.from_template("""
Analyze the code and provide output in this format:
{format_instructions}

Code:
{code}
""").partial(format_instructions=parser.get_format_instructions())

# Chain with structured output
structured_chain = structured_prompt | llm | parser

result: CodeAnalysis = structured_chain.invoke({"code": "..."})
print(f"Found {len(result.issues)} issues with {result.severity} severity")
```

## Best Practices

1. **Use `RunnablePassthrough.assign()`** for building state across steps
2. **Leverage streaming** for better UX during long reflexion cycles  
3. **Add timeout handling** for iteration chains
4. **Use structured outputs** when parsing complex results

## Related Examples

- [LangChain Agent Patterns](../agent-patterns/langchain-agents.md)
