import type { CSSProperties, ReactNode } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { useStyle } from '../hooks/useStyle.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';
import { SPACING } from '../../tokens/spacing.js';

export interface CalloutBoxProps {
  readonly children: ReactNode;
  readonly variant?: 'default' | 'success' | 'warning' | 'danger';
}

/**
 * Highlighted text block with left accent border.
 *
 * Used for key insights, takeaways, or emphasized callouts on slides.
 * Variant colors map to theme semantic colors.
 */
export function CalloutBox({ children, variant = 'default' }: CalloutBoxProps) {
  const theme = useTheme();
  const style = useStyle();

  const borderColor = variant === 'success' ? theme.success
    : variant === 'warning' ? theme.warning
    : variant === 'danger' ? theme.danger
    : theme.accent;

  const containerStyle: CSSProperties = {
    borderLeft: `3px solid ${borderColor}`,
    background: theme.surfaceDeep,
    padding: `${SPACING.sm}px ${SPACING.md}px`,
    borderRadius: `0 ${style.innerRadius}px ${style.innerRadius}px 0`,
    fontFamily: theme.fontBody,
    fontSize: TYPE_SCALE.BODY.fontSize,
    lineHeight: TYPE_SCALE.BODY.lineHeight,
    color: theme.text,
  };

  return <div style={containerStyle}>{children}</div>;
}
