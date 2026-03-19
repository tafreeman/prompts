import type { Meta, StoryObj } from '@storybook/react';
import { CompareLayout } from './CompareLayout.js';

const meta: Meta<typeof CompareLayout> = {
  title: 'Layouts/Compare',
  component: CompareLayout,
};
export default meta;
type Story = StoryObj<typeof CompareLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'compare-1',
      layout: 'compare' as const,
      title: 'Microservices outperform monolith on every dimension',
      left: {
        title: 'Before (Monolith)',
        bullets: [
          '2-week deploy cycles',
          'Single point of failure',
          'Team coupling slowed delivery',
        ],
      },
      right: {
        title: 'After (Microservices)',
        bullets: [
          'Multiple deploys per day',
          'Isolated failure domains',
          'Independent team velocity',
        ],
      },
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'compare-min',
      layout: 'compare' as const,
      title: 'Cloud vs on-premise cost comparison',
      left: { title: 'Cloud' },
      right: { title: 'On-Premise' },
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'compare-max',
      layout: 'compare' as const,
      title: 'Our platform delivers 10x improvement over legacy tooling',
      eyebrow: 'Competitive Analysis',
      left: {
        title: 'Legacy Approach',
        body: 'Manual processes with fragmented toolchains.',
        bullets: [
          '6-week integration timeline',
          '$500K annual maintenance cost',
          '72-hour incident response',
          'No self-service capability',
        ],
      },
      right: {
        title: 'Our Platform',
        body: 'Unified API-first automation platform.',
        bullets: [
          '3-day integration timeline',
          '$50K annual platform cost',
          '15-minute automated remediation',
          'Full self-service portal',
        ],
      },
      callout: 'Customers report 90% reduction in total cost of ownership within 6 months.',
      source: 'Customer survey, N=340, Feb 2026',
    },
  },
};
