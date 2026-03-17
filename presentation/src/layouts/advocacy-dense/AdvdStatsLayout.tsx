/**
 * AdvdStatsLayout — Dense stats/human screen with always-expanded icon cards.
 *
 * Ported from v10.2 information-dense HumanScreen into the v14 registry system.
 * Cards are always expanded (no toggle), icons displayed instead of marker badges.
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

export function AdvdStatsLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const cards = topic.cards as Array<{ icon?: string; marker?: string; step?: string; stat?: string; eyebrow?: string; statLabel?: string; title?: string; body?: string }> || [];
  const leadershipPoints = topic.leadershipPoints as string[] || [];

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}10,transparent 70%)`, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, maxWidth: 900, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />

        <div style={{ opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(24px)", transition: "all 0.5s cubic-bezier(0.22,1,0.36,1)" }}>
          {/* Header */}
          <h1 style={{ fontSize: 28, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.text, lineHeight: 1.05, margin: "0 0 6px" }}>
            {topic.title}
          </h1>
          {topic.subtitle && (
            <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.45, marginTop: 4, marginBottom: 14 }}>
              {topic.subtitle}
            </p>
          )}
          {topic.thesis && (
            <div style={{ background: `${T.accent}08`, border: `1px solid ${T.accent}20`, borderRadius: 10, padding: "10px 14px", marginBottom: 14 }}>
              <p style={{ fontSize: 12, color: T.text, lineHeight: 1.4, margin: 0, fontStyle: "italic" }}>
                {topic.thesis as string}
              </p>
            </div>
          )}

          {/* Card grid — always expanded */}
          <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr 1fr" : "repeat(auto-fill, minmax(180px, 1fr))", gap: 8 }}>
            {cards.map((c, i) => (
              <div
                key={i}
                style={{
                  background: T.bgCard,
                  borderRadius: 10,
                  padding: 14,
                  opacity: entered ? 1 : 0,
                  transform: entered ? "none" : "translateY(14px)",
                  transition: `all 0.5s ${0.1 + i * 0.06}s cubic-bezier(0.22,1,0.36,1)`,
                }}
              >
                {/* Icon (emoji) instead of marker badge */}
                {(c.icon || c.marker) && (
                  <div style={{ fontSize: 22, marginBottom: 4 }}>
                    {c.icon || c.marker}
                  </div>
                )}

                {/* Stat value */}
                {(c.step || c.stat) && (
                  <div style={{ fontSize: 26, fontWeight: 700, color: T.accent, fontFamily: T.fontDisplay }}>
                    {c.step || c.stat}
                  </div>
                )}

                {/* Stat label */}
                {(c.eyebrow || c.statLabel) && (
                  <div style={{ fontSize: 8, textTransform: "uppercase", letterSpacing: 1, color: T.textDim, marginTop: 2 }}>
                    {c.eyebrow || c.statLabel}
                  </div>
                )}

                {/* Title */}
                {c.title && (
                  <h4 style={{ fontSize: 12, fontWeight: 600, color: T.text, marginTop: 6, marginBottom: 0 }}>
                    {c.title}
                  </h4>
                )}

                {/* Body — always visible */}
                {c.body && (
                  <p style={{ fontSize: 11, color: T.textMuted, lineHeight: 1.35, marginTop: 4, marginBottom: 0 }}>
                    {c.body}
                  </p>
                )}
              </div>
            ))}
          </div>

          {/* Leadership points */}
          {leadershipPoints.length > 0 && (
            <div style={{ marginTop: 14 }}>
              {leadershipPoints.map((lp, i) => (
                <p key={i} style={{ fontSize: 11.5, color: T.textMuted, margin: "3px 0", lineHeight: 1.35 }}>
                  &bull;&ensp;{lp}
                </p>
              ))}
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

export default AdvdStatsLayout;
