# Archive Reference (Detailed)

**Generated**: 2025-12-19  
**Files Analyzed**: 38 files across 4 subdirectories  
**Recommendation Summary**: 0 RESTORE, 2 REVIEW, 36 ARCHIVE

---

## Summary

The `_archive/` directory contains deprecated files that have been superseded by current implementations. This analysis examines each file to determine:

1. What capability it provided
2. Whether that capability still exists in the current codebase
3. If restoring is recommended

---

## Directory Structure

```
_archive/
├── reports/     # 10 files - Historical analysis outputs
├── scripts/     # 6 files  - Python utilities (some unique!)
├── testing/     # 18 files - Legacy test artifacts
└── tools/       # 6 files  - Old evaluation agent + exports
```

---

## `_archive/scripts/` (6 files)

### Comparison with Current Tools

| Archived File | Lines | Current Equivalent | Capability Preserved? |
|--------------|-------|-------------------|----------------------|
| `fix_broken_references.py` | 482 | `tools/check_links.py` | ⚠️ **PARTIAL** - Current lacks WIP stub creation |
| `fix_frontmatter.py` | 607 | `tools/normalize_frontmatter.py` | ✅ **YES** - Current is equivalent |
| `generate_broken_refs_report.py` | 162 | `tools/check_links.py` | ✅ **YES** - Current has CSV export |
| `fix_archive_refs.py` | 188 | `tools/check_links.py` | ✅ **YES** - Path replacement handled |
| `add_platform.py` | ~80 | `tools/normalize_frontmatter.py` | ✅ **YES** - Frontmatter normalization |
| `check_platform.py` | ~70 | `tools/validate_prompts.py` | ✅ **YES** - Validation checks |

---

### Detailed File Analysis

#### `fix_broken_references.py` (482 lines) ⚠️ REVIEW

**Purpose**: Comprehensive broken reference fixer with WIP stub file creation.

**Unique Features NOT in Current Tools**:

1. **WIP stub file creation** - Creates placeholder prompts for missing files
2. **MISSING_FILES dictionary** - Pre-defined list of expected files with metadata
3. **PATH_REPLACEMENTS** - Directory renames and specific file renames
4. **FILE_SPECIFIC_FIXES** - Per-file complex replacements

**Capability Assessment**:

- The `tools/check_links.py` can FIND broken links
- But cannot CREATE stub files for missing prompts
- This script's stub creation is useful for migrations

**Recommendation**: **REVIEW** - Consider restoring WIP stub creation feature to `tools/check_links.py`

---

#### `fix_frontmatter.py` (607 lines) ✅ KEEP ARCHIVED

**Purpose**: Automated frontmatter fixing with inference logic.

**Features**:

- `extract_frontmatter()` - Parse YAML from markdown
- `infer_short_title()` - Generate shortTitle from title
- `infer_intro()` - Generate intro from description
- `infer_type_from_content()` - Detect document type
- `infer_difficulty()` - Normalize difficulty levels
- `normalize_audience()` - Validate audience values
- `infer_audiences()` - Category-based audience inference
- `infer_platforms()` - Platform detection
- `infer_governance_tags()` - Tag inference
- `serialize_frontmatter()` - Ordered YAML output

**Current Equivalent**: `tools/normalize_frontmatter.py` (~400 lines)

**Capability Assessment**: ✅ All features present in current tool.

---

#### `generate_broken_refs_report.py` (162 lines) ✅ KEEP ARCHIVED

**Purpose**: CSV report generator for broken references.

**Features**:

- Scans all markdown files
- Validates file references
- Categorizes: OK, BROKEN, FIXABLE, SKIP, ERROR
- Generates CSV report

**Current Equivalent**: `tools/check_links.py` has similar reporting.

---

#### `fix_archive_refs.py` (188 lines) ✅ KEEP ARCHIVED

**Purpose**: Fixes references to old archive paths.

**Path Mappings**:

```python
PATH_REPLACEMENTS = {
    "tools/archive/": "_archive/tools/",
    "testing/archive/": "_archive/testing/",
}
```

**Status**: One-time migration script. Not needed anymore.

---

#### `add_platform.py` (~80 lines) ✅ KEEP ARCHIVED

**Purpose**: Add platform fields to frontmatter.

**Status**: Functionality in `normalize_frontmatter.py`.

---

#### `check_platform.py` (~70 lines) ✅ KEEP ARCHIVED

**Purpose**: Validate platform fields.

**Status**: Functionality in `validate_prompts.py`.

---

## `_archive/tools/` (6 files)

### File-by-File Analysis

| File | Size | Description | Current Equivalent |
|------|------|-------------|-------------------|
| `evaluation_agent.py` | 38 KB (1112 lines) | Old autonomous agent | `tools/evaluation_agent.py` |
| `EVALUATION_AGENT_GUIDE.md` | 7 KB | Old documentation | `tools/README.md` |
| `EVALUATION_AGENT_GUIDE.html` | 16 KB | HTML export | N/A (not needed) |
| `EVALUATION_AGENT_GUIDE.pdf` | 64 KB | PDF export | N/A (not needed) |
| `EVALUATION_AGENT_GUIDE.png` | 339 KB | Image export | N/A (not needed) |
| `EVALUATION_AGENT_GUIDE.jpeg` | 780 KB | Image export | N/A (not needed) |

---

#### `evaluation_agent.py` (Archive) vs Current

**Archived Version (1112 lines)**:

```python
# Key classes/functions:
- AgentConfig - Central configuration
- TaskStatus - Status enum
- TaskResult - Task execution result
- CategoryResult - Category evaluation result
- AgentState - Persistent checkpoint state
- setup_logging() - Logging configuration
- save_checkpoint() / load_checkpoint() - Resume capability
- run_command() - Shell command execution with retry
- check_prerequisites() - Tool availability check
- count_prompts_in_category() - Prompt counting
- generate_eval_files() - Eval file generation
- run_evaluations() - Parallel evaluation execution
- parse_evaluation_results() - Result parsing
- generate_improvement_plan() - Improvement recommendations
```

**Current Version** (`tools/evaluation_agent.py`, 1118 lines):

- Same structure and capabilities
- Slightly newer with bug fixes

**Status**: ✅ Current is equal or better. Keep archived for reference.

---

## `_archive/testing/` (18 files)

### `_archive/testing/2025-12-04/` (Dated Snapshot)

Contains a snapshot of testing artifacts from December 4, 2025.

| File | Size | Purpose |
|------|------|---------|
| `developers-eval-1.prompt.yml` | 17 KB | Eval file v1 |
| `developers-eval-2.prompt.yml` | 25 KB | Eval file v2 |
| `developers-eval-3.prompt.yml` | 14 KB | Eval file v3 |
| `developers-eval.prompt.yml` | 17 KB | Main eval file |
| `developers-full-report.md` | 7 KB | Full evaluation report |
| `developers-improved-report.md` | 6 KB | Improved report |
| `developers-report-v2.md` | 5 KB | Report v2 |
| `developers-report.md` | 2 KB | Initial report |
| `example_test_suite.yaml` | 5 KB | Test suite template |
| `prompt-quality-eval.prompt.yml` | 4 KB | Quality eval template |
| `single-prompt-eval.prompt.yml` | 4 KB | Single prompt eval |
| `test_cli.py` | 4 KB | CLI tests |
| `framework/` | 6 files | Old framework components |

**Status**: Historical artifacts. Keep for reference but not needed for operations.

---

## `_archive/reports/` (10 files)

Historical analysis and fix reports.

| File | Size | Created For |
|------|------|-------------|
| `BROKEN_REFS_EXECUTIVE_SUMMARY.md` | 7 KB | Broken link analysis |
| `CODE_REVIEW_STANDARDIZATION_SUMMARY.md` | 9 KB | Code standards |
| `FINAL_REPORT.md` | 9 KB | Migration completion |
| `FIXES_APPLIED_SUMMARY.md` | 7 KB | Applied fixes |
| `Fixing Python Formatting.md` | 92 KB | Python formatting fixes |
| `broken_references_report.csv` | 107 KB | Raw broken links data |
| `git_history_analysis.md` | 6 KB | Git history research |
| `proposed_broken_link_fixes.md` | 16 KB | Proposed fixes |
| `proposed_fixes_summary.csv` | 14 KB | Fix summary data |
| `proposed_fixes_with_git_validation.md` | 13 KB | Validated fixes |

**Status**: Historical records. Keep for audit trail.

---

## Capability Gap Analysis

| Capability | Archived | Current | Gap? |
|------------|----------|---------|------|
| Broken link detection | `fix_broken_references.py` | `tools/check_links.py` | ❌ No |
| WIP stub creation | `fix_broken_references.py` | **MISSING** | ⚠️ **YES** |
| Frontmatter fix | `fix_frontmatter.py` | `tools/normalize_frontmatter.py` | ❌ No |
| CSV reporting | `generate_broken_refs_report.py` | `tools/check_links.py` | ❌ No |
| Path migration | `fix_archive_refs.py` | N/A (one-time) | ❌ No |
| Evaluation agent | `evaluation_agent.py` | `tools/evaluation_agent.py` | ❌ No |

---

## Recommendations

### Restore Feature (1)

| Feature | From | To | Priority |
|---------|------|-----|----------|
| WIP stub file creation | `_archive/scripts/fix_broken_references.py` | `tools/check_links.py` | Low |

**Rationale**: Creating placeholder prompts for missing files is useful during migrations. Could be added as `--create-stubs` flag to `check_links.py`.

### Keep Archived (37)

All other files serve historical/reference purposes only.

### Safe to Delete (0)

All files have value for audit trail or future reference.

---

## Quick Reference

| If you need... | Use this instead of archive |
|----------------|----------------------------|
| Fix frontmatter | `tools/normalize_frontmatter.py` |
| Check links | `tools/check_links.py` |
| Validate prompts | `tools/validate_prompts.py` |
| Evaluation agent | `tools/evaluation_agent.py` |
| Historical reports | Keep in `_archive/reports/` |
