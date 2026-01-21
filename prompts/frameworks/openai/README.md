---
name: OpenAI Platform Prompts
description: OpenAI API patterns including GPT-4, function calling, assistants, and structured outputs.
---

# OpenAI Platform Prompts

Comprehensive collection of prompts, patterns, and integration examples for OpenAI's API, including GPT-4, function calling, assistants API, and structured outputs.

## 📋 Contents

```text
openai/
├── README.md                    # This file
├── openai_utilities.py          # OpenAI helper utilities
├── assistants-api/              # Assistants API patterns
│   └── openai-assistants.md     # Assistant creation and management
└── function-calling/            # Function calling patterns
    └── (function calling examples)
```

## 🎯 What's Inside

OpenAI provides cutting-edge language models and APIs:

- **GPT-4 & GPT-4 Turbo**: Most capable models
- **GPT-3.5 Turbo**: Fast and cost-effective
- **Function Calling**: Structured tool use
- **Assistants API**: Stateful conversations with tools
- **Vision**: Image understanding (GPT-4V)
- **DALL-E**: Image generation
- **Whisper**: Speech-to-text
- **TTS**: Text-to-speech

## ✨ Key Features

### 1. Chat Completions API

Core API for conversational AI:

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing"}
    ]
)

print(response.choices[0].message.content)
```

### 2. Function Calling

Enable models to call external functions:

```python
functions = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and state, e.g., San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[{"role": "user", "content": "What's the weather in Boston?"}],
    functions=functions,
    function_call="auto"
)
```

### 3. Assistants API

Build stateful assistants with tools:

```python
# Create assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a math tutor. Help students solve problems.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-turbo-preview"
)

# Create thread
thread = client.beta.threads.create()

# Add message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Solve: 3x + 11 = 14"
)

# Run assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)
```

### 4. Structured Outputs

Get JSON responses with schema validation:

```python
from pydantic import BaseModel

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "Extract event details."},
        {"role": "user", "content": "Team meeting on Friday with Alice and Bob"}
    ],
    response_format=CalendarEvent
)

event = completion.choices[0].message.parsed
```

## 🚀 Quick Start

### Installation

```bash
# Install OpenAI Python SDK
pip install openai

# For async support
pip install openai[asyncio]
```

### Basic Usage

```python
from openai import OpenAI

# Initialize client
client = OpenAI(api_key="your-api-key")

# Simple completion
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

print(response.choices[0].message.content)
```

### Streaming Responses

```python
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

### Vision (GPT-4V)

```python
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg"
                    }
                }
            ]
        }
    ]
)
```

## 📚 Common Patterns

### 1. System Prompts

Set behavior and context:

```python
messages = [
    {
        "role": "system",
        "content": """You are an expert Python developer.

        - Write clean, idiomatic code
        - Include type hints
        - Add docstrings
        - Follow PEP 8 style guide"""

    },
    {
        "role": "user",
        "content": "Write a function to calculate factorial"
    }
]
```

### 2. Few-Shot Learning

Provide examples:

```python
messages = [
    {"role": "system", "content": "Convert English to SQL"},
    {"role": "user", "content": "Show all users"},
    {"role": "assistant", "content": "SELECT * FROM users;"},
    {"role": "user", "content": "Show users from California"},
    {"role": "assistant", "content": "SELECT * FROM users WHERE state = 'CA';"},
    {"role": "user", "content": "Count active users"}
]
```

### 3. Conversation History

Maintain context:

```python
conversation = [
    {"role": "system", "content": "You are a helpful assistant."}
]

while True:
    user_input = input("You: ")
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation
    )

    assistant_message = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_message})
    print(f"Assistant: {assistant_message}")
```

### 4. Error Handling

```python
from openai import OpenAIError, RateLimitError, APIError

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError:
    print("Rate limit exceeded. Please retry later.")
except APIError as e:
    print(f"API error: {e}")
except OpenAIError as e:
    print(f"OpenAI error: {e}")
```

## 🔧 Advanced Features

### Temperature and Parameters

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a creative story"}],
    temperature=0.9,        # Higher = more creative (0-2)
    top_p=0.95,             # Nucleus sampling
    frequency_penalty=0.5,  # Reduce repetition
    presence_penalty=0.5,   # Encourage new topics
    max_tokens=1000         # Response length limit
)
```

### JSON Mode

```python
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Respond in JSON."},
        {"role": "user", "content": "List 3 colors"}
    ],
    response_format={"type": "json_object"}
)
```

### Async Support

```python
import asyncio
from openai import AsyncOpenAI

async def main():
    client = AsyncOpenAI(api_key="your-api-key")

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )

    print(response.choices[0].message.content)

asyncio.run(main())
```

### Batch Processing

```python
import asyncio

async def process_batch(prompts):
    client = AsyncOpenAI()

    tasks = [
        client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        for prompt in prompts
    ]

    return await asyncio.gather(*tasks)

prompts = ["Translate 'hello' to Spanish", "What is 2+2?", "Tell me a joke"]
results = asyncio.run(process_batch(prompts))
```

## 🎓 Best Practices

### 1. Use System Messages

✅ **Do:**

```python
{"role": "system", "content": "You are an expert Python developer. Write clean, documented code."}
```

❌ **Don't:**

```python
{"role": "user", "content": "Act as a Python expert and write clean code."}
```

### 2. Be Specific

✅ **Do:**

```python
"""Generate a Python function that:

- Accepts a list of integers
- Returns the median value
- Handles empty lists by returning None
- Includes type hints and docstring"""

```

❌ **Don't:**

```python
"Write a median function"
```

### 3. Use Appropriate Models

| Model | Use Case | Cost |
| ------- | ---------- | ------ |
| **gpt-4-turbo** | Complex reasoning, coding | High |
| **gpt-4** | High-quality outputs | Highest |
| **gpt-3.5-turbo** | Simple tasks, speed | Low |

### 4. Implement Token Management

```python
import tiktoken

def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Truncate if needed
def truncate_conversation(messages, max_tokens=4000):
    total_tokens = sum(count_tokens(m["content"]) for m in messages)

    while total_tokens > max_tokens and len(messages) > 1:
        messages.pop(1)  # Remove oldest message after system
        total_tokens = sum(count_tokens(m["content"]) for m in messages)

    return messages
```

## 📊 Model Comparison

| Model | Context | Capabilities | Best For |
| ------- | --------- | -------------- | ---------- |
| **GPT-4 Turbo** | 128K | Vision, JSON, functions | Complex tasks, long context |
| **GPT-4** | 8K | High reasoning | Quality over speed |
| **GPT-3.5 Turbo** | 16K | Fast, cost-effective | Simple tasks, high volume |

## 🛠️ Utilities Reference

The `openai_utilities.py` module provides helper functions:

```python
from openai_utilities import (
    create_chat_completion,
    stream_chat_completion,
    function_call_handler,
    count_tokens,
    estimate_cost
)

# Easy completions
response = create_chat_completion(
    messages=[{"role": "user", "content": "Hello"}],
    model="gpt-4"
)

# Streaming helper
for chunk in stream_chat_completion(messages):
    print(chunk, end="")

# Token counting
tokens = count_tokens(text, model="gpt-4")

# Cost estimation
cost = estimate_cost(tokens, model="gpt-4")
```

## 📖 Additional Resources

### Official Documentation

- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)
- [Best Practices Guide](https://platform.openai.com/docs/guides/prompt-engineering)

### Pricing

- [OpenAI Pricing](https://openai.com/pricing)

### Community

- [OpenAI Community Forum](https://community.openai.com/)
- [OpenAI Discord](https://discord.gg/openai)

## 🤝 Contributing

When adding OpenAI patterns:

1. Test with latest API version
2. Include error handling
3. Document token usage
4. Provide cost estimates
5. Include both sync and async examples where relevant

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

## 🐛 Common Issues

### Issue: Rate limit errors

**Solution:** Implement exponential backoff:

```python
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
def make_request():
    return client.chat.completions.create(...)
```

### Issue: Token limit exceeded

**Solution:** Truncate or summarize:

```python
# Truncate conversation history
messages = truncate_conversation(messages, max_tokens=4000)

# Or use summarization
summary = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"Summarize: {long_text}"}]
)
```

### Issue: Inconsistent outputs

**Solution:** Set temperature to 0 for deterministic results:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    temperature=0  # Deterministic
)
```

## 📝 Version History

- **1.0** (2025-11-30): Initial release with chat completions, functions, and assistants

---

**Need Help?** Check the [OpenAI documentation](https://platform.openai.com/docs) or [open an issue](https://github.com/tafreeman/prompts/issues).
