# Framework Integrations

AI framework-specific prompt patterns and integration examples.

## 📁 Directory Structure

```
frameworks/
├── langchain/      # LangChain patterns and LCEL examples
├── anthropic/      # Claude and Anthropic SDK patterns
├── openai/         # OpenAI API and function calling
└── microsoft/      # Semantic Kernel and Copilot
```

## 🔗 Framework Categories

### LangChain

**Path:** `langchain/`

Integration examples for LangChain and LCEL (LangChain Expression Language).

**Key Files:**

- [`lcel-patterns/langchain-reflexion-example.md`](./langchain/lcel-patterns/langchain-reflexion-example.md) - Reflexion with LCEL
- `agents/` - LangChain agent patterns
- `chains/` - Chain composition examples

**Minimum Version:** langchain>=0.1.0

### Anthropic

**Path:** `anthropic/`

Claude-specific patterns and Anthropic SDK integration.

**Key Files:**

- `claude-patterns/` - Claude-optimized prompts
- `tool-use/` - Claude tool use patterns
- `constitutional-ai/` - Constitutional AI examples

**Minimum Version:** anthropic>=0.8.0

### OpenAI

**Path:** `openai/`

OpenAI API patterns including function calling and structured outputs.

**Key Files:**

- `function-calling/` - Function calling examples
- `assistants-api/` - Assistants API patterns
- `structured-outputs/` - JSON schema validation

**Minimum Version:** openai>=1.0.0

### Microsoft

**Path:** `microsoft/`

Semantic Kernel and Microsoft Copilot integration patterns.

**Key Files:**

- `semantic-kernel/` - Semantic Kernel examples
- `copilot-patterns/` - GitHub Copilot patterns

## 🚀 Quick Start

### LangChain Example

```python
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Load a pattern
with open('frameworks/langchain/lcel-patterns/langchain-reflexion-example.md') as f:
    # Extract and use the code examples
    pass
```

### Anthropic Example

```python
import anthropic

client = anthropic.Anthropic(api_key="...")
# Use Claude-specific patterns from anthropic/claude-patterns/
```

### OpenAI Example

```python
from openai import OpenAI

client = OpenAI(api_key="...")
# Use function calling patterns from openai/function-calling/
```

## 📦 Installation

Install framework dependencies as needed:

```bash
# Core dependencies
pip install -r requirements.txt

# LangChain
pip install langchain langchain-openai langchain-anthropic

# Anthropic
pip install anthropic

# OpenAI
pip install openai

# Microsoft Semantic Kernel
pip install semantic-kernel
```

## 🔄 Cross-Framework Patterns

Many prompting techniques work across frameworks. See:

- [Techniques Directory](../techniques/README.md) - Framework-agnostic patterns
- Migration guides for porting patterns between frameworks

## 🤝 Contributing

When adding framework examples:

1. Include minimum version requirements
2. Provide working code examples
3. Document framework-specific optimizations
4. Add integration tests

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for details.
