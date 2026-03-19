import type { Meta, StoryObj } from '@storybook/react';
import { TableLayout } from './TableLayout.js';

const meta: Meta<typeof TableLayout> = {
  title: 'Layouts/Table',
  component: TableLayout,
};
export default meta;
type Story = StoryObj<typeof TableLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'table-1',
      layout: 'table' as const,
      title: 'Revenue by segment shows enterprise dominance',
      columns: ['Segment', 'ARR', 'Growth', 'Margin'],
      rows: [
        { Segment: 'Enterprise', ARR: '$820M', Growth: '45%', Margin: '78%' },
        { Segment: 'Mid-Market', ARR: '$280M', Growth: '32%', Margin: '65%' },
        { Segment: 'SMB', ARR: '$100M', Growth: '18%', Margin: '52%' },
      ],
      source: 'Finance Team, Q3 2026',
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'table-min',
      layout: 'table' as const,
      title: 'Feature comparison matrix',
      columns: ['Feature', 'Status'],
      rows: [
        { Feature: 'SSO', Status: 'GA' },
        { Feature: 'RBAC', Status: 'Beta' },
      ],
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'table-max',
      layout: 'table' as const,
      title: 'Competitive landscape favors our positioning on key dimensions',
      eyebrow: 'Market Analysis',
      columns: ['Vendor', 'Price', 'Uptime', 'API Coverage', 'Support SLA', 'Security'],
      rows: [
        { Vendor: 'Us', Price: '$$', Uptime: '99.99%', 'API Coverage': '100%', 'Support SLA': '< 1hr', Security: 'SOC 2 + ISO' },
        { Vendor: 'Competitor A', Price: '$$$', Uptime: '99.9%', 'API Coverage': '80%', 'Support SLA': '< 4hr', Security: 'SOC 2' },
        { Vendor: 'Competitor B', Price: '$', Uptime: '99.5%', 'API Coverage': '60%', 'Support SLA': '< 24hr', Security: 'None' },
        { Vendor: 'Competitor C', Price: '$$$$', Uptime: '99.95%', 'API Coverage': '90%', 'Support SLA': '< 2hr', Security: 'SOC 2' },
      ],
      highlight: 'Us',
      source: 'G2 Crowd Reviews + Internal Research, 2026',
    },
  },
};
