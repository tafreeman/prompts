import React, { useState, useEffect } from "react";
import { useTheme } from "../../components/hooks/useTheme.ts";
import { usePresentationViewport } from "../../components/hooks/usePresentationViewport.ts";
import BackBtn from "../../components/navigation/BackBtn.tsx";
import Particles from "../../components/animations/Particles.tsx";
import { Figure8Cycle } from "./Figure8Cycle.tsx";
import { CircularRingCycle } from "./CircularRingCycle.tsx";
import type { Theme } from "../../tokens/themes.ts";

interface SprintNode {
  icon: string;
  label: string;
  type: string;
}

interface Topic {
  id: string;
  title: string;
  subtitle?: string;
  color: string;
  colorLight?: string;
  colorGlow?: string;
  icon?: string;
  num?: string;
  order?: number;
  callout?: string;
  banner?: string;
  eyebrow?: string;
  summary?: string;
  heroPoints?: string[];
  talkingPoints?: string[];
  cards?: Record<string, unknown>[];
  [key: string]: unknown;
}

interface SprintLayoutProps {
  topic: Topic;
  onBack: () => void;
  nodes: SprintNode[];
}

export function SprintLayout({ topic, onBack, nodes }: SprintLayoutProps) {
  const T = useTheme() as Theme;
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState<boolean>(false);
  const [layout, setLayout] = useState<string>("fig8");
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} type="sprint" active={entered} />
      <div style={{ position: "relative", zIndex: 2, padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />

        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: 24, opacity: entered ? 1 : 0, transform: entered ? "translateY(0)" : "translateY(-20px)", transition: "all 0.6s cubic-bezier(0.22,1,0.36,1)" }}>
          <div style={{ fontSize: 38, marginBottom: 6, display: "inline-block" }}>
            <span style={{ display: "inline-block", animation: entered ? "spinI 8s linear infinite" : "none" }}>⟳</span>
          </div>
          <style>{`@keyframes spinI { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
          <h1 style={{ fontFamily: "'Space Grotesk',sans-serif", fontSize: viewport.isPhone ? 28 : 36, fontWeight: 700, color: "#F0F4F8", margin: "0 0 6px" }}>AI Sprint Cycle</h1>
          <p style={{ fontSize: viewport.isPhone ? 13 : 14, color: topic.colorLight, fontStyle: "italic", margin: "0 0 16px" }}>{topic.subtitle}</p>

          {/* Layout toggle */}
          <div style={{ display: "flex", justifyContent: "center", gap: 8, flexWrap: "wrap" }}>
            {([["fig8", "Figure-8 Infinity"], ["ring", "Circular Ring"]] as [string, string][]).map(([k, l]) => (
              <button key={k} onClick={() => setLayout(k)} style={{
                padding: "6px 16px", borderRadius: 20, cursor: "pointer", fontFamily: "'Space Grotesk',sans-serif", fontSize: 12, fontWeight: 600,
                background: layout === k ? "rgba(139,92,246,0.15)" : "rgba(255,255,255,0.05)",
                border: `1px solid ${layout === k ? "#8B5CF6" : "rgba(255,255,255,0.08)"}`,
                color: layout === k ? "#A78BFA" : "#64748B",
              }}>{l}</button>
            ))}
          </div>
        </div>

        {/* Diagram container */}
        <div style={{ background: "#111827", borderRadius: 16, padding: viewport.isPhone ? "18px 10px" : "28px 20px", border: "1px solid rgba(139,92,246,0.12)", maxWidth: layout === "fig8" ? 920 : 540, margin: "0 auto", boxShadow: "0 4px 40px rgba(0,0,0,0.3)", overflowX: "auto", overflowY: "hidden" }}>
          {layout === "fig8" && <Figure8Cycle entered={entered} nodes={nodes} />}
          {layout === "ring" && <CircularRingCycle entered={entered} nodes={nodes} />}
        </div>

        {/* Callout */}
        <div style={{ marginTop: 24, background: "#162240", borderRadius: 10, padding: viewport.isPhone ? "16px 18px" : "16px 28px", borderLeft: "4px solid #8B5CF6", display: "flex", alignItems: "center", gap: 16, maxWidth: 920, marginLeft: "auto", marginRight: "auto", opacity: entered ? 1 : 0, transition: "opacity 0.6s 1.5s" }}>
          <div style={{ fontSize: 22, color: "#8B5CF6" }}>⟳</div>
          <p style={{ fontSize: 13, color: "#CBD5E1", lineHeight: 1.6, margin: 0 }}>
            <strong style={{ color: "#A78BFA" }}>{topic.callout}</strong>
          </p>
        </div>
      </div>
    </div>
  );
}

export default SprintLayout;
