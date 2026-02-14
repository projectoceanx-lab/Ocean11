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

## 3. Antfarm by Ryan Carson

_Referenced in MEMORY.md. Deterministic YAML workflows with verification gates. Step-by-step pipelines. (Detailed source pending.)_

## 4. SHIELD.md by Thomas Roccia

_Referenced in MEMORY.md. Per-agent security policies, allowed/blocked actions, threat matching. (Detailed source pending.)_

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
