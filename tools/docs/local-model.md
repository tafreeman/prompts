# Local Model (`local_model.py`)

> **Direct interface to local ONNX models** via `onnxruntime-genai` - Text generation and prompt evaluation with zero API costs.

---

## ⚡ Quick Start

```powershell
# Generate text
python tools/local_model.py --model phi4 "What is machine learning?"

# Evaluate a prompt
python tools/local_model.py --evaluate prompts/example.md

# Check available models
python tools/local_model.py --info
```

---

## Available Models

| Key | Model | Params | Hardware |
|-----|-------|--------|----------|
| `phi4` / `phi4-cpu` | Phi-4 Mini | 3.8B | CPU |
| `phi4-gpu` | Phi-4 Mini | 3.8B | GPU |
| `phi4mini` | Phi-4 Mini (alt) | 3.8B | CPU |
| `phi3.5` | Phi-3.5 Mini | 3.8B | CPU |
| `phi3.5-vision` | Phi-3.5 Vision | 4.2B | CPU |
| `phi3` / `phi3-cpu` | Phi-3 Mini | 3.8B | CPU |
| `phi3-dml` | Phi-3 Mini | 3.8B | GPU (DirectML) |
| `phi3-medium` | Phi-3 Medium | 14B | CPU |
| `mistral` / `mistral-7b` | Mistral 7B | 7B | CPU |
| `mistral-dml` | Mistral 7B | 7B | GPU |
| `whisper-*` | Whisper (speech) | Various | CPU |
| `stable-diffusion` | Stable Diffusion | - | GPU |

---

## CLI Usage

```powershell
# Text generation
python tools/local_model.py --model phi4 "Explain quantum computing"

# Evaluate prompt (6 criteria)
python tools/local_model.py --evaluate prompts/example.md

# G-Eval with Chain-of-Thought reasoning
python tools/local_model.py --geval prompts/example.md

# Dual evaluation (both methods)
python tools/local_model.py --dual prompts/example.md

# Check what models are available
python tools/local_model.py --info
```

---

## Python API

### Text Generation

```python
from tools.local_model import LocalModel, check_model_available, get_model_info

# Check availability first
if not check_model_available():
    print("No local model available!")
    sys.exit(1)

# Initialize with specific model
model = LocalModel(model_key="phi4", verbose=True)

# Generate text
response = model.generate(
    prompt="Explain quantum computing",
    max_tokens=1000,
    temperature=0.7,
    system_prompt="You are a physics expert."
)
```

### Prompt Evaluation

Three evaluation methods are available:

| Method | Description | Best For |
|--------|-------------|----------|
| `evaluate_prompt()` | Direct 6-criteria scoring | Fast evaluation |
| `evaluate_prompt_geval()` | G-Eval with Chain-of-Thought | Explainable scoring |
| `evaluate_prompt_dual()` | Both methods combined | Most robust evaluation |

```python
from tools.local_model import LocalModel

model = LocalModel()
prompt_content = open("prompts/example.md").read()

# Direct scoring (6 criteria)
result = model.evaluate_prompt(prompt_content)
print(f"Score: {result['overall']}/100")

# G-Eval with CoT reasoning (NeurIPS 2023 methodology)
result = model.evaluate_prompt_geval(prompt_content)
print(f"Score: {result['overall']}")
print(f"Reasoning: {result['criteria_results']}")

# Dual evaluation (most robust)
result = model.evaluate_prompt_dual(prompt_content)
print(f"Combined Score: {result['combined_score']}")
```

---

## Model Cache Location

Local ONNX models are cached at:

| Cache | Location |
|-------|----------|
| AI Gallery | `~/.cache/aigallery/` |
| AI Toolkit | `~/.aitk/models/` |

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'onnxruntime_genai'"

```powershell
# Install CPU version
pip install onnxruntime-genai

# Install GPU/DirectML version
pip install onnxruntime-genai-directml

# Install both
pip install onnxruntime-genai onnxruntime-genai-directml
```

### "Model not found"

```powershell
# Check AI Gallery cache
dir $HOME\.cache\aigallery

# Check AI Toolkit models
dir $HOME\.aitk\models
```

### Unicode errors on Windows

```powershell
$env:PYTHONIOENCODING = "utf-8"
python -X utf8 tools/local_model.py --info
```

---

## See Also

- [llm-client.md](./llm-client.md) - Unified LLM dispatcher
- [model-probe.md](./model-probe.md) - Model discovery
- [../WINDOWS_AI_README.md](../WINDOWS_AI_README.md) - Windows AI/NPU setup
