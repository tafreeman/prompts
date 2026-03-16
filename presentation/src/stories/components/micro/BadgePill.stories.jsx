import React from "react";
import { BadgePill } from "../../../components/micro/BadgePill.tsx";

export default {
  title: "Micro/BadgePill",
  component: BadgePill,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    color: { control: "color" },
    variant: { control: "radio", options: ["primary", "secondary"] },
  },
};

export const Default = {
  args: {
    label: "AI Governance",
    variant: "primary",
  },
};

export const WithIcon = {
  args: {
    icon: "🛡️",
    label: "Policy Enforced",
    variant: "primary",
  },
};

export const WithIconAndValue = {
  args: {
    icon: "✅",
    label: "Tests Passing",
    value: "1,400+",
    variant: "primary",
  },
};

export const Secondary = {
  args: {
    icon: "🔍",
    label: "Code Review",
    value: "24",
    variant: "secondary",
  },
};

export const CustomColor = {
  args: {
    icon: "🚀",
    label: "Sprint Velocity",
    value: "14",
    color: "#10B981",
    variant: "primary",
  },
};

export const WarningColor = {
  args: {
    icon: "⚠️",
    label: "Violations",
    value: "3",
    color: "#F59E0B",
    variant: "primary",
  },
};

export const BadgeRow = {
  render: () => (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
      <BadgePill icon="🛡️" label="AI Governance" variant="primary" />
      <BadgePill icon="✅" label="Tests Passing" value="1,400+" variant="primary" />
      <BadgePill icon="🔍" label="Code Review" value="24" variant="secondary" />
      <BadgePill icon="🚀" label="Sprints" value="14" color="#10B981" variant="primary" />
      <BadgePill icon="⚠️" label="Violations" value="3" color="#F59E0B" variant="primary" />
      <BadgePill icon="🏗️" label="ADRs Filed" value="12" color="#8B5CF6" variant="primary" />
      <BadgePill label="Zero Defects" variant="secondary" />
    </div>
  ),
};
