/**
 * Layout Registry — plugin system for dynamic layout resolution.
 *
 * Replaces the monolith's ~25-case switch statement with O(1) Map lookups.
 * Layouts self-register; new deck families can add layouts without editing core.
 *
 * Usage:
 *   import { layoutRegistry } from './registry';
 *   layoutRegistry.register('cover', Cover);
 *   const Component = layoutRegistry.get('cover');
 */

import type { ComponentType } from 'react';

/**
 * Standard props that every layout component receives.
 * Individual layouts may accept additional props via the slide object.
 */
export interface LayoutProps {
  slide: Record<string, any>;
  themeId: string;
  [key: string]: any;
}

export type LayoutComponent = ComponentType<LayoutProps>;

class LayoutRegistry {
  private registry = new Map<string, LayoutComponent>();

  /**
   * Register a single layout component.
   * Warns on overwrite to catch accidental collisions.
   */
  register(layoutId: string, Component: LayoutComponent): void {
    if (this.registry.has(layoutId)) {
      console.warn(`[LayoutRegistry] Layout "${layoutId}" already registered; overwriting.`);
    }
    this.registry.set(layoutId, Component);
  }

  /**
   * Register multiple layouts at once.
   * @example registry.registerBatch({ cover: Cover, 'nav-hub': NavHub });
   */
  registerBatch(layouts: Record<string, LayoutComponent>): void {
    Object.entries(layouts).forEach(([id, Component]) => {
      this.register(id, Component);
    });
  }

  /**
   * Get a layout component by ID.
   * Throws with a helpful error listing available layouts if not found.
   */
  get(layoutId: string): LayoutComponent {
    const Component = this.registry.get(layoutId);
    if (!Component) {
      const available = Array.from(this.registry.keys()).join(', ');
      throw new Error(
        `[LayoutRegistry] Unknown layout: "${layoutId}". Available: ${available}`,
      );
    }
    return Component;
  }

  /** Check whether a layout is registered. */
  has(layoutId: string): boolean {
    return this.registry.has(layoutId);
  }

  /** Return all registered layout IDs. */
  list(): string[] {
    return Array.from(this.registry.keys());
  }

  /** Filter registered layouts by ID prefix (e.g., 'hb-', 'eng-'). */
  listByPrefix(prefix: string): string[] {
    return this.list().filter((id) => id.startsWith(prefix));
  }
}

/** Singleton registry — import this everywhere. */
export const layoutRegistry = new LayoutRegistry();
