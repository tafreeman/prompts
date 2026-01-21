#!/usr/bin/env python3
"""Tools Ecosystem Evaluator Runner

Runs the prompt in `prompts/analysis/tools-ecosystem-evaluator.md` against a
`tools/` folder by:

- building an initial inventory (tree + selected key files)
- calling an LLM to request additional evidence files if needed (loop)
- synthesizing a final report
- writing JSONL logs and a final markdown report

Design goals:
- Safe-by-default: no remote providers unless already allowed by llm_client
- Fail-fast: use tools/tool_init.py prerequisite checks
- Script-friendly output: JSON first, markdown report file

This runner is intentionally self-contained so it can be called from `prompt.py`
without requiring additional packaging work.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Add parent directory to path for imports when run as script
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parents[2]))


# NOTE: Avoid importing `tools.*` modules at import-time.
# Many existing modules rely on unqualified imports (e.g. `from errors import ...`)
# and expect `tools/` to be on sys.path. We import those lazily in main().


# =============================================================================
# Prompt loading
# =============================================================================

_CODE_FENCE_RE = re.compile(r"^(?P<fence>`{3,})(?P<lang>\w+)?\s*$")


def extract_prompt_block(markdown: str) -> str:
    """Extract the inner prompt code block from the Tools Ecosystem Evaluator prompt.

    The prompt file stores the runnable prompt inside a fenced block:

        ## Prompt
        ```markdown
        ...
        ```

    We intentionally do not parse frontmatter; we only need the embedded block.
    """
    lines = markdown.splitlines()

    start_idx: Optional[int] = None
    fence: Optional[str] = None

    for i, line in enumerate(lines):
        m = _CODE_FENCE_RE.match(line.strip())
        if not m:
            continue
        lang = (m.group("lang") or "").strip().lower()
        if lang == "markdown":
            start_idx = i + 1
            fence = m.group("fence")
            break

    if start_idx is None:
        raise ValueError("Could not find ```markdown fenced prompt block")

    if fence is None:
        raise ValueError("Could not determine opening fence length")

    # Find closing fence
    for j in range(start_idx, len(lines)):
        if lines[j].strip() == fence:
            end_idx = j
            block = "\n".join(lines[start_idx:end_idx]).strip("\n")
            if not block:
                raise ValueError("Prompt block was empty")
            return block

    raise ValueError("Could not find closing fence for prompt block")


# =============================================================================
# JSON extraction (robust-ish, no dependencies)
# =============================================================================


def _strip_markdown_code_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```") and t.endswith("```"):
        # Remove first fence line and last fence line
        inner = "\n".join(t.splitlines()[1:-1])
        return inner.strip()

    # Common pattern: ```json ... ``` somewhere inside
    m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", t, re.IGNORECASE)
    if m:
        return m.group(1).strip()

    return t


def extract_first_json_object(text: str) -> Dict[str, Any]:
    """Extract the first JSON object from text.

    Strategy:
    1) strip markdown fences
    2) find first '{' and then brace-count until it balances
    """
    cleaned = _strip_markdown_code_fences(text)
    start = cleaned.find("{")
    if start < 0:
        raise ValueError("No JSON object found (missing '{')")

    depth = 0
    in_str = False
    escape = False

    for i in range(start, len(cleaned)):
        ch = cleaned[i]

        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue

        if ch == '"':
            in_str = True
            continue

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                candidate = cleaned[start:i + 1]
                return json.loads(candidate)

    raise ValueError("Unbalanced JSON braces; could not extract object")


# =============================================================================
# Inputs: tree + files
# =============================================================================


def render_tree(root: Path, *, max_depth: int = 4) -> str:
    """Render a compact directory tree (deterministic ordering)."""

    def _iter_children(p: Path) -> List[Path]:
        try:
            children = list(p.iterdir())
        except Exception:
            return []
        # Deterministic: directories first, then files; then name sort
        children.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
        return children

    root = root.resolve()
    lines: List[str] = [str(root.name) + "/"]

    def _walk(dir_path: Path, prefix: str, depth: int):
        if depth >= max_depth:
            return
        children = _iter_children(dir_path)
        for idx, child in enumerate(children):
            is_last = idx == len(children) - 1
            branch = "└── " if is_last else "├── "
            if child.is_dir():
                lines.append(f"{prefix}{branch}{child.name}/")
                extension = "    " if is_last else "│   "
                _walk(child, prefix + extension, depth + 1)
            else:
                lines.append(f"{prefix}{branch}{child.name}")

    _walk(root, "", 0)
    return "\n".join(lines)


def read_text_file(path: Path, *, max_chars: int) -> str:
    """Read a text file with UTF-8 fallback and truncate."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        text = path.read_text(errors="replace")

    if max_chars and len(text) > max_chars:
        return text[:max_chars] + "\n\n... [TRUNCATED]"
    return text


@dataclass
class FileRequest:
    path: str
    reason: str = ""
    max_chars: Optional[int] = None


def _normalize_requested_path(raw: str) -> str:
    # Basic normalization (no globbing): strip, remove surrounding quotes.
    p = raw.strip().strip('"').strip("'")
    p = p.replace("\\", "/")
    return p


def _safe_resolve_under(root: Path, rel: str) -> Optional[Path]:
    """Resolve a relative path under root, returning None if it escapes."""
    rel_norm = _normalize_requested_path(rel)
    candidate = (root / rel_norm).resolve()
    try:
        candidate.relative_to(root.resolve())
        return candidate
    except Exception:
        return None


# =============================================================================
# Runner
# =============================================================================


def _build_collect_prompt(
    *,
    template: str,
    run_id: str,
    chunk_index: int,
    chunk_count: Optional[int],
    focus_areas: Optional[str],
    prior_eval: Optional[str],
    comparison_targets: Optional[str],
    tools_structure: str,
    key_files: List[Tuple[str, str]],
    extra_notes: Optional[str] = None,
) -> str:
    parts: List[str] = []

    # Execution header the model can key off of.
    parts.append("# EXECUTION")
    parts.append(f"RUN_ID: {run_id}")
    parts.append("MODE: COLLECT")
    parts.append(f"CHUNK_INDEX: {chunk_index}")
    parts.append(f"CHUNK_COUNT: {chunk_count if chunk_count is not None else 'unknown'}")
    if focus_areas:
        parts.append(f"FOCUS_AREAS: {focus_areas}")
    if comparison_targets:
        parts.append(f"COMPARISON_TARGETS: {comparison_targets}")
    parts.append("")

    parts.append("# INPUT")
    parts.append("## TOOLS_STRUCTURE")
    parts.append(tools_structure)
    parts.append("")

    parts.append("## KEY_FILES")
    for fp, content in key_files:
        parts.append(f"### {fp}")
        parts.append("```")
        parts.append(content)
        parts.append("```")
        parts.append("")

    if prior_eval:
        parts.append("## PRIOR_EVAL")
        parts.append(prior_eval)
        parts.append("")

    if extra_notes:
        parts.append("## EXTRA_NOTES")
        parts.append(extra_notes)
        parts.append("")

    # We send the long rubric/instructions as the main prompt template.
    # The constructed input becomes appended context.
    return template + "\n\n" + "\n".join(parts)


def _build_synthesize_prompt(
    *,
    template: str,
    run_id: str,
    focus_areas: Optional[str],
    prior_eval: Optional[str],
    comparison_targets: Optional[str],
    collected_notes: List[Dict[str, Any]],
) -> str:
    parts: List[str] = []
    parts.append("# EXECUTION")
    parts.append(f"RUN_ID: {run_id}")
    parts.append("MODE: SYNTHESIZE")
    if focus_areas:
        parts.append(f"FOCUS_AREAS: {focus_areas}")
    if comparison_targets:
        parts.append(f"COMPARISON_TARGETS: {comparison_targets}")
    parts.append("")

    if prior_eval:
        parts.append("## PRIOR_EVAL")
        parts.append(prior_eval)
        parts.append("")

    parts.append("## COLLECTED_NOTES_JSON")
    parts.append("```json")
    parts.append(json.dumps(collected_notes, ensure_ascii=False, indent=2)[:120000])
    parts.append("```")

    return template + "\n\n" + "\n".join(parts)


def _generate_lite_report(final_obj: Dict[str, Any], run_id: str, model: str) -> str:
    """Generate a markdown report from lite mode JSON output."""
    lines = []
    lines.append("# Tools Ecosystem Evaluation Report (Lite)")
    lines.append("")
    lines.append(f"**Run ID:** {run_id}")
    lines.append(f"**Model:** {model}")
    lines.append(f"**Generated:** {datetime.now().isoformat()}")
    lines.append("")
    
    # Summary
    if final_obj.get("summary"):
        lines.append("## Executive Summary")
        lines.append("")
        lines.append(final_obj["summary"])
        lines.append("")
    
    # Scores
    scores = final_obj.get("scores", {})
    if scores:
        lines.append("## Scores")
        lines.append("")
        lines.append("| Dimension | Score |")
        lines.append("|-----------|-------|")
        for dim, score in scores.items():
            if dim != "total":
                dim_label = dim.replace("_", " ").title()
                lines.append(f"| {dim_label} | {score}/100 |")
        if "total" in scores:
            lines.append(f"| **Total** | **{scores['total']}/100** |")
        lines.append("")
    
    # Top Issues
    issues = final_obj.get("top_issues", [])
    if issues:
        lines.append("## Top Issues")
        lines.append("")
        for i, issue in enumerate(issues, 1):
            if isinstance(issue, dict):
                severity = issue.get("severity", "medium")
                desc = issue.get("issue", str(issue))
                fix = issue.get("fix", "")
                lines.append(f"{i}. **[{severity.upper()}]** {desc}")
                if fix:
                    lines.append(f"   - Fix: {fix}")
            else:
                lines.append(f"{i}. {issue}")
        lines.append("")
    
    # Strengths
    strengths = final_obj.get("top_strengths", [])
    if strengths:
        lines.append("## Top Strengths")
        lines.append("")
        for s in strengths:
            lines.append(f"- {s}")
        lines.append("")
    
    # Recommended Actions
    actions = final_obj.get("recommended_actions", [])
    if actions:
        lines.append("## Recommended Actions")
        lines.append("")
        for i, action in enumerate(actions, 1):
            if isinstance(action, dict):
                desc = action.get("action", str(action))
                effort = action.get("effort", "medium")
                impact = action.get("impact", "medium")
                lines.append(f"{i}. {desc}")
                lines.append(f"   - Effort: {effort}, Impact: {impact}")
            else:
                lines.append(f"{i}. {action}")
        lines.append("")
    
    return "\n".join(lines)


def run_tools_ecosystem_evaluator(
    *,
    repo_root: Path,
    tools_dir: Path,
    prompt_path: Path,
    model: str,
    out_path: Path,
    log_jsonl: Path,
    max_rounds: int = 6,
    max_file_chars: int = 12000,
    max_initial_file_chars: int = 8000,
    tree_depth: int = 4,
    focus_areas: Optional[str] = None,
    comparison_targets: Optional[str] = None,
    prior_eval_path: Optional[Path] = None,
    temperature: float = 0.2,
    max_tokens: int = 3500,
) -> Dict[str, Any]:
    """Main runner. Returns a dict summary and writes outputs to disk."""

    prompt_md = prompt_path.read_text(encoding="utf-8", errors="replace")
    template = extract_prompt_block(prompt_md)

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_") + uuid.uuid4().hex[:8]

    prior_eval = None
    if prior_eval_path and prior_eval_path.exists():
        prior_eval = prior_eval_path.read_text(encoding="utf-8", errors="replace")

    tools_structure = render_tree(tools_dir, max_depth=tree_depth)

    # Initial key files: minimal set; model can request more via next_requests.
    # In lite mode (tree_depth <= 1), skip initial files to minimize prompt size.
    if tree_depth <= 1:
        initial_files = []  # Lite mode: tree only, no initial file contents
    else:
        initial_files = [
            tools_dir / "llm_client.py",
            tools_dir / "tool_init.py",
            repo_root / "pyproject.toml",
        ]

    key_files: List[Tuple[str, str]] = []
    for p in initial_files:
        if p.exists() and p.is_file():
            rel = str(p.relative_to(repo_root)).replace("\\", "/")
            key_files.append((rel, read_text_file(p, max_chars=max_initial_file_chars)))

    # Import shared tooling via the packaged namespace (no sys.path hacks).
    from tools.core.tool_init import init_tool
    from tools.llm.llm_client import LLMClient

    init = init_tool(
        name="tools_ecosystem_evaluator",
        required_models=[model],
        required_env=[],
        required_paths=[prompt_path, tools_dir],
        verbose=True,
        log_file=log_jsonl,
    )

    collected_notes: List[Dict[str, Any]] = []
    requested: List[FileRequest] = []

    init.set_total(max_rounds)

    for round_idx in range(1, max_rounds + 1):
        with init.log_item(f"collect_round_{round_idx}") as log:
            # Satisfy any requested file paths from previous round; else stick with initial.
            if requested:
                req_files: List[Tuple[str, str]] = []
                for req in requested:
                    resolved = _safe_resolve_under(repo_root, req.path)
                    if not resolved or not resolved.exists() or not resolved.is_file():
                        continue
                    rel = str(resolved.relative_to(repo_root)).replace("\\", "/")
                    mc = int(req.max_chars) if req.max_chars else max_file_chars
                    req_files.append((rel, read_text_file(resolved, max_chars=mc)))

                # If none resolved, fall back to a small heartbeat file set to avoid empty inputs.
                key_files_for_round = req_files if req_files else key_files
            else:
                key_files_for_round = key_files

            prompt = _build_collect_prompt(
                template=template,
                run_id=run_id,
                chunk_index=round_idx,
                chunk_count=None,
                focus_areas=focus_areas,
                prior_eval=prior_eval,
                comparison_targets=comparison_targets,
                tools_structure=tools_structure,
                key_files=key_files_for_round,
            )

            # Debug: log prompt size
            print(f"  [DEBUG] Prompt size: {len(prompt)} chars")

            raw = LLMClient.generate_text(
                model,
                prompt,
                system_instruction=None,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Debug: show what we got back
            print(f"  [DEBUG] Response size: {len(raw) if raw else 0} chars")
            print(f"  [DEBUG] Response preview: {repr((raw or '')[:200])}")

            if not raw or not raw.strip():
                log.error("Model returned empty response", code="empty_response")
                collected_notes.append({
                    "run_id": run_id,
                    "mode": "COLLECT",
                    "round": round_idx,
                    "parse_error": "empty_response",
                    "raw_preview": "",
                })
                requested = []
                continue

            try:
                data = extract_first_json_object(raw)
            except Exception as e:
                log.error(f"Failed to parse JSON from model output: {e}", code="parse_error")
                collected_notes.append({
                    "run_id": run_id,
                    "mode": "COLLECT",
                    "round": round_idx,
                    "parse_error": str(e),
                    "raw_preview": (raw or "")[:1000],
                })
                requested = []
                continue

            collected_notes.append(data)

            # Pull next file requests (optional)
            requested = []
            for item in data.get("next_requests", []) or []:
                if not isinstance(item, dict):
                    continue
                path = item.get("path")
                if not path:
                    continue
                requested.append(FileRequest(
                    path=str(path),
                    reason=str(item.get("reason") or ""),
                    max_chars=item.get("max_chars"),
                ))

            needs_more = bool(data.get("needs_more"))
            log.success(needs_more=needs_more, requested=len(requested))
            if not needs_more:
                break

    # Synthesize
    with init.log_item("synthesize") as log:
        synth_prompt = _build_synthesize_prompt(
            template=template,
            run_id=run_id,
            focus_areas=focus_areas,
            prior_eval=prior_eval,
            comparison_targets=comparison_targets,
            collected_notes=collected_notes,
        )

        raw = LLMClient.generate_text(
            model,
            synth_prompt,
            system_instruction=None,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        report_md = None
        try:
            final_obj = extract_first_json_object(raw)
            report_md = final_obj.get("report_markdown")
            
            # Lite mode: generate markdown from JSON scores if no report_markdown
            if not report_md and final_obj.get("scores"):
                report_md = _generate_lite_report(final_obj, run_id, model)
        except Exception as e:
            # If JSON parsing fails, check if the raw output looks like markdown
            # (model may have ignored JSON instruction and returned markdown directly)
            if raw and ("# " in raw or "## " in raw):
                print("  [INFO] Model returned markdown directly (not JSON). Using raw output.")
                report_md = raw.strip()
                final_obj = {
                    "run_id": run_id,
                    "mode": "SYNTHESIZE",
                    "report_markdown": report_md,
                    "note": "Extracted from raw markdown output (JSON parse failed)",
                }
            else:
                log.error(f"Failed to parse final JSON from model output: {e}", code="parse_error")
                final_obj = {
                    "run_id": run_id,
                    "mode": "SYNTHESIZE",
                    "parse_error": str(e),
                    "raw_preview": (raw or "")[:2000],
                }

        if isinstance(report_md, str) and report_md.strip():
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report_md, encoding="utf-8")

        log.success(wrote_report=bool(report_md))

    summary = init.summary()
    summary.update({
        "run_id": run_id,
        "model": model,
        "report_path": str(out_path),
        "notes_count": len(collected_notes),
        "final": final_obj,
    })

    return summary


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(argv or sys.argv[1:])

    parser = argparse.ArgumentParser(
        description="Run the Tools Ecosystem Evaluator prompt in a loop, then synthesize a report.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Notes:
              - Remote providers are disabled by default for most prefixes; GitHub Models (gh:*) are allowed.
              - For GitHub Models, ensure `gh auth login` or set GITHUB_TOKEN.
            """
        ),
    )

    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Repository root (default: inferred)",
    )
    parser.add_argument(
        "--tools-dir",
        default=None,
        help="Tools directory (default: <repo-root>/tools)",
    )
    parser.add_argument(
        "--prompt",
        dest="prompt_path",
        default=None,
        help="Prompt markdown file (default: prompts/analysis/tools-ecosystem-evaluator.md)",
    )
    parser.add_argument(
        "--model",
        default="gh:gpt-4o-mini",
        help="Model to use (default: gh:gpt-4o-mini)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output markdown report path (default: results/tools-ecosystem-eval-<run_id>.md)",
    )
    parser.add_argument(
        "--log-jsonl",
        default=None,
        help="JSONL log path (default: logs/tools-ecosystem-eval-<timestamp>.jsonl)",
    )
    parser.add_argument("--max-rounds", type=int, default=4)
    parser.add_argument("--max-file-chars", type=int, default=3000)
    parser.add_argument("--max-initial-file-chars", type=int, default=2000)
    parser.add_argument("--tree-depth", type=int, default=2)
    parser.add_argument("--focus", dest="focus_areas", default=None)
    parser.add_argument("--compare", dest="comparison_targets", default=None)
    parser.add_argument("--prior", dest="prior_eval_path", default=None)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument(
        "--lite",
        action="store_true",
        help="Use lite prompt and minimal context for local models with small context windows",
    )

    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    tools_dir = Path(args.tools_dir).resolve() if args.tools_dir else (repo_root / "tools")

    # Lite mode: use compact prompt and minimal context
    if args.lite:
        prompt_path = (
            Path(args.prompt_path).resolve()
            if args.prompt_path
            else (repo_root / "prompts" / "analysis" / "tools-ecosystem-evaluator-lite.md")
        )
        # Override defaults for lite mode
        max_rounds = min(args.max_rounds, 2)
        max_file_chars = min(args.max_file_chars, 1500)
        max_initial_file_chars = min(args.max_initial_file_chars, 1000)
        tree_depth = min(args.tree_depth, 1)
    else:
        prompt_path = (
            Path(args.prompt_path).resolve()
            if args.prompt_path
            else (repo_root / "prompts" / "analysis" / "tools-ecosystem-evaluator.md")
        )
        max_rounds = args.max_rounds
        max_file_chars = args.max_file_chars
        max_initial_file_chars = args.max_initial_file_chars
        tree_depth = args.tree_depth

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    out_path = (
        Path(args.out).resolve()
        if args.out
        else (repo_root / "results" / f"tools-ecosystem-eval-{timestamp}.md")
    )
    log_jsonl = (
        Path(args.log_jsonl).resolve()
        if args.log_jsonl
        else (repo_root / "logs" / f"tools-ecosystem-eval-{timestamp}.jsonl")
    )

    prior = Path(args.prior_eval_path).resolve() if args.prior_eval_path else None

    _ = run_tools_ecosystem_evaluator(
        repo_root=repo_root,
        tools_dir=tools_dir,
        prompt_path=prompt_path,
        model=args.model,
        out_path=out_path,
        log_jsonl=log_jsonl,
        max_rounds=max_rounds,
        max_file_chars=max_file_chars,
        max_initial_file_chars=max_initial_file_chars,
        tree_depth=tree_depth,
        focus_areas=args.focus_areas,
        comparison_targets=args.comparison_targets,
        prior_eval_path=prior,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
