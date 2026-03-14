/**
 * QuoteBlock — styled quote with optional author attribution.
 *
 * @param {object} props
 * @param {string} props.text - The quote body.
 * @param {string} [props.author] - Attribution line below the quote.
 * @param {string} [props.color] - Override accent color (defaults to theme.accent).
 * @param {'left-accent'|'border'} [props.variant='left-accent'] - Visual style.
 */

import React from "react";
import PropTypes from "prop-types";
import { useTheme } from "../hooks/useTheme.js";

export function QuoteBlock({ text, author, color, variant = "left-accent" }) {
  const theme = useTheme();
  const accentColor = color || theme.accent;

  const baseStyle = {
    fontFamily: theme.fontBody,
    fontSize: 16,
    color: theme.text,
    lineHeight: 1.6,
    margin: 0,
    padding: "12px 0 12px 20px",
  };

  const variantStyle =
    variant === "left-accent"
      ? { borderLeft: `4px solid ${accentColor}` }
      : {
          border: `1px solid ${accentColor}40`,
          borderRadius: 8,
          padding: "16px 20px",
        };

  return (
    <blockquote style={{ ...baseStyle, ...variantStyle }}>
      <div style={{ fontStyle: "italic" }}>{text}</div>
      {author && (
        <div
          style={{
            marginTop: 8,
            fontSize: 13,
            fontWeight: 500,
            color: theme.textMuted,
            fontStyle: "normal",
          }}
        >
          {author}
        </div>
      )}
    </blockquote>
  );
}

QuoteBlock.propTypes = {
  text: PropTypes.string.isRequired,
  author: PropTypes.string,
  color: PropTypes.string,
  variant: PropTypes.oneOf(["left-accent", "border"]),
};
