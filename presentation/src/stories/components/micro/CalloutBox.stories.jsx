import React from "react";
import { CalloutBox } from "../../../components/micro/CalloutBox.tsx";

export default {
  title: "Micro/CalloutBox",
  component: CalloutBox,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    variant: { control: "radio", options: ["primary", "secondary"] },
    tone: { control: "radio", options: ["default", "warning"] },
  },
};

export const Default = {
  args: {
    variant: "primary",
    tone: "default",
  },
  render: (args) => (
    <div style={{ maxWidth: 560 }}>
      <CalloutBox {...args}>
        All AI-generated code is treated as untrusted input. Every pull request triggers automated
        review via the code-reviewer agent before merge is permitted.
      </CalloutBox>
    </div>
  ),
};

export const Secondary = {
  args: {
    variant: "secondary",
    tone: "default",
  },
  render: (args) => (
    <div style={{ maxWidth: 560 }}>
      <CalloutBox {...args}>
        Governance principle: humans set policy, AI enforces it consistently at scale across every
        sprint and every team member.
      </CalloutBox>
    </div>
  ),
};

export const WarningTone = {
  args: {
    variant: "primary",
    tone: "warning",
  },
  render: (args) => (
    <div style={{ maxWidth: 560 }}>
      <CalloutBox {...args}>
        3 critical security findings were flagged during the onboarding sprint. All were resolved
        before the code was promoted to the integration branch.
      </CalloutBox>
    </div>
  ),
};

export const SecondaryWarning = {
  args: {
    variant: "secondary",
    tone: "warning",
  },
  render: (args) => (
    <div style={{ maxWidth: 560 }}>
      <CalloutBox {...args}>
        Hardcoded secrets detected in 2 files. Rotate immediately and re-run the security scan
        before proceeding.
      </CalloutBox>
    </div>
  ),
};

export const AllVariants = {
  render: () => (
    <div style={{ display: "flex", flexDirection: "column", gap: 20, maxWidth: 560 }}>
      <CalloutBox variant="primary" tone="default">
        Primary default — key takeaway from the AI governance review cycle.
      </CalloutBox>
      <CalloutBox variant="secondary" tone="default">
        Secondary default — supporting detail about the onboarding workflow.
      </CalloutBox>
      <CalloutBox variant="primary" tone="warning">
        Primary warning — policy violation requires immediate remediation before next sprint.
      </CalloutBox>
      <CalloutBox variant="secondary" tone="warning">
        Secondary warning — elevated risk identified in dependency audit.
      </CalloutBox>
    </div>
  ),
};
