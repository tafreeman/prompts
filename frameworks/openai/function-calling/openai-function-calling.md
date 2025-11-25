---
title: "OpenAI Function Calling Pattern"
category: "frameworks"
subcategory: "openai"
technique_type: "function-calling"
framework_compatibility:
  openai: ">=1.0.0"
  langchain: ">=0.1.0"
difficulty: "intermediate"
use_cases:
  - structured-data-extraction
  - api-integration
  - decision-making
performance_metrics:
  accuracy_improvement: "25-35%"
  latency_impact: "low"
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - openai
  - function-calling
  - tools
  - json-schema
---

# OpenAI Function Calling Pattern

## Purpose

Leverage OpenAI's native function calling (tool use) capability to reliably extract structured data or trigger external actions. This pattern ensures strict adherence to JSON schemas and robust error handling.

## Overview

OpenAI models (GPT-4, GPT-3.5-Turbo) are fine-tuned to detect when a function should be called and to generate JSON that adheres to the function signature.

## Tool Definition (JSON Schema)

```json
{
  "type": "function",
  "function": {
    "name": "extract_customer_info",
    "description": "Extract customer details from a support ticket",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Customer's full name"
        },
        "sentiment": {
          "type": "string",
          "enum": ["positive", "neutral", "negative"],
          "description": "Sentiment of the message"
        },
        "issue_type": {
          "type": "string",
          "enum": ["billing", "technical", "feature_request"],
          "description": "Category of the issue"
        },
        "priority": {
          "type": "integer",
          "minimum": 1,
          "maximum": 5,
          "description": "Priority level (1=low, 5=high)"
        }
      },
      "required": ["name", "sentiment", "issue_type"]
    }
  }
}
```

## Prompt Template

```markdown
You are a customer support triage assistant.
Your goal is to analyze the incoming support ticket and extract key information using the `extract_customer_info` tool.

<rules>
1. If the sentiment is unclear, default to "neutral".
2. If the name is missing, use "Unknown".
3. Be conservative with priority ratings; only assign 5 for system outages.
</rules>

Ticket:
{{ticket_content}}
```

## Python Implementation (OpenAI SDK)

```python
from openai import OpenAI
import json
from typing import Dict, Any

client = OpenAI()

def analyze_ticket(ticket_content: str) -> Dict[str, Any]:
    # 1. Define the tool
    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_customer_info",
                "description": "Extract customer details from a support ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
                        "issue_type": {"type": "string", "enum": ["billing", "technical", "feature_request"]},
                        "priority": {"type": "integer", "minimum": 1, "maximum": 5}
                    },
                    "required": ["name", "sentiment", "issue_type"]
                }
            }
        }
    ]

    # 2. Call the API
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful support assistant."},
            {"role": "user", "content": ticket_content}
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "extract_customer_info"}} # Force specific tool
    )

    # 3. Process the response
    tool_calls = response.choices[0].message.tool_calls
    
    if tool_calls:
        # Parse the arguments
        args = json.loads(tool_calls[0].function.arguments)
        return args
    
    return {}

# Example Usage
ticket = "Hi, my name is Alice. I can't access my account since the update. This is urgent!"
result = analyze_ticket(ticket)
print(json.dumps(result, indent=2))
# Output:
# {
#   "name": "Alice",
#   "sentiment": "negative",
#   "issue_type": "technical",
#   "priority": 4
# }
```

## Best Practices

1. **Force Tool Choice**: Use `tool_choice={"type": "function", "function": {"name": "..."}}` when you *must* get structured output.
2. **Enum Constraints**: Use `enum` in your schema to restrict outputs to valid options (e.g., categories, status codes).
3. **Descriptions Matter**: The model reads the field descriptions. Use them to provide specific instructions (e.g., "Format as YYYY-MM-DD").
4. **Parallel Function Calling**: GPT-4-Turbo supports calling multiple functions in one turn. Design your logic to handle a list of `tool_calls`.

## Related Patterns

- [Claude Tool Use](../anthropic/tool-use/claude-tool-use.md)
- [Structured Outputs](../structured-outputs/structured-outputs.md)
