# `site/` — the static website

The front-end for the resource. It reads the structured data and lets people
explore it by **harness layer** (where in the stack) and by **SPRS guarantee**
(security, privacy, reliability, safety), plus type, open problem, and free-text
search.

## Pages

- `index.html` — **Home.** Landing page: hero, live stat counters (from
  `entries.json`), SPRS browse cards, and the two-track explainer.
- `resources.html` — **Resources.** The curated map (canon: papers, classics,
  courses, open source). Faceted sidebar + search. Excludes incidents.
- `incidents.html` — **Incidents.** The incident log plus a community
  "Report an incident" call to action that opens the GitHub incident issue
  template. Shows only `type: incidents` entries.

## How it works

- `scripts/build_site.py` reads `data/` + `taxonomy.yml` and writes
  `site/entries.json` (published entries only, plus facet label maps). This is
  the single build step.
- The three HTML pages, `style.css`, `app.js`, `home.js`, and `nav.js` are
  static. `app.js` powers both the Resources and Incidents lists, switching on
  `<body data-view>`; it fetches `entries.json` at runtime and renders
  client-side. `home.js` fills the homepage counters; `nav.js` drives the mobile
  nav toggle. No framework, no bundler, no Node dependency.
- The SPRS cards on the homepage link to `resources.html?sprs=<axis>`; `app.js`
  reads taxonomy facets from the query string and preselects them.

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
