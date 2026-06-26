"""arXiv API client.

Deterministic fetcher. No LLM calls. Returns ArxivPaper dataclasses with
the minimum metadata the classifier needs.

The arXiv API asks for ~3 seconds between requests. This module sleeps
between paged requests; callers fanning out across many queries should
also rate-limit themselves.
"""

from __future__ import annotations

import time
import urllib.parse
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, List

import requests

ARXIV_API = "https://export.arxiv.org/api/query"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

# arXiv rate-limits by IP and rejects blank/default User-Agents, so shared CI
# runners routinely get 429s. Identify the client and retry with backoff.
USER_AGENT = (
    "awesome-trustworthy-agentic-systems-research-agent/1.0 "
    "(+https://github.com/TrustworthyAgenticSystems/awesome-trustworthy-agentic-systems)"
)


def _get_with_retry(url: str, max_retries: int = 5, base_delay: float = 3.0) -> requests.Response:
    """GET with a descriptive UA and exponential backoff on 429/5xx.

    Honors a numeric Retry-After header when present; otherwise backs off
    exponentially (capped). Raises the last error if all retries are exhausted.
    """
    headers = {"User-Agent": USER_AGENT}
    delay = base_delay
    last_exc: Exception | None = None
    for _ in range(max_retries):
        try:
            resp = requests.get(url, timeout=60, headers=headers)
        except requests.RequestException as e:
            last_exc = e
            time.sleep(delay)
            delay = min(delay * 2, 60)
            continue
        if resp.status_code == 200:
            return resp
        if resp.status_code in (429, 500, 502, 503, 504):
            retry_after = resp.headers.get("Retry-After", "")
            wait = float(retry_after) if retry_after.isdigit() else delay
            last_exc = requests.HTTPError(f"arXiv returned {resp.status_code}", response=resp)
            time.sleep(wait)
            delay = min(delay * 2, 60)
            continue
        resp.raise_for_status()
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("arXiv request failed after retries")


@dataclass
class ArxivPaper:
    arxiv_id: str
    title: str
    authors: List[str]
    abstract: str
    submitted: datetime
    categories: List[str]
    pdf_url: str
    abs_url: str


def search(query: str, max_results: int = 100, start: int = 0) -> List[ArxivPaper]:
    """Search arXiv, sorted by submission date descending."""
    params = {
        "search_query": query,
        "start": str(start),
        "max_results": str(max_results),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    resp = _get_with_retry(url)
    return _parse(resp.text)


def search_since(
    query: str,
    since: datetime,
    page_size: int = 100,
    max_pages: int = 20,
) -> Iterator[ArxivPaper]:
    """Iterate papers whose submission date is on or after `since`.

    arXiv returns results sorted by submission date descending, so we can
    stop as soon as we encounter a paper older than the cutoff.
    """
    start = 0
    pages = 0
    while pages < max_pages:
        batch = search(query, max_results=page_size, start=start)
        if not batch:
            return
        for paper in batch:
            if paper.submitted < since:
                return
            yield paper
        if len(batch) < page_size:
            return
        start += page_size
        pages += 1
        time.sleep(3)


def _parse(xml_text: str) -> List[ArxivPaper]:
    root = ET.fromstring(xml_text)
    papers: List[ArxivPaper] = []
    for entry in root.findall("atom:entry", NS):
        id_el = entry.find("atom:id", NS)
        title_el = entry.find("atom:title", NS)
        summary_el = entry.find("atom:summary", NS)
        published_el = entry.find("atom:published", NS)
        if id_el is None or title_el is None or summary_el is None or published_el is None:
            continue

        full_id = id_el.text.rsplit("/", 1)[-1]
        arxiv_id_base = full_id.split("v")[0] if "v" in full_id else full_id

        title = " ".join((title_el.text or "").split())
        abstract = " ".join((summary_el.text or "").split())
        submitted = datetime.fromisoformat(published_el.text.replace("Z", "+00:00"))

        authors = [
            (a.find("atom:name", NS).text or "").strip()
            for a in entry.findall("atom:author", NS)
            if a.find("atom:name", NS) is not None
        ]
        categories = [
            c.get("term") for c in entry.findall("atom:category", NS) if c.get("term")
        ]

        abs_url = ""
        pdf_url = ""
        for link in entry.findall("atom:link", NS):
            rel = link.get("rel")
            title_attr = link.get("title")
            href = link.get("href") or ""
            if rel == "alternate":
                abs_url = href
            elif title_attr == "pdf":
                pdf_url = href

        papers.append(
            ArxivPaper(
                arxiv_id=arxiv_id_base,
                title=title,
                authors=authors,
                abstract=abstract,
                submitted=submitted,
                categories=categories,
                pdf_url=pdf_url,
                abs_url=abs_url or f"https://arxiv.org/abs/{arxiv_id_base}",
            )
        )
    return papers
