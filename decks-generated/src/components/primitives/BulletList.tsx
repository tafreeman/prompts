import type { CSSProperties } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';
import { SPACING } from '../../tokens/spacing.js';

export interface BulletListProps {
  readonly items: readonly string[];
  readonly marker?: 'disc' | 'check' | 'arrow' | 'number';
}

const MARKER_SYMBOL: Record<string, string> = {
  disc: '•',
  check: '✓',
  arrow: '→',
};

/**
 * Styled bullet list — renders up to 7 items at BODY scale.
 *
 * Custom markers replace default list-style for consistent rendering
 * across web preview and PPTX export.
 */
export function BulletList({ items, marker = 'disc' }: BulletListProps) {
  const theme = useTheme();
  const scale = TYPE_SCALE.BODY;

  const listStyle: CSSProperties = {
    listStyle: 'none',
    padding: 0,
    margin: 0,
    display: 'flex',
    flexDirection: 'column',
    gap: SPACING.xs,
  };

  const itemStyle: CSSProperties = {
    fontFamily: theme.fontBody,
    fontSize: scale.fontSize,
    fontWeight: scale.fontWeight,
    lineHeight: scale.lineHeight,
    color: theme.text,
    display: 'flex',
    gap: SPACING.sm,
    alignItems: 'baseline',
  };

  const markerStyle: CSSProperties = {
    color: theme.accent,
    fontWeight: 700,
    flexShrink: 0,
    minWidth: 16,
  };

  return (
    <ul style={listStyle}>
      {items.map((item, i) => (
        <li key={i} style={itemStyle}>
          <span style={markerStyle}>
            {marker === 'number' ? `${i + 1}.` : MARKER_SYMBOL[marker]}
          </span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  );
}
