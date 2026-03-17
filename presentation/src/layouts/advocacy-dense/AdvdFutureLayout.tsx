/**
 * AdvdFutureLayout — Dense future/vision screen with compact horizontal card strip.
 *
 * Ported from v10.2 information-dense FutureScreen into the v14 registry system.
 * Smaller pull-quote, tighter card spacing, shorter animation durations.
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

export function AdvdFutureLayout({ topic, onBack }: LayoutProps) {
  const T = useTheme();
  const C = useChrome();
  const viewport = usePresentationViewport();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);

  const cards = topic.cards as Array<{ eyebrow?: string; title: string; body?: string }> || [];

  return (
    <div style={{ position: "relative", minHeight: "100dvh", background: T.bg, overflowX: "hidden", overflowY: viewport.overlayScroll }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}10,transparent 70%)`, pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 2, maxWidth: 940, margin: "0 auto", padding: `${viewport.pagePaddingTop}px ${viewport.pagePaddingX}px ${viewport.pagePaddingBottom}px` }}>
        <BackBtn onClick={onBack} />

        <div style={{ opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(24px)", transition: "all 0.5s cubic-bezier(0.22,1,0.36,1)" }}>

          {/* Pull-quote */}
          {topic.pullQuote && (
            <div style={{ textAlign: "center", marginBottom: 20 }}>
              <span style={{ fontSize: 140, lineHeight: 0.6, color: `${T.accent}15`, fontFamily: T.fontDisplay, userSelect: "none" }}>&ldquo;</span>
              <p style={{ fontSize: 16, color: T.text, lineHeight: 1.45, maxWidth: 600, margin: "-40px auto 0", fontWeight: 600, fontFamily: T.fontDisplay }}>
                {topic.pullQuote as string}
              </p>
            </div>
          )}

          {/* Title */}
          <h1 style={{ fontSize: 26, fontFamily: T.fontDisplay, fontWeight: C.headingWeight, color: T.text, lineHeight: 1.05, margin: "0 0 4px" }}>
            {topic.title}
          </h1>
          {topic.subtitle && (
            <p style={{ fontSize: 12, color: T.textMuted, lineHeight: 1.45, marginTop: 4, marginBottom: 16 }}>
              {topic.subtitle}
            </p>
          )}

          {/* Card strip */}
          <div style={{ display: "flex", gap: 10, flexDirection: viewport.isPhone ? "column" : "row" }}>
            {cards.map((c, i) => (
              <div
                key={i}
                style={{
                  flex: 1,
                  background: T.bgCard,
                  borderRadius: 10,
                  padding: 14,
                  borderTop: i % 2 === 0
                    ? `${C.accentBarHeight}px solid ${T.accent}`
                    : "none",
                  borderBottom: i % 2 !== 0
                    ? `${C.accentBarHeight}px solid ${T.accent}`
                    : "none",
                  opacity: entered ? 1 : 0,
                  transform: entered ? "none" : "translateY(12px)",
                  transition: `all 0.5s ${0.2 + i * 0.1}s cubic-bezier(0.22,1,0.36,1)`,
                }}
              >
                {c.eyebrow && (
                  <div style={{ fontSize: 9, textTransform: "uppercase", letterSpacing: 1.5, color: T.textDim, marginBottom: 4 }}>
                    {c.eyebrow}
                  </div>
                )}
                <h4 style={{ fontSize: 13, fontWeight: 600, color: T.text, margin: 0 }}>
                  {c.title}
                </h4>
                {c.body && (
                  <p style={{ fontSize: 11, color: T.textMuted, lineHeight: 1.35, marginTop: 4, marginBottom: 0 }}>
                    {c.body}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdvdFutureLayout;
