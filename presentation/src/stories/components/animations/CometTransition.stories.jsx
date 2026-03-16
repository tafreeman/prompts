import React, { useState, useCallback } from "react";
import CometTransition from "../../../components/animations/CometTransition.tsx";
const action = (name) => (...args) => console.log(`[action] ${name}`, ...args);

export default {
  title: "Animations/CometTransition",
  component: CometTransition,
  parameters: {
    layout: "fullscreen",
  },
  argTypes: {
    color: { control: "color" },
  },
};

function CometHarness({ color = "#22D3EE", startX = 150, startY = 400 }) {
  const [active, setActive] = useState(false);

  const handleDone = useCallback(() => {
    action("comet-done")();
    setActive(false);
  }, []);

  return (
    <div
      style={{
        background: "#0B1426",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 24,
        fontFamily: "'Space Grotesk', sans-serif",
      }}
    >
      <CometTransition
        from={{ x: startX, y: startY }}
        color={color}
        active={active}
        onDone={handleDone}
      />
      <p style={{ color: "#64748B", fontSize: 14, margin: 0 }}>
        {active ? "Comet in flight..." : "Press the button to launch a comet"}
      </p>
      <button
        onClick={() => setActive(true)}
        disabled={active}
        style={{
          background: active ? "rgba(255,255,255,0.05)" : `${color}20`,
          border: `1px solid ${active ? "rgba(255,255,255,0.1)" : color + "60"}`,
          borderRadius: 8,
          padding: "10px 24px",
          color: active ? "#64748B" : color,
          fontSize: 13,
          fontFamily: "'Space Grotesk', sans-serif",
          cursor: active ? "not-allowed" : "pointer",
          letterSpacing: 1,
          textTransform: "uppercase",
        }}
      >
        {active ? "In Flight" : "Launch Comet"}
      </button>
      {/* Visual marker for the comet origin */}
      <div
        style={{
          position: "fixed",
          left: startX - 4,
          top: startY - 4,
          width: 8,
          height: 8,
          borderRadius: "50%",
          border: `1px solid ${color}60`,
          background: `${color}20`,
          pointerEvents: "none",
        }}
      />
    </div>
  );
}

export const Active = {
  render: () => <CometHarness color="#22D3EE" startX={150} startY={400} />,
};

export const EmberColor = {
  render: () => <CometHarness color="#F97316" startX={300} startY={500} />,
};

export const Inactive = {
  render: () => (
    <div
      style={{
        background: "#0B1426",
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "'Space Grotesk', sans-serif",
      }}
    >
      <CometTransition
        from={{ x: 200, y: 300 }}
        color="#22D3EE"
        active={false}
        onDone={action("comet-done")}
      />
      <p style={{ color: "#64748B", fontSize: 14, margin: 0 }}>
        Comet is inactive — nothing renders.
      </p>
    </div>
  ),
};
