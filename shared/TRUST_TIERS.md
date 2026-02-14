# TRUST_TIERS.md — Decision Authority Framework

_Who can decide what, without asking whom._

---

## Tier 1: Autonomous (Agent decides, logs it)

Low risk. Agents execute without approval. Results logged for review.

| Agent | Autonomous Actions |
|-------|-------------------|
| **Scout** | Fill forms, check duplicates, run enrichment, score leads, hand to Shield |
| **Shield** | Run compliance checks, pass/flag/block leads, log results |
| **Hawk** | Pull campaign metrics, analyze CPL/ROI, run A/B tests (within existing budget) |
| **Signal** | Deliver leads to existing buyers within caps, send scheduled emails, log deliveries |
| **Watchtower** | Monitor all systems, log anomalies, send low/medium severity alerts to Captain |

**Rule:** If the action is within the agent's defined scope, uses no additional budget, and doesn't touch external relationships — do it.

---

## Tier 2: Captain Review (Agent proposes, Captain approves)

Medium risk. Agent prepares the action, Captain reviews before execution.

| Action | Who Proposes | Captain Decides |
|--------|-------------|-----------------|
| Budget shift < 20% between campaigns | Hawk | Yes/No |
| Increase delivery volume to existing buyer | Signal | Yes/No |
| New lead source or form to target | Scout | Yes/No |
| Compliance edge case (flag, not clear block/pass) | Shield | Yes/No |
| Pause or kill a campaign | Hawk | Yes/No |
| Watchtower high-severity alert | Watchtower | Triage + assign |
| Re-route leads due to buyer issue | Signal | Yes/No |

**Rule:** If the action affects money, buyer relationships, or compliance grey areas — Captain reviews.

---

## Tier 3: AK Approval (Captain recommends, AK decides)

High risk. Captain prepares analysis and recommendation. AK has final say.

| Action | Captain Prepares | AK Decides |
|--------|-----------------|------------|
| New buyer onboarding | Due diligence + terms proposal | Approve/Reject |
| Budget shift > 20% or new budget allocation | Analysis + recommendation | Approve/Reject |
| Daily spend exceeding $500 | ROI justification | Approve/Reject |
| New vertical (tax debt, student loans, etc.) | Market analysis + compliance review | Approve/Reject |
| New traffic channel or platform | Cost/benefit analysis | Approve/Reject |
| Infrastructure spend (Supabase Pro, new tools) | Cost justification | Approve/Reject |
| Any legal or regulatory decision | Shield's assessment + Captain's recommendation | Approve/Reject |
| Model changes for any agent | Cost/capability comparison | Approve/Reject |
| External communications to buyers | Draft + context | Approve/Send |

**Rule:** If it involves new money, new relationships, new risk, or anything that can't be easily reversed — AK decides.

---

## Escalation Path

```
Agent → Captain → AK
  ↑                ↓
  └── Feedback ────┘
```

- **Normal flow:** Agent acts autonomously (Tier 1) or proposes to Captain (Tier 2)
- **Escalation:** Captain escalates to AK when Tier 3 criteria are met
- **Emergency:** Watchtower can alert AK directly ONLY for Critical severity (system down, compliance breach, runaway spend)
- **Override:** AK can override any decision at any tier. Captain can override Tier 1 agent decisions.

---

## Trust Evolution

Trust tiers are not permanent. As agents prove reliability:

- **Promotion:** Consistent accuracy over 2+ weeks → agent gets more Tier 1 autonomy
- **Demotion:** Error or bad judgment → action moves up a tier (more oversight)
- **Review cycle:** Captain reviews tier assignments weekly during standup

_Example: If Hawk's budget recommendations are profitable 90%+ of the time for 2 weeks, budget shifts up to 30% could move to Tier 1._

---

_Updated: Feb 14, 2026. Tiers evolve as the operation matures._
