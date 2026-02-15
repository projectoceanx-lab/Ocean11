# Failure Log — Learn or Repeat

_Every failure gets logged here with root cause and lesson. If we make the same mistake twice, we didn't learn._

---

## Format

```
### [DATE] — [AGENT] — Short Title
**What happened:** What went wrong
**Root cause:** Why it happened (dig deep — "it broke" is not a root cause)
**Impact:** What it cost us (dollars, leads lost, time wasted, reputation damage)
**Lesson:** What we do differently now
**Prevention:** Specific change made (config, workflow, rule) to prevent recurrence
```

## Failures

### 2026-02-14 — Shield 🛡️ — PRE-LAUNCH INTEL: Critical Compliance Risks from FTC Enforcement Review
**What happened:** Pre-launch research identified 3 high-severity compliance risks based on 2024-2025 FTC enforcement patterns in debt relief.
**Root cause:** These are industry risks, not our failures. Logging preventively so we never become a case study.
**Impact:** If ignored, any of these could result in FTC action, TRO, asset freeze, and total business shutdown. Recent cases show $30M-$100M+ in exposure.
**Lesson:** Three non-negotiable compliance gates before we go live:
1. **Buyer advance fee verification** — Every buyer must certify in writing they do not charge advance fees (TSR §310.4(a)(5)). No certification = no delivery. Period. (See: Strategic Financial Solutions, Accelerated Debt cases)
2. **Landing page / ad copy audit** — Zero tolerance for: specific debt reduction percentages, guaranteed timelines, impersonation of banks/creditors/government, or targeting language that singles out veterans/seniors. (See: Accelerated Debt — $100M scheme shut down for exactly this)
3. **DNC + TCPA consent architecture** — Must be built BEFORE first call-based delivery. Consent language must name specific entities, not "marketing partners." Timestamp + IP logging from day one. (See: Accelerated Debt DNC violations)
**Prevention:** Shield will not approve first lead delivery until all three gates are verified and documented. This is non-negotiable per SOUL.md veto authority.

<!-- The goal isn't zero failures. It's zero REPEATED failures. -->
