import type { Meta, StoryObj } from '@storybook/react';
import { TextLayout } from './TextLayout.js';

const meta: Meta<typeof TextLayout> = {
  title: 'Layouts/Text',
  component: TextLayout,
};
export default meta;
type Story = StoryObj<typeof TextLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'text-1',
      layout: 'text' as const,
      title: 'Platform adoption accelerated across all segments',
      columns: '1' as const,
      body: 'Enterprise customers increased usage by 60% quarter-over-quarter, driven by our new API-first integration framework and self-service provisioning.',
      bullets: [
        'API call volume grew from 2M to 8M per day',
        'Average integration time dropped from 6 weeks to 3 days',
        'Self-service onboarding now accounts for 40% of new activations',
      ],
      source: 'Internal analytics, March 2026',
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'text-min',
      layout: 'text' as const,
      title: 'Revenue grew 40% year-over-year',
      columns: '1' as const,
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'text-max',
      layout: 'text' as const,
      title: 'Two distinct growth engines drive platform expansion',
      eyebrow: 'Growth Strategy',
      columns: '2' as const,
      leftColumn: {
        title: 'Product-Led Growth',
        body: 'Self-service signups and viral adoption loops.',
        bullets: [
          'Free tier drives 50K monthly signups',
          '12% conversion to paid within 30 days',
          'Viral coefficient of 1.3',
        ],
      },
      rightColumn: {
        title: 'Sales-Led Expansion',
        body: 'Enterprise sales team lands $100K+ ACV deals.',
        bullets: [
          'Average deal size increased to $240K',
          'Sales cycle shortened to 45 days',
          '142% net dollar retention',
        ],
      },
      callout: 'Combined approach yields 3x faster growth than either channel alone.',
      source: 'RevOps Dashboard, Q3 2026',
    },
  },
};
