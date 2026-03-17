/**
 * AdvOverviewLayout — 2-column overview with hero points and story cards.
 *
 * Ported from v10.0 OverviewScreen into the v14 registry-based system.
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

export function AdvOverviewLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const cards = topic.cards as Array<{ title: string; body?: string }> || [];
  const heroPoints = topic.heroPoints as string[] || [];
  const talkingPoints = topic.talkingPoints as string[] || [];

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}10,transparent 70%)`, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, maxWidth: 960, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />

        <div style={{ opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(28px)", transition: "all 0.8s cubic-bezier(0.22,1,0.36,1)" }}>
          <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr" : "1.1fr 0.9fr", gap: 32 }}>

            {/* LEFT column */}
            <div>
              {topic.eyebrow && (
                <div style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: 2, color: T.accent, marginBottom: 10 }}>
                  {topic.eyebrow as string}
                </div>
              )}
              <h1 style={{ fontSize: 36, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.text, margin: "0 0 8px" }}>
                {topic.title}
              </h1>
              {topic.subtitle && (
                <p style={{ fontSize: 15, color: T.textMuted, lineHeight: 1.65, marginTop: 8, marginBottom: 16 }}>
                  {topic.subtitle}
                </p>
              )}

              {heroPoints.length > 0 && (
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 16 }}>
                  {heroPoints.map((pt, i) => (
                    <span key={i} style={{ display: "inline-flex", alignItems: "center", border: `1px solid ${topic.color}40`, borderRadius: 999, padding: "4px 14px", fontSize: 11, color: topic.color }}>
                      {pt}
                    </span>
                  ))}
                </div>
              )}

              {topic.summary && (
                <p style={{ fontSize: 13.5, color: T.textMuted, lineHeight: 1.6, marginTop: 18, marginBottom: 0 }}>
                  {topic.summary as string}
                </p>
              )}
            </div>

            {/* RIGHT column */}
            <div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                {cards.map((c, i) => (
                  <div
                    key={i}
                    style={{
                      background: T.bgCard,
                      borderRadius: C.cardRadius,
                      padding: 16,
                      borderLeft: `${C.accentBarHeight}px solid ${T.accent}`,
                      opacity: entered ? 1 : 0,
                      transform: entered ? "none" : "translateY(16px)",
                      transition: `all 0.5s ${0.2 + i * 0.08}s cubic-bezier(0.22,1,0.36,1)`,
                    }}
                  >
                    <h4 style={{ fontSize: 14, fontWeight: 600, color: T.text, margin: 0 }}>{c.title}</h4>
                    {c.body && (
                      <p style={{ fontSize: 12.5, color: T.textMuted, marginTop: 6, marginBottom: 0, lineHeight: 1.5 }}>
                        {c.body}
                      </p>
                    )}
                  </div>
                ))}
              </div>

              {talkingPoints.length > 0 && (
                <div style={{ marginTop: 14 }}>
                  {talkingPoints.map((tp, i) => (
                    <p key={i} style={{ fontSize: 12, color: T.textMuted, margin: "4px 0", lineHeight: 1.5 }}>
                      &bull;&ensp;{tp}
                    </p>
                  ))}
                </div>
              )}

              {topic.callout && (
                <div style={{
                  marginTop: 18,
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
      </div>
    </div>
  );
}

export default AdvOverviewLayout;
