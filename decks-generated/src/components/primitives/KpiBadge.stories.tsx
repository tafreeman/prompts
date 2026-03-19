import type { Meta, StoryObj } from '@storybook/react';
import { KpiBadge } from './KpiBadge.js';

const meta: Meta<typeof KpiBadge> = {
  title: 'Primitives/KpiBadge',
  component: KpiBadge,
};
export default meta;
type Story = StoryObj<typeof KpiBadge>;

export const TrendUp: Story = {
  args: { value: '4.2M', label: 'MAU', trend: 'up' },
};

export const TrendDown: Story = {
  args: { value: '12ms', label: 'Latency', trend: 'down' },
};

export const TrendFlat: Story = {
  args: { value: '99.9%', label: 'SLA', trend: 'flat' },
};
