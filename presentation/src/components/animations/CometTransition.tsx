/**
 * CometTransition — animated comet flying from a source point to screen center.
 *
 * Extracted from the monolith (genai_advocacy_hub_13.jsx lines 555-631).
 * Used as a transition effect when navigating between topics.
 *
 * @example
 *   <CometTransition from={{ x: 200, y: 300 }} color="#22D3EE" active={true} onDone={() => {}} />
 */

import React, { useState, useEffect, useRef } from "react";

interface CometOrigin {
  x: number;
  y: number;
}

type CometPhase = "idle" | "launch" | "done";

interface CometTransitionProps {
  from?: CometOrigin | null;
  color?: string;
  active: boolean;
  onDone: () => void;
}

function CometTransition({ from, color, active, onDone }: CometTransitionProps) {
  const onDoneRef = useRef(onDone);
  onDoneRef.current = onDone;
  const [phase, setPhase] = useState<CometPhase>("idle");

  useEffect(() => {
    if (!active || !from) return;
    setPhase("idle");
    // Force reflow then launch
    const t1 = requestAnimationFrame(() => {
      requestAnimationFrame(() => setPhase("launch"));
    });
    const t2 = setTimeout(() => {
      setPhase("done");
      onDoneRef.current();
    }, 700);
    return () => {
      cancelAnimationFrame(t1);
      clearTimeout(t2);
    };
  }, [active, from]);

  if (!active || !from) return null;

  const tx =
    (typeof window !== "undefined" ? window.innerWidth / 2 : 500) - from.x;
  const ty =
    (typeof window !== "undefined" ? window.innerHeight / 2 : 400) - from.y;

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 100,
        pointerEvents: "none",
        overflow: "hidden",
      }}
    >
      {/* Comet head */}
      <div
        style={{
          position: "absolute",
          left: from.x - 10,
          top: from.y - 10,
          width: 20,
          height: 20,
          borderRadius: "50%",
          background: color,
          boxShadow: `0 0 30px 10px ${color}, 0 0 60px 20px ${color}80, 0 0 4px 2px #FFFFFF`,
          transform:
            phase === "launch"
              ? `translate(${tx}px, ${ty}px) scale(0.3)`
              : "translate(0,0) scale(1)",
          opacity: phase === "launch" ? 0.2 : 1,
          transition:
            "transform 0.6s cubic-bezier(0.16,1,0.3,1), opacity 0.6s ease",
        }}
      />
      {/* Trail */}
      {[...Array(8)].map((_, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: from.x - (6 - i * 0.5),
            top: from.y - (6 - i * 0.5),
            width: 12 - i,
            height: 12 - i,
            borderRadius: "50%",
            background: color,
            opacity: phase === "launch" ? 0 : 0.5 - i * 0.06,
            transform:
              phase === "launch"
                ? `translate(${tx * (1 - i * 0.08)}px, ${ty * (1 - i * 0.08)}px)`
                : "translate(0,0)",
            transition: `transform ${0.6 + i * 0.03}s cubic-bezier(0.16,1,0.3,1) ${i * 0.02}s, opacity ${0.5}s ease ${i * 0.02}s`,
          }}
        />
      ))}
      {/* Impact ring */}
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "50%",
          width: phase === "launch" ? 200 : 0,
          height: phase === "launch" ? 200 : 0,
          marginLeft: phase === "launch" ? -100 : 0,
          marginTop: phase === "launch" ? -100 : 0,
          borderRadius: "50%",
          border: `2px solid ${color}60`,
          background: `${color}08`,
          transition: "all 0.4s 0.4s ease-out",
          opacity: phase === "launch" ? 0 : 1,
        }}
      />
    </div>
  );
}

export default CometTransition;
