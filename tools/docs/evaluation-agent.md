# Evaluation Agent (`evaluation_agent.py`)

> **Autonomous evaluation agent** - Runs complete evaluation pipelines with checkpoint/resume capability.

---

## ⚡ Quick Start

```powershell
# Run full evaluation pipeline
python tools/evaluation_agent.py --category advanced --runs 3

# Resume from checkpoint
python tools/evaluation_agent.py --resume

# Dry run (preview what would happen)
python tools/evaluation_agent.py --category basic --dry-run
```

---

## Features

- **Autonomous Execution** - Runs complete evaluation pipelines without intervention
- **Checkpoint/Resume** - Save progress and resume interrupted runs
- **Multi-Model** - Evaluate across multiple models
- **Progress Tracking** - Real-time progress and ETA
- **Error Recovery** - Automatic retry with exponential backoff

---

## CLI Usage

```powershell
# Full evaluation on specific category
python tools/evaluation_agent.py --category advanced --runs 3

# All prompts
python tools/evaluation_agent.py --all --runs 1

# Multiple categories
python tools/evaluation_agent.py --categories basic,advanced,developers

# Specify models
python tools/evaluation_agent.py --category advanced --models phi4,gpt-4o-mini

# Resume interrupted run
python tools/evaluation_agent.py --resume

# Dry run (show plan without executing)
python tools/evaluation_agent.py --category advanced --dry-run

# Verbose output
python tools/evaluation_agent.py --category basic -v
```

---

## Python API

```python
from tools.evaluation_agent import EvaluationAgent

# Initialize agent
agent = EvaluationAgent(
    models=["local:phi4", "gh:gpt-4o-mini"],
    verbose=True
)

# Run evaluation
results = agent.evaluate_category("advanced", runs=3)

# Check results
print(f"Total prompts: {results.total}")
print(f"Passed: {results.passed}")
print(f"Failed: {results.failed}")
print(f"Average score: {results.avg_score}")

# Resume from checkpoint
agent.resume()
```

---

## Checkpoint System

The agent saves progress to allow resuming interrupted runs:

```
~/.cache/prompts-eval/checkpoints/
├── eval_20260106_143022.json
├── eval_20260106_150145.json
└── latest.json -> eval_20260106_150145.json
```

### Resume Options

```powershell
# Resume latest checkpoint
python tools/evaluation_agent.py --resume

# Resume specific checkpoint
python tools/evaluation_agent.py --resume-from eval_20260106_143022.json

# List checkpoints
python tools/evaluation_agent.py --list-checkpoints
```

---

## Output Format

The agent generates comprehensive reports:

```
Evaluation Report - 2026-01-06
================================

Category: advanced
Models: phi4, gpt-4o-mini
Runs: 3

Results Summary:
  Total Prompts: 25
  Passed (≥70): 22 (88%)
  Failed (<70): 3 (12%)
  Average Score: 78.4

By Model:
  phi4: 76.2 avg
  gpt-4o-mini: 80.6 avg

Top Performers:

  1. react-pattern.md: 95.0
  2. chain-of-thought.md: 92.0
  3. few-shot-learning.md: 89.0

Needs Improvement:

  1. legacy-format.md: 58.0
  2. incomplete-example.md: 62.0
  3. unclear-instructions.md: 65.0

```

---

## Configuration

The agent uses default configuration from `config.py`:

| Setting | Default | Description |
| --------- | --------- | ------------- |
| `default_models` | `["local:phi4"]` | Models to use |
| `pass_threshold` | `70` | Minimum passing score |
| `max_retries` | `3` | Retry count on error |
| `timeout` | `120` | Seconds per evaluation |

Override via CLI:

```powershell
python tools/evaluation_agent.py --category advanced --threshold 80 --timeout 180
```

---

## Workflow Integration

```yaml
# GitHub Actions
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:

      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: python tools/evaluation_agent.py --category all --runs 1 --ci

```

---

## See Also

- [../prompteval/README.md](../prompteval/README.md) - PromptEval CLI
- [../enterprise-evaluator/README.md](../enterprise-evaluator/README.md) - Enterprise evaluation
- [model-probe.md](./model-probe.md) - Model availability checking
