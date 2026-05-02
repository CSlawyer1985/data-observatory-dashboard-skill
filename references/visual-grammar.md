# Visual Grammar

## Selection Rules

Choose the chart by data shape:

| Data shape | Primary visual | Use when |
|---|---|---|
| Object collection with magnitude | Treemap | Many entities, one dominant size metric, clear grouping |
| Object collection without magnitude | Matrix/grid | Comparable entities, categorical sorting, compact overview |
| Ranking | Horizontal bars | Top/bottom lists, exact comparison matters |
| Time series | Timeline or small multiples | Trends, before/after, volatility |
| Two numeric dimensions | Scatter/bubble | Tradeoffs, clusters, outliers |
| Flow between categories | Sankey/alluvial | Movement, allocation, conversion |
| Relationships | Network graph | Links are the primary fact |
| Geography | Map or region grid | Location is analytically meaningful |
| Documents/cases/events | Timeline + facet sidebar | Sequence and metadata both matter |

## Observatory Defaults

For the treemap observatory:

- Main visual: treemap, matrix, dense scatter, map, or timeline, depending on data shape.
- Sidebar: total, weighted average/intensity, distribution, group summary, top risk/opportunity, legend.
- Tooltip: entity-level details plus source and explanation.
- Mode controls: switch area/value basis, scoring basis, grouping, or time slice.

## Encoding Heuristics

- **Area/size**: count, amount, population, assets, revenue, exposure value, case volume, document count.
- **Color**: risk score, AI exposure, sentiment, growth, urgency, confidence, compliance status.
- **Position/grouping**: industry, jurisdiction, case type, department, region, stage, source.
- **Stroke**: selected, missing source, high uncertainty, manually overridden.
- **Opacity**: confidence, recency, completeness.

Never encode the same metric redundantly unless it helps legibility. Avoid one-note palettes; use neutral dark UI plus semantically meaningful color scales.

## Treemap Rules

Use treemap when:

- records are independent entities
- each record has a positive numeric size metric
- there is one useful grouping field
- approximate area comparison is acceptable

Avoid treemap when:

- exact ranking is the main task
- most values are similar and labels matter
- relationships or time order matter more than composition

Preferred treemap structure:

1. Group records by category.
2. Sort groups by total size descending.
3. Sort records within each group by size descending.
4. Use a squarified layout.
5. Draw labels only when cells are large enough.
6. Put detailed values in tooltip, not inside every cell.

## Sidebar Metrics

Compute sidebar metrics according to current mode:

- total value
- weighted average of color/intensity metric
- distribution histogram for score/intensity
- group totals and percentages
- group weighted averages
- top records by size
- top records by risk/intensity
- missing source / missing value counts when relevant

## Narrative Layer

When delivering the dashboard, include 3-6 high-signal observations if useful:

- biggest concentration
- highest risk/intensity cluster
- outliers
- missing/uncertain data
- surprising mismatch between size and score
- recommended next data to collect

