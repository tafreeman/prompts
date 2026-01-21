# PromptEval runner scripts

These are small PowerShell helpers for running this repo’s canonical evaluator:

- `python -m tools.prompteval <path> --tier N --model <model> -o <file>`

## Scripts

- `run-one.ps1` — run a single (path, tier, model) and write a JSON report.
- `run-matrix.ps1` — run multiple tiers/models and write one JSON report per combination.

## Typical usage

- Run Tier 2 and Tier 3 on `prompts/analysis/` for the default model list:
  - `./scripts/prompteval/run-matrix.ps1 -Path prompts/analysis -VerboseEval -CI`

- Run a single model:
  - `./scripts/prompteval/run-one.ps1 -Path prompts/analysis -Tier 2 -Model local:phi4-gpu -VerboseEval -CI`

## Notes

- If you include `gh:*` models, you may hit rate limits; failures will show up in the JSON report’s `error` field and the script will exit non-zero when any runs fail.
- Output files are written under `results/` by default.
