---
name: Anthropic Claude Prompts
description: Claude-specific prompt patterns and optimization techniques for Anthropic's AI models.
---

# Anthropic Claude Prompts

Prompt patterns, optimization techniques, and integration examples specifically designed for Anthropic's Claude models (Claude 3 Opus, Sonnet, and Haiku).

## 📋 Contents

```text
anthropic/
├── README.md                    # This file
├── claude_patterns.py           # Claude-specific optimization utilities
└── tool-use/                    # Claude tool use patterns
    └── claude-tool-use.md       # Tool calling and function execution
```

## ✨ What Makes Claude Special

Claude models have unique capabilities and preferences:

- **XML Tag Structuring**: Claude responds better to XML tags than markdown or plain text
- **Constitutional AI**: Built-in safety and helpfulness principles
- **Extended Context**: Up to 200K tokens of context window
- **Tool Use**: Native function calling with structured outputs
- **Prefill Technique**: Control output format by prefilling Assistant responses

## 🎯 Key Features

### 1. XML Tag Optimization

Claude performs better when prompts use XML tags to structure information:

```xml
<instruction>
You are a helpful AI assistant specialized in [domain].
</instruction>

<user_request>
[User's actual request]
</user_request>

<guidelines>

- Guideline 1
- Guideline 2

</guidelines>
```

**When to Use:**

- Complex prompts with multiple sections
- When you need clear separation of concerns
- For better token efficiency and Claude's comprehension

### 2. Constitutional AI Principles

Built-in safety and ethical guidelines:

```xml
<constitution>

1. Be helpful and harmless
2. Respect user intent
3. Avoid stereotypes and bias
4. Explain limitations clearly

</constitution>
```

**When to Use:**

- Sensitive topics or content moderation
- When ethical considerations are paramount
- Production systems requiring safety guarantees

### 3. Chain of Thought (CoT)

Encourage step-by-step reasoning:

```xml
<thinking>
Please think step-by-step:

1. Analyze the problem
2. Break it into components
3. Consider edge cases
4. Formulate your response

</thinking>
```

**When to Use:**

- Complex analysis or problem-solving
- When you need to see the reasoning process
- Code review or mathematical proofs

### 4. Prefill Technique

Control output format by starting Claude's response:

```python
messages = [
    {"role": "user", "content": "Explain quantum computing"},
    {"role": "assistant", "content": "Here's a comprehensive explanation:\n\n1."}
]
```

**When to Use:**

- Enforce specific output formats
- Skip preambles and get straight to content
- JSON or structured data generation

## 🚀 Quick Start

### Basic Usage

```python
import anthropic

client = anthropic.Anthropic(api_key="your_api_key")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": """
<instruction>
You are a Python expert. Help debug this code.
</instruction>

<code>
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-1)
</code>

<task>
Identify the bug and provide a corrected version.
</task>
"""
        }
    ]
)

print(message.content)
```

### Using the Optimizer

```python
from claude_patterns import ClaudePromptOptimizer

optimizer = ClaudePromptOptimizer()

# Apply XML structuring
raw_prompt = "Explain quantum entanglement simply"
optimized = optimizer.optimize_for_claude(raw_prompt, 'xml_structure')

# Apply Chain of Thought
cot_prompt = optimizer.optimize_for_claude(raw_prompt, 'cot')

# Apply Constitutional principles
safe_prompt = optimizer.optimize_for_claude(raw_prompt, 'constitutional')
```

## 📚 Available Patterns

### Tool Use

**Location:** `tool-use/claude-tool-use.md`

Learn how to:

- Define tools/functions for Claude
- Handle tool use responses
- Chain multiple tool calls
- Implement error handling

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
]

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)
```

### Optimization Utilities

**Location:** `claude_patterns.py`

Python utilities for:

- XML tag structuring
- Constitutional AI integration
- Chain of Thought enforcement
- Assistant prefilling
- Tool definition formatting

## 🎓 Best Practices

### 1. Use XML Tags

✅ **Do:**

```xml
<document>
<title>Document Title</title>
<content>The actual content here</content>
</document>
```

❌ **Don't:**

```markdown
# Document Title
The actual content here
```

### 2. Be Explicit About Output Format

✅ **Do:**

```xml
<instruction>
Respond in JSON format with keys: analysis, recommendation, confidence
</instruction>
```

❌ **Don't:**

```text
Give me a JSON response
```

### 3. Leverage Extended Context

```python
# Claude can handle very long contexts
with open('long_document.txt', 'r') as f:
    document = f.read()  # Can be 100K+ tokens

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": f"""
<document>
{document}
</document>

<task>
Summarize the key findings from this research paper.
</task>
"""
    }]
)
```

### 4. Use Thinking Tags for Complex Tasks

```xml
<task>
Design a distributed system architecture for [use case]
</task>

<thinking>
Think through:

1. Scalability requirements
2. Consistency vs availability tradeoffs
3. Communication patterns
4. Failure modes

Show your reasoning in <thinking> tags before providing the final design.
</thinking>
```

## 📊 Model Comparison

| Model | Context Window | Best For | Cost |
| ------- | --------------- | ---------- | ------ |
| **Claude 3 Opus** | 200K tokens | Complex analysis, creative tasks | Highest |
| **Claude 3.5 Sonnet** | 200K tokens | Balanced performance, coding | Medium |
| **Claude 3 Haiku** | 200K tokens | Speed, simple tasks | Lowest |

## 🔧 Integration Examples

### With LangChain

```python
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

template = """
<instruction>
You are a helpful assistant.
</instruction>

<user_query>
{query}
</user_query>
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm

response = chain.invoke({"query": "Explain recursion"})
```

### With Streaming

```python
with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## 🛠️ Utilities Reference

### ClaudePromptOptimizer Class

| Method | Description | Use Case |
| -------- | ------------- | ---------- |
| `optimize_for_claude()` | Main optimization entry point | General optimization |
| `_apply_xml_structure()` | Wraps content in XML tags | Structured prompts |
| `_apply_constitutional_principles()` | Adds safety guidelines | Sensitive content |
| `_enforce_chain_of_thought()` | Adds thinking instructions | Complex reasoning |
| `_add_assistant_prefill()` | Templates prefill pattern | Output control |
| `format_tool_definition()` | Formats tool schemas | Tool use setup |

## 📖 Additional Resources

### Official Documentation

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Claude Model Guide](https://docs.anthropic.com/claude/docs/models-overview)
- [Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)

### Community Resources

- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [LangChain Anthropic Integration](https://python.langchain.com/docs/integrations/chat/anthropic)

### Research Papers

- [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)
- [Claude 3 Model Family](https://www.anthropic.com/news/claude-3-family)

## 🤝 Contributing

When adding Claude-specific patterns:

1. Test on multiple Claude models (Opus, Sonnet, Haiku)
2. Use XML tags where appropriate
3. Document model-specific behaviors
4. Include token usage estimates
5. Provide comparative examples (Claude vs other models)

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for general guidelines.

## 🐛 Common Issues

### Issue: XML tags appearing in output

**Solution:** Claude sometimes includes XML tags in responses. Use prefill to control this:

```python
messages = [
    {"role": "user", "content": "<task>Analyze this</task>"},
    {"role": "assistant", "content": "Analysis: "}
]
```

### Issue: Inconsistent formatting

**Solution:** Be explicit about output format:

```xml
<instruction>
Respond ONLY with the JSON object. Do not include any explanatory text before or after.
</instruction>
```

### Issue: Tool use not working

**Solution:** Ensure tool definitions match the exact schema format:

```python
{
    "name": "tool_name",
    "description": "Clear description",
    "input_schema": {
        "type": "object",
        "properties": {...},
        "required": [...]
    }
}
```

## 📝 Version History

- **1.0** (2025-11-30): Initial release with core patterns and utilities

---

**Need Help?** Check the [main documentation](../../../docs/) or [open an issue](https://github.com/tafreeman/prompts/issues).
