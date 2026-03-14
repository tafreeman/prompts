/**
 * IconButton — small interactive button displaying an icon.
 *
 * @param {object} props
 * @param {string} props.icon - Emoji or icon character to render.
 * @param {Function} props.onClick - Click handler.
 * @param {'sm'|'md'|'lg'} [props.size='md'] - Button size.
 * @param {'primary'|'ghost'} [props.variant='primary'] - Visual style.
 */

import React from "react";
import PropTypes from "prop-types";
import { useTheme } from "../hooks/useTheme.js";

const SIZE_MAP = {
  sm: { width: 28, height: 28, fontSize: 14 },
  md: { width: 36, height: 36, fontSize: 18 },
  lg: { width: 44, height: 44, fontSize: 22 },
};

export function IconButton({ icon, onClick, size = "md", variant = "primary" }) {
  const theme = useTheme();
  const sizeTokens = SIZE_MAP[size] || SIZE_MAP.md;

  const isPrimary = variant === "primary";

  const style = {
    ...sizeTokens,
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    border: isPrimary ? "none" : `1px solid ${theme.textDim}40`,
    borderRadius: "50%",
    background: isPrimary ? `${theme.accent}18` : "transparent",
    color: isPrimary ? theme.accent : theme.textMuted,
    cursor: "pointer",
    padding: 0,
    lineHeight: 1,
    transition: "background 0.2s ease, transform 0.15s ease",
  };

  return (
    <button
      type="button"
      onClick={onClick}
      style={style}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "scale(1.1)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "scale(1)";
      }}
    >
      {icon}
    </button>
  );
}

IconButton.propTypes = {
  icon: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  size: PropTypes.oneOf(["sm", "md", "lg"]),
  variant: PropTypes.oneOf(["primary", "ghost"]),
};
