"""Tests for the frontmatter auditor/refactor tool."""

from pathlib import Path

from testing.validators.frontmatter_auditor import (
    autofix_frontmatter,
    autofix_frontmatter_file,
    validate_frontmatter_dict,
    validate_frontmatter_file,
)


def _write_tmp(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "sample.md"
    path.write_text(content, encoding="utf-8")
    return path


def test_validate_detects_missing_required(temp_invalid_prompt: Path):
    result = validate_frontmatter_file(temp_invalid_prompt)
    assert result.status == "fail"
    assert any("Missing required field" in e.message for e in result.errors)


def test_autofix_adds_missing_fields(temp_invalid_prompt: Path):
    result = autofix_frontmatter_file(temp_invalid_prompt, write=False)
    assert result.status == "fixed"
    assert any("added missing field" in fx for fx in result.fixes_applied)
    assert not result.errors  # placeholders satisfy required fields


def test_autofix_normalizes_scalar_lists(tmp_path: Path):
    content = """---
title: Test
shortTitle: T
intro: One line.
type: reference
difficulty: Beginner
audience: developer
platforms: copilot
topics: testing
author: Me
version: '1.0'
date: 11/30/2025
reviewStatus: Draft
---

Body
"""
    path = _write_tmp(tmp_path, content)
    result = autofix_frontmatter_file(path, write=False)
    assert result.status in {"fixed", "pass"}
    # Run pure autofix to inspect normalized values
    fixed_fm, _ = autofix_frontmatter(
        {
            "title": "Test",
            "shortTitle": "T",
            "intro": "One line.",
            "type": "reference",
            "difficulty": "Beginner",
            "audience": "developer",
            "platforms": "copilot",
            "topics": "testing",
            "author": "Me",
            "version": "1.0",
            "date": "11/30/2025",
            "reviewStatus": "Draft",
        }
    )
    assert isinstance(fixed_fm["audience"], list)
    assert isinstance(fixed_fm["platforms"], list)
    assert fixed_fm["difficulty"] == "beginner"
    assert fixed_fm["reviewStatus"] == "draft"
    assert fixed_fm["date"] == "2025-11-30"


def test_validate_frontmatter_dict_ok():
    fm = {
        "title": "Complete",
        "shortTitle": "Comp",
        "intro": "Complete frontmatter.",
        "type": "reference",
        "difficulty": "beginner",
        "audience": ["developers"],
        "platforms": ["github-copilot"],
        "topics": ["testing"],
        "author": "Tester",
        "version": "1.0",
        "date": "2025-12-01",
        "reviewStatus": "draft",
    }
    errors, warnings = validate_frontmatter_dict(fm)
    assert errors == []
    assert any(w.level == "warning" for w in warnings)
