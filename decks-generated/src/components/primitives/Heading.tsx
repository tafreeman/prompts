import type { CSSProperties, ReactNode } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { useStyle } from '../hooks/useStyle.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';
import type { TypeScaleKey } from '../../tokens/type-scale.js';

type HeadingLevel = Extract<TypeScaleKey, 'HERO' | 'TITLE' | 'SECTION' | 'CARD'>;

export interface HeadingProps {
  /** Type scale level — determines size, weight, and spacing. */
  readonly level: HeadingLevel;
  readonly children: ReactNode;
  /** Override the theme text color. */
  readonly color?: string;
  readonly align?: 'left' | 'center' | 'right';
  /** Semantic HTML tag. Defaults based on level. */
  readonly as?: 'h1' | 'h2' | 'h3' | 'h4';
}

const DEFAULT_TAG: Record<HeadingLevel, 'h1' | 'h2' | 'h3' | 'h4'> = {
  HERO: 'h1',
  TITLE: 'h2',
  SECTION: 'h3',
  CARD: 'h4',
};

/**
 * Type-scale heading component.
 *
 * Reads font from theme (fontDisplay), weight/transform from style mode,
 * and size/spacing from the type scale tokens.
 */
export function Heading({ level, children, color, align = 'left', as }: HeadingProps) {
  const theme = useTheme();
  const style = useStyle();
  const scale = TYPE_SCALE[level];
  const Tag = as ?? DEFAULT_TAG[level];

  const headingStyle: CSSProperties = {
    fontFamily: theme.fontDisplay,
    fontSize: scale.fontSize,
    fontWeight: style.headingWeight,
    letterSpacing: scale.letterSpacing,
    lineHeight: scale.lineHeight,
    textTransform: style.headingTransform,
    color: color ?? theme.text,
    textAlign: align,
    margin: 0,
  };

  return <Tag style={headingStyle}>{children}</Tag>;
}
