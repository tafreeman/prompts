import type { CSSProperties, ReactNode } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { useStyle } from '../hooks/useStyle.js';
import { SPACING } from '../../tokens/spacing.js';

export interface CardProps {
  readonly children: ReactNode;
  /** Accent bar color (default: theme.accent). */
  readonly accentColor?: string;
  /** Show the top accent bar (default: true). */
  readonly showAccentBar?: boolean;
  /** Make the card interactive with hover effect. */
  readonly hoverable?: boolean;
}

/**
 * Surface panel — the primary content container for slides.
 *
 * Reads shape (radius, border, shadow) from the active style mode:
 *   - clean:     rounded, soft shadow, subtle glow
 *   - bold:      sharp corners, thick border, no shadow
 *   - editorial: slight radius, soft shadow, thin border
 *
 * The accent bar at the top is the "signal stripe" from the design guide —
 * it draws the eye and creates a visual anchor for scanning.
 */
export function Card({
  children,
  accentColor,
  showAccentBar = true,
  hoverable = false,
}: CardProps) {
  const theme = useTheme();
  const style = useStyle();

  // --- Surface style: driven by style mode tokens ---
  const cardStyle: CSSProperties = {
    background: theme.surface,
    borderRadius: style.cardRadius,
    border: `${style.cardBorderWidth}px solid ${theme.surfaceDeep}`,
    padding: SPACING.lg,
    position: 'relative',
    overflow: 'hidden',
    transition: hoverable ? 'transform 0.2s, box-shadow 0.2s' : undefined,
    cursor: hoverable ? 'default' : undefined,
    ...(style.useSoftShadow && {
      boxShadow: '0 2px 8px rgba(0,0,0,0.15), 0 1px 3px rgba(0,0,0,0.1)',
    }),
    ...(style.useGlow && {
      boxShadow: `0 2px 8px rgba(0,0,0,0.15), 0 0 20px ${theme.accentGlow}`,
    }),
  };

  // --- Accent bar: the signal stripe ---
  const accentBarStyle: CSSProperties = {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: style.accentBarHeight,
    background: accentColor ?? theme.accent,
  };

  return (
    <div style={cardStyle}>
      {showAccentBar && <div style={accentBarStyle} aria-hidden="true" />}
      <div style={{ paddingTop: showAccentBar ? SPACING.xs : 0 }}>
        {children}
      </div>
    </div>
  );
}
