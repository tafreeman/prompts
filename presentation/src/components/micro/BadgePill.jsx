/**
 * BadgePill — pill-shaped badge with optional icon and stat value.
 *
 * @param {object} props
 * @param {string} [props.icon] - Leading emoji or icon character.
 * @param {string} props.label - Badge label text.
 * @param {string} [props.value] - Stat or count displayed after the label.
 * @param {string} [props.color] - Override accent color (defaults to theme.accent).
 * @param {'primary'|'secondary'} [props.variant='primary'] - Visual weight.
 */

import React from "react";
import PropTypes from "prop-types";
import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";

export function BadgePill({ icon, label, value, color, variant = "primary" }) {
  const theme = useTheme();
  const chrome = useChrome();
  const accentColor = color || theme.accent;

  const isPrimary = variant === "primary";

  const style = {
    display: "inline-flex",
    alignItems: "center",
    gap: 6,
    padding: "4px 12px",
    borderRadius: chrome.pillRadius,
    fontFamily: theme.fontBody,
    fontSize: 13,
    fontWeight: 600,
    lineHeight: 1,
    background: isPrimary ? `${accentColor}18` : "transparent",
    color: isPrimary ? accentColor : theme.textMuted,
    border: isPrimary ? "none" : `1px solid ${theme.textDim}40`,
    whiteSpace: "nowrap",
  };

  return (
    <span style={style}>
      {icon && <span style={{ fontSize: 14 }}>{icon}</span>}
      <span>{label}</span>
      {value && (
        <span style={{ fontWeight: 800, color: isPrimary ? accentColor : theme.text }}>
          {value}
        </span>
      )}
    </span>
  );
}

BadgePill.propTypes = {
  icon: PropTypes.string,
  label: PropTypes.string.isRequired,
  value: PropTypes.string,
  color: PropTypes.string,
  variant: PropTypes.oneOf(["primary", "secondary"]),
};
