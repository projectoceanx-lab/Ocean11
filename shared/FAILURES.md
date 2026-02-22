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

### 2026-02-18 — Ocean 🌊 — NDR Safe-Probe Verification Failed on Everflow+Proxy Path
**What happened:** Two live verification attempts (`--safe-submit-probe --offer-id 4905`) failed before guard assertion due to route instability: one timed out on `Page.goto` to NDR after Everflow redirect; another hit a page variant where expected debt dropdown selector was not visible in time.
**Root cause:** Combined Everflow redirect chain + proxy defaults from `.env` introduced non-deterministic page state for this verification window.
**Impact:** ~10-15 minutes delay before runtime safety proof was captured.
**Lesson:** Validate safety guards in a deterministic harness first (direct destination, controlled env), then layer attribution/proxy complexity as a separate check.
**Prevention:** Use direct-entry probe command with proxy env vars blanked for guard verification, then run Everflow/proxy path checks as secondary reliability testing.

### 2026-02-18 — Ocean 🌊 — NDR Test Run Created Prospect (Interception Bypass)
**What happened:** During a test intended to validate Step 2 submit behavior without burning a lead, the NDR flow executed a real `POST /details?...` and redirected to `/personalizesavings` with a generated `prospectId`.
**Root cause:** We used a DOM `submit` event interceptor, but NDR’s JS submit path performs logic that bypassed that control. We blocked at the wrong layer.
**Impact:** One QA-data prospect record appears to have been created on NDR side. Time cost: additional validation + incident documentation. Reputational/compliance risk is low-to-medium because test data was synthetic, but this is still an avoidable live-side effect.
**Lesson:** For external forms with JS-managed submission, only network-level route blocking (or fully mocked transport) is trustworthy for "no-submit" tests.
**Prevention:** Route-level blocking for `POST /details` is now implemented in `scripts/fdr-ndr-fill.py` via `--safe-submit-probe` (NDR-only), plus regression matcher tests in `tests/test_fdr_ndr_submit_guard.py` to protect against accidental guard drift.

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
