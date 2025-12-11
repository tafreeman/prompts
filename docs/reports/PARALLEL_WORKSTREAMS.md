# 🚀 Parallel Workstream Execution Plan

**Generated:** December 11, 2025  
**Purpose:** Copy-paste ready instructions for simultaneous agent execution

---

## Quick Reference

| Workstream | Agent | Category | Files | Est. Time |
|------------|-------|----------|-------|-----------|
| A | prompt_agent | Critical Fixes | 8 | 45-60 min |
| B | docs_agent | Business | 20 | 60 min |
| C | architecture_agent | System | 15 | 60 min |
| D | docs_agent | M365 | 18 | 50 min |
| E | security_agent | Governance (NEW) | 7 | 60 min |
| F | refactor_agent | Analysis | 18 | 50 min |

---

## 📦 WORKSTREAM A — Critical Fixes

### Copy This Prompt:

```
@prompt_agent

Fix these 8 lowest-scoring prompts by adding/improving required sections:

FILES TO EDIT:
1. prompts/governance/security-incident-response.md (59.5)
2. prompts/m365/m365-handover-document-creator.md (64.5)
3. prompts/advanced/prompt-library-refactor-react.md (65.0)
4. prompts/advanced/chain-of-thought-debugging.md (67.5)
5. prompts/advanced/library.md (67.5)
6. prompts/advanced/rag-document-retrieval.md (67.5)
7. prompts/advanced/react-tool-augmented.md (67.5)
8. prompts/advanced/tree-of-thoughts-architecture-evaluator.md (67.5)

FOR EACH FILE:
1. Add/improve **Description** section (2-3 sentences explaining what the prompt does)
2. Add/improve **Use Cases** section (3-5 bullet points of when to use it)
3. Add complete **Example** section with:
   - Context scenario
   - Sample input with variables filled in
   - Expected output
4. Fix any frontmatter warnings (ensure all required fields present)

After each file, validate with: python tools/validate_prompts.py <filepath>
```

---

## 📦 WORKSTREAM B — Business Category

### Copy This Prompt:

```
@docs_agent

Improve all 20 prompts in the Business category by adding comprehensive Examples.

FILES TO EDIT:
1. prompts/business/agile-sprint-planner.md
2. prompts/business/change-management-coordinator.md
3. prompts/business/stakeholder-communication-manager.md
4. prompts/business/board-update.md
5. prompts/business/budget-and-cost-controller.md
6. prompts/business/business-strategy-analysis.md
7. prompts/business/competitive-analysis.md
8. prompts/business/interview-questions.md
9. prompts/business/job-description-writer.md
10. prompts/business/meeting-summary.md
11. prompts/business/onboarding-checklist-creator.md
12. prompts/business/performance-review.md
13. prompts/business/pitch-deck-generator.md
14. prompts/business/risk-management-analyst.md
15. prompts/business/sales-objection-handler.md
16. prompts/business/business-process-reengineering.md
17. prompts/business/client-presentation-designer.md
18. prompts/business/cold-email-generator.md
19. prompts/business/crisis-management-coordinator.md
20. prompts/business/digital-transformation-advisor.md

FOR EACH FILE:
1. Add comprehensive **Example** section with:
   - Context: Brief scenario setup
   - Input: The actual prompt with variables filled in
   - Expected Output: What the AI should produce
2. Improve **Description** for clarity (2-3 sentences)
3. Add 1-2 additional Use Cases if fewer than 5 exist
4. Ensure frontmatter is complete

After batch complete, validate: python tools/validate_prompts.py prompts/business/
```

---

## 📦 WORKSTREAM C — System Architecture

### Copy This Prompt:

```
@architecture_agent

Enhance 15 System category architecture prompts with diagrams and decision frameworks.

FILES TO EDIT:
1. prompts/system/api-architecture-designer.md
2. prompts/system/blockchain-architecture-specialist.md
3. prompts/system/cloud-architecture-consultant.md
4. prompts/system/compliance-architecture-designer.md
5. prompts/system/data-architecture-designer.md
6. prompts/system/devops-architecture-planner.md
7. prompts/system/disaster-recovery-architect.md
8. prompts/system/enterprise-integration-architect.md
9. prompts/system/iot-architecture-designer.md
10. prompts/system/legacy-modernization-architect.md
11. prompts/system/microservices-architecture-expert.md
12. prompts/system/mobile-architecture-consultant.md
13. prompts/system/performance-architecture-optimizer.md
14. prompts/system/security-architecture-specialist.md
15. prompts/system/solution-architecture-designer.md

FOR EACH FILE:
1. Add **Mermaid diagram** showing the architecture pattern visually
2. Add **Decision Framework** section: "When to use this pattern" with criteria
3. Add **Cloud Platform Notes** for Azure, AWS, and GCP specifics
4. Enhance Example section with realistic enterprise architecture scenario
5. Add cross-references to related architecture prompts

After batch complete, validate: python tools/validate_prompts.py prompts/system/
```

---

## 📦 WORKSTREAM D — M365 Category

### Copy This Prompt:

```
@docs_agent

Improve 18 M365 prompts with Microsoft 365 Copilot-specific context and examples.

FILES TO EDIT:
1. prompts/m365/m365-daily-standup-assistant.md
2. prompts/m365/m365-customer-feedback-analyzer.md
3. prompts/m365/m365-designer-image-prompt-generator.md
4. prompts/m365/m365-designer-infographic-brief.md
5. prompts/m365/m365-designer-social-media-kit.md
6. prompts/m365/m365-manager-sync-planner.md
7. prompts/m365/m365-slide-content-refiner.md
8. prompts/m365/m365-sway-document-to-story.md
9. prompts/m365/m365-sway-visual-newsletter.md
10. prompts/m365/m365-data-insights-assistant.md
11. prompts/m365/m365-document-summarizer.md
12. prompts/m365/m365-email-triage-helper.md
13. prompts/m365/m365-excel-formula-expert.md
14. prompts/m365/m365-meeting-prep-brief.md
15. prompts/m365/m365-meeting-recap-assistant.md
16. prompts/m365/m365-personal-task-collector.md
17. prompts/m365/m365-presentation-outline-generator.md
18. prompts/m365/m365-project-status-reporter.md

FOR EACH FILE:
1. Add **Microsoft 365 Copilot-specific context** (which app this works best in)
2. Add **Example** showing actual M365 integration scenario:
   - Include realistic Microsoft Graph data references
   - Show Copilot Chat vs Copilot in specific apps usage
3. Add **Tips** section for M365-specific best practices
4. Add cross-references to related M365 prompts
5. Ensure frontmatter includes platform: "Microsoft 365 Copilot"

After batch complete, validate: python tools/validate_prompts.py prompts/m365/
```

---

## 📦 WORKSTREAM E — Governance Expansion (CREATE NEW)

### Copy This Prompt:

```
@security_agent

Create 7 NEW governance prompts to expand the category from 8 to 15 prompts.

FILES TO CREATE:
1. prompts/governance/hipaa-compliance-checker.md
2. prompts/governance/sox-audit-preparation.md
3. prompts/governance/vendor-security-review.md
4. prompts/governance/access-control-reviewer.md
5. prompts/governance/data-classification-helper.md
6. prompts/governance/regulatory-change-analyzer.md
7. prompts/governance/compliance-policy-generator.md

TEMPLATE REFERENCE:
Use prompts/governance/gdpr-compliance-assessment.md as the quality template.

EACH NEW PROMPT MUST INCLUDE:
1. Complete frontmatter:
   - title, description, author, version, date
   - type: "prompt"
   - category: "governance"
   - tags: [relevant compliance tags]
   - difficulty: appropriate level
   - platforms: applicable AI platforms

2. Sections:
   - **Description**: 2-3 sentences on purpose
   - **Use Cases**: 5+ bullet points
   - **The Prompt**: Complete prompt template with variables
   - **Example**: Full realistic compliance scenario with input/output
   - **Best Practices**: 3-5 tips for effective use
   - **Related Prompts**: Cross-references to other governance prompts

After creation, validate: python tools/validate_prompts.py prompts/governance/
```

---

## 📦 WORKSTREAM F — Analysis Category

### Copy This Prompt:

```
@refactor_agent

Improve 18 Analysis category prompts with domain specificity and real examples.

FILES TO EDIT:
1. prompts/analysis/business-case-developer.md
2. prompts/analysis/competitive-analysis-researcher.md
3. prompts/analysis/competitive-intelligence-researcher.md
4. prompts/analysis/consumer-behavior-researcher.md
5. prompts/analysis/data-analysis-specialist.md
6. prompts/analysis/gap-analysis-expert.md
7. prompts/analysis/industry-analysis-expert.md
8. prompts/analysis/library-network-graph.md
9. prompts/analysis/library-structure-treemap.md
10. prompts/analysis/market-research-analyst.md
11. prompts/analysis/metrics-and-kpi-designer.md
12. prompts/analysis/process-optimization-consultant.md
13. prompts/analysis/requirements-analysis-expert.md
14. prompts/analysis/stakeholder-requirements-gatherer.md
15. prompts/analysis/trend-analysis-specialist.md
16. prompts/analysis/user-experience-analyst.md
17. prompts/analysis/workflow-designer.md
18. prompts/analysis/library-capability-radar.md

FOR EACH FILE:
1. Add **domain-specific terminology** and industry jargon
2. Add **data visualization recommendations** where relevant (charts, graphs, dashboards)
3. Improve **Example** section with real business metrics/data:
   - Include sample numbers, percentages, timeframes
   - Show realistic analysis output format
4. **De-duplicate** any overlapping content with similar prompts
5. Add **cross-references** between related analysis prompts
6. Add **Tools Integration** tips (Excel, Power BI, Tableau mentions)

After batch complete, validate: python tools/validate_prompts.py prompts/analysis/
```

---

## ⚡ Post-Execution Commands

Run these after ALL workstreams complete:

```powershell
# Validate all prompts
python tools/validate_prompts.py

# Generate updated evaluation report
python tools/evaluate_library.py --all --output docs/reports/POST_SPRINT1_EVAL.md

# Generate updated audit CSV
python tools/audit_prompts.py --output audit_report_post_sprint1.csv
```

---

## 📊 Expected Outcomes

| Metric | Before | After Sprint 1 |
|--------|--------|----------------|
| Average Score | 66/100 | 75/100 |
| Grade D prompts | 104 | ~60 |
| Grade B+ prompts | 30 | ~80 |
| Governance prompts | 8 | 15 |
| Missing Examples | 108 | ~40 |

---

## 🔄 Conflict Prevention

These workstreams are designed to have **ZERO file conflicts**:

- **Workstream A**: Advanced + 1 governance + 1 m365 (specific files only)
- **Workstream B**: Business category only
- **Workstream C**: System category only
- **Workstream D**: M365 category (excludes the 1 file in A)
- **Workstream E**: NEW governance files only
- **Workstream F**: Analysis category only

✅ Safe to run all 6 simultaneously in separate windows/agents.
