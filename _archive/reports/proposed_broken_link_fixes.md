# Proposed Fixes for Broken References

This document contains proposed fixes for broken file references identified in the repository.

## Summary of Issues

The main patterns of broken links found:

1. **Agent files**: References pointing to `.agent\workflows\` instead of correct path
2. **Prompt files**: References using wrong relative paths (missing `prompts\` prefix)
3. **Missing documentation files**: References to files that need to be created or moved
4. **GitHub agent references**: Wrong path structure in `.github\agents\`

---

## Detailed Proposed Fixes

### 1. Agent Workflow References (`.agent\workflows\coderev.md`)

**Source File**: `.agent\workflows\coderev.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `../agents/code-review-agent.agent.md` | `../../agents/code-review-agent.agent.md` | Agent files are in `agents\` at root |
| `../prompts/developers/code-review-assistant.md` | `../../prompts/developers/code-review-assistant.md` | Needs extra `..` to reach root |
| `../prompts/developers/code-review-expert-structured.md` | `../../prompts/developers/code-review-expert-structured.md` | Needs extra `..` to reach root |
| `../prompts/developers/code-review-expert.md` | `../../prompts/developers/code-review-expert.md` | Needs extra `..` to reach root |
| `../prompts/developers/performance-optimization-specialist.md` | `../../prompts/developers/performance-optimization-specialist.md` | Needs extra `..` to reach root |
| `../prompts/developers/security-code-auditor.md` | `../../prompts/developers/security-code-auditor.md` | Needs extra `..` to reach root |
| `../prompts/developers/test-automation-engineer.md` | `../../prompts/developers/test-automation-engineer.md` | Needs extra `..` to reach root |
| `../techniques/agentic/single-agent/code-review-agent.md` | `../../techniques/agentic/single-agent/code-review-agent.md` | Needs extra `..` to reach root |

---

### 2. GitHub Agents References (`.github\agents\`)

**Source File**: `.github\agents\AGENTS_GUIDE.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `../CONTRIBUTING.md` | `../../CONTRIBUTING.md` | CONTRIBUTING.md is at root |
| `../docs/ultimate-prompting-guide.md` | `../../docs/ultimate-prompting-guide.md` | Needs extra `..` to reach root |

**Source File**: `.github\agents\README.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `../CONTRIBUTING.md` | `../../CONTRIBUTING.md` | CONTRIBUTING.md is at root |

**Source File**: `.github\agents\docs-ux-agent.agent.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `./related1.md` | **CREATE FILE** or remove reference | File doesn't exist - likely placeholder |
| `./related2.md` | **CREATE FILE** or remove reference | File doesn't exist - likely placeholder |

---

### 3. Documentation References (`docs\`)

**Source File**: `docs\README.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `../src/README.md` | **N/A - src is empty** | No web application exists yet |
| `../guides/domain-schemas.md` | `../guides/domain-schemas.md` | File exists in guides\ not docs\ |

**Source File**: `docs\create-osint-library-prompt.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `../resources/osint_tool_evaluation.md` | **CREATE FILE** or remove | Resource file doesn't exist |
| `analysis/attribution-analysis.md` | **CREATE FILE** in `prompts\socmint\` | OSINT prompts should be in socmint\ |
| `analysis/threat-intelligence.md` | **CREATE FILE** in `prompts\socmint\` | OSINT prompts should be in socmint\ |
| `analysis/timeline-reconstruction.md` | **CREATE FILE** in `prompts\socmint\` | OSINT prompts should be in socmint\ |
| `investigation/domain-investigation.md` | **CREATE FILE** in `prompts\socmint\` | OSINT prompts should be in socmint\ |
| `investigation/email-investigation.md` | **CREATE FILE** in `prompts\socmint\` | OSINT prompts should be in socmint\ |
| `investigation/phone-investigation.md` | **CREATE FILE** in `prompts\socmint\` | OSINT prompts should be in socmint\ |
| `investigation/username-investigation.md` | **CREATE FILE** in `prompts\socmint\` | OSINT prompts should be in socmint\ |
| `resources/osint_research_resources.md` | **CREATE FILE** in `resources\` | Resource file doesn't exist |
| `resources/osint_tool_evaluation.md` | **CREATE FILE** in `resources\` | Resource file doesn't exist |
| `socmint/instagram-osint.md` | **CREATE FILE** in `prompts\socmint\` | SOCMINT prompt doesn't exist |
| `../prompts/../prompts/../prompts/../prompts/../prompts/../prompts/socmint/socmint-investigator.md` | `../prompts/../prompts/../prompts/../prompts/../prompts/../prompts/../prompts/socmint/socmint-investigator.md` | File exists in prompts\socmint\ |
| `socmint/telegram-osint.md` | **CREATE FILE** in `prompts\socmint\` | SOCMINT prompt doesn't exist |
| `techniques/chain-of-thought-analysis.md` | **CREATE FILE** or remove | Template/example file |
| `techniques/react-knowledge-base.md` | **CREATE FILE** or remove | Template/example file |
| `../prompts/advanced/osint-research-react.md` | `../prompts/advanced/osint-research-react.md` | File exists as osint-research-react.md |

**Source File**: `docs\reports\FULL_EVALUATION_REPORT.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `TOT_EVALUATION_REPORT.md` | `../TOT_EVALUATION_REPORT.md` | File is in docs\ not docs\reports\ |
| `prompt-effectiveness-scoring-methodology.md` | `../prompt-effectiveness-scoring-methodology.md` | File is in docs\ not docs\reports\ |

---

### 4. Prompt References (`prompts\advanced\`)

**Source File**: `prompts\advanced\prompt-library-refactor-react.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `../../techniques/README.md` | `../../techniques/README.md` | index.md doesn't exist, should be README.md |

**Source File**: `prompts\developers\code-review-assistant.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `bug-finder.md` | **CREATE FILE** or remove | Related prompt doesn't exist |
| `documentation-generator.md` | `documentation-generator.md` | File exists as documentation-generator.md |

---

### 5. Governance References (`prompts\governance\`)

**Source File**: `prompts\governance\privacy-impact-assessment.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `ai-ml-privacy-risk-assessment.md` | `ai-ml-privacy-risk-assessment.md` | File exists with longer name |
| `cross-border-transfer-assessment.md` | **CREATE FILE** or remove | File doesn't exist |

**Source File**: `prompts\governance\soc2-audit-preparation.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `vendor-security-review.md` | `vendor-security-review.md` | File exists as vendor-security-review.md |

---

### 6. Techniques References (`techniques\README.md`)

**Source File**: `techniques\README.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `../../CONTRIBUTING.md` | `../CONTRIBUTING.md` | Only needs one `..` |

---

### 7. Templates References (`templates\prompt-improvement-template.md`)

**Source File**: `templates\prompt-improvement-template.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `../governance/risk-assessment.md` | `../prompts/governance/gdpr-compliance-assessment.md` | Closest match to risk assessment |
| `resource-allocation-optimizer.md` | `../prompts/business/resource-allocation-optimizer.md` | File exists with different name |
| `roi-calculator.md` | **CREATE FILE** or remove | File doesn't exist |

---

### 8. Workflow References

**Source File**: `workflows\business-planning.md`

All references in this file need to add `prompts\` to the path:

| Pattern | Fix |
|---------|-----|
| `../../prompts/analysis/*.md` | `../prompts/analysis/*.md` |
| `../../prompts/business/*.md` | `../prompts/business/*.md` |
| `../../prompts/creative/*.md` | `../prompts/creative/*.md` |

Missing files:

- `business-case-developer.md` ✅ EXISTS in `prompts\analysis\`
- `competitive-analysis-researcher.md` ✅ EXISTS in `prompts\analysis\`
- `consumer-behavior-researcher.md` ✅ EXISTS in `prompts\analysis\`
- `data-analysis-specialist.md` ✅ EXISTS in `prompts\analysis\`
- `market-research-analyst.md` ✅ EXISTS in `prompts\analysis\`
- `metrics-and-kpi-designer.md` ✅ EXISTS in `prompts\analysis\`
- `user-experience-analyst.md` ✅ EXISTS in `prompts\analysis\`
- `change-management-coordinator.md` ✅ EXISTS in `prompts\business\`
- `financial-modeling-expert.md` ❌ **DOESN'T EXIST** - needs creation
- `innovation-strategy-consultant.md` ✅ EXISTS in `prompts\business\`
- `project-charter-creator.md` ❌ **DOESN'T EXIST** - needs creation
- `sales-strategy-consultant.md` ❌ **DOESN'T EXIST** - needs creation
- `strategic-planning-consultant.md` ✅ EXISTS in `prompts\business\`
- `marketing-campaign-strategist.md` ❌ **DOESN'T EXIST** - needs creation
- `./sdlc.md` ❌ **DOESN'T EXIST** - needs creation

**Source File**: `workflows\data-pipeline.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `../prompts/advanced/chain-of-thought-debugging.md` | `../prompts/advanced/chain-of-thought-debugging.md` | Wrong directory name |
| `../prompts/advanced/chain-of-thought-performance-analysis.md` | `../prompts/advanced/chain-of-thought-performance-analysis.md` | Wrong directory name |
| `../prompts/advanced/reflection-data-pipeline-risk-review.md` | **CREATE FILE** or use `../prompts/advanced/reflection-self-critique.md` | Specific file doesn't exist |
| `../prompts/advanced/tree-of-thoughts-architecture-evaluator.md` | `../prompts/advanced/tree-of-thoughts-architecture-evaluator.md` | Wrong directory name |
| `../prompts/developers/sql-query-analyzer.md` | `../prompts/developers/sql-query-analyzer.md` | File exists with different name |

**Source File**: `workflows\incident-response.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `../../CONTRIBUTING.md` | `../CONTRIBUTING.md` | Wrong path depth |
| `../../prompts/analysis/data-analysis-insights.md` | `../prompts/analysis/data-analysis-insights.md` | Wrong path depth |
| `../../prompts/analysis/metrics-and-kpi-designer.md` | `../prompts/analysis/metrics-and-kpi-designer.md` | Wrong path depth |
| `../../prompts/business/crisis-management-coordinator.md` | `../prompts/business/crisis-management-coordinator.md` | Wrong path depth |
| `../../prompts/business/risk-management-analyst.md` | `../prompts/business/risk-management-analyst.md` | Wrong path depth |
| `../../prompts/developers/documentation-generator.md` | `../prompts/developers/documentation-generator.md` | File exists with different name |
| `../../prompts/governance/security-code-auditor.md` | `../prompts/developers/security-code-auditor.md` | Wrong directory |
| `../../prompts/governance/security-incident-response.md` | `../prompts/governance/security-incident-response.md` | Wrong directory name |

**Source File**: `workflows\sdlc.md`

| Broken Reference | Proposed Fix | Notes |
|-----------------|--------------|-------|
| `../../CONTRIBUTING.md` | `../CONTRIBUTING.md` | Wrong path depth |
| All `../../prompts/*` references | `../prompts/*` | Wrong path depth |
| `../../prompts/governance/*` | `../prompts/governance/*` | Wrong directory name |
| `../../prompts/developers/devops-pipeline-architect.md` | `../prompts/developers/devops-pipeline-architect.md` | Wrong directory |
| `./business-planning-blueprint.md` | **CREATE FILE** or remove | File doesn't exist |
| `./incident-response-playbook.md` | **CREATE FILE** or remove | File doesn't exist |

---

## Action Items by Category

### A. Path Depth Fixes (Simple corrections)

These are straightforward path fixes where the relative path depth is wrong:

1. **`.agent\workflows\coderev.md`**: Add one more `..` to all references
2. **`.github\agents\` files**: Add one more `..` to all references  
3. **`workflows\*.md` files**: Remove one `..` from all references
4. **`techniques\README.md`**: Remove one `..` from CONTRIBUTING.md reference

### B. Directory Name Fixes

Files exist but referenced with wrong directory names:

1. `advanced-techniques\` → `advanced\`
2. `governance-compliance\` → `governance\`
3. `system\devops-pipeline-architect.md` → `developers\devops-pipeline-architect.md`

### C. File Name Fixes  

Files exist but with different names:

1. `bug-finder.md` → `documentation-generator.md` or create new file
2. `documentation-generator.md` → `documentation-generator.md`
3. `sql-query-analyzer.md` → `sql-query-analyzer.md`
4. `ai-ml-privacy-risk-assessment.md` → `ai-ml-privacy-risk-assessment.md`
5. `vendor-security-review.md` → `vendor-security-review.md`
6. `resource-allocation-optimizer.md` → `resource-allocation-optimizer.md`
7. `index.md` → `README.md` (in techniques/)

### D. Files to Create

These files don't exist and need to be created:

**Business prompts:**

- `financial-modeling-expert.md`
- `project-charter-creator.md`
- `sales-strategy-consultant.md`
- `marketing-campaign-strategist.md`

**Governance prompts:**

- `cross-border-transfer-assessment.md`

**OSINT/SOCMINT prompts:**

- `attribution-analysis.md`
- `threat-intelligence.md`
- `timeline-reconstruction.md`
- `domain-investigation.md`
- `email-investigation.md`
- `phone-investigation.md`
- `username-investigation.md`
- `instagram-osint.md`
- `telegram-osint.md`

**Workflows:**

- `sdlc-blueprint.md`
- `business-planning-blueprint.md`
- `incident-response-playbook.md`

**Resources:**

- `osint_tool_evaluation.md`
- `osint_research_resources.md`

**Templates:**

- `roi-calculator.md`

**Other:**

- `domain-schemas.md` (exists in guides, may need to be referenced correctly)
- `related1.md` and `related2.md` in `.github\agents\` (or remove references)
- `reflection-data-pipeline-risk-review.md` (or use existing reflection prompt)

### E. Files to Remove/Update

Placeholder or example references that should be removed:

- References in `.github\agents\docs-ux-agent.agent.md` to `related1.md` and `related2.md`
- References to non-existent `src/README.md` until web app is created

---

## Priority Recommendations

### High Priority (Immediate Fix)

1. Fix all path depth issues in workflows (Category A)
2. Fix directory name issues (Category B)
3. Fix file name mismatches (Category C)

### Medium Priority

1. Create missing business prompt files (Category D)
2. Create missing workflow documentation files

### Low Priority

1. Create OSINT/SOCMINT prompt files (these appear to be planned features)
2. Create resource documentation files
3. Remove placeholder references

---

## Next Steps

1. **Automated Fix Script**: Create a script to automatically fix all Category A, B, and C issues
2. **File Creation**: Decide which missing files should be created vs. removed
3. **Re-validation**: Run the link checker again after fixes to verify all corrections
4. **Documentation**: Update any documentation that references these paths
