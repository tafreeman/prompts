import React from "react";
import { StatValue } from "../../../components/micro/StatValue.tsx";

export default {
  title: "Micro/StatValue",
  component: StatValue,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    color: { control: "color" },
  },
};

export const Default = {
  args: {
    value: "~90%",
    label: "AI-assisted code review coverage",
  },
};

export const ZeroDefects = {
  args: {
    value: "0",
    label: "Production defects post-deployment",
  },
};

export const SprintVelocity = {
  args: {
    value: "14",
    label: "Sprints completed on schedule",
  },
};

export const CustomColor = {
  args: {
    value: "1,400+",
    label: "Automated test assertions",
    color: "#10B981",
  },
};

export const WarningTone = {
  args: {
    value: "3",
    label: "Policy violations flagged",
    color: "#F59E0B",
  },
};

export const StatGrid = {
  render: () => (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 32, maxWidth: 640 }}>
      <StatValue value="~90%" label="Code review coverage" />
      <StatValue value="0" label="Production defects" />
      <StatValue value="14" label="Sprints on schedule" />
      <StatValue value="1,400+" label="Automated tests" color="#10B981" />
      <StatValue value="24" label="Agent personas defined" color="#8B5CF6" />
      <StatValue value="3" label="Critical issues flagged" color="#F59E0B" />
    </div>
  ),
};
