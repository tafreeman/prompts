import React, { useState } from "react";
import ThematicIntro from "../../../components/animations/ThematicIntro.tsx";
const action = (name) => (...args) => console.log(`[action] ${name}`, ...args);

export default {
  title: "Animations/ThematicIntro",
  component: ThematicIntro,
  parameters: {
    layout: "fullscreen",
  },
};

const advocacyDeck = {
  introBrandLine: "AI-Assisted Delivery",
  introTitle: "GenAI Transformation",
  introSubtitle: "From prototype to production in 2 months",
  introStats: [
    { val: "~40%", lbl: "Uplift", color: "#22D3EE" },
    { val: "2 mo", lbl: "Delivery", color: "#34D399" },
    { val: "0", lbl: "Defects", color: "#10B981" },
    { val: "~90%", lbl: "AI Code", color: "#A78BFA" },
  ],
};

const engineeringDeck = {
  introBrandLine: "Design System \u00B7 Engineering",
  introTitle: "Platform Architecture",
  introSubtitle: "From monolith to modular design system",
  introStats: [
    { val: "26", lbl: "Layouts", color: "#60A5FA" },
    { val: "6", lbl: "Families", color: "#34D399" },
    { val: "768", lbl: "Lines", color: "#A78BFA" },
    { val: "~1s", lbl: "Build", color: "#F59E0B" },
  ],
};

const studioDeck = {
  introBrandLine: "AI Studio \u00B7 Handbook",
  introTitle: "The Studio Handbook",
  introSubtitle: "How we work, what we build, what we believe.",
  introStats: [
    { val: "5", lbl: "Practices", color: "#F4E04D" },
    { val: "8", lbl: "Process Steps", color: "#F2A614" },
    { val: "6+", lbl: "Client Archetypes", color: "#C53B2F" },
    { val: "1", lbl: "Manifesto", color: "#0E0E0B" },
  ],
};

function IntroHarness({ deck }) {
  const [key, setKey] = useState(0);
  const [completed, setCompleted] = useState(false);

  const handleComplete = () => {
    action("intro-complete")();
    setCompleted(true);
  };

  const handleReplay = () => {
    setCompleted(false);
    setKey((k) => k + 1);
  };

  return (
    <div style={{ minHeight: "100vh", background: "#020810" }}>
      {!completed && (
        <ThematicIntro key={key} deck={deck} onComplete={handleComplete} />
      )}
      {completed && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: 16,
            fontFamily: "'Space Grotesk', sans-serif",
          }}
        >
          <p style={{ color: "#64748B", fontSize: 14, margin: 0 }}>
            Intro sequence complete.
          </p>
          <button
            onClick={handleReplay}
            style={{
              background: "rgba(34,211,238,0.1)",
              border: "1px solid rgba(34,211,238,0.4)",
              borderRadius: 8,
              padding: "10px 24px",
              color: "#22D3EE",
              fontSize: 13,
              fontFamily: "'Space Grotesk', sans-serif",
              cursor: "pointer",
              letterSpacing: 1,
              textTransform: "uppercase",
            }}
          >
            Replay
          </button>
        </div>
      )}
    </div>
  );
}

export const AdvocacyDeck = {
  render: () => <IntroHarness deck={advocacyDeck} />,
};

export const EngineeringDeck = {
  render: () => <IntroHarness deck={engineeringDeck} />,
};

export const StudioDeck = {
  render: () => <IntroHarness deck={studioDeck} />,
};

export const DefaultFallback = {
  render: () => <IntroHarness deck={{}} />,
};
