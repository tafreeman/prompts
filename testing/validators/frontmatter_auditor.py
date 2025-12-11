"""
Frontmatter auditor and refactor tool for prompt markdown files.

Features:
- Parse YAML frontmatter.
- Validate required/recommended fields.
- Normalize common issues (scalar->list, enum casing, date format).
- Optional autofix mode with idempotent writes.

This module is designed for reuse by validator tests and the eval pipeline.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REQUIRED_FIELDS: List[str] = [
    "title",
    "shortTitle",
    "intro",
    "type",
    "difficulty",
    "audience",
    "platforms",
    "topics",
    "author",
    "version",
    "date",
    "reviewStatus",
]

RECOMMENDED_FIELDS: List[str] = [
    "governance_tags",
    "dataClassification",
    "effectivenessScore",
]

LIST_FIELDS: List[str] = ["audience", "platforms", "topics", "governance_tags"]

ENUM_FIELDS = {
    "type": ["how_to", "template", "reference", "guide", "playbook"],
    "difficulty": ["beginner", "intermediate", "advanced"],
    "reviewStatus": ["draft", "in-review", "approved"],
}

PLATFORM_NORMALIZATION = {
    "copilot": "github-copilot",
    "github": "github-copilot",
    "m365": "m365",
    "chatgpt": "chatgpt",
    "claude": "claude",
    "gemini": "gemini",
    "generic": "generic",
}

PLACEHOLDERS = {
    "intro": "TODO: one-sentence summary.",
    "author": "TODO: Author Name",
    "version": "0.0.1",
    "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "reviewStatus": "draft",
    "effectivenessScore": 0.0,
}

DEFAULT_LIST_VALUES = {
    "audience": ["general"],
    "platforms": ["github-copilot"],
    "topics": ["general"],
    "governance_tags": [],
}

DEFAULT_SCALAR_VALUES = {
    "type": "reference",
    "difficulty": "beginner",
}


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class ValidationIssue:
    message: str
    field: str | None = None
    level: str = "error"  # error | warning


@dataclass
class ValidationResult:
    file_path: Path
    status: str  # pass | fixed | fail
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)
    fixes_applied: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": str(self.file_path),
            "status": self.status,
            "errors": [vars(e) for e in self.errors],
            "warnings": [vars(w) for w in self.warnings],
            "fixes_applied": self.fixes_applied,
        }


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def split_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Return (frontmatter_dict, body_text)."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    fm_raw = parts[1]
    body = parts[2]

    try:
        fm = yaml.safe_load(fm_raw) or {}
        if not isinstance(fm, dict):
            return {}, content
        return fm, body
    except yaml.YAMLError:
        return {}, content


def dump_frontmatter(fm: Dict[str, Any], body: str) -> str:
    """Serialize frontmatter + body back to markdown."""
    fm_serialized = yaml.safe_dump(fm, sort_keys=False).strip()
    return f"---\n{fm_serialized}\n---\n\n{body.lstrip()}"


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------


def _normalize_enum(value: Any, allowed: List[str]) -> Tuple[Any, bool]:
    if not isinstance(value, str):
        return value, False
    normalized = value.strip().lower()
    return (normalized, normalized in allowed)


def _normalize_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _normalize_date(value: Any) -> Tuple[str | Any, bool]:
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d"), True
    if not isinstance(value, str):
        return value, False
    candidates = ["%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"]
    for fmt in candidates:
        try:
            dt = datetime.strptime(value.strip(), fmt)
            return dt.strftime("%Y-%m-%d"), True
        except ValueError:
            continue
    return value, False


def _normalize_platforms(values: List[Any]) -> Tuple[List[Any], List[str]]:
    fixes = []
    normalized = []
    for v in values:
        if isinstance(v, str):
            key = v.strip().lower()
            mapped = PLATFORM_NORMALIZATION.get(key, key)
            if mapped != v:
                fixes.append(f"platform '{v}' -> '{mapped}'")
            normalized.append(mapped)
        else:
            normalized.append(v)
    return normalized, fixes


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_frontmatter_dict(fm: Dict[str, Any]) -> Tuple[List[ValidationIssue], List[ValidationIssue]]:
    errors: List[ValidationIssue] = []
    warnings: List[ValidationIssue] = []

    for field in REQUIRED_FIELDS:
        if field not in fm:
            errors.append(ValidationIssue(f"Missing required field: {field}", field))
            continue

        value = fm[field]

        if field in LIST_FIELDS:
            if not isinstance(value, list) or len(value) == 0:
                errors.append(ValidationIssue(f"Field '{field}' must be a non-empty list", field))
        elif field == "date":
            normalized, ok = _normalize_date(value)
            if not ok:
                errors.append(ValidationIssue("date must be YYYY-MM-DD", field))
        else:
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(ValidationIssue(f"Field '{field}' must be non-empty", field))

        if field in ENUM_FIELDS:
            normalized, ok = _normalize_enum(fm[field], ENUM_FIELDS[field])
            if not ok:
                errors.append(ValidationIssue(f"Field '{field}' has invalid value: {fm[field]}", field))

    for field in RECOMMENDED_FIELDS:
        if field not in fm:
            warnings.append(ValidationIssue(f"Missing recommended field: {field}", field, level="warning"))

    return errors, warnings


# ---------------------------------------------------------------------------
# Autofix logic
# ---------------------------------------------------------------------------


def autofix_frontmatter(fm: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    fixes: List[str] = []
    fm = dict(fm) if fm else {}

    # Add missing required fields with placeholders
    for field in REQUIRED_FIELDS:
        if field not in fm:
            if field in LIST_FIELDS:
                fm[field] = DEFAULT_LIST_VALUES.get(field, ["TODO"])
            else:
                fm[field] = DEFAULT_SCALAR_VALUES.get(field, PLACEHOLDERS.get(field, ""))
            fixes.append(f"added missing field '{field}'")

    # Add recommended defaults if absent
    for field in RECOMMENDED_FIELDS:
        if field not in fm:
            fm[field] = PLACEHOLDERS.get(field, 0.0 if field == "effectivenessScore" else [])
            fixes.append(f"added recommended field '{field}'")

    # Normalize lists
    for field in LIST_FIELDS:
        if field in fm:
            if not isinstance(fm[field], list):
                fm[field] = _normalize_list(fm[field])
                fixes.append(f"normalized '{field}' to list")
            if field == "platforms":
                normalized, platform_fixes = _normalize_platforms(fm[field])
                if platform_fixes:
                    fixes.extend(platform_fixes)
                fm[field] = normalized

    # Normalize enums
    for field, allowed in ENUM_FIELDS.items():
        if field in fm and isinstance(fm[field], str):
            norm, ok = _normalize_enum(fm[field], allowed)
            if ok and norm != fm[field]:
                fm[field] = norm
                fixes.append(f"normalized '{field}' casing")

    # Normalize date
    if "date" in fm:
        norm, ok = _normalize_date(fm["date"])
        if ok and norm != fm["date"]:
            fm["date"] = norm
            fixes.append("normalized 'date' format")

    return fm, fixes


# ---------------------------------------------------------------------------
# File-level API
# ---------------------------------------------------------------------------


def validate_frontmatter_file(path: Path) -> ValidationResult:
    content = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(content)

    errors, warnings = validate_frontmatter_dict(fm)
    status = "pass" if not errors else "fail"

    return ValidationResult(
        file_path=path,
        status=status,
        errors=errors,
        warnings=warnings,
    )


def autofix_frontmatter_file(path: Path, write: bool = False) -> ValidationResult:
    content = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(content)

    fixed_fm, fixes = autofix_frontmatter(fm)
    errors, warnings = validate_frontmatter_dict(fixed_fm)

    status = "fixed" if fixes and not errors else ("pass" if not errors else "fail")

    result = ValidationResult(
        file_path=path,
        status=status,
        errors=errors,
        warnings=warnings,
        fixes_applied=fixes,
    )

    if write and (fixes or status == "fixed"):
        new_content = dump_frontmatter(fixed_fm, body)
        path.write_text(new_content, encoding="utf-8")

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _collect_files(paths: List[str]) -> List[Path]:
    files: List[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            files.extend(path.rglob("*.md"))
        elif path.is_file():
            files.append(path)
    # Basic filtering: skip README/index
    return [f for f in files if f.name.lower() not in {"readme.md", "index.md"}]


def run_cli(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Frontmatter auditor")
    parser.add_argument("paths", nargs="+", help="Files or directories to audit")
    parser.add_argument("--fix", action="store_true", help="Apply autofixes")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-file output")
    args = parser.parse_args(argv)

    files = _collect_files(args.paths)
    results: List[ValidationResult] = []

    for f in files:
        res = autofix_frontmatter_file(f, write=args.fix) if args.fix else validate_frontmatter_file(f)
        results.append(res)
        if not args.quiet and args.format == "text":
            print(f"{res.status.upper():<6} {f}")
            for e in res.errors:
                print(f"  ERROR: {e.message}")
            for w in res.warnings:
                print(f"  WARN: {w.message}")
            for fx in res.fixes_applied:
                print(f"  FIX: {fx}")

    exit_code = 0 if all(r.status != "fail" for r in results) else 1

    if args.format == "json":
        payload = {
            "files": [r.to_dict() for r in results],
            "summary": {
                "scanned": len(results),
                "failed": sum(1 for r in results if r.status == "fail"),
                "fixed": sum(1 for r in results if r.status == "fixed"),
                "passed": sum(1 for r in results if r.status == "pass"),
            },
        }
        print(json.dumps(payload, indent=2))

    return exit_code


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(run_cli())
