import React from "react";
import { Eyebrow } from "../../../components/micro/Eyebrow.tsx";

export default {
  title: "Micro/Eyebrow",
  component: Eyebrow,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    color: { control: "color" },
    size: { control: "radio", options: ["sm", "md"] },
  },
};

export const Default = {
  args: {
    text: "AI Governance",
    size: "md",
  },
};

export const SmallSize = {
  args: {
    text: "Code Review Protocol",
    size: "sm",
  },
};

export const CustomColor = {
  args: {
    text: "Onboarding Track",
    size: "md",
    color: "#22D3EE",
  },
};

export const WarningColor = {
  args: {
    text: "Policy Violation",
    size: "md",
    color: "#F59E0B",
  },
};

export const AllVariants = {
  render: () => (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <div>
        <Eyebrow text="AI Governance" size="md" />
        <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>size md (default)</div>
      </div>
      <div>
        <Eyebrow text="Code Review Protocol" size="sm" />
        <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>size sm</div>
      </div>
      <div>
        <Eyebrow text="Onboarding Track" size="md" color="#22D3EE" />
        <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>custom color</div>
      </div>
      <div>
        <Eyebrow text="Sprint Retrospective" size="sm" color="#10B981" />
        <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>sm + custom color</div>
      </div>
    </div>
  ),
};
