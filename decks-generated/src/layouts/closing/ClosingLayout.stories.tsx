import type { Meta, StoryObj } from '@storybook/react';
import { ClosingLayout } from './ClosingLayout.js';

const meta: Meta<typeof ClosingLayout> = {
  title: 'Layouts/Closing',
  component: ClosingLayout,
};
export default meta;
type Story = StoryObj<typeof ClosingLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'closing-1',
      layout: 'closing' as const,
      title: 'Ready to Transform Your Workflow?',
      subtitle: 'Let us show you how our platform can accelerate your team.',
      nextSteps: [
        'Schedule a technical deep-dive',
        'Start a 14-day free trial',
        'Review our security documentation',
      ],
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'closing-min',
      layout: 'closing' as const,
      title: 'Thank You',
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'closing-max',
      layout: 'closing' as const,
      title: 'Partner With Us to Build the Future',
      subtitle: 'We are seeking strategic partners who share our vision for intelligent automation.',
      nextSteps: [
        'Sign LOI by end of quarter',
        'Begin joint technical evaluation',
        'Align go-to-market teams',
        'Launch co-branded pilot program',
      ],
      contact: 'partnerships@acme.dev | +1 (555) 123-4567',
      eyebrow: 'Next Steps',
    },
  },
};
