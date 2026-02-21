# Agentic V2 Evaluation Framework

A comprehensive evaluation framework for AI agent workflows, providing scoring, metrics, runners, and report generation.

## Features

- **Metrics**: Accuracy, quality, and performance evaluation
- **Runners**: Batch and streaming evaluation execution
- **Reporters**: JSON, Markdown, and HTML report generation
- **Rubrics**: Configurable scoring rubrics in YAML format
- **CLI**: Command-line interface for evaluations

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Python API

```python
from agentic_v2_eval import Scorer
from agentic_v2_eval.metrics import calculate_accuracy, code_quality_score
from agentic_v2_eval.runners import BatchRunner
from agentic_v2_eval.reporters import generate_html_report

# Calculate accuracy
accuracy = calculate_accuracy(
    predictions=["A", "B", "A"],
    ground_truth=["A", "B", "B"]
)
print(f"Accuracy: {accuracy:.2%}")

# Score with a rubric
scorer = Scorer("rubrics/default.yaml")  # or pass an in-memory rubric dict
result = scorer.score({"Accuracy": 0.85, "Completeness": 0.9})
print(f"Weighted Score: {result.weighted_score:.2f}")

# Run batch evaluation
runner = BatchRunner(evaluator=my_eval_function)
batch_result = runner.run(test_cases)
print(f"Success rate: {batch_result.success_rate:.1%}")

# Generate report
generate_html_report(results, "report.html")
```

### Command Line

```bash
# Show help
python -m agentic_v2_eval --help

# Evaluate results with a rubric
python -m agentic_v2_eval evaluate results.json

# Optionally override the default rubric
python -m agentic_v2_eval evaluate results.json --rubric rubrics/default.yaml

# Generate HTML report
python -m agentic_v2_eval report results.json --format html --output report.html
```

## Modules

### metrics

- `accuracy.py`: Accuracy, F1, precision, recall calculations
- `quality.py`: Code quality, lint, and complexity scores
- `performance.py`: Execution time, latency, and benchmarking

### runners

- `batch.py`: Synchronous batch evaluation with progress tracking
- `streaming.py`: Streaming evaluation with real-time callbacks

### reporters

- `json.py`: JSON format reports with summary statistics
- `markdown.py`: Markdown reports with tables
- `html.py`: Styled HTML reports with color-coded scores

### rubrics

YAML files defining scoring criteria with weights and descriptions.

## Running Tests

```bash
pytest tests/ -v
pytest --cov=agentic_v2_eval --cov-report=term-missing --cov-report=xml
./scripts/run_coverage.sh
```

## License

MIT
