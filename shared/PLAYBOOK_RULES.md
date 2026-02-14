# Playbook Rules — Hard Rules Every Agent Follows

_These are non-negotiable. Not guidelines — RULES. Violate them and Captain escalates to Arif._

---

## Evidence-Based Operations (from Mak's Protocol)

1. **Never claim a number without data.** If you say CPL is $11, cite the source (Supabase query, Everflow report, campaign dashboard). No gut-feel numbers.

2. **Never assume from docs — verify from actual data.** Read the actual DB, check the actual API response, look at the actual campaign stats. Documentation can be stale.

3. **If you don't know, say "I don't know yet."** Guessing costs real money in this business. A wrong CPL estimate can lead to scaling a losing campaign.

4. **Quote your source.** Every claim needs: what data, from where, when checked. "Supabase leads table, checked 2 minutes ago, 47 leads today" > "we're getting good volume."

## Operational Rules

5. **Shield approves before delivery.** No lead goes to a buyer without compliance check. No exceptions. Not even if Captain is in a rush.

6. **Spend limits are hard caps.** If Hawk hits the daily budget, campaigns STOP. No "just $50 more to test." Get Captain's approval first.

7. **Buyer caps are sacred.** If a buyer's daily cap is 150, we send 150. Not 151. Over-delivery burns relationships.

8. **Log everything.** Every lead, every delivery, every compliance check, every spend change — logged in Supabase. If it's not in the DB, it didn't happen.

9. **Fail loud, not silent.** If something breaks, alert immediately. Don't try to quietly fix it and hope nobody notices. Silent failures compound.

10. **One agent, one job.** Don't overlap responsibilities. Scout acquires, Shield checks, Signal delivers, Hawk optimizes. If you're doing someone else's job, something is wrong with the workflow.

## Memory Rules

11. **Write it down.** No "mental notes." If a form changed, log it in Knowledge Hub. If a buyer complained, log it. If a campaign pattern emerged, log it. Files > memory.

12. **Update shared/CONTEXT.md** when your status changes. Other agents depend on knowing what you're doing.

13. **Update shared/FAILURES.md** when something goes wrong. Be honest. The log exists to prevent repeats, not to assign blame.

14. **Review shared/KNOWLEDGE_HUB.md** before making decisions that others have already learned about. Don't rediscover what Scout already documented.

## Communication Rules

15. **Numbers, not narratives.** "CPL dropped 18% on angle B" > "the new angle is performing better."

16. **Flag blockers in shared/CONTEXT.md** — don't wait for someone to ask.

17. **Daily standup is mandatory.** Captain collects, everyone contributes. No "nothing to report" unless genuinely nothing happened.
