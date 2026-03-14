/**
 * StatCard — a card displaying a stat number, label, and optional body text.
 *
 * Based on the stat-card pattern from HumanScreen in the monolith
 * (genai_advocacy_hub_13.jsx ~lines 1156-1187).
 *
 * @example
 *   <StatCard
 *     title="Prompt Templates"
 *     stat="24"
 *     statLabel="active"
 *     body="Versioned prompt templates with embedded architecture context."
 *     size="md"
 *   />
 */

import React from "react";
import PropTypes from "prop-types";

import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";
import { SIZE_TO_SPACING } from "../../tokens/spacing.ts";

/* ── micro sub-components (inlined until micro/ is populated) ── */

/**
 * Eyebrow — small uppercase label above card content.
 */
function Eyebrow({ text, color, fontFamily, letterSpacing }) {
  return (
    <div
      style={{
        fontFamily,
        fontSize: 10,
        fontWeight: 700,
        color,
        textTransform: "uppercase",
        letterSpacing: letterSpacing ?? 1,
        marginTop: 2,
      }}
    >
      {text}
    </div>
  );
}

Eyebrow.propTypes = {
  text: PropTypes.string.isRequired,
  color: PropTypes.string.isRequired,
  fontFamily: PropTypes.string,
  letterSpacing: PropTypes.number,
};

/**
 * StatValue — large numeric/stat display.
 */
function StatValue({ value, color, fontFamily, fontWeight }) {
  return (
    <div
      style={{
        fontFamily,
        fontSize: 32,
        fontWeight: fontWeight ?? 700,
        color,
        lineHeight: 1,
      }}
    >
      {value}
    </div>
  );
}

StatValue.propTypes = {
  value: PropTypes.string.isRequired,
  color: PropTypes.string.isRequired,
  fontFamily: PropTypes.string,
  fontWeight: PropTypes.number,
};

/* ── main component ── */

/**
 * @param {object} props
 * @param {string} props.title — card heading
 * @param {string} props.stat — large stat value (e.g. "24", "98%")
 * @param {string} props.statLabel — small label beneath the stat
 * @param {string} [props.body] — optional body paragraph
 * @param {boolean} [props.expandable=false] — reserved for future expand behaviour
 * @param {string} [props.color] — accent colour override
 * @param {'sm'|'md'|'lg'} [props.size='md'] — card size preset
 */
function StatCard({
  title,
  stat,
  statLabel,
  body,
  expandable = false,
  color,
  size = "md",
}) {
  const T = useTheme();
  const C = useChrome();

  const accent = color || T.text;
  const minHeight = SIZE_TO_SPACING[size] * 6;

  return (
    <div
      style={{
        background: T.bgCard,
        borderRadius: C.innerRadius,
        padding: "28px 32px",
        display: "flex",
        alignItems: "flex-start",
        gap: 24,
        borderLeft: `${C.accentBarHeight + 1}px solid ${accent}`,
        minHeight,
      }}
    >
      {/* Stat column */}
      <div style={{ flexShrink: 0, textAlign: "center", minWidth: 72 }}>
        <StatValue
          value={stat}
          color={color ? `${color}` : T.textDim}
          fontFamily={T.fontDisplay}
          fontWeight={C.headingWeight}
        />
        <Eyebrow
          text={statLabel}
          color={T.textDim}
          fontFamily={T.fontDisplay}
        />
      </div>

      {/* Content column */}
      <div>
        <h3
          style={{
            fontFamily: T.fontDisplay,
            fontSize: 18,
            fontWeight: C.headingWeight,
            color: accent,
            margin: "0 0 8px",
          }}
        >
          {title}
        </h3>
        {body && (
          <p
            style={{
              fontSize: 14,
              color: T.textMuted,
              lineHeight: 1.6,
              margin: 0,
            }}
          >
            {body}
          </p>
        )}
      </div>
    </div>
  );
}

StatCard.propTypes = {
  title: PropTypes.string.isRequired,
  stat: PropTypes.string.isRequired,
  statLabel: PropTypes.string.isRequired,
  body: PropTypes.string,
  expandable: PropTypes.bool,
  color: PropTypes.string,
  size: PropTypes.oneOf(["sm", "md", "lg"]),
};

export default StatCard;
