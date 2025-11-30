---
title: "ReAct: Knowledge Base Architecture Research"
category: "advanced-techniques"
tags: ["react", "knowledge-base", "documentation", "research", "architecture", "best-practices"]
author: "Deloitte AI & Engineering Portfolio"
version: "1.0"
date: "2025-11-29"
difficulty: "advanced"
audience:
  - "solution-architect"
  - "senior-engineer"
governance_tags: ["internal-only", "architecture-guidance"]
platforms:
  - "github-copilot"
  - "claude"
  - "gpt-4"
type: "how_to"
estimatedTime: "45 min"
---

# ReAct: Knowledge Base Architecture Research

## Description

A ReAct (Reasoning + Acting) prompt for researching and synthesizing best practices from industry-leading knowledge bases (Microsoft Docs, GitHub Docs, OpenAI, Google, AWS, Anthropic) to inform the architecture of a prompt engineering library for Deloitte's AI & Engineering portfolio.

## Goal

Research how top technology companies structure their documentation and knowledge bases, then synthesize findings into actionable recommendations for refactoring the `tafreeman/prompts` repository.

## Context

**Project**: Refactoring a prompt library to serve multiple personas (junior engineers, senior engineers, architects, functional teams) with dual goals:
1. **Quick-Start**: Enable day-1 productivity with AI code generation
2. **Advanced Depth**: Provide sophisticated patterns for experienced practitioners

**Current State**: 137 prompts, 0 index files, inconsistent frontmatter, no learning tracks

**Target State**: GitHub Docs-inspired architecture with persona-aware navigation, content types, and enterprise governance

---

## Prompt

```text
You are an AI research assistant using the ReAct (Reasoning + Acting) pattern to research best practices for building enterprise knowledge bases and documentation systems.

## Task

Research how leading technology companies structure their documentation and knowledge bases, then synthesize findings into actionable recommendations for refactoring a prompt engineering library.

## Research Goal

Answer this question with evidence from multiple authoritative sources:

> "What are the best practices for structuring a prompt engineering knowledge base that serves multiple skill levels (beginner to advanced) and personas (developers, architects, business users)?"

## Context

**Project**: `tafreeman/prompts` - A prompt library for Deloitte AI & Engineering
**Target Users**: 
- Junior Engineers (need quick-start, copy-paste templates)
- Senior Engineers (need advanced patterns, optimization)
- Solution Architects (need reference architecture, governance)
- QA Testers (need quick start, copy paste, templates, reference sources)
- QA Automation Engineers (need quick start, copy paste, templates, reference sources)
- Functional Teams (need business prompts, M365 integration)

**Dual Goals**:
1. Enable rapid onboarding (<1 week to productivity)
2. Provide depth for complex enterprise problems

**Current Gaps**:
- No index/navigation files
- No content type classification
- No learning tracks by persona
- Inconsistent frontmatter schema

## Available Tools

### 1. web_search
Search the web for documentation best practices.
- Parameters: `{ "query": "search terms", "site_filter": "optional domain" }`
- Returns: Relevant URLs and snippets

### 2. fetch_documentation
Fetch and analyze documentation pages.
- Parameters: `{ "url": "documentation URL" }`
- Returns: Page content, structure analysis, frontmatter schema

### 3. compare_patterns
Compare documentation patterns across sources.
- Parameters: `{ "sources": ["source1", "source2"], "aspect": "structure|frontmatter|navigation|content-types" }`
- Returns: Comparative analysis

### 4. extract_schema
Extract metadata schema from documentation systems.
- Parameters: `{ "source": "documentation system name" }`
- Returns: Frontmatter fields, content types, navigation patterns

### 5. synthesize_findings
Combine research findings into recommendations.
- Parameters: `{ "findings": [...], "context": "project context" }`
- Returns: Prioritized recommendations with evidence

## Research Targets

Query these authoritative sources for knowledge base best practices:

### Tier 1: Documentation Leaders (Primary Research)

| Source | URL Pattern | Focus Area |
|--------|-------------|------------|
| **Microsoft Learn** | learn.microsoft.com | Content model, frontmatter, versioning |
| **GitHub Docs** | docs.github.com/contributing | Content types, style guide, structure |
| **Google Developers** | developers.google.com | Developer experience, API docs |
| **AWS Documentation** | docs.aws.amazon.com | Enterprise scale, navigation |
| **GitHub Docs local** | D:\source\githubdocs\content ([local reference](../../githubdocs/content)) | Content types, style guide, structure |

### Tier 2: AI/ML Documentation (Domain-Specific)

| Source | URL Pattern | Focus Area |
|--------|-------------|------------|
| **GitHub copilot Docs** | https://docs.github.com/en/copilot | prompt paterns, examples, best practices |
| **GitHub Docs local** | D:\source\githubdocs\content\copilot ([local reference](../../githubdocs/content/copilot)) | prompt paterns, examples, best practices |
| **OpenAI Docs** | platform.openai.com/docs | Prompt patterns, examples |
| **Anthropic Docs** | docs.anthropic.com | Claude prompting, best practices |
| **Google AI** | ai.google.dev | Gemini patterns, tutorials |
| **LangChain** | python.langchain.com/docs | Framework patterns, cookbooks |

### Tier 3: Developer Experience Leaders

| Source | URL Pattern | Focus Area |
|--------|-------------|------------|
| **Stripe Docs** | stripe.com/docs | API docs gold standard |
| **Vercel Docs** | vercel.com/docs | Modern docs UX |
| **Tailwind Docs** | tailwindcss.com/docs | Search, navigation |

## Instructions

Use the Think → Act → Observe → Reflect cycle to research each source systematically.

For each cycle:

**Thought [N]**: 
- What am I investigating? (structure, frontmatter, navigation, content types, learning paths)
- Which source is most relevant for this aspect?
- How will this inform the prompt library refactoring?

**Action [N]**:
```
Tool: [tool_name]
Parameters: { ... }
```

**Observation [N]**: [Analyze tool output - structure findings, note patterns]

**Reflection [N]**: 
- What pattern did I discover?
- How does this compare to other sources?
- How does this apply to the prompt library?

---

Continue cycles until you have researched:
- [ ] Content model patterns (at least 3 sources)
- [ ] Frontmatter/metadata schemas (at least 3 sources)
- [ ] Navigation/IA patterns (at least 3 sources)
- [ ] Learning path structures (at least 2 sources)
- [ ] Prompt-specific documentation (at least 2 sources)

## Final Deliverables

After sufficient research, provide:

### 1. Research Summary Table

| Aspect | Microsoft | GitHub | OpenAI | Anthropic | AWS | Best Practice |
|--------|-----------|--------|--------|-----------|-----|---------------|
| Content Types | ... | ... | ... | ... | ... | ... |
| Frontmatter Fields | ... | ... | ... | ... | ... | ... |
| Navigation Pattern | ... | ... | ... | ... | ... | ... |
| Learning Paths | ... | ... | ... | ... | ... | ... |

### 2. Synthesized Recommendations

For each recommendation:
- **Pattern**: What to implement
- **Evidence**: Which sources use this (with URLs)
- **Application**: How to apply to prompt library
- **Priority**: P0/P1/P2
- **Effort**: Low/Medium/High

### 3. Recommended Architecture

Based on research, provide:
- Folder structure recommendation (with rationale from sources)
- Frontmatter schema (synthesized from best practices)
- Content type definitions (with examples from sources)
- Navigation pattern (with evidence)

### 4. Specific Actions

Prioritized list of changes to `tafreeman/prompts` with:
- Task description
- Evidence supporting this change
- Estimated effort
- Dependencies

## Key Questions to Answer

1. **Content Types**: What content types do leading docs use? (conceptual, tutorial, reference, how-to, quickstart, troubleshooting)

2. **Frontmatter**: What metadata fields are standard? (title, type, difficulty, audience, prerequisites, estimatedTime)

3. **Navigation**: How do they structure index/landing pages? (featured links, persona cards, learning tracks)

4. **Learning Paths**: How do they guide users from beginner to advanced? (tracks, prerequisites, progressive disclosure)

5. **Prompt-Specific**: What patterns do OpenAI/Anthropic use for prompt documentation? (examples, variables, tips, variations)

6. **Enterprise**: What governance/compliance metadata do enterprise docs include? (audit, review status, classification)

## Constraints

- Focus on patterns applicable to a prompt library (not API reference docs)
- Prioritize patterns that serve multiple skill levels
- Consider implementation effort (favor high-impact, low-effort changes)
- Ensure recommendations are specific and actionable
- Cite sources for every recommendation
```

---

## Variables

- Modify **Research Targets** to add/remove sources based on your needs
- Adjust **Key Questions** to focus on specific aspects
- Update **Context** with current repository state

## Example Usage

**Input**: Copy the prompt above into Claude, GPT-4, or Copilot

**Expected Output Structure**:

```text
**Thought 1**: I'll start by researching Microsoft Learn's content model since they're known for enterprise documentation at scale. Their approach to content types and frontmatter will be foundational.

**Action 1**:
Tool: web_search
Parameters: { 
  "query": "Microsoft Learn content model documentation types frontmatter",
  "site_filter": "learn.microsoft.com"
}

**Observation 1**: Found Microsoft's contributor guide which describes their content model:
- Content types: conceptual, quickstart, tutorial, how-to, reference, sample
- Frontmatter: title, description, ms.date, ms.topic, ms.custom
- Structure: Product > Area > Topic hierarchy
- URL: https://learn.microsoft.com/contribute/content/

**Reflection 1**: Microsoft uses 6 content types, similar to GitHub Docs. Their `ms.topic` field is equivalent to our `type` field. Key insight: they separate "quickstart" (15-min first success) from "tutorial" (end-to-end learning). This distinction is important for our dual goals of quick-start AND depth.

---

**Thought 2**: Now I'll research GitHub Docs' contributing guide since they're the reference architecture for our refactor. I need to understand their frontmatter schema in detail.

**Action 2**:
Tool: fetch_documentation
Parameters: { 
  "url": "https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter"
}

**Observation 2**: GitHub Docs frontmatter includes:
- Required: title, versions
- Recommended: shortTitle, intro, type, topics
- Optional: permissions, layout, children, featuredLinks, learningTracks
- Types: overview, quick_start, tutorial, how_to, reference

**Reflection 2**: GitHub's schema is comprehensive but not overwhelming. Key patterns:
1. `shortTitle` for navigation (≤27 chars) - we need this
2. `children` for index pages - critical gap in our repo
3. `learningTracks` for guided paths - supports our persona-based learning
4. `featuredLinks` for landing pages - enables quick navigation

---

[Continue for 8-12 cycles covering all research targets]

---

**Final Answer**:

## Research Summary Table

| Aspect | Microsoft Learn | GitHub Docs | OpenAI | Anthropic | AWS | Recommendation |
|--------|-----------------|-------------|--------|-----------|-----|----------------|
| **Content Types** | conceptual, quickstart, tutorial, how-to, reference, sample | overview, quick_start, tutorial, how_to, reference | guide, reference, cookbook | guide, reference, cookbook | concept, task, reference, tutorial | 6 types: conceptual, quickstart, how_to, tutorial, reference, troubleshooting |
| **Frontmatter** | title, description, ms.topic, ms.date | title, shortTitle, intro, type, topics, versions | title, description | title, description | title, services | title, shortTitle, intro, type, difficulty, audience, platforms, topics |
| **Navigation** | Hub pages, TOC, breadcrumbs | index.md with children, featuredLinks | Sidebar, search | Sidebar, categories | Service-based hierarchy | index.md per folder with children + featuredLinks |
| **Learning Paths** | Learning paths with modules | learningTracks in frontmatter | None explicit | Prompt library by use case | Workshops, tutorials | 3 tracks: engineer-quickstart, architect-depth, functional-productivity |
| **Examples** | Inline + separate samples | Inline with syntax highlighting | Playground links | Claude console links | Code samples | Inline examples + "Try it" links where applicable |

## Synthesized Recommendations

### P0 - Critical (Week 1)

**1. Add index.md to every folder**
- **Evidence**: GitHub Docs, Microsoft Learn, AWS all use index pages for navigation
- **Pattern**: Each folder has index.md with `children` array listing contents
- **Application**: Create index.md for prompts/, prompts/advanced/, prompts/developers/, etc.
- **Effort**: Medium (8-12 hours for all folders)

**2. Implement content type field**
- **Evidence**: All 5 sources use explicit content types
- **Pattern**: `type: conceptual|quickstart|how_to|tutorial|reference|troubleshooting`
- **Application**: Add `type` to all 137 prompts (can be automated)
- **Effort**: Medium (bulk update script + manual review)

**3. Create quickstart guides**
- **Evidence**: Microsoft "quickstart" = 15-min first success; GitHub "quick_start" = same concept
- **Pattern**: Platform-specific quickstarts (Copilot, Claude, M365)
- **Application**: Create get-started/ folder with 3-4 quickstarts
- **Effort**: High (12-16 hours of content creation)

### P1 - High (Week 2-3)

**4. Add audience/persona field**
- **Evidence**: Microsoft uses ms.custom for audience; Anthropic organizes by use case
- **Pattern**: `audience: [junior-engineer, senior-engineer, architect, functional-team]`
- **Application**: Add to all prompts, enables persona filtering
- **Effort**: Medium

**5. Implement learning tracks**
- **Evidence**: GitHub `learningTracks`, Microsoft Learning Paths
- **Pattern**: YAML files defining ordered sequences of content
- **Application**: Create 3 tracks per persona (engineer, architect, functional)
- **Effort**: Medium

### P2 - Medium (Week 4+)

**6. Add shortTitle for navigation**
- **Evidence**: GitHub Docs requires shortTitle ≤27 chars for nav
- **Pattern**: `shortTitle: "Short Nav Label"`
- **Application**: Add to all prompts for better navigation UX
- **Effort**: Low

**7. Create featuredLinks on landing pages**
- **Evidence**: GitHub index.md pages have `featuredLinks.gettingStarted`, `featuredLinks.popular`
- **Application**: Add to index.md files for quick navigation
- **Effort**: Low

## Recommended Architecture

Based on synthesis of Microsoft Learn, GitHub Docs, and OpenAI patterns:

[Include folder structure from original refactor plan, validated by research]

## Confidence Level: High

**Justification**: Recommendations are directly supported by patterns from 5+ authoritative sources. The GitHub Docs model is particularly well-suited because it's open source and we can see exactly how they implement these patterns.

**Remaining Questions**:
1. Should we adopt Microsoft's `ms.date` pattern for tracking freshness?
2. Do we need Anthropic's "cookbook" concept as a separate content type?
3. How do we handle prompt versioning (OpenAI shows version history)?
```

## Tips

- **Prioritize Tier 1 sources**: Microsoft and GitHub have the most mature, documented content models
- **Look for contributing guides**: Most docs sites have contributor guides that explain their content model
- **Note the differences**: Where sources disagree, consider which pattern fits your context better
- **Cite everything**: Every recommendation should have at least 2 sources supporting it
- **Focus on applicable patterns**: Skip patterns that only apply to API reference docs

## When to Use This Prompt

- Starting a new documentation project
- Refactoring an existing knowledge base
- Benchmarking your docs against industry leaders
- Building a business case for documentation investment
- Training a team on documentation best practices

## Related Prompts

- [ReAct: Prompt Library Refactoring](prompt-library-refactor-react.md) - The original analysis prompt
- [Reflection: Self-Critique](reflection-self-critique.md) - For validating research findings
- [Chain-of-Thought: Detailed](chain-of-thought-detailed.md) - For deep-dive analysis

## Changelog

### Version 1.0 (2025-11-29)

- Initial release
- Research targets for 11 documentation sources
- Structured deliverables for architecture recommendations
- Integration with prompt library refactoring context
