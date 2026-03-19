import type { CSSProperties, ReactNode } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { useStyle } from '../hooks/useStyle.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';

export interface EyebrowProps {
  readonly children: ReactNode;
  /** Override color (default: theme.accent). */
  readonly color?: string;
}

/**
 * Uppercase label with wide tracking — used for category tags,
 * section markers, and slide eyebrows.
 *
 * Always renders at TYPE_SCALE.EYEBROW (11px, uppercase).
 * Tracking width comes from the active style mode.
 */
export function Eyebrow({ children, color }: EyebrowProps) {
  const theme = useTheme();
  const style = useStyle();
  const scale = TYPE_SCALE.EYEBROW;

  const eyebrowStyle: CSSProperties = {
    fontFamily: theme.fontBody,
    fontSize: scale.fontSize,
    fontWeight: scale.fontWeight,
    letterSpacing: style.labelTracking,
    lineHeight: scale.lineHeight,
    textTransform: 'uppercase',
    color: color ?? theme.accent,
    margin: 0,
  };

  return <span style={eyebrowStyle}>{children}</span>;
}
