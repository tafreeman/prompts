import type { CSSProperties } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';
import { SPACING } from '../../tokens/spacing.js';

export interface StatValueProps {
  /** The metric value (e.g., "4.2M", 99.7, "$1.2B"). */
  readonly value: string | number;
  /** Label describing the metric (e.g., "Monthly Active Users"). */
  readonly label: string;
  /** Additional context line. */
  readonly detail?: string;
  /** Trend indicator arrow. */
  readonly trend?: 'up' | 'down' | 'flat';
}

const TREND_SYMBOL: Record<string, string> = {
  up: '↑',
  down: '↓',
  flat: '→',
};

/**
 * Oversized metric display — stat value + label + optional trend.
 *
 * The stat renders at TYPE_SCALE.STAT (48px) in the accent color.
 * Used in big-number slides, scorecard KPIs, and cover KPI rows.
 */
export function StatValue({ value, label, detail, trend }: StatValueProps) {
  const theme = useTheme();
  const statScale = TYPE_SCALE.STAT;
  const captionScale = TYPE_SCALE.CAPTION;

  const trendColor = trend === 'up'
    ? theme.success
    : trend === 'down'
      ? theme.danger
      : theme.textMuted;

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: SPACING.xs,
  };

  const valueStyle: CSSProperties = {
    fontFamily: theme.fontDisplay,
    fontSize: statScale.fontSize,
    fontWeight: statScale.fontWeight,
    letterSpacing: statScale.letterSpacing,
    lineHeight: statScale.lineHeight,
    color: theme.accent,
    margin: 0,
  };

  const labelStyle: CSSProperties = {
    fontFamily: theme.fontBody,
    fontSize: captionScale.fontSize,
    fontWeight: captionScale.fontWeight,
    letterSpacing: captionScale.letterSpacing,
    lineHeight: captionScale.lineHeight,
    color: theme.textMuted,
    margin: 0,
  };

  return (
    <div style={containerStyle}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: SPACING.xs }}>
        <span style={valueStyle}>{value}</span>
        {trend && (
          <span style={{ ...labelStyle, color: trendColor, fontSize: 18 }}>
            {TREND_SYMBOL[trend]}
          </span>
        )}
      </div>
      <span style={labelStyle}>{label}</span>
      {detail && (
        <span style={{ ...labelStyle, fontSize: 11, color: theme.textDim }}>
          {detail}
        </span>
      )}
    </div>
  );
}
