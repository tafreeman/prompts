/**
 * TopicCard — generic content card with title, body, and optional icon.
 *
 * A flexible card component for rendering topic-level content blocks
 * across different deck layouts.
 *
 * @example
 *   <TopicCard
 *     title="Prompt Standardization"
 *     body="Established versioned prompt templates with embedded architecture context."
 *     icon="📋"
 *     color="#22D3EE"
 *   />
 */

import React from "react";
import PropTypes from "prop-types";

import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";

/**
 * @param {object} props
 * @param {string} props.title — card heading
 * @param {string} props.body — card body text
 * @param {string} [props.icon] — optional emoji or icon string
 * @param {string} [props.color] — accent colour override
 * @param {Function} [props.onClick] — optional click handler
 */
function TopicCard({ title, body, icon, color, onClick }) {
  const T = useTheme();
  const C = useChrome();

  const accent = color || T.text;
  const isClickable = typeof onClick === "function";

  return (
    <div
      role={isClickable ? "button" : undefined}
      tabIndex={isClickable ? 0 : undefined}
      onClick={onClick}
      onKeyDown={
        isClickable
          ? (e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onClick(e);
              }
            }
          : undefined
      }
      style={{
        background: T.bgCard,
        borderRadius: C.cardRadius,
        padding: "24px 28px",
        borderLeft: `${C.accentBarHeight + 1}px solid ${accent}`,
        cursor: isClickable ? "pointer" : "default",
        transition: "transform 0.3s ease, box-shadow 0.3s ease",
      }}
    >
      {icon && (
        <div
          style={{
            fontSize: 28,
            marginBottom: 12,
            lineHeight: 1,
          }}
        >
          {icon}
        </div>
      )}

      <h3
        style={{
          fontFamily: T.fontDisplay,
          fontSize: 17,
          fontWeight: C.headingWeight,
          color: accent,
          margin: "0 0 10px",
        }}
      >
        {title}
      </h3>

      {body && (
        <p
          style={{
            fontSize: 13.5,
            color: T.textMuted,
            lineHeight: 1.6,
            margin: 0,
          }}
        >
          {body}
        </p>
      )}
    </div>
  );
}

TopicCard.propTypes = {
  title: PropTypes.string.isRequired,
  body: PropTypes.string.isRequired,
  icon: PropTypes.string,
  color: PropTypes.string,
  onClick: PropTypes.func,
};

export default TopicCard;
