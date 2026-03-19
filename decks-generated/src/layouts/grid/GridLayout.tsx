import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { GridSlide } from '../../schemas/slide.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Eyebrow } from '../../components/primitives/Eyebrow.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { Card } from '../../components/primitives/Card.js';
import { StatValue } from '../../components/primitives/StatValue.js';
import { Body } from '../../components/primitives/Body.js';
import { CalloutBox } from '../../components/primitives/CalloutBox.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { useStyle } from '../../components/hooks/useStyle.js';
import { SPACING } from '../../tokens/spacing.js';

type GridData = z.infer<typeof GridSlide>;

/**
 * Grid layout — 2-9 cells in a CSS grid with configurable columns.
 *
 * Design guide: cells provide flexible card-based content. Large cells
 * span 2 columns for emphasis. Each cell can contain a stat, title,
 * and body text.
 */
export function GridLayout({ slide }: LayoutProps) {
  const data = slide as GridData;
  const cols = data.columns ?? 3;
  const theme = useTheme();
  const style = useStyle();

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

      {/* Cell grid */}
      <div style={gridStyle}>
        {data.cells.map((cell, i) => {
          const cellStyle: CSSProperties =
            cell.size === 'lg' ? { gridColumn: 'span 2' } : {};

          return (
            <div key={i} style={cellStyle}>
              <Card>
                <div style={{ display: 'flex', flexDirection: 'column', gap: SPACING.xs }}>
                  {cell.stat != null && (
                    <StatValue value={cell.stat} label="" />
                  )}
                  <Heading level="CARD">{cell.title}</Heading>
                  {cell.body && <Body muted>{cell.body}</Body>}
                </div>
              </Card>
            </div>
          );
        })}
      </div>

      {/* Footer */}
      {data.callout && <CalloutBox>{data.callout}</CalloutBox>}
    </div>
  );
}
