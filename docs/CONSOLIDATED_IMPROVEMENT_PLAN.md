# 📋 Consolidated Repository Improvement Plan

**Created:** December 4, 2025  
**Status:** Active  
**Replaces:** Multiple scattered planning documents

---

## Executive Summary

This document consolidates findings from 6+ separate reports into a single actionable plan. It tracks what's been completed vs. what remains, with clear priorities.

### Source Documents Analyzed

| Document | Key Findings | Status |
|----------|--------------|--------|
| `ARCHITECTURE_PLAN.md` | Tooling consolidation, eval architecture | Partially done |
| `COMPLEXITY_AND_ADOPTION_REPORT.md` | 15 adoption barriers identified | ~60% addressed |
| `VISUAL_AUDIT_REPORT.md` | 226 formatting issues | ~10% addressed |
| `VISUAL_FORMATTING_AUDIT_REPORT.md` | 50 broken links, missing sections | ~20% addressed |
| `IMPLEMENTATION_TRACKING.md` | Phase 1 eval improvements | ✅ Complete |
| `PROMPT_WEB_APP_ARCHITECTURE.md` | Webapp design | Not started |

---

## ✅ COMPLETED (Don't Repeat)

### Evaluation Tooling (Phase 1) ✅
- [x] `dual_eval.py` is the primary evaluation tool
- [x] Batch/folder evaluation (`discover_prompt_files()`)
- [x] JSON output format (`--format json`)
- [x] Changed-only mode for CI/CD (`--changed-only`)
- [x] Smart file filtering (excludes agents, instructions, README)
- [x] 116 unit tests passing (66 eval + 50 validators)
- [x] CI workflow exists (`.github/workflows/prompt-validation.yml`)

### Repository Cleanup ✅
- [x] Deprecated tools archived to `tools/archive/`
  - `evaluation_agent.py`, `evaluate_library.py`, `improve_prompts.py`
  - `generate_eval_files.py`, `run_gh_eval.py`
- [x] Stale docs archived to `docs/archive/2025-12-04/`
  - `REFACTOR_TODO.md`, `IMPROVEMENT_PLAN.md`, `PHASED_EVALUATION_PLAN.md`
  - `EVALUATION_REPORT.md`, `TOT_EVALUATION_REPORT.md`
  - `COMPLEXITY_AND_ADOPTION_REPORT.md`, `VISUAL_AUDIT_REPORT.md`, `VISUAL_FORMATTING_AUDIT_REPORT.md`
- [x] Legacy testing framework archived to `testing/archive/2025-12-04/`
  - `testing/framework/` (13 files - unused complex framework)
  - `developers-eval-*.yml` files (old manual eval configs)
  - `*-report*.md` files (old manual eval reports)
  - `test_cli.py` (broken test for non-existent module)
  - `example_test_suite.yaml` (for archived framework)

### Documentation Fixes ✅
- [x] `docs/getting-started.md` - Now exists
- [x] `docs/best-practices.md` - Now exists
- [x] `docs/advanced-techniques.md` - Now exists
- [x] `docs/intro-to-prompts.md` - Now exists

### Testing Infrastructure ✅
- [x] `testing/conftest.py` - Shared fixtures
- [x] `testing/validators/` - Schema validation tests
- [x] `testing/evals/README.md` - Updated documentation

---

## 🔴 CRITICAL (Do First)

### 1. Fix Broken Internal Links (50 links)
**Source:** VISUAL_AUDIT_REPORT.md  
**Effort:** 2 hours  
**Impact:** Navigation completely broken for users

Files with broken "Related Prompts" links:
```
prompts/advanced/chain-of-thought-*.md
prompts/advanced/rag-*.md
prompts/advanced/react-*.md
prompts/advanced/reflection-*.md
prompts/advanced/tree-of-thoughts-*.md
prompts/analysis/competitive-intelligence-researcher.md
prompts/business/agile-sprint-planner.md
prompts/business/budget-and-cost-controller.md
```

**Action:** Run link checker, then either:
1. Create missing referenced files
2. Update links to existing equivalents
3. Remove broken links

### 2. Fix README Architecture Mismatch
**Source:** COMPLEXITY_AND_ADOPTION_REPORT.md  
**Effort:** 30 minutes  
**Impact:** Misleads users about available features

README.md describes components that don't exist:
- `src/app.py` (Flask application) - ❌ Doesn't exist
- `src/templates/` - ❌ Doesn't exist
- `deployment/` directory - ❌ Doesn't exist

**Action:** Update README to remove references to non-existent components, or mark webapp as "Planned".

---

## 🟠 HIGH PRIORITY (Do This Week)

### 4. Standardize Prompt Section Order
**Source:** VISUAL_FORMATTING_AUDIT_REPORT.md  
**Effort:** 2 hours  
**Files:** ~20 prompts

Standard order should be:
1. Description (not "Purpose" or "Overview")
2. Use Cases (optional)
3. Prompt
4. Variables
5. Example Usage
6. Tips
7. Related Prompts

Files using non-standard sections:
- `prompts/developers/api-design-consultant.md` - Uses "Purpose"
- `prompts/developers/code-review-expert.md` - Uses "Purpose"
- `prompts/m365/*.md` - Various non-standard orders

### 5. Add Language Specifiers to Code Blocks
**Source:** VISUAL_AUDIT_REPORT.md  
**Effort:** 1 hour  
**Files:** 40+ code blocks

```markdown
# Change from:
```
SELECT * FROM users
```

# To:
```sql
SELECT * FROM users
```
```

### 6. Add Missing Standard Sections
**Source:** VISUAL_FORMATTING_AUDIT_REPORT.md  
**Effort:** 2 hours  
**Files:** 19 prompts

| File | Missing |
|------|---------|
| `prompts/advanced/library.md` | Description, Variables, Example, Tips |
| `prompts/advanced/chain-of-thought-guide.md` | Variables, Tips |
| `prompts/analysis/library-*.md` | Variables, Tips |
| `prompts/system/example-research-output.md` | Description, Prompt, Variables |

### 7. Create Simplified Quick Start Template
**Source:** COMPLEXITY_AND_ADOPTION_REPORT.md  
**Effort:** 1 hour  
**Impact:** Current 17-section template intimidates contributors

Create `templates/prompt-template-minimal.md` with only:
1. Title + minimal frontmatter
2. Description
3. Prompt
4. Variables
5. Example

---

## 🟡 MEDIUM PRIORITY (Do This Month)

### 8. Add Table Alignment Specifiers
**Source:** VISUAL_AUDIT_REPORT.md  
**Effort:** 1 hour  
**Files:** ~89 files

```markdown
# Change from:
| Column | Data |
| --- | --- |

# To:
| Column | Data |
|:-------|-----:|
```

### 9. Add Collapsible Sections for Large Tables
**Source:** VISUAL_AUDIT_REPORT.md  
**Effort:** 1 hour  
**Files:** Tables with 15+ rows

```html
<details>
<summary><b>View all 36 items</b></summary>

| ... table content ... |

</details>
```

### 10. Run Full Library Evaluation
**Source:** ARCHITECTURE_PLAN.md  
**Effort:** Variable (depends on API rate limits)

```bash
python testing/evals/dual_eval.py prompts/ \
  --format json \
  --output docs/EVALUATION_REPORT.json \
  --runs 1 \
  --models openai/gpt-4o-mini
```

Generate new `docs/EVALUATION_REPORT.md` with current scores.

### 11. Flatten Deep Directory Structure
**Source:** COMPLEXITY_AND_ADOPTION_REPORT.md  
**Effort:** 2 hours  
**Impact:** 76 directories make navigation confusing

Consider merging:
- `techniques/reflexion/` → `prompts/advanced/`
- `techniques/context-optimization/` → `prompts/advanced/`

### 12. Add Mermaid Diagrams to Complex Prompts
**Source:** VISUAL_AUDIT_REPORT.md  
**Effort:** 2 hours  
**Files:** 4 prompts

| File | Diagram Type |
|------|--------------|
| `prompts/advanced/react-*.md` | flowchart (Thought→Action→Observation) |
| `prompts/advanced/tree-of-thoughts-*.md` | graph (branch structure) |

---

## 🟢 LOW PRIORITY (Nice to Have)

### 13. Add Shields.io Badges to Key Files
**Effort:** 30 minutes  
**Files:** README.md, governance prompts, advanced prompts

### 14. Standardize Emoji Usage in Headers
**Effort:** 1 hour  
**Convention:**
- 📋 Description
- 🎯 Use Cases
- 💡 Tips
- ⚙️ Variables

### 15. Add Input/Output Separation in Examples
**Effort:** 2 hours  
**Files:** 32 prompts

```markdown
## Example Usage

### Input
```text
[Example with variables replaced]
```

### Output
```text
[Expected response]
```
```

---

## 🔮 FUTURE (Webapp - Not Started)

From `PROMPT_WEB_APP_ARCHITECTURE.md`:

### Phase 1: Foundation
- [ ] Create Azure resource group
- [ ] Provision Cosmos DB (serverless)
- [ ] Setup Azure Static Web App
- [ ] Create Git→Cosmos sync script

### Phase 2: Core App
- [ ] Build Next.js gallery view
- [ ] Implement prompt detail page
- [ ] Add variable form generation
- [ ] Deploy to Azure SWA

### Phase 3: AI Features
- [ ] Integrate Azure OpenAI
- [ ] Add "Ask the Architect" chat
- [ ] Implement prompt refinement suggestions

---

## Documents to Archive

These documents are now superseded by this consolidated plan:

| Document | Action |
|----------|--------|
| `docs/COMPLEXITY_AND_ADOPTION_REPORT.md` | Archive after extracting remaining items |
| `docs/VISUAL_AUDIT_REPORT.md` | Archive after extracting remaining items |
| `docs/VISUAL_FORMATTING_AUDIT_REPORT.md` | Archive after extracting remaining items |
| `testing/evals/IMPLEMENTATION_TRACKING.md` | Keep as reference for completed work |

---

## Progress Tracking

| Priority | Total Items | Completed | Remaining |
|----------|-------------|-----------|-----------|
| ✅ Done | 15 | 15 | 0 |
| 🔴 Critical | 3 | 0 | 3 |
| 🟠 High | 4 | 0 | 4 |
| 🟡 Medium | 5 | 0 | 5 |
| 🟢 Low | 3 | 0 | 3 |
| 🔮 Future | 9 | 0 | 9 |

**Next Actions:**
1. Fix broken internal links (Critical #1)
2. Update README to remove non-existent architecture (Critical #2)
3. Fix test collection errors (Critical #3)

---

*Last Updated: December 4, 2025*
