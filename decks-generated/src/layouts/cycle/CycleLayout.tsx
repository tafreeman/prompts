import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { CycleSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { useStyle } from '../../components/hooks/useStyle.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Eyebrow } from '../../components/primitives/Eyebrow.js';
import { Body } from '../../components/primitives/Body.js';
import { SourceLine } from '../../components/primitives/SourceLine.js';
import { SPACING } from '../../tokens/spacing.js';

type CycleData = z.infer<typeof CycleSlide>;

// Diagram dimensions (logical px at 1920×1080)
const CIRCLE_D = 400;     // circle diameter
const CIRCLE_R = CIRCLE_D / 2;
const STROKE_W = 10;      // circle outline stroke
const ARC_STROKE = 16;    // accent arc stroke

/**
 * Polar-to-Cartesian helper for SVG arc endpoints.
 */
function polarToCartesian(
  cx: number, cy: number, r: number, angleDeg: number,
): { x: number; y: number } {
  const rad = ((angleDeg - 90) * Math.PI) / 180;
  return {
    x: cx + r * Math.cos(rad),
    y: cy + r * Math.sin(rad),
  };
}

/**
 * Build an SVG arc path string (large-arc always false for arcs ≤ 180°,
 * large-arc true otherwise).
 */
function arcPath(
  cx: number, cy: number, r: number,
  startAngle: number, endAngle: number,
): string {
  const start = polarToCartesian(cx, cy, r, startAngle);
  const end   = polarToCartesian(cx, cy, r, endAngle);
  const sweep = ((endAngle - startAngle) + 360) % 360;
  const largeArc = sweep > 180 ? 1 : 0;
  return `M ${start.x} ${start.y} A ${r} ${r} 0 ${largeArc} 1 ${end.x} ${end.y}`;
}

/**
 * Cycle layout -- input node on left feeds a large decorative circle;
 * output items branch right from the circle.
 *
 * Design guide (Cogni "Data to Decisions" reference): full-slide dark layout,
 * eyebrow + large title span full width at top. Bottom 70% is an SVG diagram:
 * large circle (thin outline + accent arc ~200°), input block left of circle
 * with wavy connector, output items right of circle with tick connectors.
 */
export function CycleLayout({ slide }: LayoutProps) {
  const data = slide as CycleData;
  const theme = useTheme();
  const style = useStyle();

  // Slide is 1920×1080. Header occupies top ~30% (~324px).
  // Diagram canvas occupies full width, remaining height.
  const SLIDE_W = 1920;
  const SLIDE_H = 1080;
  const HEADER_H = 300;
  const DIAGRAM_H = SLIDE_H - HEADER_H;

  // Circle center: horizontally slightly right-of-center, vertically centered in diagram
  const CX = SLIDE_W * 0.52;
  const CY = DIAGRAM_H / 2;

  // Input area: left edge to circle
  const INPUT_X_CENTER = SLIDE_W * 0.18;

  // Output items: right of circle
  const OUTPUT_START_X = CX + CIRCLE_R + 60;
  const OUTPUT_W = SLIDE_W * 0.28;

  const outputCount = data.outputs.length;
  const outputSpacing = DIAGRAM_H / (outputCount + 1);

  // Accent arc angles: from ~150° to ~370° (most of the bottom-right arc)
  const ARC_START = 155;
  const ARC_END   = 370;

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    position: 'relative',
    overflow: 'hidden',
  };

  const headerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: SPACING.sm,
    paddingBottom: SPACING.md,
    flexShrink: 0,
  };

  const diagramContainerStyle: CSSProperties = {
    flex: 1,
    position: 'relative',
    overflow: 'hidden',
  };

  // Wavy connector path from input to circle left edge
  const inputEdgeX = INPUT_X_CENTER + 100;
  const circleLeftX = CX - CIRCLE_R - 10;
  const connY = CY;
  const mid = (inputEdgeX + circleLeftX) / 2;
  const wavePath = `M ${inputEdgeX} ${connY} C ${mid} ${connY - 30}, ${mid} ${connY + 30}, ${circleLeftX} ${connY}`;

  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={headerStyle}>
        {data.eyebrow && <Eyebrow>{data.eyebrow}</Eyebrow>}
        <Heading level="TITLE">{data.title}</Heading>
      </div>

      {/* Diagram */}
      <div style={diagramContainerStyle}>
        {/* SVG layer for circle and connectors */}
        <svg
          viewBox={`0 0 ${SLIDE_W} ${DIAGRAM_H}`}
          preserveAspectRatio="xMidYMid meet"
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            pointerEvents: 'none',
          }}
        >
          {/* Circle outline (thin, muted) */}
          <circle
            cx={CX}
            cy={CY}
            r={CIRCLE_R}
            fill="none"
            stroke={theme.text}
            strokeOpacity={0.18}
            strokeWidth={STROKE_W}
          />

          {/* Accent arc (thick, partial ring) */}
          <path
            d={arcPath(CX, CY, CIRCLE_R, ARC_START, ARC_END)}
            fill="none"
            stroke={theme.accent}
            strokeWidth={ARC_STROKE}
            strokeLinecap="round"
          />

          {/* Wavy connector: input → circle */}
          {data.input && (
            <path
              d={wavePath}
              fill="none"
              stroke={theme.text}
              strokeOpacity={0.35}
              strokeWidth={2}
              strokeDasharray="6 4"
            />
          )}

          {/* Tick connectors: circle right edge → each output item */}
          {data.outputs.map((_, i) => {
            const itemY = outputSpacing * (i + 1);
            const circleRightX = CX + CIRCLE_R + 10;
            const tickEndX = OUTPUT_START_X - 16;
            // Find the angle on circle right side closest to itemY
            // Simple approach: draw from circle rightmost tangent area
            const dy = itemY - CY;
            const angleRad = Math.atan2(dy, CIRCLE_R);
            const connStartX = CX + CIRCLE_R * Math.cos(angleRad);
            const connStartY = CY + CIRCLE_R * Math.sin(angleRad);
            return (
              <line
                key={i}
                x1={connStartX}
                y1={connStartY}
                x2={tickEndX}
                y2={itemY}
                stroke={theme.text}
                strokeOpacity={0.3}
                strokeWidth={1.5}
              />
            );
          })}
        </svg>

        {/* Input block (left of circle) */}
        {data.input && (
          <div
            style={{
              position: 'absolute',
              left: `${(INPUT_X_CENTER - 120) / SLIDE_W * 100}%`,
              top: `${(CY - 60) / DIAGRAM_H * 100}%`,
              width: `${220 / SLIDE_W * 100}%`,
              display: 'flex',
              flexDirection: 'column',
              gap: SPACING.xs,
            }}
          >
            <div
              style={{
                fontFamily: theme.fontDisplay,
                fontSize: 22,
                fontWeight: 700,
                color: theme.text,
                lineHeight: 1.2,
              }}
            >
              {data.input.label}
            </div>
            {data.input.body && (
              <div
                style={{
                  fontFamily: theme.fontBody,
                  fontSize: 13,
                  color: theme.textMuted,
                  lineHeight: 1.45,
                }}
              >
                {data.input.body}
              </div>
            )}
          </div>
        )}

        {/* Center label inside circle */}
        {data.centerLabel && (
          <div
            style={{
              position: 'absolute',
              left: `${(CX - CIRCLE_R * 0.6) / SLIDE_W * 100}%`,
              top: `${(CY - 20) / DIAGRAM_H * 100}%`,
              width: `${CIRCLE_R * 1.2 / SLIDE_W * 100}%`,
              textAlign: 'center',
              fontFamily: theme.fontDisplay,
              fontSize: 18,
              fontWeight: 700,
              color: theme.text,
              opacity: 0.7,
            }}
          >
            {data.centerLabel}
          </div>
        )}

        {/* Output items (right of circle) */}
        <div
          style={{
            position: 'absolute',
            left: `${OUTPUT_START_X / SLIDE_W * 100}%`,
            top: 0,
            width: `${OUTPUT_W / SLIDE_W * 100}%`,
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-around',
            paddingTop: `${outputSpacing * 0.5 / DIAGRAM_H * 100}%`,
            paddingBottom: `${outputSpacing * 0.5 / DIAGRAM_H * 100}%`,
          }}
        >
          {data.outputs.map((output, i) => (
            <div
              key={i}
              style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: SPACING.sm,
              }}
            >
              {/* Accent dot bullet */}
              <div
                style={{
                  width: 10,
                  height: 10,
                  borderRadius: '50%',
                  background: theme.accent,
                  flexShrink: 0,
                  marginTop: 5,
                }}
              />
              <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <div
                  style={{
                    fontFamily: theme.fontDisplay,
                    fontSize: 16,
                    fontWeight: 700,
                    color: theme.text,
                    lineHeight: 1.25,
                  }}
                >
                  {output.label}
                </div>
                {output.body && (
                  <div
                    style={{
                      fontFamily: theme.fontBody,
                      fontSize: 13,
                      color: theme.textMuted,
                      lineHeight: 1.45,
                    }}
                  >
                    {output.body}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Source footer */}
      {data.source && <SourceLine source={data.source} />}
    </div>
  );
}
