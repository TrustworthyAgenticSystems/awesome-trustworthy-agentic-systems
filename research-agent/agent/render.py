"""Render classified papers into a draft YAML file ready for PR review.

The agent never writes to papers/papers.yml. It writes to
papers/drafts/<mode>-<date>.yml, opens a PR, and lets a human reviewer
migrate accepted entries into papers.yml.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List

import yaml


def render_draft(entries: Iterable[dict], output_path: Path, mode: str) -> int:
    """Write classified entries to a draft file. Returns the count written."""
    entry_list: List[dict] = list(entries)
    if not entry_list:
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    header = (
        f"# Drafted by research-agent in {mode} mode at {timestamp}\n"
        f"# Review each entry before merging into papers/papers.yml.\n"
        f"# Drop entries that fail the editorial bar; correct entries that don't quite fit.\n"
        f"# When merging, also add a corresponding BibTeX entry to papers/papers.bib\n"
        f"# and delete this draft file.\n\n"
    )
    body = yaml.safe_dump(
        {"papers": entry_list},
        sort_keys=False,
        allow_unicode=True,
        width=120,
    )
    output_path.write_text(header + body)
    return len(entry_list)
