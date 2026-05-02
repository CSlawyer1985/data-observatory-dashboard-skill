---
name: data-observatory-dashboard
description: Use when transforming arbitrary structured or semi-structured data into a high-density, source-aware, interactive data visualization dashboard. Fits CSV, Excel, JSON, webpage tables, public datasets, research/policy/legal/financial/industry data, and requests that mention "可视化仪表盘", "数据可视化", "矩形树图", "treemap", "数据看板", "报表可视化", "Excel 做成看板", "业务数据大屏", "交互式数据大屏", "数据观察仪表盘", "高密度可视化", "沿用矩形树图数据观察仪表盘方法论", "自动获取数据并可视化", or "把这些数据做成交互网页".
---

# Data Observatory Dashboard

Build a restrained, high-density data observatory: a left control/stat sidebar plus a dominant right-side visual field, with clear visual encoding, source tracking, and interaction.

## Trigger Phrases

Use this skill when the user says or implies:

- 可视化仪表盘、数据可视化、数据看板、业务数据看板、交互式看板
- 矩形树图、treemap、树图、面积图、按规模分块
- 报表可视化、Excel 做成看板、把表格做成交互网页、把这些数据做成页面
- 高密度可视化、数据观察仪表盘、数据观察站、数据大屏
- 沿用矩形树图数据观察仪表盘方法论、参考矩形树图数据观察仪表盘、类似之前某个业务报表看板效果
- 自动获取数据并可视化、从网页/公开数据/接口获取数据做看板

Carry forward these learned defaults: preserve source units explicitly, especially 万元/亿元/百分比; include color legend, distribution, tier overview, group overview, breakdown overview, tooltip, and source notes; keep sidebar narrow but expanded by default, non-overlapping with the main visual, with a subtle manual collapse/expand control; place a quiet centered signature at the sidebar bottom only when the user requests or provides one.

## Core Workflow

1. **Acquire or load data**
   - Local files first: CSV, JSON, XLSX, Markdown tables.
   - For URLs, prefer official APIs, raw CSV/JSON, downloadable public files, or explicitly provided pages. If the user asks for current/latest data, verify online and record retrieval dates.
   - For Chinese public/news/social/search sources, consider OpenCLI or available app connectors when appropriate.

2. **Profile the dataset**
   - Run `scripts/profile_data.py <input> --out <output-dir>/data-profile.json` when the input is CSV/JSON/XLSX. Raw sample values are excluded by default; add `--include-samples` only when the user accepts that sample values may be written to disk.
   - Identify object label, grouping fields, numeric magnitude fields, color/risk/intensity fields, time fields, text explanation fields, and source fields.
   - Identify source units before charting: especially 万元/亿元/元, percentages already stored as 0-100, counts, people, cases, clients, and times.
   - If profiling is ambiguous, choose conservative defaults and document the mapping.

3. **Choose visual grammar**
   - Read `references/visual-grammar.md` when selecting chart type or encoding.
   - Default for object collections: treemap observatory.
   - Do not force treemap onto time-series, geospatial, or relationship-heavy data.

4. **Define a data contract**
   - Read `references/data-contract.md` when normalizing fields.
   - Create a normalized `data.json` and, when sources matter, `data_sources.json`.
   - Do not write local absolute paths, names, credentials, or private identifiers into reusable skill files or public-facing source records.
   - Attach unit metadata to dashboard fields with `--unit field:unit`; never let generic number formatting reinterpret source units.
   - Preserve original raw data unless the user only wants a quick prototype.

5. **Build the dashboard**
   - Prefer a static HTML/CSS/JS artifact for portability.
   - Use `assets/templates/observatory-treemap.html` as the starting point when the data is an object collection with magnitude + grouping + intensity.
   - Keep the first screen as the usable visualization, not a landing page.

6. **Validate**
   - Start a local static server when `fetch()` is used.
   - Use browser/Playwright screenshots for desktop and mobile.
   - Check nonblank canvas/SVG, tooltip behavior, mode switches, text overflow, and source/date display.

## Signature Design Pattern

- Fixed or persistent left sidebar: title, source note, mode controls, total metrics, weighted score, distribution, group overview, top/bottom lists, legend.
- Main visual field: canvas/SVG/grid/map occupying the remaining viewport.
- Visual encodings:
  - size/area = importance, scale, exposure, amount, or count
  - color = risk, intensity, score, sentiment, growth, or uncertainty
  - grouping/position = category, region, domain, stage, or owner
  - opacity/stroke = confidence, selection, or warning
- Tooltip explains one object: label, core metrics, source, rationale, notes.
- Mode switches recompute both visual layout and sidebar statistics.

## Output Files

For nontrivial work, create:

- `index.html` or app files
- `data.json`
- `data-profile.json`
- `data_sources.json` when data is fetched, estimated, merged, or model-scored
- `screenshots/` after visual validation
- short implementation notes only when useful for the user

## Reference Loading

- `references/visual-grammar.md`: chart and encoding selection.
- `references/data-contract.md`: normalized schema patterns and calculations.
- `references/source-strategy.md`: automatic data acquisition and source records.
- `references/implementation-patterns.md`: frontend details for dense static dashboards.
