---
type: template
name: Whitepaper Outliner
description: Create a defensible whitepaper outline with claims mapped to evidence, visuals, and a drafting plan.
---

# Whitepaper Outliner

## Description

Create a defensible whitepaper outline with claims mapped to evidence, visuals, and a drafting plan. Useful for research, thought leadership, and stakeholder alignment.

## Variables

| Variable | Description |
| :--- | ------------- |
| `[topic]` | The main subject of the whitepaper |
| `[audience]` | Intended readers |
| `[goal]` | Objective of the whitepaper |
| `[thesis]` | Central argument or claim |
| `[key_points]` | Main points to cover |
| `[evidence_sources]` | Allowed sources for evidence |
| `[length]` | Target length or word count |
| `[tone]` | Desired writing style |
| `[citation_style]` | Citation format (e.g., APA, MLA) |
| `[cta]` | Call to action |

## Example

**Topic:** AI in Healthcare
**Audience:** Hospital administrators
**Goal:** Advocate for AI adoption in patient care
**Thesis:** AI improves outcomes and efficiency
**Key points:** Diagnostic accuracy, workflow automation, patient engagement
**Evidence sources:** Peer-reviewed journals, case studies
**Length:** 8 pages
**Tone:** Authoritative
**Citation style:** APA
**CTA:** Schedule a demo with our AI team

## Use Cases

- Planning a thought-leadership piece without writing fluff
- Aligning stakeholders on narrative and claims before drafting
- Producing a research checklist and citation plan
- Creating an executive summary and CTA structure

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

## Tips

- Draft the outline first, then validate claims with sources before writing prose.
- Ask for publishable internal data early (legal/comms review can take time).
- If you need speed, start with a 2-page brief and expand.

---

## Related Prompts

- [Documentation Generator](/prompts/developers/documentation-generator)
- [Brand Voice Developer](/prompts/creative/brand-voice-developer)
- [Content Marketing Blog Post](/prompts/creative/content-marketing-blog-post)
