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

import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";
import type { Theme } from "../../tokens/themes.ts";
import type { StyleMode } from "../../tokens/style-modes.ts";

interface BeforeAfterPairProps {
  /** heading for the "before" panel */
  beforeTitle: string;
  /** body text for the "before" panel */
  beforeBody: string;
  /** heading for the "after" panel */
  afterTitle: string;
  /** body text for the "after" panel */
  afterBody: string;
  /** accent colour override */
  color?: string;
  /** panel arrangement */
  layout?: "horizontal" | "vertical";
}

function BeforeAfterPair({
  beforeTitle,
  beforeBody,
  afterTitle,
  afterBody,
  color,
  layout = "horizontal",
}: BeforeAfterPairProps): React.ReactElement {
  const T: Theme = useTheme();
  const C: StyleMode = useChrome();

  const accent = color || T.text;
  const isHorizontal = layout === "horizontal";

  const panelStyle: React.CSSProperties = {
    flex: 1,
    background: T.bgCard,
    borderRadius: C.innerRadius,
    padding: "24px 28px",
    position: "relative",
    overflow: "hidden",
  };

  const labelStyle = (labelColor: string): React.CSSProperties => ({
    fontSize: 10,
    textTransform: "uppercase",
    letterSpacing: 1.2,
    fontWeight: 700,
    color: labelColor,
    marginBottom: 4,
  });

  const bodyStyle = (textColor: string): React.CSSProperties => ({
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

export default BeforeAfterPair;
