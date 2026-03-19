import type { CSSProperties, ReactNode } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';

export interface BodyProps {
  readonly children: ReactNode;
  /** Use textMuted color for secondary content. */
  readonly muted?: boolean;
  /** Scale level — BODY (16px) or CAPTION (13px). */
  readonly size?: 'BODY' | 'CAPTION';
  readonly align?: 'left' | 'center' | 'right';
}

/**
 * Body text component — the workhorse paragraph/text element.
 *
 * Uses theme.fontBody for typeface. Set `muted` for secondary text
 * (subtitles, descriptions). Set `size="CAPTION"` for footnotes.
 */
export function Body({ children, muted = false, size = 'BODY', align = 'left' }: BodyProps) {
  const theme = useTheme();
  const scale = TYPE_SCALE[size];

  const bodyStyle: CSSProperties = {
    fontFamily: theme.fontBody,
    fontSize: scale.fontSize,
    fontWeight: scale.fontWeight,
    letterSpacing: scale.letterSpacing,
    lineHeight: scale.lineHeight,
    color: muted ? theme.textMuted : theme.text,
    textAlign: align,
    margin: 0,
  };

  return <p style={bodyStyle}>{children}</p>;
}
