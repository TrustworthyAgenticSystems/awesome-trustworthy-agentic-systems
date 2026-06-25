# awesome-trustworthy-agentic-systems

> A curated map of **trustworthy agentic systems engineering** — for builders who need the systems lens, and for researchers tracing the cross-community literature on agent harnesses, permissions, intent, and operational governance.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: MIT (code)](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0 (content)](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Why this list exists

Most existing lists on AI agents index *how to build them*. This list indexes *how to engineer them so they deserve trust*.

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
- **Building Effective Agents** (Erik Schluntz et al., 2024) — A practical engineering guide that separates predictable workflows from open-ended agents and catalogs composable patterns such as prompt chaining, routing, orchestrator-workers, and evaluator-optimizer. [[paper]](https://www.anthropic.com/engineering/building-effective-agents) `[Anthropic 2024]` `[paper]`
- **Large Language Model Agents (Berkeley MOOC)** (Dawn Song et al., 2024) — A public course on language-model agents covering reasoning, planning, tool use, code generation, multi-agent collaboration, and safety, with lectures from researchers across leading labs. [[course]](https://llmagents-learning.org/f24) `[course]`
- **Harms from Increasingly Agentic Algorithmic Systems** (Alan Chan et al., 2023) — Characterizes how harms change as algorithmic systems gain autonomy, underspecification, directness of impact, and goal-directedness. [[paper]](https://arxiv.org/abs/2302.10329) `[FAccT 2023]` `[paper]`
- **Practices for Governing Agentic AI Systems** (Yonadav Shavit et al., 2023) — Proposes baseline operational practices for keeping agentic systems accountable across their lifecycle, including suitability evaluation, constraining the action space, human approval for high-stakes actions, interruptibility, and attributability of actions to a responsible party. [[paper]](https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf) `[OpenAI 2023]` `[paper]`
- **ReAct: Synergizing Reasoning and Acting in Language Models** (Shunyu Yao et al., 2023) — Interleaves chain-of-thought reasoning with task actions so a language model alternates between thinking and calling external tools or environments. [[paper]](https://arxiv.org/abs/2210.03629) [[code]](https://github.com/ysymyth/ReAct) `[ICLR 2023]` `[paper]`
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
- **LangGraph** (LangChain, 2024) — A low-level orchestration library for building stateful, multi-actor agent applications with explicit graphs, durable execution, checkpointing, cycles, and human-in-the-loop pauses. [[repo]](https://github.com/langchain-ai/langgraph) `[tool]`
- **AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation** (Qingyun Wu et al., 2023) — Frames LLM applications as conversations among configurable, role-specialized agents that exchange natural-language messages to solve a task together. [[paper]](https://arxiv.org/abs/2308.08155) [[code]](https://github.com/microsoft/autogen) `[arXiv 2023]` `[paper]`
- **Generative Agents: Interactive Simulacra of Human Behavior** (Joon Sung Park et al., 2023) — Gives language-model agents a memory stream, periodic reflection, and planning so they produce believable individual and emergent group behavior in a sandbox world. [[paper]](https://arxiv.org/abs/2304.03442) `[UIST 2023]` `[paper]`
- **ReAct: Synergizing Reasoning and Acting in Language Models** (Shunyu Yao et al., 2023) — Interleaves chain-of-thought reasoning with task actions so a language model alternates between thinking and calling external tools or environments. [[paper]](https://arxiv.org/abs/2210.03629) [[code]](https://github.com/ysymyth/ReAct) `[ICLR 2023]` `[paper]`
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
- **Model Context Protocol (MCP)** (Anthropic, 2024) — An open standard that gives agents a uniform interface to external tools, data sources, and workflows, so a capability is described once and reused across hosts. [[repo]](https://modelcontextprotocol.io) [[code]](https://github.com/modelcontextprotocol/modelcontextprotocol) `[tool]`
- **Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection** (Kai Greshake et al., 2023) — Defines indirect prompt injection, where adversarial instructions hidden in external content that an application retrieves are later executed by the model as if they were trusted input. [[paper]](https://arxiv.org/abs/2302.12173) [[code]](https://github.com/greshake/llm-security) `[AISec 2023]` `[paper]`
- **Toolformer: Language Models Can Teach Themselves to Use Tools** (Timo Schick et al., 2023) — Trains a model to decide which API to call, when, and with what arguments using self-supervised annotation that keeps only calls which reduce perplexity. [[paper]](https://arxiv.org/abs/2302.04761) `[arXiv 2023]` `[paper]`
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
- **Generative Agents: Interactive Simulacra of Human Behavior** (Joon Sung Park et al., 2023) — Gives language-model agents a memory stream, periodic reflection, and planning so they produce believable individual and emergent group behavior in a sandbox world. [[paper]](https://arxiv.org/abs/2304.03442) `[UIST 2023]` `[paper]`
- **MemGPT: Towards LLMs as Operating Systems** (Charles Packer et al., 2023) — Borrows virtual-memory paging from operating systems to manage a tiered context hierarchy, letting the agent move information between a small active context and larger external stores. [[paper]](https://arxiv.org/abs/2310.08560) [[code]](https://github.com/letta-ai/letta) `[arXiv 2023]` `[paper]`
- **Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection** (Kai Greshake et al., 2023) — Defines indirect prompt injection, where adversarial instructions hidden in external content that an application retrieves are later executed by the model as if they were trusted input. [[paper]](https://arxiv.org/abs/2302.12173) [[code]](https://github.com/greshake/llm-security) `[AISec 2023]` `[paper]`
- **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (Patrick Lewis et al., 2020) — Combines a parametric generator with a non-parametric dense retriever so a model conditions its output on documents fetched at inference time. [[paper]](https://arxiv.org/abs/2005.11401) `[NeurIPS 2020]` `[classic]`
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
- **AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents** (Edoardo Debenedetti et al., 2024) — Provides a dynamic benchmark of realistic tool-using agent tasks paired with security test cases, so attacks and defenses are measured on end-to-end agent behavior rather than isolated prompts. [[paper]](https://arxiv.org/abs/2406.13352) [[code]](https://github.com/ethz-spylab/agentdojo) `[NeurIPS Datasets and Benchmarks 2024]` `[paper]`
- **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** (Carlos E. Jimenez et al., 2024) — Tasks agents with producing patches that resolve real GitHub issues across many Python repositories, validated by the projects' own test suites. [[paper]](https://arxiv.org/abs/2310.06770) [[code]](https://github.com/princeton-nlp/SWE-bench) `[ICLR 2024]` `[paper]`
- **tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains** (Shunyu Yao et al., 2024) — Evaluates agents on multi-turn tool use while talking to an LLM-simulated user under domain policies, scoring whether the final world state is correct. [[paper]](https://arxiv.org/abs/2406.12045) [[code]](https://github.com/sierra-research/tau-bench) `[arXiv 2024]` `[paper]`
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
- **LangGraph** (LangChain, 2024) — A low-level orchestration library for building stateful, multi-actor agent applications with explicit graphs, durable execution, checkpointing, cycles, and human-in-the-loop pauses. [[repo]](https://github.com/langchain-ai/langgraph) `[tool]`
- **Sagas** (Hector Garcia-Molina et al., 1987) — Defines the saga, a long-lived transaction split into a sequence of sub-transactions, each paired with a compensating action that semantically undoes it, so the system either completes or compensates back to consistency. [[paper]](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf) `[SIGMOD 1987]` `[classic]`
<!-- AUTOGEN:END layer=transactional-agency -->

---

## 10. Agent Supply Chain Security

Build pipelines, CI/CD, packaging, release automation, environment boundaries. Many of the highest-leverage failures will come from familiar software-engineering surfaces, not from adversarial prompts.

### Key questions
- What's the threat model for an agent in a release pipeline?
- How do we audit AI-generated commits at scale when reviewers can't keep up?
- What does SBOM mean when components are model + prompts + tools + memory?

### Failure modes
- Misconfigured build artifacts (see [INCIDENTS.md](INCIDENTS.md): Claude Code source map exposure, 2026)
- Compromised dependency suggestions from coding agents
- Provenance gaps in AI-generated code

### Resources

<!-- AUTOGEN:START layer=supply-chain -->
- **OWASP Top 10 for Large Language Model Applications** (OWASP Foundation, 2025) — A community-built awareness standard enumerating the most critical security risks in LLM applications, including prompt injection, insecure output handling, training-data poisoning, and excessive agency. [[paper]](https://owasp.org/www-project-top-10-for-large-language-model-applications/) `[OWASP 2025]` `[classic]`
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
- **OWASP Top 10 for Large Language Model Applications** (OWASP Foundation, 2025) — A community-built awareness standard enumerating the most critical security risks in LLM applications, including prompt injection, insecure output handling, training-data poisoning, and excessive agency. [[paper]](https://owasp.org/www-project-top-10-for-large-language-model-applications/) `[OWASP 2025]` `[classic]`
- **AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents** (Edoardo Debenedetti et al., 2024) — Provides a dynamic benchmark of realistic tool-using agent tasks paired with security test cases, so attacks and defenses are measured on end-to-end agent behavior rather than isolated prompts. [[paper]](https://arxiv.org/abs/2406.13352) [[code]](https://github.com/ethz-spylab/agentdojo) `[NeurIPS Datasets and Benchmarks 2024]` `[paper]`
- **garak: LLM vulnerability scanner** (NVIDIA, 2024) — An open-source scanner that probes language models for failure modes such as prompt injection, jailbreaks, toxic generation, and data leakage, combining static, dynamic, and adaptive probes. [[repo]](https://github.com/NVIDIA/garak) `[tool]`
- **Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection** (Kai Greshake et al., 2023) — Defines indirect prompt injection, where adversarial instructions hidden in external content that an application retrieves are later executed by the model as if they were trusted input. [[paper]](https://arxiv.org/abs/2302.12173) [[code]](https://github.com/greshake/llm-security) `[AISec 2023]` `[paper]`
- **Universal and Transferable Adversarial Attacks on Aligned Language Models** (Andy Zou et al., 2023) — Introduces Greedy Coordinate Gradient, an automated method that finds adversarial suffixes which bypass alignment safeguards and transfer across both open and closed models. [[paper]](https://arxiv.org/abs/2307.15043) [[code]](https://github.com/llm-attacks/llm-attacks) `[arXiv 2023]` `[paper]`
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
- **Practices for Governing Agentic AI Systems** (Yonadav Shavit et al., 2023) — Proposes baseline operational practices for keeping agentic systems accountable across their lifecycle, including suitability evaluation, constraining the action space, human approval for high-stakes actions, interruptibility, and attributability of actions to a responsible party. [[paper]](https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf) `[OpenAI 2023]` `[paper]`
<!-- AUTOGEN:END layer=oversight -->

---

## 13. Reference Architectures & Case Studies

End-to-end designs and detailed write-ups of real deployments. The published examples are still scarce — this section is high-value-to-fill.

### Resources

<!-- AUTOGEN:START layer=architectures -->
- **Building Effective Agents** (Erik Schluntz et al., 2024) — A practical engineering guide that separates predictable workflows from open-ended agents and catalogs composable patterns such as prompt chaining, routing, orchestrator-workers, and evaluator-optimizer. [[paper]](https://www.anthropic.com/engineering/building-effective-agents) `[Anthropic 2024]` `[paper]`
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
  author = {The Trustworthy Agentic Systems contributors},
  year   = {2026},
  url    = {https://github.com/TrustworthyAgenticSystems/awesome-trustworthy-agentic-systems}
}
```

## Acknowledgments

Thanks to the cross-community researchers and engineers whose work this list maps.
