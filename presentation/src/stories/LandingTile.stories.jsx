import React, { useState } from "react";
import LandingTile from "../components/cards/LandingTile.tsx";

export default {
  title: "Cards/LandingTile",
  component: LandingTile,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    color: { control: "color" },
    colorLight: { control: "color" },
    colorGlow: { control: "color" },
    hovered: { control: "boolean" },
  },
};

const baseTile = {
  title: "Hurdles We Overcame",
  subtitle: "What changed from day one to delivery",
  icon: "\u2B21",
  num: "02",
  color: "#F59E0B",
  colorLight: "#FBBF24",
  colorGlow: "rgba(245,158,11,0.3)",
  onClick: () => {},
  onHover: () => {},
};

export const Default = {
  args: {
    ...baseTile,
    hovered: false,
  },
  render: (args) => (
    <div style={{ maxWidth: 280 }}>
      <LandingTile {...args} />
    </div>
  ),
};

export const Hovered = {
  args: {
    ...baseTile,
    hovered: true,
  },
  render: (args) => (
    <div style={{ maxWidth: 280 }}>
      <LandingTile {...args} />
    </div>
  ),
};

const tiles = [
  {
    title: "Hurdles We Overcame",
    subtitle: "What changed from day one to delivery",
    icon: "\u2B21",
    num: "01",
    color: "#F59E0B",
    colorLight: "#FBBF24",
    colorGlow: "rgba(245,158,11,0.3)",
  },
  {
    title: "Human in the Loop",
    subtitle: "AI accelerates. Humans govern.",
    icon: "\u26A1",
    num: "02",
    color: "#0891B2",
    colorLight: "#22D3EE",
    colorGlow: "rgba(8,145,178,0.3)",
  },
  {
    title: "Sprint Velocity",
    subtitle: "Measurable gains in delivery speed",
    icon: "\uD83D\uDE80",
    num: "03",
    color: "#10B981",
    colorLight: "#34D399",
    colorGlow: "rgba(16,185,129,0.3)",
  },
  {
    title: "Architecture",
    subtitle: "Production-grade patterns and tooling",
    icon: "\uD83C\uDFD7\uFE0F",
    num: "04",
    color: "#8B5CF6",
    colorLight: "#A78BFA",
    colorGlow: "rgba(139,92,246,0.3)",
  },
];

export const AllVariants = {
  render: () => {
    const [hoveredIdx, setHoveredIdx] = useState(null);

    return (
      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 16, maxWidth: 600 }}>
        {tiles.map((tile, i) => (
          <LandingTile
            key={i}
            {...tile}
            hovered={hoveredIdx === i}
            onClick={() => {}}
            onHover={(isHover) => setHoveredIdx(isHover ? i : null)}
          />
        ))}
      </div>
    );
  },
};
