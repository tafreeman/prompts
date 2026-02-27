# AI/ML Best Practices

*Reproducible, responsible, production-ready*

## Reproducibility

- **Pin seeds everywhere:** random, numpy, torch, tensorflow, PYTHONHASHSEED
- Use deterministic algorithms (`torch.use_deterministic_algorithms`)
- Log full environment: Python version, packages, GPU, CUDA version
- Every experiment reproducible from commit hash + config

## Versioning

- **DVC or MLflow** for data/model versioning
- Track experiments with W&B, MLflow, or Neptune
- Configs alongside code (Hydra)
- Never rely on "latest" — pin everything

## Code Separation

Clean interfaces between concerns:
- `Trainer.train()` — training logic only
- `Evaluator.evaluate()` — evaluation logic only
- `Predictor.predict()` — inference logic only
- Each independently testable. Makes model swaps trivial.

## Data Quality

- **pandera** or **great_expectations** for data schema validation
- Validate: column types, value ranges, nulls, distribution drift
- Run checks on raw input AND after preprocessing
- Fail pipeline on check failure — don't train on bad data

## Notebooks

- Notebooks for exploration only, NEVER production logic
- Extract reusable code into .py modules immediately
- Use **nbstripout** to strip outputs from committed notebooks

## Deployment

- Docker for reproducible environments
- Pin ALL deps with pip-compile or Poetry lock
- Pin CUDA/cuDNN in Dockerfile
- No 'latest' tags anywhere
- Test inference in container before deploy

## Model Documentation

- Every deployed model needs a **model card**: intended use, limitations, training data summary, eval metrics, bias analysis, failure modes
- Consider fairness metrics for user-facing models
