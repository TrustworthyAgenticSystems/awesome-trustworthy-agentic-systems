# Incident Sweeper — scheduled agent design

A weekly remote agent that drafts candidate entries for [`INCIDENTS.md`](../INCIDENTS.md) by surveying primary sources. **This is a design document — the agent is intentionally not wired up in v1.** Review the prompt and source list below before activating it via `/schedule` or an equivalent cron mechanism.

## Why this exists

The incident log is one of the highest-value sections for both researchers (case studies for papers) and practitioners (real failure modes to design against). Hand-curating it requires regularly sweeping a dozen sources. Automation drafts; humans curate.

**The agent never writes to `INCIDENTS.md` directly.** It writes to a pending file and opens a PR. A maintainer reviews the draft, verifies the primary source, and merges or rejects.

## Schedule

- **Frequency:** weekly (Monday 09:00 UTC, suggested)
- **Mechanism:** `/schedule` (Claude Code remote routine), GitHub Actions cron, or equivalent
- **Output:** A PR titled `incidents: candidates for week of YYYY-MM-DD` containing diffs to `INCIDENTS_PENDING.md`

## Sources

Tier 1 — **always check**, primary disclosures:
- Anthropic security advisories: <https://www.anthropic.com/security>
- OpenAI security advisories
- Google AI / DeepMind security disclosures
- Microsoft Security Response Center (MSRC) for Copilot / Azure AI
- Meta AI security disclosures

Tier 2 — **check weekly**, aggregated / community:
- AI Incident Database: <https://incidentdatabase.ai/>
- MITRE ATLAS case studies: <https://atlas.mitre.org/>
- arXiv cs.CR + cs.AI new submissions, last 7 days, filtered for agent / LLM / harness keywords
- OWASP LLM Top 10 advisories
- HackerNews + lobste.rs front-page items matching agent / LLM security keywords

Tier 3 — **researcher feeds**, curated:
- Simon Willison's prompt injection writeups: <https://simonwillison.net/tags/prompt-injection/>
- Embrace The Red blog
- PromptArmor disclosures
- Curated X.com accounts (auth-walled; treat as low-confidence — never include without corroboration from Tier 1 or 2)

## Agent prompt

```
You are the incident sweeper for awesome-trustworthy-agentic-systems.

Your job: identify documented agentic-systems failures from the past 7 days
and draft candidate entries for INCIDENTS_PENDING.md.

PROCESS
1. For each source in the source list below, fetch the latest items.
2. Filter for items that:
   - Involve a deployed AI agent or agentic system (not pure model output).
   - Have a primary source (vendor advisory, postmortem, or peer-reviewed
     paper). Discard items with only social-media reports.
   - Are dated within the past 7 days (or first disclosed in that window).
3. For each qualifying item, draft an INCIDENTS.md entry using the
   template below. If you cannot verify a field (system, date, primary
   source), DO NOT fabricate — mark it [NEEDS VERIFICATION].
4. Append all drafts to INCIDENTS_PENDING.md under a heading for this
   week's run.
5. Open a PR with the diff. Title: "incidents: candidates for week of
   YYYY-MM-DD". Body: list of sources checked, count of items reviewed,
   count of drafts produced.

ENTRY TEMPLATE
### YYYY-MM-DD — Short descriptive title
- **System:** [product / project / pipeline]
- **Layer affected:** [harness layer tag]
- **Failure class:** [brief category]
- **What happened:** [2-4 sentences]
- **Why it matters:** [1-2 sentences on the generalizable lesson]
- **Primary source:** [URL]
- **Further reading:** [optional]

EDITORIAL RULES (NON-NEGOTIABLE)
- No fabrication. If a fact is not verifiable from a linked primary
  source, mark it [NEEDS VERIFICATION] and let the human reviewer
  decide.
- No marketing summaries. Describe the actual technical failure.
- No speculation. If the postmortem doesn't say it, you don't say it.
- Layer-affected must map to a tag in papers/README.md. If the failure
  spans layers, list the primary one.
- Reject items where the only source is an unverified social post.

OUTPUT
PR diff against INCIDENTS_PENDING.md only. Never modify INCIDENTS.md
directly.
```

## Activation checklist (before wiring up)

- [ ] Confirm the schedule runner has read-only access to the source list and write access only to a feature branch.
- [ ] Confirm a maintainer is on the PR review rota.
- [ ] Run the agent manually once and inspect output before enabling the cron.
- [ ] Decide whether the agent should also propose updates to existing entries (e.g., new postmortem published for an old incident) or only new entries. v1 recommendation: new entries only.

## Why not auto-merge?

The repo's credibility for academic and security audiences depends on every incident being human-verified. An auto-merging sweeper would, on a long enough timeline, eventually publish a hallucinated entry — and the cost of one bad entry to the repo's reputation exceeds the savings from skipping review.
