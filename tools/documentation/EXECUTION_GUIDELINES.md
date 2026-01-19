---
title: Tool Execution Guidelines
shortTitle: Execution Guidelines
intro: Mandatory patterns for executing tools and scripts in this repository.
type: reference
difficulty: intermediate
audience:

- senior-engineer
- junior-engineer
- ai-agent

platforms:

- github-copilot
- claude
- chatgpt

author: Prompts Library Team
version: '1.0'
date: '2026-01-06'
governance_tags:

- PII-safe

dataClassification: internal
reviewStatus: approved
---

# Tool Execution Guidelines

These guidelines MUST be followed when running any tool or script in this repository.

---

## 🚀 AUTOMATIC ENFORCEMENT (Recommended)

Instead of manually implementing all these patterns, **import `tool_init.py`** to get automatic enforcement:

```python
#!/usr/bin/env python3
"""
Example script with automatic execution guideline enforcement.
"""
from tools.tool_init import init_tool

# Initialize with prerequisites - FAILS FAST if not met
init = init_tool(
    name="my_script",
    required_models=["local:phi4"],       # Checks model availability
    required_env=["GITHUB_TOKEN"],         # Checks environment variables
    verbose=True,
)

# Your items to process
items = ["item1", "item2", "item3"]
init.set_total(len(items))

# Process with automatic logging
for item in items:
    with init.log_item(item) as log:
        try:
            result = process(item)  # Your processing logic
            log.success(score=result.score)  # Log success with data
        except Exception as e:
            log.error(str(e))  # Log error (auto-classifies)

# Print summary and exit with appropriate code
init.summary()
sys.exit(init.exit_code())
```

**What `tool_init.py` automatically provides:**

| Feature | Automatic Behavior |
| --------- | ------------------- |
| **Unicode Fix** | Applied on import (Windows console encoding) |
| **Model Check** | Exits with code 1 if required models unavailable |
| **Env Check** | Exits with code 1 if required env vars missing |
| **Path Check** | Exits with code 1 if required paths don't exist |
| **Logging** | JSONL log written immediately after each item |
| **Progress** | Shows `[1/10] (10.0%) item_name...` format |
| **Error Classification** | Auto-classifies errors as transient/permanent |
| **Summary** | Prints success/fail counts and exit code |
| **Retry Decorator** | `@with_retry()` for transient error handling |

---

## Manual Implementation (if not using tool_init.py)

If you can't use `tool_init.py`, implement these patterns manually:

---

## 1. Model Availability Check (MANDATORY)

**Before** any LLM operation, **always** verify model availability:

```python
from tools.model_probe import is_model_usable, ModelProbe

# Quick check for single model
if not is_model_usable("gh:gpt-4o-mini"):
    print("ERROR: Model not available", file=sys.stderr)
    sys.exit(1)

# Full check for batch operations
probe = ModelProbe(verbose=True)
models = ["local:phi4", "gh:gpt-4o-mini", "ollama:deepseek-r1:14b"]
runnable = probe.filter_runnable(models)

if not runnable:
    print("FATAL: No models available!", file=sys.stderr)
    sys.exit(1)
```

**Discovery command before batch runs:**

```powershell
python tools/model_probe.py --discover --force -o discovery_results.json
```

---

## 2. Fail-Fast Pattern (MANDATORY)

All scripts MUST fail immediately on:

- Missing required models
- Missing configuration/environment variables
- Invalid input files
- Permission errors

```python
import sys
from pathlib import Path

def main():
    # === FAIL-FAST CHECKS ===

    # Check required environment
    required_env = ["GITHUB_TOKEN"]
    for var in required_env:
        if not os.getenv(var):
            print(f"FATAL: Missing required env var: {var}", file=sys.stderr)
            sys.exit(1)

    # Check required files
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not input_path or not input_path.exists():
        print(f"FATAL: Input path does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Check model availability
    from tools.model_probe import is_model_usable
    if not is_model_usable("local:phi4"):
        print("FATAL: Required model 'local:phi4' not available", file=sys.stderr)
        sys.exit(1)

    print("✓ All prerequisites satisfied")
    # === PROCEED WITH MAIN LOGIC ===
```

---

## 3. Iterative Logging (MANDATORY)

All batch operations MUST log progress **immediately** (not just at end):

```python
import json
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("eval_log.jsonl")

def log_result(prompt_file: str, model: str, result: dict):
    """Append result immediately to log file (JSONL format)."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": str(prompt_file),
        "model": model,
        "score": result.get("score"),
        "duration_ms": result.get("duration_ms"),
        "error": result.get("error"),
        "error_code": result.get("error_code"),
    }
    # Append immediately - don't buffer
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        f.flush()  # Force write to disk

# Usage in loop
for i, prompt_file in enumerate(prompt_files, 1):
    print(f"[{i}/{len(prompt_files)}] Processing {prompt_file.name}...")

    try:
        result = evaluate(prompt_file)
        log_result(prompt_file, model, {"score": result.score})
        print(f"  ✓ Score: {result.score}")
    except Exception as e:
        log_result(prompt_file, model, {"error": str(e), "error_code": "internal_error"})
        print(f"  ✗ Error: {e}")
```

---

## 4. Unicode/Encoding Safety (MANDATORY)

All tools MUST handle Unicode safely. Include this at the top of scripts:

```python
import sys
import io
import os

# === CONSOLE ENCODING FIX (Windows) ===
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, IOError):
        pass  # Already wrapped or not available

# Safe string handling
def safe_str(text: str) -> str:
    """Ensure string is safe for console output."""
    if not isinstance(text, str):
        text = str(text)
    return text.encode('utf-8', errors='replace').decode('utf-8')

def safe_print(text: str):
    """Print text safely, handling Unicode errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(safe_str(text))
```

---

## 5. Error Classification

Use standardized error codes from `model_probe.py`:

| Code | Meaning | Retry? |
| ------ | --------- | -------- |
| `success` | Operation completed | N/A |
| `unavailable_model` | Model not found | NO |
| `permission_denied` | Auth/access error | NO |
| `rate_limited` | Too many requests | YES (wait) |
| `timeout` | Operation timed out | YES |
| `parse_error` | JSON/output parse failed | YES |
| `network_error` | Connection failed | YES |
| `internal_error` | Unknown error | NO |

```python
from tools.model_probe import classify_error, TRANSIENT_ERRORS

try:
    result = call_model(prompt)
except Exception as e:
    error_code, should_retry = classify_error(str(e))

    if should_retry:
        print(f"Transient error ({error_code}), will retry...")
        time.sleep(10)
        # Retry logic
    else:
        print(f"Permanent error ({error_code}), skipping")
        log_result(prompt, model, {"error": str(e), "error_code": error_code.value})
```

---

## 6. Progress Reporting

For batch operations, show clear progress:

```python
total = len(items)
success = 0
failed = 0

for i, item in enumerate(items, 1):
    # Progress indicator
    pct = (i / total) * 100
    print(f"\r[{i:4d}/{total}] ({pct:5.1f}%) Processing... ", end="", flush=True)

    try:
        process(item)
        success += 1
    except Exception as e:
        failed += 1
        print(f"\n  ✗ {item}: {e}")

print(f"\n\nCompleted: {success} success, {failed} failed ({total} total)")
```

---

## 7. Checkpoint/Resume Pattern

For long-running operations, support resume:

```python
CHECKPOINT_FILE = Path("checkpoint.json")

def save_checkpoint(state: dict):
    """Save state for resume capability."""
    CHECKPOINT_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

def load_checkpoint() -> dict:
    """Load previous state if exists."""
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8"))
    return {}

def main():
    state = load_checkpoint()
    completed = set(state.get("completed", []))

    for item in all_items:
        if item in completed:
            print(f"Skipping {item} (already done)")
            continue

        process(item)
        completed.add(item)
        save_checkpoint({"completed": list(completed)})
```

---

## Summary Checklist

Before running any tool:

- [ ] Run `python tools/model_probe.py --discover` to check model availability
- [ ] Verify required environment variables are set
- [ ] Ensure input files/folders exist
- [ ] Set `PYTHONIOENCODING=utf-8` if seeing Unicode errors
- [ ] Check Ollama is running if using `ollama:*` models
- [ ] Verify GitHub auth with `gh auth status` if using `gh:*` models

During execution:

- [ ] Log results immediately (don't buffer)
- [ ] Handle errors gracefully with proper error codes
- [ ] Show progress for batch operations
- [ ] Support Ctrl+C for graceful interruption
