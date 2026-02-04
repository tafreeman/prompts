"""Fix whitespace issues reported by `git diff --check`.

This repo currently has many staged files failing `git diff --cached --check`
(e.g., trailing whitespace, blank line at EOF). This script:

- Runs `git diff --cached --check` (or non-cached if requested)
- Parses the reported file paths
- Rewrites those files to:
  - remove trailing spaces/tabs on each line
  - remove trailing blank lines at EOF
  - (optionally) ensure a single final newline
- Optionally re-stages the touched files

Designed to be safe:
- Works at the *byte* level to avoid encoding surprises
- Skips binary files (detects NUL byte)

Usage examples:
  python tools/scripts/fix_git_whitespace.py --cached --apply --stage
  python tools/scripts/fix_git_whitespace.py --apply --paths prompts/a.md tools/x.py
  python tools/scripts/fix_git_whitespace.py --cached --dry-run
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set, Tuple

_CHECK_LINE_RE = re.compile(r"^(?P<path>.*?):(?P<line>\d+):\s*(?P<msg>.*)$")


@dataclass(frozen=True)
class CheckIssue:
    path: Path
    line: int
    msg: str


def _run_git(args: Sequence[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def find_repo_root(start: Path) -> Path:
    """Find git repo root (prefers `git rev-parse`)."""
    start = start.resolve()

    p = _run_git(["rev-parse", "--show-toplevel"], cwd=start)
    if p.returncode == 0:
        root = (p.stdout or "").strip()
        if root:
            return Path(root)

    # Fallback: walk up looking for .git
    cur = start
    for _ in range(50):
        if (cur / ".git").exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent

    raise RuntimeError(f"Unable to locate git repository root from: {start}")


def parse_git_check_output(output: str, repo_root: Path) -> List[CheckIssue]:
    issues: List[CheckIssue] = []
    for raw_line in output.splitlines():
        m = _CHECK_LINE_RE.match(raw_line.strip())
        if not m:
            continue

        path_str = m.group("path")
        # Ignore the following diff-context lines like '+foo  '
        # Those won't match the regex anyway.
        rel = Path(path_str)
        if not rel.is_absolute():
            rel = repo_root / rel

        issues.append(
            CheckIssue(
                path=rel,
                line=int(m.group("line")),
                msg=m.group("msg").strip(),
            )
        )
    return issues


def collect_paths_from_git_check(repo_root: Path, cached: bool) -> List[Path]:
    args = ["diff", "--check"]
    if cached:
        args.insert(1, "--cached")

    p = _run_git(args, cwd=repo_root)
    # git diff --check returns 1 when it finds problems; that's expected.
    combined = p.stdout or ""

    issues = parse_git_check_output(combined, repo_root)

    # De-dup while preserving order.
    seen: Set[Path] = set()
    ordered: List[Path] = []
    for i in issues:
        if i.path not in seen:
            seen.add(i.path)
            ordered.append(i.path)

    return ordered


def _detect_line_ending(data: bytes) -> bytes:
    # Preserve CRLF if present.
    if b"\r\n" in data:
        return b"\r\n"
    if b"\n" in data:
        return b"\n"
    if b"\r" in data:
        return b"\r"
    # No newline found; default to OS.
    return b"\r\n" if os.linesep == "\r\n" else b"\n"


def _split_keepends(data: bytes) -> List[Tuple[bytes, bytes]]:
    """Return list of (content, newline) preserving newline style per line."""
    parts: List[Tuple[bytes, bytes]] = []

    # bytes.splitlines(keepends=True) handles \r\n, \n, \r
    for line in data.splitlines(keepends=True):
        if line.endswith(b"\r\n"):
            parts.append((line[:-2], b"\r\n"))
        elif line.endswith(b"\n"):
            parts.append((line[:-1], b"\n"))
        elif line.endswith(b"\r"):
            parts.append((line[:-1], b"\r"))
        else:
            parts.append((line, b""))

    # Special case: empty file
    if not parts and data == b"":
        return []

    return parts


def fix_file_bytes(
    data: bytes,
    *,
    ensure_final_newline: bool,
    drop_trailing_blank_lines: bool,
) -> bytes:
    if b"\x00" in data:
        # Binary-ish; don't touch.
        return data

    default_eol = _detect_line_ending(data)
    lines = _split_keepends(data)

    fixed: List[Tuple[bytes, bytes]] = []
    for content, eol in lines:
        # Remove trailing spaces/tabs from each line's content.
        stripped = content.rstrip(b" \t")
        fixed.append((stripped, eol))

    if drop_trailing_blank_lines:
        # Remove trailing completely-empty lines (after trimming) that are at EOF.
        while fixed:
            content, eol = fixed[-1]
            if content == b"" and eol in (b"", b"\n", b"\r", b"\r\n"):
                fixed.pop()
                continue
            break

    out = b"".join(content + eol for content, eol in fixed)

    if ensure_final_newline:
        if out and not out.endswith((b"\n", b"\r")):
            out += default_eol
        elif not out:
            # Empty file: leave empty (don’t force a newline).
            pass

    return out


def fix_path(
    path: Path,
    *,
    ensure_final_newline: bool,
    drop_trailing_blank_lines: bool,
    dry_run: bool,
) -> bool:
    """Fix file in-place.

    Returns True if changed.
    """
    if not path.exists() or not path.is_file():
        return False

    original = path.read_bytes()
    fixed = fix_file_bytes(
        original,
        ensure_final_newline=ensure_final_newline,
        drop_trailing_blank_lines=drop_trailing_blank_lines,
    )

    if fixed == original:
        return False

    if not dry_run:
        path.write_bytes(fixed)

    return True


def stage_paths(repo_root: Path, paths: Iterable[Path]) -> None:
    rels: List[str] = []
    for p in paths:
        try:
            rels.append(str(p.relative_to(repo_root)))
        except ValueError:
            # Outside repo root; skip.
            continue

    if not rels:
        return

    p = _run_git(["add", "--", *rels], cwd=repo_root)
    if p.returncode != 0:
        raise RuntimeError(f"git add failed: {p.stderr}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fix whitespace issues reported by git diff --check"
    )
    parser.add_argument(
        "--cached",
        action="store_true",
        help="Use staged diff (git diff --cached --check)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not write changes")
    parser.add_argument(
        "--apply", action="store_true", help="Apply fixes (default is report-only)"
    )
    parser.add_argument(
        "--stage", action="store_true", help="Re-stage modified files (git add)"
    )
    parser.add_argument(
        "--paths",
        nargs="*",
        default=None,
        help="Explicit file paths to fix (overrides git diff --check discovery)",
    )
    parser.add_argument(
        "--no-final-newline",
        action="store_true",
        help="Do not ensure a final newline at EOF",
    )
    parser.add_argument(
        "--keep-trailing-blank-lines",
        action="store_true",
        help="Do not remove trailing blank lines at EOF",
    )

    args = parser.parse_args(argv)

    script_dir = Path(__file__).resolve().parent
    repo_root = find_repo_root(script_dir)

    if args.paths is not None and len(args.paths) > 0:
        targets = [Path(p) for p in args.paths]
        targets = [p if p.is_absolute() else (repo_root / p) for p in targets]
    else:
        targets = collect_paths_from_git_check(repo_root, cached=args.cached)

    if not targets:
        print("No files found with git whitespace issues.")
        return 0

    print(f"Repo: {repo_root}")
    print(f"Targets: {len(targets)}")

    if not args.apply:
        for p in targets:
            print(
                f"  - {p.relative_to(repo_root) if p.is_relative_to(repo_root) else p}"
            )
        print("\nRun again with --apply to perform fixes.")
        return 0

    changed: List[Path] = []
    skipped_binary: List[Path] = []

    for p in targets:
        if not p.exists() or not p.is_file():
            continue
        data = p.read_bytes()
        if b"\x00" in data:
            skipped_binary.append(p)
            continue

        did_change = fix_path(
            p,
            ensure_final_newline=not args.no_final_newline,
            drop_trailing_blank_lines=not args.keep_trailing_blank_lines,
            dry_run=args.dry_run,
        )
        if did_change:
            changed.append(p)

    print(f"Changed: {len(changed)}")
    if skipped_binary:
        print(f"Skipped (binary): {len(skipped_binary)}")

    if args.stage and changed and not args.dry_run:
        stage_paths(repo_root, changed)
        print("Re-staged modified files.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
