#!/usr/bin/env python3
"""Validate hub entries against the schema, taxonomy, and quality gates.

This is the automated half of the architecture's "human review gate": every PR
that touches data/ runs this before a human reviews. Checks, in order:

  1. taxonomy.yml <-> schema enums agree (drift guard; taxonomy is the authority)
  2. each data/<type>/*.yml parses, validates against schema/entry.schema.json
  3. type matches its folder; id matches its filename
  4. all tag values exist in taxonomy.yml (both facets + optional axes)
  5. ids are unique across the repo (dedup)
  6. `related` targets reference real entry ids
  7. publish gate: status=published requires provenance.reviewed_by
  8. incident gate: draft/in-review incidents name no parties (heuristic)
  9. url (and code, if present) resolves unless --skip-urls

Exit code 0 if clean, 1 if any error. Warnings never fail the build.

Usage:
  python scripts/validate.py [--skip-urls] [--quiet]
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY = ROOT / "taxonomy.yml"
SCHEMA = ROOT / "schema" / "entry.schema.json"
DATA = ROOT / "data"
ENTRY_TYPES = ["papers", "classics", "courses", "oss", "incidents"]

# Taxonomy axes that constrain entry list-fields. Key = entry field = taxonomy key.
TAXONOMY_AXES = [
    "harness_layer",
    "sprs",
    "open_problems",
    "architecture",
    "risk_phase",
    "disciplines",
]

USER_AGENT = "awesome-trustworthy-agentic-systems-validator/1.0"


class Reporter:
    def __init__(self, quiet: bool = False):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.quiet = quiet

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")

    def info(self, msg: str) -> None:
        if not self.quiet:
            print(msg)


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_taxonomy() -> dict[str, set[str]]:
    """Return {axis: set(ids)} for every controlled axis."""
    raw = load_yaml(TAXONOMY)
    vocab: dict[str, set[str]] = {}
    for axis in TAXONOMY_AXES:
        items = raw.get(axis, []) or []
        vocab[axis] = {item["id"] for item in items}
    return vocab


def schema_enums(schema: dict) -> dict[str, set[str]]:
    """Pull the enum sets the schema declares for each constrained array field."""
    props = schema["properties"]
    out: dict[str, set[str]] = {}
    for axis in TAXONOMY_AXES:
        node = props.get(axis, {})
        items = node.get("items", {})
        if "enum" in items:
            out[axis] = set(items["enum"])
    return out


def check_taxonomy_schema_drift(vocab, schema, rep: Reporter) -> None:
    enums = schema_enums(schema)
    for axis, enum_vals in enums.items():
        tax_vals = vocab.get(axis, set())
        missing_in_tax = enum_vals - tax_vals
        missing_in_schema = tax_vals - enum_vals
        if missing_in_tax:
            rep.error("schema<->taxonomy",
                      f"{axis}: schema allows {sorted(missing_in_tax)} absent from taxonomy.yml")
        if missing_in_schema:
            rep.error("schema<->taxonomy",
                      f"{axis}: taxonomy.yml defines {sorted(missing_in_schema)} the schema rejects")


# Crude name heuristic for the incident gate: a known-vendor token in a non-published
# incident is worth a human look. Warns only; a maintainer makes the call.
VENDOR_HINTS = {
    "google", "openai", "anthropic", "meta", "microsoft", "amazon", "apple",
    "tesla", "uber", "deepmind", "twitter", "facebook", "claude", "copilot",
}


def check_incident_naming(entry: dict, where: str, rep: Reporter) -> None:
    if entry.get("type") != "incidents":
        return
    if entry.get("status") == "published":
        return
    words = " ".join(
        str(entry.get(k, "")) for k in ("title", "summary", "org")
    ).lower().replace("/", " ").split()
    hit = sorted({v for v in VENDOR_HINTS if v in words})
    if hit:
        rep.warn(where,
                 f"draft/in-review incident may name a party {hit}; a human must "
                 f"confirm before publish (non-negotiable)")


def url_resolves(url: str, timeout: float = 10.0) -> tuple[bool, str]:
    headers = {"User-Agent": USER_AGENT}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = resp.getcode()
                if 200 <= code < 400:
                    return True, str(code)
        except urllib.error.HTTPError as e:
            # Some servers reject HEAD with 4xx/5xx; retry with GET before failing.
            if method == "HEAD" and e.code in (400, 403, 405, 501):
                continue
            return False, f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            if method == "HEAD":
                continue
            return False, str(getattr(e, "reason", e))
    return False, "unreachable"


def iter_entry_files():
    # rglob (recursive) so staging subfolders like data/papers/drafts/ are
    # validated too: the research agent's drafts must be schema-valid and
    # non-duplicate before review. The generator and site stay non-recursive
    # and published-only, so drafts never reach a public artifact.
    for etype in ENTRY_TYPES:
        folder = DATA / etype
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*.yml")):
            yield etype, path


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate hub entries.")
    ap.add_argument("--skip-urls", action="store_true",
                    help="skip network URL resolution (faster, offline)")
    ap.add_argument("--quiet", action="store_true", help="suppress per-file output")
    args = ap.parse_args()

    rep = Reporter(quiet=args.quiet)

    vocab = load_taxonomy()
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    check_taxonomy_schema_drift(vocab, schema, rep)

    seen_ids: dict[str, str] = {}
    all_ids: set[str] = set()
    entries: list[tuple[dict, str]] = []
    url_targets: list[tuple[str, str, str]] = []  # (where, label, url)

    count = 0
    for etype, path in iter_entry_files():
        count += 1
        where = str(path.relative_to(ROOT))
        try:
            entry = load_yaml(path)
        except yaml.YAMLError as e:
            rep.error(where, f"YAML parse error: {e}")
            continue
        if not isinstance(entry, dict):
            rep.error(where, "top-level YAML is not a mapping")
            continue

        for err in sorted(validator.iter_errors(entry), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in err.path) or "(root)"
            rep.error(where, f"schema: {loc}: {err.message}")

        eid = entry.get("id")

        if entry.get("type") != etype:
            rep.error(where, f"type '{entry.get('type')}' but file lives under data/{etype}/")
        if eid and path.stem != eid:
            rep.error(where, f"filename '{path.stem}.yml' does not match id '{eid}'")

        if eid:
            if eid in seen_ids:
                rep.error(where, f"duplicate id '{eid}' (also in {seen_ids[eid]})")
            else:
                seen_ids[eid] = where
                all_ids.add(eid)

        for axis in TAXONOMY_AXES:
            for val in entry.get(axis, []) or []:
                if val not in vocab[axis]:
                    rep.error(where, f"{axis}: '{val}' is not in taxonomy.yml")

        check_incident_naming(entry, where, rep)

        if not args.skip_urls:
            if entry.get("url"):
                url_targets.append((where, eid or "?", entry["url"]))
            if entry.get("code"):
                url_targets.append((where, f"{eid or '?'} (code)", entry["code"]))

        entries.append((entry, where))

    for entry, where in entries:
        for rid in entry.get("related", []) or []:
            if rid not in all_ids:
                rep.warn(where, f"related id '{rid}' does not match any entry")

    if url_targets:
        rep.info(f"Checking {len(url_targets)} URL(s)...")
        for where, label, url in url_targets:
            ok, detail = url_resolves(url)
            if not ok:
                rep.error(where, f"url does not resolve ({detail}): {url}")
            elif not args.quiet:
                rep.info(f"  ok  {label}: {url} [{detail}]")

    print()
    print(f"Validated {count} entr{'y' if count == 1 else 'ies'}.")
    for w in rep.warnings:
        print(f"  WARN  {w}")
    for e in rep.errors:
        print(f"  FAIL  {e}")

    if rep.errors:
        print(f"\n{len(rep.errors)} error(s), {len(rep.warnings)} warning(s). FAILED.")
        return 1
    print(f"\n0 errors, {len(rep.warnings)} warning(s). OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
