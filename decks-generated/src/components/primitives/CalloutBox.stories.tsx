import type { Meta, StoryObj } from '@storybook/react';
import { CalloutBox } from './CalloutBox.js';

const meta: Meta<typeof CalloutBox> = {
  title: 'Primitives/CalloutBox',
  component: CalloutBox,
};
export default meta;
type Story = StoryObj<typeof CalloutBox>;

export const ShortText: Story = {
  args: {
    children: 'Key insight: early adopters convert 3x faster than organic signups.',
  },
};

export const LongText: Story = {
  args: {
    children:
      'The migration to a microservices architecture reduced our deployment cycle from two weeks to under four hours, while simultaneously improving system reliability from 99.5% to 99.97% uptime across all production services.',
    variant: 'success',
  },
};
