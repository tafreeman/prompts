/**
 * Barrel — base layout family.
 *
 * Re-exports every layout in the `base/` directory so consumers can do:
 *   import { TwoColLayout, StatCardsLayout } from '../layouts/base';
 */

export { default as TwoColLayout, TwoColLayout } from "./TwoColLayout.jsx";
export {
  default as StatCardsLayout,
  StatCardsLayout,
  ManifestStatCardsLayout,
} from "./StatCardsLayout.jsx";
export {
  default as BeforeAfterLayout,
  BeforeAfterLayout,
} from "./BeforeAfterLayout.jsx";
export { default as HStripLayout, HStripLayout } from "./HStripLayout.jsx";
export {
  default as ProcessLanesLayout,
  ProcessLanesLayout,
} from "./ProcessLanesLayout.jsx";
