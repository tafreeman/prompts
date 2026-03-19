import type { Meta, StoryObj } from '@storybook/react';
import { BulletList } from './BulletList.js';

const meta: Meta<typeof BulletList> = {
  title: 'Primitives/BulletList',
  component: BulletList,
};
export default meta;
type Story = StoryObj<typeof BulletList>;

export const ThreeItems: Story = {
  args: {
    items: [
      'Reduced deployment time by 60%',
      'Eliminated manual configuration drift',
      'Improved MTTR from 4 hours to 15 minutes',
    ],
  },
};

export const SevenItems: Story = {
  args: {
    items: [
      'Define service boundaries',
      'Implement API contracts',
      'Set up CI/CD pipeline',
      'Configure monitoring',
      'Deploy canary release',
      'Run load tests',
      'Full production rollout',
    ],
    marker: 'number',
  },
};
