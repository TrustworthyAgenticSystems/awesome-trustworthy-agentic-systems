"""CLI entry point for the research agent.

Modes:
  bootstrap  — one-shot sweep across seed researchers + last N years of arXiv
  daily      — incremental sweep of last 24 hours on arXiv

Output: one schema-valid draft file per kept entry under
data/papers/drafts/<id>.yml, plus a final JSON status line on stdout
("{"mode": ..., "entries": N}") so the GitHub Actions workflow can decide
whether to open a PR. The agent never writes published entries; a human
reviewer promotes drafts.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, List

import yaml

# Allow `python sweep.py ...` from inside research-agent/
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent.classify import classify  # noqa: E402
from agent.dedup import (  # noqa: E402
    candidate_keys,
    is_duplicate,
    load_existing_ids,
    load_existing_keys,
)
from agent.fetchers import arxiv as arxiv_fetch  # noqa: E402
from agent.fetchers import semantic_scholar as s2_fetch  # noqa: E402
from agent.render import render_drafts  # noqa: E402


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("research-agent")

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
CONFIG = ROOT / "config"
DATA_DIR = REPO_ROOT / "data"
DRAFTS = DATA_DIR / "papers" / "drafts"


# ----- config loading ----------------------------------------------------------

def load_config():
    researchers = yaml.safe_load((CONFIG / "seed_researchers.yml").read_text()) or {}
    keywords = yaml.safe_load((CONFIG / "keywords.yml").read_text()) or {}
    sources = yaml.safe_load((CONFIG / "sources.yml").read_text()) or {}
    return researchers, keywords, sources


def _s2_api_key(sources: dict) -> str | None:
    return os.environ.get("S2_API_KEY") or (sources.get("semantic_scholar") or {}).get("api_key")


# ----- arXiv query construction ------------------------------------------------

ARXIV_CATEGORIES = ["cs.AI", "cs.CR", "cs.LG", "cs.SE", "cs.DC", "cs.OS"]


def build_arxiv_query(keywords: dict) -> str:
    cat_part = "(" + " OR ".join(f"cat:{c}" for c in ARXIV_CATEGORIES) + ")"

    terms: List[str] = []
    for layer_terms in (keywords.get("layers") or {}).values():
        terms.extend(layer_terms or [])

    seen: set = set()
    deduped_terms: List[str] = []
    for t in terms:
        if not t:
            continue
        tl = t.lower()
        if tl not in seen:
            seen.add(tl)
            deduped_terms.append(t)

    if not deduped_terms:
        return cat_part
    term_part = "(" + " OR ".join(f'abs:"{t}"' for t in deduped_terms) + ")"
    return f"{cat_part} AND {term_part}"


# ----- normalization -----------------------------------------------------------

def _entry_from_arxiv(p: "arxiv_fetch.ArxivPaper") -> dict:
    return {
        "title": p.title,
        "authors": p.authors,
        "year": p.submitted.year,
        "venue": "arXiv",
        "url": p.abs_url or f"https://arxiv.org/abs/{p.arxiv_id}",
        "_abstract": p.abstract,
        "_arxiv_id": p.arxiv_id,
        "_doi": None,
        "_first_author": p.authors[0] if p.authors else "",
    }


def _entry_from_s2(p: "s2_fetch.S2Paper") -> dict:
    url = p.url or (f"https://arxiv.org/abs/{p.arxiv_id}" if p.arxiv_id else "")
    return {
        "title": p.title,
        "authors": p.authors,
        "year": p.year,
        "venue": p.venue,
        "url": url,
        "_abstract": p.abstract or "",
        "_arxiv_id": p.arxiv_id,
        "_doi": p.doi,
        "_first_author": p.authors[0] if p.authors else "",
    }


# ----- classification pipeline -------------------------------------------------

def _classify_and_filter(
    candidates: Iterable[dict],
    existing_keys: set,
) -> List[dict]:
    """Dedupe candidates, classify each survivor, and return kept entries."""
    seen_in_run: set = set()
    kept: List[dict] = []

    for entry in candidates:
        abstract = entry.get("_abstract") or ""
        if not abstract or len(abstract) < 100:
            continue  # not enough signal to classify reliably

        keys = candidate_keys(
            entry.get("_arxiv_id"),
            entry.get("_doi"),
            entry.get("title") or "",
            entry.get("_first_author") or "",
        )
        if not keys:
            continue
        if any(k in seen_in_run for k in keys):
            continue
        if is_duplicate(keys, existing_keys):
            continue
        seen_in_run.update(keys)

        title = entry.get("title") or ""
        try:
            result = classify(
                title=title,
                abstract=abstract,
                authors=entry.get("authors") or [],
                venue=entry.get("venue"),
            )
        except Exception as e:
            log.warning("classify failed for %r: %s", title[:80], e)
            continue

        if not result.keep:
            continue

        kept.append(
            {
                "title": title,
                "authors": entry.get("authors") or [],
                "year": entry.get("year"),
                "venue": entry.get("venue") or "arXiv",
                "url": entry.get("url"),
                "harness_layer": [result.harness_layer],
                "sprs": list(result.sprs),
                "open_problems": list(result.open_problems),
                "confidence": result.confidence,
                "summary": result.summary,
                "rationale": result.reason,
            }
        )

    return kept


# ----- mode runners ------------------------------------------------------------

def run_bootstrap(years: int) -> int:
    researchers, keywords, sources = load_config()
    existing_keys = load_existing_keys(DATA_DIR)
    existing_ids = load_existing_ids(DATA_DIR)
    log.info("loaded %d existing dedup keys, %d ids", len(existing_keys), len(existing_ids))

    s2_key = _s2_api_key(sources)

    raw: List[dict] = []

    # 1) Seed researchers via Semantic Scholar
    seed = researchers.get("researchers") or []
    cutoff_year = datetime.now(timezone.utc).year - years
    log.info("sweeping %d seed researchers (years >= %d)", len(seed), cutoff_year)
    s2_enabled = (sources.get("semantic_scholar") or {}).get("enabled", True)
    if s2_enabled and seed:
        for r in seed:
            name = (r or {}).get("name")
            if not name:
                continue
            try:
                author_id = s2_fetch.find_author_id(name, s2_key)
            except Exception as e:
                log.warning("s2 author lookup failed for %s: %s", name, e)
                continue
            if not author_id:
                log.info("no s2 author match for %s", name)
                continue
            log.info("fetching papers for %s (%s)", name, author_id)
            try:
                for paper in s2_fetch.author_papers(author_id, s2_key):
                    if paper.year is not None and paper.year < cutoff_year:
                        continue
                    raw.append(_entry_from_s2(paper))
            except Exception as e:
                log.warning("s2 papers fetch failed for %s: %s", name, e)
            time.sleep(3)

    # 2) arXiv keyword backfill
    if (sources.get("arxiv") or {}).get("enabled", True):
        cutoff = datetime.now(timezone.utc) - timedelta(days=365 * years)
        query = build_arxiv_query(keywords)
        log.info("fetching arXiv since %s", cutoff.date().isoformat())
        try:
            for paper in arxiv_fetch.search_since(query, cutoff):
                raw.append(_entry_from_arxiv(paper))
        except Exception as e:
            log.warning("arXiv fetch failed: %s", e)

    log.info("collected %d raw candidates", len(raw))

    kept = _classify_and_filter(raw, existing_keys)
    log.info("classifier kept %d entries", len(kept))

    n = render_drafts(kept, DRAFTS, existing_ids)
    log.info("wrote %d draft entries to %s", n, DRAFTS)
    return n


def run_daily() -> int:
    _, keywords, sources = load_config()
    existing_keys = load_existing_keys(DATA_DIR)
    existing_ids = load_existing_ids(DATA_DIR)
    log.info("loaded %d existing dedup keys, %d ids", len(existing_keys), len(existing_ids))

    if not (sources.get("arxiv") or {}).get("enabled", True):
        log.info("arXiv disabled — nothing to sweep in daily mode")
        return 0

    cutoff = datetime.now(timezone.utc) - timedelta(days=1, hours=1)
    query = build_arxiv_query(keywords)
    log.info("fetching arXiv since %s", cutoff.isoformat())

    raw: List[dict] = []
    try:
        for paper in arxiv_fetch.search_since(query, cutoff):
            raw.append(_entry_from_arxiv(paper))
    except Exception as e:
        log.warning("arXiv fetch failed: %s", e)

    log.info("collected %d raw candidates", len(raw))

    kept = _classify_and_filter(raw, existing_keys)
    log.info("classifier kept %d entries", len(kept))

    n = render_drafts(kept, DRAFTS, existing_ids)
    if n:
        log.info("wrote %d draft entries to %s", n, DRAFTS)
    else:
        log.info("no qualifying candidates — no drafts written")
    return n


# ----- CLI ---------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Research agent for awesome-trustworthy-agentic-systems"
    )
    parser.add_argument("mode", choices=["bootstrap", "daily"])
    parser.add_argument(
        "--years",
        type=int,
        default=3,
        help="Years of backfill for bootstrap mode (default: 3)",
    )
    args = parser.parse_args()

    if args.mode == "bootstrap":
        n = run_bootstrap(years=args.years)
    else:
        n = run_daily()

    print(json.dumps({"mode": args.mode, "entries": n}))


if __name__ == "__main__":
    main()
