#!/usr/bin/env python3
"""Promote reviewed agent drafts from data/<type>/drafts/ to published entries.

For each entry, this moves the file up one directory (out of `drafts/`), sets
`status: published`, records `provenance.reviewed_by`, and strips the draft
header comment. It is the mechanical half of the human review gate; the
editorial judgment is yours.

Usage:
  python scripts/promote.py --reviewer <handle> <id|path> [<id|path> ...]
  python scripts/promote.py --reviewer <handle> --all

Then refresh the generated views and validate:
  python scripts/generate.py && python scripts/build_site.py && python scripts/validate.py

To REJECT a draft instead, just delete its file (e.g. `git rm data/papers/drafts/<id>.yml`).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def find_draft(token: str) -> Path | None:
    """Resolve a draft by path, or by id under any data/<type>/drafts/."""
    p = Path(token)
    if p.is_file():
        return p
    matches = sorted(DATA.glob(f"*/drafts/{token}.yml"))
    return matches[0] if matches else None


def promote_one(path: Path, reviewer: str) -> Path:
    lines = path.read_text(encoding="utf-8").splitlines()
    # Drop the leading comment/blank header; keep from the first real key.
    start = next((i for i, l in enumerate(lines) if l.startswith("id:")), 0)
    body = lines[start:]

    has_reviewer = any(l.strip().startswith("reviewed_by:") for l in body)
    out: list[str] = []
    for l in body:
        out.append("status: published" if l.strip() == "status: draft" else l)
        if l.strip().startswith("drafted_by:") and not has_reviewer:
            indent = l[: len(l) - len(l.lstrip())]
            out.append(f"{indent}reviewed_by: {reviewer}")

    dest = path.parent.parent / path.name  # out of drafts/, into data/<type>/
    if dest.exists():
        raise FileExistsError(f"{dest.relative_to(ROOT)} already exists")
    dest.write_text("\n".join(out) + "\n", encoding="utf-8")
    path.unlink()
    drafts_dir = path.parent
    if drafts_dir.name == "drafts" and not any(drafts_dir.iterdir()):
        drafts_dir.rmdir()
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description="Promote reviewed agent drafts to published.")
    ap.add_argument("--reviewer", required=True, help="reviewer of record (your handle)")
    ap.add_argument("--all", action="store_true", help="promote every file under data/*/drafts/")
    ap.add_argument("ids", nargs="*", help="entry ids or draft file paths")
    args = ap.parse_args()

    if args.all:
        targets = sorted(DATA.glob("*/drafts/*.yml"))
    else:
        targets = []
        for token in args.ids:
            p = find_draft(token)
            if p is None:
                print(f"  not found: {token}", file=sys.stderr)
                return 1
            targets.append(p)

    if not targets:
        print("nothing to promote (no ids given; use --all or list ids)", file=sys.stderr)
        return 1

    for path in targets:
        dest = promote_one(path, args.reviewer)
        print(f"promoted  {dest.relative_to(ROOT)}  (reviewed_by: {args.reviewer})")

    print(f"\n{len(targets)} promoted. Now run:")
    print("  python scripts/generate.py && python scripts/build_site.py && python scripts/validate.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
