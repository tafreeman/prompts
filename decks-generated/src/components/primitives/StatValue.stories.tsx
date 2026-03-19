import type { Meta, StoryObj } from '@storybook/react';
import { StatValue } from './StatValue.js';

const meta: Meta<typeof StatValue> = {
  title: 'Primitives/StatValue',
  component: StatValue,
};
export default meta;
type Story = StoryObj<typeof StatValue>;

export const NumberStat: Story = {
  args: { value: '4.2M', label: 'Monthly Active Users', trend: 'up' },
};

export const Percentage: Story = {
  args: { value: '99.7%', label: 'Uptime SLA', detail: 'Trailing 90-day average' },
};

export const Currency: Story = {
  args: { value: '$1.2B', label: 'Annual Recurring Revenue', trend: 'up' },
};
