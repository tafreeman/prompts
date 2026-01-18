# Simplified Architecture: Prompt Tools

> **Date**: 2026-01-17  
> **Status**: Proposal v2 - Simplified  
> **Philosophy**: Do less, but do it well

---

## Core Insight

After reviewing the features, most users only need **3 things**:

1. **Evaluate** a prompt (get a score)
2. **Validate** a prompt (check structure)
3. **Call an LLM** (with any provider)

Everything else is either:

- A variation of these 3 (batch, tiered, G-Eval → all just "evaluate")
- A supporting utility (caching, parsing)
- A power-user feature (agents, CoVe)

---

## Simplified Package Structure

```
prompttools/
│
├── __init__.py           # Public API: evaluate(), validate(), generate()
├── __main__.py           # CLI: prompttools evaluate|validate|generate
├── config.py             # All configuration in one place
│
├── llm.py                # Single unified LLM client (400 lines max)
│                         # Contains all providers inline - they're small
│
├── evaluate.py           # All evaluation logic (direct, geval, tiered)
│                         # ~500 lines, no submodules needed
│
├── validate.py           # All validation logic (structure, frontmatter)
│                         # ~300 lines, no submodules needed
│
├── cache.py              # Response caching (single implementation)
│
├── parse.py              # JSON/YAML extraction utilities
│
├── cli.py                # Simple CLI with 3 commands
│
└── rubrics/              # Only external data files
    ├── scoring.yaml
    └── criteria.yaml
```

**That's it. 8 files + 1 data folder.**

---

## Why This Works

### Before: Over-Abstracted

```
providers/
├── base.py           # Abstract class
├── local_onnx.py     # 80 lines
├── ollama.py         # 60 lines
├── github_models.py  # 70 lines
├── azure_openai.py   # 90 lines
├── openai.py         # 50 lines
├── gemini.py         # 40 lines
├── claude.py         # 40 lines
└── ...
```

**11 files for ~500 lines of code total.**

### After: Practical

```python
# llm.py - all providers in one file

def generate(model: str, prompt: str, **kwargs) -> str:
    """Route to appropriate provider and generate response."""
    provider = model.split(":")[0]
    
    if provider == "local":
        return _call_local(model, prompt, **kwargs)
    elif provider == "ollama":
        return _call_ollama(model, prompt, **kwargs)
    elif provider == "gh":
        return _call_github(model, prompt, **kwargs)
    # ... etc


def _call_local(model: str, prompt: str, **kwargs) -> str:
    """Call local ONNX model."""
    # 50 lines of ONNX logic


def _call_ollama(model: str, prompt: str, **kwargs) -> str:
    """Call Ollama server."""
    # 30 lines of HTTP logic


def _call_github(model: str, prompt: str, **kwargs) -> str:
    """Call GitHub Models API."""
    # 40 lines of API logic
```

**1 file, ~400 lines, zero imports between modules.**

---

## Simplified Public API

```python
import prompttools

# Evaluate a prompt (returns score + details)
result = prompttools.evaluate("prompts/my-prompt.md")
print(result.score)  # 82.5

# Evaluate with options
result = prompttools.evaluate(
    "prompts/my-prompt.md",
    model="local:phi4mini",  # or "gh:gpt-4o-mini", "ollama:llama3"
    method="geval",          # or "direct", "tiered"
)

# Validate structure only (no LLM call)
issues = prompttools.validate("prompts/my-prompt.md")
for issue in issues:
    print(f"  {issue.level}: {issue.message}")

# Direct LLM call
response = prompttools.generate(
    model="gh:gpt-4o-mini",
    prompt="Explain quantum computing",
)
```

---

## Simplified CLI

```bash
# Three commands, that's it
prompttools evaluate prompts/           # Evaluate prompts
prompttools validate prompts/           # Check structure
prompttools generate "your prompt"      # Direct LLM call

# Common options (same for all)
--model local:phi4mini    # Which model
--output results.json     # Output file
--verbose                 # Show details
```

---

## What About Advanced Features?

### Features to Keep (Built Into Core)

| Feature | Where It Lives |
|---------|----------------|
| Multi-provider support | `llm.py` - inline functions |
| Response caching | `cache.py` - single implementation |
| G-Eval, tiered eval | `evaluate.py` - as method options |
| JSON parsing | `parse.py` - one set of functions |
| Model probing | `llm.py` - `probe(model)` function |
| Rubric loading | `evaluate.py` - reads from `rubrics/` |

### Features to Remove or Defer

| Feature | Reason |
|---------|--------|
| Autonomous agents | Too complex, rarely used |
| Checkpoint/resume | Overkill for most use cases |
| LATS improvement loop | Users can script this themselves |
| CoVe verification | Niche, make it a separate tool |
| Multiple caching implementations | Keep one |
| Abstract base classes | Just use functions |
| Plugin architecture | YAGNI |

### Features Users Can Do Themselves

```python
# "Batch evaluation" - just a loop
for file in Path("prompts/").glob("*.md"):
    result = prompttools.evaluate(file)
    
# "Improvement loop" - just call evaluate + LLM
while result.score < 80:
    improved = prompttools.generate(model, f"Improve this: {prompt}")
    result = prompttools.evaluate(improved)
    
# "Multi-model comparison" - just a loop
for model in ["local:phi4mini", "gh:gpt-4o-mini"]:
    result = prompttools.evaluate(prompt, model=model)
```

---

## Implementation: All Key Files

### `__init__.py` (Public API)

```python
"""Prompt evaluation and validation tools."""

from .evaluate import evaluate, evaluate_batch
from .validate import validate, validate_batch  
from .llm import generate, list_models, probe

__all__ = [
    "evaluate", "evaluate_batch",
    "validate", "validate_batch",
    "generate", "list_models", "probe",
]

__version__ = "1.0.0"
```

### `evaluate.py` (Core Evaluation)

```python
"""Prompt evaluation - direct, G-Eval, and tiered methods."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
from .llm import generate
from .parse import extract_json, parse_frontmatter
from .cache import get_cached, set_cached

@dataclass
class EvalResult:
    file: str
    score: float
    grade: str
    criteria: dict
    model: str
    method: str
    
def evaluate(
    path: str | Path,
    model: str = "local:phi4mini",
    method: str = "geval",  # "direct", "geval", "structural"
) -> EvalResult:
    """Evaluate a single prompt file."""
    content = Path(path).read_text()
    
    if method == "structural":
        return _eval_structural(path, content)
    
    # Check cache
    cached = get_cached(content, model)
    if cached:
        return cached
    
    # Build evaluation prompt
    eval_prompt = _build_eval_prompt(content, method)
    
    # Call LLM
    response = generate(model, eval_prompt)
    
    # Parse response
    result = _parse_eval_response(response, path, model, method)
    
    # Cache and return
    set_cached(content, model, result)
    return result

def evaluate_batch(paths: List[Path], **kwargs) -> List[EvalResult]:
    """Evaluate multiple prompts."""
    return [evaluate(p, **kwargs) for p in paths]

# ... ~300 more lines for _eval_structural, _build_eval_prompt, etc.
```

### `validate.py` (Structure Validation)

```python
"""Prompt validation - structure, frontmatter, required sections."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from .parse import parse_frontmatter, extract_sections

@dataclass
class Issue:
    level: str  # "error", "warning", "info"
    message: str
    line: Optional[int] = None

def validate(path: str | Path) -> List[Issue]:
    """Validate a prompt file's structure."""
    issues = []
    content = Path(path).read_text()
    
    # Check frontmatter
    fm = parse_frontmatter(content)
    if not fm.get("title"):
        issues.append(Issue("error", "Missing required field: title"))
    if not fm.get("description"):
        issues.append(Issue("warning", "Missing description"))
    
    # Check sections
    sections = extract_sections(content)
    required = ["Description", "Prompt", "Variables", "Example"]
    for req in required:
        if req.lower() not in [s.lower() for s in sections]:
            issues.append(Issue("error", f"Missing section: {req}"))
    
    return issues

def validate_batch(paths: List[Path]) -> dict:
    """Validate multiple files, return summary."""
    results = {str(p): validate(p) for p in paths}
    return {
        "files": results,
        "total": len(results),
        "errors": sum(1 for r in results.values() if any(i.level == "error" for i in r)),
    }
```

### `llm.py` (Unified LLM Client)

```python
"""Unified LLM client - all providers in one file."""

import os
import json
import urllib.request
from typing import Optional
from pathlib import Path

def generate(
    model: str,
    prompt: str,
    system: str = "",
    temperature: float = 0.7,
    max_tokens: int = 4096,
) -> str:
    """Generate text from any supported model."""
    provider = model.split(":")[0] if ":" in model else "local"
    
    handlers = {
        "local": _call_local,
        "ollama": _call_ollama,
        "gh": _call_github,
        "azure-openai": _call_azure_openai,
        "openai": _call_openai,
        "gemini": _call_gemini,
        "claude": _call_claude,
        "windows-ai": _call_windows_ai,
    }
    
    handler = handlers.get(provider)
    if not handler:
        raise ValueError(f"Unknown provider: {provider}")
    
    return handler(model, prompt, system, temperature, max_tokens)

def list_models(provider: str = None) -> list:
    """List available models, optionally filtered by provider."""
    models = []
    
    # Local ONNX models
    if not provider or provider == "local":
        models.extend(_find_local_models())
    
    # Ollama models  
    if not provider or provider == "ollama":
        models.extend(_find_ollama_models())
    
    return models

def probe(model: str) -> bool:
    """Test if a model is available and working."""
    try:
        generate(model, "Say 'ok'", max_tokens=10)
        return True
    except Exception:
        return False

# Provider implementations (all inline, no separate files)

def _call_local(model, prompt, system, temp, max_tokens):
    """ONNX model via onnxruntime-genai."""
    import onnxruntime_genai as og
    # ... 40 lines
    
def _call_ollama(model, prompt, system, temp, max_tokens):
    """Ollama server."""
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    # ... 25 lines

def _call_github(model, prompt, system, temp, max_tokens):
    """GitHub Models API."""
    token = os.environ.get("GITHUB_TOKEN")
    # ... 35 lines

def _call_azure_openai(model, prompt, system, temp, max_tokens):
    """Azure OpenAI deployment."""
    # ... 40 lines

def _call_openai(model, prompt, system, temp, max_tokens):
    """OpenAI API."""
    # ... 30 lines

def _call_gemini(model, prompt, system, temp, max_tokens):
    """Google Gemini."""
    # ... 25 lines

def _call_claude(model, prompt, system, temp, max_tokens):
    """Anthropic Claude."""
    # ... 25 lines

def _call_windows_ai(model, prompt, system, temp, max_tokens):
    """Windows AI / Phi Silica."""
    # ... 30 lines

def _find_local_models():
    """Scan for ONNX models."""
    # ... 20 lines

def _find_ollama_models():
    """Query Ollama for models."""
    # ... 15 lines
```

### `cli.py` (Simple CLI)

```python
"""Command-line interface."""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(prog="prompttools")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # evaluate
    eval_p = subparsers.add_parser("evaluate", help="Evaluate prompts")
    eval_p.add_argument("path", type=Path)
    eval_p.add_argument("--model", default="local:phi4mini")
    eval_p.add_argument("--method", choices=["direct", "geval", "structural"], default="geval")
    eval_p.add_argument("--output", type=Path)
    
    # validate
    val_p = subparsers.add_parser("validate", help="Validate structure")
    val_p.add_argument("path", type=Path)
    
    # generate
    gen_p = subparsers.add_parser("generate", help="Generate text")
    gen_p.add_argument("prompt")
    gen_p.add_argument("--model", default="local:phi4mini")
    
    args = parser.parse_args()
    
    if args.command == "evaluate":
        from .evaluate import evaluate, evaluate_batch
        if args.path.is_dir():
            results = evaluate_batch(list(args.path.glob("**/*.md")), model=args.model)
        else:
            results = [evaluate(args.path, model=args.model)]
        _print_results(results)
        
    elif args.command == "validate":
        from .validate import validate, validate_batch
        # ...
        
    elif args.command == "generate":
        from .llm import generate
        print(generate(args.model, args.prompt))

if __name__ == "__main__":
    main()
```

---

## Summary: Before vs After

| Metric | Original Proposal | Simplified |
|--------|------------------|------------|
| Directories | 12 | 1 (just `rubrics/`) |
| Python files | 40+ | 8 |
| Lines of code | ~8,000 | ~2,000 |
| Public functions | 30+ | 7 |
| CLI commands | 15+ | 3 |
| Config files | 2 | 0 (inline defaults) |
| Abstract classes | 5+ | 0 |

---

## Migration from Current State

### Step 1: Create the new package (1 day)

```bash
mkdir prompttools
touch prompttools/{__init__,llm,evaluate,validate,cache,parse,cli}.py
```

### Step 2: Copy & consolidate providers (2 hours)

- Extract provider functions from `tools/llm_client.py`
- Inline into `llm.py` (no inheritance, just functions)

### Step 3: Merge validation logic (2 hours)

- Combine `validate_prompts.py` + `validators/` into `validate.py`

### Step 4: Simplify evaluation (3 hours)

- Extract core from `prompteval/__main__.py` (skip the 2000 lines of extras)
- Keep: direct eval, G-Eval, structural
- Drop: agents, checkpoints, retry logic

### Step 5: Wire up CLI (1 hour)

- Simple argparse, 3 commands

### Step 6: Test & document (2 hours)

- Smoke tests for each public function
- One-page README

**Total: ~1 day of focused work**

---

## The Golden Rule

> **If you can't explain what a module does in one sentence, it's too complex.**

- `llm.py` → "Calls any LLM provider"
- `evaluate.py` → "Scores a prompt using an LLM"  
- `validate.py` → "Checks prompt structure"
- `cache.py` → "Caches LLM responses"
- `parse.py` → "Extracts JSON and YAML"
- `cli.py` → "Runs commands from terminal"

Done.
