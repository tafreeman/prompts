"""Run matrix evaluations for a prompt, producing unique output files per run.

Usage:
  python scripts/run_matrix_evals.py --prompt-path prompts/advanced/lats-self-refine-evaluator-agentic-workflow.md \
    --manifest run-manifest.yaml --iteration-plan iteration-plan.yaml

This script:
- Loads run-manifest.yaml and iteration-plan.yaml
- For each model_tier and seed, runs: python -m tools.prompteval <prompt-path> -o <unique-results-file>
- Saves a summary JSON in results/<run_id>/summary_<timestamp>.json listing produced files and statuses
- Snapshots the manifest and iteration-plan into results/<run_id>/

Note: requires `tools.prompteval` to be invokable via `python -m tools.prompteval`.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import subprocess
from datetime import datetime
from pathlib import Path

import yaml


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_prompteval(
    prompt_path: Path, out_file: Path, extra_args=None, env_vars: dict | None = None
):
    cmd = [
        "python",
        "-m",
        "tools.prompteval",
        str(prompt_path),
        "-o",
        str(out_file),
        "--ci",
    ]
    if extra_args:
        cmd += extra_args
    env = os.environ.copy()
    if env_vars:
        env.update({k: str(v) for k, v in env_vars.items()})
    # Use subprocess and capture output
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return proc.returncode, proc.stdout, proc.stderr


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt-path", required=True)
    p.add_argument("--manifest", required=True)
    p.add_argument("--iteration-plan", required=True)
    p.add_argument("--output-dir", default="results")
    args = p.parse_args()

    prompt_path = Path(args.prompt_path)
    manifest_path = Path(args.manifest)
    iteration_plan_path = Path(args.iteration_plan)
    out_root = Path(args.output_dir)
    out_root.mkdir(parents=True, exist_ok=True)

    manifest = load_yaml(manifest_path)
    iteration_plan = load_yaml(iteration_plan_path)

    run_id = (
        manifest.get("run_id") or f"run_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    )
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    run_dir = out_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # snapshot manifest and plan
    (run_dir / f"manifest_snapshot_{timestamp}.yaml").write_text(
        manifest_path.read_text(encoding="utf-8"), encoding="utf-8"
    )
    (run_dir / f"iteration_plan_snapshot_{timestamp}.yaml").write_text(
        iteration_plan_path.read_text(encoding="utf-8"), encoding="utf-8"
    )

    seeds = (
        iteration_plan.get("iteration_plan", {}).get("seeds")
        or iteration_plan.get("seeds")
        or manifest.get("seeds")
        or [None]
    )
    model_tiers = (
        iteration_plan.get("iteration_plan", {}).get("model_tiers")
        or iteration_plan.get("model_tiers")
        or [manifest.get("model_version")]
    )

    # Recording reproducibility params
    system_prompt = manifest.get("system_prompt")
    model_version = manifest.get("model_version")
    temperature = manifest.get("temperature", 0.0)
    decoding = manifest.get("decoding_method", "greedy")

    summary = {
        "run_id": run_id,
        "timestamp": timestamp,
        "prompt": str(prompt_path),
        "entries": [],
    }

    # Allow override via CLI args in manifest, but defaults can be provided to the script
    cli_temp = manifest.get("temperature", 0.0)
    cli_decoding = manifest.get("decoding_method", "greedy")

    for model in model_tiers:
        model_sanitized = (model or "unknown").replace(":", "@").replace("/", "_")
        for seed in seeds:
            seed_tag = str(seed) if seed is not None else "noseed"
            out_filename = (
                f"{run_id}__{model_sanitized}__seed{seed_tag}__{timestamp}.jsonl"
            )
            out_file = run_dir / out_filename

            # Pass seed and model and reproducibility params into the evaluator where supported
            extra_args = []
            if model:
                extra_args += ["--model", str(model)]
            if seed is not None:
                # Some evaluators accept --seed; also export SEED env var to maximize coverage
                extra_args += ["--seed", str(seed)]
            # Pass temperature and decoding method if provided
            extra_args += [
                "--temperature",
                str(temperature),
                "--decoding",
                str(decoding),
            ]

            env_vars = {"SEED": seed} if seed is not None else None

            code, out, err = run_prompteval(
                prompt_path, out_file, extra_args=extra_args, env_vars=env_vars
            )

            entry = {
                "model": model,
                "model_version_recorded": model_version,
                "system_prompt": system_prompt,
                "temperature": temperature,
                "decoding_method": decoding,
                "seed": seed,
                "outfile": str(out_file),
                "returncode": code,
                "stdout": out[:4000],
                "stderr": err[:4000],
                "arg_method": "cli_args",
            }

            # If the evaluator rejected CLI args (common), retry using env vars instead
            if code != 0 and err and "unrecognized arguments" in err.lower():
                env_fallback = {
                    "SEED": seed if seed is not None else "",
                    "TEMPERATURE": temperature,
                    "DECODING_METHOD": decoding,
                    "MODEL": model or "",
                }
                code2, out2, err2 = run_prompteval(
                    prompt_path, out_file, extra_args=None, env_vars=env_fallback
                )
                entry.update(
                    {
                        "returncode": code2,
                        "stdout": out2[:4000],
                        "stderr": err2[:4000],
                        "arg_method": "env_vars_fallback",
                    }
                )

            summary["entries"].append(entry)

    # Post-process: compute aggregate score statistics if per-run outfiles contain numeric 'score' fields
    scores = []
    # collect per-criterion values across runs, e.g. {'clarity': [7.0, 7.0, ...], 'effectiveness': [...]}
    criteria_map: dict[str, list[float]] = {}
    for e in summary["entries"]:
        try:
            p = Path(e["outfile"])
            if p.exists():
                text = p.read_text(encoding="utf-8").strip()
                # try to parse last JSON object or full JSONL
                # handle JSONL or JSON
                first_char = text[:1]
                parsed = None
                if not text:
                    continue
                if first_char == "{" or first_char == "[":
                    try:
                        data = json.loads(text)
                    except Exception:
                        # try JSONL: take last line
                        try:
                            last = text.splitlines()[-1]
                            data = json.loads(last)
                        except Exception:
                            data = None
                else:
                    try:
                        last = text.splitlines()[-1]
                        data = json.loads(last)
                    except Exception:
                        data = None
                if data:
                    # look for common score keys
                    for key in ("score", "weighted_score", "weightedScore"):
                        if key in data and isinstance(data[key], (int, float)):
                            scores.append(float(data[key]))
                            break
                    # also collect per-criterion numeric subscores if present
                    if (
                        isinstance(data, dict)
                        and "criteria" in data
                        and isinstance(data["criteria"], dict)
                    ):
                        for ck, cv in data["criteria"].items():
                            try:
                                if isinstance(cv, (int, float)):
                                    criteria_map.setdefault(str(ck), []).append(
                                        float(cv)
                                    )
                            except Exception:
                                # skip non-numeric criterion values
                                continue
        except Exception:
            continue

    summary["score_stats"] = None
    if scores:
        n = len(scores)
        mean = statistics.mean(scores)
        stdev = statistics.stdev(scores) if n > 1 else 0.0
        se = stdev / math.sqrt(n) if n > 1 else 0.0
        ci_mult = 1.96  # approx 95% CI
        ci_low = mean - ci_mult * se
        ci_high = mean + ci_mult * se
        summary["score_stats"] = {
            "n": n,
            "mean": mean,
            "stdev": stdev,
            "95%_ci": [ci_low, ci_high],
        }

    # Compute per-criterion aggregated stats if any criteria were collected
    summary["criteria_stats"] = None
    if criteria_map:
        crit_stats: dict[str, dict] = {}
        for ck, vals in criteria_map.items():
            try:
                n = len(vals)
                mean = statistics.mean(vals)
                stdev = statistics.stdev(vals) if n > 1 else 0.0
                se = stdev / math.sqrt(n) if n > 1 else 0.0
                ci_low = mean - 1.96 * se
                ci_high = mean + 1.96 * se
                crit_stats[ck] = {
                    "n": n,
                    "mean": mean,
                    "stdev": stdev,
                    "95%_ci": [ci_low, ci_high],
                }
            except Exception:
                crit_stats[ck] = None
        summary["criteria_stats"] = crit_stats

    summary_path = run_dir / f"summary_{timestamp}.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Run completed. Summary written to {summary_path}")


if __name__ == "__main__":
    main()
