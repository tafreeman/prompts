# Candidate Files for Removal or Archiving

The following files have been identified as potentially orphaned, outdated, irrelevant, or redundant within the `tafreeman/prompts` repository.

> **Last Reviewed:** 2025-12-16  
> **Note:** Some files previously listed here were verified as valuable and removed from this list.

## 1. Temporary & Log Files

These files appear to be artifacts from previous executions, tests, or debugging sessions.

| File Path | Reason | Action |
|-----------|--------|--------|
| `test_run_20251125_083036.log` | Old test run log. | DELETE |
| `test_run_20251125_095501.log` | Old test run log. | DELETE |
| `test_run_20251125_095526.log` | Old test run log. | DELETE |
| `fix_output.txt` | Temporary output from a fix script. | DELETE |
| `fix_output2.txt` | Temporary output from a fix script. | DELETE |
| `chat cove.txt` | Likely a chat log export. | DELETE |
| `chat.json` | Large JSON file (10MB), likely a chat history. | DELETE |
| `sorcexy.7z` | Large archive file (50MB), likely a backup transfer. | DELETE or move to external storage |
| `validation_report.txt` | Old report artifact. | DELETE |
| `flowchart TD.mmd` | Mermaid diagram file in root (misplaced). | MOVE to `docs/diagrams/` |

## 2. Legacy Reports & Summaries

These files appear to be static reports generated in the past and may no longer be relevant.

| File Path | Reason | Action |
|-----------|--------|--------|
| `audit_report.csv` | Old audit result. | ARCHIVE or DELETE |
| `broken_references_report.csv` | Report on broken links. | ARCHIVE or DELETE |
| `proposed_fixes_summary.csv` | Summary of proposed fixes. | ARCHIVE or DELETE |
| `BROKEN_REFS_EXECUTIVE_SUMMARY.md` | Executive summary report. | ARCHIVE |
| `CODE_REVIEW_STANDARDIZATION_SUMMARY.md` | Summary report. | ARCHIVE |
| `FINAL_REPORT.md` | Generic report file. | ARCHIVE |
| `FIXES_APPLIED_SUMMARY.md` | Fix summary. | ARCHIVE |
| `Fixing Python Formatting.md` | Log/report of formatting fixes. | ARCHIVE |
| `git_history_analysis.md` | One-off analysis document. | ARCHIVE |
| `proposed_broken_link_fixes.md` | Proposal document. | ARCHIVE |
| `proposed_fixes_with_git_validation.md` | Proposal document. | ARCHIVE |

## 3. One-off / Utility Scripts

These scripts in the `scripts/` root or `tools/` directory seem to be for one-time maintenance tasks.

| File Path | Reason | Action |
|-----------|--------|--------|
| `fix_formatting.py` | Root level script for formatting fixes. | ARCHIVE |
| `scripts/fix_archive_refs.py` | One-time fix script. | ARCHIVE |
| `scripts/fix_broken_references.py` | One-time fix script. | ARCHIVE |
| `scripts/fix_frontmatter.py` | One-time fix script. | ARCHIVE |
| `scripts/generate_broken_refs_report.py` | Reporting script. | ARCHIVE |
| `scripts/add_platform.py` | Utility. | ARCHIVE |
| `scripts/check_platform.py` | Utility. | ARCHIVE |

---

## ❌ Files Previously Listed - VERIFIED AS VALUABLE (DO NOT REMOVE)

The following files were previously flagged for removal but have been verified as valuable:

| File Path | Actual Purpose | Status |
|-----------|----------------|--------|
| `CoVE Reflexion Prompt Library Evaluation.md` | 596-line research document on CoVe methodology with citations and benchmarks. | **MOVED** to `docs/research/` |
| `tools/evaluate_library.py` | 1181-line dual-rubric evaluation system (QualityScore + EffectivenessScore). | **KEEP** - Production tool |
| `tools/batch_evaluate.py` | 718-line batch evaluation with frontmatter updates. | **KEEP** - Complements tiered_eval |
| `tools/audit_prompts.py` | 186-line CSV report generator for library health. | **KEEP** - Useful utility |
| `tools/tests_README.md` | Documentation for the 38-test evaluation agent test suite. | **KEEP** - Test docs |
| `tools/test_llm_connection.py` | 43-line quick connection tester for LLM providers. | **KEEP** - Debugging utility |
| `tools/test_generator.py` | 28-line test for UniversalCodeGenerator. | **KEEP** - Test file |
| `tools/check_links.py` | Link checker utility. | **KEEP** - Useful for maintenance |
| `tools/validate_prompts.py` | Basic validation script. | **KEEP** - Part of validation pipeline |

---

## Recommendation

1. **Delete**: Safely delete the "Temporary & Log Files" listed above.
2. **Archive**: Move "Legacy Reports" and "One-off Scripts" to the `_archive/` directory.
3. **Move**: Move misplaced files (like `flowchart TD.mmd`) to appropriate directories.
