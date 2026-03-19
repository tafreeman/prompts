import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { CompareSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Body } from '../../components/primitives/Body.js';
import { Eyebrow } from '../../components/primitives/Eyebrow.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { Card } from '../../components/primitives/Card.js';
import { BulletList } from '../../components/primitives/BulletList.js';
import { CalloutBox } from '../../components/primitives/CalloutBox.js';
import { SourceLine } from '../../components/primitives/SourceLine.js';
import { SPACING } from '../../tokens/spacing.js';

type CompareData = z.infer<typeof CompareSlide>;

/**
 * Compare layout -- two side-by-side columns for juxtaposition.
 *
 * Design guide: left column gets the accent bar, right column gets the
 * muted bar. Each column renders its own title, body, and bullet list
 * inside a Card panel.
 */
export function CompareLayout({ slide }: LayoutProps) {
  const data = slide as CompareData;
  const theme = useTheme();

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    gap: SPACING.md,
  };

  const columnsStyle: CSSProperties = {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: SPACING.md,
    flex: 1,
    alignContent: 'center',
  };

  const columnContentStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: SPACING.sm,
  };

  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: SPACING.xs }}>
        {data.eyebrow && <Eyebrow>{data.eyebrow}</Eyebrow>}
        <Heading level="TITLE">{data.title}</Heading>
        <AccentBar width="80px" />
      </div>

      {/* Two-column comparison */}
      <div style={columnsStyle}>
        {/* Left column */}
        <Card accentColor={theme.accent} showAccentBar>
          <div style={columnContentStyle}>
            {data.left.title && <Heading level="CARD">{data.left.title}</Heading>}
            {data.left.body && <Body>{data.left.body}</Body>}
            {data.left.bullets && data.left.bullets.length > 0 && (
              <BulletList items={data.left.bullets} />
            )}
          </div>
        </Card>

        {/* Right column */}
        <Card accentColor={theme.textMuted} showAccentBar>
          <div style={columnContentStyle}>
            {data.right.title && <Heading level="CARD">{data.right.title}</Heading>}
            {data.right.body && <Body>{data.right.body}</Body>}
            {data.right.bullets && data.right.bullets.length > 0 && (
              <BulletList items={data.right.bullets} />
            )}
          </div>
        </Card>
      </div>

      {/* Footer */}
      {data.callout && <CalloutBox>{data.callout}</CalloutBox>}
      {data.source && <SourceLine source={data.source} />}
    </div>
  );
}
