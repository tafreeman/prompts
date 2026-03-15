/**
 * ProcessLane — swimlane displaying a persona and numbered steps.
 *
 * Based on the PlatformScreen lanes pattern (monolith ~1115-1129).
 * Each step is rendered as a numbered circle with a text label.
 * Steps may carry a `type` of 'ai' or 'human' for badge coloring.
 *
 * @param props.persona - Short description of the lane's actor/role.
 * @param props.steps - Ordered steps in the lane.
 * @param props.color - Accent color override (defaults to theme accent).
 * @param props.variant - Layout variant.
 */

import React from "react";
import { useTheme } from "../hooks/useTheme.js";
import { useChrome } from "../hooks/useChrome.js";
import type { Theme } from "../../tokens/themes.ts";
import type { StyleMode } from "../../tokens/style-modes.ts";

const AI_COLOR = "#7C3AED";
const HUMAN_COLOR = "#0891B2";

interface ProcessStep {
  label: string;
  description?: string;
  type?: "ai" | "human";
}

interface ProcessLaneProps {
  persona: string;
  steps: ProcessStep[];
  color?: string;
  variant?: "linear" | "circular";
}

export function ProcessLane({ persona, steps, color, variant = "linear" }: ProcessLaneProps): React.ReactElement {
  const T: Theme = useTheme();
  const C: StyleMode = useChrome();
  const accentColor = color || T.accent;

  return (
    <div
      style={{
        background: T.bgCard,
        borderRadius: C.cardRadius,
        padding: "16px 18px",
        borderTop: `${C.accentBarHeight}px solid ${accentColor}`,
      }}
    >
      {/* Lane title */}
      <div
        style={{
          fontSize: 11,
          textTransform: "uppercase",
          letterSpacing: 2.5,
          color: accentColor,
          fontFamily: T.fontDisplay,
          marginBottom: 6,
        }}
      >
        {variant === "circular" ? "Cycle" : "Process"}
      </div>

      {/* Persona */}
      <p style={{ fontSize: 12.5, color: T.textDim, margin: "0 0 12px" }}>
        {persona}
      </p>

      {/* Steps */}
      <div style={{ display: "grid", gap: 8 }}>
        {steps.map((step, stepIndex) => {
          const stepColor =
            step.type === "ai"
              ? AI_COLOR
              : step.type === "human"
                ? HUMAN_COLOR
                : accentColor;

          return (
            <div
              key={`${step.label}-${stepIndex}`}
              style={{
                display: "grid",
                gridTemplateColumns: "24px 1fr",
                gap: 10,
                alignItems: "start",
              }}
            >
              <div
                style={{
                  width: 22,
                  height: 22,
                  borderRadius: "50%",
                  background: `${stepColor}18`,
                  color: stepColor,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 11,
                  fontWeight: 700,
                }}
              >
                {stepIndex + 1}
              </div>
              <div>
                <p
                  style={{
                    fontSize: 13,
                    color: T.textMuted,
                    lineHeight: 1.55,
                    margin: 0,
                  }}
                >
                  {step.label}
                </p>
                {step.description && (
                  <p
                    style={{
                      fontSize: 12,
                      color: T.textDim,
                      lineHeight: 1.5,
                      margin: "4px 0 0",
                    }}
                  >
                    {step.description}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default ProcessLane;
