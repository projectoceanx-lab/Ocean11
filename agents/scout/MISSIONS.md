# Scout — Active Missions

## 🎯 Phase 1 Objectives

### Lead Acquisition
- [ ] Operate stealth browser (built by Peter) with proxy rotation
- [ ] Identify and map 10+ debt relief lead forms
- [ ] Run form-filling automation for top 5 buyer forms
- [ ] Achieve 80%+ quality score on enriched leads
- [ ] Implement dedup checking against existing DB

### Lead Delivery (NEW — owns full pipeline)
- [ ] Deliver enriched, qualified leads to buyers via form filling
- [ ] Route leads to correct buyer based on debt profile + caps
- [ ] Track delivery status: submitted → accepted/rejected
- [ ] Monitor buyer acceptance rates — flag drops >20%
- [ ] Respect cap limits: stop at 1.5x cap safety buffer
- [ ] Log every delivery attempt in Supabase deliveries table

### Enrichment & Scoring
- [ ] Run FastDebt enrichment on every lead (Peter builds the API integration)
- [ ] Score leads: A/B/C/D tier based on debt type, amount, employment
- [ ] Filter: only unsecured CC/personal loan debt qualifies

## 📋 Lead Quality Scoring Criteria
- **A-tier (80-100):** Verified income, confirmed debt $10K+, employed, valid contact
- **B-tier (60-79):** Partial verification, debt $5K+, contact valid
- **C-tier (40-59):** Minimal verification, debt amount unclear
- **D-tier (0-39):** Unverified, likely low value — flag for review

## 🚧 Blockers
- None yet

## 📝 Notes
- Always check DB before inserting — no duplicate leads
- Rotate proxies every 5-10 requests minimum
- Log every form submission attempt (success or fail)

## Standing Order (Every Session)
Before closing: update shared/CONTEXT.md, memory/YYYY-MM-DD.md, and shared/KNOWLEDGE_HUB.md per shared/PLAYBOOK_RULES.md § MANDATORY CHECKPOINTS. No exceptions.
