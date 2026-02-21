# Debt Lead Funnel QA Checklist

Use this before any paid traffic push.

## A) Content & Claim Safety
- [ ] No guaranteed savings/debt elimination claims
- [ ] No fake urgency or misleading countdowns
- [ ] Clear statement that results vary
- [ ] Contact info + business identity visible

## B) Form & Consent
- [ ] Required fields only (min friction)
- [ ] Phone/email formats validated
- [ ] Consent checkbox/copy consistent with policy
- [ ] Consent captured and stored with timestamp/IP

## C) Tracking
- [ ] UTM capture working
- [ ] Click ID / subID persists through form submit
- [ ] Conversion fires once only
- [ ] Test lead appears in destination system

## D) Routing & Buyer Delivery
- [ ] Cap reached behavior tested
- [ ] Reject handling does not drop lead silently
- [ ] Retry or backup buyer path works
- [ ] Delivery latency acceptable (<10 sec target)

## E) Mobile Reality Check
- [ ] iPhone Safari tested
- [ ] Android Chrome tested
- [ ] Form can be completed one-handed
- [ ] CTA remains visible without awkward scrolling

## F) Day-1 Decision Rules
- [ ] Pause if CPL > target by 30% for 2+ hours
- [ ] Pause if approval rate < baseline by 25%
- [ ] Duplicate rate threshold defined
- [ ] Creative/angle swap plan prepared

## Sign-off
- Operator: __________________
- Date/Time: ________________
- Final status: PASS / PASS WITH RISK / FAIL
