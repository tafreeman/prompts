import React from "react";
import { QuoteBlock } from "../../../components/micro/QuoteBlock.tsx";

export default {
  title: "Micro/QuoteBlock",
  component: QuoteBlock,
  parameters: {
    layout: "padded",
  },
  argTypes: {
    color: { control: "color" },
    variant: { control: "radio", options: ["left-accent", "border"] },
  },
};

export const Default = {
  args: {
    text: "AI accelerates delivery. Humans govern quality. That separation of concerns is what made this project succeed.",
    author: "Tech Lead, Deloitte Delivery Team",
    variant: "left-accent",
  },
  render: (args) => (
    <div style={{ maxWidth: 560 }}>
      <QuoteBlock {...args} />
    </div>
  ),
};

export const WithoutAuthor = {
  args: {
    text: "Every architectural decision is backed by an ADR. No undocumented choices reach production.",
    variant: "left-accent",
  },
  render: (args) => (
    <div style={{ maxWidth: 560 }}>
      <QuoteBlock {...args} />
    </div>
  ),
};

export const BorderVariant = {
  args: {
    text: "The code-reviewer agent caught 3 critical issues in the first sprint that would have caused integration failures downstream.",
    author: "Senior Engineer, Onboarding Cohort",
    variant: "border",
  },
  render: (args) => (
    <div style={{ maxWidth: 560 }}>
      <QuoteBlock {...args} />
    </div>
  ),
};

export const CustomColor = {
  args: {
    text: "Structured governance turned AI from a risk into a multiplier.",
    author: "Engineering Manager",
    variant: "left-accent",
    color: "#10B981",
  },
  render: (args) => (
    <div style={{ maxWidth: 560 }}>
      <QuoteBlock {...args} />
    </div>
  ),
};

export const AllVariants = {
  render: () => (
    <div style={{ display: "flex", flexDirection: "column", gap: 24, maxWidth: 560 }}>
      <QuoteBlock
        text="AI accelerates delivery. Humans govern quality."
        author="Tech Lead, Deloitte Delivery Team"
        variant="left-accent"
      />
      <QuoteBlock
        text="Every architectural decision is backed by an ADR. No undocumented choices reach production."
        variant="left-accent"
      />
      <QuoteBlock
        text="The code-reviewer agent caught 3 critical issues that would have caused downstream failures."
        author="Senior Engineer, Onboarding Cohort"
        variant="border"
      />
      <QuoteBlock
        text="Structured governance turned AI from a risk into a multiplier."
        author="Engineering Manager"
        variant="left-accent"
        color="#10B981"
      />
    </div>
  ),
};
