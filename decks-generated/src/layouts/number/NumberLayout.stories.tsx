import type { Meta, StoryObj } from '@storybook/react';
import { NumberLayout } from './NumberLayout.js';

const meta: Meta<typeof NumberLayout> = {
  title: 'Layouts/Number',
  component: NumberLayout,
};
export default meta;
type Story = StoryObj<typeof NumberLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'number-1',
      layout: 'number' as const,
      title: 'Customer retention reached an all-time high',
      stat: '142%',
      statLabel: 'Net Dollar Retention',
      context: 'Existing customers expanded usage faster than any cohort in company history.',
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'number-min',
      layout: 'number' as const,
      title: 'Record quarter for new bookings',
      stat: '$48M',
      statLabel: 'New ARR Added',
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'number-max',
      layout: 'number' as const,
      title: 'Platform reliability exceeds industry benchmarks',
      eyebrow: 'Infrastructure',
      stat: '99.997%',
      statLabel: 'Uptime (trailing 12 months)',
      context: 'Only 1.6 minutes of unplanned downtime in the past year, compared to the industry average of 87 minutes.',
      source: 'Datadog SLA Report, March 2026',
    },
  },
};
