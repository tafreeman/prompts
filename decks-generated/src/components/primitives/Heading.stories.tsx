import type { Meta, StoryObj } from '@storybook/react';
import { Heading } from './Heading.js';

const meta: Meta<typeof Heading> = {
  title: 'Primitives/Heading',
  component: Heading,
};
export default meta;
type Story = StoryObj<typeof Heading>;

export const Hero: Story = {
  args: { level: 'HERO', children: 'Revenue grew 40% year-over-year' },
};

export const Title: Story = {
  args: { level: 'TITLE', children: 'Platform adoption accelerated in Q3' },
};

export const Section: Story = {
  args: { level: 'SECTION', children: 'Key Findings' },
};

export const CardLevel: Story = {
  args: { level: 'CARD', children: 'Monthly Active Users' },
};
