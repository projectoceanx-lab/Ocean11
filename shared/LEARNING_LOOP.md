# Learning Loop — Supervised Reinforcement System

_Agents don't just execute. They learn. Every action has an outcome, every outcome has a score, every score updates behavior._

---

## How It Works

```
ACTION → OUTCOME → SCORE → FEEDBACK → BEHAVIOR UPDATE
```

### 1. Before Acting: Check History
Every agent MUST read before executing:
- `shared/FAILURES.md` — Don't repeat mistakes
- `shared/KNOWLEDGE_HUB.md` — Use what others learned
- `shared/FEEDBACK_LOG.md` — Check scores on similar past actions

### 2. During Action: Log Intent
Before executing, write to `shared/ACTION_LOG.md`:
```
### [TIMESTAMP] — [AGENT] — [ACTION_ID]
**Intent:** What I'm about to do and why
**Expected outcome:** What success looks like
**Risk:** What could go wrong
**Precedent:** Similar past action and its score (if any)
```

### 3. After Action: Log Outcome
After executing, update the same entry:
```
**Actual outcome:** What actually happened
**Delta:** Difference between expected and actual
**Self-score:** 1-5 (1=failed, 3=acceptable, 5=exceeded)
```

### 4. Fury Reviews: Supervised Score
Fury reviews outcomes and assigns:
```
**Fury score:** 1-5
**Feedback:** What to do differently
**Promote?:** YES → moves to KNOWLEDGE_HUB | NO → stays in log
**New rule?:** YES → Fury adds to PLAYBOOK_RULES | NO
```

### 5. Behavior Update
Based on scores:
- **Score 5 (Excellent):** Pattern promoted to KNOWLEDGE_HUB.md → all agents learn it
- **Score 4 (Good):** Logged, agent continues approach
- **Score 3 (Acceptable):** Logged with improvement notes
- **Score 2 (Poor):** Logged in FAILURES.md, agent must adjust approach
- **Score 1 (Failed):** Logged in FAILURES.md, Fury may add PLAYBOOK_RULE to prevent recurrence

## Reward Signals

| Agent | Positive Reward | Negative Reward |
|-------|----------------|-----------------|
| **Scout** | Lead accepted by buyer (+2), High quality score (+1) | Lead rejected (-2), Form detection/block (-1), Bad data (-3) |
| **Shield** | Caught real compliance issue (+2), Clean audit (+1) | Missed violation (-5), False positive blocking good lead (-1) |
| **Hawk** | CPL below target (+2), Profitable campaign (+3) | Overspend (-3), Scaling losing campaign (-5) |
| **Signal** | Buyer accepts delivery (+2), High connect rate (+1) | Buyer complaint (-3), Email bounce >2% (-2) |
| **Watchtower** | Caught issue before impact (+3), Clean health check (+1) | Missed outage (-4), False alarm (-1) |

## Cumulative Agent Scores

_Updated weekly by Fury. Trend matters more than absolute number._

| Agent | This Week | Last Week | Trend | Trust Tier |
|-------|-----------|-----------|-------|------------|
| Scout | — | — | — | Probation (new) |
| Shield | — | — | — | Probation (new) |
| Hawk | — | — | — | Probation (new) |
| Signal | — | — | — | Probation (new) |
| Watchtower | — | — | — | Probation (new) |

### Trust Tiers (earned, not assigned)
- **Probation** — New agent. Every action reviewed by Fury. No autonomy.
- **Supervised** — 1 week clean. Fury reviews daily summary, not every action.
- **Trusted** — 2 weeks clean, score avg >3.5. Fury reviews weekly. Agent can act autonomously within guardrails.
- **Autonomous** — 4 weeks clean, score avg >4.0. Minimal oversight. Can suggest PLAYBOOK_RULE changes.

### Demotion Triggers
- Any Score 1 → drop one tier
- Two Score 2s in a week → drop one tier
- PLAYBOOK_RULE violation → immediate Probation
- Compliance miss (Shield) → immediate Probation + full audit

## Weekly Review Protocol

Every Sunday, Fury runs:
1. Tally scores per agent from ACTION_LOG + FEEDBACK_LOG
2. Update cumulative scores above
3. Promote/demote trust tiers
4. Move top patterns to KNOWLEDGE_HUB.md
5. Move failures to FAILURES.md with prevention rules
6. Archive the week's ACTION_LOG entries
7. Brief Arif on agent performance

## Anti-Patterns (auto-flag)

These behaviors trigger automatic review:
- **Repeat failure** — Same mistake twice → Fury reviews immediately
- **Score inflation** — Agent self-scores 5 but Fury scores 2 → recalibrate
- **Knowledge ignorance** — Agent makes mistake that KNOWLEDGE_HUB already covered → -2 penalty
- **Silent failure** — Agent doesn't log an outcome → immediate Probation
- **Rule dodge** — Agent finds loophole in PLAYBOOK_RULES → Fury patches rule + feedback
