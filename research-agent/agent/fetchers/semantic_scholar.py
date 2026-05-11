"""Semantic Scholar Graph API client.

Used to look up an author by name and iterate their publications.
Deterministic fetcher. No LLM calls.

Free tier rate limit is ~1 request per 3 seconds. Pass an API key
(via the S2_API_KEY environment variable, wired through sources.yml)
for higher limits during bootstrap.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterator, List, Optional

import requests

S2_API = "https://api.semanticscholar.org/graph/v1"


@dataclass
class S2Paper:
    paper_id: str
    title: str
    abstract: Optional[str]
    authors: List[str]
    year: Optional[int]
    venue: Optional[str]
    arxiv_id: Optional[str]
    doi: Optional[str]
    url: Optional[str]


def _request(path: str, params: Optional[dict] = None, api_key: Optional[str] = None) -> dict:
    headers = {"x-api-key": api_key} if api_key else {}
    resp = requests.get(f"{S2_API}{path}", params=params, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()


def find_author_id(name: str, api_key: Optional[str] = None) -> Optional[str]:
    """Resolve a researcher name to an S2 authorId.

    Returns the best name match, or None if no candidates. Caller is
    responsible for sanity-checking the result if the name is ambiguous.
    """
    result = _request("/author/search", {"query": name, "limit": 5}, api_key)
    candidates = result.get("data", [])
    if not candidates:
        return None
    name_lc = name.lower()
    for c in candidates:
        if (c.get("name") or "").lower() == name_lc:
            return c.get("authorId")
    return candidates[0].get("authorId")


def author_papers(
    author_id: str,
    api_key: Optional[str] = None,
    page_size: int = 100,
    max_pages: int = 10,
) -> Iterator[S2Paper]:
    """Iterate publications for an author, newest-first when available."""
    fields = "title,abstract,authors,year,venue,externalIds,url"
    offset = 0
    pages = 0
    while pages < max_pages:
        result = _request(
            f"/author/{author_id}/papers",
            {"fields": fields, "limit": page_size, "offset": offset},
            api_key,
        )
        data = result.get("data") or []
        if not data:
            return
        for p in data:
            ext = p.get("externalIds") or {}
            yield S2Paper(
                paper_id=p.get("paperId") or "",
                title=(p.get("title") or "").strip(),
                abstract=p.get("abstract"),
                authors=[(a.get("name") or "") for a in (p.get("authors") or [])],
                year=p.get("year"),
                venue=p.get("venue"),
                arxiv_id=ext.get("ArXiv"),
                doi=ext.get("DOI"),
                url=p.get("url"),
            )
        if len(data) < page_size or "next" not in result:
            return
        offset += page_size
        pages += 1
        time.sleep(3)
