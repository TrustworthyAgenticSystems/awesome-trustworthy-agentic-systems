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

## How it works

Two tracks feed one taxonomy through one human review gate. A deep-research agent and community contributors propose entries; a validator and a human reviewer verify the source, tags, and deduplication; only then does an entry become a published artifact that renders to this list and the [website](https://trustworthy-agentic-systems.org).

![Architecture: high-velocity inputs (papers, incidents, news) and slow-moving canon (classics, courses, OSS) flow through a deep research agent and community/agent PRs into a human review gate, then into the GitHub source of truth (structured data + taxonomy) and the website.](docs/architecture.png)

The pipeline follows the resource's own thesis: **agents propose, a trusted base validates, and every action is logged and attributable.** See [`research-agent/DESIGN.md`](research-agent/DESIGN.md) for the live-feed agent and [`CONTRIBUTING.md`](CONTRIBUTING.md) for the review gate.

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
- **Agents That Know Too Much: A Data-Centric Survey of Privacy in LLM Agents** (Nada Lahjouji et al., 2026) — A data-centric survey taxonomizing privacy risks in LLM agents across various data sources, identifying governance mechanisms, and highlighting gaps in information-flow control and comprehensive benchmarking. [[paper]](https://arxiv.org/abs/2606.26627v1) `[arXiv 2026]` `[paper]`
- **Building Effective Agents** (Erik Schluntz et al., 2024) — A practical engineering guide that separates predictable workflows from open-ended agents and catalogs composable patterns such as prompt chaining, routing, orchestrator-workers, and evaluator-optimizer. [[paper]](https://www.anthropic.com/engineering/building-effective-agents) `[Anthropic 2024]` `[paper]`
- **Large Language Model Agents (Berkeley MOOC)** (Dawn Song et al., 2024) — A public course on language-model agents covering reasoning, planning, tool use, code generation, multi-agent collaboration, and safety, with lectures from researchers across leading labs. [[course]](https://llmagents-learning.org/f24) `[course]`
- **DecodingTrust: A Comprehensive Assessment of Trustworthiness in GPT Models** (Boxin Wang et al., 2023) — Provides a broad trustworthiness benchmark for large language models across eight perspectives, including toxicity, stereotype bias, adversarial and out-of-distribution robustness, robustness to adversarial demonstrations, privacy, machine ethics, and fairness. [[paper]](https://arxiv.org/abs/2306.11698) [[code]](https://github.com/AI-secure/DecodingTrust) `[NeurIPS 2023]` `[paper]`
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
- **To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair** (Zhihao Lin et al., 2026) — Empirical study of code execution behavior in LLM-based program repair agents, analyzing cost-effectiveness and impact on repair success across various execution paradigms and models. [[paper]](https://arxiv.org/abs/2606.26978v1) `[arXiv 2026]` `[paper]`
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
- **MAStrike: Shapley-Guided Collusive Red-Teaming on Multi-Agent Systems** (Chejian Xu et al., 2026) — Targets the distinctive risk surface of hierarchical multi-agent systems, where safety is spread across specialized agents and collusion can bypass per-agent checks. [[paper]](https://arxiv.org/abs/2606.12918) `[arXiv 2026]` `[paper]`
- **From CVE Entries to Verifiable Exploits: An Automated Multi-Agent Framework for Reproducing CVEs** (Saad Ullah et al., 2025) — Presents a multi-agent pipeline with processor, builder, exploiter, and verifier roles that rebuilds vulnerable environments from CVE entries and produces verifiable exploits, reproducing roughly half of recent CVEs at a few dollars each. [[paper]](https://arxiv.org/abs/2509.01835) `[arXiv 2025]` `[paper]`
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
- **AdvAgent: Controllable Blackbox Red-teaming on Web Agents** (Chejian Xu et al., 2025) — Trains a reinforcement-learning adversarial prompter that generates stealthy, controllable web-page injections to hijack web agents toward attacker-chosen actions, operating in a black-box setting and adapting across attack goals from agent feedback. [[paper]](https://arxiv.org/abs/2410.17401) `[ICML 2025]` `[paper]`
- **TOUCAN: Synthesizing 1.5M Tool-Agentic Data from Real-World MCP Environments** (Zhangchen Xu et al., 2025) — Releases the largest open tool-agentic dataset, roughly 1.5 million trajectories synthesized from hundreds of real Model Context Protocol servers spanning thousands of tools, with real tool execution and verified calls. [[paper]](https://arxiv.org/abs/2510.01179) [[code]](https://github.com/TheAgentArk/Toucan) `[arXiv 2025]` `[paper]`
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
- **AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases** (Zhaorun Chen et al., 2024) — Introduces a backdoor attack on generic and retrieval-augmented LLM agents that poisons the agent's long-term memory or knowledge base with a small number of malicious examples. [[paper]](https://arxiv.org/abs/2407.12784) [[code]](https://github.com/BillChan226/AgentPoison) `[NeurIPS 2024]` `[paper]`
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
- **DecodingTrust-Agent: A Controllable and Interactive Red-Teaming Platform for AI Agents** (Zhaorun Chen et al., 2026) — Extends the DecodingTrust trustworthiness benchmark to agents with a controllable, fully simulated red-teaming platform spanning many domains and dozens of reproducible environments. [[paper]](https://arxiv.org/abs/2605.04808) `[arXiv 2026]` `[paper]`
- **SoSBench: Benchmarking Safety Alignment on Scientific Domains** (Fengqing Jiang et al., 2025) — Introduces a regulation-grounded, hazard-focused safety benchmark of thousands of prompts across six high-risk scientific domains including chemistry, biology, medicine, and physics. [[paper]](https://arxiv.org/abs/2505.21605) [[code]](https://sosbench.github.io/) `[arXiv 2025]` `[paper]`
- **TOUCAN: Synthesizing 1.5M Tool-Agentic Data from Real-World MCP Environments** (Zhangchen Xu et al., 2025) — Releases the largest open tool-agentic dataset, roughly 1.5 million trajectories synthesized from hundreds of real Model Context Protocol servers spanning thousands of tools, with real tool execution and verified calls. [[paper]](https://arxiv.org/abs/2510.01179) [[code]](https://github.com/TheAgentArk/Toucan) `[arXiv 2025]` `[paper]`
- **TinyV: Reducing False Negatives in Verification Improves RL for LLM Reasoning** (Zhangchen Xu et al., 2025) — Shows that reward verifiers in reinforcement learning with verifiable rewards often reject correct model outputs, and that these false negatives degrade training. [[paper]](https://arxiv.org/abs/2505.14625) [[code]](https://github.com/uw-nsl/TinyV) `[arXiv 2025]` `[paper]`
- **AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents** (Edoardo Debenedetti et al., 2024) — Provides a dynamic benchmark of realistic tool-using agent tasks paired with security test cases, so attacks and defenses are measured on end-to-end agent behavior rather than isolated prompts. [[paper]](https://arxiv.org/abs/2406.13352) [[code]](https://github.com/ethz-spylab/agentdojo) `[NeurIPS Datasets and Benchmarks 2024]` `[paper]`
- **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** (Carlos E. Jimenez et al., 2024) — Tasks agents with producing patches that resolve real GitHub issues across many Python repositories, validated by the projects' own test suites. [[paper]](https://arxiv.org/abs/2310.06770) [[code]](https://github.com/princeton-nlp/SWE-bench) `[ICLR 2024]` `[paper]`
- **tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains** (Shunyu Yao et al., 2024) — Evaluates agents on multi-turn tool use while talking to an LLM-simulated user under domain policies, scoring whether the final world state is correct. [[paper]](https://arxiv.org/abs/2406.12045) [[code]](https://github.com/sierra-research/tau-bench) `[arXiv 2024]` `[paper]`
- **DecodingTrust: A Comprehensive Assessment of Trustworthiness in GPT Models** (Boxin Wang et al., 2023) — Provides a broad trustworthiness benchmark for large language models across eight perspectives, including toxicity, stereotype bias, adversarial and out-of-distribution robustness, robustness to adversarial demonstrations, privacy, machine ethics, and fairness. [[paper]](https://arxiv.org/abs/2306.11698) [[code]](https://github.com/AI-secure/DecodingTrust) `[NeurIPS 2023]` `[paper]`
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
- **AC4A: Access Control for Agents** (Reshabh K Sharma et al., 2026) — AC4A is an access control framework for LLM agents that enables fine-grained, hierarchical permission definition and enforcement for API and browser-based interactions, addressing the problem of agents having excessive access. [[paper]](https://arxiv.org/abs/2603.20933v1) `[arXiv 2026]` `[paper]`
- **AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A** (Sunil Prakash, 2026) — Introduces Agent Identity Protocol (AIP) using Invocation-Bound Capability Tokens (IBCTs) to provide verifiable delegation, attenuated authorization, and provenance binding for agent-to-agent and tool-calling interactions, with reference implementations and adversarial evaluation. [[paper]](https://arxiv.org/abs/2603.24775v1) `[arXiv 2026]` `[paper]`
- **AIRGuard: Guarding Agent Actions with Runtime Authority Control** (Suliu Qin et al., 2026) — AIRGuard is a runtime guard that implements action-time authorization and least privilege for tool-using agents by normalizing tool calls, deriving step-level authority, tracking trust, simulating side effects, and auditing cross-step risk. [[paper]](https://arxiv.org/abs/2605.28914v1) `[arXiv 2026]` `[paper]`
- **Agent Privilege Separation in OpenClaw: A Structural Defense Against Prompt Injection** (Darren Cheng et al., 2026) — A structural defense against prompt injection using agent isolation via privilege separation and tool partitioning in a two-agent pipeline, complemented by JSON formatting to strip persuasive framing. [[paper]](https://arxiv.org/abs/2603.13424v1) `[arXiv 2026]` `[paper]`
- **AgenticOS: An Intent-Oriented Secure Operating System Architecture for Autonomous AI Agents** (Zhen Zhao et al., 2026) — Proposes AgenticOS, an intent-oriented secure operating system architecture that reframes OS security from resource management to intent filtering, synthesizing least-privilege environments based on structured agent intent declarations. [[paper]](https://arxiv.org/abs/2606.21129v1) `[arXiv 2026]` `[paper]`
- **Aligning Provenance with Authorization: A Dual-Graph Defense for LLM Agents** (Peiran Wang et al., 2026) — AuthGraph is a dual-graph defense framework that aligns an agent's execution provenance with an authorization graph derived from user intent to detect indirect prompt injection and unauthorized operations at the parameter-source level. [[paper]](https://arxiv.org/abs/2605.26497v1) `[arXiv 2026]` `[paper]`
- **An AI Agent Execution Environment to Safeguard User Data** (Robert Stanley et al., 2026) — GAAP is an execution environment for AI agents that enforces user-defined permission specifications for private data disclosure, including to the AI model provider, by tracking information flow across execution steps and tasks. [[paper]](https://arxiv.org/abs/2604.19657v1) `[arXiv 2026]` `[paper]`
- **Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure** (Krti Tallam, 2026) — Formalizes authorization propagation as a workflow-level property in multi-agent systems, identifying sub-problems and deriving architectural requirements for identity governance as infrastructure. [[paper]](https://arxiv.org/abs/2605.05440v1) `[arXiv 2026]` `[paper]`
- **CapSeal: Capability-Sealed Secret Mediation for Secure Agent Execution** (Shutong Jin et al., 2026) — CapSeal introduces a capability-sealed secret mediation architecture that replaces direct secret access with constrained invocations through a local trusted broker, addressing prompt injection and tool misuse for agent secrets. [[paper]](https://arxiv.org/abs/2604.16762v1) `[arXiv 2026]` `[paper]`
- **ClawLess: A Security Model of AI Agents** (Hongyi Lu et al., 2026) — ClawLess is a security framework that enforces formally verified, dynamic policies on AI agents by translating them into BPF-based syscall interception rules, providing fundamental security guarantees against adversarial agents. [[paper]](https://arxiv.org/abs/2604.06284v1) `[arXiv 2026]` `[paper]`
- **Digital Identity for Agentic Systems: Toward a Portable Authorization Standard for Autonomous Agents** (Partha Madhira, 2026) — Proposes a portable authorization model for autonomous agents that addresses structural gaps in existing identity and access models for cross-organizational workflows, focusing on explicit, constrained, auditable, and revocable authority. [[paper]](https://arxiv.org/abs/2605.11487v1) `[arXiv 2026]` `[paper]`
- **Evaluating Privilege Usage of Agents with Real-World Tools** (Quan Zhang et al., 2026) — GrantBox is a security evaluation sandbox that integrates real-world tools to assess LLM agents' privilege usage under prompt injection attacks, revealing vulnerabilities in sophisticated scenarios. [[paper]](https://arxiv.org/abs/2603.28166v2) `[arXiv 2026]` `[paper]`
- **Formal Policy Enforcement for Real-World Agentic Systems** (Nils Palumbo et al., 2026) — A framework for formal policy enforcement in agentic systems using aspect-oriented programming and Datalog, enabling policies to be specified independently of agent reasoning and enforced at every policy-relevant decision. [[paper]](https://arxiv.org/abs/2602.16708v3) `[arXiv 2026]` `[paper]`
- **Governing Dynamic Capabilities: Cryptographic Binding and Reproducibility Verification for AI Agent Tool Use** (Ziling Zhou, 2026) — Proposes a cryptographic framework for agent governance that ensures capability integrity, behavioral verifiability, and interaction auditability by distinguishing tool definitions from user context at the orchestration layer, with two instantiations and an evaluation of overhead and attack detection. [[paper]](https://arxiv.org/abs/2603.14332v2) `[arXiv 2026]` `[paper]`
- **Grimlock: Guarding High-Agency Systems with eBPF and Attested Channels** (Qiancheng Wu et al., 2026) — Grimlock is an Agent Guard that uses eBPF and attested TLS channels to enforce identity, authorization, provenance, and least-privilege delegation for agent-to-agent communication across multi-cloud environments. [[paper]](https://arxiv.org/abs/2605.27488v2) `[arXiv 2026]` `[paper]`
- **HDP: A Lightweight Cryptographic Protocol for Human Delegation Provenance in Agentic AI Systems** (Asiri Dalugoda, 2026) — HDP is a lightweight cryptographic protocol that captures and verifies human authorization context and multi-hop delegation chains in agentic systems, enabling offline provenance verification of actions. [[paper]](https://arxiv.org/abs/2604.04522v1) `[arXiv 2026]` `[paper]`
- **Heartbeat-Bound Hierarchical Credentials: Cryptographic Revocation for AI Agent Swarms** (Saurabh Deochake, 2026) — Heartbeat-Bound Hierarchical Credentials (HBHC) is a cryptographic protocol that binds agent credential validity to periodic parent liveness proofs, enabling rapid, network-independent revocation of sub-agent swarms to prevent zombie agents from executing privileged operations. [[paper]](https://arxiv.org/abs/2605.20704v1) `[arXiv 2026]` `[paper]`
- **ILION: Deterministic Pre-Execution Safety Gates for Agentic AI Systems** (Florin Adrian Chitan, 2026) — ILION is a deterministic, cascade-architecture execution gate that classifies proposed agent actions as BLOCK or ALLOW, addressing the architectural mismatch of text-safety systems for agent action safety. [[paper]](https://arxiv.org/abs/2603.13247v1) `[arXiv 2026]` `[paper]`
- **Overeager Coding Agents: Measuring Out-of-Scope Actions on Benign Tasks** (Yubin Qu et al., 2026) — Introduces a benchmark, OverEager-Gen, to measure 'overeager' out-of-scope actions by coding agents on benign tasks, highlighting how prompt-based consent declarations can mask underlying authorization issues and demonstrating significant variance across agent frameworks and models. [[paper]](https://arxiv.org/abs/2605.18583v1) `[arXiv 2026]` `[paper]`
- **Overlaying Governance: A Compositional Authorization Framework for Delegation and Scope in Agentic AI** (Amjad Ibrahim et al., 2026) — A compositional authorization framework that introduces primitives for recursive delegation, contextual boundaries, and dynamic scoping to govern agentic AI systems, operationalized through an overlay operator on existing relational policies. [[paper]](https://arxiv.org/abs/2606.03518v1) `[arXiv 2026]` `[paper]`
- **PlanTwin: Privacy-Preserving Planning Abstractions for Cloud-Assisted LLM Agents** (Guangsheng Yu et al., 2026) — PlanTwin is a privacy-preserving architecture that projects a private local environment into a de-identified digital twin for cloud-assisted LLM planning, preventing raw context exposure while maintaining planning quality. [[paper]](https://arxiv.org/abs/2603.18377v2) `[arXiv 2026]` `[paper]`
- **Prompts Don't Protect: Architectural Enforcement via MCP Proxy for LLM Tool Access Control** (Rohith Uppala, 2026) — A governed MCP proxy enforces attribute-based access control for LLM tool access by filtering tool discovery and blocking unauthorized invocations, demonstrating architectural enforcement is necessary for reliable tool access control. [[paper]](https://arxiv.org/abs/2605.18414v1) `[arXiv 2026]` `[paper]`
- **Proof-Carrying Agent Actions: Model-Agnostic Runtime Governance for Heterogeneous Agent Systems** (Zexun Wang, 2026) — Introduces Proof-Carrying Agent Actions (PCAA), a runtime-neutral governance model using action certificates to consistently track authorization, approval, and evidence for high-risk actions across heterogeneous agent systems. [[paper]](https://arxiv.org/abs/2606.04104v1) `[arXiv 2026]` `[paper]`
- **SUDP: Secret-Use Delegation Protocol for Agentic Systems** (Xiaohang Yu et al., 2026) — Formalizes the Agent Secret Use (ASU) problem and proposes the Secret-Use Delegation Protocol (SUDP) to enable agents to perform secret-backed operations without gaining reusable authority, satisfying seven security properties. [[paper]](https://arxiv.org/abs/2604.24920v3) `[arXiv 2026]` `[paper]`
- **Securing the Agent: Vendor-Neutral, Multitenant Enterprise Retrieval and Tool Use** (Francisco Javier Arceo et al., 2026) — Introduces a layered isolation architecture for multitenant enterprise RAG and agentic systems, combining policy-aware ingestion, retrieval-time gating, and server-side orchestration to enforce authorization and prevent cross-tenant data leakage. [[paper]](https://arxiv.org/abs/2605.05287v1) `[arXiv 2026]` `[paper]`
- **Session Risk Memory (SRM): Temporal Authorization for Deterministic Pre-Execution Safety Gates** (Florin Adrian Chitan, 2026) — Session Risk Memory (SRM) extends stateless pre-execution safety gates with trajectory-level authorization by maintaining a semantic centroid of agent behavior to detect distributed attacks across multiple steps. [[paper]](https://arxiv.org/abs/2603.22350v1) `[arXiv 2026]` `[paper]`
- **Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents** (Cailin Winston et al., 2026) — An SMT solver-aided framework that translates natural-language tool-use policies into formal logic constraints and intercepts planned tool calls at runtime to enforce compliance, blocking policy violations. [[paper]](https://arxiv.org/abs/2603.20449v1) `[arXiv 2026]` `[paper]`
- **The Granularity Mismatch in Agent Security: Argument-Level Provenance Solves Enforcement and Isolates the LLM Reasoning Bottleneck** (Linfeng Fan et al., 2026) — Introduces Provenance-Aware Capability Contracts (PACT), a runtime monitor that assigns semantic roles to tool arguments and tracks value provenance to enforce trust contracts, addressing the granularity mismatch in agent security. [[paper]](https://arxiv.org/abs/2605.11039v1) `[arXiv 2026]` `[paper]`
- **Tracking Capabilities for Safer Agents** (Martin Odersky et al., 2026) — Proposes a programming-language-based safety harness using Scala 3's capture checking to enforce capability-based access control for agent tool calls, preventing information leakage and unintended side effects. [[paper]](https://arxiv.org/abs/2603.00991v2) `[arXiv 2026]` `[paper]`
- **VIGIL: Runtime Enforcement of Behavioral Specifications in AI Agent Skills** (Ying Li et al., 2026) — VIGIL is a runtime enforcement framework that translates natural-language behavioral policies for agent skills into executable SMT constraints over execution traces, enabling detection of violations across multiple actions and contextual dependencies. [[paper]](https://arxiv.org/abs/2606.26524v1) `[arXiv 2026]` `[paper]`
- **When Agents Control Robots: A Zero Trust Policy Model for Agentic Cyber-Physical Systems** (Tharindu Ranathunga et al., 2026) — Proposes a Zero Trust Policy Model (ZTPM) with 25 typed primitives and physical impact tiers for runtime policy enforcement in agentic cyber-physical systems, motivated by non-deterministic actuation parameter selection. [[paper]](https://arxiv.org/abs/2605.25653v1) `[arXiv 2026]` `[paper]`
- **ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning** (Zhaorun Chen et al., 2025) — Proposes a guardrail agent that enforces explicit safety policies over another agent's action trajectory rather than filtering only inputs and outputs. [[paper]](https://arxiv.org/abs/2503.22738) `[arXiv 2025]` `[paper]`
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
- **Validated Intent Compilation for Constrained Routing in LEO Mega-Constellations** (Yuanhang Li, 2026) — An end-to-end system for translating natural language operator intents into validated, low-level routing constraints for LEO mega-constellations, featuring an LLM intent compiler with a verifier-feedback repair loop and a deterministic validator for safety guarantees. [[paper]](https://arxiv.org/abs/2604.07264v1) `[arXiv 2026]` `[paper]`
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
- **Cordon: Semantic Transactions for Tool-Using LLM Agents** (Zheng Chen et al., 2026) — Cordon introduces a transactional runtime system for LLM agents that stages and validates irreversible effects within a task-level execution boundary, enabling commit, rollback, and recovery across multi-step workflows. [[paper]](https://arxiv.org/abs/2606.17573v1) `[arXiv 2026]` `[paper]`
- **Crab: A Semantics-Aware Checkpoint/Restore Runtime for Agent Sandboxes** (Tianyuan Wu et al., 2026) — Crab is a host-side runtime that bridges the agent-OS semantic gap to enable semantics-aware checkpointing and restoration of agent sandbox state, improving recovery correctness and efficiency for fault tolerance and safe rollback. [[paper]](https://arxiv.org/abs/2604.28138v1) `[arXiv 2026]` `[paper]`
- **DeltaBox: Scaling Stateful AI Agents with Millisecond-Level Sandbox Checkpoint/Rollback** (Yunpeng Dong et al., 2026) — DeltaBox proposes OS-level abstractions, DeltaFS and DeltaCR, to enable millisecond-level, change-based checkpoint and rollback of complete sandbox states for AI agents, addressing the performance bottleneck in state exploration. [[paper]](https://arxiv.org/abs/2605.22781v2) `[arXiv 2026]` `[paper]`
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
- **"Elementary, My Dear Watson." Detecting Malicious Skills via Neuro-Symbolic Reasoning across Heterogeneous Artifacts** (Shenao Wang et al., 2026) — MalSkills is a neuro-symbolic framework that detects malicious skills by extracting security-sensitive operations from heterogeneous artifacts, constructing a skill dependency graph, and performing reasoning to identify malicious patterns or suspicious workflows. [[paper]](https://arxiv.org/abs/2603.27204v1) `[arXiv 2026]` `[paper]`
- **Agent Audit: A Security Analysis System for LLM Agent Applications** (Haiyue Zhang et al., 2026) — Agent Audit is a security analysis system that combines dataflow analysis, credential detection, and privilege-risk checks to identify vulnerabilities in LLM agent code and deployment artifacts, integrating with development and CI/CD workflows. [[paper]](https://arxiv.org/abs/2603.22853v1) `[arXiv 2026]` `[paper]`
- **AgentRiskBOM: A Risk-Scoping Security Bill of Materials for Agentic AI Systems** (Srimonti Dutta et al., 2026) — Introduces AgentRiskBOM, a security bill of materials (BOM) schema for agentic AI systems that documents runtime authority, including tool permissions, memory, and external action capabilities, and evaluates its effectiveness in risk-scoping and detecting authority drift across various open-source agents. [[paper]](https://arxiv.org/abs/2606.21877v1) `[arXiv 2026]` `[paper]`
- **BadSkill: Backdoor Attacks on Agent Skills via Model-in-Skill Poisoning** (Guiyao Tie et al., 2026) — Introduces BadSkill, a backdoor attack targeting model-in-skill supply-chain risk where malicious behavior is concealed within a skill's bundled model, and evaluates its effectiveness across various model architectures and perturbation types. [[paper]](https://arxiv.org/abs/2604.09378v1) `[arXiv 2026]` `[paper]`
- **Detecting AI Coding Agents in Open Source: A Validated Multi-Method Census of 180 Million Repositories** (Arsham Khosravani et al., 2026) — A multi-layered detection framework identifies AI coding agent traces across 180 million Git repositories, revealing significant underestimation by single-method approaches and distinct work profiles based on deployment channels. [[paper]](https://arxiv.org/abs/2606.24429v1) `[arXiv 2026]` `[paper]`
- **Detecting Malicious Agent Skills in the Wild using Attention** (Bacem Etteib et al., 2026) — Locate-and-Judge is a two-stage attention-based detector for malicious agent skills, addressing the supply-chain attack surface of third-party skill marketplaces by efficiently identifying and flagging malicious instructions within skill packages. [[paper]](https://arxiv.org/abs/2606.23416v1) `[arXiv 2026]` `[paper]`
- **Exploiting LLM Agent Supply Chains via Payload-less Skills** (Xinyu Liu et al., 2026) — Introduces Semantic Compliance Hijacking (SCH), a payload-less supply chain attack that uses natural language instructions to induce agents to generate and execute unauthorized code, bypassing traditional signature-based detection. [[paper]](https://arxiv.org/abs/2605.14460v1) `[arXiv 2026]` `[paper]`
- **Inference-Time Backdoors via Chat Templates: From LLM Supply Chains to Agentic System Compromise** (Ariel Fogel et al., 2026) — Identifies chat templates as a novel and undefended attack surface for inference-time backdoors, demonstrating compromise across LLM, agent, and multi-agent system levels, and showing evasion of existing defenses. [[paper]](https://arxiv.org/abs/2602.04653v4) `[arXiv 2026]` `[paper]`
- **MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills** (Wenbo Guo et al., 2026) — Introduces MalSkillBench, a runtime-verified benchmark of malicious agent skills, to evaluate the effectiveness of detection tools against hybrid code and prompt-based supply chain risks in third-party agent skills. [[paper]](https://arxiv.org/abs/2606.07131v3) `[arXiv 2026]` `[paper]`
- **ShieldNet: Network-Level Guardrails against Emerging Supply-Chain Injections in Agentic Systems** (Zhuowen Yuan et al., 2026) — Introduces SC-Inject-Bench, a benchmark for supply-chain injection attacks via malicious MCP tools, and ShieldNet, a network-level guardrail framework that detects these attacks by observing network interactions. [[paper]](https://arxiv.org/abs/2604.04426v1) `[arXiv 2026]` `[paper]`
- **SkillJect: Effectively Automating Skill-Based Prompt Injection for Skill-Enabled Agents** (Xiaojun Jia et al., 2026) — SkillJect is an automated framework for generating poisoned skills that hide malicious payloads in auxiliary scripts and use front-loaded inducements in skill instructions to trick agents into executing them, demonstrating a supply-chain attack surface in reusable skill ecosystems. [[paper]](https://arxiv.org/abs/2602.14211v3) `[arXiv 2026]` `[paper]`
- **SkillSieve: A Hierarchical Triage Framework for Detecting Malicious AI Agent Skills** (Yinghan Hou et al., 2026) — SkillSieve is a hierarchical triage framework for detecting malicious agent skills in marketplaces, combining regex, AST, metadata checks, and multi-LLM analysis to identify vulnerabilities in both code and natural-language instructions. [[paper]](https://arxiv.org/abs/2604.06550v2) `[arXiv 2026]` `[paper]`
- **Trojan's Whisper: Stealthy Manipulation of OpenClaw through Injected Bootstrapped Guidance** (Fazhong Liu et al., 2026) — Identifies and characterizes "guidance injection" as a novel attack vector in autonomous coding agents like OpenClaw, where adversarial operational narratives are embedded into bootstrap guidance files to manipulate agent reasoning and execute harmful actions stealthily. [[paper]](https://arxiv.org/abs/2603.19974v1) `[arXiv 2026]` `[paper]`
- **VeriPort: Automated and Verified Patch Backporting at Scale** (Jonah Ghebremichael et al., 2026) — VeriPort is an agentic system that automates and verifies the backporting of security patches to all affected versions of open-source dependencies, generating evidence that patches block exploitation and preserve functionality. [[paper]](https://arxiv.org/abs/2606.22704v1) `[arXiv 2026]` `[paper]`
- **ARTIPHISHELL: Shellphish's autonomous Cyber Reasoning System** (Shellphish, 2025) — An end-to-end autonomous cyber reasoning system that combines fuzzing, program analysis, and dozens of collaborating LLM agents to discover vulnerabilities, analyze root causes, and generate validated patches without human intervention. [[repo]](https://shellphish.net/aixcc/) `[tool]`
- **OWASP Top 10 for Large Language Model Applications** (OWASP Foundation, 2025) — A community-built awareness standard enumerating the most critical security risks in LLM applications, including prompt injection, insecure output handling, training-data poisoning, and excessive agency. [[paper]](https://owasp.org/www-project-top-10-for-large-language-model-applications/) `[OWASP 2025]` `[classic]`
- **PurpCode: Reasoning for Safer Code Generation** (Jiawei Liu et al., 2025) — Aligns coding models to generate secure code and refuse attack-assistance requests while preserving utility, using a two-stage method that first teaches concrete vulnerability rules and then generalizes the safety reasoning with reinforcement learning. [[paper]](https://arxiv.org/abs/2507.19060) [[code]](https://github.com/purpcode-uiuc/purpcode) `[arXiv 2025]` `[paper]`
- **VulnLLM-R: Specialized Reasoning LLM with Agent Scaffold for Vulnerability Detection** (Yuzhou Nie et al., 2025) — Trains a compact specialized reasoning model, wrapped in an agent scaffold, to perform step-by-step software vulnerability detection, outperforming much larger models and static analyzers on the task. [[paper]](https://arxiv.org/abs/2512.07533) [[code]](https://huggingface.co/UCSB-SURFI/VulnLLM-R-7B) `[arXiv 2025]` `[paper]`
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
- **DecodingTrust-Agent: A Controllable and Interactive Red-Teaming Platform for AI Agents** (Zhaorun Chen et al., 2026) — Extends the DecodingTrust trustworthiness benchmark to agents with a controllable, fully simulated red-teaming platform spanning many domains and dozens of reproducible environments. [[paper]](https://arxiv.org/abs/2605.04808) `[arXiv 2026]` `[paper]`
- **MAStrike: Shapley-Guided Collusive Red-Teaming on Multi-Agent Systems** (Chejian Xu et al., 2026) — Targets the distinctive risk surface of hierarchical multi-agent systems, where safety is spread across specialized agents and collusion can bypass per-agent checks. [[paper]](https://arxiv.org/abs/2606.12918) `[arXiv 2026]` `[paper]`
- **MIRROR: Novelty-Constrained Memory-Guided MCTS Red-Teaming for Agentic RAG** (Inderjeet Singh et al., 2026) — MIRROR is a unified, cross-surface red-teaming framework for multimodal agentic RAG systems that uses novelty-constrained, memory-guided Monte Carlo tree search to discover novel attacks across various surfaces, including text poisoning, image injection, and orchestrator-level tool manipulation. [[paper]](https://arxiv.org/abs/2606.26793v1) `[arXiv 2026]` `[paper]`
- **Prompt Injection in Automated Résumé Screening with Large Language Models: Single and Multi-Injection Settings** (Preet Baxi et al., 2026) — Characterizes prompt injection as a strategic manipulation tactic in LLM-based résumé screening, demonstrating its effectiveness under varying conditions and highlighting fairness concerns. [[paper]](https://arxiv.org/abs/2606.27287v1) `[arXiv 2026]` `[paper]`
- **ARMs: Adaptive Red-Teaming Agent against Multimodal Models with Plug-and-Play Attacks** (Zhaorun Chen et al., 2025) — Builds an adaptive red-teaming agent that orchestrates many multimodal attack strategies exposed as plug-and-play tools through the Model Context Protocol, using layered memory and multi-step reasoning to balance attack diversity and effectiveness. [[paper]](https://arxiv.org/abs/2510.02677) `[arXiv 2025]` `[paper]`
- **AdvAgent: Controllable Blackbox Red-teaming on Web Agents** (Chejian Xu et al., 2025) — Trains a reinforcement-learning adversarial prompter that generates stealthy, controllable web-page injections to hijack web agents toward attacker-chosen actions, operating in a black-box setting and adapting across attack goals from agent feedback. [[paper]](https://arxiv.org/abs/2410.17401) `[ICML 2025]` `[paper]`
- **BadScientist: Can a Research Agent Write Convincing but Unsound Papers that Fool LLM Reviewers?** (Fengqing Jiang et al., 2025) — Tests whether a paper-generation agent using only presentation-manipulation tactics, with no real experiments, can get accepted by multi-model LLM review systems. [[paper]](https://arxiv.org/abs/2510.18003) [[code]](https://bad-scientist.github.io/) `[arXiv 2025]` `[paper]`
- **OWASP Top 10 for Large Language Model Applications** (OWASP Foundation, 2025) — A community-built awareness standard enumerating the most critical security risks in LLM applications, including prompt injection, insecure output handling, training-data poisoning, and excessive agency. [[paper]](https://owasp.org/www-project-top-10-for-large-language-model-applications/) `[OWASP 2025]` `[classic]`
- **AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents** (Edoardo Debenedetti et al., 2024) — Provides a dynamic benchmark of realistic tool-using agent tasks paired with security test cases, so attacks and defenses are measured on end-to-end agent behavior rather than isolated prompts. [[paper]](https://arxiv.org/abs/2406.13352) [[code]](https://github.com/ethz-spylab/agentdojo) `[NeurIPS Datasets and Benchmarks 2024]` `[paper]`
- **AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases** (Zhaorun Chen et al., 2024) — Introduces a backdoor attack on generic and retrieval-augmented LLM agents that poisons the agent's long-term memory or knowledge base with a small number of malicious examples. [[paper]](https://arxiv.org/abs/2407.12784) [[code]](https://github.com/BillChan226/AgentPoison) `[NeurIPS 2024]` `[paper]`
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
- **HiLSVA: Design and Evaluation of a Human-in-the-Loop Agentic System for Scientific Visualization** (Kuangshi Ai et al., 2026) — HiLSVA is a human-in-the-loop agentic system for scientific visualization that integrates a plan-first multi-agent architecture with explicit human oversight, stepwise provenance tracking, and learn-at-test-time adaptation to improve transparency and control. [[paper]](https://arxiv.org/abs/2606.26614v1) `[arXiv 2026]` `[paper]`
- **BadScientist: Can a Research Agent Write Convincing but Unsound Papers that Fool LLM Reviewers?** (Fengqing Jiang et al., 2025) — Tests whether a paper-generation agent using only presentation-manipulation tactics, with no real experiments, can get accepted by multi-model LLM review systems. [[paper]](https://arxiv.org/abs/2510.18003) [[code]](https://bad-scientist.github.io/) `[arXiv 2025]` `[paper]`
- **ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning** (Zhaorun Chen et al., 2025) — Proposes a guardrail agent that enforces explicit safety policies over another agent's action trajectory rather than filtering only inputs and outputs. [[paper]](https://arxiv.org/abs/2503.22738) `[arXiv 2025]` `[paper]`
- **Practices for Governing Agentic AI Systems** (Yonadav Shavit et al., 2023) — Proposes baseline operational practices for keeping agentic systems accountable across their lifecycle, including suitability evaluation, constraining the action space, human approval for high-stakes actions, interruptibility, and attributability of actions to a responsible party. [[paper]](https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf) `[OpenAI 2023]` `[paper]`
<!-- AUTOGEN:END layer=oversight -->

---

## 13. Reference Architectures & Case Studies

End-to-end designs and detailed write-ups of real deployments. The published examples are still scarce — this section is high-value-to-fill.

### Resources

<!-- AUTOGEN:START layer=architectures -->
- **AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems** (Changxin Lao et al., 2026) — AgentX is a production-deployed multi-agent system that automates the entire recommender system iteration cycle, from hypothesis generation and code implementation to A/B testing and self-improvement, fundamentally restructuring the development workflow. [[paper]](https://arxiv.org/abs/2606.26859v1) `[arXiv 2026]` `[paper]`
- **NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems** (Shaohua Liu et al., 2026) — NOVA is a verification-aware agent harness that guides architecture evolution in industrial recommender systems using an architecture gradient and a multi-level verification cascade to prevent silent failures and improve reliability. [[paper]](https://arxiv.org/abs/2606.27243v1) `[arXiv 2026]` `[paper]`
- **ARTIPHISHELL: Shellphish's autonomous Cyber Reasoning System** (Shellphish, 2025) — An end-to-end autonomous cyber reasoning system that combines fuzzing, program analysis, and dozens of collaborating LLM agents to discover vulnerabilities, analyze root causes, and generate validated patches without human intervention. [[repo]](https://shellphish.net/aixcc/) `[tool]`
- **From CVE Entries to Verifiable Exploits: An Automated Multi-Agent Framework for Reproducing CVEs** (Saad Ullah et al., 2025) — Presents a multi-agent pipeline with processor, builder, exploiter, and verifier roles that rebuilds vulnerable environments from CVE entries and produces verifiable exploits, reproducing roughly half of recent CVEs at a few dollars each. [[paper]](https://arxiv.org/abs/2509.01835) `[arXiv 2025]` `[paper]`
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
