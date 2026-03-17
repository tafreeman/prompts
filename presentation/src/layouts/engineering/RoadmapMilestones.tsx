/**
 * RoadmapMilestones — development roadmap & milestone tracking.
 *
 * Layout ID: "eng-roadmap"
 * Renders a horizontal milestone track from topic.cards,
 * with progress indicators and phase descriptions.
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

function RoadmapMilestones({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 50); return () => clearTimeout(t); }, []);

  const milestones = topic.cards as Array<{ stat?: string; icon?: string; title: string; body: string }> || [];
  const talkingPoints = topic.talkingPoints as string[] || [];

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

        {/* Milestone track — horizontal progress bar with nodes */}
        <div style={{ maxWidth: 900, margin: "0 auto 36px", position: "relative" }}>
          {/* Progress bar */}
          <div style={{
            position: "absolute", top: 24, left: 24, right: 24,
            height: 3,
            background: `${topic.color}20`,
          }}>
            <div style={{
              height: "100%",
              width: entered ? "100%" : "0%",
              background: `linear-gradient(90deg, ${topic.color}, ${topic.colorLight})`,
              transition: "width 1.5s 0.5s cubic-bezier(0.22,1,0.36,1)",
            }} />
          </div>

          {/* Milestone nodes */}
          <div style={{ display: "flex", justifyContent: "space-between", position: "relative" }}>
            {milestones.map((m, i) => (
              <div key={i} style={{
                display: "flex", flexDirection: "column", alignItems: "center",
                flex: "1 0 0", maxWidth: 160,
                opacity: entered ? 1 : 0,
                transform: entered ? "translateY(0)" : "translateY(15px)",
                transition: `all 0.5s ${0.4 + i * 0.15}s cubic-bezier(0.22,1,0.36,1)`,
              }}>
                {/* Node dot */}
                <div style={{
                  width: 48, height: 48, borderRadius: "50%",
                  background: T.bgCard,
                  border: `3px solid ${topic.color}`,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  marginBottom: 14, position: "relative", zIndex: 2,
                  boxShadow: `0 0 16px ${topic.color}30`,
                }}>
                  <span style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: 700, color: topic.colorLight }}>
                    {m.stat || m.icon || `M${i + 1}`}
                  </span>
                </div>

                {/* Phase card */}
                <div style={{
                  background: T.bgCard,
                  borderRadius: C.innerRadius,
                  padding: "14px 14px 12px",
                  textAlign: "center",
                  border: `1px solid ${topic.color}15`,
                  width: "100%",
                }}>
                  <h4 style={{ fontFamily: T.fontDisplay, fontSize: 12, fontWeight: C.headingWeight, color: topic.colorLight, margin: "0 0 6px", textTransform: "uppercase", letterSpacing: 0.5 }}>{m.title}</h4>
                  <p style={{ fontSize: 11, color: T.textMuted, lineHeight: 1.45, margin: 0 }}>{m.body}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Talking points */}
        {talkingPoints.length > 0 && (
          <div style={{
            maxWidth: 700, margin: "0 auto",
            opacity: entered ? 1 : 0, transition: "opacity 0.6s 1.2s",
          }}>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {talkingPoints.map((point, i) => (
                <div key={i} style={{
                  display: "flex", alignItems: "flex-start", gap: 10,
                  padding: "8px 16px",
                  background: T.bgCard,
                  borderRadius: C.innerRadius,
                  border: `1px solid ${topic.color}10`,
                }}>
                  <span style={{ color: topic.color, fontWeight: 700, fontSize: 14, lineHeight: 1.5, flexShrink: 0 }}>&bull;</span>
                  <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{point}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Callout */}
        {topic.callout && (
          <div style={{
            marginTop: 32, background: T.bgCard, borderRadius: C.innerRadius,
            padding: "16px 28px", borderLeft: `4px solid ${topic.color}`,
            display: "flex", alignItems: "center", gap: 16,
            maxWidth: 900, marginLeft: "auto", marginRight: "auto",
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

export default RoadmapMilestones;
export { RoadmapMilestones };
