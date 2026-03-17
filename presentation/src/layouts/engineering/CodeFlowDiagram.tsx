/**
 * CodeFlowDiagram — data pipeline & code execution flow visualization.
 *
 * Layout ID: "eng-code-flow"
 * Renders a horizontal flow diagram from topic.cards (steps),
 * with arrows connecting each step node.
 */

import React, { useState, useEffect } from "react";
import { useTheme } from "../../components/hooks/useTheme.ts";
import { useChrome } from "../../components/hooks/useChrome.ts";
import BackBtn from "../../components/navigation/BackBtn.tsx";
import Particles from "../../components/animations/Particles.tsx";

interface Topic {
  id: string;
  title: string;
  subtitle?: string;
  color: string;
  colorLight?: string;
  colorGlow?: string;
  icon?: string;
  callout?: string;
  [key: string]: unknown;
}

interface LayoutProps {
  topic: Topic;
  onBack: () => void;
}

function CodeFlowDiagram({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  const steps = topic.cards as Array<{ stat?: string; icon?: string; title: string; body: string }> || [];

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} type="sprint" active={entered} />
      <div style={{ position: "relative", zIndex: 2, padding: "36px 48px" }}>
        <BackBtn onClick={onBack} />

        {/* Header */}
        <div style={{
          textAlign: "center", marginBottom: 40,
          opacity: entered ? 1 : 0,
          transform: entered ? "translateY(0)" : "translateY(-20px)",
          transition: "all 0.6s cubic-bezier(0.22,1,0.36,1)",
        }}>
          <div style={{ fontSize: 36, marginBottom: 10, filter: `drop-shadow(0 0 16px ${topic.colorGlow})` }}>{topic.icon}</div>
          <h1 style={{ fontFamily: T.fontDisplay, fontSize: 40, fontWeight: C.headingWeight, color: T.text, margin: "0 0 8px", textTransform: C.headingTransform }}>{topic.title}</h1>
          <p style={{ fontSize: 15, color: topic.colorLight, fontStyle: "italic", margin: 0 }}>{topic.subtitle}</p>
        </div>

        {/* Flow diagram — horizontal pipeline with arrow connectors */}
        <div style={{
          maxWidth: 1000, margin: "0 auto",
          display: "flex", alignItems: "stretch", gap: 0,
          overflowX: "auto", padding: "8px 0",
        }}>
          {steps.map((step, i) => (
            <React.Fragment key={i}>
              {/* Step node */}
              <div style={{
                flex: "1 0 0", minWidth: 140,
                display: "flex", flexDirection: "column", alignItems: "center",
                opacity: entered ? 1 : 0,
                transform: entered ? "translateY(0)" : "translateY(20px)",
                transition: `all 0.5s ${0.2 + i * 0.12}s cubic-bezier(0.22,1,0.36,1)`,
              }}>
                {/* Node circle */}
                <div style={{
                  width: 56, height: 56, borderRadius: "50%",
                  background: `${topic.color}15`,
                  border: `2px solid ${topic.color}50`,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  marginBottom: 12,
                  boxShadow: `0 0 20px ${topic.color}20`,
                }}>
                  <span style={{ fontSize: 13, fontWeight: 700, color: topic.colorLight, fontFamily: T.fontDisplay }}>
                    {step.stat || step.icon || `${i + 1}`}
                  </span>
                </div>

                {/* Step label */}
                <div style={{
                  background: T.bgCard,
                  borderRadius: C.innerRadius,
                  padding: "14px 16px",
                  textAlign: "center",
                  border: `1px solid ${topic.color}15`,
                  width: "100%",
                }}>
                  <h4 style={{ fontFamily: T.fontDisplay, fontSize: 13, fontWeight: C.headingWeight, color: topic.colorLight, margin: "0 0 6px" }}>{step.title}</h4>
                  <p style={{ fontSize: 11.5, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{step.body}</p>
                </div>
              </div>

              {/* Arrow connector */}
              {i < steps.length - 1 && (
                <div style={{
                  display: "flex", alignItems: "center", justifyContent: "center",
                  width: 32, flexShrink: 0, paddingBottom: 60,
                  opacity: entered ? 1 : 0,
                  transition: `opacity 0.4s ${0.4 + i * 0.12}s`,
                }}>
                  <svg width="24" height="16" viewBox="0 0 24 16" fill="none">
                    <path d="M0 8H20M20 8L14 2M20 8L14 14" stroke={topic.color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
              )}
            </React.Fragment>
          ))}
        </div>

        {/* Callout */}
        {topic.callout && (
          <div style={{
            marginTop: 36, background: T.bgCard, borderRadius: C.innerRadius,
            padding: "16px 28px", borderLeft: `4px solid ${topic.color}`,
            display: "flex", alignItems: "center", gap: 16,
            maxWidth: 1000, marginLeft: "auto", marginRight: "auto",
            opacity: entered ? 1 : 0, transition: "opacity 0.6s 1.5s",
          }}>
            <div style={{ fontSize: 22, color: topic.color }}>{topic.icon}</div>
            <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.6, margin: 0 }}>
              <strong style={{ color: topic.colorLight }}>{topic.callout}</strong>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default CodeFlowDiagram;
export { CodeFlowDiagram };
