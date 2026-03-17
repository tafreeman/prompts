/**
 * ArchitectureSlide — system architecture & component topology visualization.
 *
 * Layout ID: "eng-architecture"
 * Renders a layered architecture diagram from topic.cards,
 * with each card representing a system component/layer.
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

function ArchitectureSlide({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  const layers = topic.cards as Array<{ stat?: string; icon?: string; title: string; body: string; statLabel?: string }> || [];

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} type="future" active={entered} />
      <div style={{ position: "relative", zIndex: 2, padding: "36px 48px" }}>
        <BackBtn onClick={onBack} />

        {/* Header */}
        <div style={{
          textAlign: "center", marginBottom: 36,
          opacity: entered ? 1 : 0,
          transform: entered ? "translateY(0)" : "translateY(-20px)",
          transition: "all 0.6s cubic-bezier(0.22,1,0.36,1)",
        }}>
          <div style={{ fontSize: 36, marginBottom: 10, filter: `drop-shadow(0 0 16px ${topic.colorGlow})` }}>{topic.icon}</div>
          <h1 style={{ fontFamily: T.fontDisplay, fontSize: 40, fontWeight: C.headingWeight, color: T.text, margin: "0 0 8px", textTransform: C.headingTransform }}>{topic.title}</h1>
          <p style={{ fontSize: 15, color: topic.colorLight, fontStyle: "italic", margin: 0 }}>{topic.subtitle}</p>
        </div>

        {/* Architecture layers — stacked vertically with connecting lines */}
        <div style={{ maxWidth: 800, margin: "0 auto", display: "flex", flexDirection: "column", gap: 2 }}>
          {layers.map((layer, i) => (
            <div key={i} style={{
              display: "flex", flexDirection: "column", alignItems: "center",
              opacity: entered ? 1 : 0,
              transform: entered ? "scale(1)" : "scale(0.9)",
              transition: `all 0.5s ${0.2 + i * 0.1}s cubic-bezier(0.22,1,0.36,1)`,
            }}>
              {/* Connector line */}
              {i > 0 && (
                <div style={{
                  width: 2, height: 20,
                  background: `linear-gradient(to bottom, ${topic.color}40, ${topic.color})`,
                  marginBottom: 2,
                }} />
              )}

              {/* Layer card */}
              <div style={{
                width: "100%",
                background: T.bgCard,
                borderRadius: C.innerRadius,
                padding: "20px 28px",
                border: `1px solid ${topic.color}20`,
                borderLeft: `${C.accentBarHeight + 1}px solid ${topic.color}`,
                display: "flex", alignItems: "center", gap: 16,
              }}>
                {/* Layer number badge */}
                <div style={{
                  width: 36, height: 36, borderRadius: "50%",
                  background: `${topic.color}18`,
                  border: `1px solid ${topic.color}40`,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontFamily: T.fontDisplay, fontSize: 14, fontWeight: 700,
                  color: topic.colorLight, flexShrink: 0,
                }}>
                  {layer.stat || layer.icon || `L${i + 1}`}
                </div>

                <div style={{ flex: 1 }}>
                  <h3 style={{ fontFamily: T.fontDisplay, fontSize: 16, fontWeight: C.headingWeight, color: topic.colorLight, margin: "0 0 4px" }}>{layer.title}</h3>
                  <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{layer.body}</p>
                </div>

                {layer.statLabel && (
                  <div style={{
                    fontSize: 10, color: T.textDim, textTransform: "uppercase",
                    letterSpacing: 0.8, flexShrink: 0,
                  }}>{layer.statLabel}</div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Callout */}
        {topic.callout && (
          <div style={{
            textAlign: "center", marginTop: 36, maxWidth: 700,
            marginLeft: "auto", marginRight: "auto",
            opacity: entered ? 1 : 0, transition: "opacity 0.8s 1s",
          }}>
            <p style={{ fontSize: 15, color: T.textMuted, lineHeight: 1.6, margin: 0 }}>
              <strong style={{ color: topic.colorLight }}>{topic.callout}</strong>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ArchitectureSlide;
export { ArchitectureSlide };
