#!/usr/bin/env python3
"""Instantiate the observatory treemap template with explicit field mappings."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "templates" / "observatory-treemap.html"


def load_rows(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".json":
        obj = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(obj, list):
            return [r for r in obj if isinstance(r, dict)]
        if isinstance(obj, dict):
            for key in ("data", "rows", "records", "items"):
                if isinstance(obj.get(key), list):
                    return [r for r in obj[key] if isinstance(r, dict)]
        raise SystemExit("JSON must be an array of objects or contain data/rows/records/items.")
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    raise SystemExit("This builder accepts JSON or CSV. Convert XLSX first or use profile_data.py for inspection.")


def parse_mode(raw: str) -> dict[str, str]:
    parts = raw.split(":", 2)
    if len(parts) == 2:
        key, field = parts
        label = field
    elif len(parts) == 3:
        key, field, label = parts
    else:
        raise argparse.ArgumentTypeError("Mode must be key:field or key:field:label")
    return {"key": key, "field": field, "label": label}


def parse_tooltip(raw: str) -> dict[str, str]:
    parts = raw.split(":", 1)
    if len(parts) == 1:
        return {"field": raw, "label": raw}
    return {"field": parts[0], "label": parts[1]}


def parse_tier(raw: str) -> dict[str, object]:
    parts = raw.split(":")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Tier must be label:min:max, use inf for open-ended max")
    label, min_v, max_v = parts
    return {"label": label, "min": float(min_v), "max": float("inf") if max_v == "inf" else float(max_v)}


def parse_breakdown(raw: str) -> dict[str, object]:
    parts = raw.split(":")
    if len(parts) == 2:
        field, label = parts
        return {"field": field, "label": label}
    if len(parts) == 3:
        field, label, score = parts
        return {"field": field, "label": label, "score": float(score)}
    raise argparse.ArgumentTypeError("Breakdown must be field:label or field:label:score")


def parse_unit(raw: str) -> tuple[str, str]:
    parts = raw.split(":", 1)
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("Unit must be field:unit, for example total_fee_wan:wan_cny")
    field, unit = parts
    return field, unit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--label-field", required=True)
    parser.add_argument("--group-field", required=True)
    parser.add_argument("--score-field", required=True)
    parser.add_argument("--score-label", default="")
    parser.add_argument("--score-min", type=float, default=0)
    parser.add_argument("--score-max", type=float, default=10)
    parser.add_argument("--note-field", default="")
    parser.add_argument("--mode", action="append", type=parse_mode, required=True, help="key:field:label")
    parser.add_argument("--tooltip", action="append", type=parse_tooltip, default=[], help="field:label")
    parser.add_argument("--tier", action="append", type=parse_tier, default=[], help="label:min:max")
    parser.add_argument("--breakdown", action="append", type=parse_breakdown, default=[], help="field:label[:score]")
    parser.add_argument("--unit", action="append", type=parse_unit, default=[], help="field:unit")
    parser.add_argument("--color-scheme", choices=("risk", "growth"), default="risk", help="risk: low green/high red; growth: low red/high green")
    parser.add_argument("--signature", default="", help="Optional sidebar signature text.")
    args = parser.parse_args()

    rows = load_rows(args.input)
    if not rows:
        raise SystemExit("No rows found.")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    data_path = args.out_dir / "data.json"
    data_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    config = {
        "dataUrl": "data.json",
        "labelField": args.label_field,
        "groupField": args.group_field,
        "scoreField": args.score_field,
        "scoreLabel": args.score_label or args.score_field,
        "scoreMin": args.score_min,
        "scoreMax": args.score_max,
        "noteField": args.note_field,
        "modes": args.mode,
        "tooltipFields": args.tooltip,
        "tiers": args.tier,
        "breakdownFields": args.breakdown,
        "units": dict(args.unit),
        "colorScheme": args.color_scheme,
        "signature": args.signature,
    }

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("{{TITLE}}", args.title)
    html = html.replace("{{SUBTITLE}}", args.subtitle)
    html = html.replace("{{CONFIG_JSON}}", json.dumps(config, ensure_ascii=False))
    html = html.replace("{{DATA_JSON}}", json.dumps(rows, ensure_ascii=False).replace("<", "\\u003c"))
    (args.out_dir / "index.html").write_text(html, encoding="utf-8")

    source_note = {
        "input": args.input.name,
        "rows": len(rows),
        "builder": "data-observatory-dashboard/scripts/build_treemap_dashboard.py",
        "field_mapping": config,
    }
    (args.out_dir / "data_sources.json").write_text(json.dumps(source_note, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.out_dir / 'index.html'}")
    print(f"Wrote {data_path}")


if __name__ == "__main__":
    main()
