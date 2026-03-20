import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { WorkflowSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { useStyle } from '../../components/hooks/useStyle.js';
import { Heading } from '../../components/primitives/Heading.js';
import { SPACING } from '../../tokens/spacing.js';

type WorkflowData = z.infer<typeof WorkflowSlide>;

/**
 * Workflow layout -- three-column process table with horizontal dividers.
 *
 * Design guide (WeBrand "Deeper Dive" reference): dark background, no cell
 * backgrounds or vertical borders. Columns are Stage (narrow, monospace
 * uppercase) | What Happens (wide, body text) | Time/Meta (narrow,
 * right-aligned bold). Highlighted rows show full-opacity bold text;
 * non-highlighted rows use muted opacity. Header shows large title and
 * subtitle separated from the table by a thin horizontal rule.
 */
export function WorkflowLayout({ slide }: LayoutProps) {
  const data = slide as WorkflowData;
  const theme = useTheme();
  const style = useStyle();

  // Column proportions: 25% | 55% | 20%
  const COL_STAGE = '25%';
  const COL_DESC  = '55%';
  const COL_META  = '20%';

  const MUTED_OPACITY = 0.55;

  const defaultLabels: [string, string, string] = ['Stage', 'What Happens', 'Time'];
  const [label0, label1, label2] = data.columnLabels ?? defaultLabels;

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    gap: 0,
  };

  const headerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: SPACING.xs,
    paddingBottom: SPACING.md,
  };

  const subtitleStyle: CSSProperties = {
    fontFamily: theme.fontBody,
    fontSize: 15,
    color: theme.textMuted,
    lineHeight: 1.4,
    maxWidth: '70%',
  };

  const ruleStyle: CSSProperties = {
    width: '100%',
    height: 1,
    background: theme.text,
    opacity: 0.15,
    flexShrink: 0,
  };

  const tableAreaStyle: CSSProperties = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  };

  // Column header row
  const colHeaderRowStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    paddingTop: SPACING.sm,
    paddingBottom: SPACING.xs,
    borderBottom: `1px solid ${theme.text}26`,  // 0.15 opacity approx
  };

  const colHeaderBaseStyle: CSSProperties = {
    fontFamily: theme.fontBody,
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: '0.08em',
    textTransform: 'uppercase',
    color: theme.textDim,
  };

  // Stage rows fill remaining height evenly
  const stageCount = data.stages.length;

  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={headerStyle}>
        <Heading level="TITLE">{data.title}</Heading>
        {data.subtitle && (
          <p style={subtitleStyle}>{data.subtitle}</p>
        )}
      </div>

      {/* Separator rule */}
      <div style={ruleStyle} />

      {/* Table area */}
      <div style={tableAreaStyle}>
        {/* Column header row */}
        <div style={colHeaderRowStyle}>
          <div style={{ ...colHeaderBaseStyle, width: COL_STAGE }}>{label0}</div>
          <div style={{ ...colHeaderBaseStyle, width: COL_DESC }}>{label1}</div>
          <div style={{ ...colHeaderBaseStyle, width: COL_META, textAlign: 'right' }}>{label2}</div>
        </div>

        {/* Stage rows */}
        <div style={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
          {data.stages.map((stage, i) => {
            const isHighlight = stage.highlight === true;
            const opacity = isHighlight ? 1 : MUTED_OPACITY;
            const fontWeight = isHighlight ? 700 : 400;

            const rowStyle: CSSProperties = {
              display: 'flex',
              alignItems: 'center',
              flex: 1,
              borderBottom: i < stageCount - 1
                ? `1px solid ${theme.text}1A`   // ~0.10 opacity
                : 'none',
              minHeight: 0,
            };

            const stageLabelStyle: CSSProperties = {
              width: COL_STAGE,
              fontFamily: theme.fontDisplay,
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              color: theme.text,
              opacity,
              lineHeight: 1.35,
              paddingRight: SPACING.sm,
            };

            const descStyle: CSSProperties = {
              width: COL_DESC,
              fontFamily: theme.fontBody,
              fontSize: 14,
              fontWeight,
              color: theme.text,
              opacity,
              lineHeight: 1.45,
              paddingRight: SPACING.sm,
            };

            const metaStyle: CSSProperties = {
              width: COL_META,
              fontFamily: theme.fontDisplay,
              fontSize: 16,
              fontWeight: 700,
              color: theme.text,
              opacity,
              textAlign: 'right',
              lineHeight: 1.2,
            };

            return (
              <div key={i} style={rowStyle}>
                <div style={stageLabelStyle}>{stage.label}</div>
                <div style={descStyle}>{stage.description ?? ''}</div>
                <div style={metaStyle}>{stage.meta ?? ''}</div>
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
}
