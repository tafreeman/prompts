---
title: "Claude Tool Use Pattern"
category: "frameworks"
subcategory: "anthropic"
technique_type: "tool-use"
framework_compatibility:
  anthropic: ">=0.8.0"
difficulty: "intermediate"
use_cases:
  - data-extraction
  - api-integration
  - complex-workflows
performance_metrics:
  accuracy_improvement: "20-30%"
  latency_impact: "medium"
version: "1.0.0"
author: "AI Research Team"
last_updated: "2025-11-23"
tags:
  - anthropic
  - claude
  - tool-use
  - function-calling
---

# Claude Tool Use Pattern

## Purpose

Demonstrates how to effectively define and use tools (functions) with Anthropic's Claude models. Claude 3 models are highly optimized for tool use, allowing for reliable structured data extraction and API integration.

## Overview

This pattern covers:

1. **Tool Definition**: Correct JSON schema structure.
2. **System Prompting**: Instructions for tool usage.
3. **Chain of Thought**: Encouraging reasoning before tool calls.
4. **Handling Results**: Processing tool outputs.

## Tool Definition Example

```python
weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
            }
        },
        "required": ["location"]
    }
}
```

## Prompt Template

```markdown
You are a helpful assistant with access to the following tools:
{{tool_definitions}}

Your goal is to assist the user by using these tools when necessary.

<instructions>
1. **Think before you act**: Analyze the user's request. Determine if a tool is needed.
2. **Chain of Thought**: If a tool is needed, output your reasoning in <thinking> tags before calling the tool.
3. **Tool Call**: Use the provided tool format to execute the action.
4. **Response**: Once you have the tool result, formulate a natural language response to the user.
</instructions>

<user_request>
{{user_input}}
</user_request>
```

## Python Implementation (Anthropic SDK)

```python
import anthropic
import json

client = anthropic.Anthropic()

def run_conversation(user_input):
    # 1. Define tools
    tools = [
        {
            "name": "get_stock_price",
            "description": "Get the current stock price for a given ticker symbol.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "The stock ticker symbol, e.g. AAPL"},
                },
                "required": ["ticker"]
            }
        }
    ]

    # 2. Initial API Call
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        tools=tools,
        messages=[{"role": "user", "content": user_input}]
    )

    # 3. Process Tool Use
    final_content = []
    
    for content_block in response.content:
        if content_block.type == "tool_use":
            tool_name = content_block.name
            tool_input = content_block.input
            tool_use_id = content_block.id
            
            print(f"Tool Call: {tool_name}({tool_input})")
            
            # Simulate tool execution
            if tool_name == "get_stock_price":
                result = {"price": 150.00, "currency": "USD"}
                
                # 4. Respond with Tool Result
                tool_result_message = {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": json.dumps(result)
                        }
                    ]
                }
                
                # 5. Get Final Answer
                final_response = client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1024,
                    tools=tools,
                    messages=[
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": response.content},
                        tool_result_message
                    ]
                )
                return final_response.content[0].text
        
        elif content_block.type == "text":
            final_content.append(content_block.text)

    return "".join(final_content)

# Example
# print(run_conversation("What is the stock price of Apple?"))
```

## Best Practices

1. **Clear Descriptions**: The `description` field in the tool definition is part of the prompt. Make it descriptive and precise.
2. **CoT for Complex Logic**: For multi-step tasks, explicitly ask Claude to output `<thinking>` tags before the tool use block. This improves accuracy significantly.
3. **Error Handling**: If a tool fails, return a `tool_result` with `is_error: true` and a clear error message. Claude can often self-correct.
4. **System Prompt**: Reinforce the persona and constraints in the system prompt, separate from the tool definitions.

## Related Patterns

- [OpenAI Function Calling](../openai/function-calling/openai-function-calling.md)
- [Agentic Workflows](../../techniques/agentic/multi-agent/multi-agent-workflow.md)
