# Docs Reference

**Generated**: 2025-12-19  
**Files Analyzed**: 45 files across 5 subdirectories  
**Recommendation Summary**: 25 KEEP, 12 CONSOLIDATE, 8 ARCHIVE

---

## Summary

The `docs/` directory contains documentation, reports, guides, and evaluation outputs for the prompt library. It includes both actively maintained guides and historical reports that may be outdated.

---

## Directory Structure

```
docs/
├── Root files (40)     # Guides, reports, reference docs
├── archive/            # Archived planning docs (18 files)
├── evaluations/        # Evaluation outputs (2 files)
├── research/           # Research reports (5 files)
├── reports/            # Generated reports
└── .github/            # GitHub-specific config
```

---

## Tooling Documentation (Active)

These files document the tools and should be kept in sync with the codebase.

| File | Size | Tool/System Documented | Status |
|------|------|------------------------|--------|
| **UNIFIED_TOOLING_GUIDE.md** | 8 KB | `prompt.py` CLI | ✅ KEEP - Current |
| **CLI_TOOLS.md** | 0.4 KB | CLI reference | ⚠️ CONSOLIDATE - Stub file |
| **prompt-authorship-guide.md** | 6 KB | Prompt writing standards | ✅ KEEP |
| **prompt-effectiveness-scoring-methodology.md** | 8 KB | Scoring rubrics | ✅ KEEP |
| **ARCHITECTURE_PLAN.md** | 18 KB | Tool architecture | ✅ KEEP |

---

## Generated Reference Docs (New)

Created during this session to document tool directories.

| File | Covers | Status |
|------|--------|--------|
| **tools-reference.md** | 23 Python tools | ✅ KEEP |
| **toolkit-reference.md** | 15 toolkit files | ✅ KEEP |
| **agents-reference.md** | 13 agent files | ✅ KEEP |
| **testing-reference.md** | 37 test files | ✅ KEEP |
| **frameworks-reference.md** | 13 framework files | ✅ KEEP |
| **app-reference.md** | Web app architecture | ✅ KEEP |
| **archive-reference.md** | Deprecated files | ✅ KEEP |

---

## User Guides

| File | Size | Purpose | Status |
|------|------|---------|--------|
| **README.md** | 8 KB | Docs landing page | ✅ KEEP |
| **getting-started.md** | 8 KB | Onboarding guide | ✅ KEEP |
| **intro-to-prompts.md** | 9 KB | Prompt concepts | ✅ KEEP |
| **best-practices.md** | 10 KB | Best practices | ✅ KEEP |
| **advanced-techniques.md** | 13 KB | Advanced patterns | ✅ KEEP |
| **ultimate-prompting-guide.md** | 25 KB | Comprehensive guide | ⚠️ CONSOLIDATE with advanced-techniques |
| **platform-specific-templates.md** | 20 KB | Platform-specific | ✅ KEEP |

---

## Evaluation Reports

| File | Size | Purpose | Status |
|------|------|---------|--------|
| **EVALUATION_REPORT.md** | 14 KB | Evaluation findings | 📁 ARCHIVE - Historical |
| **EVALUATION_EXECUTION_PLAN.md** | 8 KB | Eval workflow | ✅ KEEP |
| **SCORECARD.md** | 34 KB | Prompt scorecard | ⚠️ UPDATE - May be stale |
| **TOT_COMPREHENSIVE_REPOSITORY_EVALUATION.md** | 55 KB | ToT evaluation | 📁 ARCHIVE - Historical |
| **TOT_EVALUATION_REPORT.md** | 24 KB | ToT results | 📁 ARCHIVE - Historical |

---

## Improvement Plans

| File | Size | Purpose | Status |
|------|------|---------|--------|
| **CONSOLIDATED_IMPROVEMENT_PLAN.md** | 39 KB | Master improvement plan | ⚠️ UPDATE - Check currency |
| **IMPROVEMENT_PROMPTS.md** | 65 KB | Improvement prompts | ✅ KEEP |
| **WORKSTREAM_A_COMPLETION_REPORT.md** | 16 KB | Workstream A report | 📁 ARCHIVE |
| **WORKSTREAM_A_UX_UI.md** | 12 KB | UX/UI improvements | 📁 ARCHIVE |
| **WORKSTREAM_B_CONTENT.md** | 12 KB | Content improvements | 📁 ARCHIVE |

---

## Research (`docs/research/`)

| File | Size | Purpose | Status |
|------|------|---------|--------|
| **CoVE Reflexion Prompt Library Evaluation.md** | 26 KB | CoVe methodology | ✅ KEEP |
| **ResearchReport.md** | 21 KB | Research findings | ✅ KEEP |
| **R1_R2_RESEARCH_EXECUTION.md** | 16 KB | Research execution | ✅ KEEP |
| **CITATION_AND_GOVERNANCE_RESEARCH.md** | 9 KB | Governance research | ✅ KEEP |
| **flowchart LR.mmd** | 1 KB | Diagram | ✅ KEEP |

---

## Evaluations (`docs/evaluations/`)

| File | Size | Purpose | Status |
|------|------|---------|--------|
| **PROMPT_EVAL_advanced_claude-opus-4.5.md** | 10 KB | Claude prompt eval | 📁 ARCHIVE - Output |
| **REPO_EVAL_claude-opus-4.5.md** | 14 KB | Claude repo eval | 📁 ARCHIVE - Output |

---

## JSON/CSV Data Files

| File | Size | Purpose | Status |
|------|------|---------|--------|
| **cove_analysis_report.json** | 16 KB | CoVe output | 📁 ARCHIVE - Move to reports/ |
| **cove_analysis_report_2025-12-15.json** | 148 KB | CoVe output | 📁 ARCHIVE - Move to reports/ |
| **cove_analysis_report_local_2025-12-15.json** | 109 KB | CoVe output | 📁 ARCHIVE - Move to reports/ |

---

## Archive (`docs/archive/`)

Contains 18 files including dated snapshots and deprecated planning docs.

| Content | Count | Status |
|---------|-------|--------|
| `2025-12-04/` snapshots | 12 files | 📁 ARCHIVE |
| Planning docs | 6 files | 📁 ARCHIVE |

---

## Miscellaneous

| File | Size | Purpose | Status |
|------|------|---------|--------|
| **Untitled-2.md** | 11 KB | Unknown/temp file | ❌ DELETE |
| **analysis-results.md** | 12 KB | Analysis output | ⚠️ REVIEW |
| **create-osint-library-prompt.md** | 32 KB | OSINT prompt | ✅ KEEP |
| **osint_research_resources.md** | 14 KB | OSINT resources | ✅ KEEP |
| **osint_tool_evaluation_report.md** | 9 KB | OSINT eval | ✅ KEEP |

---

## Consolidation Recommendations

| Action | Files | Rationale |
|--------|-------|-----------|
| **CONSOLIDATE** | `CLI_TOOLS.md` → `UNIFIED_TOOLING_GUIDE.md` | CLI_TOOLS is a stub |
| **CONSOLIDATE** | `ultimate-prompting-guide.md` → `advanced-techniques.md` | Overlapping content |
| **ARCHIVE** | `TOT_*.md`, `WORKSTREAM_*.md` | Historical reports |
| **MOVE** | `cove_analysis_report*.json` → `reports/` | Output files |
| **DELETE** | `Untitled-2.md` | Temp file |
| **UPDATE** | `SCORECARD.md`, `CONSOLIDATED_IMPROVEMENT_PLAN.md` | Verify currency |

---

## Documentation Gaps

| Gap | Current State | Recommendation |
|-----|---------------|----------------|
| No index of all docs | Individual files | Create `docs/INDEX.md` |
| Outdated scorecard | May be stale | Re-run evaluation |
| JSON outputs in root | Cluttered | Move to `reports/` |
| No changelog | Missing | Create `docs/CHANGELOG.md` |

---

## Workflow Map

```
User Guides:
  getting-started.md → intro-to-prompts.md → best-practices.md → advanced-techniques.md

Tooling Docs:
  UNIFIED_TOOLING_GUIDE.md → ARCHITECTURE_PLAN.md → [reference docs]

Research:
  research/CoVE Reflexion*.md → toolkit/prompts/evaluation/*
```
