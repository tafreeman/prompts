import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { CoverSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Body } from '../../components/primitives/Body.js';
import { Eyebrow } from '../../components/primitives/Eyebrow.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { KpiBadge } from '../../components/primitives/KpiBadge.js';
import { SPACING } from '../../tokens/spacing.js';

type CoverData = z.infer<typeof CoverSlide>;

/**
 * Cover layout — the opening slide of every deck.
 *
 * Design guide: first impression, centered composition, gradient backdrop.
 * Optional KPI row at bottom provides immediate "so what" evidence.
 */
export function CoverLayout({ slide }: LayoutProps) {
  const data = slide as CoverData;
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

  // Subtle gradient overlay for visual depth
  const gradientStyle: CSSProperties = {
    position: 'absolute',
    inset: 0,
    background: `radial-gradient(ellipse at 50% 30%, ${theme.accentGlow} 0%, transparent 60%)`,
    pointerEvents: 'none',
  };

  const kpiRowStyle: CSSProperties = {
    display: 'flex',
    gap: SPACING.md,
    justifyContent: 'center',
    marginTop: SPACING.xl,
  };

  return (
    <div style={containerStyle}>
      <div style={gradientStyle} aria-hidden="true" />

      <div style={{ position: 'relative', zIndex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: SPACING.sm }}>
        {data.eyebrow && <Eyebrow>{data.eyebrow}</Eyebrow>}

        <Heading level="HERO" align="center">{data.title}</Heading>

        <AccentBar width="120px" />

        {data.subtitle && <Body muted align="center">{data.subtitle}</Body>}
        {data.tagline && (
          <Body muted size="BODY" align="center">{data.tagline}</Body>
        )}
      </div>

      {data.kpis && data.kpis.length > 0 && (
        <div style={{ ...kpiRowStyle, position: 'relative', zIndex: 1 }}>
          {data.kpis.map((kpi, i) => (
            <KpiBadge
              key={i}
              value={kpi.value}
              label={kpi.label}
              trend={kpi.trend}
            />
          ))}
        </div>
      )}
    </div>
  );
}
