/**
 * AdvPlatformLayout — focus panels, capabilities, and expandable lanes.
 *
 * Ported from v10.0 PlatformScreen into the v14 registry-based system.
 */

import { useState, useEffect } from "react";
import { useTheme } from "../../components/hooks/useTheme.ts";
import { useChrome } from "../../components/hooks/useChrome.ts";
import { usePresentationViewport } from "../../components/hooks/usePresentationViewport.ts";
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

export function AdvPlatformLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState(false);
  const [expandedLanes, setExpandedLanes] = useState<Record<number, boolean>>({});
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const heroPoints = topic.heroPoints as string[] || [];
  const focusPanels = topic.focusPanels as Array<{ label?: string; title: string; body?: string }> || [];
  const capabilities = topic.capabilities as Array<{ icon?: string; title: string; body?: string }> || [];
  const lanes = topic.lanes as Array<{ title: string; persona?: string; steps?: string[] }> || [];

  const toggleLane = (idx: number) => {
    setExpandedLanes((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}10,transparent 70%)`, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, maxWidth: 960, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />

        <div style={{ opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(28px)", transition: "all 0.8s cubic-bezier(0.22,1,0.36,1)" }}>

          {/* Header */}
          {topic.eyebrow && (
            <div style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: 2, color: T.accent, marginBottom: 10 }}>
              {topic.eyebrow as string}
            </div>
          )}
          <h1 style={{ fontSize: 34, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.text, margin: "0 0 8px" }}>
            {topic.title}
          </h1>
          {topic.subtitle && (
            <p style={{ fontSize: 15, color: T.textMuted, lineHeight: 1.65, marginTop: 0, marginBottom: 16 }}>
              {topic.subtitle}
            </p>
          )}

          {heroPoints.length > 0 && (
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 20 }}>
              {heroPoints.map((pt, i) => (
                <span key={i} style={{ display: "inline-flex", alignItems: "center", border: `1px solid ${topic.color}40`, borderRadius: 999, padding: "4px 14px", fontSize: 11, color: topic.color }}>
                  {pt}
                </span>
              ))}
            </div>
          )}

          {/* Focus panels */}
          {focusPanels.length > 0 && (
            <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr" : "repeat(3, 1fr)", gap: 12, marginTop: 24 }}>
              {focusPanels.map((panel, i) => (
                <div
                  key={i}
                  style={{
                    background: T.bgCard,
                    borderRadius: C.cardRadius,
                    padding: 18,
                    borderTop: `${C.accentBarHeight}px solid ${T.accent}`,
                    opacity: entered ? 1 : 0,
                    transform: entered ? "none" : "translateY(16px)",
                    transition: `all 0.5s ${0.2 + i * 0.08}s cubic-bezier(0.22,1,0.36,1)`,
                  }}
                >
                  {panel.label && (
                    <div style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: 1, color: T.accent }}>
                      {panel.label}
                    </div>
                  )}
                  <h4 style={{ fontSize: 15, fontWeight: 600, color: T.text, marginTop: 6, marginBottom: 0 }}>
                    {panel.title}
                  </h4>
                  {panel.body && (
                    <p style={{ fontSize: 12.5, color: T.textMuted, marginTop: 6, marginBottom: 0, lineHeight: 1.5 }}>
                      {panel.body}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Capabilities */}
          {capabilities.length > 0 && (
            <div style={{ marginTop: 24 }}>
              <h3 style={{ fontSize: 16, fontWeight: C.headingWeight, color: T.text, fontFamily: T.fontDisplay, margin: "0 0 12px" }}>
                Capabilities
              </h3>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                {capabilities.map((cap, i) => (
                  <div
                    key={i}
                    style={{
                      background: T.bgCard,
                      borderRadius: C.innerRadius,
                      padding: 14,
                      display: "flex",
                      gap: 10,
                      opacity: entered ? 1 : 0,
                      transform: entered ? "none" : "translateY(12px)",
                      transition: `all 0.5s ${0.35 + i * 0.06}s cubic-bezier(0.22,1,0.36,1)`,
                    }}
                  >
                    {cap.icon && (
                      <span style={{ fontSize: 20, flexShrink: 0 }}>{cap.icon}</span>
                    )}
                    <div>
                      <div style={{ fontSize: 13, fontWeight: 600, color: T.text }}>{cap.title}</div>
                      {cap.body && (
                        <p style={{ fontSize: 11.5, color: T.textMuted, marginTop: 3, marginBottom: 0, lineHeight: 1.45 }}>
                          {cap.body}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Lanes (expandable accordion) */}
          {lanes.length > 0 && (
            <div style={{ marginTop: 24 }}>
              {lanes.map((lane, i) => {
                const isOpen = !!expandedLanes[i];
                return (
                  <div key={i} style={{ marginBottom: 6 }}>
                    <button
                      onClick={() => toggleLane(i)}
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        width: "100%",
                        background: T.bgCard,
                        border: "none",
                        padding: "12px 16px",
                        borderRadius: C.innerRadius,
                        cursor: "pointer",
                        textAlign: "left",
                      }}
                    >
                      <span style={{ fontSize: 14, fontWeight: 600, color: T.text }}>{lane.title}</span>
                      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        {lane.persona && (
                          <span style={{ fontSize: 10, background: `${T.accent}15`, color: T.accent, padding: "2px 8px", borderRadius: 999 }}>
                            {lane.persona}
                          </span>
                        )}
                        <span style={{ fontSize: 14, color: T.textDim, lineHeight: 1 }}>
                          {isOpen ? "\u2212" : "+"}
                        </span>
                      </div>
                    </button>

                    {isOpen && lane.steps && (
                      <div style={{ padding: "10px 16px 6px", background: T.bgCard, borderRadius: `0 0 ${C.innerRadius}px ${C.innerRadius}px`, marginTop: 2 }}>
                        {lane.steps.map((step, si) => (
                          <div key={si} style={{ display: "flex", gap: 10, alignItems: "flex-start", marginBottom: 8 }}>
                            <span style={{ fontSize: 12, fontWeight: 700, color: T.accent, flexShrink: 0, minWidth: 16 }}>
                              {si + 1}.
                            </span>
                            <p style={{ fontSize: 12.5, color: T.textMuted, lineHeight: 1.45, margin: 0 }}>
                              {step}
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {/* Callout */}
          {topic.callout && (
            <div style={{
              marginTop: 24,
              borderLeft: `${C.accentBarHeight}px solid ${T.accent}`,
              background: T.bgCard,
              padding: 18,
              borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0`,
            }}>
              <p style={{ fontSize: 14, color: T.text, lineHeight: 1.65, margin: 0, fontWeight: 600 }}>
                &ldquo;{topic.callout}&rdquo;
              </p>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

export default AdvPlatformLayout;
