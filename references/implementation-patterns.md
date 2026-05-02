# Implementation Patterns

## Static Dashboard Stack

Default to:

- HTML
- CSS
- vanilla JavaScript
- Canvas for thousands of dense marks or treemap cells
- SVG for axes, smaller charts, labels, and accessible shapes

Use React/Vite only when the user needs a larger app, routing, stateful controls, or reusable components.

## Layout

Observatory default:

```text
┌────────────── sidebar ──────────────┬──────── main visual field ────────┐
│ title/source/modes/statistics       │ canvas/svg/map/grid               │
│ distribution/group overview/legend  │ hover/selection surface           │
└─────────────────────────────────────┴───────────────────────────────────┘
```

For mobile, do not merely squeeze a fixed sidebar unless the user explicitly wants a fixed original layout. Prefer:

- top compact toolbar
- collapsible stats drawer
- full-width visual field
- tap tooltip/selection panel

## Styling

Use restrained, data-first UI:

- dark neutral background
- one semantic color scale
- small but readable labels
- compact controls
- clear hover/focus states
- no decorative blobs, orbs, or marketing hero sections

Recommended base palette:

```css
--bg: #0a0a0f;
--panel: #12121a;
--fg: #e0e0e8;
--muted: #888894;
```

Use color interpolation functions for semantic scales rather than hardcoding many colors.

## Canvas Rules

- Always account for `devicePixelRatio`.
- Set both canvas attributes and CSS dimensions.
- Clip text to cell bounds.
- Draw labels only above size thresholds.
- Keep hover state in JS and redraw only when needed.

## Interaction Rules

- Mode controls must update visual layout and sidebar stats together.
- Tooltip must not capture pointer events.
- Edge-aware tooltip positioning is required.
- Record selection can persist details in a side panel when tooltip is too transient.
- Add keyboard/accessibility affordances when using DOM/SVG controls.

## Validation

Before delivery:

- run a local server if data is fetched
- take desktop and mobile screenshots
- verify the primary visual is nonblank
- test at least one mode switch
- test tooltip/selection
- inspect text overflow and overlapping UI
- check source notes and dates

