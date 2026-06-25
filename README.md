# awesome-trustworthy-agentic-systems

> A curated map of **trustworthy agentic systems engineering** — for builders who need the systems lens, and for researchers tracing the cross-community literature on agent harnesses, permissions, intent, and operational governance.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: MIT (code)](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0 (content)](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Why this list exists

Most existing lists on AI agents index *how to build them*. This list indexes *how to engineer them so they deserve trust*.

The thesis, drawn from the keynote *["From Models to Systems: Engineering Trustworthy AI Agents"](#talks--keynotes)* (CERIAS Annual Cybersecurity Symposium, April 2026):

> Trustworthiness is not a property of model outputs alone. Failures in agentic systems happen in the **full operational stack** — orchestration logic, tool interfaces, memory, permissions, workflows, and human oversight. Engineering trustworthy agents is therefore a *systems* problem, not just a *model* problem.

This list is organized around that reframe. Sections mirror the **harness layers** and **open engineering problems** the field needs to make progress on.

## Who this list is for

- **ML / agent builders** who already know how to wire up a model and want to understand the systems lens: sandboxing, permissions, rollback, observability, supply-chain hygiene.
- **Academic researchers** in security, systems, software engineering, and AI who are starting a research program in this space and want a map of the literature — with venue tags so the cross-community gaps are legible.
- **Practitioners** building production agents who need a reference for review checklists, threat models, and operational primitives.

If you're looking for "how to build an agent" tutorials, see [`awesome-agent-learning`](https://github.com/artnitolog/awesome-agent-learning). This list assumes you can build one and asks what it takes to deploy it responsibly.

## How to read this list

- Each section opens with the **questions it answers** and the **failure modes** it addresses. Read these first — they form the conceptual map.
- Then comes **Resources**: papers, repos, tools, write-ups. Items are tagged where helpful (`[paper]`, `[tool]`, `[talk]`, `[postmortem]`, `[standard]`).
- Publications have a separate canonical home in [`papers/`](papers/) — by-layer and by-venue views, plus a [`papers.bib`](papers/papers.bib) file for direct import into Zotero / BibTeX.
- A live [`INCIDENTS.md`](INCIDENTS.md) tracks documented real-world failures in agentic systems.

---

## Contents

**Part I — Foundations**
- [1. Foundations & Mental Models](#1-foundations--mental-models)

**Part II — The Agent Harness**
- [2. Execution Shell](#2-execution-shell)
- [3. Coordination Layer](#3-coordination-layer)
- [4. Environment & Tool Interfaces](#4-environment--tool-interfaces)
- [5. Memory & Context Integrity](#5-memory--context-integrity)
- [6. Observation, Tracing & Evaluation](#6-observation-tracing--evaluation)

**Part III — Open Engineering Problems**
- [7. Permissions & Least Privilege for Reasoning Systems](#7-permissions--least-privilege-for-reasoning-systems)
- [8. Intent Compilation](#8-intent-compilation)
- [9. Transactional Agency](#9-transactional-agency)

**Part IV — Operational Risk Surfaces**
- [10. Agent Supply Chain Security](#10-agent-supply-chain-security)
- [11. Red Teaming for Agentic Systems](#11-red-teaming-for-agentic-systems)
- [12. Human Oversight at Scale](#12-human-oversight-at-scale)

**Part V — Knowledge Base**
- [13. Reference Architectures & Case Studies](#13-reference-architectures--case-studies)
- [14. Incidents Log](INCIDENTS.md)
- [15. Publications](papers/)
- [Talks & Keynotes](#talks--keynotes)
- [Standards, Policy & Frameworks](#standards-policy--frameworks)

---

## 1. Foundations & Mental Models

The conceptual ground under everything else: the four eras of AI engineering (prompt → context → scaffolding → harness), the translation gap between ML / systems / security / SE communities, and the shift from model safety to system engineering.

### Key questions
- What changed when agents went from *answering* to *acting*?
- Why does each community (ML, systems, security, SE) see a different part of the problem?
- What shared mental models do we need across communities?

### Resources

<!-- AUTOGEN:START layer=foundations -->
- **Concrete Problems in AI Safety** (Dario Amodei et al., 2016) — Frames AI safety as a set of concrete engineering problems arising from accidents, defined as unintended and harmful behavior from poorly specified objectives or unsafe exploration. [[paper]](https://arxiv.org/abs/1606.06565) `[arXiv 2016]` `[classic]`
<!-- AUTOGEN:END layer=foundations -->

---

## 2. Execution Shell

The runtime that turns model calls into an agent: message passing, tool invocation, state and turn control, retry logic, trace collection. Without this, you don't have an agent — you just have a model.

### Key questions
- How do we isolate agent execution from the host system?
- What's the right state model for a long-running, multi-turn agent?
- How do retries, timeouts, and partial failures compose?

### Failure modes
- Execution shell integrity & state corruption
- Side effects leaking out of the sandbox
- Retry loops amplifying transient errors into systemic ones

### Resources

<!-- AUTOGEN:START layer=execution-shell -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=execution-shell -->

---

## 3. Coordination Layer

How multiple agents (or multiple roles within one agent) compose: planner / executor separation, specialist agents, reviewer / verifier roles, routing and hierarchy, multi-agent composition patterns.

### Key questions
- When is multi-agent composition genuinely useful vs. complexity for its own sake?
- How do we prevent policy drift across subtasks?
- What does "reviewer" mean when the reviewer is itself an agent?

### Failure modes
- Multi-agent coordination failures
- Exploit chaining across agents
- Bypass of human checkpoints via workflow logic

### Resources

<!-- AUTOGEN:START layer=coordination -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=coordination -->

---

## 4. Environment & Tool Interfaces

The boundary between the agent and the world: tools, APIs, browsers, filesystems, code executors, MCP servers, CRM / DB / Slack / email integrations, simulated environments.

### Key questions
- How should tool interfaces be specified so trust boundaries are explicit?
- What's the threat model for an MCP server with broad access scopes?
- How do we test environment interfaces under adversarial conditions?

### Failure modes
- Tool injection (malicious tool output influencing agent reasoning)
- Over-broad tool permissions
- Environment coupling & unintended side effects

### Resources

<!-- AUTOGEN:START layer=tool-interface -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=tool-interface -->

---

## 5. Memory & Context Integrity

What the agent reads and remembers: RAG, vector stores, episodic memory, long-term memory, context windows. The risk surface is *what the system allowed the model to believe*.

### Key questions
- How do we distinguish system input from external (potentially adversarial) input in the context window?
- What are the lifecycle and integrity guarantees on long-term agent memory?
- How does memory poisoning propagate across sessions or users?

### Failure modes
- RAG poisoning & malicious documents
- Hidden instructions in retrieved content
- Memory poisoning & stale context
- Trust confusion: system vs. external input

### Resources

<!-- AUTOGEN:START layer=memory -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=memory -->

---

## 6. Observation, Tracing & Evaluation

How we see what the agent did and decide whether it was good: logging, replay, trace analysis, regression testing, adversarial testing, failure diagnosis. Evaluation is *one function* of the harness — not its full definition.

### Key questions
- What's the right unit of observation: token, step, tool call, episode?
- How do we evaluate workflow-level correctness, not just per-step output?
- What's the production analogue of a regression test for an agent?

### Failure modes
- Evaluation blind spots in production
- Drift between eval-time and deployment-time behavior
- Logging gaps that prevent root-cause analysis

### Resources

<!-- AUTOGEN:START layer=observation-eval -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=observation-eval -->

---

## 7. Permissions & Least Privilege for Reasoning Systems

Classical least privilege governs what code is **allowed to do**. For agents, we also need to bound what the system is allowed to **infer, plan, and attempt**.

### Key questions
- What does plan-aware authorization look like?
- How do contextual permissions (varying with task / risk) get specified and enforced?
- Can we make trust boundaries dynamic without making them unauditable?

### Failure modes
- Static tool permissions that grant more than the task requires
- Privilege escalation via tool composition
- Coarse sandboxing that conflates capabilities

### Resources

<!-- AUTOGEN:START layer=permissions -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=permissions -->

---

## 8. Intent Compilation

Translating natural-language goals into machine-checkable constraints **before** the agent acts. If least privilege is the security principle, intent compilation is the mechanism.

### Key questions
- How do we represent intent in a form a policy engine can check?
- What's the right interface for a human to confirm an extracted intent?
- How do we handle ambiguous or evolving intent mid-execution?

### Failure modes
- Silent goal drift
- Constraint extraction that under-specifies real user intent
- Policy-aware planning bypassed by emergent reasoning

### Resources

<!-- AUTOGEN:START layer=intent -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=intent -->

---

## 9. Transactional Agency

Containing, checkpointing, and rolling back probabilistic side effects. ML asks whether the behavior was good; systems asks what happens when step 6 fails after steps 1–5 already changed the world.

### Key questions
- Can agent actions be modeled as database-style transactions?
- What's the right unit of journaling — token, tool call, or semantic step?
- How do we design idempotent tool interfaces by default?

### Failure modes
- Partial-failure states with no rollback path
- Compensation logic that itself fails or is non-idempotent
- Recovery that re-triggers the original failure

### Resources

<!-- AUTOGEN:START layer=transactional-agency -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=transactional-agency -->

---

## 10. Agent Supply Chain Security

Build pipelines, CI/CD, packaging, release automation, environment boundaries. Many of the highest-leverage failures will come from familiar software-engineering surfaces, not from adversarial prompts.

### Key questions
- What's the threat model for an agent in a release pipeline?
- How do we audit AI-generated commits at scale when reviewers can't keep up?
- What does SBOM mean when components are model + prompts + tools + memory?

### Failure modes
- Misconfigured build artifacts (see [INCIDENTS.md](INCIDENTS.md): Claude Code source map exposure, 2025)
- Compromised dependency suggestions from coding agents
- Provenance gaps in AI-generated code

### Resources

<!-- AUTOGEN:START layer=supply-chain -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=supply-chain -->

---

## 11. Red Teaming for Agentic Systems

Adversarial testing of the *system*, not just the model. Prompt injection, exploit chaining, multi-turn attacks, supply-chain attacks on agent components.

### Key questions
- What's the methodology equivalent of penetration testing for an agent?
- How do we red-team multi-agent and workflow-level exploit chains?
- How does red-teaming differ from evaluation in this space?

### Failure modes
- Single-turn jailbreaks vs. multi-turn manipulation
- Workflow-level exploits that no single step would flag
- Defenses that pass eval but fail in deployment

### Resources

<!-- AUTOGEN:START layer=red-team -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=red-team -->

---

## 12. Human Oversight at Scale

Review, checkpoints, cognitive load. When coding agents produce code at 42,000× growth rates, traditional human-review assurance breaks. What replaces it?

### Key questions
- What gets escalated to a human, and how is that boundary specified?
- How do we measure reviewer cognitive load — and design to reduce it?
- What does "human in the loop" mean for a 100-agent fleet?

### Failure modes
- Rubber-stamping under volume
- Checkpoint fatigue → silent approval
- Review interfaces that hide the relevant signal

### Resources

<!-- AUTOGEN:START layer=oversight -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=oversight -->

---

## 13. Reference Architectures & Case Studies

End-to-end designs and detailed write-ups of real deployments. The published examples are still scarce — this section is high-value-to-fill.

### Resources

<!-- AUTOGEN:START layer=architectures -->
- *Contributions welcome.* See [CONTRIBUTING.md](CONTRIBUTING.md) for entry templates.
<!-- AUTOGEN:END layer=architectures -->

---

## Talks & Keynotes

- **Yuan (Emily) Xue**, *"From Models to Systems: Engineering Trustworthy AI Agents"* — Purdue CERIAS Annual Cybersecurity Symposium, April 2026. The framing that organizes this list.

---

## Standards, Policy & Frameworks

- **MITRE ATLAS** — Adversarial Threat Landscape for Artificial-Intelligence Systems. <https://atlas.mitre.org/>
- **NIST AI Risk Management Framework** — <https://www.nist.gov/itl/ai-risk-management-framework>
- *Contributions welcome for additional standards and policy documents.*

---

## Contributing

We actively want community contributions — papers, incidents, tools, write-ups, and improvements to the taxonomy itself. See [**CONTRIBUTING.md**](CONTRIBUTING.md) for editorial standards and entry templates.

Good first contributions:
- Add a paper you've published or read recently to the relevant section + [`papers/papers.yml`](papers/papers.yml)
- Document a real-world incident in [`INCIDENTS.md`](INCIDENTS.md) using the template
- Propose a new sub-section or refinement to the taxonomy

## License

- **Code** (scripts, automation, renderer) is licensed under [MIT](LICENSE).
- **Content** (curated lists, taxonomy, write-ups) is licensed under [CC BY 4.0](LICENSE-CONTENT) — reuse freely with attribution.

## Citation

If this list informs your research or practice, please cite:

```bibtex
@misc{awesome-trustworthy-agentic-systems,
  title  = {awesome-trustworthy-agentic-systems: A curated map of trustworthy agentic systems engineering},
  author = {Xue, Yuan and contributors},
  year   = {2026},
  url    = {https://github.com/TrustworthyAgenticSystems/awesome-trustworthy-agentic-systems}
}
```

## Acknowledgments

Framed by the keynote *"From Models to Systems: Engineering Trustworthy AI Agents"* delivered at the Purdue CERIAS Annual Cybersecurity Symposium, April 2026. Thanks to the cross-community researchers and engineers whose work this list maps.
