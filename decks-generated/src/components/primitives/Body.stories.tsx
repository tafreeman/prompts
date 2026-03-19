import type { Meta, StoryObj } from '@storybook/react';
import { Body } from './Body.js';

const meta: Meta<typeof Body> = {
  title: 'Primitives/Body',
  component: Body,
};
export default meta;
type Story = StoryObj<typeof Body>;

export const Normal: Story = {
  args: {
    children:
      'Our platform processed 12 million transactions in Q3, representing a 40% increase from the previous quarter and validating our scalability investments.',
  },
};

export const Muted: Story = {
  args: {
    muted: true,
    children:
      'Figures represent trailing twelve-month averages adjusted for seasonal variation.',
  },
};

export const Caption: Story = {
  args: {
    size: 'CAPTION',
    children: 'Last updated March 2026. All figures in USD.',
  },
};
