import type { CSSProperties } from 'react';
import type { LayoutProps } from '../registry.js';
import type { z } from 'zod';
import type { QuoteSlide } from '../../schemas/slide.js';
import { useTheme } from '../../components/hooks/useTheme.js';
import { SPACING } from '../../tokens/spacing.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';

type QuoteData = z.infer<typeof QuoteSlide>;

/**
 * Pull-quote layout — editorial typographic composition.
 *
 * Design guide: minimal structure with maximum typographic presence.
 * The quote IS the slide; everything else is supporting context.
 * Inspired by WeBrand editorial and Smith & Diction style:
 * large decorative opening mark, oversized quote text, clean attribution.
 */
export function QuoteLayout({ slide }: LayoutProps) {
  const data = slide as QuoteData;
  const theme = useTheme();

  // Outer container — centered column composition
  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    height: '100%',
    gap: 0,
  };

  // Slide title rendered as small uppercase eyebrow label
  const eyebrowStyle: CSSProperties = {
    fontFamily: theme.fontBody,
    fontSize: TYPE_SCALE.EYEBROW.fontSize,
    fontWeight: TYPE_SCALE.EYEBROW.fontWeight,
    letterSpacing: TYPE_SCALE.EYEBROW.letterSpacing,
    lineHeight: TYPE_SCALE.EYEBROW.lineHeight,
    textTransform: 'uppercase',
    color: theme.accent,
    margin: 0,
  };

  // Decorative opening quotation mark — very large, low opacity
  const decorativeMarkStyle: CSSProperties = {
    fontFamily: theme.fontDisplay,
    fontSize: 200,
    fontWeight: 800,
    lineHeight: 0.8,
    color: theme.accent,
    opacity: 0.3,
    userSelect: 'none',
    marginBottom: -SPACING.xl,   // pull quote text up beneath the mark
    display: 'block',
  };

  // Quote body — HERO-sized, bold, display font, full text color
  const quoteTextStyle: CSSProperties = {
    fontFamily: theme.fontDisplay,
    fontSize: TYPE_SCALE.HERO.fontSize,
    fontWeight: TYPE_SCALE.HERO.fontWeight,
    letterSpacing: TYPE_SCALE.HERO.letterSpacing,
    lineHeight: 1.2,
    color: theme.text,
    margin: 0,
    display: 'block',
  };

  // Thin horizontal rule above attribution
  const ruleStyle: CSSProperties = {
    border: 'none',
    borderTop: `1px solid ${theme.textMuted}`,
    opacity: 0.35,
    width: '100%',
    margin: 0,
  };

  // Attribution block — name + role below the rule
  const attributionBlockStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: SPACING.xs / 2,
    marginTop: SPACING.md,
  };

  const attributionNameStyle: CSSProperties = {
    fontFamily: theme.fontDisplay,
    fontSize: TYPE_SCALE.CARD.fontSize,
    fontWeight: TYPE_SCALE.CARD.fontWeight,
    lineHeight: TYPE_SCALE.CARD.lineHeight,
    color: theme.text,
    margin: 0,
  };

  const attributionRoleStyle: CSSProperties = {
    fontFamily: theme.fontBody,
    fontSize: TYPE_SCALE.BODY.fontSize,
    fontWeight: TYPE_SCALE.BODY.fontWeight,
    lineHeight: TYPE_SCALE.BODY.lineHeight,
    color: theme.textMuted,
    margin: 0,
  };

  // Optional logo — bottom-right corner, fixed 40px height
  const logoWrapStyle: CSSProperties = {
    position: 'absolute',
    bottom: SPACING.lg,
    right: SPACING.lg,
  };

  const logoImgStyle: CSSProperties = {
    height: 40,
    width: 'auto',
    objectFit: 'contain',
    opacity: 0.85,
  };

  return (
    <div style={{ position: 'relative', height: '100%' }}>
      <div style={containerStyle}>
        {/* Eyebrow — slide title as category label */}
        <p style={eyebrowStyle}>{data.title}</p>

        {/* Quote block */}
        <div style={{ marginTop: SPACING.md }}>
          {/* Decorative opening mark */}
          <span style={decorativeMarkStyle} aria-hidden="true">&ldquo;</span>

          {/* Quote text */}
          <blockquote style={{ margin: 0, padding: 0 }}>
            <p style={quoteTextStyle}>{data.quote}</p>
          </blockquote>
        </div>

        {/* Attribution block — only shown when name or role provided */}
        {(data.attribution || data.role) && (
          <div style={{ marginTop: SPACING.xl }}>
            <hr style={ruleStyle} />
            <div style={attributionBlockStyle}>
              {data.attribution && (
                <p style={attributionNameStyle}>
                  &mdash;&ensp;{data.attribution}
                </p>
              )}
              {data.role && (
                <p style={attributionRoleStyle}>{data.role}</p>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Optional company logo — bottom-right */}
      {data.logo && (
        <div style={logoWrapStyle}>
          <img
            src={data.logo}
            alt={data.attribution ? `${data.attribution} company logo` : 'Company logo'}
            style={logoImgStyle}
          />
        </div>
      )}
    </div>
  );
}
