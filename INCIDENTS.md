# Incidents Log

A curated, primary-source-verified log of documented failures in agentic systems. The aim is to build a shared reference for what *actually* goes wrong in deployment — and which harness layer the failure exposed.

**Editorial bar:** Every entry must have a primary source (vendor advisory, postmortem, peer-reviewed analysis, or formal disclosure). Unverified reports do not appear here. See [CONTRIBUTING.md](CONTRIBUTING.md#incident) for the entry template.

**Layer tags** map to the [README sections](README.md#contents): `execution-shell`, `coordination`, `tool-interface`, `memory`, `observation-eval`, `permissions`, `intent`, `transactional-agency`, `supply-chain`, `red-team`, `oversight`.

---

## 2026

### 2026-03-31 — Claude Code source code exposed via npm source map
- **System:** Anthropic Claude Code (`@anthropic-ai/claude-code` npm package, v2.1.88)
- **Layer affected:** `supply-chain`
- **Failure class:** Misconfigured release artifact (build/CI configuration)
- **What happened:** Version 2.1.88 of the Claude Code npm package shipped with a JavaScript source map (`.map`) file that referenced the agent's full, unobfuscated TypeScript source — roughly 512,000 lines across about 1,900 files. The Bun bundler the project uses generates source maps by default, and the artifact was not excluded from the published package, so anyone who downloaded it could reconstruct internal functions, comments, and non-public control flow. Security researcher Chaofan Shou disclosed it publicly, and Anthropic pulled the release within hours.
- **Why it matters:** The model didn't fail. The harness around it did. What was exposed was not weights but **tool integrations, control logic, permission assumptions, and operational scaffolding** — the very layer this list is about. The fix wasn't retraining; it was packaging hygiene (excluding `.map` files, auditing `npm pack` output, disabling production source maps). As coding agents accelerate release velocity, familiar software-engineering surfaces — packaging defaults, build hygiene, release automation — become the highest-leverage failure points.
- **Primary source:** [InfoWorld — "Anthropic employee error exposes Claude Code source"](https://www.infoworld.com/article/4152856/anthropic-employee-error-exposes-claude-code-source.html) (April 2026). Anthropic issued no formal advisory; it characterized the event as "a release packaging issue caused by human error, not a security breach."
- **Further reading:** [InfoQ — "Anthropic Accidentally Exposes Claude Code Source via npm Source Map File"](https://www.infoq.com/news/2026/04/claude-code-source-leak/).
- **Generalizable lesson:** *If agents are software systems, then AI security must include software systems security.* Human review cannot keep pace with AI-generated release velocity; packaging defaults and build automation deserve the same scrutiny as model behavior.

---

## How to add an entry

See the [incident template in CONTRIBUTING.md](CONTRIBUTING.md#incident). Open an issue using the [`incident` template](.github/ISSUE_TEMPLATE/incident.yml), or open a PR adding an entry under the correct year heading. Entries are sorted by date, most recent first.

## Automated incident sweeping

A scheduled agent design lives in [`scheduled/incident-sweeper.md`](scheduled/incident-sweeper.md). The agent surveys vendor advisories, arXiv, AI Incident Database, MITRE ATLAS, and curated researcher feeds; drafts candidate entries into a pending file; and opens a PR for human review. **The sweeper is intentionally not wired up in v1** — its prompt and source list are versioned here for review before activation.
