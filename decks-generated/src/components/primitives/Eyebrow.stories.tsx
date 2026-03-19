import type { Meta, StoryObj } from '@storybook/react';
import { Eyebrow } from './Eyebrow.js';

const meta: Meta<typeof Eyebrow> = {
  title: 'Primitives/Eyebrow',
  component: Eyebrow,
};
export default meta;
type Story = StoryObj<typeof Eyebrow>;

export const ShortLabel: Story = {
  args: { children: 'Q3 2026 Results' },
};
