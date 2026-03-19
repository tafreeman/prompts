import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { Card } from './Card.js';
import { Heading } from './Heading.js';
import { Body } from './Body.js';

const meta: Meta<typeof Card> = {
  title: 'Primitives/Card',
  component: Card,
};
export default meta;
type Story = StoryObj<typeof Card>;

export const WithAccentBar: Story = {
  render: (args) => (
    <Card {...args}>
      <Heading level="CARD">Monthly Active Users</Heading>
      <Body muted>Up 24% from last quarter across all regions.</Body>
    </Card>
  ),
  args: { showAccentBar: true },
};

export const WithoutAccentBar: Story = {
  render: (args) => (
    <Card {...args}>
      <Heading level="CARD">API Latency</Heading>
      <Body muted>P99 response time dropped to 42ms.</Body>
    </Card>
  ),
  args: { showAccentBar: false },
};

export const Hoverable: Story = {
  render: (args) => (
    <Card {...args}>
      <Heading level="CARD">Interactive Card</Heading>
      <Body muted>This card responds to hover interactions.</Body>
    </Card>
  ),
  args: { hoverable: true, showAccentBar: true },
};
