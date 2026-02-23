# Research Library

Role-driven consolidated research library generated from this repository.

## Subagent Roles
- `Scout`: discover and inventory research materials across the repo.
- `Curator`: consolidate non-code artifacts into a normalized library structure.
- `Engineer`: keep executable/code assets as references instead of duplicates.
- `Source Auditor`: extract and classify source URLs for reputation and safety.
- `Librarian`: publish searchable manifests and indexes.

## Outputs
- `research/library/artifacts/`: consolidated non-code research materials.
- `research/library/material_manifest.json`: file-level inventory and actions.
- `research/library/code_references.md`: code assets referenced for research.
- `research/library/source_registry.json`: URL/domain registry with trust status.
- `research/library/approved_domains.md`: suggested approved/caution/review domains.
- `research/library/reputable_sources.md`: approved URL-level source list.
- `research/subagents/*.md`: per-role execution reports.

## Current Snapshot
- Generated: `2026-02-22T21:42:38.902881+00:00`
- Materials indexed: `65`
- Documents copied: `43`
- Documents referenced: `0`
- Code references: `22`
- URLs extracted: `222`
- Approved URLs: `88`
- Caution URLs: `18`
- Review URLs: `116`

## Top Domains
- `arxiv.org`: 22
- `anthropic.com`: 21
- `support.claude.com`: 15
- `claude.ai`: 12
- `support.anthropic.com`: 12
- `docs.aws.amazon.com`: 10
- `developers.openai.com`: 9
- `docs.anthropic.com`: 7
- `learn.microsoft.com`: 7
- `researchgate.net`: 6
- `claude.com`: 6
- `docs.claude.com`: 6
- `facebook.com`: 6
- `docs.cloud.google.com`: 5
- `platform.claude.com`: 4
- `github.com`: 3
- `docs.python.org`: 3
- `stackoverflow.com`: 3
- `openreview.net`: 3
- `ibm.com`: 3

## Regenerate
- `python tools/research/build_library.py`
