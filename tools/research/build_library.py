#!/usr/bin/env python3
"""Build a consolidated research library from repo artifacts.

This script scans the repository for research-related materials, copies non-code
artifacts into ``research/library/artifacts`` (preserving relative paths),
indexes code references, and extracts/vets URLs into a source registry.

Public API
----------
- ``build_library(root, max_copy_mb)`` — main orchestration function.
- ``main()`` — CLI entry point.

All private helpers, dataclasses, and constants live in ``library_helpers``.
They are re-exported here for backward compatibility.
"""

from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from pathlib import Path

from tools.research.library_helpers import (
    APPROVED_DOMAINS,
    APPROVED_SUFFIXES,
    ASSET_URL_SUFFIXES,
    CAUTION_DOMAINS,
    CODE_EXTS,
    DOC_EXTS,
    EXCLUDED_DIRS,
    RESEARCH_KEYWORDS,
    SEED_FILES,
    SEED_PREFIXES,
    TEXT_EXTS,
    URL_PATTERN,
    MaterialRecord,
    UrlRecord,
    _classify_domain,
    _is_asset_url,
    _is_research_material,
    _is_seed_match,
    _is_valid_domain,
    _iter_files,
    _normalize_domain,
    _normalize_url,
    _now_iso,
    _path_has_keyword,
    _read_for_urls,
    _relative,
    _sha256,
)
from urllib.parse import urlparse


def build_library(root: Path, max_copy_mb: int = 20) -> dict:
    """Scan *root* for research materials and build a consolidated library.

    Parameters
    ----------
    root:
        Repository root directory.
    max_copy_mb:
        Maximum file size (in MB) to physically copy into the library.
        Larger files are indexed as references only.

    Returns
    -------
    dict
        Paths to the generated manifest, source registry, and README.
    """
    research_root = root / "research"
    library_root = research_root / "library"
    artifacts_root = library_root / "artifacts"
    subagents_root = research_root / "subagents"

    max_copy_bytes = max_copy_mb * 1024 * 1024

    artifacts_root.parent.mkdir(parents=True, exist_ok=True)
    if artifacts_root.exists():
        shutil.rmtree(artifacts_root)
    artifacts_root.mkdir(parents=True, exist_ok=True)
    subagents_root.mkdir(parents=True, exist_ok=True)

    records: list[MaterialRecord] = []
    code_refs: list[MaterialRecord] = []
    url_map: dict[str, dict] = {}
    domain_counter: Counter[str] = Counter()

    for path in _iter_files(root):
        rel = path.relative_to(root)
        if not _is_research_material(rel):
            continue

        suffix = path.suffix.lower()
        size_bytes = path.stat().st_size

        is_code = suffix in CODE_EXTS
        is_doc = suffix in DOC_EXTS or suffix == ""

        if is_code:
            rec = MaterialRecord(
                source_path=_relative(path, root),
                category="code",
                action="reference",
                destination_path=None,
                size_bytes=size_bytes,
                sha256=None,
                reason="code artifact referenced, not duplicated",
            )
            records.append(rec)
            code_refs.append(rec)
            continue

        if not is_doc:
            continue

        if size_bytes > max_copy_bytes:
            rec = MaterialRecord(
                source_path=_relative(path, root),
                category="document",
                action="reference",
                destination_path=None,
                size_bytes=size_bytes,
                sha256=None,
                reason=f"file exceeds copy limit ({max_copy_mb} MB)",
            )
            records.append(rec)
            continue

        dest = artifacts_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)

        digest = _sha256(dest)
        rec = MaterialRecord(
            source_path=_relative(path, root),
            category="document",
            action="copied",
            destination_path=_relative(dest, root),
            size_bytes=size_bytes,
            sha256=digest,
            reason="research document consolidated",
        )
        records.append(rec)

        text = _read_for_urls(dest)
        if not text:
            continue

        urls = {_normalize_url(u) for u in URL_PATTERN.findall(text)}
        for url in sorted(urls):
            if _is_asset_url(url):
                continue
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"}:
                continue
            domain = _normalize_domain(parsed.netloc)
            if not _is_valid_domain(domain):
                continue
            status, reason = _classify_domain(domain)
            domain_counter[domain] += 1
            if url not in url_map:
                url_map[url] = {
                    "url": url,
                    "domain": domain,
                    "status": status,
                    "reason": reason,
                    "referenced_by": [_relative(dest, root)],
                }
            else:
                refs = url_map[url]["referenced_by"]
                ref = _relative(dest, root)
                if ref not in refs:
                    refs.append(ref)

    url_records = [
        UrlRecord(
            url=data["url"],
            domain=data["domain"],
            status=data["status"],
            reason=data["reason"],
            referenced_by=sorted(data["referenced_by"]),
        )
        for data in url_map.values()
    ]
    url_records.sort(key=lambda r: (r.status, r.domain, r.url))

    records.sort(key=lambda r: (r.category, r.action, r.source_path))
    code_refs.sort(key=lambda r: r.source_path)

    summary = {
        "generated_at": _now_iso(),
        "total_materials": len(records),
        "copied_documents": sum(1 for r in records if r.action == "copied"),
        "referenced_documents": sum(
            1 for r in records if r.category == "document" and r.action == "reference"
        ),
        "code_references": len(code_refs),
        "total_urls": len(url_records),
        "approved_urls": sum(1 for u in url_records if u.status == "approved"),
        "caution_urls": sum(1 for u in url_records if u.status == "caution"),
        "review_urls": sum(1 for u in url_records if u.status == "review"),
    }

    manifest_path = library_root / "material_manifest.json"
    source_registry_path = library_root / "source_registry.json"
    approved_domains_path = library_root / "approved_domains.md"
    reputable_sources_path = library_root / "reputable_sources.md"
    code_refs_path = library_root / "code_references.md"
    readme_path = research_root / "README.md"
    roles_path = subagents_root / "ROLE_DEFINITIONS.md"
    scout_path = subagents_root / "SCOUT_REPORT.md"
    curator_path = subagents_root / "CURATOR_REPORT.md"
    source_audit_path = subagents_root / "SOURCE_AUDITOR_REPORT.md"
    librarian_path = subagents_root / "LIBRARIAN_REPORT.md"

    manifest_payload = {
        "summary": summary,
        "materials": [r.__dict__ for r in records],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest_payload, indent=2), encoding="utf-8")

    source_registry_payload = {
        "summary": summary,
        "sources": [u.__dict__ for u in url_records],
    }
    source_registry_path.write_text(
        json.dumps(source_registry_payload, indent=2),
        encoding="utf-8",
    )

    approved_domains = sorted(
        {u.domain for u in url_records if u.status == "approved" and u.domain}
    )
    caution_domains = sorted(
        {u.domain for u in url_records if u.status == "caution" and u.domain}
    )
    review_domains = sorted(
        {u.domain for u in url_records if u.status == "review" and u.domain}
    )

    approved_domains_path.write_text(
        "\n".join(
            [
                "# Approved Source Domains",
                "",
                "Use these by default for research citations.",
                "",
                "## Approved",
                *[f"- `{d}`" for d in approved_domains],
                "",
                "## Caution",
                *[f"- `{d}`" for d in caution_domains],
                "",
                "## Needs Review",
                *[f"- `{d}`" for d in review_domains],
                "",
            ]
        ),
        encoding="utf-8",
    )

    approved_urls = [u for u in url_records if u.status == "approved"]
    caution_urls = [u for u in url_records if u.status == "caution"]
    review_urls = [u for u in url_records if u.status == "review"]
    reputable_sources_path.write_text(
        "\n".join(
            [
                "# Reputable Sources (URL Level)",
                "",
                "These URLs were extracted from consolidated research artifacts.",
                "",
                f"- Approved URLs: `{len(approved_urls)}`",
                f"- Caution URLs: `{len(caution_urls)}`",
                f"- Needs-review URLs: `{len(review_urls)}`",
                "",
                "## Approved URLs",
                *[f"- `{u.url}`" for u in approved_urls],
                "",
            ]
        ),
        encoding="utf-8",
    )

    code_lines = [
        "# Code References (Not Duplicated)",
        "",
        "These files are code/assets used in research workflows and are referenced only.",
        "",
    ]
    for rec in code_refs:
        code_lines.append(f"- `{rec.source_path}`")
    code_lines.append("")
    code_refs_path.write_text("\n".join(code_lines), encoding="utf-8")

    top_domains = domain_counter.most_common(20)
    top_domain_lines = [
        f"- `{domain}`: {count}" for domain, count in top_domains if domain
    ]

    readme_lines = [
        "# Research Library",
        "",
        "Role-driven consolidated research library generated from this repository.",
        "",
        "## Subagent Roles",
        "- `Scout`: discover and inventory research materials across the repo.",
        "- `Curator`: consolidate non-code artifacts into a normalized library structure.",
        "- `Engineer`: keep executable/code assets as references instead of duplicates.",
        "- `Source Auditor`: extract and classify source URLs for reputation and safety.",
        "- `Librarian`: publish searchable manifests and indexes.",
        "",
        "## Outputs",
        "- `research/library/artifacts/`: consolidated non-code research materials.",
        "- `research/library/material_manifest.json`: file-level inventory and actions.",
        "- `research/library/code_references.md`: code assets referenced for research.",
        "- `research/library/source_registry.json`: URL/domain registry with trust status.",
        "- `research/library/approved_domains.md`: suggested approved/caution/review domains.",
        "- `research/library/reputable_sources.md`: approved URL-level source list.",
        "- `research/subagents/*.md`: per-role execution reports.",
        "",
        "## Current Snapshot",
        f"- Generated: `{summary['generated_at']}`",
        f"- Materials indexed: `{summary['total_materials']}`",
        f"- Documents copied: `{summary['copied_documents']}`",
        f"- Documents referenced: `{summary['referenced_documents']}`",
        f"- Code references: `{summary['code_references']}`",
        f"- URLs extracted: `{summary['total_urls']}`",
        f"- Approved URLs: `{summary['approved_urls']}`",
        f"- Caution URLs: `{summary['caution_urls']}`",
        f"- Review URLs: `{summary['review_urls']}`",
        "",
        "## Top Domains",
        *top_domain_lines,
        "",
        "## Regenerate",
        "- `python tools/research/build_library.py`",
        "",
    ]
    readme_path.write_text("\n".join(readme_lines), encoding="utf-8")

    roles_path.write_text(
        "\n".join(
            [
                "# Subagent Role Definitions",
                "",
                "- `Scout`: Locate research artifacts and classify material relevance.",
                "- `Curator`: Consolidate non-code materials into `research/library/artifacts/`.",
                "- `Engineer`: Reference code instead of duplicating executable assets.",
                "- `Source Auditor`: Extract URLs and classify trust status by domain.",
                "- `Librarian`: Build indexes/manifests and maintain discoverability.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    scout_path.write_text(
        "\n".join(
            [
                "# Scout Report",
                "",
                f"- Files identified: `{summary['total_materials']}`",
                f"- Research documents: `{summary['copied_documents'] + summary['referenced_documents']}`",
                f"- Code references identified: `{summary['code_references']}`",
                "",
                "Primary discovery seeds:",
                *[f"- `{p.as_posix()}`" for p in SEED_PREFIXES],
                "",
            ]
        ),
        encoding="utf-8",
    )

    curator_path.write_text(
        "\n".join(
            [
                "# Curator Report",
                "",
                f"- Documents copied into library: `{summary['copied_documents']}`",
                f"- Documents referenced only: `{summary['referenced_documents']}`",
                f"- Copy size limit used: `{max_copy_mb} MB`",
                "",
                "Consolidation target: `research/library/artifacts/`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    source_audit_path.write_text(
        "\n".join(
            [
                "# Source Auditor Report",
                "",
                f"- Total URLs extracted: `{summary['total_urls']}`",
                f"- Approved URLs: `{summary['approved_urls']}`",
                f"- Caution URLs: `{summary['caution_urls']}`",
                f"- Needs-review URLs: `{summary['review_urls']}`",
                "",
                "See `research/library/source_registry.json` for full details.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    librarian_path.write_text(
        "\n".join(
            [
                "# Librarian Report",
                "",
                "Library indexes created:",
                "- `research/library/material_manifest.json`",
                "- `research/library/code_references.md`",
                "- `research/library/source_registry.json`",
                "- `research/library/approved_domains.md`",
                "- `research/library/reputable_sources.md`",
                "",
                "This structure is ready to evolve into a reusable research library.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {
        "summary": summary,
        "manifest": str(manifest_path.relative_to(root)),
        "source_registry": str(source_registry_path.relative_to(root)),
        "readme": str(readme_path.relative_to(root)),
    }


def main() -> None:
    """CLI entry point: parse arguments and run ``build_library``."""
    parser = argparse.ArgumentParser(description="Build consolidated research library")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root",
    )
    parser.add_argument(
        "--max-copy-mb",
        type=int,
        default=20,
        help="Maximum file size (MB) to copy into library",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    result = build_library(root=root, max_copy_mb=args.max_copy_mb)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
