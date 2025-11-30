# Prompt Library Analysis - Parallel Work TODO

**Generated**: 2025-11-30  
**Updated**: 2025-11-30 (incorporated research recommendations)  
**Sources**:
- ReAct Analysis: `prompt-library-refactor-react.md`
- Research Report: [RESEARCH_REPORT_2025-11-30.md](./RESEARCH_REPORT_2025-11-30.md)
- Full Analysis: [REPO_ANALYSIS_REPORT_2025-11-30.md](./REPO_ANALYSIS_REPORT_2025-11-30.md)

---

## Work Streams (Parallelizable)

Each work stream can be assigned to a separate agent. Streams are independent with no blocking dependencies.

| Stream | Priority | Focus | Parallelizable |
|--------|----------|-------|----------------|
| **S** | P0 | Simplification (remove bloat) | ✅ Yes |
| **A** | P0 | Frontmatter Remediation | ✅ Yes |
| **B** | P0 | Creative Expansion | ✅ Yes |
| **C** | P1 | Business Expansion | ✅ Yes |
| **D** | P2 | Governance Expansion | ✅ Yes |
| **R** | P1 | Scoring Rubric & Tooling | ✅ Yes |
| **E** | P3 | Content Type Gap Filling | ⚠️ After S,A |

---

## Stream S: Simplification (ALL FILES) 🆕

**Owner**: _Unassigned_  
**Priority**: P0 CRITICAL  
**Effort**: Medium  
**Dependencies**: None  
**Research Source**: [RESEARCH_REPORT Section 5](./RESEARCH_REPORT_2025-11-30.md#5-simplification-actions)

> **Key Finding**: Industry leaders use dramatically simpler structures. Target: 60-70% reduction in prompt length.

### Task S1: Remove Changelog Sections (All Files)

Remove inline changelog sections from all prompts. Use git history instead.

- [ ] Remove changelogs from `prompts/advanced/*.md`
- [ ] Remove changelogs from `prompts/analysis/*.md`
- [ ] Remove changelogs from `prompts/business/*.md`
- [ ] Remove changelogs from `prompts/creative/*.md`
- [ ] Remove changelogs from `prompts/developers/*.md`
- [ ] Remove changelogs from `prompts/governance/*.md`
- [ ] Remove changelogs from `prompts/m365/*.md`
- [ ] Remove changelogs from `prompts/system/*.md`

**Estimated savings**: ~20 lines per file

### Task S2: Remove/Simplify Deprecated Fields

Remove these fields from all frontmatter:

- [ ] Remove `estimatedTime` field (1/10 sources use)
- [ ] Remove `technique` field (can infer from content)
- [ ] Move `dataClassification` to CI/build tooling
- [ ] Move `reviewStatus` to CI/build tooling

### Task S3: Consolidate "When to Use" into Intro

- [ ] Merge "When to Use" sections into `intro` field
- [ ] Remove standalone "When to Use" headings
- [ ] Target: One-sentence intro per prompt

**Estimated savings**: ~10 lines per file

### Task S4: Reduce Tips and Related Prompts

- [ ] Limit tips to 5 bullets max (remove excess)
- [ ] Limit related prompts to 3 max

**Estimated savings**: ~15 lines per file

### Task S5: Trim Verbose Descriptions

- [ ] Reduce all Description sections to 2-3 sentences max
- [ ] Remove redundant content

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
|----------|-------------|
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

## Stream R: Scoring Rubric & Tooling 🆕

**Owner**: _Unassigned_  
**Priority**: P1 HIGH  
**Effort**: Medium  
**Dependencies**: None  
**Research Source**: [RESEARCH_REPORT Section 6](./RESEARCH_REPORT_2025-11-30.md#6-scoring-implementation-plan)

### Task R1: Create Scoring Rubric

- [ ] Create `tools/rubrics/prompt-scoring.yaml` with dimensions:
  - Clarity (25%)
  - Effectiveness (30%)
  - Reusability (20%)
  - Simplicity (15%)
  - Examples (10%)

### Task R2: Build Score Validator

- [ ] Create `tools/validators/score_validator.py`
- [ ] Validate `effectivenessScore` field (1.0-5.0)
- [ ] Integrate with CI for minimum score check (3.0)

### Task R3: Add Score Display

- [ ] Update index templates to show star ratings
- [ ] Add score badge to prompt pages

### Task R4: Backfill Scores (After R1-R3)

- [ ] Score all `prompts/advanced/*.md` files
- [ ] Score all `prompts/analysis/*.md` files
- [ ] Score all `prompts/business/*.md` files
- [ ] Score all `prompts/creative/*.md` files
- [ ] Score all `prompts/developers/*.md` files
- [ ] Score all `prompts/governance/*.md` files
- [ ] Score all `prompts/m365/*.md` files
- [ ] Score all `prompts/system/*.md` files

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
|--------|------------|-----------|------------------|----------|
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
