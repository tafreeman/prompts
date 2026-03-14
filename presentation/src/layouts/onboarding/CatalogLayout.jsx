/**
 * CatalogLayout — color-coded category catalog screen.
 *
 * Extracted from genai_advocacy_hub_13.jsx (CatalogScreen, layout id: "catalog").
 */

import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { useTheme } from "../../components/hooks/useTheme.js";
import { useChrome } from "../../components/hooks/useChrome.js";
import BackBtn from "../../components/navigation/BackBtn.jsx";
import SectionHeader from "../../components/compound/SectionHeader.jsx";
import Particles from "../../components/animations/Particles.jsx";

export function CatalogLayout({ topic, onBack }) {
  const T = useTheme();
  const C = useChrome();
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), 60); return () => clearTimeout(t); }, []);
  return (
    <div style={{ position: "relative", minHeight: "100vh", background: T.bg, overflow: "hidden" }}>
      <Particles color={topic.color} active={entered} />
      <div style={{ position: "relative", zIndex: 2, maxWidth: 1100, margin: "0 auto", padding: "36px 32px" }}>
        <BackBtn onClick={onBack} />
        <SectionHeader topic={topic} entered={entered} />
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${Math.min((topic.categories || []).length, 4)}, 1fr)`, gap: 16 }}>
          {(topic.categories || []).map((cat, ci) => (
            <div key={ci} style={{ background: T.bgCard, borderRadius: C.cardRadius, padding: "20px 18px", borderTop: `${C.accentBarHeight}px solid ${cat.color}`, opacity: entered ? 1 : 0, transform: entered ? "none" : "translateY(16px)", transition: `all 0.5s ${0.15 + ci * 0.12}s ease` }}>
              <h3 style={{ fontFamily: T.fontDisplay, fontSize: 14, fontWeight: C.headingWeight, color: cat.color, margin: "0 0 16px" }}>{cat.title}</h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {cat.items.map((item, i) => (
                  <div key={i} style={{ padding: "10px 12px", borderRadius: C.innerRadius, background: T.bgDeep, borderLeft: `${C.accentBarHeight}px solid ${cat.color}40` }}>
                    <div style={{ fontFamily: T.fontDisplay, fontSize: 12, fontWeight: C.headingWeight, color: T.text, marginBottom: 3 }}>{item.label}</div>
                    <p style={{ fontSize: 11.5, color: T.textMuted, lineHeight: 1.5, margin: 0 }}>{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 28, padding: "18px 22px", borderLeft: `${C.accentBarHeight}px solid ${T.accent}`, background: T.bgCard, borderRadius: `0 ${C.innerRadius}px ${C.innerRadius}px 0` }}>
          <p style={{ fontSize: 14, color: T.text, lineHeight: 1.65, margin: 0, fontWeight: 600 }}>&ldquo;{topic.callout}&rdquo;</p>
        </div>
      </div>
    </div>
  );
}
CatalogLayout.propTypes = { topic: PropTypes.object.isRequired, onBack: PropTypes.func.isRequired };

export default CatalogLayout;
