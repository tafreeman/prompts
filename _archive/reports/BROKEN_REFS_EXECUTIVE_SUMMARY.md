# Broken References Fix Summary

**Analysis Date**: 2025-12-15  
**Total Broken References**: 118 out of 916 links

---

## 📊 Quick Stats

| Category | Count | Can Auto-Fix? | Priority |
|----------|-------|---------------|----------|
| **Directory renames** | ~20 | ✅ Yes | HIGH |
| **Path depth issues** | ~55 | ✅ Yes | HIGH |
| **File name variations** | ~10 | ✅ Yes | HIGH |
| **Files never existed** | ~35 | ❌ No (need decisions) | MEDIUM |
| **Placeholder references** | ~5 | ✅ Yes | LOW |

**TOTAL AUTO-FIXABLE**: ~85 out of 118 (72%)

---

## ✅ Git-Validated Directory Moves

These directories were renamed (confirmed via git history):

1. **`prompts/governance/` → `prompts/governance/`**
   - Affects: 5 broken references
   - Fix: Global replace in workflows

2. **`prompts/advanced/` → `prompts/advanced/`**
   - Affects: 3 broken references
   - Fix: Global replace in workflows

3. **`guides/domain-schemas.md` → `guides/domain-schemas.md`**
   - Affects: 1 broken reference
   - Fix: Update docs/README.md

---

## 🔧 Path Depth Corrections Needed

| Directory | Current Pattern | Should Be | Affected Files |
|-----------|----------------|-----------|----------------|
| `.agent\workflows\` | `../` | `../../` | 8 refs in coderev.md |
| `workflows\` | `../../prompts/` | `../prompts/` | ~45 refs across 3 files |
| `workflows\` | `../../CONTRIBUTING.md` | `../CONTRIBUTING.md` | 3 refs |
| `.github\agents\` | `../` | `../../` | 3 refs |
| `techniques\` | `../../CONTRIBUTING.md` | `../CONTRIBUTING.md` | 1 ref |

---

## 📝 File Name Corrections

Files that exist but are referenced with wrong names:

| Referenced As | Actually Named | Location |
|---------------|----------------|----------|
| documentation-generator.md | documentation-generator.md | prompts/developers/ |
| documentation-generator.md | documentation-generator.md | prompts/developers/ |
| sql-query-analyzer.md | sql-query-analyzer.md | prompts/developers/ |
| ai-ml-privacy-risk-assessment.md | ai-ml-privacy-risk-assessment.md | prompts/governance/ |
| vendor-security-review.md | vendor-security-review.md | prompts/governance/ |
| resource-allocation-optimizer.md | resource-allocation-optimizer.md | prompts/business/ |
| index.md | README.md | techniques/ |

---

## ⚠️ Files in Wrong Directory

| Referenced Path | Actual Path |
|-----------------|-------------|
| system/cloud-architecture-consultant.md | system/cloud-architecture-consultant.md |
| system/solution-architecture-designer.md | system/solution-architecture-designer.md |
| developers/devops-pipeline-architect.md | developers/devops-pipeline-architect.md |
| governance/security-code-auditor.md | developers/security-code-auditor.md |

---

## ❌ Files Never Created (Need Decisions)

### Business Prompts (4 files - MEDIUM priority)

- `financial-modeling-expert.md`
- `project-charter-creator.md`
- `sales-strategy-consultant.md`
- `marketing-campaign-strategist.md`

**Referenced by**: `workflows/business-planning.md`

### Developer Prompts (3 files - MEDIUM priority)

- `bug-finder.md`
- `database-migration-specialist.md`
- `refactoring-specialist.md` (maybe use `refactoring-plan-designer.md`?)

### OSINT/SOCMINT Suite (12 files - LOW priority, appears to be planned feature)

- `attribution-analysis.md`
- `threat-intelligence.md`
- `timeline-reconstruction.md`
- `domain-investigation.md`
- `email-investigation.md`
- `phone-investigation.md`
- `username-investigation.md`
- `instagram-osint.md`
- `telegram-osint.md`
- Various resource files

**Referenced by**: `docs/create-osint-library-prompt.md`

### Other (6 files - LOW priority)

- `cross-border-transfer-assessment.md` (governance)
- `business-planning-blueprint.md` (workflow)
- `incident-response-playbook.md` (workflow)
- `roi-calculator.md` (template)
- `related1.md` and `related2.md` (placeholders)

---

## 🚀 Recommended Action Plan

### IMMEDIATE (Can automate today)

**Script can fix: ~85 references automatically**

1. Run automated fix script for:
   - Directory renames (governance-compliance, advanced-techniques)
   - Path depth corrections (all workflow files)
   - File name variations (where target exists)
   - Wrong directory fixes

2. Test on a branch first
3. Re-run broken references checker
4. Validate fixes before merge

---

### SHORT TERM (This week)

**Decisions needed: ~35 references**

1. **Review business prompts** (4 files)
   - Decide: Create them or remove references?
   - If creating, prioritize which ones

2. **Review developer prompts** (3 files)
   - `bug-finder.md`: Create or remove?
   - `database-migration-specialist.md`: Create or remove?
   - `refactoring-specialist.md`: Use existing `refactoring-plan-designer.md`?

3. **Review workflow docs** (2 files)
   - Create blueprint/playbook files or remove refs?

---

### LONG TERM (Future)

**Defer: ~12 OSINT references**

1. OSINT/SOCMINT suite appears to be planned feature
2. Either:
   - Create stub files with "Coming soon"
   - Remove from `docs/create-osint-library-prompt.md`
   - Add to backlog for future development

---

## 📁 Deliverables Created

1. **`git_history_analysis.md`**
   - Full git history investigation
   - Documents what was moved vs never existed

2. **`proposed_fixes_with_git_validation.md`**
   - Comprehensive fix proposal
   - All categories with evidence
   - Implementation phases

3. **`proposed_fixes_summary.csv`**
   - Spreadsheet of all fixes
   - Sortable/filterable

4. **THIS FILE** - Executive summary

---

## 🎯 Success Metrics

After fixes applied:

- **Before**: 118 broken references
- **After immediate fixes**: ~33 broken references (72% reduction)
- **After short-term decisions**: 0-5 broken references (depends on create vs remove)

---

## 💡 Key Insights

1. **Most issues are simple path problems** (72% auto-fixable)
2. **Two major directory renames** caused many breaks
3. **~35 files were never created** - need stakeholder input
4. **OSINT suite** represents planned but unbuilt feature
5. **Some confusion** between system/ and developers/ directories

---

## 📋 Next Steps Checklist

- [ ] Review this summary with stakeholders
- [ ] Get decisions on "never existed" files (create vs remove)
- [ ] Create and test automated fix script
- [ ] Run fixes on feature branch
- [ ] Re-validate with link checker
- [ ] Merge if validation passes
- [ ] Document repository structure to prevent recurrence
- [ ] Update CONTRIBUTING.md with directory naming conventions

---

## Questions for Stakeholders

1. **Business prompts**: Should we create the 4 missing business prompts or remove the references?
2. **Developer prompts**: Same question for the 3 missing dev prompts
3. **OSINT suite**: Is this still planned? Should we create stubs or remove?
4. **Workflow docs**: Create blueprint/playbook files or remove references?
5. **Architecture files**: Confirm correct location (system/ vs developers/)
