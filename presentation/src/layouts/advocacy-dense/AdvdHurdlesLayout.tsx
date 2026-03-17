/**
 * AdvdHurdlesLayout — Dense hurdles/timeline screen with compact rows.
 *
 * Ported from v10.2 information-dense HurdlesScreen into the v14 registry system.
 * Smaller number boxes, tighter gaps, less dramatic entry animation.
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

export function AdvdHurdlesLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const cards = topic.cards as Array<{ title: string; labels?: string[]; challenge?: string; fix?: string }> || [];

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} active={entered} type="hurdles" />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}10,transparent 70%)`, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, maxWidth: 880, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />

        <div style={{ opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(24px)", transition: "all 0.5s cubic-bezier(0.22,1,0.36,1)" }}>
          <div style={{ display: "grid", gridTemplateColumns: viewport.isPhone ? "1fr" : "1fr 260px", gap: 16 }}>

            {/* LEFT — Timeline */}
            <div>
              <h1 style={{ fontSize: 28, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.text, lineHeight: 1.05, margin: "0 0 6px" }}>
                {topic.title}
              </h1>
              {topic.subtitle && (
                <p style={{ fontSize: 13, color: T.textMuted, lineHeight: 1.45, marginTop: 4, marginBottom: 16 }}>
                  {topic.subtitle}
                </p>
              )}

              {cards.map((c, i) => (
                <div
                  key={i}
                  style={{
                    display: "flex",
                    gap: 10,
                    marginBottom: 14,
                    opacity: entered ? 1 : 0,
                    transform: entered ? "none" : "translateX(-40px)",
                    transition: `all 0.5s ${0.15 + i * 0.1}s cubic-bezier(0.22,1,0.36,1)`,
                  }}
                >
                  {/* Number box */}
                  <div style={{
                    width: 24,
                    height: 24,
                    borderRadius: 4,
                    background: `${T.accent}18`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 11,
                    fontWeight: 700,
                    color: T.accent,
                    flexShrink: 0,
                    marginTop: 2,
                  }}>
                    {i + 1}
                  </div>

                  {/* Content */}
                  <div style={{ flex: 1 }}>
                    <h4 style={{ fontSize: 13, fontWeight: 600, color: T.text, margin: 0 }}>
                      {c.title}
                    </h4>
                    {(c.labels || []).length > 0 && (
                      <div style={{ display: "flex", flexWrap: "wrap", gap: 4, marginTop: 4 }}>
                        {(c.labels || []).map((label, li) => (
                          <span key={li} style={{ fontSize: 9, color: T.textDim, background: `${T.accent}10`, borderRadius: 999, padding: "1px 6px" }}>
                            {label}
                          </span>
                        ))}
                      </div>
                    )}
                    {c.challenge && (
                      <p style={{ fontSize: 11, color: T.textMuted, lineHeight: 1.35, marginTop: 4, marginBottom: 0 }}>
                        <strong style={{ color: T.text }}>Challenge:</strong> {c.challenge}
                      </p>
                    )}
                    {c.fix && (
                      <p style={{ fontSize: 11, color: T.textMuted, lineHeight: 1.35, marginTop: 3, marginBottom: 0 }}>
                        <strong style={{ color: T.accent }}>Fix:</strong> {c.fix}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* RIGHT — Callout */}
            <div>
              {topic.callout && (
                <div style={{
                  borderLeft: `${C.accentBarHeight}px solid ${T.accent}`,
                  background: T.bgCard,
                  padding: 16,
                  borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0`,
                }}>
                  <p style={{ fontSize: 11.5, color: T.text, lineHeight: 1.45, margin: 0, fontWeight: 600 }}>
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

export default AdvdHurdlesLayout;
