import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { SlideContainer } from './SlideContainer.js';
import { Heading } from '../primitives/Heading.js';
import { Body } from '../primitives/Body.js';

const meta: Meta<typeof SlideContainer> = {
  title: 'Deck/SlideContainer',
  component: SlideContainer,
  decorators: [
    // Override the default preview decorator sizing — SlideContainer
    // manages its own 16:9 viewport, so we give it full area.
    (Story) => (
      <div style={{ width: '100%', height: '100%', position: 'absolute', inset: 0 }}>
        <Story />
      </div>
    ),
  ],
};
export default meta;
type Story = StoryObj<typeof SlideContainer>;

export const Empty: Story = {
  args: {},
  render: (args) => <SlideContainer {...args}>{null}</SlideContainer>,
};

export const WithContent: Story = {
  render: (args) => (
    <SlideContainer {...args}>
      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%', gap: 16 }}>
        <Heading level="HERO" align="center">Sample Slide Content</Heading>
        <Body align="center" muted>This demonstrates the SlideContainer viewport scaling.</Body>
      </div>
    </SlideContainer>
  ),
};

export const WithBgOverride: Story = {
  render: () => (
    <SlideContainer bgOverride="#1a0030">
      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%', gap: 16 }}>
        <Heading level="HERO" align="center" color="#ffffff">Custom Background</Heading>
        <Body align="center">Background override is set to deep purple.</Body>
      </div>
    </SlideContainer>
  ),
};
