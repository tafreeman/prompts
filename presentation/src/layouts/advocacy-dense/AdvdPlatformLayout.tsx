/**
 * AdvdPlatformLayout — Dense platform screen with 4-col capabilities and flat lanes.
 *
 * Ported from v10.2 information-dense PlatformScreen into the v14 registry system.
 * Capabilities always visible in 4-column grid, lanes are flat (no accordion).
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

export function AdvdPlatformLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const heroPoints = topic.heroPoints as string[] || [];
  const focusPanels = topic.focusPanels as Array<{ label?: string; title: string; body?: string }> || [];
  const capabilities = topic.capabilities as Array<{ icon?: string; title: string; body?: string }> || [];
  const lanes = topic.lanes as Array<{ title: string; persona?: string; steps?: string[] }> || [];

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}10,transparent 70%)`, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, maxWidth: 940, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />

        <div style={{ opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(24px)", transition: "all 0.5s cubic-bezier(0.22,1,0.36,1)" }}>

          {/* Header */}
          {topic.eyebrow && (
            <div style={{ fontSize: 9, textTransform: "uppercase", letterSpacing: 2, color: T.accent, marginBottom: 6 }}>
              {topic.eyebrow as string}
            </div>
          )}
          <h1 style={{ fontSize: 28, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.text, lineHeight: 1.05, margin: "0 0 4px" }}>
            {topic.title}
          </h1>
          {topic.subtitle && (
            <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.45, marginTop: 4, marginBottom: 10 }}>
              {topic.subtitle}
            </p>
          )}

          {/* Hero points pills */}
          {heroPoints.length > 0 && (
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 12 }}>
              {heroPoints.map((pt, i) => (
                <span key={i} style={{ display: "inline-flex", alignItems: "center", border: `1px solid ${topic.color}40`, borderRadius: 999, padding: "3px 10px", fontSize: 10, color: topic.color }}>
                  {pt}
                </span>
              ))}
            </div>
          )}

          {/* Focus panels */}
          {focusPanels.length > 0 && (
            <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr" : "repeat(3, 1fr)", gap: 8, marginTop: 16 }}>
              {focusPanels.map((fp, i) => (
                <div
                  key={i}
                  style={{
                    background: T.bgCard,
                    borderRadius: 10,
                    padding: 14,
                    borderTop: `${C.accentBarHeight}px solid ${T.accent}`,
                    opacity: entered ? 1 : 0,
                    transform: entered ? "none" : "translateY(12px)",
                    transition: `all 0.5s ${0.15 + i * 0.06}s cubic-bezier(0.22,1,0.36,1)`,
                  }}
                >
                  {fp.label && (
                    <div style={{ fontSize: 9, textTransform: "uppercase", letterSpacing: 1.5, color: T.textDim, marginBottom: 4 }}>
                      {fp.label}
                    </div>
                  )}
                  <h4 style={{ fontSize: 13, fontWeight: 600, color: T.text, margin: 0 }}>
                    {fp.title}
                  </h4>
                  {fp.body && (
                    <p style={{ fontSize: 11, color: T.textMuted, lineHeight: 1.35, marginTop: 4, marginBottom: 0 }}>
                      {fp.body}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Capabilities — 4-column grid, always visible */}
          {capabilities.length > 0 && (
            <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr 1fr" : "repeat(4, 1fr)", gap: 8, marginTop: 16 }}>
              {capabilities.map((cap, i) => (
                <div
                  key={i}
                  style={{
                    background: T.bgCard,
                    borderRadius: 8,
                    padding: 10,
                    opacity: entered ? 1 : 0,
                    transform: entered ? "none" : "translateY(10px)",
                    transition: `all 0.5s ${0.2 + i * 0.04}s cubic-bezier(0.22,1,0.36,1)`,
                  }}
                >
                  {cap.icon && (
                    <div style={{ fontSize: 16, marginBottom: 4 }}>{cap.icon}</div>
                  )}
                  <div style={{ fontSize: 11.5, fontWeight: 600, color: T.text }}>{cap.title}</div>
                  {cap.body && (
                    <p style={{ fontSize: 10, color: T.textMuted, lineHeight: 1.3, marginTop: 3, marginBottom: 0 }}>
                      {cap.body}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Lanes — flat list, no accordion */}
          {lanes.length > 0 && (
            <div style={{ marginTop: 16 }}>
              {lanes.map((lane, i) => {
                const steps = lane.steps || [];
                return (
                  <div
                    key={i}
                    style={{
                      marginBottom: 12,
                      background: T.bgCard,
                      borderRadius: 10,
                      padding: 14,
                      opacity: entered ? 1 : 0,
                      transform: entered ? "none" : "translateY(10px)",
                      transition: `all 0.5s ${0.3 + i * 0.08}s cubic-bezier(0.22,1,0.36,1)`,
                    }}
                  >
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                      <span style={{ fontSize: 12, fontWeight: 600, color: T.text }}>{lane.title}</span>
                      {lane.persona && (
                        <span style={{ fontSize: 9, color: T.accent, background: `${T.accent}10`, borderRadius: 999, padding: "1px 8px" }}>
                          {lane.persona}
                        </span>
                      )}
                    </div>
                    {steps.length > 0 && (
                      <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                        {steps.map((step, si) => (
                          <span key={si} style={{ display: "inline-flex", fontSize: 9, borderRadius: 999, padding: "2px 8px", background: `${T.accent}10`, color: T.textMuted }}>
                            {step}
                          </span>
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
              marginTop: 14,
              borderLeft: `${C.accentBarHeight}px solid ${T.accent}`,
              background: T.bgCard,
              padding: 12,
              borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0`,
            }}>
              <p style={{ fontSize: 12, color: T.text, lineHeight: 1.45, margin: 0, fontWeight: 600 }}>
                &ldquo;{topic.callout}&rdquo;
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AdvdPlatformLayout;
