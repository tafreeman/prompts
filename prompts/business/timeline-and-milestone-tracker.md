---
title: Timeline and Milestone Tracker
shortTitle: Milestone Tracker
intro: Tracks project progress and milestones with dashboards, schedule variance analysis,
  and recovery planning.
type: how_to
difficulty: intermediate
audience:
- project-manager
- business-analyst
platforms:
- claude
- chatgpt
- github-copilot
topics:
- tracking
- project-management
author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# Timeline and Milestone Tracker

---

## Description

Tracks project progress and milestones

---

## Use Cases

- Progress Tracking for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Track progress for:

Project: [project_name]
Current Phase: [phase]
Upcoming Milestones: [milestones]
Progress Concerns: [concerns]

Provide:
1. Progress dashboard
2. Milestone analysis
3. Schedule variance
4. Critical path assessment
5. Recovery planning
6. Stakeholder updates
```text

---

## Variables

- `[project_name]`: Project name (e.g., "Mobile App v3.0 App Store Submission")
- `[phase]`: Current phase (e.g., "Beta Testing – Week 2 of 3")
- `[milestones]`: Upcoming milestones (e.g., "Beta Release Nov 15, App Store Submission Nov 30")
- `[concerns]`: Progress concerns (e.g., "3 critical bugs blocking beta, iOS 17 crash issue")

---

## Example

```text
## Project Progress Tracker

### 1. Progress Dashboard
*   **Overall Status:** 🟡 AMBER (At Risk)
*   **Schedule:** 3 days behind
*   **Budget:** On track
*   **Scope:** Stable

### 2. Milestone Analysis
*   **Code Freeze:** ✅ Complete.
*   **Beta Release:** ⚠️ At Risk. Needs 3 critical bugs fixed by EOD tomorrow.
*   **Submission:** 📅 Scheduled for 11/30, but buffer is depleted.

### 3. Critical Path Assessment
*   **Current Blocker:** Bug #402 (Login Crash on iOS 17).
*   **Impact:** Cannot start Beta testing until fixed.
*   **Mitigation:** Reallocated Senior iOS Dev from feature work to bug fixing immediately.

[... continues with recovery planning and stakeholder updates ...]
```text

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- Browse other Project Manager prompts in this category
- Check the business folder for similar templates
