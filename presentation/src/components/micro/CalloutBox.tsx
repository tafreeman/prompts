/**
 * CalloutBox — bordered highlight box for callout sections and key takeaways.
 *
 * @param props.children - Content to display inside the box.
 * @param props.variant - Visual weight.
 * @param props.tone - Color tone (warning uses theme.warning).
 */

import React from "react";
import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";
import { SPACING } from "../../tokens/spacing.ts";
import type { Theme } from "../../tokens/themes.ts";
import type { StyleMode } from "../../tokens/style-modes.ts";

const VARIANT_STYLES = {
  primary: (theme: Theme, chrome: StyleMode) => ({
    background: theme.bgCard,
    borderRadius: chrome.cardRadius,
    borderTop: `${chrome.accentBarHeight}px solid ${theme.accent}`,
  }),
  secondary: (theme: Theme, chrome: StyleMode) => ({
    background: "transparent",
    borderRadius: chrome.innerRadius,
    borderLeft: `${chrome.accentBarHeight}px solid ${theme.accent}`,
  }),
};

interface CalloutBoxProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary";
  tone?: "default" | "warning";
}

export function CalloutBox({ children, variant = "primary", tone = "default" }: CalloutBoxProps): React.ReactElement {
  const theme: Theme = useTheme();
  const chrome: StyleMode = useChrome();

  const accentColor = tone === "warning" ? theme.warning : theme.accent;
  const variantFn = VARIANT_STYLES[variant] || VARIANT_STYLES.primary;
  const variantStyle = variantFn(theme, chrome);

  // Override accent with tone-aware color
  const borderKeys = Object.keys(variantStyle).filter((k) => k.startsWith("border"));
  const toneOverrides: Record<string, string> = {};
  for (const key of borderKeys) {
    const val = variantStyle[key as keyof typeof variantStyle];
    if (typeof val === "string" && val.includes(theme.accent)) {
      toneOverrides[key] = val.replace(theme.accent, accentColor);
    }
  }

  const style = {
    ...variantStyle,
    ...toneOverrides,
    padding: `${SPACING.lg}px ${SPACING.xl}px`,
    color: theme.text,
    fontFamily: theme.fontBody,
    fontSize: 14,
    lineHeight: 1.6,
  };

  return <div style={style}>{children}</div>;
}

export default CalloutBox;
