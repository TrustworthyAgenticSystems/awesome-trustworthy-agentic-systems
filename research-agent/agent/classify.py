"""Paper classifier — the only module that calls a model provider API.

Uses:
- gemini-2.5-flash by default (cheap, fast, capable for classification).
  Override via the CLASSIFIER_MODEL env var (e.g. gemini-2.5-flash-lite,
  gemini-2.5-pro).
- Implicit prefix caching. Gemini automatically caches stable input prefixes
  >=1024 tokens — our system prompt is large and identical across all calls in
  a run, so per-call cost drops to cached-token pricing after the first call.
- Structured output via response_schema with a Pydantic model.

The classifier assigns BOTH facets the repository schema requires on every
entry: a primary `harness_layer` (where in the stack) and one or two `sprs`
guarantees (what property). It also proposes optional open-problem tags and a
confidence, which the human reviewer uses to triage the draft.

Reads the API key from the GEMINI_API_KEY env var (set as a GitHub Actions
secret on the workflow).
"""

from __future__ import annotations

import os
from typing import List, Literal, Optional

from google import genai
from google.genai import types
from pydantic import BaseModel, Field


MODEL = os.environ.get("CLASSIFIER_MODEL", "gemini-2.5-flash")


LayerTag = Literal[
    "foundations",
    "execution-shell",
    "coordination",
    "tool-interface",
    "memory",
    "observation-eval",
    "permissions",
    "intent",
    "transactional-agency",
    "supply-chain",
    "red-team",
    "oversight",
    "architectures",
    "out-of-scope",
]

SprsTag = Literal["security", "privacy", "reliability", "safety"]

OpenProblemTag = Literal[
    "transactional-agency",
    "least-privilege-reasoning",
    "intent-to-constraints",
    "observability-attribution",
    "long-horizon-eval",
]


class Classification(BaseModel):
    """Structured classification result for a single paper."""

    keep: bool = Field(
        description=(
            "True only if the paper makes a substantive contribution to engineering "
            "trustworthy agentic systems (the operational stack). False for pure "
            "model-side, capability-only, or off-topic work."
        )
    )
    harness_layer: LayerTag = Field(
        description=(
            "The primary harness layer (structural facet). Use 'out-of-scope' when keep is false."
        )
    )
    sprs: List[SprsTag] = Field(
        description=(
            "The system guarantee(s) this work serves (guarantee facet). One or two "
            "values when keep is true. Empty list when keep is false."
        ),
    )
    open_problems: List[OpenProblemTag] = Field(
        default_factory=list,
        description=(
            "Zero to two of the white paper's open research problems this work bears on. "
            "Leave empty if none apply."
        ),
    )
    confidence: float = Field(
        description=(
            "Confidence in this keep/tag decision, 0.0 to 1.0. Lower it when the abstract "
            "is ambiguous about systems-engineering substance or facet assignment."
        ),
    )
    summary: str = Field(
        description=(
            "One-sentence summary of the technical contribution and why it matters "
            "for the chosen layer. Plain English, no marketing words."
        ),
    )
    reason: str = Field(
        description=(
            "One short sentence justifying the keep/skip decision. Be specific."
        ),
    )


SYSTEM_PROMPT = """\
You are an editorial classifier for `awesome-trustworthy-agentic-systems`, a curated map of research on engineering trustworthy AI agents *as systems* — not as isolated models.

The list's thesis: trustworthiness is not a property of model outputs alone. Failures in agentic systems happen in the full operational stack — orchestration logic, tool interfaces, memory, permissions, workflows, and human oversight. Engineering trustworthy agents is therefore a *systems* problem, not just a *model* problem.

Your job: read a paper's title, authors, venue, and abstract; decide whether it belongs on this list; and if so, assign two facets — the harness layer (where in the stack) and the SPRS guarantee(s) (what property it serves) — plus any open-research-problem tags and a confidence.

# Editorial bar

A paper is IN SCOPE if and only if it makes a substantive contribution to engineering trustworthy *agentic systems* — the operational stack on top of model inference. That includes:
- orchestration logic (planners, multi-agent composition, reviewer roles)
- tool interfaces and tool-use security
- agent memory (RAG integrity, episodic memory, context-window trust boundaries)
- permissions and authorization at the agent-action layer
- transactional semantics for probabilistic actions (rollback, checkpointing, idempotence)
- observation, tracing, and runtime evaluation of agent behavior
- adversarial testing of multi-step agent workflows
- supply-chain security for AI-generated code and agent software
- human oversight at scale (review cognitive load, escalation, governance)
- reference architectures and operational postmortems

A paper is OUT OF SCOPE if it is primarily about:
- pure model-side alignment or safety training (RLHF, constitutional AI, debate, reward modeling)
- capability papers ("our new agent framework does X better") with no systems-engineering content
- generic NLP, LLM benchmarking, or evaluation on static text tasks
- vendor whitepapers, marketing pieces, position papers without technical methodology
- pre-LLM agent / RL papers with no connection to modern agentic systems
- workshop posters, abstracts, or short-form pieces without methodology

The list is read by both ML/agent builders and academic researchers in security, systems, software engineering, and AI. The bar is substance + systems angle, not popularity.

When in doubt, skip. A tight editorial bar protects the list's credibility — false negatives can be re-added by a contributor, false positives erode trust.

# Facet 1 — harness layer (structural)

Use ONE of these layer tags (kebab-case) for `harness_layer`. For keep=false, use `out-of-scope`.

1. `foundations` — Mental models, surveys, taxonomies of agentic-system risks; cross-community framing of the agent-as-system problem; the translation gap between ML, systems, security, and SE.
2. `execution-shell` — The runtime that turns model calls into an agent: sandboxing, isolation, state machines, retry logic, turn control.
3. `coordination` — Multi-agent composition, planner/executor separation, specialist/reviewer roles, agent-to-agent routing, workflow graphs.
4. `tool-interface` — Tool calling, MCP servers, browser/filesystem/code-executor interfaces, API integrations treated as trust boundaries. Includes tool-injection threats and tool-schema design.
5. `memory` — RAG, episodic and long-term agent memory, context-window management, memory poisoning defenses, distinguishing system-input from external-input in context.
6. `observation-eval` — Logging, tracing, replay, regression testing, adversarial evaluation, production monitoring for agent behavior.
7. `permissions` — Least privilege for reasoning systems: plan-aware authorization, contextual permissions, dynamic trust boundaries, capability-based security for agents.
8. `intent` — Intent compilation: translating natural-language goals into machine-checkable constraints before the agent acts.
9. `transactional-agency` — Checkpointing, rollback, compensation, idempotence, journaling of agent actions.
10. `supply-chain` — Build/CI/release security for agent software, SBOM for prompt+model+tools, AI-generated code provenance, packaging hygiene.
11. `red-team` — Adversarial testing of agentic systems: prompt injection, exploit chaining across tools, multi-turn attacks evaluated as system-level threats.
12. `oversight` — Human-in-the-loop at scale, review cognitive load, checkpoint design, escalation policies.
13. `architectures` — End-to-end reference designs, real-world deployment case studies, postmortems with systems detail.

A paper may touch several layers — pick the *primary* one for `harness_layer`.

# Facet 2 — SPRS guarantee (what property)

Assign one or two `sprs` values: the system guarantee(s) the work primarily serves. This is orthogonal to the layer.

- `security` — constraining agent behavior within authorized boundaries; defending against adversaries (injection, exploit chains, privilege escalation, supply-chain compromise).
- `privacy` — protecting sensitive information as agents retrieve, process, and generate data (leakage, memorization, context exfiltration, access to sensitive knowledge).
- `reliability` — stability and consistency of long-running workflows under failure or uncertainty (recovery, rollback, evaluation of correctness, reproducibility).
- `safety` — preventing harmful real-world outcomes from agent actions (unsafe tool use, harmful side effects, governance of consequential actions).

Pick the guarantee the contribution most directly advances. Most red-team/permissions/supply-chain work is `security`; transactional-agency and evaluation work is usually `reliability`; oversight and harmful-action work is usually `safety`; data-leakage and least-privilege-to-knowledge work is `privacy`. Use two only when the contribution genuinely serves both.

# Optional — open research problems

Add zero to two `open_problems` tags when the work bears on one of the white paper's open problems:
- `transactional-agency` — checkpointing, rollback, compensation, recovery for multi-step side effects.
- `least-privilege-reasoning` — context- and intent-dependent access, including to internal knowledge.
- `intent-to-constraints` — translating natural-language intent into enforceable constraints.
- `observability-attribution` — instrumentation of actions and reasoning states for debugging and governance.
- `long-horizon-eval` — trajectory- and workflow-level evaluation beyond static benchmarks.

# Output rules

- `harness_layer`: the single primary layer (or `out-of-scope` when keep=false).
- `sprs`: one or two guarantees when keep=true; empty list when keep=false.
- `open_problems`: zero to two, only when they genuinely apply.
- `confidence`: 0.0–1.0. Lower it when the abstract is ambiguous about systems-engineering substance or when facet assignment is a judgment call. The reviewer triages low-confidence drafts first.
- `summary`: the actual technical contribution and which harness-layer concern it addresses, one sentence, plain technical English, no marketing words.
- `reason`: one short sentence justifying keep/skip. Be specific.
- If you cannot tell from the abstract whether the paper qualifies, default to skip with a reason explaining the ambiguity.

# Worked examples

## Example 1 — keep, supply-chain
Title: "Vulnerabilities in AI-Authored Code: A Large-Scale Study of Copilot Commits"
Abstract: We analyze 10,000 commits authored by GitHub Copilot across 500 public repositories and find that 12% contain insecure dependency suggestions, including 41 instances of typosquatted-package imports. We propose CopilotGuard, a CI-side scanner that flags AI-introduced dependencies for human review before merge.
Classification:
- keep: true
- harness_layer: supply-chain
- sprs: [security]
- open_problems: []
- confidence: 0.9
- summary: Empirical study of insecure dependency suggestions in 10,000 AI-authored commits and a CI-side scanner that intercepts them at review time.
- reason: Direct contribution to agent supply-chain security with a deployable build-pipeline mitigation.

## Example 2 — skip, out-of-scope
Title: "Improved Reward Modeling for Mathematical Reasoning"
Abstract: We propose a new reward modeling approach combining chain-of-thought consistency signals with verifiable-reward bootstrapping. On GSM8K our method improves accuracy by 4.2 points over PPO baselines.
Classification:
- keep: false
- harness_layer: out-of-scope
- sprs: []
- open_problems: []
- confidence: 0.92
- summary: New reward modeling approach for math chain-of-thought accuracy on GSM8K.
- reason: Pure model-level training improvement with no agentic-systems engineering content.

## Example 3 — keep, permissions
Title: "Plan-Time Authorization for LLM Agents: Capability Tokens Bound to Reasoning Traces"
Abstract: We introduce a capability-based authorization model in which an LLM agent must produce a verifiable plan before acquiring tool tokens. Tokens are scoped to the plan's declared actions and revoked on deviation. We evaluate on three production agent harnesses, catching 23 of 25 unauthorized tool calls.
Classification:
- keep: true
- harness_layer: permissions
- sprs: [security, privacy]
- open_problems: [least-privilege-reasoning]
- confidence: 0.88
- summary: Capability-based authorization model that binds tool access tokens to verified agent plans, evaluated on three production harnesses against a red-team suite.
- reason: Directly addresses plan-aware least privilege — a core open problem for trustworthy agent permissions — with concrete experimental validation.

## Example 4 — skip, capability-only
Title: "AutoOrchestrator: A New Multi-Agent Framework for Software Engineering Tasks"
Abstract: We present AutoOrchestrator, a multi-agent system that orchestrates planner, coder, reviewer, and tester agents. On HumanEval-Plus, AutoOrchestrator achieves 87% pass@1, outperforming GPT-4 single-agent by 12 points.
Classification:
- keep: false
- harness_layer: out-of-scope
- sprs: []
- open_problems: []
- confidence: 0.85
- summary: Multi-agent framework for software-engineering tasks with HumanEval-Plus benchmark gains.
- reason: Pure capability paper — no trust, safety, governance, or systems-engineering contribution to the agentic stack.

## Example 5 — keep, red-team
Title: "Workflow-Level Exploit Chains in Multi-Agent Systems: An Adversarial Study"
Abstract: We construct adversarial multi-agent workflows in which each step passes its local safety check yet the composition produces a globally unsafe outcome. Across six frameworks we demonstrate exploit chains — data exfiltration via memory-write chains, unauthorized API calls via reviewer-bypass — and propose workflow-invariant checking as a defense.
Classification:
- keep: true
- harness_layer: red-team
- sprs: [security]
- open_problems: [long-horizon-eval]
- confidence: 0.9
- summary: Demonstrates workflow-level exploit chains that bypass per-step guardrails across six agent frameworks and proposes invariant checking as a deployable defense.
- reason: System-level adversarial study with concrete defense mechanism — squarely in agent red-teaming.

## Example 6 — keep, memory
Title: "Memory Poisoning via Adversarial Retrieval: Attacks and Provenance-Based Defenses"
Abstract: We show that long-running agents with retrieval-augmented memory are vulnerable to memory poisoning: an attacker who can write to any document the agent later retrieves can inject persistent malicious instructions. We propose provenance-tagging memory entries so the agent can distinguish system-input from externally-sourced content.
Classification:
- keep: true
- harness_layer: memory
- sprs: [security, privacy]
- open_problems: [observability-attribution]
- confidence: 0.87
- summary: Characterizes a memory-poisoning attack surface on RAG-backed agents and proposes provenance-tagging to distinguish trusted from external memory content.
- reason: Directly addresses memory integrity and trust-boundary confusion with an attack/defense pair on real deployments.

## Example 7 — skip, benchmark-only
Title: "Long-Context Retrieval Augmented Generation Across 1M Tokens"
Abstract: We benchmark several retrieval strategies for 1M-token contexts and report retrieval accuracy gains of 3-7 points across five QA datasets.
Classification:
- keep: false
- harness_layer: out-of-scope
- sprs: []
- open_problems: []
- confidence: 0.9
- summary: Benchmark of retrieval strategies for long-context RAG with accuracy gains on five QA datasets.
- reason: Retrieval benchmarking only — no integrity, poisoning, trust-boundary, or systems-engineering angle.

## Example 8 — keep, observation-eval
Title: "TraceAgent: Replay and Regression Testing for Production LLM Agent Workflows"
Abstract: TraceAgent captures full execution traces of production LLM agents and replays them against new versions to detect regressions, with a workflow-level diff. Deployed at a fintech company, it caught 14 production-impacting regressions over six months.
Classification:
- keep: true
- harness_layer: observation-eval
- sprs: [reliability]
- open_problems: [long-horizon-eval, observability-attribution]
- confidence: 0.9
- summary: Trace-capture and replay system for production LLM agents with workflow-level regression diffing, validated by six months of fintech deployment.
- reason: Concrete observation and regression-testing infrastructure for production agent systems with measurable deployment impact.

## Example 9 — skip, vendor-marketing
Title: "Introducing AgentCloud: Enterprise-Ready Agent Infrastructure"
Abstract: AgentCloud is our new managed platform for deploying LLM agents, with our proprietary safety filter, our RoboPolicy permissions engine, and scalable serving.
Classification:
- keep: false
- harness_layer: out-of-scope
- sprs: []
- open_problems: []
- confidence: 0.93
- summary: Vendor announcement of a managed agent-deployment platform with proprietary safety and permissions components.
- reason: Marketing piece — no technical methodology, no evaluation, no reproducible contribution.

## Example 10 — keep, transactional-agency
Title: "Compensable Agents: Transactional Semantics for Long-Running Tool Sequences"
Abstract: We model agent tool sequences as long-running transactions with compensation actions. On failure mid-sequence the runtime executes compensations in reverse to roll back observable state. 89% of incidents in our 200-case corpus roll back cleanly vs 12% under per-call retry.
Classification:
- keep: true
- harness_layer: transactional-agency
- sprs: [reliability]
- open_problems: [transactional-agency]
- confidence: 0.91
- summary: Transactional middleware for agent tool sequences with compensation-based rollback, evaluated against a 200-case failure corpus.
- reason: Direct contribution to transactional agency — one of the open engineering problems for trustworthy agents — with concrete experimental validation.

Now classify the paper provided by the user in the next message. Return only the structured Classification — do not include extra prose.
"""


def classify(
    title: str,
    abstract: str,
    authors: List[str],
    venue: Optional[str] = None,
) -> Classification:
    """Classify one paper. Returns a validated Classification.

    The system prompt is large and stable across all calls in a sweep run,
    so Gemini's implicit prefix caching kicks in automatically — per-call
    cost drops to cached-token pricing after the first call. No explicit
    cache markers required.
    """
    client = genai.Client()  # reads GEMINI_API_KEY from environment

    venue_line = f"\nVenue: {venue}" if venue else ""
    if authors:
        if len(authors) > 6:
            authors_line = ", ".join(authors[:6]) + " et al."
        else:
            authors_line = ", ".join(authors)
    else:
        authors_line = "(unknown)"

    user_content = (
        f"Title: {title}\n"
        f"Authors: {authors_line}{venue_line}\n\n"
        f"Abstract:\n{abstract}"
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=user_content,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=Classification,
            temperature=0.0,
            # gemini-2.5-flash is a thinking model: its reasoning tokens count
            # against max_output_tokens and were truncating the JSON (parse
            # failures). Disable thinking for this classification task and give
            # the structured output ample room. (gemini-2.5-pro cannot fully
            # disable thinking — raise the budget to >=128 there instead.)
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            max_output_tokens=1500,
        ),
    )

    parsed = response.parsed
    if parsed is None:
        raise RuntimeError(
            f"Classification parsing failed for paper: {title[:80]!r}; "
            f"response_text={response.text!r}"
        )
    return parsed
