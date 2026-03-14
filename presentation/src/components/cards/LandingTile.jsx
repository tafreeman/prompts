/**
 * LandingTile — interactive hover-state navigation tile.
 *
 * Extracted from the LandingTile function in the monolith
 * (genai_advocacy_hub_13.jsx lines 634-663).
 *
 * @example
 *   <LandingTile
 *     title="Hurdles We Overcame"
 *     subtitle="What changed from day one to delivery"
 *     icon="⬡"
 *     num="02"
 *     color="#F59E0B"
 *     colorLight="#FBBF24"
 *     colorGlow="rgba(245,158,11,0.3)"
 *     onClick={(pos) => navigate(pos)}
 *     hovered={true}
 *     onHover={(id) => setHovered(id)}
 *   />
 */

import React from "react";
import PropTypes from "prop-types";

import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";
import { usePresentationViewport } from "../hooks/usePresentationViewport.js";

/**
 * @param {object} props
 * @param {string} props.title — tile heading
 * @param {string} props.subtitle — descriptive text below heading
 * @param {string} props.icon — emoji or icon string
 * @param {string} props.num — eyebrow number (e.g. "02")
 * @param {string} props.color — primary accent colour
 * @param {string} props.colorLight — lighter variant of accent
 * @param {string} props.colorGlow — glow shadow colour (with alpha)
 * @param {Function} props.onClick — click handler, receives click position {x, y}
 * @param {boolean} props.hovered — whether this tile is currently hovered
 * @param {Function} props.onHover — called with true on mouseEnter, false on mouseLeave
 */
function LandingTile({
  title,
  subtitle,
  icon,
  num,
  color,
  colorLight,
  colorGlow,
  onClick,
  hovered,
  onHover,
}) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();

  const h = hovered;
  const glowShadow = C.useGlow
    ? `0 0 40px ${colorGlow}, 0 8px 32px rgba(0,0,0,0.4)`
    : "0 8px 32px rgba(0,0,0,0.5)";
  const restShadow = C.useSoftShadow
    ? "0 4px 20px rgba(0,0,0,0.3)"
    : "none";

  return (
    <div
      onClick={(e) => {
        const r = e.currentTarget.getBoundingClientRect();
        onClick({ x: r.left + r.width / 2, y: r.top + r.height / 2 });
      }}
      onMouseEnter={() => onHover(true)}
      onMouseLeave={() => onHover(false)}
      style={{
        flex: 1,
        position: "relative",
        cursor: "pointer",
        overflow: "hidden",
        borderRadius: C.tileRadius,
        padding: viewport.isPhone ? "24px 20px" : viewport.isCompact ? "28px 22px" : "32px 28px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        minHeight: viewport.tileMinHeight,
        background: T.bgDeep,
        border: `${C.cardBorderWidth}px solid ${
          h ? color + "60" : "rgba(255,255,255,0.06)"
        }`,
        boxShadow: h ? glowShadow : restShadow,
        transform: h
          ? "translateY(-8px) scale(1.02)"
          : "translateY(0) scale(1)",
        transition: "all 0.4s cubic-bezier(0.34,1.56,0.64,1)",
      }}
    >
      <div>
        {/* Eyebrow number */}
        <div
          style={{
            fontFamily: T.fontDisplay,
            fontSize: 12,
            fontWeight: 500,
            color,
            letterSpacing: C.labelTracking,
            textTransform: "uppercase",
            marginBottom: 6,
            opacity: 0.8,
          }}
        >
          {num}
        </div>

        {/* Icon */}
        <div
          style={{
            fontSize: viewport.isPhone ? 30 : 36,
            marginBottom: viewport.isPhone ? 8 : 10,
            lineHeight: 1,
            filter:
              h && C.useGlow
                ? `drop-shadow(0 0 12px ${colorGlow})`
                : "none",
            transition: "filter 0.4s",
          }}
        >
          {icon}
        </div>

        {/* Title */}
        <h2
          style={{
            fontFamily: T.fontDisplay,
            fontSize: viewport.isPhone ? 18 : viewport.isCompact ? 20 : 22,
            fontWeight: C.headingWeight,
            color: T.text,
            lineHeight: 1.15,
            margin: "0 0 6px",
            textTransform: C.headingTransform,
          }}
        >
          {title}
        </h2>

        {/* Subtitle */}
        <p style={{ fontSize: viewport.isPhone ? 12 : 13, color: T.textDim, lineHeight: 1.5, margin: 0 }}>
          {subtitle}
        </p>
      </div>

      {/* Explore CTA */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          marginTop: viewport.isPhone ? 16 : 20,
          color,
          fontSize: viewport.isPhone ? 11 : 12,
          fontWeight: 600,
          fontFamily: T.fontDisplay,
          transform: h ? "translateX(6px)" : "translateX(0)",
          transition: "transform 0.3s",
        }}
      >
        <span>Explore</span>
        <span style={{ fontSize: 16, lineHeight: 1 }}>&rarr;</span>
      </div>

      {/* Bottom accent bar */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: C.accentBarHeight,
          background: color,
          opacity: h ? 1 : 0.4,
          transition: "opacity 0.3s",
        }}
      />
    </div>
  );
}

LandingTile.propTypes = {
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
  num: PropTypes.string.isRequired,
  color: PropTypes.string.isRequired,
  colorLight: PropTypes.string.isRequired,
  colorGlow: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  hovered: PropTypes.bool.isRequired,
  onHover: PropTypes.func.isRequired,
};

export default LandingTile;
