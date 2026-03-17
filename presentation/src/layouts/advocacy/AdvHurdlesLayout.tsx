/**
 * AdvHurdlesLayout — timeline with challenge/resolution rows.
 *
 * Ported from v10.0 HurdlesScreen into the v14 registry-based system.
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

export function AdvHurdlesLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const cards = topic.cards as Array<{ title: string; challenge?: string; fix?: string }> || [];

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} active={entered} type="hurdles" />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}10,transparent 70%)`, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, maxWidth: 900, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />

        <div style={{ opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(28px)", transition: "all 0.8s cubic-bezier(0.22,1,0.36,1)" }}>
          <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr" : "1fr 300px", gap: 28 }}>

            {/* LEFT column — Timeline */}
            <div>
              <h1 style={{ fontSize: 34, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.text, margin: "0 0 8px" }}>
                {topic.title}
              </h1>
              {topic.subtitle && (
                <p style={{ fontSize: 15, color: T.textMuted, lineHeight: 1.65, marginTop: 0, marginBottom: 24 }}>
                  {topic.subtitle}
                </p>
              )}

              {cards.map((c, i) => (
                <div
                  key={i}
                  style={{
                    display: "flex",
                    gap: 14,
                    alignItems: "flex-start",
                    marginBottom: 20,
                    opacity: entered ? 1 : 0,
                    transform: entered ? "none" : "translateX(-60px)",
                    transition: `all 0.5s ${0.2 + i * 0.12}s cubic-bezier(0.22,1,0.36,1)`,
                  }}
                >
                  <div style={{
                    width: 30,
                    height: 30,
                    borderRadius: 6,
                    background: `${T.accent}15`,
                    color: T.accent,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 14,
                    fontWeight: 700,
                    flexShrink: 0,
                  }}>
                    {i + 1}
                  </div>

                  <div>
                    <div style={{ fontSize: 15, fontWeight: 600, color: T.text }}>{c.title}</div>

                    {c.challenge && (
                      <>
                        <div style={{ fontSize: 10, color: "#ef4444", textTransform: "uppercase", letterSpacing: 1, marginTop: 8 }}>
                          Challenge
                        </div>
                        <p style={{ fontSize: 12.5, color: T.textMuted, lineHeight: 1.5, margin: "4px 0 0" }}>
                          {c.challenge}
                        </p>
                      </>
                    )}

                    {c.fix && (
                      <>
                        <div style={{ fontSize: 10, color: "#22c55e", textTransform: "uppercase", letterSpacing: 1, marginTop: 8 }}>
                          Resolution
                        </div>
                        <p style={{ fontSize: 12.5, color: T.textMuted, lineHeight: 1.5, margin: "4px 0 0" }}>
                          {c.fix}
                        </p>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* RIGHT column */}
            <div style={{ position: "relative" }}>
              <div style={{
                position: "absolute",
                width: 200,
                height: 600,
                transform: "rotate(35deg)",
                background: `${topic.color}08`,
                top: -50,
                right: -40,
                pointerEvents: "none",
                borderRadius: 20,
              }} />

              {topic.callout && (
                <div style={{
                  position: "relative",
                  borderLeft: `${C.accentBarHeight}px solid ${T.accent}`,
                  background: T.bgCard,
                  padding: 20,
                  borderRadius: `0 ${C.cardRadius}px ${C.cardRadius}px 0`,
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

export default AdvHurdlesLayout;
