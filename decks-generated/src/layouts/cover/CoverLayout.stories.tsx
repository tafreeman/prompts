import type { Meta, StoryObj } from '@storybook/react';
import { CoverLayout } from './CoverLayout.js';

const meta: Meta<typeof CoverLayout> = {
  title: 'Layouts/Cover',
  component: CoverLayout,
};
export default meta;
type Story = StoryObj<typeof CoverLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'cover-1',
      layout: 'cover' as const,
      title: 'AI-Native Platform Strategy',
      subtitle: 'Transforming enterprise workflows with intelligent automation',
      eyebrow: 'Q3 2026 Board Review',
      kpis: [
        { value: '4.2M', label: 'MAU', trend: 'up' as const },
        { value: '$1.2B', label: 'ARR', trend: 'up' as const },
        { value: '99.9%', label: 'Uptime', trend: 'flat' as const },
      ],
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'cover-min',
      layout: 'cover' as const,
      title: 'Quarterly Business Review',
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'cover-max',
      layout: 'cover' as const,
      title: 'Series B Investor Update',
      subtitle: 'Record quarter driven by enterprise expansion and platform stickiness',
      eyebrow: 'Confidential',
      tagline: 'Building the operating system for modern enterprises',
      kpis: [
        { value: '$1.2B', label: 'ARR', trend: 'up' as const },
        { value: '4.2M', label: 'MAU', trend: 'up' as const },
        { value: '142%', label: 'NDR', trend: 'up' as const },
        { value: '< 12mo', label: 'Payback', trend: 'down' as const },
      ],
      notes: 'Speaker notes for the presenter',
    },
  },
};
