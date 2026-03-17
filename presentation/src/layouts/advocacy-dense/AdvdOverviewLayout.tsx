/**
 * AdvdOverviewLayout — Dense 2-column overview with Deck Flow widget.
 *
 * Ported from v10.2 information-dense OverviewScreen into the v14 registry system.
 * Tighter typography, reduced gaps, and a compact Deck Flow navigation strip.
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

export function AdvdOverviewLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const cards = topic.cards as Array<{ title: string; body?: string }> || [];
  const heroPoints = topic.heroPoints as string[] || [];
  const allTopics = topic.allTopics as Array<{ color: string; title: string }> || [];

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}10,transparent 70%)`, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, maxWidth: 940, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />

        <div style={{ opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(24px)", transition: "all 0.5s cubic-bezier(0.22,1,0.36,1)" }}>
          <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr" : "1.05fr 0.95fr", gap: 16 }}>

            {/* LEFT column */}
            <div>
              {topic.eyebrow && (
                <div style={{ fontSize: 9, textTransform: "uppercase", letterSpacing: 2, color: T.accent, marginBottom: 8 }}>
                  {topic.eyebrow as string}
                </div>
              )}
              <h1 style={{ fontSize: 30, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.text, lineHeight: 1.05, margin: "0 0 6px" }}>
                {topic.title}
              </h1>
              {topic.subtitle && (
                <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.45, marginTop: 6, marginBottom: 12 }}>
                  {topic.subtitle}
                </p>
              )}

              {heroPoints.length > 0 && (
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 12 }}>
                  {heroPoints.map((pt, i) => (
                    <span key={i} style={{ display: "inline-flex", alignItems: "center", border: `1px solid ${topic.color}40`, borderRadius: 999, padding: "3px 10px", fontSize: 10, color: topic.color }}>
                      {pt}
                    </span>
                  ))}
                </div>
              )}

              {topic.summary && (
                <p style={{ fontSize: 12, color: T.textMuted, lineHeight: 1.45, marginTop: 12, marginBottom: 0 }}>
                  {topic.summary as string}
                </p>
              )}
            </div>

            {/* RIGHT column */}
            <div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                {cards.map((c, i) => (
                  <div
                    key={i}
                    style={{
                      background: T.bgCard,
                      borderRadius: 10,
                      padding: 12,
                      borderLeft: `${C.accentBarHeight}px solid ${T.accent}`,
                      opacity: entered ? 1 : 0,
                      transform: entered ? "none" : "translateY(14px)",
                      transition: `all 0.5s ${0.15 + i * 0.06}s cubic-bezier(0.22,1,0.36,1)`,
                    }}
                  >
                    <h4 style={{ fontSize: 12, fontWeight: 600, color: T.text, margin: 0 }}>{c.title}</h4>
                    {c.body && (
                      <p style={{ fontSize: 11, color: T.textMuted, marginTop: 4, marginBottom: 0, lineHeight: 1.25 }}>
                        {c.body}
                      </p>
                    )}
                  </div>
                ))}
              </div>

              {topic.callout && (
                <div style={{
                  marginTop: 12,
                  borderLeft: `${C.accentBarHeight}px solid ${T.accent}`,
                  background: T.bgCard,
                  padding: 14,
                  borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0`,
                }}>
                  <p style={{ fontSize: 12, color: T.text, lineHeight: 1.45, margin: 0, fontWeight: 600 }}>
                    &ldquo;{topic.callout}&rdquo;
                  </p>
                </div>
              )}
            </div>

          </div>

          {/* Deck Flow widget */}
          {allTopics.length > 0 && (
            <div style={{ marginTop: 16, background: T.bgCard, borderRadius: 10, padding: "10px 14px" }}>
              <div style={{ fontSize: 8, textTransform: "uppercase", letterSpacing: 2, color: T.textDim, marginBottom: 6 }}>
                DECK FLOW
              </div>
              <div style={{ display: "flex", flexWrap: "wrap" }}>
                {allTopics.map((t, i) => (
                  <span key={i} style={{ display: "inline-flex", alignItems: "center", gap: 4, marginRight: 10, marginBottom: 4 }}>
                    <span style={{ width: 6, height: 6, borderRadius: "50%", background: t.color, flexShrink: 0 }} />
                    <span style={{ fontSize: 9, color: T.textDim }}>{t.title}</span>
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AdvdOverviewLayout;
