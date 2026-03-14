/**
 * CalloutBox — bordered highlight box for callout sections and key takeaways.
 *
 * @param {object} props
 * @param {React.ReactNode} props.children - Content to display inside the box.
 * @param {'primary'|'secondary'} [props.variant='primary'] - Visual weight.
 * @param {'default'|'warning'} [props.tone='default'] - Color tone (warning uses theme.warning).
 */

import React from "react";
import PropTypes from "prop-types";
import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";
import { SPACING } from "../../tokens/spacing.ts";

const VARIANT_STYLES = {
  primary: (theme, chrome) => ({
    background: theme.bgCard,
    borderRadius: chrome.cardRadius,
    borderTop: `${chrome.accentBarHeight}px solid ${theme.accent}`,
  }),
  secondary: (theme, chrome) => ({
    background: "transparent",
    borderRadius: chrome.innerRadius,
    borderLeft: `${chrome.accentBarHeight}px solid ${theme.accent}`,
  }),
};

export function CalloutBox({ children, variant = "primary", tone = "default" }) {
  const theme = useTheme();
  const chrome = useChrome();

  const accentColor = tone === "warning" ? theme.warning : theme.accent;
  const variantFn = VARIANT_STYLES[variant] || VARIANT_STYLES.primary;
  const variantStyle = variantFn(theme, chrome);

  // Override accent with tone-aware color
  const borderKeys = Object.keys(variantStyle).filter((k) => k.startsWith("border"));
  const toneOverrides = {};
  for (const key of borderKeys) {
    if (typeof variantStyle[key] === "string" && variantStyle[key].includes(theme.accent)) {
      toneOverrides[key] = variantStyle[key].replace(theme.accent, accentColor);
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

CalloutBox.propTypes = {
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(["primary", "secondary"]),
  tone: PropTypes.oneOf(["default", "warning"]),
};
