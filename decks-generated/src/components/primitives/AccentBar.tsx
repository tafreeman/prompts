import type { CSSProperties } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { useStyle } from '../hooks/useStyle.js';

export interface AccentBarProps {
  /** CSS width (default: '100%'). */
  readonly width?: string;
  /** Override color (default: theme.accent). */
  readonly color?: string;
}

/**
 * Decorative horizontal bar — used as a visual separator between
 * heading and content, or as a top accent on cards.
 *
 * Height comes from style.accentBarHeight (3px clean, 6px bold, 1px editorial).
 */
export function AccentBar({ width = '100%', color }: AccentBarProps) {
  const theme = useTheme();
  const style = useStyle();

  const barStyle: CSSProperties = {
    width,
    height: style.accentBarHeight,
    background: color ?? theme.accent,
    borderRadius: style.innerRadius,
    flexShrink: 0,
  };

  return <div style={barStyle} aria-hidden="true" />;
}
