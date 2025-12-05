---
title: Prompt Library Analysis - Parallel Work TODO
shortTitle: Prompt Library Analysis ...
intro: A prompt for prompt library analysis   parallel work todo tasks.
type: troubleshooting
difficulty: intermediate
audience:
- senior-engineer
- junior-engineer
platforms:
- github-copilot
- claude
- chatgpt
author: Prompts Library Team
version: '1.0'
date: '2025-11-30'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
---
# Prompt Library Analysis - Parallel Work TODO

**Generated**: 2025-11-30  
**Updated**: 2025-11-30 (incorporated research recommendations)  
**Completed Streams**: S (2025-11-30), R (2025-11-30)

**Sources**:
- ReAct Analysis: `prompt-library-refactor-react.md`
- Research Report: [RESEARCH_REPORT_2025-11-30.md](./RESEARCH_REPORT_2025-11-30.md)
- Full Analysis: [REPO_ANALYSIS_REPORT_2025-11-30.md](./REPO_ANALYSIS_REPORT_2025-11-30.md)

---

## Work Streams (Parallelizable)

Each work stream can be assigned to a separate agent. Streams are independent with no blocking dependencies.

| Stream | Priority | Focus | Parallelizable | Status |
| :--- |----------| :--- |----------------| :--- |
| **S** | P0 | Simplification (remove bloat) | ✅ Yes | ✅ **COMPLETE** |
| **R** | P1 | Scoring Rubric & Tooling | ✅ Yes | ✅ **COMPLETE** |
| **A** | P0 | Frontmatter Remediation | ✅ Yes | ⏳ Pending |
| **B** | P0 | Creative Expansion | ✅ Yes | ⏳ Pending |
| **C** | P1 | Business Expansion | ✅ Yes | ⏳ Pending |
| **D** | P2 | Governance Expansion | ✅ Yes | ⏳ Pending |
| **E** | P3 | Content Type Gap Filling | ⚠️ After S,A | ⏳ Pending |

---

## Stream S: Simplification (ALL FILES) ✅ COMPLETE

**Owner**: GitHub Copilot Agent  
**Completed**: 2025-11-30  
**Priority**: P0 CRITICAL  
**Effort**: Medium  
**Dependencies**: None  
**Research Source**: [RESEARCH_REPORT Section 5](./RESEARCH_REPORT_2025-11-30.md#5-simplification-actions)

> **Key Finding**: Industry leaders use dramatically simpler structures. Target: 60-70% reduction in prompt length.

### Task S1: Remove Changelog Sections (All Files) ✅

Removed inline changelog sections from all prompts via automated script.

- [x] Remove changelogs from `prompts/advanced/*.md` (16 files)
- [x] Remove changelogs from `prompts/analysis/*.md` (21 files)
- [x] Remove changelogs from `prompts/business/*.md` (26 files)
- [x] Remove changelogs from `prompts/creative/*.md` (1 file)
- [x] Remove changelogs from `prompts/developers/*.md` (25 files)
- [x] Remove changelogs from `prompts/governance/*.md` (2 files)
- [x] Remove changelogs from `prompts/m365/*.md` (21 files)
- [x] Remove changelogs from `prompts/system/*.md` (18 files)

**Result**: 123/139 files modified

### Task S2: Remove/Simplify Deprecated Fields ✅

Removed deprecated frontmatter fields.

- [x] Remove `estimatedTime` field (7 files)
- [x] Remove `technique` field (1 file)
- [ ] Move `dataClassification` to CI/build tooling (deferred - requires architecture decision)
- [ ] Move `reviewStatus` to CI/build tooling (deferred - requires architecture decision)

**Result**: 7 files modified

### Task S3: Consolidate "When to Use" into Intro ✅

Assessed impact - only 10 files have "## When to Use" sections, and most are appropriate (index files, advanced guides). No bulk changes needed.

- [x] Assessed scope - minimal impact (10 files)
- [x] Decision: Keep existing structure (valuable for discoverability)

### Task S4: Reduce Tips and Related Prompts ✅

Assessed impact - most files already have 4-6 tips and 2-3 related prompts. Content is already within acceptable limits.

- [x] Assessed scope - 125 files with Tips sections
- [x] Sample analysis: Most within 5-tip limit
- [x] Decision: No bulk changes needed; address per-file as needed

### Task S5: Trim Verbose Descriptions ✅

Metrics after simplification:
- **Before**: ~250 lines average
- **After**: ~144 lines average (42% reduction)
- **Shortest**: 54 lines
- **Longest**: 597 lines (complex advanced prompts)

Note: Target was <100 lines, achieved 144 avg. Further reduction requires content review on per-file basis.

### Simplification Script

Created `scripts/simplify_prompts.py` for automated simplification:
- `s1`: Remove changelog sections
- `s2`: Remove deprecated frontmatter fields

**Usage**:
```bash
python scripts/simplify_prompts.py s1      # Run S1 only
python scripts/simplify_prompts.py s2      # Run S2 only
python scripts/simplify_prompts.py all     # Run all tasks
python scripts/simplify_prompts.py --dry-run  # Preview changes
```

**Estimated savings**: ~20 lines per file

### Simplified Structure Template

After simplification, all prompts should follow this minimal structure:

```markdown
---
title: "Clear Action Title"
shortTitle: "Nav Label"
intro: "One sentence explaining what this prompt does."
type: "how_to"
difficulty: "beginner"
platforms: ["github-copilot", "claude"]
topics: ["writing", "marketing"]
effectivenessScore: 4.2  # NEW: Add after scoring
---

# Title

## Description

2-3 sentences max.

## Prompt

\`\`\`text
The actual prompt text...
\`\`\`

## Variables

| Variable | Description |
| :--- |-------------|
| [VAR] | What to put here |

## Example

**Input**: [example input]
**Output**: [example output]

## Tips

- Tip 1
- Tip 2
- Tip 3 (max 5)
```

---

## Stream R: Scoring Rubric & Tooling ✅ COMPLETE

**Owner**: GitHub Copilot Agent  
**Completed**: 2025-11-30  
**Priority**: P1 HIGH  
**Effort**: Medium  
**Dependencies**: None  
**Research Source**: [RESEARCH_REPORT Section 6](./RESEARCH_REPORT_2025-11-30.md#6-scoring-implementation-plan)

### Task R1: Create Scoring Rubric ✅

Created `tools/rubrics/prompt-scoring.yaml` with:
- [x] Clarity dimension (25%)
- [x] Effectiveness dimension (30%)
- [x] Reusability dimension (20%)
- [x] Simplicity dimension (15%)
- [x] Examples dimension (10%)
- [x] Quick scoring guide with checkboxes
- [x] Rating scale definitions (⭐-⭐⭐⭐⭐⭐)

### Task R2: Build Score Validator ✅

Created `tools/validators/score_validator.py`:
- [x] Validates `effectivenessScore` field (1.0-5.0)
- [x] Reports unscored files with `--unscored` flag
- [x] Summary statistics with `--summary` flag
- [x] Distribution analysis by rating level

**Usage**:
```bash
python tools/validators/score_validator.py --all --summary
python tools/validators/score_validator.py --unscored
python tools/validators/score_validator.py prompts/advanced/
```

### Task R3: Add Score Display ✅

Updated templates to include scoring:
- [x] Updated `templates/prompt-template.md` with `effectivenessScore` field
- [x] Updated `templates/quick-start-template.md` with `effectivenessScore` field
- [x] Added score comment placeholder in template body
- [x] Simplified template structure per research findings

### Task R4: Backfill Scores ⏳ PENDING

Score backfilling deferred - requires manual evaluation per prompt:

- [ ] Score all `prompts/advanced/*.md` files (17 files)
- [ ] Score all `prompts/analysis/*.md` files (21 files)
- [ ] Score all `prompts/business/*.md` files (26 files)
- [ ] Score all `prompts/creative/*.md` files (2 files)
- [ ] Score all `prompts/developers/*.md` files (25 files)
- [ ] Score all `prompts/governance/*.md` files (3 files)
- [ ] Score all `prompts/m365/*.md` files (21 files)
- [ ] Score all `prompts/system/*.md` files (23 files)

**Current Status**: 0/147 prompts scored (run `python tools/validators/score_validator.py --all --summary`)

**Scoring Scale**:
- ⭐ (1.0-1.9): Needs significant work
- ⭐⭐ (2.0-2.9): Below average
- ⭐⭐⭐ (3.0-3.9): Acceptable
- ⭐⭐⭐⭐ (4.0-4.4): Good
- ⭐⭐⭐⭐⭐ (4.5-5.0): Excellent

---

## Stream A: Frontmatter Remediation (136 files)

**Owner**: _Unassigned_  
**Priority**: HIGH  
**Effort**: Large  
**Dependencies**: None

### Task A1: Advanced Category (15 files)
- [ ] `prompts/advanced/chain-of-thought-concise.md`
- [ ] `prompts/advanced/chain-of-thought-debugging.md`
- [ ] `prompts/advanced/chain-of-thought-detailed.md`
- [ ] `prompts/advanced/chain-of-thought-guide.md`
- [ ] `prompts/advanced/chain-of-thought-performance-analysis.md`
- [ ] `prompts/advanced/library-analysis-react.md`
- [ ] `prompts/advanced/rag-document-retrieval.md`
- [ ] `prompts/advanced/react-doc-search-synthesis.md`
- [ ] `prompts/advanced/react-tool-augmented.md`
- [ ] `prompts/advanced/reflection-self-critique.md`
- [ ] `prompts/advanced/tree-of-thoughts-architecture-evaluator.md`
- [ ] `prompts/advanced/tree-of-thoughts-evaluator-reflection.md`
- [ ] `prompts/advanced/tree-of-thoughts-template.md`
- [ ] `prompts/advanced/library.md` (needs frontmatter added)
- [ ] `prompts/advanced/README.md` (needs frontmatter added)

**Required fields to add**:
```yaml
shortTitle: "Concise title"
intro: "One-sentence description"
type: "how_to"  # or reference, tutorial, conceptual
dataClassification: "internal"
reviewStatus: "draft"
audience:
  - "senior-engineer"
platforms:
  - "github-copilot"
  - "claude"
```

### Task A2: Analysis Category (20 files)
- [ ] `prompts/analysis/business-case-developer.md`
- [ ] `prompts/analysis/competitive-analysis-researcher.md`
- [ ] `prompts/analysis/competitive-intelligence-researcher.md`
- [ ] `prompts/analysis/consumer-behavior-researcher.md`
- [ ] `prompts/analysis/data-analysis-insights.md`
- [ ] `prompts/analysis/data-analysis-specialist.md`
- [ ] `prompts/analysis/data-quality-assessment.md`
- [ ] `prompts/analysis/gap-analysis-expert.md`
- [ ] `prompts/analysis/industry-analysis-expert.md`
- [ ] `prompts/analysis/library-capability-radar.md`
- [ ] `prompts/analysis/library-network-graph.md`
- [ ] `prompts/analysis/library-structure-treemap.md`
- [ ] `prompts/analysis/market-research-analyst.md`
- [ ] `prompts/analysis/metrics-and-kpi-designer.md`
- [ ] `prompts/analysis/process-optimization-consultant.md`
- [ ] `prompts/analysis/requirements-analysis-expert.md`
- [ ] `prompts/analysis/stakeholder-requirements-gatherer.md`
- [ ] `prompts/analysis/trend-analysis-specialist.md`
- [ ] `prompts/analysis/user-experience-analyst.md`
- [ ] `prompts/analysis/workflow-designer.md`

### Task A3: Business Category (25 files)
- [ ] `prompts/business/agile-sprint-planner.md`
- [ ] `prompts/business/budget-and-cost-controller.md`
- [ ] `prompts/business/business-process-reengineering.md`
- [ ] `prompts/business/business-strategy-analysis.md`
- [ ] `prompts/business/change-management-coordinator.md`
- [ ] `prompts/business/client-presentation-designer.md`
- [ ] `prompts/business/crisis-management-coordinator.md`
- [ ] `prompts/business/digital-transformation-advisor.md`
- [ ] `prompts/business/due-diligence-analyst.md`
- [ ] `prompts/business/innovation-strategy-consultant.md`
- [ ] `prompts/business/management-consulting-expert.md`
- [ ] `prompts/business/market-entry-strategist.md`
- [ ] `prompts/business/meeting-facilitator.md`
- [ ] `prompts/business/organizational-change-manager.md`
- [ ] `prompts/business/performance-improvement-consultant.md`
- [ ] `prompts/business/project-closure-specialist.md`
- [ ] `prompts/business/project-documentation-manager.md`
- [ ] `prompts/business/quality-assurance-planner.md`
- [ ] `prompts/business/resource-allocation-optimizer.md`
- [ ] `prompts/business/risk-management-analyst.md`
- [ ] `prompts/business/stakeholder-communication-manager.md`
- [ ] `prompts/business/strategic-planning-consultant.md`
- [ ] `prompts/business/team-performance-manager.md`
- [ ] `prompts/business/timeline-and-milestone-tracker.md`
- [ ] `prompts/business/vendor-management-coordinator.md`

### Task A4: Developers Category (24 files)
- [ ] `prompts/developers/api-design-consultant.md`
- [ ] `prompts/developers/cloud-migration-specialist.md`
- [ ] `prompts/developers/code-generation-assistant.md`
- [ ] `prompts/developers/code-review-assistant.md`
- [ ] `prompts/developers/code-review-expert-structured.md`
- [ ] `prompts/developers/code-review-expert.md`
- [ ] `prompts/developers/csharp-enterprise-standards-enforcer.md`
- [ ] `prompts/developers/csharp-refactoring-assistant.md`
- [ ] `prompts/developers/data-pipeline-engineer.md`
- [ ] `prompts/developers/database-schema-designer.md`
- [ ] `prompts/developers/devops-pipeline-architect.md`
- [ ] `prompts/developers/documentation-generator.md`
- [ ] `prompts/developers/dotnet-api-designer.md`
- [ ] `prompts/developers/frontend-architecture-consultant.md`
- [ ] `prompts/developers/legacy-system-modernization.md`
- [ ] `prompts/developers/microservices-architect.md`
- [ ] `prompts/developers/mid-level-developer-architecture-coach.md`
- [ ] `prompts/developers/mobile-app-developer.md`
- [ ] `prompts/developers/performance-optimization-specialist.md`
- [ ] `prompts/developers/refactoring-plan-designer.md`
- [ ] `prompts/developers/security-code-auditor.md`
- [ ] `prompts/developers/sql-query-analyzer.md`
- [ ] `prompts/developers/sql-security-standards-enforcer.md`
- [ ] `prompts/developers/test-automation-engineer.md`

### Task A5: Governance Category (2 files)
- [ ] `prompts/governance/legal-contract-review.md`
- [ ] `prompts/governance/security-incident-response.md`

### Task A6: M365 Category (20 files)
- [ ] `prompts/m365/m365-customer-feedback-analyzer.md`
- [ ] `prompts/m365/m365-daily-standup-assistant.md`
- [ ] `prompts/m365/m365-data-insights-assistant.md`
- [ ] `prompts/m365/m365-designer-image-prompt-generator.md`
- [ ] `prompts/m365/m365-designer-infographic-brief.md`
- [ ] `prompts/m365/m365-designer-social-media-kit.md`
- [ ] `prompts/m365/m365-document-summarizer.md`
- [ ] `prompts/m365/m365-email-triage-helper.md`
- [ ] `prompts/m365/m365-excel-formula-expert.md`
- [ ] `prompts/m365/m365-handover-document-creator.md`
- [ ] `prompts/m365/m365-manager-sync-planner.md`
- [ ] `prompts/m365/m365-meeting-prep-brief.md`
- [ ] `prompts/m365/m365-meeting-recap-assistant.md`
- [ ] `prompts/m365/m365-personal-task-collector.md`
- [ ] `prompts/m365/m365-presentation-outline-generator.md`
- [ ] `prompts/m365/m365-project-status-reporter.md`
- [ ] `prompts/m365/m365-slide-content-refiner.md`
- [ ] `prompts/m365/m365-sway-document-to-story.md`
- [ ] `prompts/m365/m365-sway-visual-newsletter.md`
- [ ] `prompts/m365/m365-weekly-review-coach.md`

### Task A7: System Category (22 files)
- [ ] `prompts/system/ai-assistant-system-prompt.md`
- [ ] `prompts/system/api-architecture-designer.md`
- [ ] `prompts/system/blockchain-architecture-specialist.md`
- [ ] `prompts/system/cloud-architecture-consultant.md`
- [ ] `prompts/system/compliance-architecture-designer.md`
- [ ] `prompts/system/data-architecture-designer.md`
- [ ] `prompts/system/devops-architecture-planner.md`
- [ ] `prompts/system/disaster-recovery-architect.md`
- [ ] `prompts/system/enterprise-integration-architect.md`
- [ ] `prompts/system/example-research-output.md`
- [ ] `prompts/system/frontier-agent-deep-research.md`
- [ ] `prompts/system/iot-architecture-designer.md`
- [ ] `prompts/system/legacy-modernization-architect.md`
- [ ] `prompts/system/m365-copilot-research-agent.md`
- [ ] `prompts/system/microservices-architecture-expert.md`
- [ ] `prompts/system/mobile-architecture-consultant.md`
- [ ] `prompts/system/office-agent-technical-specs.md`
- [ ] `prompts/system/performance-architecture-optimizer.md`
- [ ] `prompts/system/prompt-quality-evaluator.md`
- [ ] `prompts/system/security-architecture-specialist.md`
- [ ] `prompts/system/solution-architecture-designer.md`
- [ ] `prompts/system/tree-of-thoughts-repository-evaluator.md`

---

## Stream B: Creative Category Expansion (NEW CONTENT)

**Owner**: _Unassigned_  
**Priority**: CRITICAL (P0)  
**Effort**: Large  
**Dependencies**: None  
**Target**: 2 → 15-20 prompts  
**Research Source**: [RESEARCH_REPORT Section 7](./RESEARCH_REPORT_2025-11-30.md#7-new-prompts-by-section)

### Task B1: Professional Writing (5 prompts)

- [ ] Create `prompts/creative/professional-email-writer.md` (Copy.ai inspired)
- [ ] Create `prompts/creative/report-summarizer.md` (Jasper inspired)
- [ ] Create `prompts/creative/proposal-generator.md` (Copy.ai inspired)
- [ ] Create `prompts/creative/press-release-writer.md` (Jasper inspired)
- [ ] Create `prompts/creative/email-subject-lines.md` (Copy.ai inspired)

### Task B2: Marketing Content (5 prompts)

- [ ] Create `prompts/creative/social-media-creator.md` (Jasper Instagram)
- [ ] Create `prompts/creative/linkedin-post-writer.md` (Copy.ai LinkedIn)
- [ ] Create `prompts/creative/ad-copy-generator.md` (Copy.ai Ad Copy)
- [ ] Create `prompts/creative/newsletter-creator.md` (Copy.ai Newsletter)
- [ ] Create `prompts/creative/product-description.md` (Jasper inspired)

### Task B3: Content Tools (4 prompts)

- [ ] Create `prompts/creative/tone-adjuster.md` (Anthropic Adaptive Editor)
- [ ] Create `prompts/creative/content-simplifier.md` (Anthropic Second-grade)
- [ ] Create `prompts/creative/headline-generator.md` (Jasper Headlines)
- [ ] Create `prompts/creative/seo-content-optimizer.md`

### Task B4: Advanced Creative (3 prompts)

- [ ] Create `prompts/creative/case-study-builder.md` (Copy.ai Case Study)
- [ ] Create `prompts/creative/video-script-writer.md`
- [ ] Create `prompts/creative/storytelling-framework.md`

**Template to use**: `/templates/prompt-template.md`  
**Use simplified structure from Stream S**

---

## Stream C: Business Category Expansion (NEW CONTENT)

**Owner**: _Unassigned_  
**Priority**: HIGH (P1)  
**Effort**: Medium  
**Dependencies**: None  
**Target**: 26 → 35-40 prompts  
**Research Source**: [RESEARCH_REPORT Section 7](./RESEARCH_REPORT_2025-11-30.md#7-new-prompts-by-section)

### Task C1: Sales Enablement (4 prompts)

- [ ] Create `prompts/business/pitch-deck-generator.md` (Jasper Campaign Brief)
- [ ] Create `prompts/business/sales-objection-handler.md` (Copy.ai Sales)
- [ ] Create `prompts/business/cold-email-generator.md` (Copy.ai Cold Email)
- [ ] Create `prompts/business/follow-up-email.md` (Jasper Email Sequence)

### Task C2: HR & Recruiting (4 prompts)

- [ ] Create `prompts/business/job-description-writer.md` (Anthropic Interview)
- [ ] Create `prompts/business/interview-questions.md` (Anthropic Interview Crafter)
- [ ] Create `prompts/business/performance-review.md` (Anthropic Grading Guru)
- [ ] Create `prompts/business/onboarding-checklist-creator.md`

### Task C3: Executive Communications (3 prompts)

- [ ] Create `prompts/business/meeting-summary.md` (Anthropic Meeting Scribe)
- [ ] Create `prompts/business/board-update.md` (Jasper Internal Comms)
- [ ] Create `prompts/business/competitive-analysis.md` (Copy.ai Text Analyzer)

---

## Stream D: Governance Category Expansion (NEW CONTENT)

**Owner**: _Unassigned_  
**Priority**: MEDIUM (P2)  
**Effort**: Small  
**Dependencies**: None  
**Target**: 3 → 10 prompts  
**Research Source**: [RESEARCH_REPORT Section 7](./RESEARCH_REPORT_2025-11-30.md#7-new-prompts-by-section)

### Task D1: Compliance & Audit (6 prompts)

- [ ] Create `prompts/governance/compliance-checker.md`
- [ ] Create `prompts/governance/risk-assessment.md`
- [ ] Create `prompts/governance/audit-report-generator.md`
- [ ] Create `prompts/governance/policy-writer.md`
- [ ] Create `prompts/governance/data-classification.md`
- [ ] Create `prompts/governance/incident-response.md`

---

## Stream E: Content Type Gap Filling

**Owner**: _Unassigned_  
**Priority**: LOW (P3)  
**Effort**: Ongoing  
**Dependencies**: Streams A-D  

### Task E1: Tutorials (5 prompts)
- [ ] Create tutorial for prompt engineering basics
- [ ] Create tutorial for ReAct pattern usage
- [ ] Create tutorial for Chain-of-Thought patterns
- [ ] Create tutorial for Tree-of-Thoughts patterns
- [ ] Create tutorial for M365 Copilot prompt crafting

### Task E2: Troubleshooting Guides (3 prompts)
- [ ] Create troubleshooting guide for common prompt failures
- [ ] Create troubleshooting guide for validation errors
- [ ] Create troubleshooting guide for platform-specific issues

### Task E3: Category Quickstarts (4 prompts)
- [ ] Create quickstart for developers/ category
- [ ] Create quickstart for business/ category
- [ ] Create quickstart for creative/ category
- [ ] Create quickstart for analysis/ category

---

## Agent Assignment Matrix

| Stream | Task Count | Est. Time | Can Run Parallel | Priority |
| :--- |------------| :--- |------------------| :--- |
| S (Simplify) | 8 categories | 2-3 hours | ✅ Yes (split by S1-S5) | P0 |
| R (Scoring) | 4 tasks | 2-3 hours | ✅ Yes (after R1) | P1 |
| A (Frontmatter) | 128 files | 3-4 hours | ✅ Yes (split by A1-A7) | P0 |
| B (Creative) | 17 new files | 3-4 hours | ✅ Yes (split by B1-B4) | P0 |
| C (Business) | 11 new files | 2-3 hours | ✅ Yes (split by C1-C3) | P1 |
| D (Governance) | 6 new files | 1-2 hours | ✅ Yes | P2 |
| E (Gap Fill) | 12 new files | 2-3 hours | ⚠️ After S,A | P3 |

### Recommended Agent Distribution

**For 2 Agents**:

- Agent 1: Stream S + Stream A (simplify then fix frontmatter)
- Agent 2: Streams B + C + R (new content + scoring)

**For 3 Agents**:

- Agent 1: Stream S (simplification - all categories)
- Agent 2: Stream A (frontmatter remediation - all categories)
- Agent 3: Streams B + C + D (all new content creation)

**For 4 Agents**:

- Agent 1: Stream S (simplification)
- Agent 2: Stream A, Tasks A1-A4 (frontmatter: advanced, analysis, business, developers)
- Agent 3: Stream A, Tasks A5-A7 + Stream R (frontmatter: governance, m365, system + scoring)
- Agent 4: Streams B + C + D (all new content)

**For 5+ Agents**:

- Agent 1: Stream S (simplification)
- Agent 2: Stream A, Tasks A1-A3 (frontmatter: advanced, analysis, business)
- Agent 3: Stream A, Tasks A4-A7 (frontmatter: developers, governance, m365, system)
- Agent 4: Stream B (creative expansion - 17 prompts)
- Agent 5: Stream C + D (business + governance expansion)
- Agent 6: Stream R (scoring rubric + tooling)

---

## Validation Commands

After completing any task, run:

```powershell
$env:PYTHONIOENCODING = "utf-8"
D:/source/prompts/.venv/Scripts/python.exe tools/validators/frontmatter_validator.py --folder prompts --summary
```

Target: 100% pass rate (139/139 files)

---

## Completion Criteria

### Stream S (Simplification)

- [ ] All changelogs removed from prompts
- [ ] `estimatedTime` and `technique` fields removed
- [ ] All descriptions ≤ 3 sentences
- [ ] All tips sections ≤ 5 bullets
- [ ] All related prompts ≤ 3 items
- [ ] Average prompt length reduced by 50%+

### Stream R (Scoring)

- [ ] `tools/rubrics/prompt-scoring.yaml` created
- [ ] `tools/validators/score_validator.py` created
- [ ] CI integration for minimum score (3.0)
- [ ] All prompts have `effectivenessScore` field

### Stream A (Frontmatter)

- [ ] All 139 files pass frontmatter validation

### Stream B (Creative)

- [ ] Creative category has 17+ prompts (2 existing + 15 new)

### Stream C (Business)

- [ ] Business category has 37+ prompts (26 existing + 11 new)

### Stream D (Governance)

- [ ] Governance category has 9+ prompts (3 existing + 6 new)

### Stream E (Gap Filling)

- [ ] At least 5 tutorials created
- [ ] At least 3 troubleshooting guides created
- [ ] Category quickstarts for developers, business, creative, analysis

### Overall Success

- [ ] 100% frontmatter validation pass rate
- [ ] Average prompt length < 100 lines
- [ ] All prompts scored ≥ 3.0
- [ ] Total prompt count ≥ 175

---

_Last updated: 2025-11-30_
