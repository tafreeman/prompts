---
title: "Whitepaper Outliner"
shortTitle: "Whitepaper"
intro: "Create a defensible whitepaper outline with claims mapped to evidence, visuals, and a drafting plan."
type: "how_to"
difficulty: "intermediate"
audience:
  - "functional-team"
  - "business-analyst"
  - "project-manager"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "creative"
  - "documentation"
  - "analysis"
author: "Prompts Library Team"
version: "1.0"
date: "2026-01-03"
governance_tags:
  - "PII-safe"
  - "general-use"
  - "requires-review"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 0.0
---

# Whitepaper Outliner

---

## Description

Generate a whitepaper outline that is structured, persuasive, and evidence-driven. This prompt produces a section-by-section plan, key claims, required sources, and recommended visuals so drafting is fast and consistent.

---

## Use Cases

- Planning a thought-leadership piece without writing fluff
- Aligning stakeholders on narrative and claims before drafting
- Producing a research checklist and citation plan
- Creating an executive summary and CTA structure

---

## Variables

| Variable | Description | Example |
|---|---|---|
| `[topic]` | Whitepaper topic | `Modernizing data governance for mid-market orgs` |
| `[audience]` | Primary reader persona | `CIOs and data leaders` |
| `[goal]` | What the whitepaper should achieve | `Drive demo requests and position expertise` |
| `[thesis]` | One-sentence main argument | `Governance must be automated to scale` |
| `[key_points]` | Bulleted supporting points | `Risk reduction, faster access, auditability` |
| `[evidence_sources]` | Allowed sources or links | `Internal survey + industry reports` |
| `[length]` | Target length | `8–12 pages` |
| `[tone]` | Style constraints | `Authoritative, practical, not salesy` |
| `[citation_style]` | Citation expectations | `Footnotes + reference list` |
| `[cta]` | Desired call to action | `Book a 30-min assessment` |

---

## Prompt

```text
You are a senior researcher and technical writer.

Create a whitepaper OUTLINE (not the full draft yet) using the inputs below.

## Inputs
Topic: [topic]
Audience: [audience]
Goal: [goal]
Thesis: [thesis]
Key points: [key_points]
Allowed evidence/sources: [evidence_sources]
Target length: [length]
Tone: [tone]
Citation style: [citation_style]
Call to action: [cta]

## Requirements
1) Do not invent facts or statistics. For each claim that would need support, add a "Evidence needed" note.
2) Make the structure skimmable and logical for the audience.
3) Include a visuals plan (tables/figures) that supports the narrative.
4) Provide a drafting plan (what to write first, and what inputs to request).

## Output format (Markdown)
- Working title (5 options)
- Executive summary (bullet outline)
- Detailed outline with H2/H3 headings
  - For each section: purpose, key claims, evidence needed, suggested visuals
- Glossary (terms the audience may not know)
- References plan (what sources to cite)
- Drafting plan (sequence + ownership suggestions)
- Missing inputs (questions to answer before writing)
```

---

## Example

**Input:**

```text
[topic]=Reducing SaaS sprawl without slowing teams down
[audience]=IT leaders and procurement
[goal]=Provide a practical framework and promote our assessment offering
[thesis]=You can reduce sprawl by standardizing intake, measuring usage, and enforcing lightweight governance
[key_points]=Usage visibility; security review gates; renewal calendar; owner accountability
[evidence_sources]=Internal license audit data + reputable industry reports (no paywalled quotes)
[length]=10 pages
[tone]=Practical, structured, neutral
[citation_style]=Inline citations + reference list
[cta]=Request a SaaS governance assessment
```

**Output (excerpt):**

```text
## Working title options
1. "SaaS Governance That Doesn’t Slow Teams"
2. "A Practical Playbook to Reduce SaaS Sprawl"
...

## Detailed outline
## 1. The real cost of SaaS sprawl
- Purpose: Establish urgency for IT/procurement
- Key claims:
  - Sprawl increases security and compliance risk
  - Redundant tools increase spend
- Evidence needed:
  - Industry estimate of redundant spend (cite)
  - Example: anonymized internal audit counts [ADD DATA]
- Suggested visuals:
  - Table: "Symptoms of sprawl" vs "Business impact"
...

## Missing inputs
- What assessment deliverable do we offer (scope, timeline)?
- Which internal audit metrics are publishable?
```

---

## Tips

- Draft the outline first, then validate claims with sources before writing prose.
- Ask for publishable internal data early (legal/comms review can take time).
- If you need speed, start with a 2-page brief and expand.

---

## Related Prompts

- [Documentation Generator](/prompts/developers/documentation-generator)
- [Brand Voice Developer](/prompts/creative/brand-voice-developer)
- [Content Marketing Blog Post](/prompts/creative/content-marketing-blog-post)
