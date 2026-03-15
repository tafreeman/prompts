/**
 * Eyebrow — uppercase label used above headings and sections.
 *
 * @param props.text - The label text to display.
 * @param props.color - Override color (defaults to theme.textDim).
 * @param props.size - Size variant controlling font-size and letter-spacing.
 */

import React from "react";
import { useTheme } from "../hooks/useTheme.js";
import { TYPE_SCALE } from "../../tokens/type-scale.ts";
import type { Theme } from "../../tokens/themes.ts";

const SIZE_MAP = {
  sm: { fontSize: 9, letterSpacing: 1 },
  md: { fontSize: TYPE_SCALE.EYEBROW.fontSize, letterSpacing: TYPE_SCALE.EYEBROW.letterSpacing },
};

interface EyebrowProps {
  text: string;
  color?: string;
  size?: "sm" | "md";
}

export function Eyebrow({ text, color, size = "md" }: EyebrowProps): React.ReactElement {
  const theme: Theme = useTheme();
  const sizeTokens = SIZE_MAP[size] || SIZE_MAP.md;

  const style = {
    ...TYPE_SCALE.EYEBROW,
    ...sizeTokens,
    color: color || theme.textDim,
    margin: 0,
  };

  return <div style={style}>{text}</div>;
}

export default Eyebrow;
