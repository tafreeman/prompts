import { useEffect, useState, useCallback, type CSSProperties } from 'react';
import { useTheme } from '../hooks/useTheme.js';
import { TYPE_SCALE } from '../../tokens/type-scale.js';
import { SPACING } from '../../tokens/spacing.js';

interface SlideNavigatorProps {
  readonly totalSlides: number;
  readonly currentIndex: number;
  readonly onNavigate: (index: number) => void;
}

/**
 * Keyboard navigation + slide counter overlay.
 *
 * Controls:
 *   ←/↑     previous slide
 *   →/↓/Space  next slide
 *   Home     first slide
 *   End      last slide
 *   1-9      jump to slide N
 *
 * Renders a hover-reveal pill at bottom-right showing "3 / 12".
 */
export function SlideNavigator({
  totalSlides,
  currentIndex,
  onNavigate,
}: SlideNavigatorProps) {
  const theme = useTheme();
  const [visible, setVisible] = useState(false);

  const goTo = useCallback(
    (i: number) => {
      const clamped = Math.max(0, Math.min(i, totalSlides - 1));
      onNavigate(clamped);
    },
    [totalSlides, onNavigate],
  );

  // Keyboard handler
  useEffect(() => {
    function handleKey(e: KeyboardEvent) {
      switch (e.key) {
        case 'ArrowRight':
        case 'ArrowDown':
        case ' ':
          e.preventDefault();
          goTo(currentIndex + 1);
          break;
        case 'ArrowLeft':
        case 'ArrowUp':
          e.preventDefault();
          goTo(currentIndex - 1);
          break;
        case 'Home':
          e.preventDefault();
          goTo(0);
          break;
        case 'End':
          e.preventDefault();
          goTo(totalSlides - 1);
          break;
        default:
          // Number keys 1-9
          if (/^[1-9]$/.test(e.key)) {
            e.preventDefault();
            goTo(parseInt(e.key, 10) - 1);
          }
      }
    }

    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [currentIndex, totalSlides, goTo]);

  // Hover-reveal: show on mouse move, fade after 3s
  useEffect(() => {
    let timer: ReturnType<typeof setTimeout>;

    function handleMove() {
      setVisible(true);
      clearTimeout(timer);
      timer = setTimeout(() => setVisible(false), 3000);
    }

    window.addEventListener('mousemove', handleMove);
    return () => {
      window.removeEventListener('mousemove', handleMove);
      clearTimeout(timer);
    };
  }, []);

  const pillStyle: CSSProperties = {
    position: 'fixed',
    bottom: SPACING.md,
    right: SPACING.md,
    display: 'flex',
    alignItems: 'center',
    gap: SPACING.xs,
    background: theme.surface,
    border: `1px solid ${theme.surfaceDeep}`,
    borderRadius: 999,
    padding: `${SPACING.xs}px ${SPACING.sm}px`,
    fontFamily: theme.fontBody,
    fontSize: TYPE_SCALE.CAPTION.fontSize,
    color: theme.textMuted,
    opacity: visible ? 0.9 : 0,
    transition: 'opacity 0.3s ease',
    pointerEvents: visible ? 'auto' : 'none',
    zIndex: 1000,
    userSelect: 'none',
  };

  const btnStyle: CSSProperties = {
    background: 'none',
    border: 'none',
    color: theme.textMuted,
    cursor: 'pointer',
    fontSize: 16,
    padding: '2px 6px',
    borderRadius: 4,
    lineHeight: 1,
  };

  return (
    <div style={pillStyle}>
      <button
        style={btnStyle}
        onClick={() => goTo(currentIndex - 1)}
        disabled={currentIndex === 0}
        aria-label="Previous slide"
      >
        ‹
      </button>
      <span>
        {currentIndex + 1} / {totalSlides}
      </span>
      <button
        style={btnStyle}
        onClick={() => goTo(currentIndex + 1)}
        disabled={currentIndex === totalSlides - 1}
        aria-label="Next slide"
      >
        ›
      </button>
    </div>
  );
}
