/**
 * SectionHeader — module heading with icon, title, subtitle, and accent bar.
 *
 * Extracted from the monolith (genai_advocacy_hub_13.jsx lines 1622-1638).
 */

import React from "react";
import PropTypes from "prop-types";

import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";

function SectionHeader({ topic, entered }) {
  const T = useTheme();
  const C = useChrome();

  return (
    <div
      style={{
        marginBottom: 28,
        opacity: entered ? 1 : 0,
        transform: entered ? "none" : "translateY(20px)",
        transition: "all 0.7s cubic-bezier(0.22,1,0.36,1)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 14,
          marginBottom: 6,
        }}
      >
        <div
          style={{
            fontSize: 32,
            filter: C.useGlow
              ? `drop-shadow(0 0 10px ${topic.colorGlow})`
              : "none",
          }}
        >
          {topic.icon}
        </div>
        <div>
          <div
            style={{
              fontSize: 10,
              fontFamily: T.fontDisplay,
              fontWeight: C.headingWeight,
              color: T.textDim,
              letterSpacing: 2,
              textTransform: "uppercase",
            }}
          >
            Module {topic.order || ""}
          </div>
          <h1
            style={{
              fontFamily: T.fontDisplay,
              fontSize: 32,
              fontWeight: C.headingWeight,
              color: T.text,
              margin: 0,
              textTransform: C.headingTransform,
            }}
          >
            {topic.title}
          </h1>
        </div>
      </div>
      {topic.subtitle && (
        <p
          style={{
            fontSize: 14,
            color: topic.colorLight || T.textMuted,
            fontStyle: "italic",
            margin: "0 0 4px",
            paddingLeft: 46,
          }}
        >
          {topic.subtitle}
        </p>
      )}
      <div
        style={{
          width: 60,
          height: C.accentBarHeight,
          background: topic.color,
          marginTop: 12,
          borderRadius: 2,
        }}
      />
    </div>
  );
}

SectionHeader.propTypes = {
  topic: PropTypes.shape({
    icon: PropTypes.string,
    order: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    title: PropTypes.string.isRequired,
    subtitle: PropTypes.string,
    color: PropTypes.string.isRequired,
    colorGlow: PropTypes.string,
    colorLight: PropTypes.string,
  }).isRequired,
  entered: PropTypes.bool.isRequired,
};

export default SectionHeader;
