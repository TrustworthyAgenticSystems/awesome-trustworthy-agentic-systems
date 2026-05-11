# Incidents Log

A curated, primary-source-verified log of documented failures in agentic systems. The aim is to build a shared reference for what *actually* goes wrong in deployment — and which harness layer the failure exposed.

**Editorial bar:** Every entry must have a primary source (vendor advisory, postmortem, peer-reviewed analysis, or formal disclosure). Unverified reports do not appear here. See [CONTRIBUTING.md](CONTRIBUTING.md#incident) for the entry template.

**Layer tags** map to the [README sections](README.md#contents): `execution-shell`, `coordination`, `tool-interface`, `memory`, `observation-eval`, `permissions`, `intent`, `transactional-agency`, `supply-chain`, `red-team`, `oversight`.

---

## 2025

### 2025-03 — Claude Code source map exposure
- **System:** Anthropic Claude Code (npm package distribution)
- **Layer affected:** `supply-chain`
- **Failure class:** Misconfigured release artifact (build/CI configuration)
- **What happened:** The Claude Code npm package was published with JavaScript `.map` (source map) files included by default. Source maps in modern web development bridge compiled/obfuscated code back to original sources. By shipping them, the build effectively made the proprietary agent logic — internal functions, comments, and non-public control flow — fully reconstructible by anyone who downloaded the package.
- **Why it matters:** The model didn't fail. The harness around it did. What was exposed was not weights but **tool integrations, control logic, permission assumptions, and operational scaffolding** — the very layer this list is about. The fix wasn't retraining; it was updating `.npmignore` and CI scripts. As coding agents accelerate release velocity (Claude Code reached ~4% of all public GitHub commits within 13 months of preview), familiar software-engineering surfaces — packaging defaults, build hygiene, release automation — become the highest-leverage failure points.
- **Primary source:** Anthropic Security Advisory, March 2025.
- **Generalizable lesson:** *If agents are software systems, then AI security must include software systems security.* Human review cannot keep pace with AI-generated release velocity; the cognitive load of reviewing AI output at 42,000× growth rates breaks traditional assurance processes.

---

## How to add an entry

See the [incident template in CONTRIBUTING.md](CONTRIBUTING.md#incident). Open an issue using the [`incident` template](.github/ISSUE_TEMPLATE/incident.yml), or open a PR adding an entry under the correct year heading. Entries are sorted by date, most recent first.

## Automated incident sweeping

A scheduled agent design lives in [`scheduled/incident-sweeper.md`](scheduled/incident-sweeper.md). The agent surveys vendor advisories, arXiv, AI Incident Database, MITRE ATLAS, and curated researcher feeds; drafts candidate entries into a pending file; and opens a PR for human review. **The sweeper is intentionally not wired up in v1** — its prompt and source list are versioned here for review before activation.
