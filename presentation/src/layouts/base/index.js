/**
 * Barrel — base layout family.
 *
 * Re-exports every layout in the `base/` directory so consumers can do:
 *   import { TwoColLayout, StatCardsLayout } from '../layouts/base';
 */

export { default as TwoColLayout, TwoColLayout } from "./TwoColLayout.tsx";
export {
  default as StatCardsLayout,
  StatCardsLayout,
  ManifestStatCardsLayout,
} from "./StatCardsLayout.tsx";
export {
  default as BeforeAfterLayout,
  BeforeAfterLayout,
} from "./BeforeAfterLayout.tsx";
export { default as HStripLayout, HStripLayout } from "./HStripLayout.tsx";
export {
  default as ProcessLanesLayout,
  ProcessLanesLayout,
} from "./ProcessLanesLayout.tsx";
