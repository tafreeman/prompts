# Microsoft 365 Copilot Prompts

This folder contains end-user prompts optimized for **Microsoft 365 Copilot**, designed to help knowledge workers be more productive across Outlook, Teams, Word, Excel, PowerPoint, and other M365 apps.

## Overview

All prompts in this package are:

- **End-user focused**: Designed for individual knowledge workers, not admins or developers.
- **Context-aware**: Leverage Microsoft 365 data (emails, chats, calendar, documents).
- **Template-compliant**: Follow the repo's standard `prompt-template.md` structure.
- **Action-oriented**: Produce clear, actionable outputs (talking points, summaries, tasks, outlines).

## Prompt List

### Daily & Weekly Planning

- **[m365-daily-standup-assistant.md](m365-daily-standup-assistant.md)**: Generate daily standup talking points (Yesterday / Today / Blockers) from recent M365 activity.
- **[m365-weekly-review-coach.md](m365-weekly-review-coach.md)**: Reflect on the past week and plan next week's priorities using calendar, emails, and documents.
- **[m365-manager-sync-planner.md](m365-manager-sync-planner.md)**: Prepare a structured agenda for 1:1s with your manager, covering wins, blockers, and career topics.

### Communication & Email

- **[m365-email-triage-helper.md](m365-email-triage-helper.md)**: Triage inbox by urgency and draft replies for high-priority messages.
- **[m365-handover-document-creator.md](m365-handover-document-creator.md)**: Create a comprehensive handover guide for role transitions or project transfers.

### Meetings

- **[m365-meeting-prep-brief.md](m365-meeting-prep-brief.md)**: Prepare for meetings with context, talking points, and questions based on invite and related M365 data.
- **[m365-meeting-recap-assistant.md](m365-meeting-recap-assistant.md)**: Turn meeting transcripts into structured summaries with decisions, action items, and follow-ups.

### Project & Task Management

- **[m365-project-status-reporter.md](m365-project-status-reporter.md)**: Generate project status updates for stakeholders from recent communications and documents.
- **[m365-personal-task-collector.md](m365-personal-task-collector.md)**: Extract and organize personal tasks from emails, chats, and meetings into a prioritized list.

### Content & Document Work

- **[m365-document-summarizer.md](m365-document-summarizer.md)**: Summarize long documents for specific audiences with key points and next steps.
- **[m365-presentation-outline-generator.md](m365-presentation-outline-generator.md)**: Create PowerPoint outlines with slide titles, bullets, and visual suggestions.
- **[m365-slide-content-refiner.md](m365-slide-content-refiner.md)**: Transform dense text into punchy, slide-ready content with speaker notes.

### Data & Insights

- **[m365-data-insights-assistant.md](m365-data-insights-assistant.md)**: Analyze Excel data, identify trends and anomalies, and recommend visualizations in plain language.
- **[m365-excel-formula-expert.md](m365-excel-formula-expert.md)**: Generate complex Excel formulas from plain English descriptions and explain how they work.
- **[m365-customer-feedback-analyzer.md](m365-customer-feedback-analyzer.md)**: Analyze unstructured customer feedback to identify sentiment, themes, and actionable insights.

### Creative & Visual Design

- **[m365-designer-image-prompt-generator.md](m365-designer-image-prompt-generator.md)**: Create detailed, artistic prompts for Microsoft Designer to generate professional imagery.
- **[m365-designer-infographic-brief.md](m365-designer-infographic-brief.md)**: Transform data points into a structured design brief for creating infographics.
- **[m365-designer-social-media-kit.md](m365-designer-social-media-kit.md)**: Generate a cohesive set of image prompts for Instagram, LinkedIn, and Twitter assets.
- **[m365-sway-document-to-story.md](m365-sway-document-to-story.md)**: Convert standard documents into engaging Sway storylines with visual suggestions.
- **[m365-sway-visual-newsletter.md](m365-sway-visual-newsletter.md)**: Compile team updates into a modern, mobile-friendly Sway newsletter structure.

## How to Use These Prompts

1. **Choose a prompt** that matches your workflow or task.
2. **Open the file** and review the `## Prompt` section.
3. **Replace placeholders** (e.g., `[time_window]`, `[audience]`, `[project_name]`) with your specific values.
4. **Paste the prompt into Microsoft 365 Copilot** in the relevant app (Word, Teams, Outlook, Excel, PowerPoint).
5. **Review and refine** the output as needed.

## Tips for Success

- **Be specific**: The more detail you provide in placeholders, the better the output.
- **Iterate**: Ask Copilot to refine, shorten, or expand the output if needed.
- **Combine prompts**: Use multiple prompts in sequence (e.g., meeting prep → meeting → meeting recap).
- **Customize tone**: Adjust `[tone]` variables to match your audience and context.

## Contributing

If you want to add new M365 prompts to this package:

- Follow the structure in `templates/prompt-template.md`.
- Focus on end-user productivity workflows.
- Use `[placeholders]` for variables and document them in the `## Variables` section.
- Include realistic `## Example Usage` to help users understand how to apply the prompt.

## Related Resources

- [Microsoft 365 Copilot Overview](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-overview)
- [Copilot Prompt Gallery](https://m365.cloud.microsoft/copilot-prompts)
- [Best Practices for Microsoft 365 Copilot](https://learn.microsoft.com/en-us/training/modules/optimize-and-extend-microsoft-365-copilot/)

---

**Note**: These prompts are designed for Microsoft 365 Copilot but many patterns can be adapted for other AI assistants (e.g., Claude, ChatGPT) with minor adjustments to context instructions.
