# Failure Patterns

Capture recurring failures and convert them into hard rules.

## Pattern FP-001: Hype Claim
- Symptom: "guaranteed", "erase debt", "instant approval" style language.
- Effect: compliance block risk, trust damage.
- Action: block and rewrite with soft certainty ("may", "could", "results vary").

## Pattern FP-002: Multi-CTA Drift
- Symptom: two or more CTA intents in one asset.
- Effect: lower clarity and conversion quality.
- Action: enforce single-CTA lint failure.

## Pattern FP-003: Vanity Hook, Low Intent
- Symptom: high clicks, near-zero qualified clicks or lead starts.
- Effect: poor downstream economics.
- Action: rewrite hooks to qualify intent earlier.

## Pattern FP-004: Missing Compliance Footer (Email)
- Symptom: footer missing address/unsubscribe/disclosure.
- Effect: CAN-SPAM risk.
- Action: auto-fail preflight for email channel.

## Pattern FP-005: Government Program Implication
- Symptom: wording implies government endorsement/program.
- Effect: FTC/Impersonation risk.
- Action: immediate block and add phrase to blocked set.
