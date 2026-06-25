# Contributing

Thanks for considering a contribution. This list aims to be a credible, research-adjacent reference for both engineers and academics — so editorial standards matter. Please read this guide before opening a PR.

## What we accept

| Type | Accepted | Borderline | Rejected |
|---|---|---|---|
| **Papers** | Peer-reviewed venues; reputable preprints (arXiv with clear methodology) | Workshop papers, technical reports from established labs | Marketing whitepapers, undated blog posts, AI-generated summaries |
| **Tools / repos** | Active projects with documentation, real users or production deployments | New projects with clear technical depth | Abandoned repos, vaporware, demos with no implementation |
| **Incidents** | Documented with primary source (vendor advisory, postmortem, peer-reviewed analysis) | Reported in reputable outlet with verifiable detail | Unverified X/social posts, hearsay, speculation |
| **Talks / writeups** | Recorded talks from established venues; long-form analysis with technical substance | Conference workshops, well-cited blog posts | Generic introductions, recycled content |
| **Standards** | Published by recognized bodies (NIST, ISO, MITRE, IETF, OWASP) | Industry-coalition drafts | Vendor "frameworks" with no external adoption |

The bar is **substance + primary-source verifiability**, not popularity.

## How to contribute

### Option A — Open an issue (preferred for first-time contributors)
Use one of the [issue templates](.github/ISSUE_TEMPLATE/) — paper, incident, resource, or taxonomy proposal. A maintainer will review and either add it directly or invite you to open a PR.

### Option B — Open a PR directly
For maintainers and frequent contributors. Follow the entry templates below.

## Entry templates

> **The README is generated, not hand-edited.** The single source of truth is one
> YAML file per entry under [`data/<type>/`](data/). The `### Resources` lists in
> `README.md` and the BibTeX in `papers/papers.bib` are produced from `data/` by
> `python scripts/generate.py`. Do not edit the content between the `AUTOGEN`
> markers in `README.md` by hand — it will be overwritten. See
> [`data/README.md`](data/README.md) for the data model.

### Add an entry (papers, classics, courses, oss)
1. Copy [`templates/entry.template.yml`](templates/entry.template.yml) to
   `data/<type>/<id>.yml`.
2. Tag it against [`taxonomy.yml`](taxonomy.yml). Both facets are required:
   `harness_layer` (>=1) and `sprs` (>=1).
3. Run `python scripts/validate.py` (schema, taxonomy, dead links, dedup), then
   `python scripts/generate.py` to refresh `README.md` and `papers/papers.bib`.
4. Commit the entry **and** the regenerated `README.md` / `papers.bib`. CI fails if
   they are out of sync (`scripts/generate.py --check`).

Example entry shape (`data/papers/2026-example.yml`):

```yaml
id: 2026-example
type: papers
title: "Paper Title"
url: "https://arxiv.org/abs/..."
code: "https://github.com/..."   # optional
authors: ["Firstname Lastname", "Firstname Lastname"]
venue: "USENIX Security"
year: 2026
summary: >
  One to four sentences, in your own words, on the contribution and why it
  matters here. Never paste the abstract.
harness_layer: ["execution-shell"]   # one or more of the 13 sections
sprs: ["security"]                    # one or more of: security, privacy, reliability, safety
provenance:
  added_by: human
  drafted_by: your-handle
status: draft
```

### Incident
Add to [`INCIDENTS.md`](INCIDENTS.md). Required fields:

```markdown
### YYYY-MM-DD — Short descriptive title
- **System:** What product / project / pipeline
- **Layer affected:** Which harness layer (Execution Shell, Supply Chain, etc.)
- **Failure class:** Brief category (misconfigured release, prompt injection, etc.)
- **What happened:** 2–4 sentences
- **Why it matters:** 1–2 sentences on the generalizable lesson
- **Primary source:** Link to vendor advisory / postmortem / paper
- **Further reading:** Optional additional analysis links
```

**Do not** add incidents without a primary source. Unverified reports get rejected.

### Tool / repo
Add to the relevant section in `README.md`:

```markdown
- **Project name** — one-line description. Why it matters for this layer. [[repo]](url) `[tool]`
```

## Editorial principles

1. **One-line entries.** If you can't summarize the contribution in one sentence, the entry isn't ready.
2. **Primary sources.** Link to the paper, the vendor advisory, the canonical repo — not aggregators or news coverage.
3. **No fabrication.** If you don't have verified information (correct authors, correct venue, working URL), don't add the entry.
4. **Substance over hype.** "State-of-the-art", "revolutionary", and "groundbreaking" don't belong in entries. Describe the actual contribution.
5. **Cross-community framing.** When a paper crosses communities (e.g., systems + ML), mention both lenses in the summary.
6. **Currency.** Items older than ~5 years get included only if they remain canonical references.

## Style

- Use US English.
- Capitalize section names in `Title Case`.
- Use `kebab-case` for layer tags in YAML.
- Sort entries within a subsection by year (most recent first), then alphabetically by first author.
- Prefer `[paper]`, `[tool]`, `[talk]`, `[postmortem]`, `[standard]`, `[dataset]` as type tags.

## Review process

- Maintainers aim to review within 7 days.
- Substantive disagreements (taxonomy placement, editorial fit) are discussed in the PR comments — please don't take a request for revision personally.
- For contested incidents or claims, we err on the side of *not* including until primary-source verification is clear.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## Licensing of contributions

By contributing, you agree that your code contributions are licensed under [MIT](LICENSE) and your content contributions (markdown, YAML, prose) are licensed under [CC BY 4.0](LICENSE-CONTENT).
