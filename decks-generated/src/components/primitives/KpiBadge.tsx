import type { CSSProperties } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { useStyle } from '../hooks/useStyle.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';
import { SPACING } from '../../tokens/spacing.js';

export interface KpiBadgeProps {
  /** Metric value (e.g., "4.2M", "$120k"). */
  readonly value: string | number;
  /** Short label (e.g., "ARR", "Users"). */
  readonly label: string;
  readonly trend?: 'up' | 'down' | 'flat';
}

const TREND_ARROW: Record<string, string> = {
  up: '↑',
  down: '↓',
  flat: '→',
};

/**
 * Compact KPI pill — used in cover slide KPI rows.
 *
 * Renders value + label side by side in a surface-colored badge.
 * Smaller and denser than StatValue, designed for horizontal arrays.
 */
export function KpiBadge({ value, label, trend }: KpiBadgeProps) {
  const theme = useTheme();
  const style = useStyle();

  const trendColor = trend === 'up'
    ? theme.success
    : trend === 'down'
      ? theme.danger
      : theme.textMuted;

  const badgeStyle: CSSProperties = {
    display: 'inline-flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: 2,
    background: theme.surface,
    padding: `${SPACING.xs}px ${SPACING.sm}px`,
    borderRadius: style.cardRadius,
    minWidth: 100,
  };

  const valueStyle: CSSProperties = {
    fontFamily: theme.fontDisplay,
    fontSize: TYPE_SCALE.SECTION.fontSize,
    fontWeight: TYPE_SCALE.SECTION.fontWeight,
    letterSpacing: TYPE_SCALE.SECTION.letterSpacing,
    lineHeight: 1,
    color: theme.accent,
  };

  const labelStyle: CSSProperties = {
    fontFamily: theme.fontBody,
    fontSize: TYPE_SCALE.EYEBROW.fontSize,
    fontWeight: TYPE_SCALE.EYEBROW.fontWeight,
    letterSpacing: TYPE_SCALE.EYEBROW.letterSpacing,
    lineHeight: 1,
    textTransform: 'uppercase',
    color: theme.textMuted,
  };

  return (
    <div style={badgeStyle}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 4 }}>
        <span style={valueStyle}>{value}</span>
        {trend && (
          <span style={{ fontSize: 14, color: trendColor }}>{TREND_ARROW[trend]}</span>
        )}
      </div>
      <span style={labelStyle}>{label}</span>
    </div>
  );
}
