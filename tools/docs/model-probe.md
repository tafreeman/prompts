# Model Probe (`model_probe.py`)

> **Model discovery and availability checking** - Always use before batch operations to avoid wasted runs.

---

## ⚡ Quick Start

```powershell
# Discover ALL available models (run this FIRST)
python tools/model_probe.py --discover -o discovery_results.json

# Check specific models
python tools/model_probe.py gh:gpt-4o-mini local:phi4 ollama:deepseek-r1:14b

# Clear cache and re-probe
python tools/model_probe.py --clear-cache
python tools/model_probe.py --discover --force
```

---

## Why Use Model Probe?

**Critical before batch operations:**

- Avoids wasted evaluation runs on unavailable models
- Intelligent caching reduces repeated probes
- Classifies errors as permanent vs transient

**Cache TTL:**

- Success: 1 hour
- Permanent Error: 24 hours  
- Transient Error: 5 minutes

---

## CLI Usage

```powershell
# Full discovery (all providers)
python tools/model_probe.py --discover -v

# Probe all GitHub models
python tools/model_probe.py --all-github --force

# Probe all local ONNX models
python tools/model_probe.py --all-local

# Check specific models
python tools/model_probe.py gh:gpt-4o-mini local:phi4 ollama:deepseek-r1:14b

# Output to file
python tools/model_probe.py --discover -o discovery_results.json

# Force re-probe (ignore cache)
python tools/model_probe.py --discover --force

# Clear cache
python tools/model_probe.py --clear-cache
```

---

## Python API

### Quick Check

```python
from tools.model_probe import is_model_usable

# Simple boolean check
if is_model_usable("gh:gpt-4o-mini"):
    print("Model is available")
else:
    print("Model is not available")
```

### Detailed Probing

```python
from tools.model_probe import ModelProbe

probe = ModelProbe(verbose=True)

# Check single model
result = probe.check_model("gh:gpt-4o-mini")
if result.usable:
    print("Model is ready!")
else:
    print(f"Model unavailable: {result.error_message}")
    print(f"Should retry later: {result.should_retry}")
```

### Filter Runnable Models

```python
from tools.model_probe import ModelProbe

probe = ModelProbe()
models = ["gh:gpt-4o-mini", "local:phi4", "gh:unavailable-model"]

# Get only models that work
runnable = probe.filter_runnable(models)
print(f"Runnable models: {runnable}")
```

### Full Discovery

```python
from tools.model_probe import discover_all_models

discovered = discover_all_models(verbose=True)
print(f"Total available: {discovered['summary']['total_available']}")
print(f"By provider: {discovered['by_provider']}")
```

---

## Error Classification

The probe classifies errors to determine retry behavior:

| Error Type | Should Retry? | Examples |
|------------|---------------|----------|
| `unavailable_model` | NO | Model not found |
| `permission_denied` | NO | Auth failed |
| `rate_limited` | YES (wait) | 429 Too Many Requests |
| `timeout` | YES | Connection timeout |
| `network_error` | YES | Connection refused |
| `parse_error` | YES | Invalid response |

```python
from tools.model_probe import classify_error

error_code, should_retry = classify_error("429 rate limit exceeded")
if should_retry:
    time.sleep(60)  # Wait before retry
```

---

## Pre-Batch Workflow

**Always run before batch evaluations:**

```powershell
# Step 1: Discover available models
python tools/model_probe.py --discover --force -o discovery.json

# Step 2: Review results
type discovery.json

# Step 3: Run evaluation with available models only
python -m prompteval prompts/ -m phi4,gpt-4o-mini
```

**In Python:**

```python
from tools.model_probe import is_model_usable, discover_all_models
import sys

# Pre-check for batch operations
def validate_models(required_models: list[str]) -> list[str]:
    """Check models and return only usable ones."""
    usable = []
    for model in required_models:
        if is_model_usable(model):
            usable.append(model)
        else:
            print(f"WARNING: {model} not available")
    
    if not usable:
        print("FATAL: No models available!", file=sys.stderr)
        sys.exit(1)
    
    return usable

# Usage
models = validate_models(["local:phi4", "gh:gpt-4o-mini"])
print(f"Proceeding with: {models}")
```

---

## Cache Location

Probe results are cached at:

```
~/.cache/prompts-eval/model-probes/
```

---

## See Also

- [llm-client.md](./llm-client.md) - LLM dispatcher
- [../EXECUTION_GUIDELINES.md](../EXECUTION_GUIDELINES.md) - Mandatory patterns
