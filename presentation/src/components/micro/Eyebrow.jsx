/**
 * Eyebrow — uppercase label used above headings and sections.
 *
 * @param {object} props
 * @param {string} props.text - The label text to display.
 * @param {string} [props.color] - Override color (defaults to theme.textDim).
 * @param {'sm'|'md'} [props.size='md'] - Size variant controlling font-size and letter-spacing.
 */

import React from "react";
import PropTypes from "prop-types";
import { useTheme } from "../hooks/useTheme.js";
import { TYPE_SCALE } from "../../tokens/type-scale.js";

const SIZE_MAP = {
  sm: { fontSize: 9, letterSpacing: 1 },
  md: { fontSize: TYPE_SCALE.EYEBROW.fontSize, letterSpacing: TYPE_SCALE.EYEBROW.letterSpacing },
};

export function Eyebrow({ text, color, size = "md" }) {
  const theme = useTheme();
  const sizeTokens = SIZE_MAP[size] || SIZE_MAP.md;

  const style = {
    ...TYPE_SCALE.EYEBROW,
    ...sizeTokens,
    color: color || theme.textDim,
    margin: 0,
  };

  return <div style={style}>{text}</div>;
}

Eyebrow.propTypes = {
  text: PropTypes.string.isRequired,
  color: PropTypes.string,
  size: PropTypes.oneOf(["sm", "md"]),
};
