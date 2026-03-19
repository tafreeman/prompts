import type { Slide } from '../schemas/slide.js';
import { layoutRegistry } from './registry.js';

interface LayoutRendererProps {
  /** The validated slide to render. */
  readonly slide: Slide;
}

/**
 * Resolves a slide's `layout` field to its registered React component
 * and renders it. Displays a red error box if the layout is not registered.
 */
export function LayoutRenderer({ slide }: LayoutRendererProps) {
  try {
    const Component = layoutRegistry.get(slide.layout);
    return <Component slide={slide} />;
  } catch (error) {
    return (
      <div
        style={{
          padding: 40,
          background: 'rgba(239,68,68,0.08)',
          color: '#EF4444',
          fontFamily: 'monospace',
          fontSize: 14,
          borderRadius: 8,
          margin: 20,
        }}
      >
        <strong>Layout Error: &quot;{slide.layout}&quot;</strong>
        <p style={{ marginTop: 8, opacity: 0.7 }}>
          {(error as Error).message}
        </p>
      </div>
    );
  }
}
