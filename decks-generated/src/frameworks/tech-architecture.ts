import type { Framework } from '../schemas/framework.js';
import type { DeckManifest } from '../schemas/manifest.js';

/** Tech Architecture — engineering-focused system design presentation. */
export const techArchitecture: Framework = {
  id: 'tech-architecture',
  name: 'Tech Architecture',
  description: 'Engineering-focused system design presentation. Covers context, before/after comparison, architecture overview, implementation plan, and success metrics.',
  audience: 'Engineering teams',
  slideRange: { min: 6, max: 10 },
  defaultTheme: 'linear',
  defaultStyle: 'editorial',
  slots: [
    {
      position: 1,
      layout: 'cover',
      titleHint: '[System/Project Name] — Architecture Overview',
      contentHint: 'System name and 2-3 key technical metrics (latency, throughput, availability).',
      required: true,
    },
    {
      position: 2,
      layout: 'text',
      titleHint: '[Context: Why This Architecture Decision Matters]',
      contentHint: 'Business context, technical constraints, and key requirements in 3-5 bullets.',
      required: true,
    },
    {
      position: 3,
      layout: 'compare',
      titleHint: '[New Architecture Resolves Key Limitations]',
      contentHint: 'Left: current architecture limitations. Right: proposed architecture benefits.',
      required: true,
    },
    {
      position: 4,
      layout: 'grid',
      titleHint: '[Architecture Components and Responsibilities]',
      contentHint: '4-6 cells showing major system components with key specs.',
      required: true,
    },
    {
      position: 5,
      layout: 'steps',
      titleHint: '[Implementation Follows Phased Rollout Plan]',
      contentHint: '3-5 implementation phases with deliverables per phase.',
      required: true,
    },
    {
      position: 6,
      layout: 'table',
      titleHint: '[Success Metrics Define Done for Each Phase]',
      contentHint: 'Table with metrics, current values, targets, and measurement method.',
      required: true,
    },
    {
      position: 7,
      layout: 'timeline',
      titleHint: '[Rollout Timeline Targets Production by Date]',
      contentHint: '4-6 milestones from design review to production GA.',
      required: false,
    },
    {
      position: 8,
      layout: 'closing',
      titleHint: '[Requesting Review Approval to Begin Phase 1]',
      contentHint: 'Decision needed, review process, next steps with owners.',
      required: true,
    },
  ],
};

/** Sample manifest for Tech Architecture framework — AI replaces placeholders. */
export const sampleManifest: DeckManifest = {
  title: '[System Name] — Architecture Review',
  subtitle: 'Technical Design Document',
  author: '[Engineering Lead]',
  date: '2025-Q4',
  version: '1.0.0',
  theme: 'linear',
  style: 'editorial',
  framework: 'tech-architecture',
  slides: [
    {
      id: 'cover',
      layout: 'cover',
      title: '[System Name] — [Architecture Decision Title]',
      subtitle: 'Architecture Review — [Team Name]',
      kpis: [
        { value: '[Metric]', label: '[e.g., p99 Latency]' },
        { value: '[Metric]', label: '[e.g., Throughput]' },
        { value: '[Metric]', label: '[e.g., Availability]' },
      ],
    },
    {
      id: 'context',
      layout: 'text',
      title: '[Business Need Drives Architecture Change]',
      columns: '1',
      body: '[Explain the business context and technical motivation in 2-3 sentences.]',
      bullets: [
        '[Key technical requirement or constraint]',
        '[Scale target or performance requirement]',
        '[Compliance or security requirement]',
        '[Team or operational constraint]',
      ],
    },
    {
      id: 'before-after',
      layout: 'compare',
      title: '[New Design Eliminates Key Bottlenecks]',
      left: {
        title: 'Current Architecture',
        bullets: [
          '[Limitation or bottleneck 1]',
          '[Limitation or bottleneck 2]',
          '[Limitation or bottleneck 3]',
          '[Operational pain point]',
        ],
      },
      right: {
        title: 'Proposed Architecture',
        bullets: [
          '[How it addresses limitation 1]',
          '[How it addresses limitation 2]',
          '[How it addresses limitation 3]',
          '[Operational improvement]',
        ],
      },
    },
    {
      id: 'architecture',
      layout: 'grid',
      title: '[System Comprises N Core Components]',
      columns: 3,
      cells: [
        { title: '[Component 1]', stat: '[Key spec]', body: '[Responsibility description]', size: 'md' },
        { title: '[Component 2]', stat: '[Key spec]', body: '[Responsibility description]', size: 'md' },
        { title: '[Component 3]', stat: '[Key spec]', body: '[Responsibility description]', size: 'md' },
        { title: '[Component 4]', stat: '[Key spec]', body: '[Responsibility description]', size: 'md' },
        { title: '[Component 5]', body: '[Responsibility description]', size: 'md' },
        { title: '[Component 6]', body: '[Responsibility description]', size: 'md' },
      ],
    },
    {
      id: 'implementation',
      layout: 'steps',
      title: '[Four-Phase Rollout Minimizes Risk]',
      steps: [
        { label: 'Phase 1: Foundation', description: '[Core infrastructure and data migration]' },
        { label: 'Phase 2: Core Services', description: '[Primary service implementation]' },
        { label: 'Phase 3: Integration', description: '[System integration and testing]' },
        { label: 'Phase 4: Cutover', description: '[Traffic migration and validation]' },
      ],
    },
    {
      id: 'metrics',
      layout: 'table',
      title: '[Success Metrics Track Progress Across Phases]',
      columns: ['Metric', 'Current', 'Target', 'Measurement'],
      rows: [
        { Metric: '[e.g., p99 Latency]', Current: '[Value]', Target: '[Value]', Measurement: '[How measured]' },
        { Metric: '[e.g., Throughput]', Current: '[Value]', Target: '[Value]', Measurement: '[How measured]' },
        { Metric: '[e.g., Error Rate]', Current: '[Value]', Target: '[Value]', Measurement: '[How measured]' },
        { Metric: '[e.g., Deploy Time]', Current: '[Value]', Target: '[Value]', Measurement: '[How measured]' },
      ],
    },
    {
      id: 'timeline',
      layout: 'timeline',
      title: '[Production Readiness Targeted for Date]',
      events: [
        { date: '[Week 1-2]', title: 'Design Review', description: '[Architecture review and approval]' },
        { date: '[Week 3-6]', title: 'Phase 1', description: '[Foundation and infrastructure]' },
        { date: '[Week 7-10]', title: 'Phase 2-3', description: '[Core services and integration]' },
        { date: '[Week 11-12]', title: 'GA', description: '[Production cutover and validation]' },
      ],
    },
    {
      id: 'next',
      layout: 'closing',
      title: '[Requesting Architecture Review Approval]',
      nextSteps: [
        '[Schedule design review with platform team]',
        '[Finalize resource allocation for Phase 1]',
        '[Set up monitoring and alerting infrastructure]',
        '[Begin Phase 1 sprint planning]',
      ],
      contact: '[tech-lead@company.com]',
    },
  ],
};
