#!/usr/bin/env python3
"""Build the static site's data file from data/ (the source of truth).

Emits site/entries.json: every `published` entry plus the taxonomy label maps
the front-end needs to render facet filters. The site itself (index.html,
app.js, style.css) is static and loads this JSON at runtime, so the only build
step is running this script.

Usage:
  python scripts/build_site.py            # write site/entries.json
  python scripts/build_site.py --check    # exit 1 if it would change
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TAXONOMY = ROOT / "taxonomy.yml"
OUT = ROOT / "site" / "entries.json"
ENTRY_TYPES = ["papers", "classics", "courses", "oss", "incidents"]
TYPE_LABELS = {
    "papers": "Papers",
    "classics": "Classics",
    "courses": "Courses",
    "oss": "Open Source",
    "incidents": "Incidents",
}

# Fields carried into the front-end, in a stable order.
FIELDS = [
    "id", "type", "title", "url", "code", "authors", "org", "venue",
    "year", "date", "summary", "harness_layer", "sprs", "open_problems",
    "architecture", "risk_phase", "disciplines", "tags",
]
FACETS = ["sprs", "harness_layer", "open_problems"]


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def taxonomy_labels() -> dict:
    raw = load_yaml(TAXONOMY)
    out = {}
    for axis in FACETS:
        out[axis] = [{"id": i["id"], "label": i["label"]} for i in raw.get(axis, [])]
    out["type"] = [{"id": t, "label": TYPE_LABELS[t]} for t in ENTRY_TYPES]
    return out


def load_published() -> list[dict]:
    entries = []
    for etype in ENTRY_TYPES:
        folder = DATA / etype
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.yml")):
            e = load_yaml(path)
            if not isinstance(e, dict) or e.get("status") != "published":
                continue
            entries.append({k: e[k] for k in FIELDS if k in e})
    # Most recent first, then title.
    entries.sort(key=lambda e: (-(e.get("year") or 0), e.get("title", "")))
    return entries


def build() -> str:
    payload = {
        "count": None,
        "taxonomy": taxonomy_labels(),
        "entries": load_published(),
    }
    payload["count"] = len(payload["entries"])
    # default=str coerces any stray YAML date/datetime to ISO text (the schema
    # wants date as a quoted string; this is defense in depth if one slips by).
    return json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Build site/entries.json from data/.")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if site/entries.json would change")
    args = ap.parse_args()

    new = build()
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != new:
            print(f"DRIFT  {OUT.relative_to(ROOT)} is out of date. "
                  f"Run: python scripts/build_site.py")
            return 1
        print(f"{OUT.relative_to(ROOT)} is in sync with data/.")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(new, encoding="utf-8")
    payload = json.loads(new)
    print(f"wrote  {OUT.relative_to(ROOT)} ({payload['count']} published entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
