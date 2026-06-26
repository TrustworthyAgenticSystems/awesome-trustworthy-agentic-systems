# Backfill staging

Candidate pools from one-shot `bootstrap` sweeps, kept here so the work is not
lost. These are **not** entries: they are raw classifier output awaiting triage.
Nothing here is rendered to the README or the website (the generators read only
`data/<type>/*.yml`).

## `2026-bootstrap-candidates.jsonl`

The 1-year arXiv keyword bootstrap (run #50) collected 2,000 recent candidates
and the classifier kept 1,491. That is far too many to publish into a curated
list, so instead of opening 1,491 draft files we stage them here as one record
per line, sorted by confidence (descending).

Each line has: `id`, `title`, `url`, `authors`, `venue`, `year`, `summary`,
`harness_layer`, `sprs`, `open_problems`, `confidence`, `rationale`.

By layer: coordination 315, observation-eval 230, red-team 220, memory 189,
architectures 152, foundations 110, oversight 69, tool-interface 67,
execution-shell 67, permissions 33, supply-chain 24, intent 11,
transactional-agency 4.

### How to triage

A follow-up promotes a small, high-value subset into `data/papers/` (e.g. the
under-represented layers + highest confidence), then the rest stays archived
here for reference. Read the file, filter, and write the kept records as normal
entries:

```bash
python - <<'PY'
import json
rows = [json.loads(l) for l in open("research-agent/backfill/2026-bootstrap-candidates.jsonl")]
thin = {"transactional-agency","intent","permissions","supply-chain"}
picks = [r for r in rows if (r.get("confidence") or 0) >= 0.9
         and thin & set(r.get("harness_layer") or [])]
print(len(picks))
PY
```

Caveat: classifier summaries and tags are proposals. Verify the source, reword
the summary, and confirm both facets before publishing any of these.
