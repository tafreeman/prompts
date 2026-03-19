import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { ClosingSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Body } from '../../components/primitives/Body.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { Card } from '../../components/primitives/Card.js';
import { BulletList } from '../../components/primitives/BulletList.js';
import { SPACING } from '../../tokens/spacing.js';

type ClosingData = z.infer<typeof ClosingSlide>;

/**
 * Closing layout -- the final CTA slide.
 *
 * Design guide: centered like cover with gradient overlay. Includes
 * optional "Next Steps" bullet list in a Card panel and muted contact
 * info at the bottom.
 */
export function ClosingLayout({ slide }: LayoutProps) {
  const data = slide as ClosingData;
  const theme = useTheme();

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
    textAlign: 'center',
    position: 'relative',
    gap: SPACING.md,
  };

  // Gradient overlay matching CoverLayout
  const gradientStyle: CSSProperties = {
    position: 'absolute',
    inset: 0,
    background: `radial-gradient(ellipse at 50% 30%, ${theme.accentGlow} 0%, transparent 60%)`,
    pointerEvents: 'none',
  };

  const contentStyle: CSSProperties = {
    position: 'relative',
    zIndex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: SPACING.sm,
    width: '100%',
    maxWidth: 720,
  };

  return (
    <div style={containerStyle}>
      <div style={gradientStyle} aria-hidden="true" />

      <div style={contentStyle}>
        <Heading level="HERO" align="center">{data.title}</Heading>

        <AccentBar width="120px" />

        {data.subtitle && (
          <Body align="center">{data.subtitle}</Body>
        )}

        {data.nextSteps && data.nextSteps.length > 0 && (
          <div style={{ width: '100%', marginTop: SPACING.md }}>
            <div style={{ marginBottom: SPACING.sm }}>
              <Heading level="CARD" align="center">Next Steps</Heading>
            </div>
            <Card>
              <BulletList items={data.nextSteps} marker="arrow" />
            </Card>
          </div>
        )}

        {data.contact && (
          <div style={{ marginTop: SPACING.sm }}>
            <Body muted align="center">{data.contact}</Body>
          </div>
        )}
      </div>
    </div>
  );
}
