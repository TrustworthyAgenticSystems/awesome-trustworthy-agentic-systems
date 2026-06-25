# `site/` — the static website

The browse / filter / search front-end for the resource. It is the "Website"
box of the architecture: it reads the structured data and lets people explore it
by **harness layer** (where in the stack) and by **SPRS guarantee** (security,
privacy, reliability, safety), plus type, open problem, and free-text search.

## How it works

- `scripts/build_site.py` reads `data/` + `taxonomy.yml` and writes
  `site/entries.json` (published entries only, plus facet label maps). This is
  the single build step.
- `index.html`, `style.css`, `app.js` are static. `app.js` fetches
  `entries.json` at runtime and renders the faceted list client-side. No
  framework, no bundler, no Node dependency.

`entries.json` is a generated artifact and is git-ignored. It is rebuilt in CI
and on deploy, so it is never committed.

## Preview locally

```bash
python scripts/build_site.py     # writes site/entries.json
python -m http.server 8000 -d site
# open http://localhost:8000
```

(Open it through a web server, not as a `file://` URL — the page fetches
`entries.json`, which browsers block over `file://`.)

## Deploy

`.github/workflows/deploy-pages.yml` builds `entries.json` and publishes `site/`
to GitHub Pages on every push to `main` that touches `data/`, `site/`,
`taxonomy.yml`, or the build script.

One-time setup: **Settings → Pages → Source: GitHub Actions**. Pages on a private
repo requires a plan that supports it; otherwise make the repo public first.
