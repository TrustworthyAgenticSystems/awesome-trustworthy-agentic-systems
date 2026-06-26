# Research agent — design

This document explains how the research agent is built and why. For setup,
secrets, and how to run it, see [`README.md`](README.md).

## Purpose

The research agent is the **live-feed** half of the resource. It keeps the
publications list current by surveying arXiv and Semantic Scholar, proposing
new entries that fit the trustworthy-agentic-systems frame. It exists to solve
one problem: a hand-curated list goes stale, but auto-publishing erodes trust.

The agent resolves that tension with a single rule:

> **The agent proposes; a human disposes.**

It can only ever open a pull request full of `status: draft` entries. It never
writes a published entry, never merges, and never touches the live site. Every
output passes the same two gates as a human contribution: the validator, then a
human reviewer.

This mirrors the resource's own thesis — agents act inside a trusted base that
validates them, and every action is attributable.

## Where it sits in the overall architecture

```
            ┌─────────────────────────── research-agent/ ──────────────────────────┐
arXiv  ─┐   │                                                                       │
        ├──▶│  fetch ──▶ dedup ──▶ classify (LLM) ──▶ render ──▶ data/papers/drafts/ │
S2     ─┘   │  (free, deterministic)        ▲                    (status: draft)     │
            └───────────────────────────────┼───────────────────────────────────────┘
                                            one model call per surviving paper
                                                     │
   agent-draft PR  ◀── scripts/validate.py ◀─────────┘
        │
        ▼  (human reviews, promotes)
   data/papers/<id>.yml  ──▶ scripts/generate.py ──▶ README + papers.bib
   (status: published)   ──▶ scripts/build_site.py ──▶ the website
```

The agent owns only the left box. Everything downstream of the draft is shared
with the human-contribution path.

## The pipeline

The whole run is six stages. Five are deterministic and free; only one calls a
model.

### 1. Fetch — `agent/fetchers/`

Two sources, both returning a uniform paper shape (`title`, `authors`,
`abstract`, `year`, `venue`, `url`, optional `arxiv_id` / `doi`):

- **`arxiv.py`** queries the arXiv API. The query is built in `sweep.py`
  (`build_arxiv_query`): the per-layer terms in `config/keywords.yml` are OR'd
  at the abstract level and AND'd with the category filter
  (`cs.AI, cs.CR, cs.LG, cs.SE, cs.DC, cs.OS`). Results are paged newest-first;
  `search_since` stops as soon as it crosses the date cutoff. The client sends a
  descriptive User-Agent and retries with exponential backoff on `429`/`5xx`
  (arXiv rate-limits by IP and throttles blank User-Agents).
- **`semantic_scholar.py`** resolves each name in `config/seed_researchers.yml`
  to an author id, then pulls that author's recent papers.

Fetch is pure I/O. No model is involved, so it is free and reproducible.

### 2. Dedup — `agent/dedup.py`

Each candidate gets up to three identity keys, any of which is a match:
`arxiv:<id>`, `doi:<lowercased>`, `title-author:<normalized-title>:<first-author>`.

`load_existing_keys(data/)` and `load_existing_ids(data/)` scan every entry file
under `data/` **recursively** (so prior drafts in `data/papers/drafts/` count
too). Candidates matching an existing key, or each other within a run, are
dropped before they cost a model call.

### 3. Classify — `agent/classify.py`  (the only LLM step)

One model call per surviving candidate. The model is forced into a Pydantic
`Classification` via structured output (`response_schema`), so the result is
validated at the API boundary and needs no parsing:

```python
class Classification(BaseModel):
    keep: bool                       # in scope for the resource?
    harness_layer: LayerTag          # primary structural facet (or "out-of-scope")
    sprs: list[SprsTag]              # guarantee facet: 1–2 of security/privacy/reliability/safety
    open_problems: list[...]         # 0–2 of the white paper's open problems
    confidence: float                # 0–1, for reviewer triage
    summary: str                     # one sentence, our words
    reason: str                      # why keep/skip
```

The model assigns **both required facets** the schema demands on every entry: a
primary `harness_layer` (where in the stack) and one or two `sprs` guarantees
(what property). The editorial bar — what is in scope, what is not, and ten
worked keep/skip examples — lives in the system prompt. The bar is deliberately
strict: a false negative can be re-added by a contributor, a false positive
erodes the list's credibility.

Defaults: `gemini-2.5-flash` (override with `CLASSIFIER_MODEL`), `temperature=0`
for stable classification. The system prompt is large and identical across every
call in a run, so the provider's implicit prefix caching makes all calls after
the first bill at the cached rate.

This is the **only** place a provider API is touched. Swapping back to Claude or
to another model changes this file and the secret name, nothing else.

### 4. Render — `agent/render.py`

Each kept candidate becomes one schema-valid file, `data/papers/drafts/<id>.yml`:

- `id` is a stable slug (`slugify`): `<year>-<first-8-title-words>`, matching the
  schema's id pattern, de-duplicated against existing ids with a `-2` suffix.
- `provenance.added_by: agent`, `drafted_by: research-agent`, plus the model's
  `confidence` and `reason` (as `rationale`).
- `status: draft`.

`_build_entry` is defensive: if a candidate has no usable `harness_layer`, no
`sprs`, or a summary shorter than the schema minimum, it is **dropped with a
warning** rather than written as invalid YAML. The agent cannot emit something
the validator would reject.

### 5. Gate + PR — `.github/workflows/research-sweep.yml`

After the sweep writes drafts, the workflow runs `scripts/validate.py
--skip-urls` over them (schema, taxonomy, dedup, the publish/incident gates),
then opens a pull request labeled `agent-draft`. The PR is created with a
fine-grained PAT (`AGENT_PAT`) rather than the default Actions token, for two
reasons: the org policy blocks the Actions token from creating PRs, and a
PAT-created PR triggers the **Validate entries** workflow on the new PR (a
token-created PR would not).

### 6. Human promote

A reviewer reads the draft, checks the source and tags, and either:

- **accepts** — move the file to `data/papers/<id>.yml`, set `status: published`,
  record `provenance.reviewed_by`; or
- **rejects** — delete the draft file.

On the next push to `main`, `scripts/generate.py` and `scripts/build_site.py`
fold published entries into the README, `papers.bib`, and the website. Drafts
never reach those artifacts: the generators read `data/<type>/*.yml`
non-recursively and render only `status: published`, so the `drafts/` subfolder
is invisible to them even though the validator gates it.

## Modes

`sweep.py` has two entry points, selected by the workflow:

| Mode | Sources | Window | Trigger | Expected volume |
|---|---|---|---|---|
| `bootstrap` | seed authors (S2) + arXiv | last N years (default 3) | manual dispatch | hundreds, one-shot |
| `daily` | arXiv only | last ~24h | cron (09:00 UTC) + manual | tens per day |

`bootstrap` seeds the list from a backfill; `daily` keeps it fresh. Both run the
identical fetch → dedup → classify → render → PR pipeline.

## Configuration — `config/`

- **`keywords.yml`** — per-harness-layer arXiv search terms. Tighter terms mean
  fewer wasted classifier calls; the classifier still filters off-topic hits.
- **`seed_researchers.yml`** — names whose publications to ingest wholesale in
  `bootstrap`. Curatorial: an off-topic name produces many skipped
  classifications (wasted spend). Ships empty; arXiv keyword sweep works without
  it.
- **`sources.yml`** — per-source on/off toggles. Secrets come from env vars, not
  this file.

## Design properties

- **Deterministic shell, isolated brain.** Fetch, dedup, and render are pure
  code: free, reproducible, testable without an API key. The single
  nondeterministic step is quarantined in `classify.py`.
- **Provider-swappable.** Only `classify.py`, `requirements.txt`, and the
  workflow secret name know which model is used. Fetchers, dedup, render, and the
  CLI are provider-agnostic.
- **Fail-soft.** A failed fetch, a failed classification, or an unrenderable
  candidate is logged and skipped; the run still completes and reports a count.
  One bad paper never aborts a sweep.
- **Gated twice, always.** Validator then human. The agent's most privileged
  action is opening a draft PR.
- **Attributable.** Every draft records `added_by: agent`, the drafting agent id,
  a confidence, and a rationale, so a reviewer can see what the agent thought and
  why.

## Failure modes and how they are handled

| Failure | Handling |
|---|---|
| arXiv `429` / blank-UA throttle | descriptive User-Agent + exponential backoff honoring `Retry-After` (`arxiv.py:_get_with_retry`) |
| Model API error on one paper | caught per-paper in `_classify_and_filter`, logged, skipped |
| Model **daily quota** exhausted (free tier) | surfaces as repeated `429 RESOURCE_EXHAUSTED`; not retriable within the day — requires a paid tier for bootstrap volumes |
| Candidate already listed | dropped in dedup before any model call |
| Model returns an out-of-scope or thin result | `keep: false` skip, or dropped in render if it can't be made schema-valid |
| Duplicate generated id | suffixed `-2`, `-3`, … in render |

## Extension points

- **New source:** add a fetcher under `agent/fetchers/` returning the uniform
  paper shape, wire it into `sweep.py`, add a toggle in `config/sources.yml`. The
  classifier is source-agnostic.
- **New model / provider:** change `MODEL` (or `CLASSIFIER_MODEL`) and the client
  in `classify.py`, update `requirements.txt`, and set the matching secret.
- **Tuning recall vs precision:** edit the system prompt in `classify.py` (the
  editorial bar) and/or the term sets in `config/keywords.yml`.

## Non-goals

- It does not publish. It cannot set `status: published` or merge.
- It does not rebuild incident databases; incident sourcing is handled
  separately (see [`../scheduled/incident-sweeper.md`](../scheduled/incident-sweeper.md)).
- It does not replace editorial judgment. Confidence and rationale inform a human;
  they do not authorize anything.
