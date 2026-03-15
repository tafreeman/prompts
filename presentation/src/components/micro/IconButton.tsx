/**
 * IconButton — small interactive button displaying an icon.
 *
 * @param props.icon - Emoji or icon character to render.
 * @param props.onClick - Click handler.
 * @param props.size - Button size.
 * @param props.variant - Visual style.
 */

import React from "react";
import { useTheme } from "../hooks/useTheme.js";
import type { Theme } from "../../tokens/themes.ts";

const SIZE_MAP = {
  sm: { width: 28, height: 28, fontSize: 14 },
  md: { width: 36, height: 36, fontSize: 18 },
  lg: { width: 44, height: 44, fontSize: 22 },
};

interface IconButtonProps {
  icon: string;
  onClick: (e?: React.MouseEvent) => void;
  size?: "sm" | "md" | "lg";
  variant?: "primary" | "ghost";
}

export function IconButton({ icon, onClick, size = "md", variant = "primary" }: IconButtonProps): React.ReactElement {
  const theme: Theme = useTheme();
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
      onMouseEnter={(e: React.MouseEvent<HTMLButtonElement>) => {
        e.currentTarget.style.transform = "scale(1.1)";
      }}
      onMouseLeave={(e: React.MouseEvent<HTMLButtonElement>) => {
        e.currentTarget.style.transform = "scale(1)";
      }}
    >
      {icon}
    </button>
  );
}

export default IconButton;
