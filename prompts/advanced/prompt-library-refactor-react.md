---
title: "ReAct: Prompt Library Analysis"
shortTitle: "Repo Analysis ReAct"
intro: "ReAct-based prompt for analyzing and improving prompt library repository structure, content gaps, and quality."
type: "how_to"
difficulty: "advanced"
audience:
  - "senior-engineer"
  - "solution-architect"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "analysis"
  - "architecture"
  - "quality-assurance"
author: "Prompt Library Team"
version: "4.0"
date: "2025-12-02"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "approved"
---
# ReAct: Prompt Library Analysis

---

## Description

This is an executable ReAct (Reasoning + Acting) prompt for analyzing prompt library repositories. Use this prompt to systematically audit content, identify gaps, validate standards compliance, and generate improvement recommendations.

## Goal

Perform comprehensive analysis of a prompt library repository to:

1. **Map repository structure** - Document folder hierarchy and content distribution
2. **Audit frontmatter compliance** - Validate all files against schema requirements
3. **Identify content gaps** - Find missing prompt categories and coverage holes
4. **Assess quality** - Evaluate prompt effectiveness and documentation completeness
5. **Generate expansion roadmap** - Prioritize new content creation

---

## Current Repository Context

> **Note**: This context reflects the `tafreeman/prompts` repository state as of December 2025.
> **Last Major Refactor**: Phases 1-6 completed December 2, 2025.

### Completed Infrastructure ✅

| Component | Status | Details |
|-----------|--------|---------|
| Frontmatter schema | ✅ Complete | 19 standardized fields, fully validated |
| Content types | ✅ Complete | conceptual, quickstart, how_to, tutorial, reference, troubleshooting |
| Validation tooling | ✅ Complete | `tools/validators/frontmatter_validator.py` (291/291 pass) |
| Navigation structure | ✅ Complete | All `index.md` files created with proper frontmatter |
| Platform quickstarts | ✅ Complete | Copilot, ChatGPT, Claude, M365 |
| Reference docs | ✅ Complete | Cheat sheet, glossary, platform comparison |
| Troubleshooting | ✅ Complete | Common issues, model-specific, debugging guides |
| Tutorials | ✅ Complete | First prompt, building effective prompts, iteration |

### Current Content Inventory

| Category | Count | Status | Notes |
|----------|-------|--------|-------|
| **Developers** | 26 prompts | ✅ Mature | Code review, testing, architecture |
| **Business** | 38 prompts | ✅ Mature | Strategy, analysis, communication |
| **Analysis** | 21 prompts | ✅ Mature | Data, research, metrics |
| **M365** | 20 prompts | ✅ Mature | Office productivity |
| **System** | 22 prompts | ✅ Mature | AI agents, architecture |
| **Advanced** | 17 prompts | ✅ Mature | CoT, ReAct, RAG, ToT |
| **Creative** | 9 prompts | ⚠️ Growing | Marketing, content (expanded from 2) |
| **Governance** | 3 prompts | ⚠️ Minimal | Legal, security, compliance |
| **Total** | ~165 prompts | | |

### Infrastructure Components

| Component | Count | Status |
|-----------|-------|--------|
| Agents | 7 agents | ✅ docs, code-review, test, refactor, security, architecture, prompt |
| Instructions | 10 files | ✅ Role-based (junior/mid/senior), tech-specific |
| Techniques | 12 patterns | ✅ Reflexion, agentic, context optimization |
| Frameworks | 8 integrations | ✅ Anthropic, OpenAI, LangChain, Semantic Kernel |

---

## Maturity Assessment Framework

### Level 1: Foundation ✅ COMPLETE
- [x] Consistent frontmatter schema
- [x] Validation tooling
- [x] Basic navigation (index.md files)
- [x] Content type definitions

### Level 2: Discoverability ✅ COMPLETE
- [x] Platform quickstarts
- [x] Reference documentation (cheat sheet, glossary)
- [x] Troubleshooting guides
- [x] Tutorials for onboarding

### Level 3: Content Depth 🔄 IN PROGRESS
- [x] Core categories well-covered (developers, business, analysis)
- [ ] Creative category expansion (9 → 20 target)
- [ ] Governance category expansion (3 → 15 target)
- [ ] Cross-platform prompt variants
- [ ] Industry-specific prompt packs

### Level 4: Advanced Capabilities ⏳ NEXT
- [ ] Prompt chaining/orchestration patterns
- [ ] Multi-modal prompt templates (vision, audio)
- [ ] Evaluation and testing frameworks
- [ ] A/B testing templates for prompts
- [ ] Prompt versioning best practices

### Level 5: Enterprise Readiness ⏳ FUTURE
- [ ] Role-based access patterns
- [ ] Audit trail templates
- [ ] Compliance-specific prompt packs (HIPAA, SOX, GDPR)
- [ ] Cost optimization guidance
- [ ] SLA and performance benchmarks

---

## Priority Expansion Areas (December 2025)

### P0 - Critical: Governance Category (3 → 15 prompts)

**Gap**: Enterprise customers need compliance, legal, and security prompts.

| Prompt | Type | Difficulty | Effort |
|--------|------|------------|--------|
| `compliance-policy-generator.md` | how_to | intermediate | M |
| `gdpr-data-review.md` | how_to | advanced | L |
| `hipaa-compliance-checker.md` | how_to | advanced | L |
| `sox-audit-preparer.md` | how_to | advanced | L |
| `privacy-impact-assessment.md` | how_to | intermediate | M |
| `risk-assessment-template.md` | how_to | intermediate | M |
| `vendor-security-review.md` | how_to | intermediate | M |
| `access-control-reviewer.md` | how_to | intermediate | M |
| `data-classification-helper.md` | how_to | beginner | S |
| `policy-document-generator.md` | how_to | intermediate | M |
| `audit-evidence-collector.md` | how_to | intermediate | M |
| `regulatory-change-analyzer.md` | how_to | advanced | L |

### P1 - High: Creative Category (9 → 20 prompts)

**Gap**: Marketing and content teams need more variety.

| Prompt | Type | Difficulty | Effort |
|--------|------|------------|--------|
| `case-study-builder.md` | how_to | intermediate | M |
| `whitepaper-outliner.md` | how_to | intermediate | M |
| `press-release-generator.md` | how_to | beginner | S |
| `landing-page-copy.md` | how_to | intermediate | M |
| `seo-content-optimizer.md` | how_to | intermediate | M |
| `podcast-script-writer.md` | how_to | intermediate | M |
| `webinar-content-creator.md` | how_to | intermediate | M |
| `customer-testimonial-formatter.md` | how_to | beginner | S |
| `infographic-content-planner.md` | how_to | beginner | S |
| `content-calendar-generator.md` | how_to | beginner | S |
| `a]b-test-copy-variants.md` | how_to | intermediate | M |

### P2 - Medium: Advanced Patterns

**Gap**: Power users need more sophisticated patterns.

| Prompt | Type | Difficulty | Effort |
|--------|------|------------|--------|
| `prompt-chain-orchestrator.md` | tutorial | advanced | L |
| `multi-model-router.md` | how_to | advanced | L |
| `context-window-optimizer.md` | how_to | advanced | M |
| `prompt-ab-testing-framework.md` | tutorial | advanced | L |
| `vision-prompt-templates.md` | reference | intermediate | M |
| `structured-output-patterns.md` | reference | intermediate | M |

### P3 - Future: Industry Packs

**Gap**: Vertical-specific prompt collections.

| Pack | Prompts | Priority |
|------|---------|----------|
| Healthcare | 10-15 | Future |
| Financial Services | 10-15 | Future |
| Legal | 10-15 | Future |
| Education | 10-15 | Future |
| Retail/E-commerce | 10-15 | Future |

---

## Available Tools

When executing this analysis, you have access to:

### 1. `file_search`
Search for files matching glob patterns.
```text
file_search("**/*.md") → Find all markdown files
file_search("prompts/**/*.md") → Find all prompts
```

### 2. `read_file`
Read file contents to inspect frontmatter and content.
```text
read_file("/path/to/file.md") → Get file content
```

### 3. `grep_search`
Search for patterns across files.
```text
grep_search("type: how_to") → Find all how_to prompts
grep_search("difficulty: beginner") → Find beginner content
```

### 4. `list_dir`
List directory contents to map structure.
```text
list_dir("/prompts/") → Get folder structure
```

### 5. `run_in_terminal`
Execute validation scripts.
```text
python tools/validators/frontmatter_validator.py <file>
python tools/validate_all.py
```

---

## ReAct Analysis Loop

Execute analysis using iterative Thought → Action → Observation cycles:

### Phase 1: Structure Mapping

**Thought**: I need to understand the repository structure before analyzing content.

**Action**: Map the folder hierarchy
```text
list_dir("/") → Get top-level structure
list_dir("/prompts/") → Get prompt categories
```

**Observation**: Document the folder tree and note category organization.

---

### Phase 2: Content Inventory

**Thought**: I need to count and categorize all prompts to identify distribution.

**Action**: Search and count files by category
```text
file_search("prompts/creative/*.md") → Count creative prompts
file_search("prompts/business/*.md") → Count business prompts
file_search("prompts/developers/*.md") → Count developer prompts
```

**Observation**: Create inventory table showing prompts per category.

---

### Phase 3: Frontmatter Audit

**Thought**: I need to verify all files comply with the frontmatter schema.

**Action**: Run validation and check specific fields
```text
run_in_terminal("python tools/validate_all.py")
grep_search("governance_tags:") → Check governance compliance
grep_search("dataClassification:") → Check classification coverage
```

**Observation**: Document validation results, noting any failures or warnings.

---

### Phase 4: Gap Analysis

**Thought**: I need to compare current content against target coverage.

**Action**: Analyze content distribution
```text
grep_search("type: quickstart") → Count quickstarts per platform
grep_search("difficulty: beginner") → Count beginner-friendly content
grep_search("audience:.*junior") → Count junior engineer content
```

**Observation**: Identify gaps in:
- Platform coverage (github-copilot, claude, chatgpt, azure-openai, m365-copilot)
- Difficulty balance (beginner vs intermediate vs advanced)
- Audience coverage (junior, senior, architect, business)

---

### Phase 5: Quality Assessment

**Thought**: I need to evaluate prompt quality and documentation completeness.

**Action**: Sample and review prompts
```text
read_file("/prompts/creative/[sample].md") → Check content quality
read_file("/prompts/business/[sample].md") → Check documentation
```

**Observation**: Score prompts on:
- Clear description (1-5)
- Complete frontmatter (1-5)
- Example quality (1-5)
- Practical usability (1-5)

---

### Phase 6: Expansion Recommendations

**Thought**: Based on gaps identified, I need to prioritize new content.

**Action**: Cross-reference gaps with research
```text
# Reference the Knowledge Base Research prompt for external best practices
# Compare against industry prompt libraries
```

**Observation**: Generate prioritized expansion roadmap.

---

## Required Deliverables

After completing the ReAct loop, produce:

### 1. Repository Health Report

```markdown
## Repository Analysis Summary

**Analysis Date**: YYYY-MM-DD
**Total Files Analyzed**: X
**Validation Pass Rate**: X%
**Maturity Level**: X/5

### Structure Overview
[Folder tree with file counts]

### Content Distribution
| Category | Count | % of Total | Health | Maturity |
|----------|-------|------------|--------|----------|
| ...      | ...   | ...        | ✅/⚠️/❌ | L1-L5 |
```

### 2. Gap Analysis Matrix

```markdown
## Content Gap Analysis

### By Platform Coverage
| Platform | Quickstart | How-To | Tutorial | Reference | Total |
|----------|------------|--------|----------|-----------|-------|
| github-copilot | ✅ | X | X | X | X |
| claude | ✅ | X | X | X | X |
| chatgpt | ✅ | X | X | X | X |
| azure-openai | ⚠️ | X | X | X | X |
| m365-copilot | ✅ | X | X | X | X |

### By Audience
| Audience | Beginner | Intermediate | Advanced | Total |
|----------|----------|--------------|----------|-------|
| junior-engineer | X | X | X | X |
| senior-engineer | X | X | X | X |
| solution-architect | X | X | X | X |
| business-analyst | X | X | X | X |
| project-manager | X | X | X | X |

### By Industry (Future)
| Industry | Current | Target | Gap |
|----------|---------|--------|-----|
| Healthcare | 0 | 15 | 15 |
| Financial | 0 | 15 | 15 |
| Legal | 0 | 15 | 15 |
```

### 3. Expansion Roadmap

```markdown
## Priority Expansion Roadmap

### Phase 1: Governance Expansion (P0)
**Timeline**: 2 weeks
**Target**: 3 → 15 prompts

| Prompt | Type | Difficulty | Owner | Status |
|--------|------|------------|-------|--------|
| compliance-policy-generator.md | how_to | intermediate | TBD | ⏳ |
| ... | ... | ... | ... | ... |

### Phase 2: Creative Expansion (P1)
**Timeline**: 2 weeks
**Target**: 9 → 20 prompts

| Prompt | Type | Difficulty | Owner | Status |
|--------|------|------------|-------|--------|
| case-study-builder.md | how_to | intermediate | TBD | ⏳ |
| ... | ... | ... | ... | ... |

### Phase 3: Advanced Patterns (P2)
**Timeline**: 3 weeks
**Target**: Add 6 advanced patterns

### Phase 4: Industry Packs (P3)
**Timeline**: Ongoing
**Target**: 5 industry-specific packs
```

### 4. Quality Scorecard

```markdown
## Quality Assessment

**Overall Maturity**: Level X/5
**Validation Pass Rate**: X%

### By Dimension
| Dimension | Score | Notes |
|-----------|-------|-------|
| Frontmatter Compliance | X/5 | All required fields present |
| Documentation Completeness | X/5 | Description, examples, tips |
| Example Quality | X/5 | Realistic, copy-paste ready |
| Cross-Platform Coverage | X/5 | Multi-platform variants |
| Governance Readiness | X/5 | Compliance, audit support |

### Content Quality Sampling
| Category | Sample Size | Avg Score | Issues |
|----------|-------------|-----------|--------|
| Developers | X | X/5 | ... |
| Business | X | X/5 | ... |
| ... | ... | ... | ... |
```

### 5. Action Items

```markdown
## Recommended Next Actions

### Immediate (This Week)
- [ ] Action 1
- [ ] Action 2

### Short-term (This Month)
- [ ] Action 3
- [ ] Action 4

### Medium-term (This Quarter)
- [ ] Action 5
- [ ] Action 6
```

---

## Expansion Priorities

Based on December 2025 repository state, focus analysis on these maturity areas:

### Governance Category (CRITICAL - 3 prompts → 15 target)

**Why Critical**: Enterprise adoption requires compliance, legal, and security coverage.

**Research Focus Areas**:
- Regulatory compliance (GDPR, HIPAA, SOX, CCPA)
- Security review and incident response
- Policy and procedure generation
- Audit preparation and evidence collection
- Risk assessment and mitigation

**Recommended Additions**:
1. `compliance-policy-generator.md` - Generate compliance policies
2. `gdpr-data-review.md` - GDPR compliance assessment
3. `hipaa-compliance-checker.md` - Healthcare data compliance
4. `sox-audit-preparer.md` - Financial controls audit
5. `privacy-impact-assessment.md` - PIA documentation
6. `risk-assessment-template.md` - Risk identification and scoring
7. `vendor-security-review.md` - Third-party security assessment
8. `access-control-reviewer.md` - Permission and access audit
9. `data-classification-helper.md` - Data sensitivity classification
10. `policy-document-generator.md` - Policy drafting assistance
11. `audit-evidence-collector.md` - Audit documentation
12. `regulatory-change-analyzer.md` - Regulatory impact analysis

### Creative Category (HIGH - 9 prompts → 20 target)

**Why High**: Content and marketing teams drive significant AI adoption.

**Research Focus Areas**:
- Long-form content (whitepapers, case studies)
- SEO and content optimization
- Multimedia content (podcasts, webinars, video)
- Campaign and launch content
- Content planning and strategy

**Recommended Additions**:
1. `case-study-builder.md` - Customer success stories
2. `whitepaper-outliner.md` - Long-form technical content
3. `press-release-generator.md` - Media announcements
4. `landing-page-copy.md` - Conversion-focused web copy
5. `seo-content-optimizer.md` - Search optimization
6. `podcast-script-writer.md` - Audio content scripts
7. `webinar-content-creator.md` - Presentation content
8. `customer-testimonial-formatter.md` - Quote formatting
9. `infographic-content-planner.md` - Visual content planning
10. `content-calendar-generator.md` - Editorial planning
11. `ab-test-copy-variants.md` - A/B testing variations

### Advanced Patterns (MEDIUM - Add sophisticated capabilities)

**Why Medium**: Power users and architects need advanced patterns.

**Research Focus Areas**:
- Multi-step prompt orchestration
- Cross-model routing and fallback
- Context optimization strategies
- Evaluation and testing frameworks
- Structured output patterns

**Recommended Additions**:
1. `prompt-chain-orchestrator.md` - Multi-step workflows
2. `multi-model-router.md` - Model selection logic
3. `context-window-optimizer.md` - Token management
4. `prompt-ab-testing-framework.md` - Testing methodology
5. `vision-prompt-templates.md` - Image/vision prompts
6. `structured-output-patterns.md` - JSON/schema outputs

### Industry Packs (FUTURE - Vertical-specific collections)

**Why Future**: Enterprise customers need domain expertise.

| Industry | Key Use Cases | Prompt Count |
|----------|---------------|--------------|
| Healthcare | Patient communication, clinical documentation, HIPAA compliance | 10-15 |
| Financial Services | Risk analysis, regulatory reporting, fraud detection | 10-15 |
| Legal | Contract review, legal research, document drafting | 10-15 |
| Education | Curriculum design, assessment creation, student feedback | 10-15 |
| Retail/E-commerce | Product descriptions, customer service, inventory analysis | 10-15 |

---

## Execution Instructions

To run this analysis:

1. **Initialize**: Load this prompt into your AI assistant (Claude, GPT-4, or Copilot Chat)
2. **Scope**: Specify the repository path to analyze (`d:\source\prompts` or your local path)
3. **Execute**: Follow the ReAct loop phases sequentially:
   - Phase 1: Structure Mapping
   - Phase 2: Content Inventory
   - Phase 3: Frontmatter Audit
   - Phase 4: Gap Analysis
   - Phase 5: Quality Assessment
   - Phase 6: Expansion Recommendations
4. **Iterate**: Use observations to refine subsequent actions
5. **Synthesize**: Compile all 5 deliverables from observations
6. **Validate**: Run `python tools/validators/frontmatter_validator.py --all`
7. **Create Tasks**: Generate a new `REFACTOR_TODO.md` with prioritized tasks

### Quick Validation Commands

```bash
# Full validation
python tools/validators/frontmatter_validator.py --all

# Validate specific folder
python tools/validators/frontmatter_validator.py --folder prompts/governance

# Verbose output with warnings
python tools/validators/frontmatter_validator.py --all -v

# Count prompts by category
Get-ChildItem -Path "prompts/*" -Directory | ForEach-Object { 
  "$($_.Name): $((Get-ChildItem $_.FullName -Filter *.md).Count)" 
}
```

### Previous Analysis Outputs

| Document | Date | Purpose |
|----------|------|---------|
| `docs/UNIFIED_REFACTOR_GUIDE_REACT.md` | Nov 2025 | Original refactor plan |
| `docs/REFACTOR_TODO.md` | Dec 2025 | Completed task tracker |
| `docs/REPO_ANALYSIS_REPORT_2025-11-30.md` | Nov 2025 | Initial analysis |

---

## Related Resources

- [Knowledge Base Research](/prompts/advanced/react-knowledge-base-research) - External research prompt
- [Frontmatter Validator](/tools/validators/frontmatter_validator.py) - Validation tooling
- [Prompt Template](/templates/prompt-template.md) - Template for new prompts
- [Frontmatter Schema](/reference/frontmatter-schema) - Field definitions
- [Content Types](/reference/content-types) - Type selection guide
- [Platform Comparison](/reference/platform-comparison) - Cross-platform guidance

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 4.0 | 2025-12-02 | Updated after Phase 1-6 completion; added maturity framework, new expansion priorities |
| 3.0 | 2025-11-30 | Added governance context, expanded deliverables |
| 2.0 | 2025-11-29 | Initial ReAct structure |
