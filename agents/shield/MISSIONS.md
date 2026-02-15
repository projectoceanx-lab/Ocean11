# Shield — Active Missions

## 🎯 Phase 1 Objectives

### Compliance (Core Mandate)
- [ ] Review every lead before delivery for TSR compliance
- [ ] Implement state-level regulation checks (NY, CA, TX, FL high priority)
- [ ] Map all 50 states: licensing requirements for debt relief lead gen
- [ ] Verify TCPA consent for any call-based delivery
- [ ] Ensure all email communications are CAN-SPAM compliant
- [ ] Maintain compliance pass rate logs for audit trail
- [ ] Flag any lead with missing required disclosures
- [ ] Review ALL ad copy (Hawk) and landing page copy (Forge) before launch

### Agent Security & Access Control (New Mandate)
- [ ] Define and enforce agent access matrix (who can read/write which DB tables)
- [ ] Audit agent actions: flag any agent accessing data outside its scope
- [ ] Credential security: verify all secrets are in .env, never in committed files or logs
- [ ] Review agent tool permissions: each agent should only use tools it needs
- [ ] Flag unauthorized access attempts in compliance_log
- [ ] Quarterly access review: are agent permissions still appropriate?

### Buyer Vetting (Pre-Delivery Gate)
- [ ] Vet every buyer's fee structure before first delivery (advance fee ban)
- [ ] Verify buyer licensing in their operating states
- [ ] Check buyer against FTC enforcement history
- [ ] Document buyer compliance status in buyers table (compliance_notes)
- [ ] Re-vet buyers quarterly or on any flagged incident

## 📋 Compliance Check Sequence
1. **TSR Check** — Telemarketing Sales Rule requirements met?
2. **State Rules** — State-specific debt relief regulations?
3. **TCPA** — Proper consent for calls/texts?
4. **CAN-SPAM** — Email opt-out mechanism present?
5. **Data Accuracy** — Lead info internally consistent?
6. **Buyer Eligibility** — Is this buyer vetted and clear?

## 📋 Security Audit Checklist
1. **Agent scope** — Is each agent only accessing its authorized tables?
2. **Credential exposure** — Any secrets in logs, commits, or shared files?
3. **Tool permissions** — Any agent using tools outside its mandate?
4. **Data leakage** — PII appearing where it shouldn't (logs, shared context)?
5. **External access** — Any unauthorized API calls or browser sessions?

## 🚧 Blockers
- State licensing map not started yet
- Buyer vetting can't start until buyers are identified (Step 7)

## 📝 Notes
- **Shield has VETO power** — no agent can override a compliance block
- When in doubt, BLOCK. Better to lose a lead than face a fine.
- Every check must be logged in compliance_log with reason
- Shield reviews Hawk's ad copy, Forge's landing pages, Captain's buyer outreach
- Agent access violations are treated as Critical — immediate escalation to Captain + Arif

## Standing Order (Every Session)
Before closing: update shared/CONTEXT.md, memory/YYYY-MM-DD.md, and shared/KNOWLEDGE_HUB.md per shared/PLAYBOOK_RULES.md § MANDATORY CHECKPOINTS. No exceptions.
