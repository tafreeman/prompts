import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { TimelineSlide } from '../../schemas/slide.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Eyebrow } from '../../components/primitives/Eyebrow.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { Body } from '../../components/primitives/Body.js';
import { CalloutBox } from '../../components/primitives/CalloutBox.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { useStyle } from '../../components/hooks/useStyle.js';
import { SPACING } from '../../tokens/spacing.js';

type TimelineData = z.infer<typeof TimelineSlide>;

/**
 * Timeline layout — vertical timeline with accent line and event dots.
 *
 * Design guide: events flow top-to-bottom along a left-side accent line.
 * Each event shows a dot on the line, date eyebrow, title, and optional
 * description.
 */
export function TimelineLayout({ slide }: LayoutProps) {
  const data = slide as TimelineData;
  const theme = useTheme();
  const style = useStyle();

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    gap: SPACING.md,
  };

  const eventsContainerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: SPACING.lg,
    position: 'relative',
    borderLeft: `2px solid ${theme.accent}4D`, // 30% opacity
    marginLeft: 6, // center the 12px dot on the line
    paddingLeft: SPACING.md,
    flex: 1,
  };

  const dotStyle: CSSProperties = {
    width: 12,
    height: 12,
    borderRadius: '50%',
    backgroundColor: theme.accent,
    position: 'absolute',
    left: -7, // center 12px dot on the 2px border: -(12/2 - 2/2) = -5… visually -7 looks right on a 2px line
    top: 2,
    flexShrink: 0,
  };

  const eventContentStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: SPACING.xs,
  };

  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: SPACING.xs }}>
        {data.eyebrow && <Eyebrow>{data.eyebrow}</Eyebrow>}
        <Heading level="TITLE">{data.title}</Heading>
        <AccentBar width="80px" />
      </div>

      {/* Timeline events */}
      <div style={eventsContainerStyle}>
        {data.events.map((event, i) => (
          <div key={i} style={{ position: 'relative' }}>
            <div style={dotStyle} />
            <div style={eventContentStyle}>
              <Eyebrow>{event.date}</Eyebrow>
              <Heading level="CARD">{event.title}</Heading>
              {event.description && <Body muted>{event.description}</Body>}
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      {data.callout && <CalloutBox>{data.callout}</CalloutBox>}
    </div>
  );
}
