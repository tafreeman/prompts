import type { Meta, StoryObj } from '@storybook/react';
import { TimelineLayout } from './TimelineLayout.js';

const meta: Meta<typeof TimelineLayout> = {
  title: 'Layouts/Timeline',
  component: TimelineLayout,
};
export default meta;
type Story = StoryObj<typeof TimelineLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'timeline-1',
      layout: 'timeline' as const,
      title: 'Product roadmap delivers three major milestones in 2026',
      events: [
        { date: 'Q1 2026', title: 'API v3 Launch', description: 'Unified REST and GraphQL gateway' },
        { date: 'Q2 2026', title: 'Enterprise SSO', description: 'SAML 2.0 and OIDC integration' },
        { date: 'Q3 2026', title: 'AI Copilot GA', description: 'Embedded AI assistance across all workflows' },
      ],
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'timeline-min',
      layout: 'timeline' as const,
      title: 'Key milestones completed this year',
      events: [
        { date: 'Jan 2026', title: 'Series A closed' },
        { date: 'Mar 2026', title: 'First enterprise customer' },
      ],
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'timeline-max',
      layout: 'timeline' as const,
      title: 'Company journey from founding to market leadership',
      eyebrow: 'Company History',
      events: [
        { date: '2020', title: 'Founded', description: 'Two co-founders in a garage' },
        { date: '2021', title: 'Seed Round', description: '$3M from top-tier angels' },
        { date: '2022', title: 'Product-Market Fit', description: 'First 100 paying customers' },
        { date: '2023', title: 'Series A', description: '$25M led by Benchmark' },
        { date: '2024', title: 'Enterprise Launch', description: 'SOC 2 + first Fortune 500 deal' },
        { date: '2025', title: 'Series B', description: '$80M at $800M valuation' },
        { date: '2026', title: 'Market Leader', description: 'Gartner Leader quadrant placement' },
      ],
      callout: 'From zero to $1B ARR in six years.',
    },
  },
};
