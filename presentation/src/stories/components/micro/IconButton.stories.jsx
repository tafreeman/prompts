import React from "react";
import { IconButton } from "../../../components/micro/IconButton.tsx";

export default {
  title: "Micro/IconButton",
  component: IconButton,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    size: { control: "radio", options: ["sm", "md", "lg"] },
    variant: { control: "radio", options: ["primary", "ghost"] },
  },
};

export const Default = {
  args: {
    icon: "🔍",
    size: "md",
    variant: "primary",
    onClick: () => {},
  },
};

export const SmallPrimary = {
  args: {
    icon: "✅",
    size: "sm",
    variant: "primary",
    onClick: () => {},
  },
};

export const LargePrimary = {
  args: {
    icon: "🚀",
    size: "lg",
    variant: "primary",
    onClick: () => {},
  },
};

export const Ghost = {
  args: {
    icon: "🛡️",
    size: "md",
    variant: "ghost",
    onClick: () => {},
  },
};

export const GhostLarge = {
  args: {
    icon: "📋",
    size: "lg",
    variant: "ghost",
    onClick: () => {},
  },
};

export const SizeScale = {
  render: () => (
    <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
      <IconButton icon="🔍" size="sm" variant="primary" onClick={() => {}} />
      <IconButton icon="🔍" size="md" variant="primary" onClick={() => {}} />
      <IconButton icon="🔍" size="lg" variant="primary" onClick={() => {}} />
    </div>
  ),
};

export const VariantComparison = {
  render: () => (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <IconButton icon="🛡️" size="md" variant="primary" onClick={() => {}} />
        <IconButton icon="✅" size="md" variant="primary" onClick={() => {}} />
        <IconButton icon="📋" size="md" variant="primary" onClick={() => {}} />
        <IconButton icon="🚀" size="md" variant="primary" onClick={() => {}} />
        <span style={{ fontSize: 12, color: "#888", marginLeft: 8 }}>primary</span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <IconButton icon="🛡️" size="md" variant="ghost" onClick={() => {}} />
        <IconButton icon="✅" size="md" variant="ghost" onClick={() => {}} />
        <IconButton icon="📋" size="md" variant="ghost" onClick={() => {}} />
        <IconButton icon="🚀" size="md" variant="ghost" onClick={() => {}} />
        <span style={{ fontSize: 12, color: "#888", marginLeft: 8 }}>ghost</span>
      </div>
    </div>
  ),
};
