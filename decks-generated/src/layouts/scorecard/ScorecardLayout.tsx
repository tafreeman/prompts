import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { ScorecardSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { useStyle } from '../../components/hooks/useStyle.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Eyebrow } from '../../components/primitives/Eyebrow.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { Card } from '../../components/primitives/Card.js';
import { KpiBadge } from '../../components/primitives/KpiBadge.js';
import { Body } from '../../components/primitives/Body.js';
import { CalloutBox } from '../../components/primitives/CalloutBox.js';
import { SourceLine } from '../../components/primitives/SourceLine.js';
import { SPACING } from '../../tokens/spacing.js';

type ScorecardData = z.infer<typeof ScorecardSlide>;

/**
 * Compute grid columns based on KPI count:
 * 1-2 → 2 cols, 3-4 → 2 cols, 5-6 → 3 cols, 7-8 → 4 cols.
 */
function gridColumns(count: number): number {
  if (count <= 4) return 2;
  if (count <= 6) return 3;
  return 4;
}

/**
 * Scorecard layout -- a grid of KPI metric cards with trend indicators.
 *
 * Design guide: scorecards surface the most important numbers at a glance.
 * Each KPI uses the KpiBadge primitive for value + label + trend arrow.
 * Optional detail text provides context below the badge.
 */
export function ScorecardLayout({ slide }: LayoutProps) {
  const data = slide as ScorecardData;
  const cols = gridColumns(data.kpis.length);

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    gap: SPACING.md,
  };

  const gridStyle: CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(${cols}, 1fr)`,
    gap: SPACING.md,
    flex: 1,
    alignContent: 'center',
  };

  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: SPACING.xs }}>
        {data.eyebrow && <Eyebrow>{data.eyebrow}</Eyebrow>}
        <Heading level="TITLE">{data.title}</Heading>
        <AccentBar width="80px" />
      </div>

      {/* KPI grid */}
      <div style={gridStyle}>
        {data.kpis.map((kpi, i) => (
          <Card key={i}>
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: SPACING.xs,
            }}>
              <KpiBadge
                value={kpi.value}
                label={kpi.label}
                trend={kpi.trend}
              />
              {kpi.detail && (
                <Body muted size="CAPTION" align="center">{kpi.detail}</Body>
              )}
            </div>
          </Card>
        ))}
      </div>

      {/* Footer */}
      {data.callout && <CalloutBox>{data.callout}</CalloutBox>}
      {data.source && <SourceLine source={data.source} />}
    </div>
  );
}
