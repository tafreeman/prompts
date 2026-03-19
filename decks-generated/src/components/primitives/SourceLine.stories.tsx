import type { Meta, StoryObj } from '@storybook/react';
import { SourceLine } from './SourceLine.js';

const meta: Meta<typeof SourceLine> = {
  title: 'Primitives/SourceLine',
  component: SourceLine,
};
export default meta;
type Story = StoryObj<typeof SourceLine>;

export const Attribution: Story = {
  args: { source: 'Gartner Magic Quadrant for Cloud Infrastructure, 2026' },
};
