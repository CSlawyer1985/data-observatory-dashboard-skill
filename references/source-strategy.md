# Source Strategy

## Acquisition Priority

Use sources in this order:

1. User-provided files or pasted data.
2. Official APIs or official downloadable CSV/JSON/XLSX.
3. GitHub raw files or documented public datasets.
4. Stable webpage tables from authoritative sites.
5. Search/OpenCLI results for discovery, followed by source verification.
6. Manual/model estimation only when clearly labeled.

For current/latest data, browse or use an appropriate connector and record the exact retrieval date.

## Automatic Fetching

Possible fetch modes:

- direct CSV/JSON/XLSX download
- API request
- webpage table extraction
- static HTML extraction of embedded JSON
- OpenCLI adapters for public/search/social/legal/scholar/news sources

Avoid opaque scraping when an API or download file is available.

## Provenance Rules

Every transformed dataset should keep:

- raw input file or URL
- retrieval timestamp
- normalization script or notes
- field mapping
- confidence/limitation notes

Use confidence labels:

- `high`: official source or user-owned file
- `medium`: reputable report, stable public dataset, or well-documented extraction
- `low`: news estimate, search aggregation, model-generated or inferred value

## Refreshable Pipelines

For dashboards likely to be updated, create scripts:

```text
fetch_sources.py -> normalize_data.py -> profile_data.py -> build dashboard
```

Keep generated files separate from raw data:

```text
raw/
processed/
dashboard/
```

## Ethics and Robustness

- Respect site access limits and terms.
- Do not bypass authentication unless the user owns or has access to the data.
- Prefer cached snapshots for reproducibility.
- If a source fails, keep the previous snapshot and mark the refresh failure.

