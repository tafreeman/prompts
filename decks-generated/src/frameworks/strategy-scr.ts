import type { Framework } from '../schemas/framework.js';
import type { DeckManifest } from '../schemas/manifest.js';

/** Strategy SCR — Situation-Complication-Resolution for internal stakeholders. */
export const strategySCR: Framework = {
  id: 'strategy-scr',
  name: 'Strategy (SCR)',
  description: 'Situation-Complication-Resolution framework for internal strategy presentations. Builds a logical argument from context to action.',
  audience: 'Internal stakeholders',
  slideRange: { min: 5, max: 8 },
  defaultTheme: 'signal-cobalt',
  defaultStyle: 'clean',
  slots: [
    {
      position: 1,
      layout: 'cover',
      titleHint: '[Strategy Initiative] — [Desired Outcome]',
      contentHint: 'Strategy name and 2-3 KPIs showing current state or target.',
      required: true,
    },
    {
      position: 2,
      layout: 'text',
      titleHint: '[Current Situation Summary with Key Context]',
      contentHint: 'Establish shared understanding of where things stand. 3-5 factual bullets.',
      required: true,
    },
    {
      position: 3,
      layout: 'compare',
      titleHint: '[Complication Creates Urgency to Act Now]',
      contentHint: 'Left: current state with pain points. Right: what happens if we act (or do nothing).',
      required: true,
    },
    {
      position: 4,
      layout: 'steps',
      titleHint: '[Resolution: X-Step Plan to Achieve Outcome]',
      contentHint: '3-5 concrete steps with descriptions. Each step actionable and ownable.',
      required: true,
    },
    {
      position: 5,
      layout: 'scorecard',
      titleHint: '[Evidence Supports This Approach]',
      contentHint: '3-5 KPIs from pilots, benchmarks, or comparable initiatives.',
      required: false,
    },
    {
      position: 6,
      layout: 'closing',
      titleHint: '[Requesting Alignment on Next Steps]',
      contentHint: 'Clear ask, 3-4 next steps with owners and timelines.',
      required: true,
    },
  ],
};

/** Sample manifest for Strategy SCR framework — AI replaces placeholders. */
export const sampleManifest: DeckManifest = {
  title: '[Strategy Initiative Name]',
  subtitle: 'Situation-Complication-Resolution',
  author: '[Your Name]',
  date: '2025-Q4',
  version: '1.0.0',
  theme: 'signal-cobalt',
  style: 'clean',
  framework: 'strategy-scr',
  slides: [
    {
      id: 'cover',
      layout: 'cover',
      title: '[Initiative Name] — [Achieving Target Outcome]',
      subtitle: '[Team or department context]',
      kpis: [
        { value: '[Current metric]', label: '[Metric name]' },
        { value: '[Target metric]', label: '[Target name]' },
      ],
    },
    {
      id: 'situation',
      layout: 'text',
      title: '[Current State Provides Foundation for Change]',
      columns: '1',
      body: '[Brief context paragraph establishing the shared understanding.]',
      bullets: [
        '[Factual observation about current state]',
        '[Key data point the audience agrees on]',
        '[Relevant market or competitive context]',
      ],
    },
    {
      id: 'complication',
      layout: 'compare',
      title: '[Gap Between Current and Needed State Grows]',
      left: {
        title: 'Current State',
        bullets: [
          '[Pain point or limitation 1]',
          '[Pain point or limitation 2]',
          '[Pain point or limitation 3]',
        ],
      },
      right: {
        title: 'If We Act Now',
        bullets: [
          '[Opportunity or benefit 1]',
          '[Opportunity or benefit 2]',
          '[Opportunity or benefit 3]',
        ],
      },
      callout: '[Why acting now matters — urgency statement]',
    },
    {
      id: 'resolution',
      layout: 'steps',
      title: '[Three-Phase Plan Closes the Gap by Target Date]',
      steps: [
        { label: '[Phase 1]', description: '[Concrete action with timeline]' },
        { label: '[Phase 2]', description: '[Concrete action with timeline]' },
        { label: '[Phase 3]', description: '[Concrete action with timeline]' },
      ],
      callout: '[Expected timeline: X weeks/months]',
    },
    {
      id: 'evidence',
      layout: 'scorecard',
      title: '[Pilot Results Validate This Approach]',
      kpis: [
        { value: '[Metric]', label: '[What it measures]', trend: 'up' },
        { value: '[Metric]', label: '[What it measures]', trend: 'up' },
        { value: '[Metric]', label: '[What it measures]', trend: 'flat' },
      ],
      source: '[Pilot program, date]',
    },
    {
      id: 'next-steps',
      layout: 'closing',
      title: '[Requesting Team Alignment on Resolution Plan]',
      nextSteps: [
        '[Decision needed from leadership]',
        '[Resource allocation requirement]',
        '[First milestone and owner]',
        '[Review checkpoint date]',
      ],
      contact: '[your-email@company.com]',
    },
  ],
};
