/**
 * BeforeAfterPair — challenge/fix dual card.
 *
 * Based on the HurdlesScreen card pattern in the monolith
 * (genai_advocacy_hub_13.jsx ~lines 1211-1220).
 *
 * Renders a "before" (challenge) panel and an "after" (solution) panel
 * side-by-side (horizontal) or stacked (vertical).
 *
 * @example
 *   <BeforeAfterPair
 *     beforeTitle="Challenge"
 *     beforeBody="Developers used ad-hoc, inconsistent prompts."
 *     afterTitle="Solution"
 *     afterBody="Established versioned prompt templates."
 *     color="#F59E0B"
 *     layout="horizontal"
 *   />
 */

import React from "react";
import PropTypes from "prop-types";

import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";

/**
 * @param {object} props
 * @param {string} props.beforeTitle — heading for the "before" panel
 * @param {string} props.beforeBody — body text for the "before" panel
 * @param {string} props.afterTitle — heading for the "after" panel
 * @param {string} props.afterBody — body text for the "after" panel
 * @param {string} [props.color] — accent colour override
 * @param {'horizontal'|'vertical'} [props.layout='horizontal'] — panel arrangement
 */
function BeforeAfterPair({
  beforeTitle,
  beforeBody,
  afterTitle,
  afterBody,
  color,
  layout = "horizontal",
}) {
  const T = useTheme();
  const C = useChrome();

  const accent = color || T.text;
  const isHorizontal = layout === "horizontal";

  const panelStyle = {
    flex: 1,
    background: T.bgCard,
    borderRadius: C.innerRadius,
    padding: "24px 28px",
    position: "relative",
    overflow: "hidden",
  };

  const labelStyle = (labelColor) => ({
    fontSize: 10,
    textTransform: "uppercase",
    letterSpacing: 1.2,
    fontWeight: 700,
    color: labelColor,
    marginBottom: 4,
  });

  const bodyStyle = (textColor) => ({
    fontSize: 13,
    color: textColor,
    lineHeight: 1.5,
    margin: 0,
  });

  return (
    <div
      style={{
        display: "flex",
        flexDirection: isHorizontal ? "row" : "column",
        gap: 20,
      }}
    >
      {/* Before / Challenge panel */}
      <div
        style={{
          ...panelStyle,
          borderTop: `${C.accentBarHeight}px solid ${accent}`,
        }}
      >
        <div style={labelStyle(T.danger)}>{beforeTitle}</div>
        <p style={bodyStyle(T.textDim)}>{beforeBody}</p>
      </div>

      {/* After / Solution panel */}
      <div
        style={{
          ...panelStyle,
          borderTop: `${C.accentBarHeight}px solid ${accent}`,
        }}
      >
        <div style={labelStyle(T.success)}>{afterTitle}</div>
        <p style={bodyStyle(T.textMuted)}>{afterBody}</p>
      </div>
    </div>
  );
}

BeforeAfterPair.propTypes = {
  beforeTitle: PropTypes.string.isRequired,
  beforeBody: PropTypes.string.isRequired,
  afterTitle: PropTypes.string.isRequired,
  afterBody: PropTypes.string.isRequired,
  color: PropTypes.string,
  layout: PropTypes.oneOf(["horizontal", "vertical"]),
};

export default BeforeAfterPair;
