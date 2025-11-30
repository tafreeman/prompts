---
title: "Quickstart for Microsoft 365 Copilot"
shortTitle: "M365 Copilot Quickstart"
intro: "Get productive with Microsoft 365 Copilot in 15 minutes. Learn the essential prompting patterns for Word, Excel, PowerPoint, Outlook, and Teams."
type: "quickstart"
difficulty: "beginner"
estimatedTime: "15 min"
audience:
  - "product-manager"
  - "business-analyst"
  - "junior-engineer"
  - "mid-engineer"
platforms:
  - "m365-copilot"
topics:
  - "quickstart"
  - "m365-copilot"
  - "productivity"
author: "Deloitte AI & Engineering"
date: "2025-11-29"
version: "1.0"
governance_tags:
  - "PII-safe"
learningTrack: "functional-productivity"
---

# Quickstart for Microsoft 365 Copilot

Get productive with Microsoft 365 Copilot across Word, Excel, Outlook, and Teams in just 15 minutes. This guide covers essential prompting patterns for each app.

## Prerequisites

Before you begin, ensure you have:

- [ ] **Microsoft 365 Copilot license** assigned to your account
- [ ] **Microsoft 365 apps** installed and updated (Word, Excel, PowerPoint, Outlook, Teams)
- [ ] **Copilot enabled** by your organization's IT administrator
- [ ] Basic familiarity with the Microsoft 365 apps

> **Note**: Microsoft 365 Copilot works within your organizational data through Microsoft Graph. All interactions stay within your tenant's security and compliance boundaries.

---

## Step 1: Copilot in Word (3 min)

Microsoft Word Copilot helps you draft, rewrite, and summarize documents.

### Access Copilot in Word

1. Open a new or existing Word document
2. Look for the **Copilot icon** in the ribbon or the side panel
3. Click to open the Copilot chat pane

### Try These Prompts

**Draft new content:**

```text
Draft a project status update for the Q4 marketing campaign. Include sections for:
- Completed milestones
- Current blockers
- Next steps
- Timeline update
```

**Summarize a document:**

```text
Summarize this document in 3-5 bullet points, focusing on the key decisions and action items.
```

**Rewrite for tone:**

```text
Rewrite the selected paragraph to be more formal and suitable for executive leadership.
```

### Key Word Features

| Feature | How to Use |
|---------|------------|
| Draft with Copilot | Click "Draft with Copilot" in an empty document |
| Rewrite | Select text → Click Copilot icon → Choose "Rewrite" |
| Summarize | Open Copilot pane → Ask for a summary |
| Reference files | Use `/` to reference other documents from OneDrive/SharePoint |

---

## Step 2: Copilot in Excel (4 min)

Excel Copilot analyzes data, creates formulas, and generates insights from your spreadsheets.

### Access Copilot in Excel

1. Open an Excel workbook with data formatted as a **table** (Ctrl+T to convert)
2. Click the **Copilot button** in the ribbon
3. The Copilot pane opens on the right side

> **Important**: Your data must be in a formatted table for Copilot to work effectively.

### Try These Prompts

**Analyze data:**

```text
What are the top 5 products by revenue in this data? Show me the trends over the last 3 months.
```

**Create formulas:**

```text
Add a column that calculates the profit margin as a percentage (Revenue - Cost) / Revenue.
```

**Generate insights:**

```text
Highlight any outliers or anomalies in the sales data. What patterns do you see?
```

**Create visualizations:**

```text
Create a bar chart comparing sales by region for Q3 and Q4.
```

### Key Excel Features

| Feature | How to Use |
|---------|------------|
| Formula generation | Describe what you want to calculate in plain language |
| Data analysis | Ask questions about patterns, trends, or outliers |
| Conditional formatting | Ask Copilot to highlight specific conditions |
| Chart creation | Describe the visualization you need |

---

## Step 3: Copilot in Outlook (4 min)

Outlook Copilot helps you draft emails, summarize long threads, and manage your inbox efficiently.

### Access Copilot in Outlook

1. Open Outlook (desktop or web)
2. When composing: Click the **Copilot icon** in the compose toolbar
3. When reading: Look for **Summary by Copilot** at the top of long threads

### Try These Prompts

**Draft a new email:**

```text
Draft a meeting request to the product team for next Tuesday at 2 PM to discuss the 
Q1 roadmap priorities. Keep it professional but friendly.
```

**Reply to an email:**

```text
Draft a reply accepting the proposal but asking for clarification on the timeline 
and budget allocation.
```

**Summarize a thread:**

```text
Summarize this email thread. What are the main discussion points and any decisions made?
```

**Adjust tone:**

```text
Make this email more concise and direct. Keep it under 100 words.
```

### Key Outlook Features

| Feature | How to Use |
|---------|------------|
| Draft with Copilot | New email → Click Copilot → Describe your email |
| Thread summary | Open long thread → Click "Summary by Copilot" |
| Coaching | Select draft text → Ask Copilot for improvements |
| Scheduling | Ask Copilot to suggest meeting times based on calendars |

### Outlook-Specific Commands

In the Copilot chat within Outlook, use these shortcuts:

- `/summarize` - Quick summary of the current thread
- `/draft` - Start drafting a new message
- `/schedule` - Help with meeting scheduling

---

## Step 4: Copilot in Teams (4 min)

Teams Copilot summarizes meetings, catches you up on chats, and helps manage action items.

### Access Copilot in Teams

1. **In a meeting**: Click the Copilot icon in the meeting controls (recording must be enabled)
2. **In a chat**: Click the Copilot icon in the compose box
3. **In Teams Chat**: Open the Copilot app from the left sidebar

### Try These Prompts

**During a meeting:**

```text
What decisions have been made so far in this meeting?
```

```text
List the action items mentioned with who is responsible for each.
```

**After a meeting:**

```text
Summarize this meeting. Include key discussion points, decisions, and next steps.
```

**In a chat:**

```text
What has been discussed in this chat over the past week? Any items that need my attention?
```

**Catch up on channels:**

```text
Summarize the key updates from the #project-alpha channel since Monday.
```

### Key Teams Features

| Feature | How to Use |
|---------|------------|
| Meeting recap | After meeting → Open chat → Ask Copilot for summary |
| Live meeting assist | During meeting → Ask about decisions or action items |
| Chat summary | In any chat → Click Copilot → Ask for highlights |
| Channel catch-up | In channel → Ask Copilot what you missed |

### Teams-Specific Commands

Use these reference commands in Teams Copilot:

- `/files` - Reference a specific file shared in the chat
- `/meetings` - Reference a recent meeting transcript
- `/people` - Find information about a colleague

---

## Quick Reference by App

| App | Best For | Sample Prompt |
|-----|----------|---------------|
| **Word** | Drafting, summarizing, rewriting | "Draft a proposal for..." |
| **Excel** | Data analysis, formulas, charts | "What trends do you see in..." |
| **PowerPoint** | Creating slides, organizing content | "Create a presentation about..." |
| **Outlook** | Email drafting, thread summaries | "Summarize this conversation..." |
| **Teams** | Meeting recaps, chat catch-ups | "What action items were assigned..." |

### Universal Prompting Tips

1. **Be specific** - Include context, format, and length requirements
2. **Use references** - Mention specific files, people, or meetings with `/`
3. **Iterate** - Ask Copilot to refine, expand, or adjust its response
4. **Provide examples** - Show Copilot what you're looking for when possible

---

## What You Learned

After completing this quickstart, you can:

- [ ] Access Copilot in Word, Excel, Outlook, and Teams
- [ ] Draft and summarize documents in Word
- [ ] Analyze data and create formulas in Excel
- [ ] Draft emails and summarize threads in Outlook
- [ ] Get meeting summaries and action items in Teams
- [ ] Use `/` commands to reference files and meetings
- [ ] Write effective prompts for each M365 app

---

## Next Steps

Now that you've mastered the basics, explore these resources:

| Resource | Description |
|----------|-------------|
| [M365 Copilot Prompts](/prompts/m365/) | Ready-to-use prompts for specific M365 scenarios |
| [Advanced Techniques](/docs/advanced-techniques.md) | Learn prompt chaining and complex workflows |
| [Best Practices](/guides/best-practices.md) | Optimize your prompts for better results |
| [Business Prompts](/prompts/business/) | Industry-specific prompt templates |

### Recommended Learning Path

1. **Practice** - Use Copilot daily for common tasks
2. **Experiment** - Try different prompt styles and see what works
3. **Build a library** - Save your best prompts for reuse
4. **Share** - Help teammates with effective prompts

---

## Troubleshooting

### Copilot icon not visible

- Verify your Microsoft 365 Copilot license is active
- Check that your admin has enabled Copilot for your organization
- Ensure your M365 apps are updated to the latest version
- Try signing out and back into your Microsoft account

### "I can't help with that" response

- Rephrase your prompt to be more specific
- Ensure you're not asking for content outside your organizational data
- Check that the file or data you're referencing is accessible

### Excel Copilot not working

- Convert your data to a formatted table (Ctrl+T)
- Ensure the table has clear headers
- Remove merged cells or complex formatting

### Meeting summaries unavailable

- Meeting transcription must be enabled
- You must be a participant in the meeting
- The meeting must have been recorded with transcription on

### Slow or incomplete responses

- Try breaking complex requests into smaller parts
- Simplify your prompt and iterate
- Check your network connection

---

## Security and Compliance

Microsoft 365 Copilot is designed with enterprise security in mind:

- **Data stays in your tenant** - Copilot only accesses data you already have permission to see
- **No training on your data** - Your organizational data isn't used to train the models
- **Compliance inherited** - Existing M365 compliance policies apply to Copilot interactions
- **Audit logging** - Copilot activities are logged for compliance purposes

For more information, consult your IT administrator or review Microsoft's [Copilot data protection documentation](https://learn.microsoft.com/microsoft-365-copilot/microsoft-365-copilot-privacy).
