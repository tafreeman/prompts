import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { TableSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { useStyle } from '../../components/hooks/useStyle.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Eyebrow } from '../../components/primitives/Eyebrow.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { Card } from '../../components/primitives/Card.js';
import { SourceLine } from '../../components/primitives/SourceLine.js';
import { SPACING } from '../../tokens/spacing.js';

type TableData = z.infer<typeof TableSlide>;

/**
 * Detect whether a value is numeric (for right-alignment).
 */
function isNumeric(val: string | number): boolean {
  if (typeof val === 'number') return true;
  return !isNaN(Number(val)) && val.trim() !== '';
}

/**
 * Table layout -- structured data in a styled HTML table inside a Card panel.
 *
 * Design guide: tables show precise evidence. Header row uses accent color
 * for scannability. Alternating row backgrounds aid readability. An optional
 * highlight key draws attention to a specific row.
 */
export function TableLayout({ slide }: LayoutProps) {
  const data = slide as TableData;
  const theme = useTheme();
  const style = useStyle();

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    gap: SPACING.md,
  };

  const tableStyle: CSSProperties = {
    width: '100%',
    borderCollapse: 'collapse',
    fontFamily: theme.fontBody,
    fontSize: 14,
    color: theme.text,
  };

  const thStyle: CSSProperties = {
    background: theme.surface,
    color: theme.accent,
    textTransform: 'uppercase',
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: '0.05em',
    padding: `${SPACING.xs}px ${SPACING.sm}px`,
    textAlign: 'left',
    borderBottom: `2px solid ${theme.surfaceDeep}`,
  };

  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: SPACING.xs }}>
        {data.eyebrow && <Eyebrow>{data.eyebrow}</Eyebrow>}
        <Heading level="TITLE">{data.title}</Heading>
        <AccentBar width="80px" />
      </div>

      {/* Table card */}
      <Card showAccentBar={false}>
        <div style={{ overflowX: 'auto' }}>
          <table style={tableStyle}>
            <thead>
              <tr>
                {data.columns.map((col) => (
                  <th key={col} style={thStyle}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.rows.map((row, rowIdx) => {
                const isHighlighted = data.highlight != null &&
                  Object.values(row).some((v) => String(v) === data.highlight);

                const rowBg = isHighlighted
                  ? `${theme.accent}18`
                  : rowIdx % 2 === 0
                    ? 'transparent'
                    : `${theme.surface}4D`;

                const rowStyle: CSSProperties = {
                  background: rowBg,
                  borderLeft: isHighlighted
                    ? `3px solid ${theme.accent}`
                    : '3px solid transparent',
                };

                return (
                  <tr key={rowIdx} style={rowStyle}>
                    {data.columns.map((col) => {
                      const val = row[col] ?? '';
                      const numeric = isNumeric(val);

                      const tdStyle: CSSProperties = {
                        padding: `${SPACING.xs}px ${SPACING.sm}px`,
                        textAlign: numeric ? 'right' : 'left',
                        borderBottom: `1px solid ${theme.surfaceDeep}`,
                        fontVariantNumeric: numeric ? 'tabular-nums' : undefined,
                      };

                      return (
                        <td key={col} style={tdStyle}>{val}</td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Source footer */}
      {data.source && <SourceLine source={data.source} />}
    </div>
  );
}
