# Evaluation Datasets

This directory stores evaluation datasets for workflow benchmarking.

## Structure

- `humaneval/` - OpenAI HumanEval dataset
- `mbpp/` - Mostly Basic Python Problems
- `swe_bench/` - SWE-bench GitHub issues
- `fullstack/` - Custom full-stack examples
- `refactoring/` - Legacy code refactoring examples
- `architecture/` - Architecture case studies

## Usage

Datasets are loaded automatically by the `WorkflowEvaluator`:

```python
from multiagent_workflows.core.evaluator import WorkflowEvaluator

evaluator = WorkflowEvaluator()
# Datasets are loaded from config/evaluation.yaml paths
```

## Adding Custom Datasets

1. Create a directory for your dataset
2. Add a `dataset.json` manifest file
3. Include sample inputs and golden outputs
4. Update `config/evaluation.yaml` to reference the new dataset
