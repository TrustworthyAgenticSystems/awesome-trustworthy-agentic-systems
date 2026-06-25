"""Dedupe candidate papers against existing entries in data/ and each other.

Three identity keys per paper, any of which is sufficient for a match:
  - arxiv:<arxiv_id>
  - doi:<lowercased_doi>
  - title-author:<normalized_title>:<first_author>

The source of truth is data/<type>/*.yml (one mapping per file), scanned
recursively so prior drafts under data/papers/drafts/ count too.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Optional, Set, Tuple

import yaml

Key = Tuple[str, ...]


def _normalize_title(title: str) -> str:
    return re.sub(r"\W+", "", title.lower())


def _arxiv_from_url(url: str) -> Optional[str]:
    if not url:
        return None
    m = re.search(r"arxiv\.org/abs/([\w.\-/]+)", url)
    return m.group(1) if m else None


def _keys_from_entry(p: dict) -> List[Key]:
    keys: List[Key] = []
    arxiv = _arxiv_from_url(p.get("url") or "")
    if arxiv:
        keys.append(("arxiv", arxiv))
    doi = p.get("doi")
    if doi:
        keys.append(("doi", str(doi).lower()))
    title = p.get("title") or ""
    authors = p.get("authors") or []
    if title and authors:
        keys.append(("title-author", _normalize_title(title), authors[0]))
    return keys


def _iter_entries(data_dir: Path):
    if not data_dir.is_dir():
        return
    for path in sorted(data_dir.rglob("*.yml")):
        try:
            entry = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if isinstance(entry, dict):
            yield entry


def load_existing_keys(data_dir: Path) -> Set[Key]:
    """Dedup keys for every entry under data/ (recursive)."""
    keys: Set[Key] = set()
    for entry in _iter_entries(data_dir):
        keys.update(_keys_from_entry(entry))
    return keys


def load_existing_ids(data_dir: Path) -> Set[str]:
    """All entry ids under data/ (recursive), so generated slugs never collide."""
    ids: Set[str] = set()
    for entry in _iter_entries(data_dir):
        if entry.get("id"):
            ids.add(entry["id"])
    return ids


def candidate_keys(
    arxiv_id: Optional[str],
    doi: Optional[str],
    title: str,
    first_author: str,
) -> List[Key]:
    keys: List[Key] = []
    if arxiv_id:
        keys.append(("arxiv", arxiv_id))
    if doi:
        keys.append(("doi", doi.lower()))
    if title and first_author:
        keys.append(("title-author", _normalize_title(title), first_author))
    return keys


def is_duplicate(keys: Iterable[Key], existing: Set[Key]) -> bool:
    return any(k in existing for k in keys)
