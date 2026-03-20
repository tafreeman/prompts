/**
 * Side-effect module — registers all layout components with the registry.
 *
 * Import this ONCE in main.tsx before React renders. Each layout
 * is registered by its YAML `layout` field value.
 */
import { layoutRegistry } from './registry.js';
import { CoverLayout } from './cover/CoverLayout.js';
import { SectionLayout } from './section/SectionLayout.js';
import { TextLayout } from './text/TextLayout.js';
import { CardsLayout } from './cards/CardsLayout.js';
import { NumberLayout } from './number/NumberLayout.js';
import { CompareLayout } from './compare/CompareLayout.js';
import { StepsLayout } from './steps/StepsLayout.js';
import { TableLayout } from './table/TableLayout.js';
import { ScorecardLayout } from './scorecard/ScorecardLayout.js';
import { TimelineLayout } from './timeline/TimelineLayout.js';
import { GridLayout } from './grid/GridLayout.js';
import { ClosingLayout } from './closing/ClosingLayout.js';
import { ChartLayout } from './chart/ChartLayout.js';
import { HubLayout } from './hub/HubLayout.js';
import { WorkflowLayout } from './workflow/WorkflowLayout.js';
import { CycleLayout } from './cycle/CycleLayout.js';
import { QuoteLayout } from './quote/QuoteLayout.js';

layoutRegistry.register('cover', CoverLayout, 'Cover');
layoutRegistry.register('section', SectionLayout, 'Section');
layoutRegistry.register('text', TextLayout, 'Text');
layoutRegistry.register('cards', CardsLayout, 'Cards');
layoutRegistry.register('number', NumberLayout, 'Big Number');
layoutRegistry.register('compare', CompareLayout, 'Compare');
layoutRegistry.register('steps', StepsLayout, 'Steps');
layoutRegistry.register('table', TableLayout, 'Table');
layoutRegistry.register('scorecard', ScorecardLayout, 'Scorecard');
layoutRegistry.register('timeline', TimelineLayout, 'Timeline');
layoutRegistry.register('grid', GridLayout, 'Grid');
layoutRegistry.register('closing', ClosingLayout, 'Closing');
layoutRegistry.register('chart', ChartLayout, 'Bar Chart');
layoutRegistry.register('hub', HubLayout, 'Hub & Spoke');
layoutRegistry.register('workflow', WorkflowLayout, 'Workflow');
layoutRegistry.register('cycle', CycleLayout, 'Cycle Diagram');
layoutRegistry.register('quote', QuoteLayout, 'Pull Quote');
