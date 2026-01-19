#!/usr/bin/env python3
"""Tools Ecosystem Evaluator - Merge Reports

This script takes multiple *generated* Tools Ecosystem Evaluator reports (markdown)
from different models and synthesizes them into a single consolidated MVP report.

Design goals:
- Safe-by-default: relies on tools/llm_client.py provider gating.
- Fail-fast: uses tools/tool_init.py prerequisite checks.
- Script-friendly: writes one merged markdown file.

Typical usage:
  python tools/tools_ecosystem_merge.py \
    --model gh:openai/gpt-4o-mini \
    --out results/tools-ecosystem-eval-merged.md \
    results/tools-ecosystem-eval-*.md
"""

from __future__ import annotations

import argparse
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import List, Optional


def read_text(path: Path, *, max_chars: int) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        text = path.read_text(errors="replace")

    if max_chars and len(text) > max_chars:
        return text[:max_chars] + "\n\n... [TRUNCATED]"
    return text


def build_merge_prompt(*, inputs: List[tuple[str, str]], focus: Optional[str]) -> str:
    parts: List[str] = []
    parts.append(
        textwrap.dedent(
            """
            You are an expert software architect and developer tooling analyst.

            You will be given multiple evaluation reports of the same tooling ecosystem,
            produced by different models. Your job is to merge them into ONE practical,
            action-oriented MVP deliverable.

            Critical rules:
            1) Be evidence-conscious: if the reports disagree, preserve the uncertainty.
            2) Prefer consensus: only treat a claim as 'high confidence' if multiple reports agree.
            3) Produce an MVP plan: the smallest set of PR-sized changes that delivers the biggest ROI.
            4) Do not invent new facts about the repository.

            Output: Return Markdown ONLY (no JSON), using this structure:

            1. Executive Summary (with "Consensus" and "Disagreements" bullets)
            2. MVP Plan (2 PRs max)
               - PR title, files touched (best guess from reports), acceptance criteria, test plan
            3. Risk Register (top 5)
            4. Follow-ups (nice-to-haves)
            """
        ).strip()
    )

    if focus:
        parts.append(f"\nFocus areas: {focus}\n")

    parts.append("\n## Input Reports\n")
    for label, body in inputs:
        parts.append(f"### {label}\n")
        parts.append(body)
        parts.append("\n---\n")

    return "\n".join(parts).strip() + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(argv or sys.argv[1:])

    parser = argparse.ArgumentParser(
        description="Merge multiple Tools Ecosystem Evaluator markdown reports into one MVP report.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Repository root (default: inferred)",
    )
    parser.add_argument(
        "--model",
        default="gh:openai/gpt-4o-mini",
        help="Model to use for merging (default: gh:openai/gpt-4o-mini)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output markdown file (default: results/tools-ecosystem-eval-merged-<timestamp>.md)",
    )
    parser.add_argument(
        "--log-jsonl",
        default=None,
        help="JSONL log path (default: logs/tools-ecosystem-merge-<timestamp>.jsonl)",
    )
    parser.add_argument(
        "--max-chars-per-report",
        type=int,
        default=45000,
        help="Max characters to read from each input report (default: 45000)",
    )
    parser.add_argument(
        "--focus",
        default=None,
        help="Optional focus areas to emphasize during merge",
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input report markdown files (paths)",
    )

    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    tools_dir = repo_root / "tools"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    out_path = (
        Path(args.out).resolve()
        if args.out
        else (repo_root / "results" / f"tools-ecosystem-eval-merged-{timestamp}.md")
    )
    log_jsonl = (
        Path(args.log_jsonl).resolve()
        if args.log_jsonl
        else (repo_root / "logs" / f"tools-ecosystem-merge-{timestamp}.jsonl")
    )

    in_paths = [Path(p).resolve() for p in args.inputs]

    # Import shared tooling via the packaged namespace (no sys.path hacks).
    from tools.core.tool_init import init_tool
    from tools.llm.llm_client import LLMClient

    init = init_tool(
        name="tools_ecosystem_merge",
        required_models=[args.model],
        required_env=[],
        required_paths=[tools_dir, *in_paths],
        verbose=True,
        log_file=log_jsonl,
    )

    inputs: List[tuple[str, str]] = []
    init.set_total(len(in_paths) + 1)

    for p in in_paths:
        with init.log_item(f"read:{p.name}") as log:
            body = read_text(p, max_chars=args.max_chars_per_report)
            label = p.name
            inputs.append((label, body))
            log.success(chars=len(body))

    with init.log_item("merge") as log:
        prompt = build_merge_prompt(inputs=inputs, focus=args.focus)
        merged = LLMClient.generate_text(
            args.model,
            prompt,
            system_instruction=None,
            temperature=0.2,
            max_tokens=3500,
        )

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(merged, encoding="utf-8")
        log.success(wrote=str(out_path))

    init.summary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
