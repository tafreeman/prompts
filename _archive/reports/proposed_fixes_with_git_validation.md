# Updated Proposed Fixes (With Git History Validation)

**Analysis Date**: 2025-12-15  
**Based on**: Git history analysis + Current broken references report

---

## Executive Summary

Based on git history analysis, the broken references fall into three categories:

1. **✅ Files that were moved/renamed** (~15-20 fixes) - Simple path updates needed
2. **❌ Files that never existed** (~35-40 issues) - Need creation or reference removal
3. **⚠️ Files with similar names** (~10 issues) - Name mismatches to reconcile

---

## Category 1: Directory Renames (CONFIRMED via Git History)

### A. `governance/` → `governance/`

**Git Evidence**: Files were bulk-renamed from `governance-compliance` to `governance`

**Affected Files**: All references to `governance/` should be `governance/`

| Source File | Current (Broken) | Correct Path | Priority |
|-------------|------------------|--------------|----------|
| workflows\incident-response.md | ../../prompts/governance/security-code-auditor.md | ../prompts/developers/security-code-auditor.md | **HIGH** |
| workflows\incident-response.md | ../../prompts/governance/security-incident-response.md | ../prompts/governance/security-incident-response.md | **HIGH** |
| workflows\sdlc.md | ../../prompts/governance/README.md | ../prompts/governance/README.md | **HIGH** |
| workflows\sdlc.md | ../../prompts/governance/security-code-auditor.md | ../prompts/developers/security-code-auditor.md | **HIGH** |
| workflows\sdlc.md | ../../prompts/governance/security-incident-response.md | ../prompts/governance/security-incident-response.md | **HIGH** |

**Note**: `security-code-auditor.md` is actually in `developers/` not `governance/`

### B. `advanced/` → `advanced/`

**Git Evidence**: Directory was renamed from `advanced-techniques` to `advanced`

**Affected Files**: All references to `advanced/` should be `advanced/`

| Source File | Current (Broken) | Correct Path | Priority |
|-------------|------------------|--------------|----------|
| workflows\data-pipeline.md | ../prompts/advanced/chain-of-thought-debugging.md | ../prompts/advanced/chain-of-thought-debugging.md | **HIGH** |
| workflows\data-pipeline.md | ../prompts/advanced/chain-of-thought-performance-analysis.md | ../prompts/advanced/chain-of-thought-performance-analysis.md | **HIGH** |
| workflows\data-pipeline.md | ../prompts/advanced/tree-of-thoughts-architecture-evaluator.md | ../prompts/advanced/tree-of-thoughts-architecture-evaluator.md | **HIGH** |

---

## Category 2: Specific File Moves (CONFIRMED via Git History)

### `guides/domain-schemas.md` → `guides/domain-schemas.md`

**Git Evidence**: `R100 guides/domain-schemas.md → guides/domain-schemas.md`

| Source File | Current (Broken) | Correct Path | Priority |
|-------------|------------------|--------------|----------|
| docs\README.md | ../guides/domain-schemas.md | ../guides/domain-schemas.md | **HIGH** |

### `docs/workflows/sdlc-blueprint.md` → `workflows/sdlc.md`

**Git Evidence**: File was moved and renamed

| Source File | Current (Broken) | Correct Path | Priority |
|-------------|------------------|--------------|----------|
| workflows\business-planning.md | ./sdlc.md | ./sdlc.md | **HIGH** |

---

## Category 3: Path Depth Issues (Simple Corrections)

These need one `..` added or removed based on git repository structure:

### Files in `.agent\workflows\` (Need extra `..`)

| Source File | Pattern | Fix |
|-------------|---------|-----|
| .agent\workflows\coderev.md | `../` → `../../` | Add one more `..` to all 8 references |

### Files in `workflows\` (Need one less `..`)

| Source File | Pattern | Fix |
|-------------|---------|-----|
| workflows\business-planning.md | `../../prompts/` → `../prompts/` | Remove one `..` from all references |
| workflows\incident-response.md | `../../prompts/` → `../prompts/` | Remove one `..` from all references |
| workflows\incident-response.md | `../../CONTRIBUTING.md` → `../CONTRIBUTING.md` | Remove one `..` |
| workflows\sdlc.md | `../../prompts/` → `../prompts/` | Remove one `..` from all references |
| workflows\sdlc.md | `../../CONTRIBUTING.md` → `../CONTRIBUTING.md` | Remove one `..` |

### Files in `.github\agents\` (Need extra `..`)

| Source File | Pattern | Fix |
|-------------|---------|-----|
| .github\agents\AGENTS_GUIDE.md | `../` → `../../` | Add one more `..` (2 references) |
| .github\agents\README.md | `../CONTRIBUTING.md` → `../../CONTRIBUTING.md` | Add one more `..` |

### Files in `techniques\`

| Source File | Current (Broken) | Correct Path |
|-------------|------------------|--------------|
| techniques\README.md | ../../CONTRIBUTING.md | ../CONTRIBUTING.md |

---

## Category 4: File Name Variations (Files exist with different names)

**Git Evidence**: These files were NOT found in git history with the referenced names

### Developer Files

| Broken Reference | Actual File Name | Source File | Priority |
|------------------|------------------|-------------|----------|
| documentation-generator.md | documentation-generator.md | prompts\developers\code-review-assistant.md | **HIGH** |
| documentation-generator.md | documentation-generator.md | workflows\incident-response.md | **HIGH** |
| sql-query-analyzer.md | sql-query-analyzer.md | workflows\data-pipeline.md | **HIGH** |

### Governance Files

| Broken Reference | Actual File Name | Source File | Priority |
|------------------|------------------|-------------|----------|
| ai-ml-privacy-risk-assessment.md | ai-ml-privacy-risk-assessment.md | prompts\governance\privacy-impact-assessment.md | **HIGH** |
| vendor-security-review.md | vendor-security-review.md | prompts\governance\soc2-audit-preparation.md | **HIGH** |

### Business Files

| Broken Reference | Actual File Name | Source File | Priority |
|------------------|------------------|-------------|----------|
| resource-allocation-optimizer.md | resource-allocation-optimizer.md | templates\prompt-improvement-template.md | **HIGH** |

### Techniques Files

| Broken Reference | Actual File Name | Source File | Priority |
|------------------|------------------|-------------|----------|
| ../../techniques/README.md | ../../techniques/README.md | prompts\advanced\prompt-library-refactor-react.md | **HIGH** |

---

## Category 5: Files in Wrong Directory (Files exist elsewhere)

**Git Evidence**: These files exist but are referenced from wrong directories

### Architecture Files (system vs developers confusion)

| Referenced As | Actual Location | Source File | Priority |
|---------------|-----------------|-------------|----------|
| ../../prompts/system/cloud-architecture-consultant.md | prompts/system/cloud-architecture-consultant.md | workflows\sdlc.md | **HIGH** |
| ../../prompts/system/solution-architecture-designer.md | prompts/system/solution-architecture-designer.md | workflows\sdlc.md | **HIGH** |
| ../../prompts/developers/devops-pipeline-architect.md | prompts/developers/devops-pipeline-architect.md | workflows\sdlc.md | **HIGH** |

### Security Files

| Referenced As | Actual Location | Note |
|---------------|-----------------|------|
| governance/security-code-auditor.md | developers/security-code-auditor.md | In developers, not governance |
| governance/security-incident-response.md | governance/security-incident-response.md | governance (not governance-compliance) |

---

## Category 6: Files NEVER Existed (Need Decision)

**Git Evidence**: NO history found for these files - they were never created

### Business Prompts (Never Created)

These referenced files were **never in git**:

- `financial-modeling-expert.md` - Referenced by: workflows\business-planning.md
- `project-charter-creator.md` - Referenced by: workflows\business-planning.md  
- `sales-strategy-consultant.md` - Referenced by: workflows\business-planning.md
- `marketing-campaign-strategist.md` - Referenced by: workflows\business-planning.md

**Decision Needed**: Create these files or remove references?

### Developer Prompts (Never Created)

- `bug-finder.md` - Referenced by: prompts\developers\code-review-assistant.md
- `database-migration-specialist.md` - Referenced by: workflows\sdlc.md
- `refactoring-specialist.md` - Referenced by: workflows\sdlc.md (might be `refactoring-plan-designer.md`)

**Decision Needed**: Create or use closest match?

### Governance Prompts (Never Created)

- `cross-border-transfer-assessment.md` - Referenced by: prompts\governance\privacy-impact-assessment.md

**Decision Needed**: Create this file or remove reference?

### OSINT/SOCMINT Prompts (Never Created)

All referenced from `docs\create-osint-library-prompt.md`:

- `analysis/attribution-analysis.md`
- `analysis/threat-intelligence.md`
- `analysis/timeline-reconstruction.md`
- `investigation/domain-investigation.md`
- `investigation/email-investigation.md`
- `investigation/phone-investigation.md`
- `investigation/username-investigation.md`
- `socmint/instagram-osint.md`
- `socmint/telegram-osint.md`
- `resources/osint_tool_evaluation.md`
- `resources/osint_research_resources.md`

**Decision Needed**: These appear to be a planned feature set. Create or defer?

### Workflow Documentation (Never Created)

- `business-planning-blueprint.md` - Referenced by: workflows\sdlc.md
- `incident-response-playbook.md` - Referenced by: workflows\sdlc.md

**Decision Needed**: Create or remove references?

### Other Missing Files

- `roi-calculator.md` - Referenced by: templates\prompt-improvement-template.md
- Related placeholder files in `.github\agents\`:
  - `related1.md` - Referenced by: .github\agents\docs-ux-agent.agent.md
  - `related2.md` - Referenced by: .github\agents\docs-ux-agent.agent.md

**Decision Needed**: Remove placeholder references

### Special Case: Data Pipeline Reflection

- `reflection-data-pipeline-risk-review.md` - Never existed
  - **Recommendation**: Use existing `reflection-self-critique.md` instead

---

## Implementation Plan

### Phase 1: Automated Fixes (HIGH PRIORITY - Can script)

**Total: ~75 fixes**

1. **Directory renames** (global replace):
   - Replace `governance/` with `governance/`
   - Replace `advanced/` with `advanced/`

2. **Path depth corrections**:
   - `.agent\workflows\coderev.md`: Add `..` to 8 references
   - All `workflows\*.md`: Remove one `..` from all prompts references
   - `.github\agents\*.md`: Add `..` to references

3. **Specific file moves**:
   - `guides/domain-schemas.md` → `guides/domain-schemas.md`
   - `./sdlc.md` → `./sdlc.md`

4. **File name corrections**:
   - All the "File Name Variations" from Category 4

5. **Wrong directory fixes**:
   - System vs developers architecture files
   - Security file locations

### Phase 2: Content Review (MEDIUM PRIORITY - Need decisions)

**Total: ~35-40 references**

1. **Business prompts** (4 files): Create or remove?
2. **Developer prompts** (3 files): Create or use alternatives?
3. **Governance prompts** (1 file): Create or remove?
4. **OSINT/SOCMINT** (12 files): Create as planned feature or defer?
5. **Workflows** (2 files): Create or remove?

### Phase 3: Cleanup (LOW PRIORITY)

**Total: ~5 references**

1. Remove placeholder references (`related1.md`, `related2.md`)
2. Remove or defer references to unimplemented features
3. Update documentation about repository structure

---

## Automated Fix Script Recommendations

### High-Confidence Fixes (Safe to automate)

1. All path depth corrections
2. All directory rename fixes (governance-compliance, advanced-techniques)
3. All proven file moves from git history
4. All file name variations where target file exists

### Review Before Apply

1. Files in wrong directories (verify logic)
2. Any files that need directory structure decisions

### Manual Review Required

1. All "never existed" files - need stakeholder decision
2. Placeholder removals - verify they're truly not needed

---

## Next Actions

1. ✅ **Review this analysis** - Confirm the categorization makes sense
2. **Create automated fix script** - For Phase 1 only (high confidence)
3. **Stakeholder review** - For Phase 2 decisions (create vs remove)
4. **Execute fixes** - Run script with backup/branch
5. **Re-validate** - Run link checker again
6. **Document** - Update repo structure docs to prevent recurrence

---

## Files Created

1. `proposed_broken_link_fixes.md` - Original analysis
2. `proposed_fixes_summary.csv` - Quick reference CSV  
3. `git_history_analysis.md` - Git history investigation
4. `THIS FILE` - Updated fixes with git validation
