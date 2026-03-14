/**
 * ProcessNode — circular node used in sprint-cycle diagrams.
 *
 * Based on Figure8Cycle / CircularRingCycle node rendering
 * (monolith ~2230-2254, ~2353-2377). Renders an icon inside a circle
 * with an AI/Human badge and a label underneath.
 *
 * @param {object} props
 * @param {string} props.label - Text shown below the node.
 * @param {string} [props.icon] - Emoji or icon character displayed inside the circle.
 * @param {string} [props.color] - Override color for the node ring.
 * @param {'sm'|'md'|'lg'} [props.size='md'] - Controls the circle diameter.
 * @param {'pending'|'active'|'complete'} [props.status='pending'] - Visual status indicator.
 * @param {'ai'|'human'} [props.type='ai'] - Determines badge color and background tint.
 */

import React from "react";
import PropTypes from "prop-types";
import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";

const AI_BG = "#1E1B4B";
const AI_COLOR = "#7C3AED";
const HUMAN_COLOR = "#0891B2";

const SIZE_MAP = {
  sm: { circle: 22, font: 16, badge: 6, label: 9 },
  md: { circle: 26, font: 20, badge: 7, label: 10 },
  lg: { circle: 30, font: 22, badge: 8, label: 11 },
};

const STATUS_OPACITY = {
  pending: 0.5,
  active: 1,
  complete: 0.85,
};

export function ProcessNode({
  label,
  icon,
  color,
  size = "md",
  status = "pending",
  type = "ai",
}) {
  const T = useTheme();
  // useChrome imported for future chrome-aware sizing
  useChrome();

  const isAI = type === "ai";
  const nodeColor = color || (isAI ? AI_COLOR : HUMAN_COLOR);
  const dims = SIZE_MAP[size] || SIZE_MAP.md;
  const opacity = STATUS_OPACITY[status] || 1;

  return (
    <div
      style={{
        display: "inline-flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 6,
        opacity,
      }}
    >
      {/* Circle */}
      <div
        style={{
          position: "relative",
          width: dims.circle * 2,
          height: dims.circle * 2,
          borderRadius: "50%",
          background: isAI ? AI_BG : "#162240",
          border: `2px solid ${nodeColor}60`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: dims.font,
          boxShadow: `0 0 14px ${isAI ? "rgba(139,92,246,0.16)" : "rgba(8,145,178,0.12)"}`,
        }}
      >
        {icon}
        {/* Badge */}
        <div
          style={{
            position: "absolute",
            top: -5,
            right: -5,
            fontSize: dims.badge,
            fontWeight: 700,
            background: isAI ? AI_COLOR : HUMAN_COLOR,
            color: "#FFF",
            borderRadius: 5,
            padding: "1px 4px",
            fontFamily: "'Space Grotesk',sans-serif",
          }}
        >
          {isAI ? "AI" : "\uD83D\uDC64"}
        </div>
      </div>

      {/* Label */}
      <div
        style={{
          fontSize: dims.label,
          color: T.text || "#E2E8F0",
          textAlign: "center",
          fontWeight: 600,
          fontFamily: "'Space Grotesk',sans-serif",
          whiteSpace: "nowrap",
        }}
      >
        {label}
      </div>
    </div>
  );
}

ProcessNode.propTypes = {
  label: PropTypes.string.isRequired,
  icon: PropTypes.string,
  color: PropTypes.string,
  size: PropTypes.oneOf(["sm", "md", "lg"]),
  status: PropTypes.oneOf(["pending", "active", "complete"]),
  type: PropTypes.oneOf(["ai", "human"]),
};

export default ProcessNode;
