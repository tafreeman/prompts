/**
 * AdvStatsLayout — expandable stat cards with markers.
 *
 * Ported from v10.0 HumanScreen into the v14 registry-based system.
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

export function AdvStatsLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState(false);
  const [expandedMap, setExpandedMap] = useState<Record<number, boolean>>({});
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const cards = topic.cards as Array<{ marker?: string; step?: string; stat?: string; eyebrow?: string; statLabel?: string; title: string; body?: string }> || [];
  const leadershipPoints = topic.leadershipPoints as string[] || [];

  const toggleCard = (idx: number) => {
    setExpandedMap((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}10,transparent 70%)`, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, maxWidth: 920, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />

        <div style={{ opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(28px)", transition: "all 0.8s cubic-bezier(0.22,1,0.36,1)" }}>
          <h1 style={{ fontSize: 34, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.text, margin: "0 0 8px" }}>
            {topic.title}
          </h1>
          {topic.subtitle && (
            <p style={{ fontSize: 15, color: T.textMuted, lineHeight: 1.65, marginTop: 0, marginBottom: 16 }}>
              {topic.subtitle}
            </p>
          )}

          {topic.thesis && (
            <div style={{ background: T.accent + "0C", border: `1px solid ${T.accent}22`, borderLeft: `${C.accentBarHeight}px solid ${T.accent}`, borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0`, padding: "14px 20px", marginBottom: 24 }}>
              <p style={{ fontSize: 14, color: T.textMuted, lineHeight: 1.65, margin: 0 }}>{topic.thesis as string}</p>
            </div>
          )}

          <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr" : "repeat(auto-fill, minmax(190px, 1fr))", gap: 12 }}>
            {cards.map((c, i) => {
              const isExpanded = !!expandedMap[i];
              return (
                <button
                  key={i}
                  onClick={() => toggleCard(i)}
                  style={{
                    minHeight: isExpanded ? 260 : 170,
                    background: T.bgCard,
                    borderRadius: C.cardRadius,
                    padding: 18,
                    cursor: "pointer",
                    border: "none",
                    textAlign: "left",
                    position: "relative",
                    opacity: entered ? 1 : 0,
                    transform: entered ? "none" : "translateY(16px)",
                    transition: `all 0.4s ${0.15 + i * 0.08}s cubic-bezier(0.22,1,0.36,1)`,
                  }}
                >
                  {c.marker && (
                    <div style={{
                      fontSize: 14,
                      width: 36,
                      height: 36,
                      borderRadius: "50%",
                      background: `${T.accent}18`,
                      color: T.accent,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontWeight: 700,
                      marginBottom: 10,
                    }}>
                      {c.marker}
                    </div>
                  )}

                  <div style={{ fontFamily: T.fontDisplay, fontSize: 32, fontWeight: 700, color: T.accent, lineHeight: 1.1 }}>
                    {c.step || c.stat}
                  </div>

                  {(c.eyebrow || c.statLabel) && (
                    <div style={{ fontSize: 9, textTransform: "uppercase", letterSpacing: 1, color: T.textDim, marginTop: 4 }}>
                      {c.eyebrow || c.statLabel}
                    </div>
                  )}

                  <div style={{ fontSize: 14, fontWeight: 600, color: T.text, marginTop: 8 }}>
                    {c.title}
                  </div>

                  {isExpanded && c.body && (
                    <p style={{ fontSize: 12.5, color: T.textMuted, lineHeight: 1.5, marginTop: 6, marginBottom: 0 }}>
                      {c.body}
                    </p>
                  )}

                  <div style={{ position: "absolute", bottom: 12, right: 14, fontSize: 14, color: T.textDim, lineHeight: 1 }}>
                    {isExpanded ? "\u2212" : "+"}
                  </div>
                </button>
              );
            })}
          </div>

          {leadershipPoints.length > 0 && (
            <div style={{
              marginTop: 24,
              background: `linear-gradient(135deg, ${T.accent}08, transparent)`,
              borderRadius: C.cardRadius,
              padding: 20,
            }}>
              {leadershipPoints.map((pt, i) => (
                <div key={i} style={{ display: "flex", gap: 12, alignItems: "flex-start", marginBottom: i < leadershipPoints.length - 1 ? 12 : 0 }}>
                  <span style={{ fontSize: 18, fontWeight: 700, color: T.accent, flexShrink: 0, lineHeight: 1.2 }}>
                    {i + 1}
                  </span>
                  <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.55, margin: 0 }}>
                    {pt}
                  </p>
                </div>
              ))}
            </div>
          )}

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

export default AdvStatsLayout;
