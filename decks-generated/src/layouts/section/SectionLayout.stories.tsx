import type { Meta, StoryObj } from '@storybook/react';
import { SectionLayout } from './SectionLayout.js';

const meta: Meta<typeof SectionLayout> = {
  title: 'Layouts/Section',
  component: SectionLayout,
};
export default meta;
type Story = StoryObj<typeof SectionLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'section-1',
      layout: 'section' as const,
      title: 'Market Opportunity',
      sectionNumber: 1,
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'section-min',
      layout: 'section' as const,
      title: 'Appendix',
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'section-max',
      layout: 'section' as const,
      title: 'Product Strategy & Roadmap',
      subtitle: 'Three pillars driving our next phase of growth',
      sectionNumber: 3,
      eyebrow: 'Strategic Overview',
    },
  },
};
