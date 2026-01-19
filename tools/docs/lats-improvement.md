# LATS Improvement (`run_lats_improvement.py`)

> **Language Agent Tree Search (LATS) Self-Refine** - Automated iterative prompt improvement using the LATS evaluator pattern.

---

## ⚡ Quick Start

```powershell
# Improve a single prompt
python tools/run_lats_improvement.py prompts/example.md

# Improve all prompts in a folder
python tools/run_lats_improvement.py prompts/advanced/

# Use lite version for local models
python tools/run_lats_improvement.py prompts/ --lite

# Visible mode with PowerShell wrapper
.\tools\run_lats_visible.ps1 prompts/advanced/
```

---

## What is LATS
LATS (Language Agent Tree Search) Self-Refine is a multi-branch evaluation pattern:

1. **Branch A** - Criteria validation (structure, clarity, completeness)
2. **Branch B** - Scoring with evidence (quantitative assessment)
3. **Branch C** - Improvement suggestions (actionable recommendations)
4. **Synthesis** - Final score computation and threshold check

The process iterates until the threshold is met or max iterations reached.

---

## CLI Usage

```powershell
# Single prompt
python tools/run_lats_improvement.py prompts/example.md

# Folder (recursive)
python tools/run_lats_improvement.py prompts/advanced/

# All prompts
python tools/run_lats_improvement.py prompts/ --all

# Custom threshold (default: 80)
python tools/run_lats_improvement.py prompts/ --threshold 85

# Max iterations (default: 5)
python tools/run_lats_improvement.py prompts/ --max-iterations 3

# Use LATS-Lite for local models (smaller, ~1.5KB vs ~5.5KB)
python tools/run_lats_improvement.py prompts/ --lite

# Specific model
python tools/run_lats_improvement.py prompts/ --model ollama:phi4-reasoning
python tools/run_lats_improvement.py prompts/ --model gh:gpt-4.1

# Output results to file
python tools/run_lats_improvement.py prompts/ -o results.json

# Verbose output
python tools/run_lats_improvement.py prompts/ -v

# Dry run (show what would be processed)
python tools/run_lats_improvement.py prompts/ --dry-run
```

---

## Recommended Models

| Model | Type | Quality | Speed | Cost |
| ------- | ------ | --------- | ------- | ------ |
| `ollama:phi4-reasoning` | Local | Excellent | Medium | FREE |
| `ollama:deepseek-r1:14b` | Local | Excellent | Slow | FREE |
| `ollama:qwen2.5-coder:14b` | Local | Good (code) | Medium | FREE |
| `gh:gpt-4.1` | Cloud | Best | Fast | FREE tier |
| `gh:gpt-4o-mini` | Cloud | Good | Fast | FREE tier |
| `gh:deepseek/deepseek-r1` | Cloud | Excellent | Medium | FREE tier |

The script auto-selects the best available model, preferring local Ollama models.

---

## Output Format

```
LATS Evaluation: prompts/advanced/react-pattern.md
================================================
Model: ollama:phi4-reasoning
Threshold: 80.0

Iteration 1/5:
  Score: 72.0
  Feedback: Missing examples, unclear edge cases

Iteration 2/5:
  Score: 78.0
  Feedback: Examples added, consider more context

Iteration 3/5:
  Score: 84.0 ✓
  Threshold met!

Result:
  Initial Score: 72.0
  Final Score: 84.0
  Improvement: +12.0
  Iterations: 3
  Duration: 45.2s
  Key Changes:

    - Added 3 practical examples
    - Clarified edge case handling
    - Improved variable naming section

```

---

## LATS vs LATS-Lite

| Version | Size | Best For | Command |
| --------- | ------ | ---------- | --------- |
| **LATS Full** | ~5.5KB | Cloud models (GPT-4, etc.) | Default |
| **LATS-Lite** | ~1.5KB | Local models (Phi4, Ollama) | `--lite` |

```powershell
# Full version (cloud)
python tools/run_lats_improvement.py prompts/ --model gh:gpt-4.1

# Lite version (local)
python tools/run_lats_improvement.py prompts/ --lite --model ollama:phi4-reasoning
```

---

## Coverage Report

After processing, a coverage report is generated:

```json
{
  "total_prompts": 25,
  "evaluated": 25,
  "passed": 22,
  "failed": 3,
  "skipped": 0,
  "avg_improvement": 8.4,
  "duration_seconds": 1234.5,
  "folders": {
    "advanced": {"total": 15, "passed": 14, "failed": 1},
    "basic": {"total": 10, "passed": 8, "failed": 2}
  }
}
```

---

## PowerShell Wrapper

For visible execution with progress:

```powershell
# Run with visible output
.\tools\run_lats_visible.ps1 prompts/advanced/

# With custom options
.\tools\run_lats_visible.ps1 prompts/ -Threshold 85 -Model "ollama:phi4-reasoning"
```

---

## Python API

```python
from tools.run_lats_improvement import (
    evaluate_prompt_with_lats,
    load_lats_evaluator,
    get_best_available_model,
    LATS_Result
)

# Load evaluator template
template = load_lats_evaluator(use_lite=True)

# Get best available model
model = get_best_available_model()  # Auto-selects

# Evaluate a prompt
result: LATS_Result = evaluate_prompt_with_lats(
    prompt_path=Path("prompts/example.md"),
    evaluator_template=template,
    model=model,
    threshold=80.0,
    max_iterations=5,
    verbose=True
)

print(f"Initial: {result.initial_score}")
print(f"Final: {result.final_score}")
print(f"Improvement: {result.improvement:+.1f}")
print(f"Iterations: {result.iterations}")
print(f"Changes: {result.key_changes}")
```

---

## Integration with Evaluation Workflow

```powershell
# Step 1: Check current scores
python -m prompteval prompts/advanced/ -o before.json

# Step 2: Run LATS improvement
python tools/run_lats_improvement.py prompts/advanced/ --threshold 80

# Step 3: Verify improvements
python -m prompteval prompts/advanced/ -o after.json

# Step 4: Compare results
# (Manual review or diff the JSON files)
```

---

## See Also

- [evaluation-agent.md](./evaluation-agent.md) - Autonomous evaluation
- [../prompteval/README.md](../prompteval/README.md) - PromptEval CLI
- [analyzers.md](./analyzers.md) - Analysis tools
