---
name: M365 Presentation Outline Generator
description: Creates structured PowerPoint outlines with slide titles, bullets, and visual suggestions.
type: how_to
---

# M365 Presentation Outline Generator

## Description

Generate structured PowerPoint presentation outlines using Microsoft 365 context. Creates slide titles, bullet points, speaker notes, and visual suggestions based on your topic and audience.

## Prompt

You are a Presentation Design Assistant using Microsoft 365 Copilot.

Create a presentation outline for [topic].

### Presentation Context
**Topic**: [topic]
**Audience**: [audience]
**Emphasis**: [emphasis]
**Slide Count**: [slide_count]
**Source Material**: [source]

### Output Format
For each slide:
- **Slide Title**: Clear, action-oriented
- **Key Points**: 3-4 bullets
- **Visual Suggestion**: Chart, image, or diagram idea
- **Speaker Note**: What to emphasize verbally

## Variables

- `[topic]`: E.g., "Q4 Product Roadmap".
- `[audience]`: E.g., "Executives", "Technical team".
- `[emphasis]`: E.g., "ROI and benefits", "Technical details".
- `[slide_count]`: Target number of slides.
- `[source]`: Reference document if any.

## Example

**Input**:
Topic: Cloud Migration Proposal
Audience: CIO and IT leadership
Emphasis: Cost savings and risk mitigation
Slide Count: 8 slides

**Response**:
### Slide 1: Executive Summary
- **Points**: Current cost burden, proposed solution, 30% savings projection
- **Visual**: Single stat callout "$1.2M annual savings"
- **Note**: Lead with the bottom line, details follow

### Slide 2: Current State Pain Points
- **Points**: Legacy infrastructure costs, security vulnerabilities, scaling limitations
- **Visual**: 3-column comparison table
- **Note**: Emphasize the "do nothing" risk

### Slide 3: Proposed Solution
- **Points**: Azure migration, phased approach, 6-month timeline
- **Visual**: Architecture diagram
- **Note**: Keep high-level, detailed timeline on next slide
