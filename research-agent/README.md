# Research agent

A deep-research agent that bootstraps the publications list from seed researchers + arXiv, then runs daily incremental scans. The agent **drafts**; humans **curate**. Every run produces a PR against `papers/drafts/`; nothing is auto-merged into `papers/papers.yml`.

## Modes

| Mode | What it does | Triggered by |
|---|---|---|
| **`bootstrap`** | One-shot. For each researcher in `config/seed_researchers.yml`, fetch their Semantic Scholar publications from the last N years (default 3). Also fetch arXiv submissions matching `config/keywords.yml` over the same window. Dedupe, classify, draft. Expect a few hundred candidates and ~$1–3 in Claude API cost. | Manual via workflow_dispatch |
| **`daily`** | Incremental. Fetch arXiv submissions from the last 24 hours matching the keyword set. Dedupe, classify, draft. Expect 10–50 candidates per day. | Daily cron + manual |

## How it runs

GitHub Actions, defined in [`.github/workflows/research-sweep.yml`](../.github/workflows/research-sweep.yml):

- **Daily cron** (09:00 UTC) → runs `daily` mode → opens a PR if any candidates pass classification.
- **Manual dispatch** (Actions tab → Research sweep → Run workflow) → choose `bootstrap` or `daily`. Use `bootstrap` for the first run after seeding `config/seed_researchers.yml`.

### Required GitHub secrets

| Secret | Purpose | Required? |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude API key for classification | **Required** |
| `S2_API_KEY` | Semantic Scholar API key for higher rate limits | Optional (only for bootstrap on large seed lists) |

Set these in **Settings → Secrets and variables → Actions**.

### Required repo setting

The workflow uses `peter-evans/create-pull-request` to open a PR with drafts. This requires:

> **Settings → Actions → General → Workflow permissions → check "Allow GitHub Actions to create and approve pull requests"**

Without this, the workflow's sweep step runs successfully but the PR step fails with a permissions error.

## Configuration

### `config/seed_researchers.yml`
**You populate this.** Names of researchers whose publications should be ingested wholesale during bootstrap. Curatorial judgment — don't add a name unless you've confirmed their work fits the harness-layer taxonomy. v1 ships empty.

### `config/keywords.yml`
Keyword sets per harness layer, used to query arXiv. Terms are OR'd at the abstract level, AND'd with arXiv categories (`cs.AI`, `cs.CR`, `cs.LG`, `cs.SE`, `cs.DC`, `cs.OS`). Edit if you find the daily sweep is too noisy or missing items.

### `config/sources.yml`
Per-source enable toggles. Secrets are passed via env vars (above), not committed here.

## What the agent decides vs what you decide

| Decision | Made by |
|---|---|
| Which sources to query | Config (you) |
| Which researchers to include | `seed_researchers.yml` (you) |
| Which fetched papers match the topic | Claude (classification) |
| Which classified papers end up in `papers.yml` | Human reviewer of the PR (you) |

The agent never writes to `papers/papers.yml` directly. It writes to `papers/drafts/<mode>-<date>.yml` and opens a PR. You review, prune, and migrate accepted entries into `papers.yml` (plus a BibTeX entry in `papers.bib`), then delete the draft file when merging.

## Costs

Default model is `claude-haiku-4-5` (override via `CLASSIFIER_MODEL` env var; `claude-sonnet-4-6` gives higher classification quality at ~3× the cost). The classifier system prompt is intentionally long enough to cross Haiku 4.5's minimum cacheable prefix, so after the first call per run you pay only the cache-read rate.

Rough estimates (Haiku 4.5, prompt caching active):

| Mode | Calls | Approx cost |
|---|---|---|
| Bootstrap (~500 papers, 3-year backfill) | ~500 | ~$0.50–$1.00 |
| Daily | ~10–50 | ~$0.02–$0.10 |

## First-run checklist

Before the cron starts producing useful PRs:

1. **Set the `ANTHROPIC_API_KEY` secret** (above).
2. **Enable PR-creation permissions** (above).
3. **Populate `config/seed_researchers.yml`** with ~5–15 researchers whose work fits.
4. **Manually trigger a `bootstrap` run** to validate end-to-end before the cron picks up:
   - Actions tab → Research sweep → Run workflow → mode: `bootstrap`
5. **Review the resulting PR** — sanity-check the classifier quality on a few entries.
6. Once you're comfortable with output quality, let the daily cron run.

If classification quality is too aggressive (lots of low-quality drafts) or too conservative (missing on-topic papers), tune the system prompt in `agent/classify.py` and/or the keyword set in `config/keywords.yml`.

## Running locally

```bash
cd research-agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python sweep.py daily         # incremental sweep, writes to ../papers/drafts/
python sweep.py bootstrap --years 3
```

Status output (last line of stdout) is JSON: `{"mode": "daily", "entries": 5}`.

## Code layout

```
research-agent/
├── config/
│   ├── seed_researchers.yml  # you populate
│   ├── keywords.yml          # tune as the field shifts
│   └── sources.yml           # per-source toggles
├── agent/
│   ├── fetchers/
│   │   ├── arxiv.py          # arXiv API client (deterministic, no LLM)
│   │   └── semantic_scholar.py
│   ├── classify.py           # Claude API: keep/skip + layer + summary
│   ├── dedup.py              # match against existing papers.yml
│   └── render.py             # write to papers/drafts/
└── sweep.py                  # CLI entry point
```

Fetch / dedupe / render are deterministic and free. Only `classify.py` calls Claude, exactly once per candidate paper.

## Adding a new source

1. Add a fetcher module in `agent/fetchers/` returning a uniform paper shape (`title`, `authors`, `abstract`, `year`, `venue`, `url`, optional `arxiv_id` / `doi`).
2. Wire it into `sweep.py` (`run_bootstrap` and/or `run_daily`).
3. Add an enable toggle in `config/sources.yml`.

The classifier is source-agnostic — it only needs title + abstract + authors + venue.

## Editorial bar

See [CONTRIBUTING.md](../CONTRIBUTING.md). The classifier's system prompt encodes the same bar: peer-reviewed venues or reputable preprints with substantive systems-engineering content; out-of-scope for pure model-side alignment, capability-only papers, marketing, or workshop posters without methodology.
