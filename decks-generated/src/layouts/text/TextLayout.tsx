import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { TextSlide } from '../../schemas/slide.js';
import { Heading } from '../../components/primitives/Heading.js';
import { Body } from '../../components/primitives/Body.js';
import { Eyebrow } from '../../components/primitives/Eyebrow.js';
import { AccentBar } from '../../components/primitives/AccentBar.js';
import { BulletList } from '../../components/primitives/BulletList.js';
import { CalloutBox } from '../../components/primitives/CalloutBox.js';
import { SourceLine } from '../../components/primitives/SourceLine.js';
import { SPACING } from '../../tokens/spacing.js';

type TextData = z.infer<typeof TextSlide>;

/**
 * Text layout — the assertion-evidence workhorse.
 *
 * Design guide: title states a conclusion (assertion), body provides
 * evidence. Supports single-column (body + bullets) or two-column
 * (left/right comparison or text + image).
 */
export function TextLayout({ slide }: LayoutProps) {
  const data = slide as TextData;
  const isTwoCol = data.columns === '2';

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    gap: SPACING.md,
  };

  const contentStyle: CSSProperties = {
    flex: 1,
    display: 'flex',
    flexDirection: isTwoCol ? 'row' : 'column',
    gap: SPACING.lg,
  };

  const columnStyle: CSSProperties = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    gap: SPACING.sm,
  };

  return (
    <div style={containerStyle}>
      {/* Header area */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: SPACING.xs }}>
        {data.eyebrow && <Eyebrow>{data.eyebrow}</Eyebrow>}
        <Heading level="TITLE">{data.title}</Heading>
        <AccentBar width="80px" />
      </div>

      {/* Content area */}
      <div style={contentStyle}>
        {isTwoCol ? (
          <>
            {/* Two-column mode */}
            <div style={columnStyle}>
              {data.leftColumn?.title && (
                <Heading level="CARD">{data.leftColumn.title}</Heading>
              )}
              {data.leftColumn?.body && <Body>{data.leftColumn.body}</Body>}
              {data.leftColumn?.bullets && (
                <BulletList items={data.leftColumn.bullets} />
              )}
            </div>
            <div style={columnStyle}>
              {data.rightColumn?.title && (
                <Heading level="CARD">{data.rightColumn.title}</Heading>
              )}
              {data.rightColumn?.body && <Body>{data.rightColumn.body}</Body>}
              {data.rightColumn?.bullets && (
                <BulletList items={data.rightColumn.bullets} />
              )}
            </div>
          </>
        ) : (
          <>
            {/* Single-column mode */}
            {data.body && <Body>{data.body}</Body>}
            {data.bullets && <BulletList items={data.bullets} />}
            {data.image && (
              <img
                src={data.image}
                alt={data.imageAlt ?? ''}
                style={{
                  maxWidth: '100%',
                  maxHeight: 400,
                  borderRadius: 8,
                  objectFit: 'contain',
                }}
              />
            )}
          </>
        )}
      </div>

      {/* Footer area */}
      {data.callout && <CalloutBox>{data.callout}</CalloutBox>}
      {data.source && <SourceLine source={data.source} />}
    </div>
  );
}
