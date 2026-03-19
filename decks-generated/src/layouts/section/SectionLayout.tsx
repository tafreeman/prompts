import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { SectionSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Body } from '../../components/primitives/Body.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { SPACING } from '../../tokens/spacing.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';

type SectionData = z.infer<typeof SectionSlide>;

/**
 * Section divider — minimal layout with oversized number + title.
 *
 * Design guide: section breaks use the Pyramid Principle to
 * signal narrative structure. Left-aligned for Z-pattern entry.
 */
export function SectionLayout({ slide }: LayoutProps) {
  const data = slide as SectionData;
  const theme = useTheme();

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    height: '100%',
    gap: SPACING.md,
    paddingLeft: SPACING['2xl'],
  };

  const numberStyle: CSSProperties = {
    fontFamily: theme.fontDisplay,
    fontSize: TYPE_SCALE.STAT.fontSize,
    fontWeight: TYPE_SCALE.STAT.fontWeight,
    letterSpacing: TYPE_SCALE.STAT.letterSpacing,
    lineHeight: 1,
    color: theme.accent,
    margin: 0,
  };

  return (
    <div style={containerStyle}>
      {data.sectionNumber != null && (
        <span style={numberStyle}>
          {String(data.sectionNumber).padStart(2, '0')}
        </span>
      )}

      <AccentBar width="200px" />

      <Heading level="TITLE">{data.title}</Heading>

      {data.subtitle && <Body muted>{data.subtitle}</Body>}
    </div>
  );
}
