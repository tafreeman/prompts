/**
 * InfoCardsLayout — onboarding stat-cards screen.
 *
 * Extracted from genai_advocacy_hub_13.jsx (InfoCardsScreen, layout id: "info-cards").
 */

import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { useTheme } from "../../components/hooks/useTheme.js";
import { useChrome } from "../../components/hooks/useChrome.js";
import BackBtn from "../../components/navigation/BackBtn.jsx";
import SectionHeader from "../../components/compound/SectionHeader.jsx";
import Particles from "../../components/animations/Particles.jsx";

export function InfoCardsLayout({ topic, onBack }) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);
  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "absolute", top: 0, right: 0, width: "40%", height: "50%", background: `radial-gradient(ellipse at top right,${topic.color}10,transparent 70%)`, pointerEvents: "none" }} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 900, margin: "0 auto", padding: "36px 32px" }}>
        <BackBtn onClick={onBack} />
        <div style={{ opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(28px)", transition: "all 0.8s cubic-bezier(0.22,1,0.36,1)" }}>
          <SectionHeader topic={topic} entered={entered} />
          {topic.banner && (
            <div style={{ background: T.accent + "0C", border: `1px solid ${T.accent}22`, borderLeft: `${C.accentBarHeight}px solid ${T.accent}`, borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0`, padding: "14px 20px", marginBottom: 24 }}>
              <p style={{ fontSize: 14, color: T.textMuted, lineHeight: 1.65, margin: 0 }}>{topic.banner}</p>
            </div>
          )}
          {(topic.cards || []).map((c, i) => (
            <div key={i} style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "22px 26px", marginBottom: 14, display: "flex", alignItems: "flex-start", gap: 20, borderLeft: `${C.accentBarHeight}px solid ${T.accent}`, opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(16px)", transition: `all 0.5s ${0.2 + i * 0.1}s cubic-bezier(0.22,1,0.36,1)` }}>
              <div style={{ flexShrink: 0, textAlign: "center", minWidth: 60 }}>
                {c.stat && <div style={{ fontFamily: T.fontDisplay, fontSize: 26, fontWeight: C.headingWeight, color: T.accent, lineHeight: 1 }}>{c.stat}</div>}
                {c.statLabel && <div style={{ fontSize: 9, color: T.textDim, textTransform: "uppercase", letterSpacing: 1, marginTop: 3 }}>{c.statLabel}</div>}
              </div>
              <div>
                <h3 style={{ fontFamily: T.fontDisplay, fontSize: 16, fontWeight: C.headingWeight, color: T.text, margin: "0 0 6px" }}>{c.title}</h3>
                <p style={{ fontSize: 13.5, color: T.textMuted, lineHeight: 1.6, margin: 0 }}>{c.body}</p>
              </div>
            </div>
          ))}
          <div style={{ marginTop: 28, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${T.accent}`, background: T.bgCard, borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0` }}>
            <p style={{ fontSize: 14, color: T.text, lineHeight: 1.65, margin: 0, fontWeight: 600 }}>&ldquo;{topic.callout}&rdquo;</p>
          </div>
        </div>
      </div>
    </div>
  );
}
InfoCardsLayout.propTypes = { topic: PropTypes.object.isRequired, onBack: PropTypes.func.isRequired };

export default InfoCardsLayout;
