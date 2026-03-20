import { useRef, useState, useEffect, type ReactNode } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { SLIDE_PADDING } from '../../tokens/spacing.js';

/** Logical slide dimensions (2x of 960x540 for crisp text). */
const LOGICAL_W = 1920;
const LOGICAL_H = 1080;

/** DPI used for the logical 1920x1080 space (2x of 96dpi). */
const DPI = 192;

interface SlideContainerProps {
  readonly children: ReactNode;
  /** Per-slide background color override from the manifest. */
  readonly bgOverride?: string;
}

/**
 * 16:9 viewport wrapper that scales slides to fit the browser window.
 *
 * Renders content at 1920x1080 logical pixels and uses CSS `scale()`
 * transform to fit within the available viewport. A ResizeObserver
 * recalculates the scale factor on window resize.
 */
export function SlideContainer({ children, bgOverride }: SlideContainerProps) {
  const theme = useTheme();
  const wrapperRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);

  useEffect(() => {
    const wrapper = wrapperRef.current;
    if (!wrapper) return;

    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        const next = Math.min(width / LOGICAL_W, height / LOGICAL_H);
        setScale(next);
      }
    });

    observer.observe(wrapper);
    return () => observer.disconnect();
  }, []);

  // Convert SLIDE_PADDING from inches to px at 192dpi for the logical space.
  const padTop = SLIDE_PADDING.top * DPI;
  const padRight = SLIDE_PADDING.right * DPI;
  const padBottom = SLIDE_PADDING.bottom * DPI;
  const padLeft = SLIDE_PADDING.left * DPI;

  const bg = bgOverride ?? theme.bg;

  return (
    <div
      ref={wrapperRef}
      style={{
        width: '100vw',
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
        background: '#000',
      }}
    >
      <div
        style={{
          width: LOGICAL_W,
          height: LOGICAL_H,
          minWidth: LOGICAL_W,
          minHeight: LOGICAL_H,
          flexShrink: 0,
          transform: `scale(${scale})`,
          transformOrigin: 'center center',
          background: bg,
          padding: `${padTop}px ${padRight}px ${padBottom}px ${padLeft}px`,
          position: 'relative',
          overflow: 'hidden',
          fontFamily: `"${theme.fontBody}", system-ui, sans-serif`,
          color: theme.text,
          boxSizing: 'border-box',
        }}
      >
        {children}
      </div>
    </div>
  );
}
