# Running Pattern Evaluation with Local Models

This guide shows how to evaluate advanced prompt patterns using local ONNX models on your machine.

## Quick Start

### 1. Prepare Test Data

Create a file with model output to evaluate:

```bash
# Example: Save a ReAct output to evaluate
cat > test_output.txt << 'EOF'
**Thought:** I need to find the capital of France.

**Action:** search_knowledge_base("capital of France")

**Observation:** France's capital is Paris, located on the Seine River.

**Final Answer:** The capital of France is Paris.
EOF
```

### 2. Run Evaluation

```bash
# Activate virtual environment (Windows)
.venv\Scripts\Activate.ps1

# Quick evaluation (1 run)
python testing/run_pattern_eval_local.py \
    prompts/advanced/react-tool-augmented.md \
    test_output.txt

# Full evaluation (20 runs for robust results)
python testing/run_pattern_eval_local.py \
    prompts/advanced/react-tool-augmented.md \
    test_output.txt \
    --runs 20 \
    --output-json results.json
```

## Available Local Models

The system supports these local ONNX models:

| Model | ID | Size | Best For |
|-------|-----|------|----------|
| **Phi-4 Mini** | `local:phi4mini` | 3.8B | Default, fast, accurate |
| **Phi-3.5** | `local:phi3.5` | 3.8B | Alternative to Phi-4 |
| **Phi-3** | `local:phi3` | 3.8B | Older, but proven |
| **Phi-3 Medium** | `local:phi3-medium` | 14B | More capable, slower |
| **Mistral 7B** | `local:mistral-7b` | 7B | Open source alternative |

### Choosing a Model

```bash
# Default (Phi-4 Mini - recommended)
python testing/run_pattern_eval_local.py prompt.md output.txt

# Use Phi-3.5
python testing/run_pattern_eval_local.py prompt.md output.txt --model local:phi3.5

# Use Mistral 7B (more verbose judge)
python testing/run_pattern_eval_local.py prompt.md output.txt --model local:mistral-7b

# Use Phi-3 Medium (slower but more thorough)
python testing/run_pattern_eval_local.py prompt.md output.txt --model local:phi3-medium
```

## Supported Patterns

The evaluation system supports these advanced patterns:

1. **ReAct** - Reasoning + Acting with tool calls
   - Phases: Thought → Action → Observation → Final Answer
   - Use case: Tool-augmented reasoning

2. **CoVe** - Chain-of-Verification
   - Phases: Draft Answer → Verification Questions → Independent Verification → Revised Answer
   - Use case: Reducing hallucinations

3. **Reflexion** - Self-improvement through critique
   - Phases: Attempt → Self-Critique → Reflection Memory → Improved Attempt
   - Use case: Iterative improvement

4. **RAG** - Retrieval-Augmented Generation
   - Phases: Query Analysis → Retrieval → Evidence Integration → Grounded Answer
   - Use case: Document-grounded responses

## Command-Line Options

```bash
python testing/run_pattern_eval_local.py [OPTIONS] PROMPT_FILE OUTPUT_FILE

Required Arguments:
  PROMPT_FILE         Path to prompt template (e.g., prompts/advanced/CoVe.md)
  OUTPUT_FILE         Path to file with model output to evaluate

Options:
  --model MODEL       Judge model to use (default: local:phi4mini)
  --pattern PATTERN   Force pattern type (auto-detect if omitted)
  --runs N            Number of evaluation runs (default: 1, use 20 for robust)
  --temperature T     Judge sampling temperature (default: 0.1)
  --output-json FILE  Save detailed results to JSON
  --verbose           Show detailed progress
```

## Example Workflows

### Evaluate CoVe Pattern

```bash
# 1. Create sample CoVe output
cat > cove_output.txt << 'EOF'
**Baseline Response:**
The Python GIL prevents true parallelism in multi-threaded programs.

**Verification Questions:**
1. Does the GIL affect all Python implementations?
2. Does it prevent ALL types of parallelism?

**Independent Verification:**
1. No, the GIL is specific to CPython. Jython and IronPython don't have it.
2. No, the GIL only affects CPU-bound tasks. I/O operations can run in parallel.

**Revised Answer:**
The CPython GIL prevents parallel execution of Python bytecode in multi-threaded
programs, but only for CPU-bound tasks. I/O-bound operations can still benefit
from multi-threading. Other Python implementations like Jython don't have a GIL.
EOF

# 2. Run evaluation
python testing/run_pattern_eval_local.py \
    prompts/advanced/CoVe.md \
    cove_output.txt \
    --runs 5 \
    --output-json cove_results.json
```

### Evaluate ReAct Pattern

```bash
# 1. Create sample ReAct output
cat > react_output.txt << 'EOF'
**Thought:** I need to debug why the API is returning 500 errors.

**Action:** search_logs(service="api-gateway", level="ERROR", time="last_hour")

**Observation:** Found 47 errors, 35 are "Database connection timeout".

**Thought:** The database connection pool might be saturated.

**Action:** query_metrics(service="database", metric="connection_pool")

**Observation:** Connection pool is at 100/100 capacity with 20 requests waiting.

**Final Answer:**
Root cause: Database connection pool exhaustion.
Fix: Increase pool size from 100 to 200 and add indexes to slow queries.
EOF

# 2. Run evaluation
python testing/run_pattern_eval_local.py \
    prompts/advanced/react-tool-augmented.md \
    react_output.txt \
    --runs 10
```

### Batch Evaluation

```bash
# Evaluate multiple outputs
for output in outputs/*.txt; do
    echo "Evaluating $output..."
    python testing/run_pattern_eval_local.py \
        prompts/advanced/react-tool-augmented.md \
        "$output" \
        --runs 5 \
        --output-json "results/$(basename $output .txt).json"
done
```

## Interpreting Results

### Scoring Dimensions

Each pattern is scored on 6 universal dimensions (0-5 scale):

- **PIF** (Pattern Invocation Fidelity): Did the model attempt the pattern?
- **POI** (Phase Ordering Integrity): Correct phase sequence?
- **PC** (Phase Completeness): All required phases present?
- **CA** (Constraint Adherence): Pattern-specific rules followed?
- **SRC** (Self-Referential Consistency): Internal consistency?
- **IR** (Intermediate Reasoning): Quality of reasoning steps?

### Hard Gates

Your output must pass these thresholds:

- **PC ≥ 4**: All required phases must be present
- **POI ≥ 4**: Phases must be in correct order
- **CA ≥ 4**: Pattern constraints must be followed
- **PR ≥ 0.75**: Must pass in at least 75% of runs

If any hard gate fails, the overall evaluation fails.

### Sample Output

```
============================================================
 RESULTS
============================================================

Pattern: react
Overall Score: 4.65/5.0 (93.0/100)
Pass Rate: 100.0%
Hard Gates: PASS ✓

📊 Dimension Scores (median across 10 runs):
  CA  : 4.50/5.0 (σ=0.22)
  PC  : 5.00/5.0 (σ=0.00)
  PIF : 4.80/5.0 (σ=0.14)
  POI : 5.00/5.0 (σ=0.00)

📈 Statistical Metrics:
  Mean Phase Fidelity: 96.0%
  Critical Failure Rate: 0.0%
  Perfect Pass Rate: 100.0%
```

## Programmatic Usage

You can also use the evaluation API directly in Python:

```python
from tools.llm.llm_client import LLMClient
from tools.prompteval.pattern_evaluator import PatternEvaluator

# Create wrapper for LLMClient
class LLMClientWrapper:
    def __init__(self, model_name="local:phi4mini"):
        self.model_name = model_name

    def complete(self, prompt: str, temperature: float = 0.1) -> str:
        return LLMClient.generate_text(
            model_name=self.model_name,
            prompt=prompt,
            temperature=temperature,
        )

# Run evaluation
client = LLMClientWrapper("local:phi4mini")
evaluator = PatternEvaluator(client, num_runs=20)

score = evaluator.evaluate(
    prompt_content="...",  # Your prompt
    model_output="...",     # Model output to evaluate
    pattern_name="react",   # Pattern type
)

print(f"Score: {score.overall_score:.2f}/5.0")
print(f"Passes: {score.passes_hard_gates}")
```

## Troubleshooting

### Model Not Found

If you get "Model not found" errors, the model may not be cached locally:

1. Open **AI Toolkit** in VS Code
2. Go to **Models** section
3. Download the model (e.g., "Phi-4 mini instruct")
4. Wait for download to complete
5. Try evaluation again

### Slow Evaluation

If evaluation is too slow:

1. Use fewer runs: `--runs 3` instead of `--runs 20`
2. Use a smaller model: `--model local:phi4mini` (default)
3. Use quick evaluation mode (1 run) for development

### Memory Issues

If you run out of memory:

1. Close other applications
2. Use CPU models instead of GPU: `--model local:phi4-cpu`
3. Reduce context size in prompts
4. Use a smaller model (phi3 instead of phi3-medium)

## Performance Tips

### Speed Optimization

- **Development**: Use `--runs 1` for quick feedback
- **Testing**: Use `--runs 5` for reasonable confidence
- **Production**: Use `--runs 20` for robust evaluation

### Accuracy Optimization

- Use `--temperature 0.1` (default) for consistency
- Use median aggregation (automatic with multiple runs)
- Compare multiple judge models for critical evaluations

### Resource Management

- Local models run on CPU by default (no GPU required)
- Phi-4 Mini uses ~2GB RAM
- Phi-3 Medium uses ~7GB RAM
- Enable caching to avoid re-evaluating identical outputs

## Next Steps

1. **Test with your prompts**: Evaluate outputs from your library prompts
2. **Tune patterns**: Adjust pattern definitions in `tools/rubrics/patterns/`
3. **Custom dimensions**: Add pattern-specific scoring in `tools/rubrics/pattern-scoring.yaml`
4. **Mutation testing**: Use `tools/prompteval/mutations.py` for robustness tests

## See Also

- [Pattern Evaluation Framework](../tools/prompteval/README.md)
- [Pattern Definitions](../tools/rubrics/patterns/)
- [Scoring Schema](../tools/rubrics/pattern-scoring.yaml)
- [LLM Client Documentation](../tools/llm/README.md)
