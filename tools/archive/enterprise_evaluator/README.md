# Enterprise Prompt Evaluator

A standalone tool for evaluating GenAI prompts against the Enterprise Prompt Evaluation Framework (v2.0).

## Features

- **Holistic Scoring**: Evaluates prompts across 6 dimensions:
  1. Technical Quality
  2. Business Alignment
  3. Security & Compliance
  4. Performance & Reliability
  5. Maintainability
  6. Innovation & Optimization
- **Weighted Scoring**: Calculates a final 0-100 score based on enterprise weights.
- **Dual-Mode Evaluation**: Combines deterministic checks (reproducibility tests, static analysis) with LLM-as-a-Judge qualitative assessment.
- **Local & Private**: Powered by local ONNX models (e.g., Phi-4) by default, ensuring no data leaves your environment.

## Directory Structure

```
enterprise-evaluator/
├── main.py          # CLI Entry point
├── evaluator.py     # Orchestrator logic
├── core/            # Self-contained LLM infrastructure
│   ├── llm_client.py
│   └── local_model.py
└── framework/       # Evaluation logic
    ├── dimensions.py
    ├── rubrics.py
    └── scoring.py
```

## Installation

1. Ensure you have Python 3.10+ installed.
2. Install dependencies:

   ```bash
   pip install onnxruntime-genai
   ```

   *(Note: For GPU support, install `onnxruntime-genai-cuda` or `onnxruntime-genai-directml`)*

## Usage

### Evaluate a single file

```bash
python main.py path/to/prompt.md
```

### Evaluate a directory

```bash
python main.py path/to/prompts_dir/
```

### Output to JSON

```bash
python main.py path/to/prompt.md --output results.json
```

### Select Model

By default, the tool uses `local:phi4mini`. You can specify others if configured in `core/llm_client.py`:

```bash
python main.py path/to/prompt.md --model gh:gpt-4o
```
