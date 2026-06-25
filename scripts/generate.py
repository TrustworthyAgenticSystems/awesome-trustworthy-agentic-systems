#!/usr/bin/env python3
"""Generate the awesome-list views from data/ (the single source of truth).

Two outputs, both derived from data/<type>/*.yml:

  1. README.md   — each harness-layer section's "### Resources" block is filled
                   with the entries tagged for that layer. Hand-written prose
                   (section intros, Key questions, Failure modes) is untouched;
                   only the content between the AUTOGEN markers is replaced.
  2. papers/papers.bib — BibTeX export of every papers/classics entry.

Run after editing data/. CI runs `--check` to fail if either output drifted
from data/ (i.e. someone edited data but did not regenerate).

Usage:
  python scripts/generate.py            # write README.md and papers.bib
  python scripts/generate.py --check    # exit 1 if either would change
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
README = ROOT / "README.md"
BIB = ROOT / "papers" / "papers.bib"
ENTRY_TYPES = ["papers", "classics", "courses", "oss", "incidents"]

# README "## N. Heading" line -> harness_layer id. Headings are matched by their
# stable "## N. " prefix, so wording after the number can change freely.
SECTION_LAYER = [
    (1, "foundations"),
    (2, "execution-shell"),
    (3, "coordination"),
    (4, "tool-interface"),
    (5, "memory"),
    (6, "observation-eval"),
    (7, "permissions"),
    (8, "intent"),
    (9, "transactional-agency"),
    (10, "supply-chain"),
    (11, "red-team"),
    (12, "oversight"),
    (13, "architectures"),
]

# Type -> link label and trailing tag in the rendered bullet.
TYPE_RENDER = {
    "papers": ("paper", "paper"),
    "classics": ("paper", "classic"),
    "courses": ("course", "course"),
    "oss": ("repo", "tool"),
}

FALLBACK = "- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates."


def load_entries() -> list[dict]:
    entries = []
    for etype in ENTRY_TYPES:
        folder = DATA / etype
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.yml")):
            entry = yaml.safe_load(path.read_text(encoding="utf-8"))
            if isinstance(entry, dict):
                entries.append(entry)
    return entries


def first_sentence(summary: str) -> str:
    text = " ".join((summary or "").split())
    m = re.search(r"(.+?[.!?])(\s|$)", text)
    return m.group(1) if m else text


def author_label(entry: dict) -> str:
    authors = entry.get("authors") or []
    if not authors:
        return entry.get("org") or ""
    if len(authors) == 1:
        return authors[0]
    return f"{authors[0]} et al."


def render_bullet(entry: dict) -> str:
    link_label, type_tag = TYPE_RENDER.get(entry["type"], ("link", entry["type"]))
    title = entry["title"]
    by = author_label(entry)
    year = entry.get("year")
    paren = ""
    if by and year:
        paren = f" ({by}, {year})"
    elif by:
        paren = f" ({by})"
    elif year:
        paren = f" ({year})"

    summary = first_sentence(entry.get("summary", "")).rstrip(".")
    parts = [f"- **{title}**{paren} — {summary}.", f"[[{link_label}]]({entry['url']})"]
    if entry.get("code"):
        parts.append(f"[[code]]({entry['code']})")
    venue = entry.get("venue")
    if venue and year:
        parts.append(f"`[{venue} {year}]`")
    parts.append(f"`[{type_tag}]`")
    return " ".join(parts)


def render_layer(entries: list[dict], layer: str) -> str:
    # Only published entries reach the public README. Draft / in-review entries
    # live in data/ and pass validation, but stay out of the rendered artifact
    # until a human flips them to published (the review gate).
    matching = [e for e in entries if layer in (e.get("harness_layer") or [])
                and e.get("type") != "incidents"
                and e.get("status") == "published"]
    # Most recent first, then alphabetical by title.
    matching.sort(key=lambda e: (-(e.get("year") or 0), e.get("title", "")))
    if not matching:
        return FALLBACK
    return "\n".join(render_bullet(e) for e in matching)


def block(layer: str, body: str) -> str:
    return f"<!-- AUTOGEN:START layer={layer} -->\n{body}\n<!-- AUTOGEN:END layer={layer} -->"


def build_readme(entries: list[dict], current: str) -> str:
    lines = current.split("\n")
    out: list[str] = []
    i = 0
    # Map section number -> layer for quick lookup.
    num_to_layer = dict(SECTION_LAYER)

    while i < len(lines):
        line = lines[i]
        out.append(line)
        m = re.match(r"^## (\d+)\.\s", line)
        if not m:
            i += 1
            continue
        num = int(m.group(1))
        layer = num_to_layer.get(num)
        if layer is None:
            i += 1
            continue
        # Walk forward to this section's "### Resources" heading, copying lines,
        # stopping before the next "## " section heading.
        i += 1
        while i < len(lines) and not lines[i].startswith("## "):
            if lines[i].strip() == "### Resources":
                out.append(lines[i])  # the "### Resources" heading
                i += 1
                # Collect the resources body up to the trailing "---" or next "##".
                while i < len(lines) and lines[i].strip() not in ("---",) \
                        and not lines[i].startswith("## "):
                    i += 1
                out.append("")
                out.append(block(layer, render_layer(entries, layer)))
                out.append("")
                break
            out.append(lines[i])
            i += 1
    return "\n".join(out)


def build_bib(entries: list[dict]) -> str:
    header = (
        "% BibTeX export for awesome-trustworthy-agentic-systems.\n"
        "% GENERATED from data/ by scripts/generate.py. Do not edit by hand.\n"
        "% Run: python scripts/generate.py\n"
    )
    pubs = [e for e in entries if e.get("type") in ("papers", "classics")
            and e.get("status") == "published"]
    pubs.sort(key=lambda e: (-(e.get("year") or 0), e.get("id", "")))
    blocks = [header]
    for e in pubs:
        fields = [f"  title = {{{e['title']}}}"]
        authors = e.get("authors") or []
        if authors:
            fields.append(f"  author = {{{' and '.join(authors)}}}")
        if e.get("year"):
            fields.append(f"  year = {{{e['year']}}}")
        if e.get("venue"):
            fields.append(f"  howpublished = {{{e['venue']}}}")
        fields.append(f"  url = {{{e['url']}}}")
        blocks.append("@misc{" + e["id"] + ",\n" + ",\n".join(fields) + "\n}")
    return "\n\n".join(blocks) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate README + bib from data/.")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if outputs would change (no writes)")
    args = ap.parse_args()

    entries = load_entries()
    new_readme = build_readme(entries, README.read_text(encoding="utf-8"))
    new_bib = build_bib(entries)

    targets = [(README, new_readme), (BIB, new_bib)]

    if args.check:
        drift = [p for p, new in targets if p.read_text(encoding="utf-8") != new]
        if drift:
            for p in drift:
                print(f"DRIFT  {p.relative_to(ROOT)} is out of date. "
                      f"Run: python scripts/generate.py")
            return 1
        print("README.md and papers/papers.bib are in sync with data/.")
        return 0

    changed = []
    for p, new in targets:
        if p.read_text(encoding="utf-8") != new:
            p.write_text(new, encoding="utf-8")
            changed.append(p.relative_to(ROOT))
    if changed:
        for p in changed:
            print(f"wrote  {p}")
    else:
        print("No changes; outputs already in sync with data/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
