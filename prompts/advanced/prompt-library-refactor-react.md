---
name: Prompt Library Refactor React
description: ## Description
type: how_to
---
## Description

## Prompt

```

## Current Repository Context

> **Repository**: `tafreeman/prompts`  
> **Last Evaluation**: January 2, 2026 (run new baseline)  
> **Prompt Count**: 190 prompts across 9 categories  
> **Validation Status**: 18 files with issues (missing Example sections)

### Completed Infrastructure ✅

| Component | Status | Details |
| ----------- | -------- | --------- |
| Frontmatter schema | ✅ Complete | 19 standardized fields, fully validated |
| Content types | ✅ Complete | conceptual, quickstart, how_to, tutorial, reference, troubleshooting |
| Validation tooling | ✅ Complete | `tools/validate_prompts.py` |
| Evaluation tooling | ✅ Complete | `tools/evaluation_agent.py`, `python -m prompteval` |
| Navigation structure | ✅ Complete | All `index.md` files created with proper frontmatter |
| Advanced techniques | ✅ Complete | CoT, ToT, ReAct, RAG, CoVe, Reflexion |

### Current Content Inventory (January 2026)

| Category | Count | Status | Notes |
| ---------- | ------- | -------- | ------- |
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
| ------ | --------- | --------- |
| Full Evaluation | `python tools/evaluation_agent.py --full` | Autonomous multi-phase evaluation |
| Dry Run | `python tools/evaluation_agent.py --full --dry-run` | Preview evaluation plan |
| Library Scorer | `python tools/evaluate_library.py --all` | Dual-rubric scoring |
| Validation | `python tools/validate_prompts.py` | Frontmatter compliance |
| Audit | `python tools/audit_prompts.py` | Content audit CSV |

### Infrastructure Components

| Component | Count | Status |
| ----------- | ------- | -------- |
| Agents | 7 agents | ✅ docs, code-review, test, refactor, security, architecture, prompt |
| Instructions | 10 files | ✅ Role-based (junior/mid/senior), tech-specific |
| Techniques | 12 patterns | ✅ Reflexion, agentic, context optimization |
| Frameworks | 8 integrations | ✅ Anthropic, OpenAI, LangChain, Semantic Kernel |

## Priority Expansion Areas (January 2026)

### ~~P0 - Critical: Governance Category~~ ✅ COMPLETE (16 prompts)

**Status**: Target exceeded! 16 governance prompts now available.

<details>
<summary>Current Governance Prompts (click to expand)</summary>

| Prompt | Status |
| -------- | -------- |
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
| -------- | ------ | ------------ | -------- | ---------- |
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
| -------- | ------ | ------------ | -------- |
| `prompt-chain-orchestrator.md` | tutorial | advanced | L |
| `multi-model-router.md` | how_to | advanced | L |
| `context-window-optimizer.md` | how_to | advanced | M |
| `prompt-ab-testing-framework.md` | tutorial | advanced | L |
| `vision-prompt-templates.md` | reference | intermediate | M |
| `structured-output-patterns.md` | reference | intermediate | M |

### P2 - Medium: Industry Packs

**Gap**: Vertical-specific prompt collections.

| Pack | Prompts | Priority |
| ------ | --------- | ---------- |
| Healthcare | 10-15 | Future |
| Financial Services | 10-15 | Future |
| Legal | 10-15 | Future |
| Education | 10-15 | Future |
| Retail/E-commerce | 10-15 | Future |

## ToT-ReAct Execution Protocol

Execute using the 4-phase methodology shown above. Each phase builds on the previous.

### Phase 1: ToT Research Planning

**Generate 3-5 Research Branches** for the evaluation goal:

```

## Description

## Description

## Prompt

```

## Current Repository Context

> **Repository**: `tafreeman/prompts`  
> **Last Evaluation**: January 2, 2026 (run new baseline)  
> **Prompt Count**: 190 prompts across 9 categories  
> **Validation Status**: 18 files with issues (missing Example sections)

### Completed Infrastructure ✅

| Component | Status | Details |
| ----------- | -------- | --------- |
| Frontmatter schema | ✅ Complete | 19 standardized fields, fully validated |
| Content types | ✅ Complete | conceptual, quickstart, how_to, tutorial, reference, troubleshooting |
| Validation tooling | ✅ Complete | `tools/validate_prompts.py` |
| Evaluation tooling | ✅ Complete | `tools/evaluation_agent.py`, `python -m prompteval` |
| Navigation structure | ✅ Complete | All `index.md` files created with proper frontmatter |
| Advanced techniques | ✅ Complete | CoT, ToT, ReAct, RAG, CoVe, Reflexion |

### Current Content Inventory (January 2026)

| Category | Count | Status | Notes |
| ---------- | ------- | -------- | ------- |
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
| ------ | --------- | --------- |
| Full Evaluation | `python tools/evaluation_agent.py --full` | Autonomous multi-phase evaluation |
| Dry Run | `python tools/evaluation_agent.py --full --dry-run` | Preview evaluation plan |
| Library Scorer | `python tools/evaluate_library.py --all` | Dual-rubric scoring |
| Validation | `python tools/validate_prompts.py` | Frontmatter compliance |
| Audit | `python tools/audit_prompts.py` | Content audit CSV |

### Infrastructure Components

| Component | Count | Status |
| ----------- | ------- | -------- |
| Agents | 7 agents | ✅ docs, code-review, test, refactor, security, architecture, prompt |
| Instructions | 10 files | ✅ Role-based (junior/mid/senior), tech-specific |
| Techniques | 12 patterns | ✅ Reflexion, agentic, context optimization |
| Frameworks | 8 integrations | ✅ Anthropic, OpenAI, LangChain, Semantic Kernel |

## Priority Expansion Areas (January 2026)

### ~~P0 - Critical: Governance Category~~ ✅ COMPLETE (16 prompts)

**Status**: Target exceeded! 16 governance prompts now available.

<details>
<summary>Current Governance Prompts (click to expand)</summary>

| Prompt | Status |
| -------- | -------- |
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
| -------- | ------ | ------------ | -------- | ---------- |
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
| -------- | ------ | ------------ | -------- |
| `prompt-chain-orchestrator.md` | tutorial | advanced | L |
| `multi-model-router.md` | how_to | advanced | L |
| `context-window-optimizer.md` | how_to | advanced | M |
| `prompt-ab-testing-framework.md` | tutorial | advanced | L |
| `vision-prompt-templates.md` | reference | intermediate | M |
| `structured-output-patterns.md` | reference | intermediate | M |

### P2 - Medium: Industry Packs

**Gap**: Vertical-specific prompt collections.

| Pack | Prompts | Priority |
| ------ | --------- | ---------- |
| Healthcare | 10-15 | Future |
| Financial Services | 10-15 | Future |
| Legal | 10-15 | Future |
| Education | 10-15 | Future |
| Retail/E-commerce | 10-15 | Future |

## ToT-ReAct Execution Protocol

Execute using the 4-phase methodology shown above. Each phase builds on the previous.

### Phase 1: ToT Research Planning

**Generate 3-5 Research Branches** for the evaluation goal:

```

## Description


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

## Phase 1: ToT Research Planning

### Selected Branches

| Branch | Focus | Priority |
| -------- | ------- | ---------- |
| A | Structural Validation Audit | High |
| B | Missing Section Identification | High |
| C | Frontmatter Schema Compliance | Medium |

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

## Current Repository Context

> **Repository**: `tafreeman/prompts`  
> **Last Evaluation**: January 2, 2026 (run new baseline)  
> **Prompt Count**: 190 prompts across 9 categories  
> **Validation Status**: 18 files with issues (missing Example sections)

### Completed Infrastructure ✅

| Component | Status | Details |
| ----------- | -------- | --------- |
| Frontmatter schema | ✅ Complete | 19 standardized fields, fully validated |
| Content types | ✅ Complete | conceptual, quickstart, how_to, tutorial, reference, troubleshooting |
| Validation tooling | ✅ Complete | `tools/validate_prompts.py` |
| Evaluation tooling | ✅ Complete | `tools/evaluation_agent.py`, `python -m prompteval` |
| Navigation structure | ✅ Complete | All `index.md` files created with proper frontmatter |
| Advanced techniques | ✅ Complete | CoT, ToT, ReAct, RAG, CoVe, Reflexion |

### Current Content Inventory (January 2026)

| Category | Count | Status | Notes |
| ---------- | ------- | -------- | ------- |
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
| ------ | --------- | --------- |
| Full Evaluation | `python tools/evaluation_agent.py --full` | Autonomous multi-phase evaluation |
| Dry Run | `python tools/evaluation_agent.py --full --dry-run` | Preview evaluation plan |
| Library Scorer | `python tools/evaluate_library.py --all` | Dual-rubric scoring |
| Validation | `python tools/validate_prompts.py` | Frontmatter compliance |
| Audit | `python tools/audit_prompts.py` | Content audit CSV |

### Infrastructure Components

| Component | Count | Status |
| ----------- | ------- | -------- |
| Agents | 7 agents | ✅ docs, code-review, test, refactor, security, architecture, prompt |
| Instructions | 10 files | ✅ Role-based (junior/mid/senior), tech-specific |
| Techniques | 12 patterns | ✅ Reflexion, agentic, context optimization |
| Frameworks | 8 integrations | ✅ Anthropic, OpenAI, LangChain, Semantic Kernel |

## Priority Expansion Areas (January 2026)

### ~~P0 - Critical: Governance Category~~ ✅ COMPLETE (16 prompts)

**Status**: Target exceeded! 16 governance prompts now available.

<details>
<summary>Current Governance Prompts (click to expand)</summary>

| Prompt | Status |
| -------- | -------- |
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
| -------- | ------ | ------------ | -------- | ---------- |
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
| -------- | ------ | ------------ | -------- |
| `prompt-chain-orchestrator.md` | tutorial | advanced | L |
| `multi-model-router.md` | how_to | advanced | L |
| `context-window-optimizer.md` | how_to | advanced | M |
| `prompt-ab-testing-framework.md` | tutorial | advanced | L |
| `vision-prompt-templates.md` | reference | intermediate | M |
| `structured-output-patterns.md` | reference | intermediate | M |

### P2 - Medium: Industry Packs

**Gap**: Vertical-specific prompt collections.

| Pack | Prompts | Priority |
| ------ | --------- | ---------- |
| Healthcare | 10-15 | Future |
| Financial Services | 10-15 | Future |
| Legal | 10-15 | Future |
| Education | 10-15 | Future |
| Retail/E-commerce | 10-15 | Future |

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
| --- | -------- | ------------- | ---------- |
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
| ---------- | --------------- | -------------- |
| Healthcare | Patient communication, clinical documentation, HIPAA compliance | 10-15 |
| Financial Services | Risk analysis, regulatory reporting, fraud detection | 10-15 |
| Legal | Contract review, legal research, document drafting | 10-15 |
| Education | Curriculum design, assessment creation, student feedback | 10-15 |
| Retail/E-commerce | Product descriptions, customer service, inventory analysis | 10-15 |

## Related Resources

- [Evaluation Agent Guide](../../tools/archive/EVALUATION_AGENT_GUIDE.md) - Detailed agent documentation
- [Validate Prompts](../../tools/validate_prompts.py) - Frontmatter validation
- [Evaluate Library](../../tools/evaluate_library.py) - Dual-rubric scoring
- [Frontmatter Schema](../../reference/frontmatter-schema.md) - Field definitions
- [Content Types](../../reference/content-types.md) - Type selection guide
- [Advanced Techniques](../../techniques/index.md) - CoT, ToT, Reflexion patterns## Variables

_No bracketed variables detected._

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[Advanced Techniques]` | AUTO-GENERATED: describe `Advanced Techniques` |
| `[Content Types]` | AUTO-GENERATED: describe `Content Types` |
| `[Evaluate Library]` | AUTO-GENERATED: describe `Evaluate Library` |
| `[Evaluation Agent Guide]` | AUTO-GENERATED: describe `Evaluation Agent Guide` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Frontmatter Schema]` | AUTO-GENERATED: describe `Frontmatter Schema` |
| `[If failures, list specific files]` | AUTO-GENERATED: describe `If failures, list specific files` |
| `[List with current/target]` | AUTO-GENERATED: describe `List with current/target` |
| `[Re-verify with file_search if uncertain]` | AUTO-GENERATED: describe `Re-verify with file_search if uncertain` |
| `[Reflexion, Agentic, etc.]` | AUTO-GENERATED: describe `Reflexion, Agentic, etc.` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[Validate Prompts]` | AUTO-GENERATED: describe `Validate Prompts` |
| `[Yes/No - list any missed]` | AUTO-GENERATED: describe `Yes/No - list any missed` |
| `[junior, senior, architect, etc.]` | AUTO-GENERATED: describe `junior, senior, architect, etc.` |
| `[quickstart, tutorial, etc.]` | AUTO-GENERATED: describe `quickstart, tutorial, etc.` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

