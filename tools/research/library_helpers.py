"""Private helpers, dataclasses, and constants for build_library.py.

This module contains the internal building blocks used by ``build_library``:
constants (file-extension sets, domain lists, seed paths), dataclasses
(``MaterialRecord``, ``UrlRecord``), and all private helper functions.
Nothing in this module is intended for direct external use, but the
public-facing names are re-exported from ``build_library`` for backward
compatibility.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

URL_PATTERN = re.compile(r"https?://[^\s\"'<>`]+")

TEXT_EXTS = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".html",
    ".htm",
    ".log",
    ".csv",
    ".rst",
}

DOC_EXTS = TEXT_EXTS | {".pdf", ".docx"}

CODE_EXTS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".ps1",
    ".sh",
    ".go",
    ".rs",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".sql",
}

ASSET_URL_SUFFIXES = (
    ".js",
    ".css",
    ".map",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".eot",
    ".mp4",
    ".webm",
    ".mov",
)

RESEARCH_KEYWORDS = {
    "research",
    "report",
    "analysis",
    "bakeoff",
    "benchmark",
    "findings",
    "evidence",
    "literature",
    "reference",
    "review",
    "adr",
    "migration_plan",
    "deep_research",
}

SEED_PREFIXES = [
    Path("research"),
    Path("reports"),
    Path("agentic-v2-eval/docs/deep_research_plan_series"),
    Path("agentic-workflows-v2/docs/reports"),
    Path("agentic-workflows-v2/docs/adr"),
]

SEED_FILES = {
    Path("REFACTORING_PLAN.md"),
    Path("REVIEW.md"),
    Path("folder_report.txt"),
    Path("directory_analysis.log"),
    Path("system.md"),
}

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    ".venv-wsl",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".next",
    ".cache",
    "dist",
    "build",
    "runs",
    ".run-logs",
}

APPROVED_DOMAINS = {
    "arxiv.org",
    "openai.com",
    "developers.openai.com",
    "platform.openai.com",
    "learn.microsoft.com",
    "microsoft.com",
    "docs.python.org",
    "python.org",
    "fastapi.tiangolo.com",
    "pydantic.dev",
    "postgresql.org",
    "github.com",
    "docs.github.com",
    "langchain.com",
    "langchain-ai.github.io",
    "docs.langchain.com",
    "dl.acm.org",
    "ieeexplore.ieee.org",
    "pypi.org",
    "w3.org",
    "ietf.org",
    "nist.gov",
    "owasp.org",
    "mozilla.org",
    "developer.mozilla.org",
    "cloud.google.com",
    "docs.cloud.google.com",
    "aws.amazon.com",
    "docs.aws.amazon.com",
    "cloudflare.com",
    "developers.cloudflare.com",
    "anthropic.com",
    "docs.anthropic.com",
    "support.anthropic.com",
    "claude.ai",
    "claude.com",
    "docs.claude.com",
    "support.claude.com",
    "platform.claude.com",
}

APPROVED_SUFFIXES = (
    ".gov",
    ".edu",
    ".mil",
    ".ac.uk",
)

CAUTION_DOMAINS = {
    "reddit.com",
    "medium.com",
    "x.com",
    "twitter.com",
    "facebook.com",
    "tiktok.com",
    "youtube.com",
    "substack.com",
    "blogspot.com",
    "stackoverflow.com",
    "researchgate.net",
    "en.wikipedia.org",
    "infoq.com",
}


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class MaterialRecord:
    """Represents a single scanned file and the action taken on it."""

    source_path: str
    category: str
    action: str
    destination_path: str | None
    size_bytes: int
    sha256: str | None
    reason: str


@dataclass
class UrlRecord:
    """Represents a URL extracted from a research artifact."""

    url: str
    domain: str
    status: str
    reason: str
    referenced_by: list[str]


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _sha256(path: Path) -> str:
    """Compute the SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _iter_files(root: Path) -> Iterable[Path]:
    """Yield every accessible file under *root*, skipping excluded directories."""
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)

        dirnames[:] = [
            d for d in dirnames if d not in EXCLUDED_DIRS and not d.startswith(".venv")
        ]

        if rel_dir.parts[:2] == ("research", "library"):
            dirnames[:] = []
            continue

        for name in filenames:
            path = Path(dirpath) / name
            try:
                if path.is_file():
                    yield path
            except OSError:
                # Skip broken links or inaccessible filesystem entries.
                continue


def _path_has_keyword(rel: Path) -> bool:
    """Return True if the POSIX path string contains a research keyword."""
    lowered = rel.as_posix().lower()
    return any(keyword in lowered for keyword in RESEARCH_KEYWORDS)


def _is_seed_match(rel: Path) -> bool:
    """Return True if *rel* is an explicit seed file or under a seed prefix."""
    if rel in SEED_FILES:
        return True
    return any(str(rel).startswith(str(prefix)) for prefix in SEED_PREFIXES)


def _is_research_material(rel: Path) -> bool:
    """Return True if the relative path should be treated as research material."""
    if rel.parts[:2] == ("research", "library"):
        return False
    if rel.parts[:2] == ("research", "subagents"):
        return False
    if rel.as_posix() == "research/README.md":
        return False
    if "site-packages" in rel.parts:
        return False
    if any(part.startswith(".") for part in rel.parts):
        return False
    if _is_seed_match(rel):
        return True
    return _path_has_keyword(rel)


def _normalize_domain(netloc: str) -> str:
    """Strip port, credentials, leading ``www.``, and trailing punctuation."""
    domain = netloc.split("@")[-1].split(":")[0].lower().strip()
    if domain.startswith("www."):
        domain = domain[4:]
    domain = domain.rstrip(".\\/'\"`")
    return domain


def _normalize_url(raw: str) -> str:
    """Strip trailing punctuation characters commonly appended to inline URLs."""
    return raw.rstrip(").,;:'\"\n\r\t\\")


def _is_valid_domain(domain: str) -> bool:
    """Return True if *domain* is a well-formed hostname."""
    if not domain:
        return False
    if domain == "localhost":
        return True
    if not re.fullmatch(r"[a-z0-9.-]+", domain):
        return False
    if "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
        return False
    labels = domain.split(".")
    for label in labels:
        if not label:
            return False
        if len(label) > 63:
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
    return True


def _is_asset_url(url: str) -> bool:
    """Return True if the URL path ends with a static-asset extension."""
    path = urlparse(url).path.lower()
    return path.endswith(ASSET_URL_SUFFIXES)


def _classify_domain(domain: str) -> tuple[str, str]:
    """Return ``(status, reason)`` for a domain name."""
    if not domain:
        return "review", "missing domain"
    if domain in {"localhost", "127.0.0.1"}:
        return "caution", "local/non-public host"
    if domain in APPROVED_DOMAINS or any(
        domain.endswith(sfx) for sfx in APPROVED_SUFFIXES
    ):
        return "approved", "known reputable/official source"
    if domain in CAUTION_DOMAINS:
        return "caution", "user-generated or social platform"
    return "review", "domain not yet in approved/caution lists"


def _read_for_urls(path: Path, limit_bytes: int = 4 * 1024 * 1024) -> str:
    """Read a file's text content for URL extraction.

    Text files are decoded as UTF-8; binary files are read up to
    *limit_bytes* and decoded with latin-1 (no errors).
    """
    suffix = path.suffix.lower()
    try:
        if suffix in TEXT_EXTS:
            return path.read_text(encoding="utf-8", errors="ignore")
        data = path.read_bytes()[:limit_bytes]
        return data.decode("latin-1", errors="ignore")
    except Exception:
        return ""


def _relative(path: Path, root: Path) -> str:
    """Return the POSIX-style path of *path* relative to *root*."""
    return path.relative_to(root).as_posix()
