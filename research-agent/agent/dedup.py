"""Dedupe candidate papers against existing papers.yml and against each other.

Three identity keys per paper, any of which is sufficient for a match:
  - arxiv:<arxiv_id>
  - doi:<lowercased_doi>
  - title-author:<normalized_title>:<first_author>
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


def load_existing_keys(papers_yml: Path) -> Set[Key]:
    """Read papers/papers.yml and extract dedup keys for every entry."""
    if not papers_yml.exists():
        return set()
    raw = papers_yml.read_text()
    data = yaml.safe_load(raw) or {}
    papers = data.get("papers") or []
    keys: Set[Key] = set()
    for p in papers:
        if not isinstance(p, dict):
            continue
        url = p.get("url") or ""
        arxiv = _arxiv_from_url(url)
        if arxiv:
            keys.add(("arxiv", arxiv))
        doi = p.get("doi")
        if doi:
            keys.add(("doi", doi.lower()))
        title = p.get("title") or ""
        authors = p.get("authors") or []
        if title and authors:
            keys.add(("title-author", _normalize_title(title), authors[0]))
    return keys


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
