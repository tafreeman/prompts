import React from "react";
import Particles from "../components/animations/Particles.tsx";

export default {
  title: "Animations/Particles",
  component: Particles,
  parameters: {
    layout: "fullscreen",
  },
  argTypes: {
    color: { control: "color" },
    type: {
      control: { type: "select" },
      options: ["hurdles", "human", "sprint"],
    },
    active: { control: "boolean" },
  },
};

const wrapper = {
  position: "relative",
  height: 400,
  background: "#0B1426",
  borderRadius: 8,
  overflow: "hidden",
};

export const Default = {
  args: {
    color: "#22D3EE",
    type: "human",
    active: true,
  },
  render: (args) => (
    <div style={wrapper}>
      <Particles {...args} />
    </div>
  ),
};

export const Hurdles = {
  args: {
    color: "#F59E0B",
    type: "hurdles",
    active: true,
  },
  render: (args) => (
    <div style={wrapper}>
      <Particles {...args} />
    </div>
  ),
};

export const Human = {
  args: {
    color: "#10B981",
    type: "human",
    active: true,
  },
  render: (args) => (
    <div style={wrapper}>
      <Particles {...args} />
    </div>
  ),
};

export const Sprint = {
  args: {
    color: "#8B5CF6",
    type: "sprint",
    active: true,
  },
  render: (args) => (
    <div style={wrapper}>
      <Particles {...args} />
    </div>
  ),
};
