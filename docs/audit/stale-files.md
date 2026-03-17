# Stale Files Audit

**Date:** 2026-03-17
**Auditor:** Claude Code (automated)
**Scope:** Dead directories, unused files, duplicated content, temp file contamination

---

## Findings Summary

| # | Severity | Finding | Files Affected | Recoverable Space |
|---|----------|---------|----------------|-------------------|
| SF-1 | HIGH | Retired `.agent/` directory | 5 files | Minimal |
| SF-2 | HIGH | 6 unused persona prompts | 6 `.md` files | Minimal |
| SF-3 | MEDIUM | Research library artifacts (old snapshot) | 23 `.md` files | ~50 KB |
| SF-4 | MEDIUM | Triple-duplicated eval docs | 21 files (7 x 3) | ~100 KB |
| SF-5 | MEDIUM | Presentation temp/lock files committed | ~8 files | ~260 KB |
| SF-6 | MEDIUM | Verbose `.gitignore` for `.playwright-cli/` | 43 entries | N/A |
| SF-7 | LOW | PDF copies alongside markdown sources | ~5 PDFs | ~2.3 MB |

**Total recoverable:** ~2.7 MB of binary blobs and duplicated content.

---

## Detailed Findings

### SF-1: Retired `.agent/` Directory (HIGH)

**Path:** `.agent/` (5 files)

| File | Purpose |
|------|---------|
| `.agent/rules/run.md` | Old agent run rules |
| `.agent/workflows/coderev.md` | Code review workflow |
| `.agent/workflows/generate-prompt.md` | Prompt generation workflow |
| `.agent/workflows/improve-prompt.md` | Prompt improvement workflow |
| `.agent/workflows/repo-documenter.md` | Repo documentation workflow |

This directory was the predecessor to `.claude/` and has been fully replaced. The `.claude/README.md` confirms the migration. No code references `.agent/` paths.

**Action:** Delete the entire `.agent/` directory.

### SF-2: Possibly Unused Persona Prompts (HIGH)

**Path:** `agentic-workflows-v2/agentic_v2/prompts/`

6 persona prompt files may be unused:

| File | Referenced in `agents.yaml`? | Referenced in workflow YAML? | Referenced in code? |
|------|-----------------------------|-----------------------------|---------------------|
| `developer.md` | Yes (stale entry) | No | No |
| `linter.md` | Yes (stale entry) | No | No |
| `summarizer.md` | Yes (stale entry) | No | No |
| `validator.md` | Yes (stale entry) | No | No |
| `analyzer.md` | Yes (stale entry) | No | No |
| `assembler.md` | Yes (stale entry) | No | No |

**Caveat:** The agent system supports tier-based lookup where agent names are resolved dynamically. If any runtime code constructs persona file paths from user input or config, these files could be loaded without static references. A thorough grep is needed to confirm.

**Action:** Grep for dynamic path construction patterns. If confirmed unused, delete the files and remove corresponding `agents.yaml` entries.

### SF-3: Research Library Artifacts -- Old Snapshot (MEDIUM)

**Path:** `research/library/artifacts/` (23 markdown files)

This directory contains markdown files that mirror the main project's directory structure. The content appears to be a snapshot created by a research subagent during an early exploration phase. File modification dates suggest they have not been updated since initial creation.

Sample files:
- `research/library/artifacts/agentic-workflows-v2/README.md`
- `research/library/artifacts/tools/llm/README.md`
- `research/library/artifacts/docs/adr/ADR-001.md`

These duplicate content that exists at the canonical paths and will drift further out of date over time.

**Action:** Delete `research/library/artifacts/`. If any unique analysis content exists, move it to `docs/analysis/` first.

### SF-4: Triple-Duplicated Eval Documentation (MEDIUM)

**Path:** Three copies of the deep research plan series:

| Location | Status |
|----------|--------|
| `agentic-v2-eval/docs/deep_research_plan_series/` (7 files) | **Canonical** |
| `agentic-v2-eval/.gitignored/deep_research_plan_series/` (7 files) | Duplicate |
| `research/library/artifacts/agentic-v2-eval/docs/deep_research_plan_series/` (7 files) | Duplicate |

The `.gitignored/` copy appears to be a backup made before a reorganization. The `research/library/artifacts/` copy is part of the old snapshot (SF-3).

**Action:** Keep the `docs/` version. Delete the other two copies.

### SF-5: Presentation Temp and Lock Files Committed (MEDIUM)

**Path:** `presentation/`

The following files should never have been committed:

| File | Type | Size |
|------|------|------|
| `~$practitioners-playbook.pptx` | Excel/PPT lock file | ~1 KB |
| `~$team-onboarding-deck.pptx` | Excel/PPT lock file | ~1 KB |
| `transfer-test.txt` | Test artifact | ~1 KB |
| `onb_b64_part1.txt` | Base64 dump | ~50 KB |
| `genai_advocacy_hub_10.jsx` | Old monolith version | ~103 KB |
| `genai_advocacy_hub_10_v2.0.jsx` | Old monolith version | ~130 KB |
| `*.zip` | Archive | ~28 KB |

**Action:**
1. Delete all listed files
2. Add to `.gitignore`:
   ```
   presentation/~$*
   presentation/*.zip
   presentation/transfer-test.txt
   ```

### SF-6: Verbose `.gitignore` for `.playwright-cli/` (MEDIUM)

**Path:** Root `.gitignore`

The `.gitignore` file contains 43 individual filename entries for `.playwright-cli/` artifacts instead of a single glob pattern. This is brittle -- any new Playwright artifact will not be ignored until manually added.

**Current (43 lines):**
```
.playwright-cli/chromium-1234/
.playwright-cli/firefox-5678/
.playwright-cli/webkit-9012/
# ... 40 more
```

**Recommended (1 line):**
```
.playwright-cli/
```

**Action:** Replace all 43 entries with a single `.playwright-cli/` glob.

### SF-7: PDF Copies Alongside Markdown Sources (LOW)

**Path:** `docs/`

Several PDF files exist alongside their markdown source equivalents:

| PDF File | Markdown Source | Size |
|----------|----------------|------|
| `docs/Architecture-Analysis.pdf` | `docs/Architecture-Analysis.md` | ~800 KB |
| `docs/adr/ADR-002-*.pdf` | `docs/adr/ADR-002-*.md` | ~500 KB |
| `docs/adr/ADR-003-*.pdf` | `docs/adr/ADR-003-*.md` | ~500 KB |
| Others | Various | ~500 KB |

PDFs are binary blobs that inflate repository size and create merge conflicts. Since the markdown sources are the canonical versions, the PDFs are redundant for anyone with a markdown renderer.

**Action:** Delete the PDF files. If PDF distribution is needed, generate them in CI with `pandoc` or similar. Alternatively, use Git LFS for the PDFs.

---

## Quick Wins

| Action | Effort | Impact |
|--------|--------|--------|
| Delete `.agent/` directory | 2 min | Remove retired system |
| Delete presentation temp files + update `.gitignore` | 5 min | Remove committed junk |
| Replace 43 `.gitignore` entries with `.playwright-cli/` glob | 5 min | Maintainability |
| Delete duplicate eval docs (2 copies) | 5 min | Remove confusion |
| Delete `research/library/artifacts/` | 5 min | Remove stale snapshot |

---

## Totals

- **~70+ stale or duplicated files** identified
- **~2.7 MB recoverable** (primarily PDFs and large JSX artifacts)
- **All quick wins achievable in under 30 minutes**
