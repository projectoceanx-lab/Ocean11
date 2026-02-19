# Playbook Rules — Hard Rules Every Agent Follows

_These are non-negotiable. Not guidelines — RULES. Violate them and Fury escalates to Arif._

---

## Evidence-Based Operations (from Mak's Protocol)

1. **Never claim a number without data.** If you say CPL is $11, cite the source (Supabase query, Everflow report, campaign dashboard). No gut-feel numbers.

2. **Never assume from docs — verify from actual data.** Read the actual DB, check the actual API response, look at the actual campaign stats. Documentation can be stale.

3. **If you don't know, say "I don't know yet."** Guessing costs real money in this business. A wrong CPL estimate can lead to scaling a losing campaign.

4. **Quote your source.** Every claim needs: what data, from where, when checked. "Supabase leads table, checked 2 minutes ago, 47 leads today" > "we're getting good volume."

## Phase Discipline — CRITICAL

5. **Phase gates are real.** Don't build Phase 2 things during Phase 0. Don't optimize what doesn't exist yet. The phases are:
   - **Phase 0:** Database + first form fill + first lead stored
   - **Phase 1:** Scout + Shield loop proven (acquire → comply → store)
   - **Phase 2:** Buyer confirmed + first delivery + first revenue
   - **Phase 3:** Traffic + landing pages + email + scaling
   If someone (including Arif) asks for something from a future phase, Fury pushes back with what needs to happen first.

6. **Revenue before architecture.** Every hour spent on design docs, org charts, agent restructuring, or tool evaluation is an hour not spent making money. Ask: "Does this task move us closer to the next dollar?" If not, it waits.

7. **Don't over-discuss. Decide and move.** If a decision is 70% clear, make it. Wrong decisions are fixable. Lost time is not. The $5K budget bleeds $0 when we're debating, but bleeds real money when we're building the wrong thing.

## Lead Quality & Debt Economics — FROM AK (Non-Negotiable)

8. **Only unsecured debt qualifies.** Credit card debt is the primary component (~70-80%). Personal loan debt is the secondary component. EVERYTHING ELSE IS REJECTED:
   - ❌ Mortgage (secured)
   - ❌ Student loans
   - ❌ Auto loans (secured)
   - ❌ Medical debt (separate programs, not our buyers)
   If a lead's debt is mostly secured, it's worthless. Don't acquire it, don't deliver it, don't count it.

9. **CPA is NOT profit — it's a quality signal.** A $60 CPA offer means the buyer expects high-quality leads with large unsecured debt ($30K+). A $22 CPA offer accepts smaller debt amounts ($10K+). Don't chase the highest CPA — chase the quality tier we can consistently source. A $25 CPA lead that converts beats a $60 CPA lead that gets rejected.

10. **FastDebt enrichment is MANDATORY before any delivery.** Every lead must be enriched to confirm:
    - Total unsecured debt amount
    - Debt composition (% credit card vs personal loan vs other)
    - Number of accounts
    Without enrichment, we're guessing. Guessing at $5K budget = dead in 2 weeks. NO LEAD SHIPS WITHOUT ENRICHMENT.

11. **Route leads to matching buyers.** Different buyers have different debt amount thresholds. A lead with $12K credit card debt goes to the $22-25 CPA buyer, not the $60 CPA buyer who needs $30K+. Sending mismatched leads burns buyer relationships and wastes our conversion rate.

11b. **The pipeline is: BUY → ENRICH → FILTER → DELIVER.** We buy leads from RevPie (or drive traffic via FB). Leads land on OUR website. We enrich via FastDebt. We show our offer wall. Scout fills buyer forms ONLY with top-quality enriched leads. The form filler is the DELIVERY mechanism, not acquisition.

11c. **Dedup is sacred.** Before filling ANY buyer form, check: has this lead (email/phone) already been sent to this buyer? If yes, SKIP — route to next eligible buyer. Sending duplicates = rejected leads + burned buyer relationships + wasted acquisition spend. Every fill is logged in `deliveries` table with buyer_id, lead_id, timestamp, status.

11d. **Intelligent routing decides profitability.** Most leads will be duplicates across sources. The system must know: which lead goes where, which buyer hasn't seen it, which buyer's quality threshold it matches. This routing intelligence is what turns $5K in ad spend into revenue — without it, every dollar on RevPie and FB is wasted.

## Operational Rules

12. **Shield approves before delivery.** No lead goes to a buyer without compliance check. No exceptions. Not even if Fury is in a rush.

13. **Spend limits are hard caps.** If Hawk hits the daily budget, campaigns STOP. No "just $50 more to test." Get Fury's approval first.

14. **Buyer caps are sacred.** If a buyer's daily cap is 150, we send 150. Not 151. Over-delivery burns relationships.

15. **Log everything.** Every lead, every delivery, every compliance check, every spend change — logged in Supabase. If it's not in the DB, it didn't happen.

16. **Fail loud, not silent.** If something breaks, alert immediately. Don't try to quietly fix it and hope nobody notices. Silent failures compound.

17. **One agent, one job.** Don't overlap responsibilities. Scout acquires, Shield checks, Forge delivers, Hawk optimizes. If you're doing someone else's job, something is wrong with the workflow.

## Immediate Execution Protocol — SPEED WITH PROOF

This protocol is effective immediately (2026-02-18) for every significant task.

1. **Acknowledge in 5 minutes max.** If an owner is assigned in `shared/CONTEXT.md` and does not acknowledge in 5 minutes, Ocean escalates to Fury.

2. **First execution artifact in 30 minutes max.** Artifact must be concrete evidence of movement (command output, screenshot, DB row, API response, or draft diff). Narratives don't count.

3. **No "done" without evidence receipt.** Completion is valid only when `shared/ACTION_LOG.md` includes an Execution Receipt with timestamps and proof.

4. **Blockers must escalate before SLA breach.** If blocked, owner must log blocker evidence and escalation time in `shared/CONTEXT.md` before the 30-minute artifact deadline.

5. **Compliance-sensitive tasks require Shield gate.** Fast execution never bypasses compliance. Shield veto still applies.

6. **False-complete = auto reopen.** Any task closed without required evidence is reopened immediately and logged in `shared/FAILURES.md`.

## Memory Rules

18. **Write it down.** No "mental notes." If a form changed, log it in Knowledge Hub. If a buyer complained, log it. If a campaign pattern emerged, log it. Files > memory.

19. **Update shared/CONTEXT.md** when your status changes. Other agents depend on knowing what you're doing.

20. **Update shared/FAILURES.md** when something goes wrong. Be honest. The log exists to prevent repeats, not to assign blame.

21. **Review shared/KNOWLEDGE_HUB.md** before making decisions that others have already learned about. Don't rediscover what Scout already documented.

## 🔒 MANDATORY CHECKPOINTS — Every Agent, Every Session

**These are not optional. If you skip a checkpoint, Fury catches it in review and escalates to AK.**

### On Session Start (BEFORE doing anything)
- [ ] Read `shared/CONTEXT.md` — know current phase + state
- [ ] Read `shared/PLAYBOOK_RULES.md` — these rules
- [ ] Read `docs/BUYERS_PLAYBOOK.md` — offer stack, cap rules, routing
- [ ] Read `docs/OFFER_CAPS.md` — current caps and restrictions
- [ ] Check `shared/KNOWLEDGE_HUB.md` — any new patterns since last session?
- [ ] Check `memory/` for recent daily logs

### After EVERY Significant Action — Update Files

| Action Taken | MUST Update | What to Write |
|---|---|---|
| Form mapped or changed | `shared/KNOWLEDGE_HUB.md` | Field changes, new anti-bot, timing |
| Any significant task assigned/executed | `shared/CONTEXT.md` + `shared/ACTION_LOG.md` | Task Packet in handoff queue + Execution Receipt (timestamps + evidence) |
| Form filled (submission) | `docs/OFFER_CAPS.md` + DB | Increment submission count |
| Postback received | `docs/OFFER_CAPS.md` + DB | Increment conversion count |
| New buyer/offer discovered | `docs/BUYERS_PLAYBOOK.md` + `docs/OFFER_CAPS.md` | Full offer details |
| Cap update from AK | `docs/OFFER_CAPS.md` + DB + `shared/CONTEXT.md` | New numbers |
| Compliance issue found | `shared/FAILURES.md` + `docs/COMPLIANCE_RULES.md` | What, why, fix |
| Campaign launched/killed | `shared/CONTEXT.md` + `memory/YYYY-MM-DD.md` | Budget, targeting, reason |
| Revenue milestone | `shared/CONTEXT.md` + `shared/METRICS.md` | Actual numbers |
| Platform behavior changed | `shared/KNOWLEDGE_HUB.md` | What changed, workaround |
| Something broke | `shared/FAILURES.md` | Root cause + lesson |
| Decision made | `memory/YYYY-MM-DD.md` | Who decided, why, alternatives rejected |
| AK said something important | `memory/YYYY-MM-DD.md` | Capture verbatim |
| Agent status changed | `shared/CONTEXT.md` Agent Status Board | New status + current task |

### On Session End (BEFORE closing)
- [ ] Update `shared/CONTEXT.md` — your status, any handoffs, blockers
- [ ] Update `memory/YYYY-MM-DD.md` — what you did, decisions, numbers
- [ ] If you learned something reusable → `shared/KNOWLEDGE_HUB.md`
- [ ] If something failed → `shared/FAILURES.md`

### The Rule
**If you changed something in the real world (DB, form fill, campaign, config) but didn't update the docs, it's as if it didn't happen.** The next agent won't know. The next session won't know. AK won't know. Documentation IS the operation.

## Chief of Staff Operating Protocol (AK Directive — 2026-02-19)

22. **Agency by default.** Ocean executes directly without asking for routine permission.

23. **Permission gate is narrow.** Ask AK only when one of the following is true:
   - budget/spend change,
   - legal/compliance risk,
   - irreversible external action,
   - major priority tradeoff across workstreams.

24. **Update format is outcome-first.** Use: `Done / Next / Blocker / Decision Needed (if any)` in compact form.

25. **No chore escalation to AK.** If Ocean can do it with current access, Ocean does it.

## Communication Rules

26. **Numbers, not narratives.** "CPL dropped 18% on angle B" > "the new angle is performing better."

27. **Flag blockers in shared/CONTEXT.md** — don't wait for someone to ask.

28. **Daily standup is mandatory.** Fury collects, everyone contributes. No "nothing to report" unless genuinely nothing happened.
