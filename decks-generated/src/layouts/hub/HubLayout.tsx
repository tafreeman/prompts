import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { HubSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { useStyle } from '../../components/hooks/useStyle.js';
import { SPACING } from '../../tokens/spacing.js';

type HubData = z.infer<typeof HubSlide>;

// Slide logical size
const SLIDE_W = 1920;
const SLIDE_H = 1080;

// Diagram box inset from slide edges
const BOX_INSET_X = 120;
const BOX_INSET_Y = 80;
const BOX_W = SLIDE_W - BOX_INSET_X * 2;
const BOX_H = SLIDE_H - BOX_INSET_Y * 2;

// Center circle
const CX = SLIDE_W / 2;
const CY = SLIDE_H / 2;
const CR = 140;  // radius px

// Corner points of the outer box
const CORNERS = {
  topLeft:     { x: BOX_INSET_X,          y: BOX_INSET_Y },
  topRight:    { x: BOX_INSET_X + BOX_W,  y: BOX_INSET_Y },
  bottomLeft:  { x: BOX_INSET_X,          y: BOX_INSET_Y + BOX_H },
  bottomRight: { x: BOX_INSET_X + BOX_W,  y: BOX_INSET_Y + BOX_H },
};

/**
 * Compute the point on the circle's edge that faces a given corner,
 * so the diagonal line touches the circle boundary rather than center.
 */
function circleEdgePoint(corner: { x: number; y: number }): { x: number; y: number } {
  const dx = corner.x - CX;
  const dy = corner.y - CY;
  const dist = Math.sqrt(dx * dx + dy * dy);
  return {
    x: CX + (dx / dist) * CR,
    y: CY + (dy / dist) * CR,
  };
}

/**
 * Hub layout — full-bleed SVG hub-and-spoke diagram.
 *
 * Design guide:
 * - Outer border rect marks the diagram boundary
 * - Center circle contains the central concept label
 * - Diagonal lines connect each corner to the circle edge
 * - Spoke labels sit at top/bottom/left/right with eyebrow text above
 * - Slide title and body appear outside the box, bottom-right
 */
export function HubLayout({ slide }: LayoutProps) {
  const data = slide as HubData;
  const theme = useTheme();
  const style = useStyle();

  const outerStyle: CSSProperties = {
    position: 'relative',
    width: '100%',
    height: '100%',
    backgroundColor: theme.bg,
    overflow: 'hidden',
  };

  // SVG fills the slide
  const svgStyle: CSSProperties = {
    position: 'absolute',
    inset: 0,
    width: '100%',
    height: '100%',
  };

  // Spoke data keyed by position
  const spokeByPos = Object.fromEntries(
    data.spokes.map((s) => [s.position, s]),
  ) as Partial<Record<'top' | 'bottom' | 'left' | 'right', typeof data.spokes[number]>>;

  // Diagonal line endpoints
  const diagonals: Array<{ from: { x: number; y: number }; to: { x: number; y: number } }> = [
    { from: CORNERS.topLeft,     to: circleEdgePoint(CORNERS.topLeft) },
    { from: CORNERS.topRight,    to: circleEdgePoint(CORNERS.topRight) },
    { from: CORNERS.bottomLeft,  to: circleEdgePoint(CORNERS.bottomLeft) },
    { from: CORNERS.bottomRight, to: circleEdgePoint(CORNERS.bottomRight) },
  ];

  return (
    <div style={outerStyle}>
      {/* SVG diagram layer */}
      <svg
        viewBox={`0 0 ${SLIDE_W} ${SLIDE_H}`}
        preserveAspectRatio="xMidYMid meet"
        style={svgStyle}
        aria-hidden="true"
      >
        {/* Outer border rect */}
        <rect
          x={BOX_INSET_X}
          y={BOX_INSET_Y}
          width={BOX_W}
          height={BOX_H}
          fill="none"
          stroke={theme.text}
          strokeOpacity={0.4}
          strokeWidth={1}
        />

        {/* Diagonal corner lines */}
        {diagonals.map((d, i) => (
          <line
            key={i}
            x1={d.from.x}
            y1={d.from.y}
            x2={d.to.x}
            y2={d.to.y}
            stroke={theme.text}
            strokeOpacity={0.35}
            strokeWidth={1}
          />
        ))}

        {/* Center circle */}
        <circle
          cx={CX}
          cy={CY}
          r={CR}
          fill="none"
          stroke={theme.text}
          strokeWidth={1}
        />

        {/* Center label */}
        <text
          x={CX}
          y={data.center.sublabel ? CY - 12 : CY + 6}
          textAnchor="middle"
          fontFamily={theme.fontDisplay}
          fontSize={22}
          fontWeight={700}
          fill={theme.text}
        >
          {data.center.label}
        </text>
        {data.center.sublabel && (
          <text
            x={CX}
            y={CY + 18}
            textAnchor="middle"
            fontFamily={theme.fontDisplay}
            fontSize={14}
            fontWeight={500}
            fill={theme.textMuted}
          >
            {data.center.sublabel}
          </text>
        )}
      </svg>

      {/* Spoke labels — positioned via absolute divs over the SVG */}
      {spokeByPos.top && (
        <SpokeLabel
          spoke={spokeByPos.top}
          position="top"
          theme={theme}
          style={style}
          slideW={SLIDE_W}
          slideH={SLIDE_H}
          boxInsetX={BOX_INSET_X}
          boxInsetY={BOX_INSET_Y}
          boxW={BOX_W}
          boxH={BOX_H}
        />
      )}
      {spokeByPos.bottom && (
        <SpokeLabel
          spoke={spokeByPos.bottom}
          position="bottom"
          theme={theme}
          style={style}
          slideW={SLIDE_W}
          slideH={SLIDE_H}
          boxInsetX={BOX_INSET_X}
          boxInsetY={BOX_INSET_Y}
          boxW={BOX_W}
          boxH={BOX_H}
        />
      )}
      {spokeByPos.left && (
        <SpokeLabel
          spoke={spokeByPos.left}
          position="left"
          theme={theme}
          style={style}
          slideW={SLIDE_W}
          slideH={SLIDE_H}
          boxInsetX={BOX_INSET_X}
          boxInsetY={BOX_INSET_Y}
          boxW={BOX_W}
          boxH={BOX_H}
        />
      )}
      {spokeByPos.right && (
        <SpokeLabel
          spoke={spokeByPos.right}
          position="right"
          theme={theme}
          style={style}
          slideW={SLIDE_W}
          slideH={SLIDE_H}
          boxInsetX={BOX_INSET_X}
          boxInsetY={BOX_INSET_Y}
          boxW={BOX_W}
          boxH={BOX_H}
        />
      )}

      {/* Title + body — bottom-right outside box */}
      <div style={{
        position: 'absolute',
        right: '3%',
        bottom: '2%',
        maxWidth: '30%',
        textAlign: 'right',
        display: 'flex',
        flexDirection: 'column',
        gap: SPACING.xs,
      }}>
        <div style={{
          fontFamily: theme.fontDisplay,
          fontSize: 14,
          fontWeight: 700,
          textTransform: style.headingTransform === 'uppercase' ? 'uppercase' : 'none',
          color: theme.text,
          letterSpacing: '0.08em',
        }}>
          {data.title}
        </div>
        {data.body && (
          <div style={{
            fontFamily: theme.fontBody,
            fontSize: 11,
            color: theme.textMuted,
            lineHeight: 1.5,
          }}>
            {data.body}
          </div>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// SpokeLabel component
// ---------------------------------------------------------------------------

interface SpokeLabelProps {
  spoke: HubData['spokes'][number];
  position: 'top' | 'bottom' | 'left' | 'right';
  theme: ReturnType<typeof useTheme>;
  style: ReturnType<typeof useStyle>;
  slideW: number;
  slideH: number;
  boxInsetX: number;
  boxInsetY: number;
  boxW: number;
  boxH: number;
}

function SpokeLabel({
  spoke,
  position,
  theme,
  style,
  slideW,
  slideH,
  boxInsetX,
  boxInsetY,
  boxW,
  boxH,
}: SpokeLabelProps) {
  // Convert SVG coordinates to percentage positions for CSS absolute positioning.
  // SVG coordinate system: 0,0 at top-left, SLIDE_W x SLIDE_H.
  // The slide container is 100% x 100%.

  let posStyle: CSSProperties = {};
  let textAlign: CSSProperties['textAlign'] = 'center';

  const labelBoxW = 220;
  const labelBoxH = 64;

  switch (position) {
    case 'top': {
      // Top center of the outer box
      const svgX = boxInsetX + boxW / 2;
      const svgY = boxInsetY;
      posStyle = {
        position: 'absolute',
        left: `${(svgX / slideW) * 100}%`,
        top: `${(svgY / slideH) * 100}%`,
        transform: `translate(-50%, -${labelBoxH + 16}px)`,
        width: labelBoxW,
        textAlign: 'center',
      };
      textAlign = 'center';
      break;
    }
    case 'bottom': {
      const svgX = boxInsetX + boxW / 2;
      const svgY = boxInsetY + boxH;
      posStyle = {
        position: 'absolute',
        left: `${(svgX / slideW) * 100}%`,
        top: `${(svgY / slideH) * 100}%`,
        transform: `translate(-50%, 16px)`,
        width: labelBoxW,
        textAlign: 'center',
      };
      textAlign = 'center';
      break;
    }
    case 'left': {
      const svgX = boxInsetX;
      const svgY = boxInsetY + boxH / 2;
      posStyle = {
        position: 'absolute',
        left: `${(svgX / slideW) * 100}%`,
        top: `${(svgY / slideH) * 100}%`,
        transform: `translate(calc(-100% - 20px), -50%)`,
        width: labelBoxW,
        textAlign: 'right',
      };
      textAlign = 'right';
      break;
    }
    case 'right': {
      const svgX = boxInsetX + boxW;
      const svgY = boxInsetY + boxH / 2;
      posStyle = {
        position: 'absolute',
        left: `${(svgX / slideW) * 100}%`,
        top: `${(svgY / slideH) * 100}%`,
        transform: `translate(20px, -50%)`,
        width: labelBoxW,
        textAlign: 'left',
      };
      textAlign = 'left';
      break;
    }
  }

  return (
    <div style={{ ...posStyle, display: 'flex', flexDirection: 'column', gap: 4 }}>
      {spoke.eyebrow && (
        <div style={{
          fontFamily: theme.fontBody,
          fontSize: 10,
          fontWeight: 600,
          textTransform: 'uppercase',
          letterSpacing: '0.1em',
          color: theme.accent,
          textAlign,
        }}>
          {spoke.eyebrow}
        </div>
      )}
      <div style={{
        fontFamily: theme.fontDisplay,
        fontSize: 13,
        fontWeight: 700,
        textTransform: style.headingTransform === 'uppercase' ? 'uppercase' : 'none',
        color: theme.text,
        letterSpacing: '0.04em',
        lineHeight: 1.2,
        textAlign,
      }}>
        {spoke.label}
      </div>
    </div>
  );
}
