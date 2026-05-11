# Publications

Structured data for the curated publications list. Two views of the same data:

- [`papers.yml`](papers.yml) — the canonical source of truth. One entry per paper.
- [`papers.bib`](papers.bib) — BibTeX export, suitable for direct import into Zotero, Mendeley, or LaTeX.

## Schema

Each entry in `papers.yml`:

```yaml
- title: "Paper Title"
  authors: ["Last, First", "Last, First"]
  year: 2026
  venue: "NeurIPS"                  # conference / journal / "arXiv"
  layer:                            # one or more thematic sections
    - "execution-shell"
    - "supply-chain"
  url: "https://arxiv.org/abs/..."
  code: "https://github.com/..."    # optional
  summary: "One-sentence contribution + why it matters here."
```

### Layer tags

Use kebab-case, matching the [README contents](../README.md#contents):

| Tag | Section |
|---|---|
| `foundations` | Foundations & Mental Models |
| `execution-shell` | Execution Shell |
| `coordination` | Coordination Layer |
| `tool-interface` | Environment & Tool Interfaces |
| `memory` | Memory & Context Integrity |
| `observation-eval` | Observation, Tracing & Evaluation |
| `permissions` | Permissions & Least Privilege |
| `intent` | Intent Compilation |
| `transactional-agency` | Transactional Agency |
| `supply-chain` | Agent Supply Chain Security |
| `red-team` | Red Teaming for Agentic Systems |
| `oversight` | Human Oversight at Scale |
| `architectures` | Reference Architectures & Case Studies |

A paper may have multiple layer tags — that's expected and useful for cross-community work.

### Venue tags (for the by-venue view)

Use the standard short form: `NeurIPS`, `ICML`, `ICLR`, `S&P`, `USENIX Security`, `CCS`, `NDSS`, `OSDI`, `SOSP`, `FSE`, `ICSE`, `arXiv`, etc.

## Adding a paper

1. Append your entry to `papers.yml`, sorted by year (most recent first) within each layer when the renderer is enabled.
2. Add a corresponding BibTeX entry to `papers.bib`.
3. Also add a one-line reference under the relevant section in the main [`README.md`](../README.md).

See [CONTRIBUTING.md](../CONTRIBUTING.md#paper) for the editorial bar.

## Renderer (planned)

A small script that reads `papers.yml` and renders two views — by-layer and by-venue — to markdown will be added in a future revision. For v1, the YAML is the source of truth and entries are also listed manually in `README.md`.
