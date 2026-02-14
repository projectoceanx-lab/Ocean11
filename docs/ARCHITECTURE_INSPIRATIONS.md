# Architecture Inspirations — Research Notes

_Sources studied for Project Ocean's 4-layer hybrid architecture._

---

## 1. VoxYZ by @Voxyz_ai

**What it is:** 6 AI agents running as an autonomous content/business system, live 24/7.

**Agents:**
- **Brain** — Core reasoning/strategy (cannot post tweets, cannot self-approve)
- **Xalt** — Execution agent (cannot approve itself)
- **Sage** — Methodology/knowledge
- **Scout** — Research/discovery
- **Observer** — Reviews outputs, quality control
- Plus additional agents in the system

**Key Architecture Patterns:**

1. **Closed-Loop Autonomy** — Agents run continuously without human input. In one observed instance, Xalt and Sage argued about methodology for 7 rounds, then Scout jumped in and they converged on a task orchestration plan — zero human input.

2. **Role Cards with Hard Bans** — Every agent has a role card defining scope, external actions, and resources. Hard limits on what each agent can touch. "Bans > skills" — what agents CAN'T do matters more than what they can.

3. **Kill Switches Per Layer** — Every layer has a kill switch. Critical actions like `post_tweet` and `deploy` never auto-approve.

4. **Cap Gates** — Reject bad proposals automatically. Spend limits, volume limits.

5. **Reaction Matrix / Triggers** — Event-based handoffs between agents. Staleness detection triggers recovery.

6. **Self-Healing** — Stale tasks auto-recover. "The system heals itself" via mechanical heartbeat patterns.

7. **Model Diversity** — Uses different models per agent (Claude Opus 4.5, GPT-5.3, Gemini 3 Pro). "Same model and they all start sounding the same. Model diversity matters as much as prompt diversity."

8. **Observer Pattern** — Dedicated observer agent reviews outputs from other agents.

**Live dashboard:** https://www.voxyz.space/stage

**Key quote:** "giving AI agents 'free will' is easy. the hard part is deciding what they're never allowed to touch."

---

## 2. Mission Control by @pbteja1998 (Bhanu Teja P)

**What it is:** Squad of 10 autonomous OpenClaw agents led by Jarvis, built as a SaaS product (MissionControlHQ).

**Architecture:**

1. **Jarvis as Orchestrator** — Lead agent coordinates the squad. Runs on beefed-up instance (16 vCPU/30GB RAM). 24/7 persistent.

2. **Thread-Based Collaboration** — "Each task or activity is a thread that agents can subscribe to." Agents collaborate, review, and refute each other's work within threads.

3. **Telegram Integration** — Users chat with Jarvis/squad via Telegram for onboarding and commands. Group chats for collaboration.

4. **Custom Dashboard** — Kanban mission queue, task details, activity feed, memories, rate/budget limits. Real-time sync. Initially vibe-coded by Jarvis itself.

5. **Workflow Pattern:** User sets mission → Jarvis coordinates → Agents self-task, collaborate/review/refute → High output (e.g., full marketing plans) → Human reviews/executes.

6. **Dynamic Squad** — Squad composition is dynamic, not fixed. Agents are provisioned based on need.

7. **Integrations:** SuperMemory (shared context across agents), AutoSendEmail.

8. **SaaS Deployment:** 1-click setup → Auto-provision server → Telegram onboarding → Dashboard access. No terminal needed. Fully managed.

9. **Built on OpenClaw** — Uses Claude LLMs. BYOK (bring your own key) for Claude. Tried Fly.io Sprites, switched to VPS.

**Key insight:** The "abundance problem" — agents produce so much output that human review/execution becomes the bottleneck, not agent capability.

---

## 3. Antfarm by Ryan Carson (@ryancarson)

**What it is:** Open-source multi-agent framework. Agents run deterministic workflows as "teams" for real work.

**Source:** https://x.com/ryancarson/status/2020931274219594107 | https://www.antfarm.cool/

**Key Architecture Patterns:**

1. **Workflow-Driven Agents** — You define workflows, then invoke them. The system breaks tasks into atomic user stories, then agents execute autonomously in a loop ("Ralph loop" — agents poll every 30 seconds for new work).

2. **Deterministic Pipelines** — Workflows define the steps. Same input, same steps, same order. Not hoping agents coordinate loosely — the pipeline is explicit.

3. **Self-Defining Agents** — The framework "defines its own agents and only starts crons once you invoke a workflow." Agents spin up on demand.

4. **Multi-Agent Teams** — Designed for "teams of agents" doing real work: security audits on large codebases (~$38-100), shipping startup features, PRD generation, code reviews.

5. **Open Source** — Democratize agent productivity. Claims 5x+ output leverage. Ryan uses it with Amp/OpenClaw for his own startup.

**Key insight:** Workflows are the backbone. Agents are the executors. The workflow doesn't hope agents will figure it out — it tells them exactly what to do, step by step.

---

## 4. SHIELD.md by Thomas Roccia (@fr0gger_)

**What it is:** A context-based runtime security policy standard for AI agents. Think of it as a threat feed that agents check before every action.

**Source:** https://x.com/fr0gger_/status/2020025525784514671 | https://nova-hunting.github.io/shield.md/

**Key Architecture Patterns:**

1. **Threat-Object Driven Decisions** — Every threat has: id, fingerprint, category, severity, confidence, action, and lifecycle metadata. Agents match events against active threats before acting.

2. **Three Enforcement States Only:**
   - `block` — Stop immediately. Do not proceed.
   - `require_approval` — Ask human. Wait.
   - `log` — Continue normally, record the event.
   - No other actions allowed. Simplicity is the point.

3. **Decision Block Before Every Action** — Before any tool call, network request, secret access, skill install, or MCP interaction, the agent must output a Decision block first. Then act.

4. **Strongest Match Wins** — If multiple threats match: block > require_approval > log. Escalation is automatic.

5. **Threat Categories:** prompt injection, tool abuse, MCP compromise, memory poisoning, supply chain attacks, vulnerability exploitation, fraud, policy bypass, anomaly, malicious skills.

6. **Confidence Thresholds** — If confidence >= 0.85, enforce. Below 0.85, default to require_approval unless it's critical severity + block action.

7. **Context Limits** — Cap active threats to 25 entries. Only load what's needed for the current task. Don't overflow the context window.

8. **Hard Stop Rule** — If action = block: no tools, no network, no secrets, no skills. Stop immediately.

9. **v0 is Guidance, v1 is Enforcement** — Current v0 is context-loaded (the model reads the policy). v1 moves enforcement outside the LLM — making it authoritative, not advisory.

**Key quote from Roccia:** "The idea is to create a standard for agent security, similar to the concept of agents.md."

**Key insight for Ocean:** Shield's compliance checks are our version of SHIELD.md's threat matching. Every lead goes through a decision flow (pass/flag/block) before any action. The three-state model (pass/flag/block) directly mirrors SHIELD.md's (log/require_approval/block).

---

## How Ocean Uses These Patterns

| Pattern | Source | Ocean Implementation |
|---------|--------|---------------------|
| Deterministic pipelines | Antfarm | YAML workflows in `workflows/` |
| Closed-loop autonomy | VoxYZ | Agents run via heartbeats, self-coordinate |
| Kill switches / hard bans | VoxYZ | Shield veto power, budget caps per agent |
| Role cards | VoxYZ | SOUL.md per agent with explicit scope |
| Model diversity | VoxYZ | 4 different models across 6 agents |
| Reaction matrix / triggers | VoxYZ | Agent notifications trigger downstream workflows |
| Self-healing | VoxYZ | Watchtower monitors + auto-recovery |
| Thread collaboration | Mission Control | Agent-to-agent notifications in workflows |
| Dashboard observability | Mission Control | Daily standup + P&L tracking |
| Built-in tensions | Ocean original | Hawk vs Shield, Signal vs Hawk by design |
| Cap gates | VoxYZ | Daily budget caps, spend limits per agent |

---

_Updated: Feb 14, 2026_
