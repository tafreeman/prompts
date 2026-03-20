import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { ChartSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { useStyle } from '../../components/hooks/useStyle.js';
import { Heading } from '../../components/primitives/Heading.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { SourceLine } from '../../components/primitives/SourceLine.js';
import { SPACING } from '../../tokens/spacing.js';

type ChartData = z.infer<typeof ChartSlide>;

/**
 * Compute the global value domain [min, max] across all bars.
 * Always includes 0 so the baseline is meaningful.
 */
function computeDomain(data: ChartData): { min: number; max: number } {
  const allValues = data.groups.flatMap((g) => g.bars.map((b) => b.value));
  return {
    min: Math.min(0, ...allValues),
    max: Math.max(0, ...allValues),
  };
}

/**
 * Chart layout — grouped horizontal bar chart with optional right-side
 * annotations panel.
 *
 * Design guide: bars extend left (negative) or right (positive) from a center
 * baseline. Highlighted rows get a pill-shaped surface band. Accent bars use
 * higher opacity to signal aggregate rows.
 */
export function ChartLayout({ slide }: LayoutProps) {
  const data = slide as ChartData;
  const theme = useTheme();
  const style = useStyle();
  const { min, max } = computeDomain(data);
  const range = max - min || 1;

  const hasAnnotations = (data.annotations?.length ?? 0) > 0;

  // Layout proportions
  const GROUP_LABEL_W = 96;   // px — left bracket column
  const ANNO_W = hasAnnotations ? 200 : 0;  // px — right annotations panel
  const BAR_SECTION_GAP = SPACING.md;
  const BAR_H = 22;           // px per bar row
  const BAR_GAP = 4;          // px between bars in a group
  const GROUP_GAP = SPACING.md; // px between groups

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    gap: SPACING.md,
  };

  const chartBodyStyle: CSSProperties = {
    display: 'flex',
    flex: 1,
    gap: SPACING.sm,
    overflow: 'hidden',
  };

  // Left: groups column
  const groupsColumnStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: GROUP_GAP,
    flex: 1,
    minWidth: 0,
  };

  // Right: annotations panel
  const annotationsPanelStyle: CSSProperties = {
    width: ANNO_W,
    flexShrink: 0,
    borderLeft: `1px solid ${theme.textMuted}`,
    paddingLeft: SPACING.sm,
    display: 'flex',
    flexDirection: 'column',
    gap: SPACING.sm,
  };

  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: SPACING.xs }}>
        <Heading level="TITLE">{data.title}</Heading>
        <AccentBar width="80px" />
      </div>

      {/* Chart body */}
      <div style={chartBodyStyle}>
        {/* Groups */}
        <div style={groupsColumnStyle}>
          {data.groups.map((group) => (
            <GroupRow
              key={group.id}
              group={group}
              min={min}
              range={range}
              unit={data.unit ?? ''}
              theme={theme}
              groupLabelW={GROUP_LABEL_W}
              barH={BAR_H}
              barGap={BAR_GAP}
              barSectionGap={BAR_SECTION_GAP}
              style={style}
            />
          ))}
        </div>

        {/* Annotations */}
        {hasAnnotations && (
          <div style={annotationsPanelStyle}>
            {(data.annotations ?? []).map((anno, ai) => (
              <div key={ai} style={{ display: 'flex', flexDirection: 'column', gap: SPACING.xs }}>
                {/* Annotation group label */}
                <div style={{
                  fontFamily: theme.fontDisplay,
                  fontSize: 11,
                  fontWeight: 700,
                  color: theme.textMuted,
                  textTransform: 'uppercase',
                  letterSpacing: '0.06em',
                  whiteSpace: 'pre-line',
                }}>
                  {anno.label}
                </div>
                {/* Annotation items */}
                {(anno.items ?? []).map((item, ii) => (
                  <div key={ii} style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'baseline',
                    gap: SPACING.xs,
                  }}>
                    <span style={{
                      fontFamily: theme.fontBody,
                      fontSize: 11,
                      fontStyle: 'italic',
                      color: theme.textMuted,
                    }}>
                      {item.label}
                    </span>
                    <span style={{
                      fontFamily: theme.fontDisplay,
                      fontSize: 12,
                      fontWeight: 700,
                      color: theme.accent,
                    }}>
                      {item.value}
                    </span>
                  </div>
                ))}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Source */}
      {data.source && <SourceLine source={data.source} />}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

interface GroupRowProps {
  group: ChartData['groups'][number];
  min: number;
  range: number;
  unit: string;
  theme: ReturnType<typeof useTheme>;
  style: ReturnType<typeof useStyle>;
  groupLabelW: number;
  barH: number;
  barGap: number;
  barSectionGap: number;
}

function GroupRow({
  group,
  min,
  range,
  unit,
  theme,
  groupLabelW,
  barH,
  barGap,
}: GroupRowProps) {
  const groupRowStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'stretch',
    gap: SPACING.sm,
  };

  // Group bracket label — rotated text on left
  const labelStyle: CSSProperties = {
    width: groupLabelW,
    flexShrink: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    paddingRight: SPACING.xs,
  };

  const labelTextStyle: CSSProperties = {
    fontFamily: theme.fontDisplay,
    fontSize: 11,
    fontWeight: 700,
    color: theme.textMuted,
    textAlign: 'right',
    whiteSpace: 'pre-line',
    borderRight: `2px solid ${theme.accent}`,
    paddingRight: SPACING.xs,
  };

  const barsColStyle: CSSProperties = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    gap: barGap,
    justifyContent: 'center',
  };

  return (
    <div style={groupRowStyle}>
      {/* Group label */}
      <div style={labelStyle}>
        {group.label && (
          <div style={labelTextStyle}>{group.label}</div>
        )}
      </div>

      {/* Bars */}
      <div style={barsColStyle}>
        {group.bars.map((bar, bi) => (
          <BarRow
            key={bi}
            bar={bar}
            min={min}
            range={range}
            unit={unit}
            theme={theme}
            barH={barH}
          />
        ))}
      </div>
    </div>
  );
}

interface BarRowProps {
  bar: ChartData['groups'][number]['bars'][number];
  min: number;
  range: number;
  unit: string;
  theme: ReturnType<typeof useTheme>;
  barH: number;
}

function BarRow({ bar, min, range, unit, theme, barH }: BarRowProps) {
  const isNegative = bar.value < 0;

  // The full bar track goes from `min` to `max`.
  // Baseline (0) is at position `(-min / range)` from the left.
  const baselineRatio = -min / range;                        // 0..1
  const valueRatio = Math.abs(bar.value) / range;            // magnitude
  const barLeft = isNegative ? baselineRatio - valueRatio : baselineRatio;
  const barWidth = valueRatio;

  const rowStyle: CSSProperties = {
    position: 'relative',
    height: barH,
    display: 'flex',
    alignItems: 'center',
  };

  // Highlight pill band behind the whole row
  const highlightStyle: CSSProperties = {
    position: 'absolute',
    inset: 0,
    backgroundColor: theme.surface,
    borderRadius: barH / 2,
    zIndex: 0,
  };

  // Actual bar
  const barStyle: CSSProperties = {
    position: 'absolute',
    top: '15%',
    height: '70%',
    left: `${barLeft * 100}%`,
    width: `${barWidth * 100}%`,
    backgroundColor: theme.accent,
    opacity: bar.accent ? 0.9 : 0.6,
    borderRadius: 2,
    zIndex: 1,
  };

  // Baseline tick
  const baselineStyle: CSSProperties = {
    position: 'absolute',
    left: `${baselineRatio * 100}%`,
    top: 0,
    bottom: 0,
    width: 1,
    backgroundColor: theme.textDim,
    zIndex: 2,
  };

  // Bar label (left side, italic, muted)
  const labelStyle: CSSProperties = {
    position: 'absolute',
    right: `${(1 - baselineRatio + 0.02) * 100}%`,
    fontFamily: theme.fontBody,
    fontSize: 10,
    fontStyle: 'italic',
    color: theme.textMuted,
    whiteSpace: 'nowrap',
    zIndex: 3,
  };

  // Value label (right of bar)
  const valueLabelX = isNegative
    ? `${(baselineRatio - valueRatio - 0.02) * 100}%`
    : `${(baselineRatio + valueRatio + 0.01) * 100}%`;

  const valueLabelStyle: CSSProperties = {
    position: 'absolute',
    left: valueLabelX,
    fontFamily: theme.fontDisplay,
    fontSize: 10,
    fontWeight: 700,
    color: theme.text,
    whiteSpace: 'nowrap',
    zIndex: 3,
    transform: isNegative ? 'translateX(-100%)' : 'none',
  };

  return (
    <div style={rowStyle}>
      {bar.highlight && <div style={highlightStyle} />}
      <div style={baselineStyle} />
      <div style={barStyle} />
      <div style={labelStyle}>{bar.label}</div>
      <div style={valueLabelStyle}>
        {bar.value > 0 ? '+' : ''}{bar.value}{unit}
      </div>
    </div>
  );
}
