import type { Meta, StoryObj } from '@storybook/react';
import { ScorecardLayout } from './ScorecardLayout.js';

const meta: Meta<typeof ScorecardLayout> = {
  title: 'Layouts/Scorecard',
  component: ScorecardLayout,
};
export default meta;
type Story = StoryObj<typeof ScorecardLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'scorecard-1',
      layout: 'scorecard' as const,
      title: 'All operational KPIs trending positively this quarter',
      kpis: [
        { value: '$1.2B', label: 'ARR', trend: 'up' as const },
        { value: '4.2M', label: 'MAU', trend: 'up' as const },
        { value: '142%', label: 'NDR', trend: 'up' as const },
        { value: '42ms', label: 'P99 Latency', trend: 'down' as const },
      ],
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'scorecard-min',
      layout: 'scorecard' as const,
      title: 'Revenue health check',
      kpis: [
        { value: '$48M', label: 'MRR' },
      ],
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'scorecard-max',
      layout: 'scorecard' as const,
      title: 'Comprehensive health dashboard shows strong execution across all pillars',
      eyebrow: 'Executive Dashboard',
      kpis: [
        { value: '$1.2B', label: 'ARR', trend: 'up' as const, detail: '+45% YoY' },
        { value: '4.2M', label: 'MAU', trend: 'up' as const, detail: '+60% QoQ' },
        { value: '142%', label: 'NDR', trend: 'up' as const, detail: 'Best in class' },
        { value: '< 12mo', label: 'CAC Payback', trend: 'down' as const, detail: 'From 18mo' },
        { value: '78%', label: 'Gross Margin', trend: 'up' as const, detail: '+3pp QoQ' },
        { value: '42ms', label: 'P99 Latency', trend: 'down' as const, detail: 'From 120ms' },
        { value: '99.99%', label: 'Uptime', trend: 'flat' as const, detail: 'SLA met' },
        { value: '87', label: 'NPS', trend: 'up' as const, detail: '+12 points' },
      ],
      callout: 'All KPIs at or above target for the third consecutive quarter.',
      source: 'BizOps Dashboard, March 2026',
    },
  },
};
