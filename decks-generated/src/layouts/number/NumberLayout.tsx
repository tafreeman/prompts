import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { NumberSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Eyebrow } from '../../components/primitives/Eyebrow.js';
import { Body } from '../../components/primitives/Body.js';
import { SourceLine } from '../../components/primitives/SourceLine.js';
import { SPACING } from '../../tokens/spacing.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';

type NumberData = z.infer<typeof NumberSlide>;

/**
 * Big number layout — a single oversized metric with context.
 *
 * Design guide: the "So What?" slide. The number IS the assertion;
 * the context explains why it matters. Centered composition
 * forces the audience to focus on one data point.
 */
export function NumberLayout({ slide }: LayoutProps) {
  const data = slide as NumberData;
  const theme = useTheme();

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    gap: SPACING.md,
  };

  const metricAreaStyle: CSSProperties = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    gap: SPACING.sm,
    textAlign: 'center',
  };

  // The stat renders at 1.5× STAT scale (72px) for maximum impact
  const bigStatStyle: CSSProperties = {
    fontFamily: theme.fontDisplay,
    fontSize: TYPE_SCALE.STAT.fontSize * 1.5,
    fontWeight: TYPE_SCALE.STAT.fontWeight,
    letterSpacing: TYPE_SCALE.STAT.letterSpacing,
    lineHeight: 1,
    color: theme.accent,
    margin: 0,
  };

  const labelStyle: CSSProperties = {
    fontFamily: theme.fontBody,
    fontSize: TYPE_SCALE.SECTION.fontSize,
    fontWeight: TYPE_SCALE.SECTION.fontWeight,
    lineHeight: TYPE_SCALE.SECTION.lineHeight,
    color: theme.textMuted,
    margin: 0,
  };

  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: SPACING.xs }}>
        {data.eyebrow && <Eyebrow>{data.eyebrow}</Eyebrow>}
        <Heading level="TITLE">{data.title}</Heading>
      </div>

      {/* Metric area — vertically centered */}
      <div style={metricAreaStyle}>
        <span style={bigStatStyle}>{data.stat}</span>
        <span style={labelStyle}>{data.statLabel}</span>
        {data.context && (
          <div style={{ maxWidth: 700, marginTop: SPACING.sm }}>
            <Body muted align="center">{data.context}</Body>
          </div>
        )}
      </div>

      {/* Footer */}
      {data.source && <SourceLine source={data.source} />}
    </div>
  );
}
