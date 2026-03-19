import type { Framework } from '../schemas/framework.js';
import type { DeckManifest } from '../schemas/manifest.js';

/** Status Report — program status for managers and sponsors. */
export const statusReport: Framework = {
  id: 'status-report',
  name: 'Status Report',
  description: 'Program status report for managers and sponsors. Covers KPIs, progress, risks, timeline, and next actions.',
  audience: 'Program managers, sponsors',
  slideRange: { min: 5, max: 8 },
  defaultTheme: 'paper-ink',
  defaultStyle: 'clean',
  slots: [
    {
      position: 1,
      layout: 'cover',
      titleHint: '[Program Name] — Status Report [Period]',
      contentHint: 'Program name and 2-3 high-level status KPIs (on-track, budget, timeline).',
      required: true,
    },
    {
      position: 2,
      layout: 'scorecard',
      titleHint: '[Key Metrics Show Program Health]',
      contentHint: '4-6 KPIs with trends: budget, schedule, scope, quality, risk.',
      required: true,
    },
    {
      position: 3,
      layout: 'steps',
      titleHint: '[Phase X of Y Complete — On Track for Target]',
      contentHint: '3-5 workstream progress items showing completed and upcoming work.',
      required: true,
    },
    {
      position: 4,
      layout: 'table',
      titleHint: '[Top Risks Tracked with Mitigation Plans]',
      contentHint: 'Risk register table: risk, likelihood, impact, mitigation, owner.',
      required: true,
    },
    {
      position: 5,
      layout: 'timeline',
      titleHint: '[Key Milestones Through End of Program]',
      contentHint: '4-6 milestones with dates showing past completions and upcoming deadlines.',
      required: true,
    },
    {
      position: 6,
      layout: 'closing',
      titleHint: '[Decisions Needed Before Next Reporting Period]',
      contentHint: 'Blockers requiring sponsor action. 3-4 next steps with owners.',
      required: true,
    },
  ],
};

/** Sample manifest for Status Report framework — AI replaces placeholders. */
export const sampleManifest: DeckManifest = {
  title: '[Program Name] — Status Report',
  subtitle: '[Reporting period, e.g., Week of March 17, 2025]',
  author: '[Program Manager]',
  date: '2025-Q4',
  version: '1.0.0',
  theme: 'paper-ink',
  style: 'clean',
  framework: 'status-report',
  slides: [
    {
      id: 'cover',
      layout: 'cover',
      title: '[Program Name] — [Period] Status Report',
      subtitle: '[Department or team context]',
      kpis: [
        { value: '[Status]', label: 'Overall Health' },
        { value: '[X%]', label: 'Budget Consumed' },
        { value: '[Status]', label: 'Schedule' },
      ],
    },
    {
      id: 'scorecard',
      layout: 'scorecard',
      title: '[Program Metrics Indicate On-Track Delivery]',
      kpis: [
        { value: '[X%]', label: 'Budget Utilization', trend: 'flat', detail: '[Budget narrative]' },
        { value: '[X%]', label: 'Schedule Adherence', trend: 'up', detail: '[Schedule narrative]' },
        { value: '[N/M]', label: 'Milestones Complete', trend: 'up', detail: '[Progress narrative]' },
        { value: '[N]', label: 'Open Risks', trend: 'down', detail: '[Risk narrative]' },
        { value: '[X%]', label: 'Quality Score', trend: 'up', detail: '[Quality narrative]' },
      ],
    },
    {
      id: 'progress',
      layout: 'steps',
      title: '[Workstream Progress Shows Phase X Nearing Completion]',
      steps: [
        { label: '[Workstream 1]', description: '[Status and key accomplishment this period]' },
        { label: '[Workstream 2]', description: '[Status and key accomplishment this period]' },
        { label: '[Workstream 3]', description: '[Status and key accomplishment this period]' },
        { label: '[Workstream 4]', description: '[Status and upcoming deliverable]' },
      ],
    },
    {
      id: 'risks',
      layout: 'table',
      title: '[Three Active Risks Require Monitoring]',
      columns: ['Risk', 'Likelihood', 'Impact', 'Mitigation', 'Owner'],
      rows: [
        { Risk: '[Risk description 1]', Likelihood: '[H/M/L]', Impact: '[H/M/L]', Mitigation: '[Plan]', Owner: '[Name]' },
        { Risk: '[Risk description 2]', Likelihood: '[H/M/L]', Impact: '[H/M/L]', Mitigation: '[Plan]', Owner: '[Name]' },
        { Risk: '[Risk description 3]', Likelihood: '[H/M/L]', Impact: '[H/M/L]', Mitigation: '[Plan]', Owner: '[Name]' },
      ],
    },
    {
      id: 'timeline',
      layout: 'timeline',
      title: '[Next Major Milestone Due on Target Date]',
      events: [
        { date: '[Past date]', title: '[Completed Milestone]', description: '[Delivered on time]' },
        { date: '[Past date]', title: '[Completed Milestone]', description: '[Delivered on time]' },
        { date: '[Upcoming date]', title: '[Next Milestone]', description: '[Expected deliverable]' },
        { date: '[Future date]', title: '[Final Milestone]', description: '[Program completion criteria]' },
      ],
    },
    {
      id: 'next',
      layout: 'closing',
      title: '[Two Decisions Needed from Sponsors This Week]',
      nextSteps: [
        '[Decision or action item 1 — owner, due date]',
        '[Decision or action item 2 — owner, due date]',
        '[Blocker requiring escalation]',
        '[Next reporting date]',
      ],
      contact: '[pm@company.com]',
    },
  ],
};
