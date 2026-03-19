import type { Meta, StoryObj } from '@storybook/react';
import { CardsLayout } from './CardsLayout.js';

const meta: Meta<typeof CardsLayout> = {
  title: 'Layouts/Cards',
  component: CardsLayout,
};
export default meta;
type Story = StoryObj<typeof CardsLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'cards-1',
      layout: 'cards' as const,
      title: 'Three pillars drive our competitive advantage',
      cards: [
        { title: 'Speed', stat: '10x', label: 'Faster deploys', body: 'CI/CD pipeline runs in under 3 minutes.' },
        { title: 'Scale', stat: '4.2M', label: 'Daily requests', body: 'Auto-scaling handles peak loads seamlessly.' },
        { title: 'Security', stat: 'SOC 2', label: 'Certified', body: 'End-to-end encryption with zero-trust architecture.' },
      ],
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'cards-min',
      layout: 'cards' as const,
      title: 'Key differentiators',
      cards: [
        { title: 'Open Source' },
        { title: 'Cloud Native' },
      ],
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'cards-max',
      layout: 'cards' as const,
      title: 'Platform capabilities span the full development lifecycle',
      eyebrow: 'Product Overview',
      cards: [
        { title: 'Build', stat: '10x', label: 'Faster', body: 'AI-assisted code generation and review.' },
        { title: 'Test', stat: '99.7%', label: 'Coverage', body: 'Automated test suites with mutation testing.' },
        { title: 'Deploy', stat: '< 3min', label: 'Pipeline', body: 'Blue-green deployments with instant rollback.' },
        { title: 'Monitor', stat: '42ms', label: 'P99 latency', body: 'Real-time observability across all services.' },
        { title: 'Secure', stat: 'SOC 2', label: 'Type II', body: 'Continuous compliance monitoring and alerting.' },
        { title: 'Scale', stat: '10M', label: 'RPS', body: 'Auto-scaling from zero to planetary scale.' },
      ],
      callout: 'All capabilities available through a unified API and dashboard.',
      source: 'Product Engineering Team, 2026',
    },
  },
};
