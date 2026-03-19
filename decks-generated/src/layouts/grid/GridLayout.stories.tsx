import type { Meta, StoryObj } from '@storybook/react';
import { GridLayout } from './GridLayout.js';

const meta: Meta<typeof GridLayout> = {
  title: 'Layouts/Grid',
  component: GridLayout,
};
export default meta;
type Story = StoryObj<typeof GridLayout>;

export const Default: Story = {
  args: {
    slide: {
      id: 'grid-1',
      layout: 'grid' as const,
      title: 'Platform modules cover the full development lifecycle',
      columns: 3,
      cells: [
        { title: 'Build', body: 'AI-assisted code generation', stat: '10x', size: 'md' as const },
        { title: 'Test', body: 'Automated coverage and mutation testing', stat: '99%', size: 'md' as const },
        { title: 'Deploy', body: 'Zero-downtime blue-green deploys', stat: '< 3min', size: 'md' as const },
      ],
    },
  },
};

export const Minimal: Story = {
  args: {
    slide: {
      id: 'grid-min',
      layout: 'grid' as const,
      title: 'Two focus areas for next quarter',
      columns: 2,
      cells: [
        { title: 'Growth', size: 'md' as const },
        { title: 'Retention', size: 'md' as const },
      ],
    },
  },
};

export const Maximal: Story = {
  args: {
    slide: {
      id: 'grid-max',
      layout: 'grid' as const,
      title: 'Nine capabilities differentiate our platform from alternatives',
      eyebrow: 'Product Matrix',
      columns: 3,
      cells: [
        { title: 'Auth', body: 'SSO, MFA, RBAC out of the box', stat: '< 5min', size: 'md' as const },
        { title: 'API Gateway', body: 'Rate limiting, caching, transforms', stat: '10M RPS', size: 'lg' as const },
        { title: 'Compute', body: 'Serverless and container workloads', size: 'md' as const },
        { title: 'Storage', body: 'Object, block, and file storage', stat: '99.999%', size: 'md' as const },
        { title: 'Observability', body: 'Logs, metrics, and traces unified', size: 'md' as const },
        { title: 'ML Pipeline', body: 'Train, evaluate, deploy models', stat: '3x faster', size: 'lg' as const },
        { title: 'Edge', body: 'Global CDN with edge compute', stat: '< 50ms', size: 'md' as const },
        { title: 'Security', body: 'Continuous compliance monitoring', size: 'md' as const },
        { title: 'Support', body: '24/7 enterprise support team', stat: '< 1hr', size: 'md' as const },
      ],
      callout: 'All modules included in the enterprise tier at a single price point.',
    },
  },
};
