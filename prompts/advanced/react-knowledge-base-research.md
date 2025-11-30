---
title: "Knowledge Base Research Guide"
shortTitle: "KB Research"
intro: "Research patterns from industry-leading documentation sites to improve our prompt library."
type: "reference"
difficulty: "intermediate"
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
author: "Prompt Library Team"
version: "2.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "approved"
estimatedTime: "20 min"
---

# Knowledge Base Research Guide

## What This Guide Is For

This is a **research reference** for improving and expanding the prompt library. Use it when:

- Adding new content categories (like expanding creative or business prompts)
- Benchmarking against industry documentation leaders
- Planning new features or navigation improvements

## Current Status: ✅ Foundation Complete

The major refactor is done! We now have:

| What | Status | Count |
|------|--------|-------|
| Prompts with valid frontmatter | ✅ | 145+ |
| Index.md navigation files | ✅ | All folders |
| Content types | ✅ | 6 types |
| Learning tracks | ✅ | 3 tracks |
| Quickstart guides | ✅ | 4 platforms |

## Next Priority: Content Expansion

### 🎨 Creative Prompts (HIGH PRIORITY - Currently 2 prompts)

The `prompts/creative/` folder needs significant expansion:

| Needed | Description | Effort |
|--------|-------------|--------|
| Writing assistance | Blog posts, emails, reports, proposals | Medium |
| Marketing content | Social media, ad copy, taglines | Medium |
| Storytelling | Narratives, case studies, presentations | Medium |
| Visual descriptions | Image prompts, design briefs | Low |
| Editing & refinement | Tone adjustment, simplification, expansion | Low |

**Target**: 15-20 creative prompts covering common business writing needs.

### 💼 Business Prompts (MEDIUM PRIORITY - Currently 26 prompts)

The `prompts/business/` folder is well-populated but can expand:

| Gap | Description | Effort |
|-----|-------------|--------|
| Sales enablement | Pitch decks, objection handling, proposals | Medium |
| HR & recruiting | Job descriptions, interview questions, feedback | Medium |
| Finance | Budget narratives, forecasting explanations | Low |
| Legal summaries | Contract review, compliance checklists | Medium |
| Executive comms | Board updates, investor materials | Medium |

**Target**: 35-40 business prompts covering all major functions.

### 📊 Analysis Prompts (LOW PRIORITY - Good coverage)

Add as needed for specific use cases.

---

## Research Sources (For Expansion)

When researching new content patterns, consult these sources:

### Tier 1: Documentation Leaders

| Source | URL | What to Learn |
|--------|-----|---------------|
| **GitHub Docs** | docs.github.com | Content types, frontmatter, navigation |
| **Microsoft Learn** | learn.microsoft.com | Enterprise scale, learning paths |
| **Stripe Docs** | stripe.com/docs | Copy patterns, clarity |

### Tier 2: AI-Specific Documentation

| Source | URL | What to Learn |
|--------|-----|---------------|
| **OpenAI Cookbook** | cookbook.openai.com | Prompt examples, variations |
| **Anthropic Docs** | docs.anthropic.com | Claude patterns, best practices |
| **GitHub Copilot Docs** | docs.github.com/copilot | Code generation prompts |

### Tier 3: Creative & Business Content

| Source | URL | What to Learn |
|--------|-----|---------------|
| **Copy.ai Templates** | copy.ai | Marketing copy patterns |
| **Jasper Templates** | jasper.ai | Business writing patterns |
| **HubSpot Resources** | hubspot.com | Sales/marketing content |

---

## Patterns We've Adopted

These patterns are **already implemented** in our library:

### Content Types (6 types)

| Type | When to Use | Example |
|------|-------------|---------|
| `conceptual` | Explain what/why | "About Chain-of-Thought" |
| `quickstart` | 15-min first success | "Quickstart for Copilot" |
| `how_to` | Complete a task | "Generating Unit Tests" |
| `tutorial` | End-to-end learning | "Building a RAG Pipeline" |
| `reference` | Quick lookup | "Frontmatter Schema" |
| `troubleshooting` | Fix problems | "Troubleshooting Output Quality" |

### Frontmatter Schema

Required fields for all prompts:

```yaml
---
title: "Clear, descriptive title"
shortTitle: "Nav label (≤27 chars)"
intro: "One sentence summary"
type: "how_to"
difficulty: "beginner|intermediate|advanced"
audience:
  - "junior-engineer"
  - "senior-engineer"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
```

### Learning Tracks (3 tracks)

| Track | Audience | Duration |
|-------|----------|----------|
| `engineer-quickstart` | Junior/Senior Engineers | 4 hours |
| `architect-depth` | Architects, Tech Leads | 8 hours |
| `functional-productivity` | BAs, PMs, Business | 2 hours |

---

## Expansion Roadmap

### Phase 1: Creative Content (Next)

Create 15+ prompts in `prompts/creative/`:

**Writing Assistance**
- [ ] Professional email writer
- [ ] Report summarizer
- [ ] Proposal generator
- [ ] Executive summary creator

**Marketing Content**
- [ ] Blog post generator
- [ ] Social media content creator
- [ ] Ad copy writer
- [ ] Tagline brainstormer

**Editing & Refinement**
- [ ] Tone adjuster (formal ↔ casual)
- [ ] Content simplifier
- [ ] Expansion assistant
- [ ] Proofreading helper

**Storytelling**
- [ ] Case study builder
- [ ] Presentation narrative creator
- [ ] User story writer

### Phase 2: Business Expansion

Add 10+ prompts to `prompts/business/`:

**Sales Enablement**
- [ ] Pitch deck outline generator
- [ ] Objection handler
- [ ] Proposal customizer
- [ ] Follow-up email writer

**HR & Recruiting**
- [ ] Job description writer
- [ ] Interview question generator
- [ ] Performance feedback assistant
- [ ] Onboarding guide creator

**Executive Communications**
- [ ] Board update generator
- [ ] Investor narrative creator
- [ ] All-hands announcement writer

### Phase 3: Specialized Tracks

- [ ] Create `creative-productivity` learning track
- [ ] Create `sales-enablement` learning track
- [ ] Add M365 Copilot-specific business prompts

---

## How to Add New Prompts

1. **Choose the right folder** based on primary use case
2. **Copy the template** from `templates/prompt-template.md`
3. **Fill in frontmatter** (all required fields)
4. **Write the prompt** with clear structure
5. **Add examples** showing expected output
6. **Run validation**: `python tools/validators/frontmatter_validator.py your-file.md`
7. **Update index.md** in the folder to include your prompt

---

## Quality Checklist for New Content

Before submitting:

- [ ] Title follows the pattern for its content type
- [ ] `shortTitle` is ≤27 characters
- [ ] `intro` is one clear sentence
- [ ] `difficulty` matches actual complexity
- [ ] `audience` targets the right personas
- [ ] `platforms` lists where it works
- [ ] Examples show realistic input/output
- [ ] No PII or sensitive data in examples
- [ ] Validation passes

---

## Related Resources

- [Frontmatter Schema](/reference/frontmatter-schema) - Complete field reference
- [Content Types](/reference/content-types) - When to use each type
- [Prompt Template](/templates/prompt-template) - Starting template
- [Contributing Guide](/CONTRIBUTING.md) - Full contribution process

## Changelog

### Version 2.0 (2025-11-30)

- Updated to reflect completed refactor
- Added expansion roadmap for creative and business content
- Simplified from research prompt to reference guide
- Added practical "How to Add New Prompts" section

### Version 1.0 (2025-11-29)

- Initial release as research prompt
