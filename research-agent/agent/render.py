"""Render classified papers into schema-valid draft entries for PR review.

The agent never writes to data/papers/ directly. It writes one file per
candidate to data/papers/drafts/<id>.yml at status: draft, opens a PR labeled
`agent-draft`, and lets a human reviewer promote accepted entries (move the
file up to data/papers/, set status: published, record reviewed_by).

Each file matches schema/entry.schema.json so the validator gates the draft in
CI. Entries that cannot be made schema-valid (missing facet, too-short summary)
are dropped with a warning rather than written as invalid YAML.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Iterable, List, Optional, Set

import yaml

log = logging.getLogger("research-agent")

MIN_SUMMARY = 20  # schema/entry.schema.json: summary minLength
# Plain dicts preserve insertion order (Python 3.7+), and yaml.safe_dump with
# sort_keys=False keeps that order, so no custom representer is needed.


def slugify(title: str, year) -> str:
    """Stable id slug matching ^[a-z0-9]+(?:-[a-z0-9]+)*$, prefixed by year."""
    words = re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).split()
    stem = "-".join(words[:8]) or "untitled"
    prefix = f"{year}-" if year else ""
    slug = f"{prefix}{stem}"
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def _unique_id(base: str, taken: Set[str]) -> str:
    if base not in taken:
        return base
    i = 2
    while f"{base}-{i}" in taken:
        i += 1
    return f"{base}-{i}"


def _build_entry(e: dict, eid: str) -> Optional[dict]:
    layers = [l for l in (e.get("harness_layer") or []) if l and l != "out-of-scope"]
    sprs = list(e.get("sprs") or [])
    summary = " ".join((e.get("summary") or "").split())

    if not layers:
        log.warning("dropping %r: no usable harness_layer", eid)
        return None
    if not sprs:
        log.warning("dropping %r: no sprs guarantee", eid)
        return None
    if len(summary) < MIN_SUMMARY:
        log.warning("dropping %r: summary too short (%d chars)", eid, len(summary))
        return None

    entry: dict = {
        "id": eid,
        "type": "papers",
        "title": e.get("title") or "",
        "url": e.get("url") or "",
    }
    if e.get("code"):
        entry["code"] = e["code"]
    if e.get("authors"):
        entry["authors"] = list(e["authors"])
    if e.get("venue"):
        entry["venue"] = e["venue"]
    if e.get("year"):
        entry["year"] = e["year"]
    entry["summary"] = summary
    entry["harness_layer"] = layers
    entry["sprs"] = sprs
    if e.get("open_problems"):
        entry["open_problems"] = list(e["open_problems"])

    prov: dict = {"added_by": "agent", "drafted_by": "research-agent"}
    if e.get("confidence") is not None:
        prov["confidence"] = round(float(e["confidence"]), 2)
    if e.get("rationale"):
        prov["rationale"] = " ".join(str(e["rationale"]).split())
    entry["provenance"] = prov

    entry["status"] = "draft"
    return entry


def render_drafts(entries: Iterable[dict], drafts_dir: Path, existing_ids: Set[str]) -> int:
    """Write one draft file per entry to drafts_dir. Returns the count written.

    `existing_ids` are ids already present across data/ (and prior drafts) so
    generated slugs never collide with a real entry.
    """
    entry_list: List[dict] = list(entries)
    if not entry_list:
        return 0

    drafts_dir.mkdir(parents=True, exist_ok=True)
    taken: Set[str] = set(existing_ids)
    written = 0

    for e in entry_list:
        base = slugify(e.get("title", ""), e.get("year"))
        eid = _unique_id(base, taken)
        record = _build_entry(e, eid)
        if record is None:
            continue
        taken.add(eid)

        header = (
            "# Drafted by research-agent. Review before promoting.\n"
            "# To accept: move this file to data/papers/<id>.yml, set\n"
            "# status: published, and record provenance.reviewed_by.\n"
            "# To reject: delete this file.\n\n"
        )
        body = yaml.safe_dump(
            record, sort_keys=False, allow_unicode=True, width=100, default_flow_style=False
        )
        (drafts_dir / f"{eid}.yml").write_text(header + body, encoding="utf-8")
        written += 1

    return written
