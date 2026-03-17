/**
 * Layout Registry — plugin system for dynamic layout resolution.
 *
 * Replaces the monolith's ~25-case switch statement with O(1) Map lookups.
 * Layouts self-register; new deck families can add layouts without editing core.
 *
 * Usage:
 *   import { layoutRegistry } from './registry';
 *   layoutRegistry.register('cover', Cover, { effects: true, background: true });
 *   const Component = layoutRegistry.get('cover');
 *   const features = layoutRegistry.getFeatures('cover');
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

/**
 * Feature manifest — declares what ControlPanel sections a layout supports.
 *
 * Each boolean flag controls whether the corresponding ControlPanel section
 * is shown when a slide using this layout is active.  Defaults (when a layout
 * is registered without features) are defined by DEFAULT_FEATURES.
 */
export interface LayoutFeatures {
  /** Show the "Render As" family picker (transcription to other families). */
  renderAs: boolean;
  /** Show the "Effects" section (intro sequence, comet transitions). */
  effects: boolean;
  /** Show the "Background" section (hero image toggle + URL). */
  background: boolean;
}

/** Sensible defaults — everything off until explicitly opted-in. */
export const DEFAULT_FEATURES: Readonly<LayoutFeatures> = Object.freeze({
  renderAs: false,
  effects: false,
  background: false,
});

class LayoutRegistry {
  private registry = new Map<string, LayoutComponent>();
  private features = new Map<string, LayoutFeatures>();

  /**
   * Register a single layout component with optional feature metadata.
   * Warns on overwrite to catch accidental collisions.
   */
  register(
    layoutId: string,
    Component: LayoutComponent,
    featureOverrides?: Partial<LayoutFeatures>,
  ): void {
    if (this.registry.has(layoutId)) {
      console.warn(`[LayoutRegistry] Layout "${layoutId}" already registered; overwriting.`);
    }
    this.registry.set(layoutId, Component);
    this.features.set(layoutId, { ...DEFAULT_FEATURES, ...featureOverrides });
  }

  /**
   * Register multiple layouts at once, all sharing the same features.
   * @example registry.registerBatch({ cover: Cover, 'nav-hub': NavHub }, { effects: true });
   */
  registerBatch(
    layouts: Record<string, LayoutComponent>,
    featureOverrides?: Partial<LayoutFeatures>,
  ): void {
    Object.entries(layouts).forEach(([id, Component]) => {
      this.register(id, Component, featureOverrides);
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

  /**
   * Get the feature manifest for a layout.
   * Returns DEFAULT_FEATURES for unknown layout IDs (safe fallback).
   */
  getFeatures(layoutId: string): LayoutFeatures {
    return this.features.get(layoutId) ?? { ...DEFAULT_FEATURES };
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
