import type { ComponentType } from 'react';
import type { Slide } from '../schemas/slide.js';

/** Props passed to every layout component. */
export interface LayoutProps {
  /** The validated slide data from the Zod schema. */
  readonly slide: Slide;
}

interface RegistryEntry {
  readonly component: ComponentType<LayoutProps>;
  readonly name: string;
}

/**
 * Singleton registry that maps layout ID strings to React components.
 *
 * Each layout module calls `layoutRegistry.register()` at import time.
 * The LayoutRenderer calls `layoutRegistry.get()` to resolve a slide's
 * `layout` field to the component that renders it.
 */
class LayoutRegistry {
  private readonly entries = new Map<string, RegistryEntry>();

  /** Register a layout component. Called at import time by each layout module. */
  register(
    layoutId: string,
    component: ComponentType<LayoutProps>,
    name: string,
  ): void {
    if (this.entries.has(layoutId)) {
      console.warn(`Layout "${layoutId}" already registered -- overwriting.`);
    }
    this.entries.set(layoutId, { component, name });
  }

  /** Get a registered layout component. Throws with helpful message if not found. */
  get(layoutId: string): ComponentType<LayoutProps> {
    const entry = this.entries.get(layoutId);
    if (!entry) {
      const available = [...this.entries.keys()].join(', ');
      throw new Error(
        `Layout "${layoutId}" not registered. Available: ${available}`,
      );
    }
    return entry.component;
  }

  /** All registered layout IDs. */
  ids(): readonly string[] {
    return [...this.entries.keys()];
  }

  /** Number of registered layouts. */
  get size(): number {
    return this.entries.size;
  }
}

/** Singleton layout registry. Import and use directly. */
export const layoutRegistry = new LayoutRegistry();
