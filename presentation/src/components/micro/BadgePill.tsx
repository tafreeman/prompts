/**
 * BadgePill — pill-shaped badge with optional icon and stat value.
 *
 * @param props.icon - Leading emoji or icon character.
 * @param props.label - Badge label text.
 * @param props.value - Stat or count displayed after the label.
 * @param props.color - Override accent color (defaults to theme.accent).
 * @param props.variant - Visual weight.
 */

import React from "react";
import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";
import type { Theme } from "../../tokens/themes.ts";
import type { StyleMode } from "../../tokens/style-modes.ts";

interface BadgePillProps {
  icon?: string;
  label: string;
  value?: string;
  color?: string;
  variant?: "primary" | "secondary";
}

export function BadgePill({ icon, label, value, color, variant = "primary" }: BadgePillProps): React.ReactElement {
  const theme: Theme = useTheme();
  const chrome: StyleMode = useChrome();
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
    whiteSpace: "nowrap" as const,
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

export default BadgePill;
