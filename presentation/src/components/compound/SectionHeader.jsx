/**
 * SectionHeader — module heading with icon, title, subtitle, and accent bar.
 *
 * Extracted from the monolith (genai_advocacy_hub_13.jsx lines 1622-1638).
 */

import React from "react";
import PropTypes from "prop-types";

import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";
import { usePresentationViewport } from "../hooks/usePresentationViewport.js";

function SectionHeader({ topic, entered }) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();

  return (
    <div
      style={{
        marginBottom: viewport.isPhone ? 22 : 28,
        opacity: entered ? 1 : 0,
        transform: entered ? "none" : "translateY(20px)",
        transition: "all 0.7s cubic-bezier(0.22,1,0.36,1)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: viewport.isPhone ? "flex-start" : "center",
          gap: viewport.isPhone ? 10 : 14,
          marginBottom: 6,
        }}
      >
        <div
          style={{
            fontSize: viewport.isPhone ? 26 : 32,
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
              fontSize: viewport.sectionTitleSize,
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
            fontSize: viewport.isPhone ? 13 : 14,
            color: topic.colorLight || T.textMuted,
            fontStyle: "italic",
            margin: "0 0 4px",
            paddingLeft: viewport.isPhone ? 0 : 46,
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
