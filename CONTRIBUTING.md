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

### Paper
Add to the relevant section in `README.md` **and** to [`papers/papers.yml`](papers/papers.yml). README format:

```markdown
- **Title** (Authors et al., Year) — one-line summary of contribution and why it matters for this section. [[paper]](url) [[code]](url) `[venue: VENUE-YEAR]`
```

YAML format in `papers/papers.yml`:

```yaml
- title: "Paper Title"
  authors: ["Last, First", "Last, First"]
  year: 2026
  venue: "NeurIPS"
  layer: "execution-shell"  # one of the 13 thematic sections, kebab-case
  url: "https://arxiv.org/abs/..."
  code: "https://github.com/..."  # optional
  summary: "One sentence on contribution and relevance."
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
