/**
 * TechStackTimeline — technology evolution & timeline progression.
 *
 * Layout ID: "eng-tech-stack"
 * Renders a vertical timeline from topic.cards (milestones),
 * alternating left/right with a center spine.
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

function TechStackTimeline({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  const milestones = topic.cards as Array<{ stat?: string; title: string; body: string }> || [];
  const results = topic.results as Array<{ value?: string; val?: string; label?: string; lbl?: string }> || [];

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} type="future" active={entered} />
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

        {/* Results strip (if present) */}
        {results.length > 0 && (
          <div style={{
            display: "flex", justifyContent: "center", gap: 32, marginBottom: 36,
            opacity: entered ? 1 : 0, transition: "opacity 0.6s 0.3s",
          }}>
            {results.map((r, i) => (
              <div key={i} style={{ textAlign: "center" }}>
                <div style={{ fontFamily: T.fontDisplay, fontSize: 24, fontWeight: 700, color: topic.colorLight }}>{r.value || r.val}</div>
                <div style={{ fontSize: 10, color: T.textDim, textTransform: "uppercase", letterSpacing: 0.8 }}>{r.label || r.lbl}</div>
              </div>
            ))}
          </div>
        )}

        {/* Vertical timeline */}
        <div style={{ maxWidth: 720, margin: "0 auto", position: "relative" }}>
          {/* Center spine */}
          <div style={{
            position: "absolute", left: "50%", top: 0, bottom: 0,
            width: 2, background: `${topic.color}30`,
            transform: "translateX(-50%)",
          }} />

          {milestones.map((item, i) => {
            const isLeft = i % 2 === 0;
            return (
              <div key={i} style={{
                display: "flex", alignItems: "flex-start",
                flexDirection: isLeft ? "row" : "row-reverse",
                marginBottom: 24, position: "relative",
                opacity: entered ? 1 : 0,
                transform: entered ? "translateX(0)" : `translateX(${isLeft ? "-30px" : "30px"})`,
                transition: `all 0.5s ${0.3 + i * 0.1}s cubic-bezier(0.22,1,0.36,1)`,
              }}>
                {/* Card */}
                <div style={{
                  width: "calc(50% - 28px)",
                  background: T.bgCard,
                  borderRadius: C.innerRadius,
                  padding: "18px 22px",
                  border: `1px solid ${topic.color}15`,
                  [isLeft ? "borderRight" : "borderLeft"]: `3px solid ${topic.color}`,
                }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                    {item.stat && (
                      <span style={{ fontFamily: T.fontDisplay, fontSize: 18, fontWeight: 700, color: topic.colorLight }}>{item.stat}</span>
                    )}
                    <h4 style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: C.headingWeight, color: topic.colorLight, margin: 0 }}>{item.title}</h4>
                  </div>
                  <p style={{ fontSize: 12.5, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{item.body}</p>
                </div>

                {/* Center dot */}
                <div style={{
                  position: "absolute", left: "50%", top: 18,
                  width: 12, height: 12, borderRadius: "50%",
                  background: topic.color,
                  border: `2px solid ${T.bg}`,
                  transform: "translateX(-50%)",
                  boxShadow: `0 0 10px ${topic.color}40`,
                }} />
              </div>
            );
          })}
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

export default TechStackTimeline;
export { TechStackTimeline };
