---
title: 'ToT-ReAct: Prompt Library Evaluation & Research'
shortTitle: Library Eval ToT-ReAct
intro: Tree-of-Thoughts + ReAct prompt for comprehensive evaluation, research, and
  improvement of the tafreeman/prompts library.
type: how_to
difficulty: advanced
audience:
- senior-engineer
- solution-architect
platforms:
- github-copilot
- claude
- chatgpt
topics:
- analysis
- architecture
- quality-assurance
- research
author: Prompt Library Team
version: '5.1'
date: '2026-01-18'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: approved
effectivenessScore: 0.0
---

# ToT-ReAct: Prompt Library Evaluation & Research

---

## Description

This is an executable prompt combining **Tree-of-Thoughts (ToT)** branching for parallel research exploration with **ReAct** (Reasoning + Acting) for systematic execution. Use this prompt to:

1. **Evaluate prompt library quality** using dual-rubric scoring
2. **Research new prompting techniques** for library expansion
3. **Identify content gaps** and prioritize improvements
4. **Generate improvement recommendations** with academic rigor

## Goal

Perform comprehensive evaluation and research on the `tafreeman/prompts` library to:

1. **Score existing prompts** using Quality Standards (0-100) and Effectiveness (1.0-5.0) rubrics
2. **Research new techniques** using ToT branching with Reflexion-based iteration
3. **Map repository structure** and validate standards compliance
4. **Identify content gaps** and prioritize expansion areas
5. **Generate production-ready templates** for new prompts

---

## Variables

| Variable | Required? | Description | Example |
|---|---:|---|---|
| `[evaluation_goal]` | Yes | What you want this workflow to achieve. | `Reduce validator failures to 0` |
| `[scope]` | No | Optional boundaries (folders, categories, tiers). | `prompts/advanced/* only` |
| `[constraints]` | No | Constraints to respect while executing. | `minimal edits; do not change frontmatter` |

## Prompt

```text
You are a Prompt Library Maintainer.

Goal: [evaluation_goal]
Scope: [scope]
Constraints: [constraints]

Follow the ToT-ReAct execution protocol in this document:
1) Plan research branches and prioritize the top branches
2) Execute iterative Thought → Action → Observe cycles to gather evidence
3) Apply Reflexion self-critique to detect gaps
4) Produce deliverables (structure map, scorecard, gap analysis, recommendations)

When making edits, prioritize adding missing required sections (Description, Prompt, Variables, Example) while keeping original prompt intent intact.
```

## Example

### Scenario: Bringing the Advanced Folder to 100% Validation

**Input:**

```text
[evaluation_goal]: Bring all prompts into validator compliance
[scope]: prompts/advanced/*
[constraints]: smallest change possible; no rewrites
```

**Output:**

```markdown
# ToT-ReAct Execution Report: Advanced Folder Compliance

**Date**: 2026-01-18
**Goal**: Bring all prompts into validator compliance
**Scope**: prompts/advanced/*
**Constraints**: Minimal edits; preserve original prompt intent

---

## Phase 1: ToT Research Planning

### Selected Branches

| Branch | Focus | Priority |
|--------|-------|----------|
| A | Structural Validation Audit | High |
| B | Missing Section Identification | High |
| C | Frontmatter Schema Compliance | Medium |

---

## Phase 2: ReAct Execution

### Branch A - Cycle 1: Validation Baseline

**Thought**: I need to establish the current validation status.

**Action**: `run_in_terminal("python tools/validate_prompts.py prompts/advanced/")`

**Observation**:
- Total files: 21
- Files with issues: 5
- Common issue: Missing "## Example" section (4 files)
- Common issue: Missing "## Tips" section (3 files)

### Branch A - Cycle 2: Issue Categorization

**Thought**: I need to group files by the type of fix required.

**Action**: `grep_search("## Example", "prompts/advanced/*.md")`

**Observation**:
- Files missing Example section:
  1. `chain-of-thought-concise.md`
  2. `rag-document-retrieval.md`
  3. `react-tool-augmented.md`
  4. `tree-of-thoughts-template.md`

### Branch B - Cycle 1: Section Gap Analysis

**Thought**: I need to identify all missing required sections.

**Action**: Cross-reference each file against template requirements.

**Observation**:

| File | Missing Sections |
|------|------------------|
| `chain-of-thought-concise.md` | Example, Tips |
| `rag-document-retrieval.md` | Example |
| `react-tool-augmented.md` | Example, Variables |
| `tree-of-thoughts-template.md` | Tips |
| `reflection-self-critique.md` | Tips |

---

## Phase 3: Reflexion Self-Critique

### Completeness Check
1. ✅ Evaluated ALL 21 prompts in scope
2. ✅ Checked both structural and content validation
3. ✅ Identified specific missing sections per file

### Gap Identification
- 5/21 files (24%) have validation issues
- Most common gap: Missing Example section (4 files)
- Second gap: Missing Tips section (3 files)

### Improvement Batch Plan
- **Batch 1**: Add Example sections to 4 files (highest impact)
- **Batch 2**: Add Tips sections to 3 files
- **Batch 3**: Add Variables section to 1 file

---

## Phase 4: Execution Summary

### Files Modified

| File | Change | Status |
|------|--------|--------|
| `chain-of-thought-concise.md` | Added Example + Tips | ✅ |
| `rag-document-retrieval.md` | Added Example | ✅ |
| `react-tool-augmented.md` | Added Example + Variables | ✅ |
| `tree-of-thoughts-template.md` | Added Tips | ✅ |
| `reflection-self-critique.md` | Added Tips | ✅ |

### Validation After Changes

```text
python tools/validate_prompts.py prompts/advanced/
✅ Validated 21 files
✅ Files with issues: 0
✅ All files pass frontmatter and section requirements
```

### Quality Metrics

| Metric | Before | After | Δ |
|--------|--------|-------|---|
| Validation Pass Rate | 76% | 100% | +24% |
| Avg Quality Score | 72/100 | 81/100 | +9 |
| Files with Examples | 17/21 | 21/21 | +4 |
| Files with Tips | 18/21 | 21/21 | +3 |

---

## Recommendations

### Immediate (This Session)

1. ✅ Completed - All validation issues resolved

### Short-Term (Next Sprint)

1. Expand example depth in 5 prompts (currently < 10 lines)
2. Add platform-specific variations to 3 prompts

### Medium-Term (Next Month)

1. Create advanced pattern cross-references
2. Add Mermaid diagrams to 4 methodology prompts

```

---

## Tips

- **Start with validation baseline**: Always run `python tools/validate_prompts.py` before and after changes to track progress quantitatively.
- **Batch by missing section**: Group files by the same missing section type (e.g., all files missing "Example") to apply consistent fixes efficiently.
- **Use the dry-run flag**: Run `python tools/evaluation_agent.py --full --dry-run` to preview the execution plan before making changes.
- **Preserve original intent**: When adding missing sections, read the existing prompt carefully to ensure new content aligns with the author's original purpose.
- **Leverage ToT backtracking**: If a branch leads to a dead end (e.g., a file can't be fixed without a rewrite), explicitly document why and move to the next branch.
- **Check for cascading effects**: After fixing one file, re-run validation to ensure no new issues were introduced.
- **Use Reflexion iteratively**: If the self-critique reveals gaps, loop back to Phase 2 with a targeted follow-up action rather than restarting from scratch.

## Methodology Overview

```mermaid
flowchart TD
    subgraph Phase1["Phase 1: ToT Research Planning"]
        A["Research Question"] --> B["Generate 3-5 Research Branches"]
        B --> C["Prioritize Top 3 Branches"]
    end
    
    subgraph Phase2["Phase 2: ReAct Execution"]
        C --> D["Branch A: Thought → Action → Observe"]
        C --> E["Branch B: Thought → Action → Observe"]
        C --> F["Branch C: Thought → Action → Observe"]
    end
    
    subgraph Phase3["Phase 3: Reflexion"]
        D & E & F --> G["Self-Critique Questions"]
        G --> H{"Gaps Remain?"}
        H -->|Yes| I["Targeted Follow-up"]
        H -->|No| J["Proceed to Synthesis"]
        I --> G
    end
    
    subgraph Phase4["Phase 4: Synthesis"]
        J --> K["Compile Findings"]
        K --> L["Generate Deliverables"]
        L --> M["Quality Score + Recommendations"]
    end
    
    style Phase1 fill:#e1f5fe
    style Phase2 fill:#fff3e0
    style Phase3 fill:#e8f5e9
    style Phase4 fill:#fce4ec
```

---

## Current Repository Context

> **Repository**: `tafreeman/prompts`  
> **Last Evaluation**: January 2, 2026 (run new baseline)  
> **Prompt Count**: 190 prompts across 9 categories  
> **Validation Status**: 18 files with issues (missing Example sections)

### Completed Infrastructure ✅

| Component | Status | Details |
|-----------|--------|---------|
| Frontmatter schema | ✅ Complete | 19 standardized fields, fully validated |
| Content types | ✅ Complete | conceptual, quickstart, how_to, tutorial, reference, troubleshooting |
| Validation tooling | ✅ Complete | `tools/validate_prompts.py` |
| Evaluation tooling | ✅ Complete | `tools/evaluation_agent.py`, `python -m prompteval` |
| Navigation structure | ✅ Complete | All `index.md` files created with proper frontmatter |
| Advanced techniques | ✅ Complete | CoT, ToT, ReAct, RAG, CoVe, Reflexion |

### Current Content Inventory (January 2026)

| Category | Count | Status | Notes |
|----------|-------|--------|-------|
| **Business** | 39 prompts | ✅ Mature | Largest category |
| **Developers** | 27 prompts | ✅ Mature | Core dev workflows |
| **System** | 23 prompts | ✅ Mature | Agent/system prompts |
| **Advanced** | 21 prompts | ✅ Mature | Complex patterns |
| **Analysis** | 20 prompts | ✅ Mature | Data/research |
| **M365** | 20 prompts | ✅ Mature | Microsoft 365 |
| **Governance** | 16 prompts | ✅ **COMPLETE** | Target exceeded! |
| **SOCMINT** | 15 prompts | ✅ New | OSINT/investigation |
| **Creative** | 9 prompts | ⚠️ **GAP** | Need +11 prompts |
| **Total** | **190 prompts** | | +25 since Dec 2025 |

### Evaluation Tools Available

| Tool | Command | Purpose |
|------|---------|---------|
| Full Evaluation | `python tools/evaluation_agent.py --full` | Autonomous multi-phase evaluation |
| Dry Run | `python tools/evaluation_agent.py --full --dry-run` | Preview evaluation plan |
| Library Scorer | `python tools/evaluate_library.py --all` | Dual-rubric scoring |
| Validation | `python tools/validate_prompts.py` | Frontmatter compliance |
| Audit | `python tools/audit_prompts.py` | Content audit CSV |

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
- [x] Governance category expansion (16 prompts) ✅
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
- [x] Compliance-specific prompt packs (HIPAA, SOX, GDPR) ✅
- [ ] Cost optimization guidance
- [ ] SLA and performance benchmarks

---

## Priority Expansion Areas (January 2026)

### ~~P0 - Critical: Governance Category~~ ✅ COMPLETE (16 prompts)

**Status**: Target exceeded! 16 governance prompts now available.

<details>
<summary>Current Governance Prompts (click to expand)</summary>

| Prompt | Status |
|--------|--------|
| `access-control-reviewer.md` | ✅ |
| `ai-ml-privacy-risk-assessment.md` | ✅ |
| `compliance-policy-generator.md` | ✅ |
| `data-classification-helper.md` | ✅ |
| `data-retention-policy.md` | ✅ |
| `data-subject-request-handler.md` | ✅ |
| `gdpr-compliance-assessment.md` | ✅ |
| `hipaa-compliance-checker.md` | ✅ |
| `legal-contract-review.md` | ✅ |
| `privacy-impact-assessment.md` | ✅ |
| `regulatory-change-analyzer.md` | ✅ |
| `risk-assessment.md` | ✅ |
| `security-incident-response.md` | ✅ |
| `soc2-audit-preparation.md` | ✅ |
| `sox-audit-preparer.md` | ✅ |
| `vendor-security-review.md` | ✅ |

</details>

### P0 - Critical: Creative Category (9 → 20 prompts)

**Gap**: Marketing and content teams need more variety. **11 prompts needed.**

**Current Creative Prompts (9)**:

- `ad-copy-generator.md`, `brand-voice-developer.md`, `content-marketing-blog-post.md`
- `email-newsletter-writer.md`, `headline-tagline-creator.md`, `marketing-campaign-strategist.md`
- `product-description-generator.md`, `social-media-content-generator.md`, `video-script-writer.md`

**Recommended Additions (11)**:

| Prompt | Type | Difficulty | Effort | Priority |
|--------|------|------------|--------|----------|
| `case-study-builder.md` | how_to | intermediate | M | High |
| `whitepaper-outliner.md` | how_to | intermediate | M | High |
| `press-release-generator.md` | how_to | beginner | S | High |
| `landing-page-copy.md` | how_to | intermediate | M | High |
| `seo-content-optimizer.md` | how_to | intermediate | M | Medium |
| `podcast-script-writer.md` | how_to | intermediate | M | Medium |
| `webinar-content-creator.md` | how_to | intermediate | M | Medium |
| `customer-testimonial-formatter.md` | how_to | beginner | S | Low |
| `infographic-content-planner.md` | how_to | beginner | S | Low |
| `content-calendar-generator.md` | how_to | beginner | S | Low |
| `ab-test-copy-variants.md` | how_to | intermediate | M | Medium |

### P1 - High: Advanced Patterns

**Gap**: Power users need more sophisticated patterns.

| Prompt | Type | Difficulty | Effort |
|--------|------|------------|--------|
| `prompt-chain-orchestrator.md` | tutorial | advanced | L |
| `multi-model-router.md` | how_to | advanced | L |
| `context-window-optimizer.md` | how_to | advanced | M |
| `prompt-ab-testing-framework.md` | tutorial | advanced | L |
| `vision-prompt-templates.md` | reference | intermediate | M |
| `structured-output-patterns.md` | reference | intermediate | M |

### P2 - Medium: Industry Packs

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

When executing this analysis, you have access to these tool categories:

### 1. Workspace Navigation

| Tool | Usage | Example |
|------|-------|---------|
| `file_search` | Find files by glob pattern | `file_search("prompts/**/*.md")` |
| `list_dir` | List directory contents | `list_dir("/prompts/")` |
| `read_file` | Read file contents | `read_file("prompts/developers/code-review.md", 1, 50)` |
| `grep_search` | Search content patterns | `grep_search("governance_tags:", isRegexp=false)` |
| `semantic_search` | Semantic code search | `semantic_search("chain of thought prompts")` |

### 2. Evaluation & Validation

| Tool | Command | Purpose |
|------|---------|---------|
| Full Evaluation | `python tools/evaluation_agent.py --full` | Autonomous multi-phase scoring |
| Dry Run | `python tools/evaluation_agent.py --full --dry-run` | Preview evaluation plan |
| Library Scorer | `python tools/evaluate_library.py --all` | Dual-rubric scoring |
| Validation | `python tools/validate_prompts.py` | Frontmatter compliance |
| Audit | `python tools/audit_prompts.py` | Content audit CSV |

### 3. External Research (MCP Tools)

| Tool | Purpose |
|------|---------|
| `fetch_webpage` | Fetch content from URLs for research |
| `github_repo` | Search GitHub repos for prompt examples |
| `mcp_context7_get-library-docs` | Get library documentation |
| `mcp_microsoft_doc_*` | Search Microsoft/Azure documentation |

### 4. Execution

| Tool | Purpose |
|------|---------|
| `run_in_terminal` | Execute Python scripts, validation, git commands |
| `create_file` | Create new prompt files |
| `replace_string_in_file` | Edit existing content |

---

## ToT-ReAct Execution Protocol

Execute using the 4-phase methodology shown above. Each phase builds on the previous.

### Phase 1: ToT Research Planning

**Generate 3-5 Research Branches** for the evaluation goal:

```markdown
## Research Branches for Library Evaluation

### Branch A: Structural Quality Analysis
- Question: How well-organized is the prompt library structure?
- Approach: Map directories, validate frontmatter, check index.md files
- Priority: High (foundational)

### Branch B: Content Coverage Assessment  
- Question: What content gaps exist across categories and audiences?
- Approach: Count by type/platform/difficulty, compare to targets
- Priority: High (roadmap input)

### Branch C: Academic Best Practices Comparison
- Question: How does this library compare to published prompting research?
- Approach: Research CoT, ToT, Reflexion patterns; compare to library coverage
- Priority: Medium (quality improvement)

### Branch D: Scoring & Benchmarking
- Question: What is the current quality score using dual rubrics?
- Approach: Run evaluation_agent.py, analyze per-category scores
- Priority: High (baseline)

### Branch E: External Competitive Analysis
- Question: How does this compare to other public prompt libraries?
- Approach: Analyze awesome-prompts, dair-ai/Prompt-Engineering-Guide
- Priority: Low (future expansion)
```

**Prioritize Top 3**: Select A, B, D for core evaluation; C, E for enhancement.

---

### Phase 2: ReAct Execution (Per Branch)

For each prioritized branch, execute Thought → Action → Observe cycles:

#### Branch A: Structural Quality

**Cycle 1 - Structure Mapping**

```text
Thought: I need to understand the repository folder hierarchy.
Action: list_dir("d:/source/tafreeman/prompts/prompts/")
Observe: [Record categories and counts]
```

**Cycle 2 - Frontmatter Audit**

```text
Thought: I need to verify all files comply with the frontmatter schema.
Action: run_in_terminal("python tools/validate_prompts.py")
Observe: [Record validation results, note failures]
```

**Cycle 3 - Governance Compliance**

```text
Thought: I need to check governance field coverage.
Action: grep_search("governance_tags:|dataClassification:", isRegexp=true)
Observe: [Calculate compliance percentage]
```

#### Branch B: Content Coverage

**Cycle 1 - Type Distribution**

```text
Thought: I need to count prompts by content type.
Action: grep_search("type: quickstart|type: how_to|type: tutorial", isRegexp=true)
Observe: [Create type distribution table]
```

**Cycle 2 - Platform Coverage**

```text
Thought: I need to verify multi-platform coverage.
Action: grep_search("platforms:.*github-copilot|platforms:.*claude|platforms:.*chatgpt", isRegexp=true)
Observe: [Create platform coverage matrix]
```

**Cycle 3 - Audience Analysis**

```text
Thought: I need to check audience distribution.
Action: grep_search("audience:.*junior|audience:.*senior|audience:.*architect", isRegexp=true)
Observe: [Create audience coverage table]
```

#### Branch D: Scoring & Benchmarking

**Cycle 1 - Run Full Evaluation**

```text
Thought: I need current quality scores using dual rubrics.
Action: run_in_terminal("python tools/evaluation_agent.py --full --verbose")
Observe: [Record overall score, per-category breakdown]
```

**Cycle 2 - Identify Low Scorers**

```text
Thought: I need to find prompts scoring below threshold.
Action: read_file("docs/reports/EVALUATION_REPORT.md", 1, 200)
Observe: [List prompts needing improvement, by priority]
```

---

### Phase 3: Reflexion Self-Critique

After completing ReAct cycles, apply structured self-critique:

```markdown
## Reflexion Questions

### Completeness Check
1. Did I evaluate ALL prompt categories? [Yes/No - list any missed]
2. Did I check BOTH rubrics (Quality 0-100 AND Effectiveness 1.0-5.0)?
3. Did I compare against target counts for each category?

### Accuracy Verification  
4. Are my counts accurate? [Re-verify with file_search if uncertain]
5. Did validation pass? [If failures, list specific files]
6. Are scores from the LATEST evaluation run?

### Gap Identification
7. What categories are below target count? [List with current/target]
8. What content types are underrepresented? [quickstart, tutorial, etc.]
9. What audiences lack coverage? [junior, senior, architect, etc.]

### Improvement Opportunities
10. Which 5 prompts would benefit most from improvement?
11. What new prompts would have highest impact?
12. Are there emerging techniques not yet covered? [Reflexion, Agentic, etc.]
```

**If gaps remain**: Return to Phase 2 for targeted follow-up actions.

---

### Phase 4: Synthesis & Deliverables

Compile findings into structured outputs:

#### Deliverable 1: Repository Structure Map

```markdown
## Repository Structure (as of YYYY-MM-DD)

prompts/
├── advanced/ (X prompts) - Tier 1
├── analysis/ (X prompts) - Tier 2
├── business/ (X prompts) - Tier 2  
├── creative/ (X prompts) - Tier 3 ⚠️
├── developers/ (X prompts) - Tier 2
├── governance/ (X prompts) - Tier 3 ⚠️
├── m365/ (X prompts) - Tier 2
└── system/ (X prompts) - Tier 2

Total: X prompts | Validation: X% pass | Overall Score: X/100
```

#### Deliverable 2: Quality Scorecard

```markdown
| Category | Count | Quality Score | Effectiveness | Trend |
|----------|-------|---------------|---------------|-------|
| Advanced | X | X/100 | X.X/5.0 | ↑↓→ |
| Analysis | X | X/100 | X.X/5.0 | ↑↓→ |
| ... | ... | ... | ... | ... |
| **Overall** | **X** | **X/100** | **X.X/5.0** | **→** |
```

#### Deliverable 3: Gap Analysis Matrix

```markdown
| Dimension | Current | Target | Gap | Priority |
|-----------|---------|--------|-----|----------|
| Governance prompts | X | 15 | X | P0 |
| Creative prompts | X | 20 | X | P1 |
| Industry packs | 0 | 45 | 45 | P2 |
| Multi-modal | 0 | 10 | 10 | P3 |
```

#### Deliverable 4: Prioritized Recommendations

```markdown
## Immediate Actions (This Sprint)
1. [Specific prompt to create or improve]
2. [Specific prompt to create or improve]

## Short-Term (Next 2 Weeks)
1. [Category expansion goal]
2. [Quality improvement target]

## Medium-Term (Next Month)
1. [New capability to add]
2. [Research area to explore]
```

#### Deliverable 5: Execution Commands

```powershell
# Validation
python tools/validate_prompts.py

# Full Evaluation (generates reports)
python tools/evaluation_agent.py --full --verbose

# Audit CSV Export
python tools/audit_prompts.py --output audit_report.csv

# Count by Category
Get-ChildItem -Path "prompts/*" -Directory | ForEach-Object { 
  "$($_.Name): $((Get-ChildItem $_.FullName -Filter *.md -Recurse).Count)" 
}
```

---

## Expansion Priorities

Based on December 2025 repository state, focus analysis on these maturity areas:

### ~~Governance Category~~ ✅ COMPLETE (16 prompts)

**Status**: Target exceeded. Enterprise compliance coverage achieved.

**Coverage Areas**:

- ✅ Regulatory compliance (GDPR, HIPAA, SOX, SOC2)
- ✅ Security review and incident response
- ✅ Policy and procedure generation
- ✅ Risk assessment and mitigation
- ✅ Data classification and retention
- ✅ Privacy impact assessments
- ✅ AI/ML-specific privacy risks

### Creative Category (CRITICAL - 9 prompts → 20 target)

**Why Critical**: Now the #1 gap. Content and marketing teams drive significant AI adoption.

**Current Prompts (9)**:

- `ad-copy-generator.md`
- `brand-voice-developer.md`
- `content-marketing-blog-post.md`
- `email-newsletter-writer.md`
- `headline-tagline-creator.md`
- `marketing-campaign-strategist.md`
- `product-description-generator.md`
- `social-media-content-generator.md`
- `video-script-writer.md`

**Research Focus Areas**:

- Long-form content (whitepapers, case studies)
- SEO and content optimization
- Multimedia content (podcasts, webinars)
- Campaign and launch content
- Content planning and strategy

**Recommended Additions (11 needed)**:

| # | Prompt | Description | Priority |
|---|--------|-------------|----------|
| 1 | `case-study-builder.md` | Customer success stories | High |
| 2 | `whitepaper-outliner.md` | Long-form technical content | High |
| 3 | `press-release-generator.md` | Media announcements | High |
| 4 | `landing-page-copy.md` | Conversion-focused web copy | High |
| 5 | `seo-content-optimizer.md` | Search optimization | Medium |
| 6 | `podcast-script-writer.md` | Audio content scripts | Medium |
| 7 | `webinar-content-creator.md` | Presentation content | Medium |
| 8 | `customer-testimonial-formatter.md` | Quote formatting | Low |
| 9 | `infographic-content-planner.md` | Visual content planning | Low |
| 10 | `content-calendar-generator.md` | Editorial planning | Low |
| 11 | `ab-test-copy-variants.md` | A/B testing variations | Medium |

### Advanced Patterns (HIGH - Add sophisticated capabilities)

**Why High**: Power users and architects need advanced patterns.

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

### Quick Start

```powershell
# 1. Run automated evaluation (recommended)
python tools/evaluation_agent.py --full --verbose

# 2. Or execute this prompt manually in an AI assistant
# Load this file in Claude, GPT-4, or GitHub Copilot Chat
# The agent will follow the ToT-ReAct protocol above
```

### Manual Execution Steps

1. **Phase 1 - ToT Planning**: Generate 3-5 research branches for your evaluation goal
2. **Phase 2 - ReAct Execution**: For each branch, execute Thought → Action → Observe cycles
3. **Phase 3 - Reflexion**: Apply self-critique questions, iterate if gaps remain
4. **Phase 4 - Synthesis**: Compile the 5 deliverables

### Validation Commands

```powershell
# Frontmatter validation
python tools/validate_prompts.py

# Full evaluation with reports
python tools/evaluation_agent.py --full --verbose

# Dry run (preview only)
python tools/evaluation_agent.py --full --dry-run

# Content audit CSV
python tools/audit_prompts.py --output audit_report.csv

# Count prompts by category
Get-ChildItem -Path "prompts/*" -Directory | ForEach-Object { 
  "$($_.Name): $((Get-ChildItem $_.FullName -Filter *.md -Recurse).Count)" 
}
```

### Previous Evaluations

| Document | Date | Score | Notes |
|----------|------|-------|-------|
| *Run new evaluation* | 2026-01-02 | TBD | Current state baseline |
| `docs/TOT_EVALUATION_REPORT.md` | 2025-12-05 | 79/100 | Tree-of-Thoughts evaluation |
| `docs/evaluations/EVALUATION_REPORT_*.md` | 2025-12-04 | 79/100 | Archived baseline reports |

---

## Related Resources

- [Evaluation Agent Guide](../../tools/archive/EVALUATION_AGENT_GUIDE.md) - Detailed agent documentation
- [Validate Prompts](../../tools/validate_prompts.py) - Frontmatter validation
- [Evaluate Library](../../tools/evaluate_library.py) - Dual-rubric scoring
- [Frontmatter Schema](../../reference/frontmatter-schema.md) - Field definitions
- [Content Types](../../reference/content-types.md) - Type selection guide
- [Advanced Techniques](../../techniques/index.md) - CoT, ToT, Reflexion patterns
