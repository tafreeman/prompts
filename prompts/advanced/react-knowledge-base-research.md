---
title: "ReAct: Knowledge Base Research"
shortTitle: "KB Research"
intro: "A ReAct prompt for researching documentation best practices from industry leaders."
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
  - "documentation"
  - "architecture"
  - "react"
author: "Prompt Library Team"
version: "2.3"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "approved"
---
# ReAct: Knowledge Base Research

## Description

Use this prompt to research how leading technology companies structure their documentation, then synthesize findings into actionable recommendations for improving a prompt library or knowledge base. This includes identifying what content is essential versus bloated, and researching current prompt scoring/rating methodologies.

## When to Use

- Expanding content categories (creative, business, etc.)
- Benchmarking against industry documentation leaders
- **Simplifying prompts** to only essential, high-value content
- Researching **prompt scoring and rating systems**
- Planning new navigation or content type features
- Researching prompt patterns from OpenAI, Anthropic, etc.

---

## Prompt

```text
You are an AI research assistant using the ReAct (Reasoning + Acting) pattern to research best practices for knowledge bases and documentation systems.

## Your Task

Research how leading technology companies structure their documentation, then synthesize findings into actionable recommendations. Additionally:

1. **Simplify**: Identify what content is essential vs. unnecessary bloat
2. **Score**: Research current prompt scoring and rating methodologies
3. **Expand**: Research and add prompts across ALL library sections

## Research Goals

### Goal 1: Content Simplification

Determine what makes a prompt document effective and minimal:

- What fields/sections are truly necessary?
- What can be removed without losing value?
- How do top libraries balance completeness vs. brevity?

### Goal 2: Prompt Scoring & Rating

Research current methodologies for evaluating prompt quality:

- What metrics do leading AI companies use?
- How are prompts rated for effectiveness?
- What scoring rubrics exist in the industry?

### Goal 3: Content Expansion (All Sections)

Research and identify new prompts to add across ALL library categories:

- What prompts are missing in each section?
- What do industry leaders offer that we don't?
- What emerging use cases should we cover?
- How do we balance breadth vs. depth per category?

## Research Question

[RESEARCH_QUESTION]

## Context

[CONTEXT_ABOUT_YOUR_PROJECT]

## Research Targets

### Tier 1: Documentation Leaders

| Source | URL | Focus |
|--------|-----|-------|
| GitHub Docs | docs.github.com | Content types, frontmatter, navigation |
| Microsoft Learn | learn.microsoft.com | Enterprise scale, learning paths |
| Stripe Docs | stripe.com/docs | Clarity, copy patterns |

### Tier 2: AI Documentation

| Source | URL | Focus |
|--------|-----|-------|
| OpenAI Cookbook | cookbook.openai.com | Prompt examples, variations |
| Anthropic Docs | docs.anthropic.com | Claude patterns, best practices |
| GitHub Copilot Docs | docs.github.com/copilot | Code generation prompts |

### Tier 3: Creative & Business

| Source | URL | Focus |
|--------|-----|-------|
| Copy.ai | copy.ai | Marketing copy patterns |
| Jasper | jasper.ai | Business writing |
| HubSpot | hubspot.com | Sales/marketing content |

### Tier 4: Prompt Scoring & Evaluation

| Source | URL | Focus |
|--------|-----|-------|
| OpenAI Evals | github.com/openai/evals | Evaluation frameworks |
| LangSmith | docs.smith.langchain.com | Prompt testing & scoring |
| PromptLayer | promptlayer.com | Prompt analytics |
| Humanloop | humanloop.com | Prompt optimization metrics |
| HELM Benchmark | crfm.stanford.edu/helm | Holistic evaluation |

## Instructions

Use the Think → Act → Observe → Reflect cycle:

**Thought [N]**: What am I investigating? Which source is most relevant?

**Action [N]**: Search or fetch documentation from the source.

**Observation [N]**: What patterns did I find? Key structures, fields, approaches?

**Reflection [N]**: How does this apply to the research question? What should I recommend?

Continue until you have:

- [ ] Researched at least 3 sources
- [ ] Identified common patterns
- [ ] Found differences worth noting
- [ ] Formed actionable recommendations
- [ ] Identified what to REMOVE (simplification)
- [ ] Documented prompt scoring criteria
- [ ] Identified new prompts to ADD per section

## Deliverables

### 1. Research Summary Table

| Aspect | Source 1 | Source 2 | Source 3 | Best Practice |
|--------|----------|----------|----------|---------------|
| Content Types | ... | ... | ... | ... |
| Structure | ... | ... | ... | ... |
| Navigation | ... | ... | ... | ... |
| Key Pattern | ... | ... | ... | ... |

### 2. Simplification Analysis

| Current Element | Keep/Remove | Rationale | Industry Support |
|-----------------|-------------|-----------|------------------|
| ... | ✅ Keep / ❌ Remove | ... | X of Y sources use this |

### 3. Prompt Scoring Rubric

| Dimension | Weight | Criteria | Score Range |
|-----------|--------|----------|-------------|
| Clarity | ...% | ... | 1-5 |
| Effectiveness | ...% | ... | 1-5 |
| Reusability | ...% | ... | 1-5 |
| ... | ... | ... | ... |

### 4. Recommendations

For each recommendation:

- **Pattern**: What to implement
- **Evidence**: Which sources use this
- **Application**: How to apply it
- **Priority**: P0/P1/P2
- **Effort**: Low/Medium/High

### 5. Simplification Actions

What to REMOVE from prompts:

| Remove This | Why | Savings |
|-------------|-----|---------|
| ... | Not used by industry leaders | -X lines avg |

### 6. Scoring Implementation Plan

How to implement prompt scoring in the library:

- Recommended scoring dimensions
- Automation possibilities
- Review workflow integration

### 7. New Prompts by Section

Prompts to ADD across all library categories:

| Section | Current | Target | New Prompts to Add |
|---------|---------|--------|--------------------|
| Creative | 2 | 15-20 | [list specific prompts] |
| Business | 26 | 35-40 | [list specific prompts] |
| Developers | 15+ | 25+ | [list specific prompts] |
| Analysis | 10+ | 15+ | [list specific prompts] |
| Advanced | 20+ | 25+ | [list specific prompts] |
| Governance | 5+ | 10+ | [list specific prompts] |
| M365 | 10+ | 20+ | [list specific prompts] |
| System | 5+ | 10+ | [list specific prompts] |

For each new prompt:
- Name and description
- Difficulty level
- Source/inspiration
- Priority (P0/P1/P2)

### 8. Specific Actions

Prioritized list of changes with:

- Task description
- Supporting evidence
- Estimated effort
```

---

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[RESEARCH_QUESTION]` | The specific question to answer | "What are best practices for organizing creative writing prompts?" |
| `[CONTEXT_ABOUT_YOUR_PROJECT]` | Background on your project | "A prompt library with 145 prompts, expanding creative section from 2 to 20 prompts" |

---

## Example Usage: Simplification & Scoring Research

### Input

```text
## Research Question

What is the minimal effective structure for prompt documents, and what scoring systems are used to rate prompt quality?

## Context

Project: tafreeman/prompts - A prompt library with 145+ prompts
Problem: Current prompts may have unnecessary sections/fields
Goal: 1) Simplify to essential content only, 2) Implement prompt scoring
```

### Expected Output

```text
**Thought 1**: I'll research OpenAI's prompt examples first - they're the industry leader and likely have a minimal, effective format.

**Action 1**: Analyze OpenAI Cookbook prompt structure.

**Observation 1**: OpenAI prompts are remarkably simple:
- Title
- Brief description (1-2 sentences)
- The prompt itself
- 1 example (input/output)
- NO extensive metadata, NO lengthy explanations

**Reflection 1**: Our prompts may be over-engineered. OpenAI proves minimal works.

---

**Thought 2**: Now I'll research prompt evaluation frameworks to understand scoring.

**Action 2**: Research LangSmith and OpenAI Evals scoring approaches.

**Observation 2**: Common scoring dimensions:
- **Relevance**: Does output match intent? (0-1)
- **Coherence**: Is output well-structured? (0-1)
- **Groundedness**: Is output factually accurate? (0-1)
- **Fluency**: Is output well-written? (0-1)
- **Task Completion**: Did it achieve the goal? (0-1)

---

## Simplification Analysis

| Current Element | Keep/Remove | Rationale |
|-----------------|-------------|-----------|
| Title | ✅ Keep | Universal - all sources use |
| Description | ✅ Keep | All sources have brief intro |
| Prompt text | ✅ Keep | Core content |
| 1-2 Examples | ✅ Keep | Industry standard |
| Variables table | ✅ Keep | Useful for customization |
| Frontmatter (minimal) | ✅ Keep | Needed for tooling |
| Lengthy "When to Use" | ❌ Remove | Merge into description |
| Multiple tip sections | ❌ Remove | Keep to 3-5 bullets max |
| Extensive changelog | ❌ Remove | Use git history instead |
| Related prompts (long) | ⚠️ Simplify | Keep to 2-3 max |

## Prompt Scoring Rubric (Recommended)

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Clarity | 25% | Is the prompt unambiguous? |
| Effectiveness | 30% | Does it produce quality output? |
| Reusability | 20% | Works across contexts? |
| Simplicity | 15% | Minimal without losing value |
| Examples | 10% | Are examples helpful? |

**Scoring Scale**: 1-5 stars, automated where possible
```

---

## Example Usage: Content Expansion

### Input

```text
## Research Question

What are best practices for structuring creative writing and content generation prompts that serve multiple skill levels?

## Context

Project: tafreeman/prompts - A prompt library for AI-assisted work
Current State: 145 prompts total, only 2 in creative category
Goal: Expand creative prompts to 15-20, covering writing, marketing, editing, storytelling
Target Users: Business professionals, marketing teams, content creators
```

### Expected Output

```text
**Thought 1**: I'll start with Copy.ai since they specialize in creative content templates. Their organization of marketing and writing prompts will be directly applicable.

**Action 1**: Research Copy.ai template categories and structure.

**Observation 1**: Copy.ai organizes templates by:
- Use case (blog posts, emails, ads, social)
- Output length (short-form vs long-form)
- Tone/style options built into templates
- Industry verticals (ecommerce, SaaS, etc.)

**Reflection 1**: Key insight: they separate templates by OUTPUT TYPE not INPUT TYPE. A "Blog Post" template is different from an "Ad Copy" template even though both are "writing." This is user-centric organization.

---

**Thought 2**: Now I'll check Anthropic's prompt library to see how they structure examples for Claude.

**Action 2**: Research Anthropic's prompt examples and documentation structure.

**Observation 2**: Anthropic organizes by:
- Task category (analysis, writing, coding, math)
- Complexity level
- Each prompt includes: description, prompt text, example output
- They show variations for different use cases

**Reflection 2**: Anthropic uses a simpler category scheme but includes rich examples. The "show expected output" pattern is valuable for creative prompts where quality is subjective.

---

[Continue for 2-3 more cycles...]

---

## Research Summary Table

| Aspect | Copy.ai | Anthropic | Jasper | Best Practice |
|--------|---------|-----------|--------|---------------|
| Organization | By output type | By task category | By use case + industry | Output type + audience |
| Skill levels | Implicit in complexity | Explicit complexity tags | Templates vs custom | Add difficulty field |
| Examples | Before/after | Full output | Variations | Include 2+ examples |
| Customization | Tone, length, style inputs | System prompt guidance | Brand voice settings | Add variables section |

## Recommendations

**1. Organize by Output Type**

- Pattern: Group prompts by what they produce (emails, posts, ads) not how they work
- Evidence: Copy.ai, Jasper both use this
- Application: Create subfolders: creative/emails/, creative/social/, creative/long-form/
- Priority: P0
- Effort: Medium

**2. Include Rich Examples**

- Pattern: Show 2+ example outputs for each creative prompt
- Evidence: Anthropic shows full outputs; Copy.ai shows before/after
- Application: Add "Example Output" section to all creative prompts
- Priority: P0
- Effort: High

**3. Add Tone/Style Variables**

- Pattern: Let users specify tone (formal/casual), length, audience
- Evidence: All three sources include customization options
- Application: Add [TONE], [LENGTH], [AUDIENCE] variables
- Priority: P1
- Effort: Low
```

---

## Tips

- **Start with the most specialized source** for your topic (Copy.ai for creative, Stripe for API docs)
- **Look for contributing guides** - they often explain the content model
- **Note the differences** - where sources disagree may indicate context-dependent choices
- **Focus on actionable patterns** - skip things that don't apply to your project
- **Cite everything** - recommendations are stronger with multiple sources
- **Favor simplicity** - if top sources don't use a feature, question whether you need it
- **Research scoring early** - understand how to measure prompt quality before creating more

---

## Current Repository Context

For reference when researching, our library currently has:

| Category | Count | Target | Status | Expansion Ideas |
|----------|-------|--------|--------|------------------|
| Creative | 2 | 15-20 | 🔴 Critical | Writing, marketing, editing, storytelling |
| Business | 26 | 35-40 | 🟡 Expand | Sales, HR, exec comms, operations |
| Developers | 15+ | 25+ | 🟡 Expand | Testing, DevOps, architecture, debugging |
| Analysis | 10+ | 15+ | 🟡 Expand | Data viz, reporting, competitive analysis |
| Advanced | 20+ | 25+ | 🟢 Good | Multi-agent, RAG patterns, fine-tuning |
| Governance | 5+ | 10+ | 🟡 Expand | Compliance, risk, audit, policy |
| M365 | 10+ | 20+ | 🟡 Expand | Teams, SharePoint, Power Platform |
| System | 5+ | 10+ | 🟡 Expand | Agent configs, personas, guardrails |

**Expansion Priorities (All Sections):**

| Priority | Section | Current → Target | Focus Areas |
|----------|---------|------------------|-------------|
| P0 | Creative | 2 → 15-20 | Writing, marketing, editing, storytelling |
| P0 | Business | 26 → 35-40 | Sales, HR, executive comms, operations |
| P1 | M365 | 10+ → 20+ | Teams, SharePoint, Power Platform, Outlook |
| P1 | Developers | 15+ → 25+ | Testing, DevOps, architecture, code review |
| P1 | Governance | 5+ → 10+ | Compliance, risk assessment, audit, policy |
| P2 | Analysis | 10+ → 15+ | Data viz, reporting, competitive intel |
| P2 | Advanced | 20+ → 25+ | Multi-agent, RAG, fine-tuning guides |
| P2 | System | 5+ → 10+ | Agent personas, guardrails, configurations |

**Simplification Targets:**

- Reduce average prompt length by 30-40%
- Remove redundant sections across all prompts
- Standardize to minimal effective structure

**Scoring Implementation:**

- Add `effectivenessScore` field to frontmatter
- Create automated scoring via `tools/validators/`
- Implement review workflow with scoring criteria

---

## Related Prompts

- [ReAct: Repository Analysis](prompt-library-refactor-react.md) - Analyze repository structure
- [ReAct: Tool-Augmented](react-tool-augmented.md) - General ReAct pattern with tools
- [Chain-of-Thought Debugging](chain-of-thought-debugging.md) - Step-by-step reasoning
