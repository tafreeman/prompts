import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { StepsSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Body } from '../../components/primitives/Body.js';
import { Eyebrow } from '../../components/primitives/Eyebrow.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { CalloutBox } from '../../components/primitives/CalloutBox.js';
import { SPACING } from '../../tokens/spacing.js';

type StepsData = z.infer<typeof StepsSlide>;

/** Circle diameter for step numbers. */
const CIRCLE_SIZE = 36;

/**
 * Steps layout -- horizontal process flow with numbered circles.
 *
 * Design guide: each step shows a numbered circle connected by a line,
 * with a label and optional description below. If more than 5 steps,
 * font sizes reduce to fit.
 */
export function StepsLayout({ slide }: LayoutProps) {
  const data = slide as StepsData;
  const theme = useTheme();
  const compact = data.steps.length > 5;

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    gap: SPACING.md,
  };

  const flowStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'flex-start',
    gap: 0,
    flex: 1,
    alignContent: 'center',
  };

  const stepStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    flex: 1,
    gap: SPACING.xs,
    textAlign: 'center',
  };

  const circleStyle: CSSProperties = {
    width: CIRCLE_SIZE,
    height: CIRCLE_SIZE,
    borderRadius: '50%',
    backgroundColor: theme.accent,
    color: theme.bg,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 700,
    fontSize: compact ? 14 : 16,
    flexShrink: 0,
  };

  const lineStyle: CSSProperties = {
    height: 2,
    backgroundColor: theme.accent,
    opacity: 0.4,
    flex: 1,
    alignSelf: 'center',
    marginTop: CIRCLE_SIZE / 2,
  };

  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: SPACING.xs }}>
        {data.eyebrow && <Eyebrow>{data.eyebrow}</Eyebrow>}
        <Heading level="TITLE">{data.title}</Heading>
        <AccentBar width="80px" />
      </div>

      {/* Step flow */}
      <div style={flowStyle}>
        {data.steps.map((step, i) => (
          <div key={i} style={{ display: 'contents' }}>
            {/* Connecting line before step (skip first) */}
            {i > 0 && <div style={lineStyle} aria-hidden="true" />}

            {/* Step column */}
            <div style={stepStyle}>
              <div style={circleStyle}>{i + 1}</div>
              <Heading level="CARD" align="center">{step.label}</Heading>
              {step.description && (
                <Body muted size={compact ? 'CAPTION' : 'BODY'} align="center">
                  {step.description}
                </Body>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      {data.callout && <CalloutBox>{data.callout}</CalloutBox>}
    </div>
  );
}
