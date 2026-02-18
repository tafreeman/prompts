#!/usr/bin/env python3
"""Model bakeoff + alignment helper for local and hosted model endpoints.

Purpose
-------
Run a lightweight, repeatable capability comparison across discovered models and
recommend model alignment values for deep research workflows:

- ``DEEP_RESEARCH_SMALL_MODEL``
- ``DEEP_RESEARCH_HEAVY_MODEL``

Designed to run from Windows PowerShell outside WSL as requested.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class TaskSpec:
    task_id: str
    title: str
    prompt: str
    expect_json: bool
    required_keys: list[str]
    required_terms: list[str]
    weight: float


TASKS: list[TaskSpec] = [
    TaskSpec(
        task_id="workflow_strategy",
        title="Workflow Pattern Selection",
        prompt=(
            "You are advising engineers on agentic AI workflow design.\n"
            "Choose among ToT, ReAct, CoVe, and iterative review loops for a deep "
            "research system. Return JSON with keys:\n"
            "recommended_workflow, when_to_use, when_not_to_use, quality_gates.\n"
            "Keep it concise and practical."
        ),
        expect_json=True,
        required_keys=[
            "recommended_workflow",
            "when_to_use",
            "when_not_to_use",
            "quality_gates",
        ],
        required_terms=["tot", "react", "cove", "confidence", "verification"],
        weight=1.0,
    ),
    TaskSpec(
        task_id="architecture",
        title="Architecture Plan",
        prompt=(
            "Design an architecture for a multi-agent deep research platform used "
            "by software engineers and architects. Include source governance, "
            "verification, and RAG packaging. Return JSON with keys:\n"
            "components, data_flow, observability, failure_modes, mitigations."
        ),
        expect_json=True,
        required_keys=[
            "components",
            "data_flow",
            "observability",
            "failure_modes",
            "mitigations",
        ],
        required_terms=["rag", "cit", "source", "policy", "guardrail"],
        weight=1.1,
    ),
    TaskSpec(
        task_id="implementation_plan",
        title="Implementation Plan",
        prompt=(
            "Produce an implementation plan for the architecture. Include testing "
            "strategy for unit, integration, and end-to-end. Return JSON with keys:\n"
            "phases, tests, rollback, risks, owners."
        ),
        expect_json=True,
        required_keys=["phases", "tests", "rollback", "risks", "owners"],
        required_terms=["unit", "integration", "end-to-end", "rollback", "adr"],
        weight=1.0,
    ),
    TaskSpec(
        task_id="code_task",
        title="Coding Practicality",
        prompt=(
            "Write Python code for a function `rank_sources(sources)` that sorts "
            "research sources by trust score and recency. Include a minimal pytest "
            "unit test snippet."
        ),
        expect_json=False,
        required_keys=[],
        required_terms=["def rank_sources", "pytest", "assert"],
        weight=0.9,
    ),
]


def _repo_root() -> Path:
    # tools/llm/model_bakeoff.py -> repo root
    return Path(__file__).resolve().parents[2]


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if value and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        os.environ.setdefault(key, value)


def _ensure_import_path() -> None:
    root = _repo_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


def _provider_of(model_id: str) -> str:
    if ":" not in model_id:
        return "ollama"
    return model_id.split(":", 1)[0].lower()


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _is_local_openai_base(base_url: str | None) -> bool:
    if not base_url:
        return False
    text = base_url.lower()
    return any(host in text for host in ["localhost", "127.0.0.1", "::1"])


def _discover_openai_compatible_models(base_url: str) -> list[str]:
    base = base_url.rstrip("/")
    url = f"{base}/models" if base.endswith("/v1") else f"{base}/v1/models"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return []

    models: list[str] = []
    if isinstance(data, dict):
        for item in data.get("data", []):
            if isinstance(item, dict):
                model_id = str(item.get("id", "")).strip()
                if model_id:
                    models.append(f"openai:{model_id}")
    return models


def _parse_json_from_text(text: str) -> dict[str, Any] | None:
    raw = text.strip()
    if not raw:
        return None

    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    for candidate in fenced:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            continue

    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            parsed = json.loads(raw[start : end + 1])
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

    return None


def _score_task(task: TaskSpec, response_text: str, elapsed_s: float, error: str | None) -> dict[str, Any]:
    checks: dict[str, Any] = {
        "has_content": bool(response_text.strip()),
        "json_ok": False,
        "required_key_ratio": 0.0,
        "required_term_ratio": 0.0,
        "error": error,
    }

    if error:
        return {"score": 0.0, "checks": checks}

    score = 0.0
    text_lower = response_text.lower()

    if checks["has_content"]:
        score += 20.0

    parsed_json = None
    if task.expect_json:
        parsed_json = _parse_json_from_text(response_text)
        checks["json_ok"] = parsed_json is not None
        if checks["json_ok"]:
            score += 30.0
        if task.required_keys:
            present = sum(1 for key in task.required_keys if isinstance(parsed_json, dict) and key in parsed_json)
            ratio = present / len(task.required_keys)
            checks["required_key_ratio"] = ratio
            score += ratio * 30.0

    if task.required_terms:
        present_terms = sum(1 for term in task.required_terms if term.lower() in text_lower)
        term_ratio = present_terms / len(task.required_terms)
        checks["required_term_ratio"] = term_ratio
        score += term_ratio * 20.0

    # Latency penalty to reward usable responsiveness for interactive workflows.
    score -= min(elapsed_s, 120.0) * 0.15
    score = max(0.0, min(score, 100.0))

    return {"score": round(score, 2), "checks": checks}


def _discover_candidates(
    providers: list[str],
    max_per_provider: int,
    explicit_models: list[str],
    include_openai_local: bool,
    force_probe: bool,
    verbose: bool,
) -> tuple[list[str], dict[str, Any], dict[str, Any]]:
    from tools.llm.model_probe import ModelProbe, discover_all_models

    discovered = discover_all_models(verbose=verbose)
    candidates: list[str] = []

    if explicit_models:
        candidates.extend(explicit_models)
    else:
        for provider in providers:
            available = discovered.get("providers", {}).get(provider, {}).get("available", [])
            if isinstance(available, list):
                candidates.extend([str(m) for m in available[:max_per_provider]])

        if include_openai_local:
            base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")
            if _is_local_openai_base(base_url):
                candidates.extend(_discover_openai_compatible_models(base_url))

    candidates = _dedupe_keep_order([m for m in candidates if m.strip()])

    probe = ModelProbe(verbose=verbose)
    runnable = probe.filter_runnable(candidates, force_probe=force_probe)
    report = probe.get_probe_report(candidates)
    return runnable, discovered, report


def _run_bakeoff(
    models: list[str],
    tasks: list[TaskSpec],
    temperature: float,
    max_tokens: int,
) -> list[dict[str, Any]]:
    from tools.llm.llm_client import LLMClient

    model_results: list[dict[str, Any]] = []
    system_prompt = (
        "You are a pragmatic senior AI/software architect. Provide concise, "
        "technically precise outputs."
    )

    for model in models:
        task_results: list[dict[str, Any]] = []
        for task in tasks:
            started = time.perf_counter()
            error = None
            response = ""
            try:
                response = LLMClient.generate_text(
                    model_name=model,
                    prompt=task.prompt,
                    system_instruction=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            except Exception as exc:  # noqa: BLE001
                error = str(exc)
            elapsed = time.perf_counter() - started
            scored = _score_task(task, response, elapsed, error)
            task_results.append(
                {
                    "task_id": task.task_id,
                    "title": task.title,
                    "elapsed_s": round(elapsed, 3),
                    "score": scored["score"],
                    "checks": scored["checks"],
                    "error": error,
                    "response_preview": response[:1200],
                }
            )

        successful = [t for t in task_results if not t["error"]]
        avg_latency = statistics.mean(t["elapsed_s"] for t in task_results) if task_results else 0.0
        weighted_score = 0.0
        total_weight = 0.0
        for task, result in zip(tasks, task_results, strict=False):
            weighted_score += float(result["score"]) * task.weight
            total_weight += task.weight
        task_score = (weighted_score / total_weight) if total_weight else 0.0
        success_rate = (len(successful) / len(task_results)) if task_results else 0.0
        overall_score = max(0.0, min(task_score + (success_rate * 10.0) - (avg_latency * 0.2), 100.0))

        model_results.append(
            {
                "model": model,
                "provider": _provider_of(model),
                "overall_score": round(overall_score, 2),
                "task_score": round(task_score, 2),
                "success_rate": round(success_rate, 3),
                "avg_latency_s": round(avg_latency, 3),
                "tasks": task_results,
            }
        )

    model_results.sort(
        key=lambda r: (
            r["overall_score"],
            r["task_score"],
            r["success_rate"],
            -r["avg_latency_s"],
        ),
        reverse=True,
    )
    return model_results


def _recommend_alignment(results: list[dict[str, Any]]) -> dict[str, str | None]:
    if not results:
        return {"small": None, "heavy": None}

    heavy = results[0]["model"]

    # Prefer fast + decent for small model.
    small_ranked = sorted(
        results,
        key=lambda r: (
            r["task_score"] - (r["avg_latency_s"] * 0.8),
            r["success_rate"],
        ),
        reverse=True,
    )
    small = small_ranked[0]["model"] if small_ranked else heavy

    return {"small": small, "heavy": heavy}


def _write_reports(
    out_dir: Path,
    payload: dict[str, Any],
    alignment: dict[str, str | None],
    write_env: Path | None,
) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")

    json_path = out_dir / f"model_bakeoff_{ts}.json"
    md_path = out_dir / f"model_bakeoff_{ts}.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines: list[str] = []
    lines.append("# Model Bakeoff Report")
    lines.append("")
    lines.append(f"- Generated: `{payload['timestamp_utc']}`")
    lines.append(f"- Models tested: `{payload['summary']['tested_models']}`")
    lines.append(f"- Runnable models: `{payload['summary']['runnable_models']}`")
    lines.append("")
    lines.append("## Recommended Alignment")
    lines.append("")
    lines.append("```env")
    lines.append(f"DEEP_RESEARCH_SMALL_MODEL={alignment.get('small') or ''}")
    lines.append(f"DEEP_RESEARCH_HEAVY_MODEL={alignment.get('heavy') or ''}")
    if alignment.get("small"):
        lines.append(f"AGENTIC_MODEL_TIER_2={alignment['small']}")
    if alignment.get("heavy"):
        lines.append(f"AGENTIC_MODEL_TIER_3={alignment['heavy']}")
        lines.append(f"AGENTIC_MODEL_TIER_4={alignment['heavy']}")
    lines.append("```")
    lines.append("")
    lines.append("## Ranking")
    lines.append("")
    lines.append("| Rank | Model | Provider | Overall | Task Score | Success | Avg Latency (s) |")
    lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: |")
    for idx, row in enumerate(payload["results"], start=1):
        lines.append(
            f"| {idx} | `{row['model']}` | `{row['provider']}` | "
            f"{row['overall_score']:.2f} | {row['task_score']:.2f} | "
            f"{row['success_rate']:.2%} | {row['avg_latency_s']:.3f} |"
        )
    lines.append("")
    lines.append(f"- JSON details: `{json_path}`")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    if write_env:
        write_env.parent.mkdir(parents=True, exist_ok=True)
        env_lines = [
            f"# Generated by tools/llm/model_bakeoff.py at {payload['timestamp_utc']}",
            f"DEEP_RESEARCH_SMALL_MODEL={alignment.get('small') or ''}",
            f"DEEP_RESEARCH_HEAVY_MODEL={alignment.get('heavy') or ''}",
        ]
        if alignment.get("small"):
            env_lines.append(f"AGENTIC_MODEL_TIER_2={alignment['small']}")
        if alignment.get("heavy"):
            env_lines.append(f"AGENTIC_MODEL_TIER_3={alignment['heavy']}")
            env_lines.append(f"AGENTIC_MODEL_TIER_4={alignment['heavy']}")
        write_env.write_text("\n".join(env_lines) + "\n", encoding="utf-8")

    return json_path, md_path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Run a lightweight model bakeoff and suggest alignment values."
    )
    parser.add_argument(
        "--providers",
        default="local_onnx,ollama,ai_toolkit,openai",
        help=(
            "Comma-separated providers from model_probe discovery "
            "(default: local_onnx,ollama,ai_toolkit,openai)"
        ),
    )
    parser.add_argument(
        "--models",
        nargs="*",
        default=[],
        help="Explicit model IDs (skips discovery selection).",
    )
    parser.add_argument(
        "--max-models-per-provider",
        type=int,
        default=6,
        help="Limit models selected per provider during discovery (default: 6).",
    )
    parser.add_argument(
        "--max-models",
        type=int,
        default=24,
        help="Global cap on runnable models tested (default: 24).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="Generation temperature for bakeoff prompts (default: 0.1).",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=900,
        help="Max tokens per prompt call (default: 900).",
    )
    parser.add_argument(
        "--out-dir",
        default="reports/model-bakeoff",
        help="Output directory for JSON/Markdown reports.",
    )
    parser.add_argument(
        "--write-env",
        default="",
        help="Optional env file path to write recommended model alignment values.",
    )
    parser.add_argument(
        "--force-probe",
        action="store_true",
        help="Force fresh model probe checks (ignore cache).",
    )
    parser.add_argument(
        "--include-openai-local",
        action="store_true",
        help="Include models from OPENAI_BASE_URL /v1/models when local endpoint is set.",
    )
    parser.add_argument(
        "--allow-remote",
        action="store_true",
        help="Set PROMPTEVAL_ALLOW_REMOTE=1 for openai/gemini/claude providers.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Probe/select models and print alignment without running prompts.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose discovery/probe logs.",
    )
    args = parser.parse_args(argv)

    _ensure_import_path()
    _load_dotenv(_repo_root() / ".env")

    if args.allow_remote:
        os.environ.setdefault("PROMPTEVAL_ALLOW_REMOTE", "1")

    providers = [p.strip() for p in args.providers.split(",") if p.strip()]
    explicit_models = _dedupe_keep_order([m.strip() for m in args.models if m.strip()])

    runnable, discovered, probe_report = _discover_candidates(
        providers=providers,
        max_per_provider=max(1, args.max_models_per_provider),
        explicit_models=explicit_models,
        include_openai_local=bool(args.include_openai_local),
        force_probe=bool(args.force_probe),
        verbose=bool(args.verbose),
    )

    runnable = runnable[: max(1, args.max_models)]
    if not runnable:
        print("No runnable models found for the selected discovery settings.")
        return 1

    if args.dry_run:
        preview_alignment = {
            "small": runnable[0] if runnable else None,
            "heavy": runnable[0] if runnable else None,
        }
        print("Runnable models:")
        for model in runnable:
            print(f"- {model}")
        print("\nPreview alignment:")
        print(json.dumps(preview_alignment, indent=2))
        return 0

    results = _run_bakeoff(
        models=runnable,
        tasks=TASKS,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )
    alignment = _recommend_alignment(results)

    now_utc = datetime.now(timezone.utc).isoformat()
    payload = {
        "timestamp_utc": now_utc,
        "config": {
            "providers": providers,
            "explicit_models": explicit_models,
            "max_models_per_provider": args.max_models_per_provider,
            "max_models": args.max_models,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "allow_remote": args.allow_remote,
            "include_openai_local": args.include_openai_local,
        },
        "summary": {
            "tested_models": len(results),
            "runnable_models": len(runnable),
        },
        "alignment": alignment,
        "probe_report": probe_report,
        "discovery_snapshot": discovered,
        "results": results,
    }

    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = _repo_root() / out_dir

    write_env_path = Path(args.write_env) if args.write_env else None
    if write_env_path and not write_env_path.is_absolute():
        write_env_path = _repo_root() / write_env_path

    json_path, md_path = _write_reports(
        out_dir=out_dir,
        payload=payload,
        alignment=alignment,
        write_env=write_env_path,
    )

    print("\nModel bakeoff complete.")
    print(f"- JSON report: {json_path}")
    print(f"- Markdown report: {md_path}")
    print("- Recommended alignment:")
    print(f"  DEEP_RESEARCH_SMALL_MODEL={alignment.get('small') or ''}")
    print(f"  DEEP_RESEARCH_HEAVY_MODEL={alignment.get('heavy') or ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
