import type { Meta, StoryObj } from '@storybook/react';
import { AccentBar } from './AccentBar.js';

const meta: Meta<typeof AccentBar> = {
  title: 'Primitives/AccentBar',
  component: AccentBar,
};
export default meta;
type Story = StoryObj<typeof AccentBar>;

export const Default: Story = {
  args: {},
};

export const CustomWidth: Story = {
  args: { width: '200px' },
};
