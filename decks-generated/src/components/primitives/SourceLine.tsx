import type { CSSProperties } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';

export interface SourceLineProps {
  /** The data attribution text (displayed after "Source: " prefix). */
  readonly source: string;
}

/**
 * Right-aligned data attribution caption.
 *
 * Design guide: every data slide should cite its source.
 * The Zod schema recommends (but doesn't require) the `source` field.
 */
export function SourceLine({ source }: SourceLineProps) {
  const theme = useTheme();
  const scale = TYPE_SCALE.CAPTION;

  const lineStyle: CSSProperties = {
    fontFamily: theme.fontBody,
    fontSize: scale.fontSize,
    fontWeight: scale.fontWeight,
    letterSpacing: scale.letterSpacing,
    lineHeight: scale.lineHeight,
    color: theme.textDim,
    textAlign: 'right',
    fontStyle: 'italic',
    margin: 0,
  };

  return <p style={lineStyle}>Source: {source}</p>;
}
