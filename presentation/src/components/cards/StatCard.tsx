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

import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";
import { SIZE_TO_SPACING } from "../../tokens/spacing.ts";
import type { Theme } from "../../tokens/themes.ts";
import type { StyleMode } from "../../tokens/style-modes.ts";

/* ── micro sub-components (inlined until micro/ is populated) ── */

interface InlineEyebrowProps {
  text: string;
  color: string;
  fontFamily?: string;
  letterSpacing?: number;
}

/**
 * Eyebrow — small uppercase label above card content.
 */
function Eyebrow({ text, color, fontFamily, letterSpacing }: InlineEyebrowProps): React.ReactElement {
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

interface InlineStatValueProps {
  value: string;
  color: string;
  fontFamily?: string;
  fontWeight?: number;
}

/**
 * StatValue — large numeric/stat display.
 */
function StatValue({ value, color, fontFamily, fontWeight }: InlineStatValueProps): React.ReactElement {
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

/* ── main component ── */

interface StatCardProps {
  /** card heading */
  title: string;
  /** large stat value (e.g. "24", "98%") */
  stat: string;
  /** small label beneath the stat */
  statLabel: string;
  /** optional body paragraph */
  body?: string;
  /** reserved for future expand behaviour */
  expandable?: boolean;
  /** accent colour override */
  color?: string;
  /** card size preset */
  size?: "sm" | "md" | "lg";
}

function StatCard({
  title,
  stat,
  statLabel,
  body,
  expandable = false,
  color,
  size = "md",
}: StatCardProps): React.ReactElement {
  const T: Theme = useTheme();
  const C: StyleMode = useChrome();

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

export default StatCard;
