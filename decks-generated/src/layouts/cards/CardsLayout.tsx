import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { CardsSlide } from '../../schemas/slide.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Eyebrow } from '../../components/primitives/Eyebrow.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { Card } from '../../components/primitives/Card.js';
import { StatValue } from '../../components/primitives/StatValue.js';
import { Body } from '../../components/primitives/Body.js';
import { CalloutBox } from '../../components/primitives/CalloutBox.js';
import { SourceLine } from '../../components/primitives/SourceLine.js';
import { SPACING } from '../../tokens/spacing.js';

type CardsData = z.infer<typeof CardsSlide>;

/**
 * Compute grid columns: 1-2 cards → 2 cols, 3-4 → 3 cols, 5-6 → 3 cols.
 */
function gridColumns(count: number): number {
  if (count <= 2) return 2;
  return 3;
}

/**
 * Cards layout — 2-6 content or stat cards in a responsive grid.
 *
 * Design guide: cards provide parallel evidence. Each card follows the
 * assertion-evidence model at micro scale: stat (evidence) → title
 * (assertion) → body (supporting detail).
 */
export function CardsLayout({ slide }: LayoutProps) {
  const data = slide as CardsData;
  const cols = gridColumns(data.cards.length);

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

      {/* Card grid */}
      <div style={gridStyle}>
        {data.cards.map((card, i) => (
          <Card key={i}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: SPACING.xs }}>
              {card.stat != null && (
                <StatValue
                  value={card.stat}
                  label={card.label ?? ''}
                />
              )}
              <Heading level="CARD">{card.title}</Heading>
              {card.body && <Body muted size="CAPTION">{card.body}</Body>}
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
