/**
 * QuoteBlock — styled quote with optional author attribution.
 *
 * @param props.text - The quote body.
 * @param props.author - Attribution line below the quote.
 * @param props.color - Override accent color (defaults to theme.accent).
 * @param props.variant - Visual style.
 */

import React from "react";
import { useTheme } from "../hooks/useTheme.js";
import type { Theme } from "../../tokens/themes.ts";

interface QuoteBlockProps {
  text: string;
  author?: string;
  color?: string;
  variant?: "left-accent" | "border";
}

export function QuoteBlock({ text, author, color, variant = "left-accent" }: QuoteBlockProps): React.ReactElement {
  const theme: Theme = useTheme();
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

export default QuoteBlock;
