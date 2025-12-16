# Git History Analysis of Missing Files

This document contains findings from analyzing git history to determine if "missing" files ever existed in the repository.

## Analysis Date

2025-12-15

## Key Findings

### 1. Files That Were Moved/Renamed ✅

Based on git history analysis, the following files were renamed or moved:

#### A. Directory Renames

**`prompts/governance/` → `prompts/governance/`**

- All files in this directory were moved from `governance-compliance` to `governance`
- This explains broken references like `governance/security-code-auditor.md`
- **Status**: Files exist, just need path updates

**`prompts/advanced/` → `prompts/advanced/`**

- Advanced prompts directory was renamed
- This explains broken references to `advanced/`
- **Status**: Files exist, just need path updates

#### B. Specific File Moves

**`guides/domain-schemas.md` → `guides/domain-schemas.md`**

- File was moved from docs to guides directory
- Git log shows: `R100 guides/domain-schemas.md → guides/domain-schemas.md`
- **Status**: File exists in guides/, references need updating

**`docs/workflows/sdlc-blueprint.md` → `workflows/sdlc.md`**

- Workflow file was moved and renamed
- **Status**: File exists as workflows/sdlc.md

### 2. Files Never in Git History ❌

The following files were **never** found in git history and appear to be referenced but never created:

#### Business Prompts

- `financial-modeling-expert.md` - Never existed
- `project-charter-creator.md` - Never existed
- `sales-strategy-consultant.md` - Never existed
- `marketing-campaign-strategist.md` - Never existed

#### Developer Prompts

- `bug-finder.md` - Never existed
- `documentation-generator.md` - Might be `documentation-generator.md`
- `documentation-generator.md` - Likely `documentation-generator.md`
- `database-migration-specialist.md` - Never existed
- `refactoring-specialist.md` - Likely `refactoring-plan-designer.md`
- `sql-query-analyzer.md` - Likely `sql-query-analyzer.md`

#### Governance Prompts

- `cross-border-transfer-assessment.md` - Never existed
- `ai-ml-privacy-risk-assessment.md` - Likely `ai-ml-privacy-risk-assessment.md`
- `vendor-security-review.md` - Likely `vendor-security-review.md`

#### OSINT/SOCMINT Prompts

- `attribution-analysis.md` - Never existed
- `threat-intelligence.md` - Never existed
- `timeline-reconstruction.md` - Never existed
- `domain-investigation.md` - Never existed
- `email-investigation.md` - Never existed (though `email-osint-investigation.md` exists)
- `phone-investigation.md` - Never existed
- `username-investigation.md` - Never existed (though `username-pivot-investigation.md` exists)
- `instagram-osint.md` - Never existed
- `telegram-osint.md` - Never existed

#### Workflow Files

- `sdlc-blueprint.md` in workflows/ - Never existed (though workflows/sdlc.md exists)
- `business-planning-blueprint.md` - Never existed
- `incident-response-playbook.md` - Never existed

#### System/Architecture Files

- `cloud-architecture-consultant.md` in developers/ - Exists in `prompts/system/` not `developers/`
- `solution-architecture-designer.md` in developers/ - Exists in `prompts/system/` not `developers/`

#### Other Files

- `roi-calculator.md` - Never existed
- `resource-allocation-optimizer.md` - Likely `resource-allocation-optimizer.md`
- `related1.md` and `related2.md` in .github/agents/ - Never existed (placeholders)

### 3. Files in Wrong Directory

These files exist but are referenced from the wrong directory:

**Architecture/System Files**:

- `cloud-architecture-consultant.md` - Is in `prompts/system/` not `prompts/developers/`
- `devops-pipeline-architect.md` - Is in `prompts/developers/` not `prompts/system/`  
- `solution-architecture-designer.md` - Is in `prompts/system/` not `prompts/developers/`

**Security Files**:

- `security-code-auditor.md` - Is in `prompts/developers/` not `prompts/governance/`
- `security-incident-response.md` - Is in `prompts/governance/` not `prompts/governance/`

## Summary Statistics

### Files That Moved (Fix with path update): ~15-20 files

- governance/*→ governance/*
- advanced/*→ advanced/*
- guides/domain-schemas.md → guides/domain-schemas.md
- Various system/developer directory mix-ups

### Files Never Existed (Need creation or reference removal): ~35-40 files

- Business prompts: 4 files
- Developer prompts: 6 files
- Governance prompts: 3 files
- OSINT/SOCMINT prompts: 12 files
- Workflow files: 3 files
- Other: 5 files

### Files with Name Variations (Exist but different name): ~10 files

- Examples: `bug-finder` vs `documentation-generator`, `sql-query-optimizer-advanced` vs `sql-query-analyzer`

## Recommendations

### High Priority - Update Paths (Can be automated)

1. Replace all `governance/` with `governance/`
2. Replace all `advanced/` with `advanced/`
3. Replace `guides/domain-schemas.md` with `guides/domain-schemas.md`
4. Fix all workflow path depth issues (../../prompts → ../prompts)

### Medium Priority - Decide on Missing Files

For files that never existed, decide whether to:

1. **Create them** - If they represent planned features
2. **Remove references** - If they were ideas that won't be implemented
3. **Replace with closest match** - If similar files exist with different names

### Low Priority - Clean Up Placeholders

Remove references to obvious placeholder files like `related1.md`, `related2.md`

## Next Steps

1. **Use this analysis** to refine the proposed fixes document
2. **Create automated script** for High Priority path updates
3. **Review Medium Priority** files with stakeholders to decide on creation vs removal
4. **Document** the final repository structure to prevent future confusion
