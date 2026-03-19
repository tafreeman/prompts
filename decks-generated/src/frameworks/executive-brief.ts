import type { Framework } from '../schemas/framework.js';
import type { DeckManifest } from '../schemas/manifest.js';

/** Executive Brief — concise decision-ready briefing for C-suite. */
export const executiveBrief: Framework = {
  id: 'executive-brief',
  name: 'Executive Brief',
  description: 'Concise decision-ready briefing for C-suite and board audiences. Gets to the point fast with a clear ask.',
  audience: 'C-suite, board',
  slideRange: { min: 4, max: 8 },
  defaultTheme: 'midnight-teal',
  defaultStyle: 'clean',
  slots: [
    {
      position: 1,
      layout: 'cover',
      titleHint: '[Initiative Name] — [One-Line Value Proposition]',
      contentHint: 'Opening slide with company/project name and 2-3 top-level KPIs.',
      required: true,
    },
    {
      position: 2,
      layout: 'text',
      titleHint: '[Problem Statement as a Conclusion]',
      contentHint: 'State the core problem or opportunity in 3-5 bullets. Quantify the cost of inaction.',
      required: true,
    },
    {
      position: 3,
      layout: 'cards',
      titleHint: '[Solution Delivers Measurable Outcome]',
      contentHint: '3-4 cards summarizing solution pillars. Each card: title, key stat, one-sentence body.',
      required: true,
    },
    {
      position: 4,
      layout: 'number',
      titleHint: '[Key Impact Metric Proves Value]',
      contentHint: 'Single big number showing ROI, cost savings, or revenue impact with supporting context.',
      required: true,
    },
    {
      position: 5,
      layout: 'closing',
      titleHint: '[Clear Ask with Specific Next Steps]',
      contentHint: 'State the decision needed. 3-4 concrete next steps. Include contact for follow-up.',
      required: true,
    },
  ],
};

/** Sample manifest for Executive Brief framework — AI replaces placeholders. */
export const sampleManifest: DeckManifest = {
  title: '[Your Company] — Executive Brief',
  subtitle: '[One-line value proposition]',
  author: '[Your Name]',
  date: '2025-Q4',
  version: '1.0.0',
  theme: 'midnight-teal',
  style: 'clean',
  framework: 'executive-brief',
  slides: [
    {
      id: 'cover',
      layout: 'cover',
      title: '[Your Company] — [Initiative That Drives Growth]',
      subtitle: '[Brief context for the audience]',
      tagline: '[Memorable one-liner]',
      kpis: [
        { value: '[Key metric]', label: '[Metric name]' },
        { value: '[Key metric]', label: '[Metric name]' },
        { value: '[Key metric]', label: '[Metric name]' },
      ],
    },
    {
      id: 'problem',
      layout: 'text',
      title: '[Problem Costs Organization $X Annually]',
      columns: '1',
      body: '[Explain the core challenge in 2-3 sentences. Quantify the impact.]',
      bullets: [
        '[Current state metric that shows the gap]',
        '[Customer or stakeholder pain point]',
        '[Competitive risk or market pressure]',
      ],
    },
    {
      id: 'solution',
      layout: 'cards',
      title: '[Solution Delivers X% Improvement in Key Area]',
      cards: [
        { title: '[Pillar 1]', stat: '[Metric]', label: '[Label]', body: '[One sentence on value]' },
        { title: '[Pillar 2]', stat: '[Metric]', label: '[Label]', body: '[One sentence on value]' },
        { title: '[Pillar 3]', stat: '[Metric]', label: '[Label]', body: '[One sentence on value]' },
      ],
    },
    {
      id: 'impact',
      layout: 'number',
      title: '[Investment Returns X% in First Year]',
      stat: '[Value]',
      statLabel: '[What this number represents]',
      context: '[Supporting context: how this was calculated, comparison to alternatives]',
    },
    {
      id: 'ask',
      layout: 'closing',
      title: '[Requesting Approval to Proceed with Initiative]',
      nextSteps: [
        '[Specific decision needed from this audience]',
        '[Timeline for next milestone]',
        '[Resource or budget requirement]',
      ],
      contact: '[your-email@company.com]',
    },
  ],
};
