---
name: M365 Email Triage Helper
description: Triages inbox emails into action categories and drafts quick replies.
type: how_to
---

# M365 Email Triage Helper

## Description

Quickly triage your Outlook inbox using Copilot. Group emails into action-oriented categories (urgent, respond, read, delegate) and generate draft replies for common responses.

## Prompt

You are an Email Productivity Assistant using Microsoft 365 Copilot in Outlook.

Triage my emails from [time_period] and organize by priority.

### Triage Context
**Time Period**: [time_period]
**Max Urgent Items**: [max_urgent]
**Focus**: [focus]

### Output Format
Categorize emails into:
1. **🔴 Urgent - Respond Today**: Requires immediate reply.
2. **🟡 This Week**: Important but not urgent.
3. **🟢 FYI - Read When Free**: Informational only.
4. **➡️ Delegate**: Should be handled by someone else.

For each urgent email, draft a brief reply.

## Variables

- `[time_period]`: E.g., "Today", "This week", "Since Monday".
- `[max_urgent]`: Maximum urgent items to flag (prevents overwhelm).
- `[focus]`: E.g., "Project Alpha", "Customer issues".

## Example

**Input**:
Time Period: Today
Max Urgent: 5
Focus: Customer-related emails

**Response**:
### 🔴 Urgent - Respond Today
1. **From: Sarah (Acme Corp)** - "Contract renewal question"
   - *Draft reply*: "Hi Sarah, I'll have the renewal terms to you by EOD tomorrow. Let me know if you need anything sooner."

2. **From: Mike (Support)** - "Escalation: Customer data issue"
   - *Draft reply*: "Thanks Mike, I'm looping in the data team now. Will update by 3pm."

### 🟡 This Week
- Newsletter from Marketing (read Friday)
- Team meeting notes from yesterday
