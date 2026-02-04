# Evaluations POC

This folder demonstrates the proposed structure for the `prompts` repo modularization, moving evaluation logic into a first-class package.

## Structure

```
prompts/evaluations/
├── __init__.py       # Package marker
├── __main__.py       # Entry point (python -m prompts.evaluations)
├── runner.py         # Minimal eval runner (POC)
└── examples/         # Example evaluation definitions
    └── sentiment_eval.yaml
```

## Usage

Run an evaluation using the runner:

```bash
# Run specific eval YAML
python -m prompts.evaluations.runner prompts/evaluations/examples/sentiment_eval.yaml

# Run with limit (smoke test)
python -m prompts.evaluations.runner prompts/evaluations/examples/sentiment_eval.yaml --limit 5
```

## Migration Plan

1. **Phase 1 (POC)**: Establish this folder and runner.
2. **Phase 2**: Migrate `tools/prompteval` logic here or adapt this runner to use it.
3. **Phase 3**: Move all eval implementations from `tools/` to `prompts/evaluations/` or `prompts/metrics/`.
