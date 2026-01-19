# LLM Client (`llm_client.py`)

> **Unified LLM dispatcher for all providers** - Routes requests to the appropriate backend based on model prefix.

---

## ⚡ Quick Start

```powershell
# Use through prompt.py CLI (recommended)
python prompt.py run prompts/example.md -p local -m phi4

# Direct Python usage
python -c "from tools.llm_client import LLMClient; print(LLMClient.generate_text('local:phi4', 'Hello world'))"
```

---

## Supported Providers

| Prefix | Provider | Cost | Requirements |
| -------- | ---------- | ------ | -------------- |
| `local:*` | Local ONNX | $0 | onnxruntime-genai + model files |
| `windows-ai:*` | Windows AI (NPU) | $0 | Windows 11 + NPU + LAF token |
| `gh:*` | GitHub Models | FREE tier | gh CLI + auth |
| `ollama:*` | Ollama | $0 | Ollama server running |
| `aitk:*` | AI Toolkit | $0 | VS Code AI Toolkit models |
| `azure-foundry:*` | Azure Foundry | Pay-per-use | API key + endpoint |
| `azure-openai:*` | Azure OpenAI | Pay-per-use | API key + endpoint |
| `openai:*` | OpenAI | Paid | OPENAI_API_KEY |
| `gemini:*` | Google Gemini | Varies | GEMINI_API_KEY |
| `claude:*` | Anthropic Claude | Paid | CLAUDE_API_KEY |

---

## Python API

### Basic Usage

```python
from tools.llm_client import LLMClient

# Simple generation (auto-routes based on prefix)
response = LLMClient.generate_text("local:phi4", "What is 2+2?")

# With system instruction
response = LLMClient.generate_text(
    "local:phi4",
    "Review this code",
    system_instruction="You are a code reviewer.",
    temperature=0.3,
    max_tokens=2000
)
```

### Provider-Specific Examples

```python
# Local ONNX model (FREE)
response = LLMClient.generate_text("local:phi4", "What is recursion?")

# GitHub Models (FREE tier)
response = LLMClient.generate_text("gh:gpt-4o-mini", "Explain REST APIs")

# Ollama (FREE, requires server)
response = LLMClient.generate_text("ollama:deepseek-r1:14b", "Hello world")

# Windows AI (NPU - requires LAF token)
response = LLMClient.generate_text("windows-ai:phi-silica", "Summarize this")
```

---

## CLI Usage

```powershell
# Through prompt.py (recommended)
python prompt.py run prompts/example.md -p local -m phi4
python prompt.py run prompts/example.md -p gh -m gpt-4o-mini
python prompt.py run prompts/example.md -p windows

# Direct execution with Python
python -c "from tools.llm_client import LLMClient; print(LLMClient.generate_text('gh:gpt-4o-mini', 'Hello'))"
```

---

## Environment Variables

| Variable | Provider | Required |
| ---------- | ---------- | ---------- |
| `GITHUB_TOKEN` | GitHub Models (`gh:*`) | Yes |
| `OPENAI_API_KEY` | OpenAI (`openai:*`) | Yes |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI | Yes |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI | Yes |
| `AZURE_FOUNDRY_ENDPOINT` | Azure Foundry | Yes |
| `AZURE_FOUNDRY_API_KEY` | Azure Foundry | Yes |
| `GEMINI_API_KEY` | Google Gemini | Yes |
| `CLAUDE_API_KEY` | Anthropic Claude | Yes |
| `OLLAMA_HOST` | Ollama | Optional (default: localhost:11434) |

---

## Troubleshooting

### "Model not found"

```powershell
# Check available models
python tools/model_probe.py --discover
```

### "401 Unauthorized" (GitHub Models)

```powershell
gh auth status
gh auth login
```

### "Connection refused" (Ollama)

```powershell
ollama serve  # Start server
ollama list   # Check models
```

---

## See Also

- [model-probe.md](./model-probe.md) - Model discovery
- [local-model.md](./local-model.md) - Direct ONNX interface
- [../EXECUTION_GUIDELINES.md](../EXECUTION_GUIDELINES.md) - Execution patterns
