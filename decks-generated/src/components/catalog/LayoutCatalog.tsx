import type { CSSProperties } from 'react';
import { ThemeContext } from '../context/ThemeContext.js';
import { StyleContext } from '../context/StyleContext.js';
import { LayoutRenderer } from '../../layouts/LayoutRenderer.js';
import { THEMES_BY_ID } from '../../tokens/themes.js';
import { STYLE_MODES_BY_ID } from '../../tokens/style-modes.js';
import { SLIDE_PADDING } from '../../tokens/spacing.js';
import { LAYOUT_IDS, type Slide } from '../../schemas/slide.js';

/** Logical slide dimensions matching SlideContainer. */
const LOGICAL_W = 1920;
const LOGICAL_H = 1080;
const DPI = 192;
const SCALE = 0.25;

/**
 * Minimal valid sample data for each layout type.
 * Used only for rendering previews in the catalog.
 */
const SAMPLE_DATA: Record<string, Slide> = {
  cover: {
    id: 'sample-cover',
    layout: 'cover',
    title: 'Acme Corp — Q4 Strategy Review',
    subtitle: 'Driving Growth Through Innovation',
    tagline: 'Built for the future',
    kpis: [
      { value: '$12M', label: 'Revenue' },
      { value: '340%', label: 'Growth' },
      { value: '98%', label: 'Retention' },
    ],
  },
  section: {
    id: 'sample-section',
    layout: 'section',
    title: 'Market Analysis',
    sectionNumber: 2,
  },
  text: {
    id: 'sample-text',
    layout: 'text',
    title: 'Cloud Adoption Accelerated 3x in Enterprise',
    body: 'Organizations are shifting workloads to cloud at an unprecedented pace, driven by cost efficiency and scalability requirements.',
    bullets: [
      '78% of enterprises now cloud-first',
      'Average migration timeline: 14 months',
      'Cost savings of 30-40% reported',
    ],
    columns: '1',
  },
  cards: {
    id: 'sample-cards',
    layout: 'cards',
    title: 'Three Pillars Drive Platform Differentiation',
    cards: [
      { title: 'Speed', stat: '<20ms', label: 'p99 Latency', body: 'Edge compute at 200+ locations' },
      { title: 'Scale', stat: '99.99%', label: 'Uptime', body: 'Auto-scaling with zero config' },
      { title: 'Simplicity', stat: '1 line', label: 'Migration', body: 'Drop-in replacement' },
    ],
  },
  number: {
    id: 'sample-number',
    layout: 'number',
    title: 'Edge Computing Market Reaches $61B by 2028',
    stat: '$61B',
    statLabel: 'Total Addressable Market',
    context: 'Growing 37% CAGR from $15B in 2024.',
  },
  compare: {
    id: 'sample-compare',
    layout: 'compare',
    title: 'New Platform Eliminates Key Bottlenecks',
    left: {
      title: 'Before',
      bullets: ['180ms latency', 'Manual scaling', '3 regions'],
    },
    right: {
      title: 'After',
      bullets: ['18ms latency', 'Auto-scaling', '200+ regions'],
    },
    callout: '10x improvement across all metrics',
  },
  steps: {
    id: 'sample-steps',
    layout: 'steps',
    title: 'Three Steps to Production Deployment',
    steps: [
      { label: 'Design', description: 'Architecture review and approval' },
      { label: 'Build', description: 'Implementation and testing' },
      { label: 'Deploy', description: 'Staged rollout to production' },
    ],
  },
  table: {
    id: 'sample-table',
    layout: 'table',
    title: 'Platform Outperforms on Every Key Metric',
    columns: ['Metric', 'Ours', 'Competitor A', 'Competitor B'],
    rows: [
      { Metric: 'Latency', Ours: '18ms', 'Competitor A': '65ms', 'Competitor B': '120ms' },
      { Metric: 'Uptime', Ours: '99.99%', 'Competitor A': '99.9%', 'Competitor B': '99.5%' },
      { Metric: 'Price', Ours: '$0.15/M', 'Competitor A': '$0.40/M', 'Competitor B': '$0.60/M' },
    ],
  },
  scorecard: {
    id: 'sample-scorecard',
    layout: 'scorecard',
    title: 'Key Metrics Show Strong Program Health',
    kpis: [
      { value: '$2.4M', label: 'ARR', trend: 'up' as const, detail: '14 months from $0' },
      { value: '42', label: 'Customers', trend: 'up' as const },
      { value: '118%', label: 'NRR', trend: 'up' as const },
      { value: '<2%', label: 'Churn', trend: 'down' as const },
    ],
  },
  timeline: {
    id: 'sample-timeline',
    layout: 'timeline',
    title: 'Clear Path to $10M ARR by Q4 2026',
    events: [
      { date: 'Q1 2025', title: 'Launch', description: 'GA release' },
      { date: 'Q3 2025', title: 'Enterprise', description: 'SOC 2, SSO' },
      { date: 'Q1 2026', title: 'Platform', description: 'Marketplace launch' },
      { date: 'Q4 2026', title: 'Scale', description: '$10M ARR' },
    ],
  },
  grid: {
    id: 'sample-grid',
    layout: 'grid',
    title: 'A Complete Edge Platform',
    columns: 3,
    cells: [
      { title: 'Compute', stat: '200+', body: 'V8 isolates, WASM', size: 'md' as const },
      { title: 'Storage', stat: '10ms', body: 'Distributed KV', size: 'md' as const },
      { title: 'Network', stat: 'Anycast', body: 'Global LB', size: 'md' as const },
    ],
  },
  closing: {
    id: 'sample-closing',
    layout: 'closing',
    title: 'Raising $8M to Capture the Edge Market',
    subtitle: 'Series A at $40M pre-money',
    nextSteps: [
      'Expand engineering team (8 to 20)',
      'Launch APAC and EU regions',
      'Build enterprise sales team',
    ],
    contact: 'founders@acmecloud.io',
  },
};

/** Layout display names — mirrors register-all.ts. */
const LAYOUT_NAMES: Record<string, string> = {
  cover: 'Cover',
  section: 'Section',
  text: 'Text',
  cards: 'Cards',
  number: 'Big Number',
  compare: 'Compare',
  steps: 'Steps',
  table: 'Table',
  scorecard: 'Scorecard',
  timeline: 'Timeline',
  grid: 'Grid',
  closing: 'Closing',
};

/**
 * Visual reference catalog showing all 12 layouts with sample data.
 * Each layout is rendered at 25% scale in a CSS grid.
 */
export function LayoutCatalog() {
  const theme = THEMES_BY_ID['midnight-teal'];
  const style = STYLE_MODES_BY_ID['clean'];

  const padTop = SLIDE_PADDING.top * DPI;
  const padRight = SLIDE_PADDING.right * DPI;
  const padBottom = SLIDE_PADDING.bottom * DPI;
  const padLeft = SLIDE_PADDING.left * DPI;

  const gridStyle: CSSProperties = {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: 24,
    padding: 32,
    maxWidth: 1600,
    margin: '0 auto',
    background: '#0B0F1A',
    minHeight: '100vh',
  };

  const headerStyle: CSSProperties = {
    gridColumn: '1 / -1',
    textAlign: 'center',
    padding: '24px 0 8px',
    fontFamily: 'system-ui, sans-serif',
  };

  return (
    <ThemeContext.Provider value={theme}>
      <StyleContext.Provider value={style}>
        <link href={theme.fontsUrl} rel="stylesheet" />
        <div style={gridStyle}>
          <div style={headerStyle}>
            <h1 style={{ color: '#F0F4F8', fontSize: 28, fontWeight: 700, margin: 0 }}>
              Layout Catalog
            </h1>
            <p style={{ color: '#64748B', fontSize: 14, marginTop: 8 }}>
              All 12 layouts rendered with sample data at 25% scale
            </p>
          </div>

          {LAYOUT_IDS.map((layoutId) => {
            const slide = SAMPLE_DATA[layoutId];
            if (!slide) return null;

            const cardStyle: CSSProperties = {
              background: '#111827',
              borderRadius: 12,
              overflow: 'hidden',
              border: '1px solid rgba(255,255,255,0.06)',
            };

            const labelStyle: CSSProperties = {
              padding: '10px 14px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            };

            const slideWrapperStyle: CSSProperties = {
              width: LOGICAL_W * SCALE,
              height: LOGICAL_H * SCALE,
              overflow: 'hidden',
              margin: '0 auto',
            };

            const slideInnerStyle: CSSProperties = {
              width: LOGICAL_W,
              height: LOGICAL_H,
              transform: `scale(${SCALE})`,
              transformOrigin: 'top left',
              background: theme.bg,
              padding: `${padTop}px ${padRight}px ${padBottom}px ${padLeft}px`,
              position: 'relative',
              overflow: 'hidden',
              fontFamily: `"${theme.fontBody}", system-ui, sans-serif`,
              color: theme.text,
            };

            return (
              <div key={layoutId} style={cardStyle}>
                <div style={slideWrapperStyle}>
                  <div style={slideInnerStyle}>
                    <LayoutRenderer slide={slide} />
                  </div>
                </div>
                <div style={labelStyle}>
                  <span style={{
                    color: '#F0F4F8',
                    fontSize: 13,
                    fontWeight: 600,
                    fontFamily: 'system-ui, sans-serif',
                  }}>
                    {LAYOUT_NAMES[layoutId] ?? layoutId}
                  </span>
                  <code style={{
                    color: '#64748B',
                    fontSize: 11,
                    fontFamily: 'monospace',
                    background: 'rgba(255,255,255,0.04)',
                    padding: '2px 6px',
                    borderRadius: 4,
                  }}>
                    {layoutId}
                  </code>
                </div>
              </div>
            );
          })}
        </div>
      </StyleContext.Provider>
    </ThemeContext.Provider>
  );
}
