import React from "react";
import { OptionalDeckLink } from "../components/navigation/OptionalDeckLink.tsx";
import { THEMES } from "../tokens/themes.ts";
import { STYLE_MODES_BY_ID } from "../tokens/style-modes.ts";

export default {
  title: "Navigation/OptionalDeckLink",
  component: OptionalDeckLink,
  parameters: {
    layout: "padded",
  },
};

const defaultTheme = THEMES[0];
const defaultChrome = STYLE_MODES_BY_ID["default"];

const mockTopic = {
  id: "one-pager",
  icon: "\uD83D\uDCCB",
  title: "Executive One-Pager",
  summary:
    "A single-slide companion deck distilling the key metrics, governance model, and delivery outcomes for leadership review.",
  heroPoints: ["12 Sprints", "1,400+ Tests", "Zero Defects"],
  talkingPoints: [
    "Structured AI governance prevented quality regression",
    "Every architectural decision backed by ADR evidence",
  ],
  color: "#22D3EE",
  colorGlow: "rgba(34,211,238,0.3)",
};

export const Default = {
  args: {
    topic: mockTopic,
    theme: defaultTheme,
    chrome: defaultChrome,
    onNavigate: () => {},
  },
  render: (args) => (
    <div style={{ maxWidth: 600 }}>
      <OptionalDeckLink {...args} />
    </div>
  ),
};

export const WithHover = {
  args: {
    topic: mockTopic,
    theme: defaultTheme,
    chrome: defaultChrome,
    onNavigate: () => {},
  },
  render: (args) => (
    <div style={{ maxWidth: 600 }}>
      <p style={{ fontSize: 13, color: args.theme.textMuted, marginBottom: 12 }}>
        Hover over the card below to see the interaction state.
      </p>
      <OptionalDeckLink {...args} />
    </div>
  ),
};
