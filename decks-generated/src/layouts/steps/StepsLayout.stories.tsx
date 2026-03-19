import type { Meta, StoryObj } from '@storybook/react';
import { StepsLayout } from './StepsLayout.js';

const meta: Meta<typeof StepsLayout> = {
  title: 'Layouts/Steps',
  component: StepsLayout,
};
export default meta;
type Story = StoryObj<typeof StepsLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'steps-1',
      layout: 'steps' as const,
      title: 'Four-phase migration delivers results in 90 days',
      steps: [
        { label: 'Assess', description: 'Audit current infrastructure and dependencies' },
        { label: 'Plan', description: 'Design target architecture and migration path' },
        { label: 'Migrate', description: 'Execute phased migration with zero downtime' },
        { label: 'Optimize', description: 'Tune performance and validate SLAs' },
      ],
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'steps-min',
      layout: 'steps' as const,
      title: 'Simple two-step process',
      steps: [
        { label: 'Connect' },
        { label: 'Deploy' },
      ],
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'steps-max',
      layout: 'steps' as const,
      title: 'End-to-end implementation follows a proven seven-step methodology',
      eyebrow: 'Implementation Guide',
      steps: [
        { label: 'Discovery', description: 'Map stakeholders and requirements' },
        { label: 'Design', description: 'Architecture and capacity planning' },
        { label: 'Provision', description: 'Infrastructure and environment setup' },
        { label: 'Develop', description: 'Build integrations and workflows' },
        { label: 'Test', description: 'Load testing and security audit' },
        { label: 'Deploy', description: 'Staged rollout with monitoring' },
        { label: 'Operate', description: 'Ongoing support and optimization' },
      ],
      callout: 'Average time-to-value: 45 days from kickoff to production.',
    },
  },
};
