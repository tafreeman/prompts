/**
 * AdvFutureLayout — horizontal card strip with pull-quote.
 *
 * Ported from v10.0 FutureScreen into the v14 registry-based system.
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

const BORDER_POSITIONS = ["borderLeft", "borderTop", "borderBottom", "borderLeft"] as const;

export function AdvFutureLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const cards = topic.cards as Array<{ title: string; body?: string }> || [];

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}10,transparent 70%)`, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, maxWidth: 960, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />

        <div style={{ opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(28px)", transition: "all 0.8s cubic-bezier(0.22,1,0.36,1)" }}>

          {/* Pull-quote section */}
          <div style={{ position: "relative", padding: "32px 0", marginBottom: 32 }}>
            <span style={{
              position: "absolute",
              top: -20,
              left: -10,
              fontSize: 200,
              opacity: 0.06,
              fontFamily: "serif",
              color: T.accent,
              pointerEvents: "none",
              lineHeight: 1,
            }}>
              &ldquo;
            </span>

            {topic.callout && (
              <p style={{ fontSize: 20, fontStyle: "italic", color: T.text, lineHeight: 1.55, maxWidth: 700, fontFamily: T.fontDisplay, margin: "0 0 16px", position: "relative" }}>
                {topic.callout}
              </p>
            )}

            <h1 style={{ fontSize: 30, fontWeight: C.headingWeight, color: T.text, fontFamily: T.fontDisplay, margin: "0 0 6px", position: "relative" }}>
              {topic.title}
            </h1>

            {topic.subtitle && (
              <p style={{ fontSize: 14, color: T.textMuted, marginTop: 6, marginBottom: 0, position: "relative" }}>
                {topic.subtitle}
              </p>
            )}
          </div>

          {/* Card strip */}
          <div style={{ display: "flex", gap: 14, flexDirection: viewport.isPhone ? "column" : "row" }}>
            {cards.map((c, i) => {
              const borderProp = BORDER_POSITIONS[i % BORDER_POSITIONS.length];
              return (
                <div
                  key={i}
                  style={{
                    flex: 1,
                    background: T.bgCard,
                    borderRadius: C.cardRadius,
                    padding: 20,
                    [borderProp]: `${C.accentBarHeight}px solid ${T.accent}`,
                    opacity: entered ? 1 : 0,
                    transform: entered ? "none" : "translateY(16px)",
                    transition: `all 0.5s ${0.3 + i * 0.12}s cubic-bezier(0.22,1,0.36,1)`,
                  }}
                >
                  <div style={{ fontSize: 10, color: T.accent, letterSpacing: 1, textTransform: "uppercase" }}>
                    {`0${i + 1}`}
                  </div>
                  <h4 style={{ fontSize: 15, fontWeight: 600, color: T.text, marginTop: 8, marginBottom: 0 }}>
                    {c.title}
                  </h4>
                  {c.body && (
                    <p style={{ fontSize: 12.5, color: T.textMuted, lineHeight: 1.55, marginTop: 6, marginBottom: 0 }}>
                      {c.body}
                    </p>
                  )}
                </div>
              );
            })}
          </div>

        </div>
      </div>
    </div>
  );
}

export default AdvFutureLayout;
